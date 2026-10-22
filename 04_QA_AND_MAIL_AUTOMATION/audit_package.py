import os, sys, re, json, zipfile, hashlib, subprocess, tempfile

def audit_package(pkg_dir):
    rm_path = os.path.join(pkg_dir, "README.md")
    zips = [f for f in os.listdir(pkg_dir) if f.endswith(".zip")]
    assert len(zips) == 1, f"Expected 1 zip file, found {zips}"
    z_path = os.path.join(pkg_dir, zips[0])

    rm_bytes = open(rm_path, "rb").read()
    assert b"\r\n" not in rm_bytes, "CRLF found in outer README.md"
    rm_sha = hashlib.sha256(rm_bytes).hexdigest()
    rm_text = rm_bytes.decode("utf-8")

    with zipfile.ZipFile(z_path, "r") as zf:
        names = zf.namelist()
        assert "README.md" in names and "fix.patch" in names, "Missing README.md or fix.patch in ZIP"
        z_rm_bytes = zf.read("README.md")
        assert hashlib.sha256(z_rm_bytes).hexdigest() == rm_sha, "Outer and inner README.md mismatch"

        for name in names:
            data = zf.read(name)
            assert b"\r\n" not in data, f"CRLF found in {name}"
            for bad in (b"# REPO:", b"# PATH:", b"# HTML_URL:"):
                assert bad not in data, f"Scanner header {bad} found in {name}"
            if name.endswith(".json"):
                json.loads(data.decode("utf-8"))

        patch_text = zf.read("fix.patch").decode("utf-8").strip()
        diff_blocks = re.findall(r"```diff\n(.*?)\n```", rm_text, flags=re.S)
        assert diff_blocks and diff_blocks[-1].strip() == patch_text, "README diff block != fix.patch"

        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["git", "init", "-q"], cwd=tmp, check=True)
            for name in names:
                full = os.path.join(tmp, name)
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, "wb") as f:
                    f.write(zf.read(name))
                if name.startswith("workflows/"):
                    gh_full = os.path.join(tmp, ".github", name)
                    os.makedirs(os.path.dirname(gh_full), exist_ok=True)
                    with open(gh_full, "wb") as f:
                        f.write(zf.read(name))
            for m_path in re.findall(r"^--- a/(.+)$", patch_text, flags=re.M):
                dest = os.path.join(tmp, m_path)
                if not os.path.exists(dest):
                    base = os.path.basename(m_path)
                    for cand in (f"src/{base}", f"workflows/{base}", base):
                        if cand in names:
                            os.makedirs(os.path.dirname(dest), exist_ok=True)
                            with open(dest, "wb") as f:
                                f.write(zf.read(cand))
                            break
            subprocess.run(["git", "apply", "--check", "fix.patch"], cwd=tmp, check=True)

    print(f"[100% PASS] {os.path.basename(pkg_dir)} | README={len(rm_bytes)}B ({rm_sha[:12]}) | ZIP={os.path.getsize(z_path)}B")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(target, "README.md")):
        audit_package(target)
    else:
        for d in sorted(os.listdir(target)):
            p = os.path.join(target, d)
            if os.path.isdir(p) and os.path.exists(os.path.join(p, "README.md")):
                audit_package(p)
