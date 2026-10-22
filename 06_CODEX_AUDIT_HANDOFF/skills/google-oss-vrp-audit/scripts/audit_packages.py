"""Passive report-package QA. Never executes archived code or patches originals."""
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess
import tempfile
import urllib.request
import zipfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    p = pathlib.PurePosixPath(name)
    return bool(name) and not p.is_absolute() and not re.match(r"^[A-Za-z]:", name) and ".." not in p.parts and "\\" not in name


def read_zip(path):
    with zipfile.ZipFile(path) as z:
        names = [e.filename for e in z.infolist()]
        if len(set(names)) != len(names):
            raise ValueError("Duplicate ZIP entry names")
        if any(not safe_name(n) for n in names):
            raise ValueError("Unsafe ZIP path")
        if sum(e.file_size for e in z.infolist()) > 100_000_000:
            raise ValueError("Archive exceeds audit size limit")
        if any((e.external_attr >> 16) & 0o170000 == 0o120000 for e in z.infolist()):
            raise ValueError("ZIP symlink entry")
        return {e.filename: z.read(e) for e in z.infolist() if not e.is_dir()}


def github_refs(text):
    pat = r"https://github\.com/([^/\s`]+)/([^/\s`]+)/blob/([0-9a-fA-F]{40})/([^\s`\)<>#]+)(?:#L(\d+)(?:-L(\d+))?)?"
    return [dict(repo=f"{m[0]}/{m[1]}", commit=m[2], path=m[3], start=int(m[4]) if m[4] else None, end=int(m[5] or m[4]) if m[4] else None) for m in re.findall(pat, text)]


def source_candidates(name, refs):
    base = pathlib.PurePosixPath(name).name
    matches = [r for r in refs if pathlib.PurePosixPath(r['path']).name == base]
    if '/' in name and name.split('/')[0] not in ('src', 'workflows'):
        prefix = name.split('/')[0]
        matches = [r for r in matches if r['repo'].split('/')[1] == prefix]
    unique = {(r['repo'], r['commit'], r['path']): r for r in matches}
    if not unique and name.startswith('workflows/'):
        repo_commits = {(r['repo'], r['commit']) for r in refs}
        if len(repo_commits) == 1:
            repo, commit = next(iter(repo_commits))
            unique[(repo, commit, '.github/'+name)] = dict(repo=repo, commit=commit, path='.github/'+name, inferred=True)
    # For multi-repository dossiers each top-level directory identifies the repository.
    if not unique and '/' in name and name.split('/')[0] not in ('src', 'workflows'):
        prefix = name.split('/')[0]
        repo_commits = {(r['repo'], r['commit']) for r in refs if r['repo'].split('/')[1] == prefix}
        if len(repo_commits) == 1:
            repo, commit = next(iter(repo_commits))
            unique[(repo, commit, '.github/workflows/'+base)] = dict(repo=repo, commit=commit, path='.github/workflows/'+base, inferred=True)
    return list(unique.values())


def fetch(ref, cache):
    url = f"https://raw.githubusercontent.com/{ref['repo']}/{ref['commit']}/{ref['path']}"
    target = cache / (sha(url.encode()) + '.raw')
    if not target.exists():
        request = urllib.request.Request(url, headers={'User-Agent': 'Passive-Report-QA'})
        with urllib.request.urlopen(request, timeout=35) as response:
            target.write_bytes(response.read())
    return url, target.read_bytes()


def patch_check(files, patch):
    paths = re.findall(r'^--- (?:a/)?([^\t\r\n]+)', patch.decode('utf-8'), re.M)
    if not paths or not re.search(br'^@@ ', patch, re.M):
        return dict(status='FAIL', reason='Not a complete unified diff')
    mapping = {}
    with tempfile.TemporaryDirectory(prefix='vrp-patch-') as tmp:
        tree = pathlib.Path(tmp)
        for path in paths:
            if path == '/dev/null':
                continue
            if not safe_name(path):
                return dict(status='FAIL', reason='Unsafe patch path', path=path)
            candidates = [n for n in files if n == path or n.endswith('/'+path)]
            if not candidates:
                candidates = [n for n in files if pathlib.PurePosixPath(n).name == pathlib.PurePosixPath(path).name]
            if len(candidates) != 1:
                return dict(status='UNVERIFIED', reason='Base file mapping not unique', path=path, candidates=candidates)
            source = candidates[0]
            dst = tree / path
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(files[source])
            mapping[path] = source
        patch_path = tree / 'input.patch'
        patch_path.write_bytes(patch)
        env = __import__('os').environ.copy()
        env['GIT_CONFIG_NOSYSTEM'] = '1'
        result = subprocess.run(['git', '-c', 'core.autocrlf=false', 'apply', '--check', str(patch_path)], cwd=tree, env=env, capture_output=True, text=True, timeout=20)
        return dict(status='PASS' if result.returncode == 0 else 'FAIL', exit_code=result.returncode, output=result.stderr.strip(), mapping=mapping)


def audit(folder, cache, network):
    readme = (folder / 'README.md').read_bytes()
    zips = list(folder.glob('*.zip'))
    if len(zips) != 1:
        raise ValueError(f'Expected one ZIP, found {len(zips)}')
    files = read_zip(zips[0])
    text = readme.decode('utf-8-sig')
    refs = github_refs(text)
    result = dict(profile=folder.name, folder=str(folder), readme_bytes=len(readme), readme_sha256=sha(readme), zip_sha256=sha(zips[0].read_bytes()), readme_identical=files.get('README.md') == readme, outside_crlf=readme.count(b'\r\n'), entries=[], source_checks=[], reference_ranges=[], excerpt_checks=[], evidence_json=[], run_ids=sorted(set(re.findall(r'actions/runs/(\d+)', text))))
    for name, data in files.items():
        markers = []
        decoded = data.decode('utf-8', errors='replace')
        for i, line in enumerate(decoded.splitlines(), 1):
            if re.match(r'\s*(?:#|//|<!--)\s*(?:REPO|PATH|HTML_URL)\s*:|\s*#\s*Generated by scanner', line, re.I):
                markers.append(i)
        result['entries'].append(dict(name=name, bytes=len(data), sha256=sha(data), crlf=data.count(b'\r\n'), bare_cr=data.count(b'\r')-data.count(b'\r\n'), scanner_marker_lines=markers))
        if name.endswith('.json'):
            try:
                value = json.loads(data)
                result['evidence_json'].append(dict(name=name, valid=True, keys=list(value) if isinstance(value, dict) else None))
            except (ValueError, UnicodeDecodeError) as error:
                result['evidence_json'].append(dict(name=name, valid=False, error=str(error)))
    blocks = re.findall(r'^```diff[^\n]*\n(.*?)^```', text, re.M|re.S)
    patch = files.get('fix.patch')
    result['patch'] = dict(present=patch is not None, readme_diff_blocks=len(blocks))
    if patch is not None:
        result['patch'].update(bytes=len(patch), sha256=sha(patch), block_matches=any(b.rstrip('\n') == patch.decode('utf-8').rstrip('\n') for b in blocks))
        result['patch']['apply_check'] = patch_check(files, patch)
    fetched = {}
    if network:
        for name, data in files.items():
            if not name.endswith(('.yml', '.yaml', '.py', '.sh', '.js', '.ts')):
                continue
            candidates = source_candidates(name, refs)
            if len(candidates) != 1:
                result['source_checks'].append(dict(name=name, status='UNVERIFIED', candidates=candidates))
                continue
            ref = candidates[0]
            try:
                url, remote = fetch(ref, cache)
                fetched[(ref['repo'], ref['commit'], ref['path'])] = remote
                result['source_checks'].append(dict(name=name, status='PASS' if remote == data else 'FAIL', url=url, path_inferred=bool(ref.get('inferred')), local_sha256=sha(data), remote_sha256=sha(remote), line_count=len(remote.splitlines())))
            except Exception as error:
                result['source_checks'].append(dict(name=name, status='UNVERIFIED', ref=ref, error=str(error)))
        for ref in refs:
            try:
                key = (ref['repo'], ref['commit'], ref['path'])
                if key not in fetched:
                    _, fetched[key] = fetch(ref, cache)
                count = len(fetched[key].splitlines())
                valid = ref['start'] is None or 1 <= ref['start'] <= ref['end'] <= count
                result['reference_ranges'].append(dict(**ref, bounds_valid=valid, line_count=count))
            except Exception as error:
                result['reference_ranges'].append(dict(**ref, error=str(error)))
        # Check each non-elision segment exactly; elided excerpts are not a verbatim block.
        for match in re.finditer(r'^```(?:yaml|yml|python|py)[^\n]*\n(.*?)^```', text, re.M|re.S):
            block = match.group(1)
            pieces = re.split(r'^\s*\.\.\.\s*\n', block, flags=re.M)
            exact = []
            for piece in pieces:
                piece = piece.rstrip('\n')
                if not piece.strip():
                    continue
                sources = [f'{key[0]}@{key[1]}:{key[2]}' for key, value in fetched.items() if piece in value.decode('utf-8-sig')]
                exact.append(dict(matches=sources, lines=len(piece.splitlines())))
            result['excerpt_checks'].append(dict(readme_line=text.count('\n', 0, match.start())+1, elided=len(pieces)>1, segments=exact, exact_segments=bool(exact) and all(x['matches'] for x in exact)))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=pathlib.Path)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    parser.add_argument('--cache', type=pathlib.Path, required=True)
    parser.add_argument('--fetch-upstream', action='store_true')
    parser.add_argument('--profiles', nargs='*', default=['02','03','04','05','06','07','08','09'])
    args = parser.parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    folders = [d for d in sorted(args.root.iterdir()) if d.is_dir() and d.name[:2] in args.profiles]
    if not folders:
        parser.error('No matching report folders; provide existing two-digit IDs using --profiles')
    def one(folder):
        try:
            return audit(folder, args.cache, args.fetch_upstream)
        except Exception as error:
            return dict(profile=folder.name, error=str(error))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(one, folders))
    output = dict(checked_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(), network_enabled=args.fetch_upstream, scope='Mechanical package QA; not a vulnerability/eligibility verdict', results=results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False)+'\n', encoding='utf-8', newline='\n')
    for r in results:
        print(r['profile'], 'ERROR='+r['error'] if 'error' in r else f"readme={r['readme_identical']} files={len(r['entries'])} patch={r['patch'].get('apply_check',{}).get('status')} upstream={sum(s['status']=='PASS' for s in r['source_checks'])}/{len(r['source_checks'])} excerpts={sum(s['exact_segments'] for s in r['excerpt_checks'])}/{len(r['excerpt_checks'])}")


if __name__ == '__main__':
    main()
