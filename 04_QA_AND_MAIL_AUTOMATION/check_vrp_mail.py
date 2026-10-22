import base64
import json
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(os.getenv("VRP_SUBMISSIONS_DIR", Path(__file__).resolve().parent))
STATE_FILE = ROOT / "vrp_mail_state.json"
REPORT_FILE = ROOT / "VRP_MAIL_TRACKER.md"

GWS_BIN = shutil.which("gws") or "gws"


def run_gws(args_list):
    proc = subprocess.run(
        [GWS_BIN] + args_list,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        return None
    out = proc.stdout
    idx = out.find("{")
    if idx == -1:
        return None
    try:
        return json.loads(out[idx:])
    except Exception:
        return None


def decode_part(body_data):
    if not body_data:
        return ""
    try:
        padded = body_data + "=" * (-len(body_data) % 4)
        return base64.urlsafe_b64decode(padded).decode("utf-8", errors="replace")
    except Exception:
        return ""


def extract_body(payload):
    if not payload:
        return ""
    mime = payload.get("mimeType", "")
    body_data = payload.get("body", {}).get("data")
    if mime == "text/plain" and body_data:
        return decode_part(body_data)
    parts = payload.get("parts", [])
    for p in parts:
        text = extract_body(p)
        if text:
            return text
    if body_data:
        return decode_part(body_data)
    return ""


def parse_issue_meta(subject, body_text):
    issue_m = re.search(r"issues/(\d+)|Reference Info:\s*(\d+)|Issue\s+(\d+)", subject + "\n" + body_text)
    issue_id = next((g for g in issue_m.groups() if g), "Unknown") if issue_m else "Unknown"
    comp_m = re.search(r"component:\s*(\d+)", body_text)
    status_m = re.search(r"status:\s*([^\r\n]+)", body_text)
    prio_m = re.search(r"priority:\s*([^\r\n]+)", body_text)
    sev_m = re.search(r"severity:\s*([^\r\n]+)", body_text)
    return {
        "issue_id": issue_id,
        "component": comp_m.group(1).strip() if comp_m else "-",
        "status": status_m.group(1).strip() if status_m else "-",
        "priority": prio_m.group(1).strip() if prio_m else "-",
        "severity": sev_m.group(1).strip() if sev_m else "-",
    }


def main():
    state = {"messages": {}, "last_checked": None}
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass

    query = "in:anywhere (buganizer-system@google.com OR bughunters@google.com OR issuetracker.google.com)"
    params = json.dumps({"userId": "me", "q": query, "includeSpamTrash": True, "maxResults": 30})
    listing = run_gws(["gmail", "users", "messages", "list", "--params", params])
    msgs = (listing or {}).get("messages", [])

    for item in msgs:
        msg_id = item["id"]
        if msg_id in state["messages"]:
            continue
        get_params = json.dumps({"userId": "me", "id": msg_id})
        detail = run_gws(["gmail", "users", "messages", "get", "--params", get_params])
        if not detail:
            continue
        headers = {h["name"].lower(): h["value"] for h in detail.get("payload", {}).get("headers", [])}
        subject = headers.get("subject", "(No Subject)")
        sender = headers.get("from", "")
        date_str = headers.get("date", "")
        snippet = detail.get("snippet", "")
        body = extract_body(detail.get("payload", {}))
        meta = parse_issue_meta(subject, body or snippet)
        state["messages"][msg_id] = {
            "id": msg_id,
            "internalDate": int(detail.get("internalDate", "0")),
            "date": date_str,
            "from": sender,
            "subject": subject,
            "snippet": snippet,
            "body": (body or snippet).strip(),
            **meta,
        }

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state["last_checked"] = now_str
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    sorted_msgs = sorted(state["messages"].values(), key=lambda x: x.get("internalDate", 0), reverse=True)
    issue_summary = {}
    for m in reversed(sorted_msgs):
        iid = m.get("issue_id", "Unknown")
        if iid == "Unknown":
            continue
        prev = issue_summary.get(iid, {})
        clean_subj = re.sub(r"^(Re:\s*)?Issue\s+\d+:\s*", "", m["subject"]).strip()
        issue_summary[iid] = {
            "title": prev.get("title") or clean_subj,
            "component": m["component"] if m["component"] != "-" else prev.get("component", "-"),
            "status": m["status"] if m["status"] != "-" else prev.get("status", "-"),
            "prio": f"{m['priority']} / {m['severity']}" if m["priority"] != "-" else prev.get("prio", "-"),
            "updated": m["date"],
        }

    table_rows = []
    for iid, info in issue_summary.items():
        table_rows.append(
            f"| [`{iid}`](https://issuetracker.google.com/issues/{iid}) | {info['title']} | `{info['component']}` | `{info['status']}` | `{info['prio']}` | {info['updated']} |"
        )

    lines = [
        "# 📬 Nhật Ký Theo Dõi Email Google VRP (`VRP_MAIL_TRACKER.md`)",
        "",
        f"- **Lần kiểm tra tự động gần nhất:** `{now_str}`",
        f"- **Tổng số email VRP/Buganizer đã ghi nhận:** `{len(sorted_msgs)}`",
        "",
        "## 1. Bảng Tổng Hợp Các Issue Đã Nộp",
        "| Issue ID | Hồ sơ / Tiêu đề | Component | Status | Priority / Severity | Cập nhật gần nhất |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
        *table_rows,
        "",
        "## 2. Chi Tiết Các Email Tự Động Thu Thập Từ Gmail",
        "",
    ]

    if not sorted_msgs:
        lines.append("*(Chưa có email mới nào trong hộp thư khớp bộ lọc `buganizer-system@google.com`)*")
    else:
        for m in sorted_msgs:
            lines.extend([
                f"### 📩 [{m['date']}] {m['subject']}",
                f"- **Issue:** `{m['issue_id']}` | **Component:** `{m['component']}` | **Status:** `{m['status']}` | **Priority/Severity:** `{m['priority']} / {m['severity']}`",
                f"- **From:** `{m['from']}`",
                "```text",
                m["body"][:2500],
                "```",
                "",
            ])

    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Checked at {now_str}: {len(sorted_msgs)} VRP messages recorded.")


if __name__ == "__main__":
    main()
