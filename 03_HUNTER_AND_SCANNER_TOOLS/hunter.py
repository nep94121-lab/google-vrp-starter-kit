import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
WORKFLOWS_DIR = BASE_DIR / "workflows"
REPORTS_DIR = BASE_DIR / "reports"
RULES_FILE = BASE_DIR / "rules" / "targets.json"

WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

UNTRUSTED_EXPR_PATTERNS = [
    r"github\.event\.issue\.title",
    r"github\.event\.issue\.body",
    r"github\.event\.pull_request\.title",
    r"github\.event\.pull_request\.body",
    r"github\.event\.comment\.body",
    r"github\.event\.review\.body",
    r"github\.event\.review_comment\.body",
    r"github\.event\.Discussion\.title",
    r"github\.event\.Discussion\.body",
    r"github\.event\.pages\..*\.page_name",
    r"github\.event\.commits\..*\.message",
    r"github\.event\.commits\..*\.author\.name",
    r"github\.event\.commits\..*\.author\.email",
    r"github\.event\.head_commit\.message",
    r"github\.event\.head_commit\.author\.name",
    r"github\.head_ref",
    r"github\.event\.pull_request\.head\.ref",
    r"github\.event\.pull_request\.head\.label",
    r"github\.event\.workflow_run\.head_branch",
    r"github\.event\.workflow_run\.head_commit\.message",
]


def gh_api(endpoint: str):
    cmd = ["gh", "api", endpoint]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if res.returncode != 0:
        return None
    try:
        return json.loads(res.stdout)
    except Exception:
        return None


def search_workflows_in_org(org: str, query_keyword: str, per_page: int = 15):
    """Search workflow files inside a Google organization using GitHub Code Search API."""
    q = f"{query_keyword} org:{org} path:.github/workflows language:YAML"
    endpoint = f"search/code?q={ subprocess.list2cmdline([q]).strip('\"').replace(' ', '+') }&per_page={per_page}"
    data = gh_api(endpoint)
    if not data or "items" not in data:
        return []
    return data["items"]


def download_workflow(item: dict) -> Path | None:
    repo_full = item["repository"]["full_name"]
    if item["repository"].get("fork") or item["repository"].get("archived"):
        return None
    file_path = item["path"]
    safe_name = f"{repo_full.replace('/', '__')}__{Path(file_path).name}"
    dest = WORKFLOWS_DIR / safe_name
    if dest.exists() and dest.stat().st_size > 0:
        return dest

    content_data = gh_api(f"repos/{repo_full}/contents/{file_path}")
    if not content_data or "download_url" not in content_data or not content_data["download_url"]:
        return None

    import urllib.request
    req = urllib.request.Request(content_data["download_url"], headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8", errors="ignore")

    header = f"# REPO: https://github.com/{repo_full}\n# PATH: {file_path}\n# HTML_URL: {item.get('html_url', '')}\n"
    dest.write_text(header + raw, encoding="utf-8")
    return dest


def analyze_workflow_custom(filepath: Path) -> list[dict]:
    """Deep custom AST/pattern analysis for exploitable Google VRP Supply Chain bugs."""
    text = filepath.read_text(encoding="utf-8", errors="ignore")
    findings = []

    lines = text.splitlines()
    repo_url = lines[0].replace("# REPO: ", "").strip() if lines and lines[0].startswith("# REPO:") else filepath.name
    html_url = lines[2].replace("# HTML_URL: ", "").strip() if len(lines) > 2 and lines[2].startswith("# HTML_URL:") else ""

    # 1. Check for pull_request_target + checkout of PR head
    has_prt = bool(re.search(r"^\s*pull_request_target\s*:", text, re.MULTILINE))
    if has_prt:
        checks_out_pr = bool(
            re.search(
                r"ref\s*:\s*\$\{\{\s*github\.event\.pull_request\.(head\.(sha|ref)|number|merge_commit_sha)",
                text,
                re.IGNORECASE,
            )
            or re.search(r"gh\s+pr\s+checkout", text)
        )
        if checks_out_pr:
            findings.append({
                "type": "GHA-01: Pwn Request Candidate (pull_request_target + PR Checkout)",
                "severity": "CRITICAL",
                "file": filepath.name,
                "repo": repo_url,
                "url": html_url,
                "detail": "Workflow triggers on pull_request_target and explicitly checks out the untrusted PR head/branch.",
            })

    # 2. Check for untrusted expression interpolation inside `run:` blocks
    try:
        docs = list(yaml.safe_load_all(text))
    except Exception:
        docs = []

    for doc in docs:
        if not isinstance(doc, dict):
            continue
        jobs = doc.get("jobs") or {}
        if not isinstance(jobs, dict):
            continue
        for job_name, job_data in jobs.items():
            if not isinstance(job_data, dict):
                continue
            steps = job_data.get("steps") or []
            if not isinstance(steps, list):
                continue
            for idx, step in enumerate(steps):
                if not isinstance(step, dict):
                    continue
                run_script = step.get("run")
                if isinstance(run_script, str):
                    for pat in UNTRUSTED_EXPR_PATTERNS:
                        matches = re.findall(r"\$\{\{\s*" + pat + r"[^}]*\}\}", run_script, re.IGNORECASE)
                        if matches:
                            findings.append({
                                "type": "GHA-02: Untrusted Expression Injection in `run:` script",
                                "severity": "HIGH",
                                "file": filepath.name,
                                "repo": repo_url,
                                "url": html_url,
                                "detail": f"Job '{job_name}' step #{idx+1} ('{step.get('name', 'unnamed')}') interpolates {matches} directly inside `run:` shell block.",
                            })

    return findings


def run_zizmor_audit() -> list[dict]:
    files = [str(f) for f in list(WORKFLOWS_DIR.glob("*.yml")) + list(WORKFLOWS_DIR.glob("*.yaml"))]
    if not files:
        return []
    cmd = ["zizmor", "--format", "json", "--min-severity", "medium"] + files
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    try:
        data = json.loads(res.stdout)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def main():
    orgs = ["google", "googleapis", "flutter", "angular", "tensorflow", "firebase", "google-gemini"]
    keywords = ["pull_request_target", "workflow_run", "issue_comment"]

    print("=== [1/3] Đang thu thập mẫu Workflows từ các tổ chức GitHub của Google ===")
    downloaded = []
    for org in orgs[:4]:
        for kw in keywords[:2]:
            print(f"  -> Quét org:{org} với từ khóa '{kw}'...")
            items = search_workflows_in_org(org, kw, per_page=8)
            for item in items:
                p = download_workflow(item)
                if p:
                    downloaded.append(p)
            time.sleep(2.5)  # Tránh chạm giới hạn tốc độ của GitHub Code Search API (10 req/phút)

    all_files = list(WORKFLOWS_DIR.glob("*.yml")) + list(WORKFLOWS_DIR.glob("*.yaml"))
    print(f"=== [2/3] Tổng số file Workflow đã tải về máy: {len(all_files)} files ===")

    custom_findings = []
    for f in all_files:
        custom_findings.extend(analyze_workflow_custom(f))

    print(f"=== [3/3] Đang chạy Zizmor Static Analyzer & Bộ lọc AST chuyên sâu ===")
    zizmor_findings = run_zizmor_audit()

    summary = {
        "total_workflows_scanned": len(all_files),
        "custom_ast_findings_count": len(custom_findings),
        "zizmor_high_findings_count": len(zizmor_findings),
        "custom_findings": custom_findings,
    }
    out_file = REPORTS_DIR / "initial_scan_results.json"
    out_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Hoàn tất! Đã lưu kết quả tại: {out_file}")
    print(f" - Phát hiện từ bộ lọc chuyên sâu (Custom AST): {len(custom_findings)}")
    print(f" - Phát hiện mức High/Critical từ Zizmor: {len(zizmor_findings)}")


if __name__ == "__main__":
    main()
