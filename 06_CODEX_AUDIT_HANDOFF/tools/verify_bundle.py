"""Check the portable handoff against its unsigned file manifest; no network."""
import hashlib
import json
import pathlib
import sys


def main():
    root = pathlib.Path(__file__).resolve().parents[1]
    manifest_path = root / 'MANIFEST.sha256.json'
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        failures = []
        names = set()
        for item in manifest['files']:
            name = item['path']
            rel = pathlib.PurePosixPath(name)
            if rel.is_absolute() or '..' in rel.parts or '\\' in name or ':' in name or name in names:
                failures.append({'path': name, 'error': 'unsafe or duplicate manifest path'})
                continue
            names.add(name)
            path = root / name
            if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root):
                failures.append({'path': name, 'error': 'missing, symlink or outside bundle'})
                continue
            data = path.read_bytes()
            if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                failures.append({'path': name, 'error': 'bytes or SHA-256 mismatch'})
        extra = sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p != manifest_path and p.relative_to(root).as_posix() not in names)
        print(json.dumps({'status': 'FAIL' if failures else 'PASS', 'checked_files': len(names), 'failures': failures, 'extra_files': extra, 'scope': 'Unsigned manifest integrity only'}, ensure_ascii=False, indent=2))
        return 1 if failures else 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
