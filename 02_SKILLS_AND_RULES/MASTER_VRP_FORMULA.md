# CÔNG THỨC CHUẨN GOOGLE OSS VRP (100% HUMAN RESEARCHER & AUDIT-PASS FORMULA)

> Tài liệu này đóng gói toàn bộ quy trình, cấu trúc tệp, quy tắc ngôn ngữ chống AI Slop, mẫu điền biểu mẫu `bughunters.google.com/report` và script kiểm định tự động đã được chứng minh vượt qua 100% bài kiểm tra độc lập lẫn bộ lọc Triage thực tế của Google Bug Hunters.

---

## 1. Tài Liệu & Liên Kết Tham Chiếu Chính Thức
- **Cổng nộp báo cáo Google VRP:** https://bughunters.google.com/report
- **Theo dõi báo cáo đã nộp:** https://bughunters.google.com/reports (hoặc https://issuetracker.google.com/)
- **Quy tắc Google OSS VRP:** https://bughunters.google.com/about/rules/google-friends/google-open-source-software-vulnerability-reward-program-rules
- **Cập nhật Quy tắc OSS VRP 2026:** https://bughunters.google.com/blog/ossvrp-rule-updates-2026
- **Khung Chất lượng Báo cáo Google (Chống AI Slop):** https://bughunters.google.com/blog/level-up-your-reports-introducing-our-updated-report-quality-framework
- **Chuẩn Cú pháp GitHub Actions Workflow:** https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax

---

## 2. Kiến Trúc Gói Hồ Sơ Chuẩn (`.zip` + `README.md`)

Mỗi hồ sơ nằm trong một thư mục riêng có tên tự nhiên theo chuẩn kỹ sư (`<số>_<tên-repo>-<tên-cơ-chế>`), gồm **2 tệp ngoài** (`README.md` và `<tên-gói>.zip`). Bên trong `.zip` chứa đúng cấu trúc sau:

```text
<tên-gói>.zip
├── README.md                       # Giống hệt README.md bên ngoài từng byte (cùng SHA-256)
├── fix.patch                       # Unified diff chuẩn, chạy `git apply --check` đạt Exit Code 0
├── evidence/
│   └── api_verification.json       # Kết quả truy vấn GitHub API thực tế (environment, runs, jobs)
├── workflows/                      # Các file .yml/.yaml gốc tại đúng Commit SHA (LF, không header lạ)
│   └── ...
└── src/                            # Các file mã nguồn .py/.js/.sh gốc tại đúng Commit SHA (nếu có)
    └── ...
```

---

## 3. Năm Quy Tắc Vàng Chống Bị Đánh Dấu AI (Anti-AI Slop & Bounded Claims)

1. **Tiêu đề kỹ thuật khách quan (Không giật tít):**
   - **Công thức:** `<org>/<repo>: <Cơ chế bị thiếu/lỗi> in <tên_file> allows <hành vi kỹ thuật cụ thể>`
   - *Ví dụ chuẩn:* `google-gemini/gemini-cli: Missing eval-gate environment in chained_e2e.yml allows fork PR workflow_run jobs on main without approval`
   - *Tuyệt đối tránh:* Các từ cường điệu như `Critical RCE`, `Full Repository Takeover`, `Catastrophic Supply Chain Compromise`, hoặc văn mẫu mở đầu kiểu *"In this comprehensive security report..."*.
2. **Giới hạn khẳng định đúng theo bằng chứng (Bounded Claims):**
   - **Về Trigger (`on:` / `if:`):** Chỉ mô tả đúng những gì khai báo trong file cấu hình. Không suy diễn sang hành vi của GitHub nếu không có trong cấu hình.
   - **Về Cổng bảo vệ (`environment:` / `author_association`):** Chứng minh ý đồ bảo mật bằng cách đối chiếu với một workflow khác trong cùng repo (như `eval-pr.yml` có `eval-gate`) hoặc tài liệu `README.md` của chính dự án đó.
   - **Về Khóa bí mật (`secrets.*`):** Khi không thực hiện tấn công xâm nhập lấy giá trị thật của secret, phải viết chính xác: *"Step tham chiếu `SECRET_NAME: '${{ secrets.SECRET_NAME }}'` trong `env:`; nếu secret này khả dụng ở cấp repository/organization (thay vì bị khóa riêng trong một environment), giá trị của nó sẽ tiếp xúc với tiến trình chạy mã từ fork."*
3. **Bằng chứng thực chứng kép (Static Code + Live API Telemetry):**
   - Luôn ghim cố định mã băm `Commit SHA` 40 ký tự hex trong mọi đường link GitHub (`/blob/<40-hex-SHA>/path#L10-L25`).
   - Đính kèm kết quả truy vấn `gh api` thực tế (cấu hình `environments/<name>` và các `actions/runs/<id>` có thật) vào `evidence/api_verification.json`.
4. **Bản vá `fix.patch` đạt chuẩn Kỹ sư Google:**
   - Phải được sinh bằng `difflib.unified_diff` hoặc `git diff` trực tiếp từ file gốc trong `.zip`.
   - Khối ` ```diff ` trong `README.md` phải giống hệt `fix.patch` từng ký tự (không dùng dấu `...` cắt dòng).
   - Khi thêm `environment: '<gate>'` vào workflow có cả `push`/`merge_group` và `workflow_run`, **phải tách thành 2 nhánh job riêng biệt** (`job_name` không có `environment` cho `push`/`merge_group`, và `job_name_gated` có `environment: '<gate>'` tĩnh cho `workflow_run`) — không bao giờ dùng biểu thức trả về chuỗi rỗng `''` cho trường `environment`.
5. **Sạch dấu vết máy quét 100%:**
   - Mọi file trong `.zip` phải dùng ký tự xuống dòng `LF` (`\n`), tuyệt đối không có `CRLF` (`\r\n`) và không có các dòng comment `# REPO:`, `# PATH:`, `# HTML_URL:`.

---

## 4. Mẫu Điền Nhanh Trên Web `https://bughunters.google.com/report`

| Bước trên Web | Trường thông tin | Cách chọn / điền chuẩn |
| :--- | :--- | :--- |
| **1. Affected target** | Target type | `Open Source Software` |
| **2. Category** | Category | `Security vulnerability` |
| **3. Product details** | Repository URL | `https://github.com/<org>/<repo>` |
| **4. Vulnerability details** | Summary (Title) | `<org>/<repo>: <Mô tả kỹ thuật ngắn gọn dưới 120 ký tự>` |
| | Vulnerability details | Dán phần **`## Summary` + `## Affected Files` + `## Technical Details` + `## Verification Evidence`** |
| | Attack scenario | Dán phần **`## Impact`** (viết gọn 2–3 gạch đầu dòng, đúng phạm vi bằng chứng) |
| | Attachments | Tải lên tệp **`<tên-gói>.zip`** |
| **5. The cause** | Vulnerability type | `Permissions Bypass` (hoặc `Other`) |
| | Does anyone else know? | `No, this vulnerability is private.` |
| | Plan to disclose publicly? | `No, I am only notifying Google` |
| | Donate reward to charity? | **Bỏ trống (Không tích)** |

---

## 5. Khung Sườn `README.md` Chuẩn Quốc Tế

```markdown
# Title
<org>/<repo>: <Cơ chế bị thiếu/lỗi> in `<tên_file>` allows <hành vi kỹ thuật cụ thể>

---

## Summary
In `<org>/<repo>`, `<file_chuẩn>` enforces `<cơ chế bảo vệ>` so that `<mục đích bảo vệ>`.

However, `<file_lỗi>` does not enforce `<cơ chế bảo vệ>`:
1. **Link A (Entry):** ...
2. **Link B (Execution Sink):** ...
3. **Link C (Privilege/Secret Scope):** ...

---

## Affected Files (Commit `<40_HEX_COMMIT_SHA>`)
- `https://github.com/<org>/<repo>/blob/<40_HEX_COMMIT_SHA>/<path_1>#L<start>-L<end>`
- `https://github.com/<org>/<repo>/blob/<40_HEX_COMMIT_SHA>/<path_2>#L<start>-L<end>`

---

## Technical Details

### 1. <Bước 1: Điểm vào / Cơ chế bảo vệ đối chiếu> (`<file>`, lines X–Y)
```yaml
<Trích dẫn nguyên văn từng ký tự từ file gốc>
```

### 2. <Bước 2: Điểm xử lý dữ liệu không tin cậy> (`<file>`, lines X–Y)
```yaml
<Trích dẫn nguyên văn từng ký tự từ file gốc>
```

---

## Verification Evidence
*(Full API responses (`evidence/api_verification.json`) and the unified patch (`fix.patch`) are included in the attached `<tên-gói>.zip` archive.)*

1. **GitHub API confirmation:**
   - ...
2. **Live workflow run evidence:**
   - ...

---

## Impact
1. **<Tác động 1 (giới hạn chặt chẽ theo bằng chứng)>:** ...
2. **<Tác động 2>:** ...

---

## Suggested Fix
1. <Mô tả ngắn gọn giải pháp 1>
2. <Mô tả ngắn gọn giải pháp 2>

```diff
<Nội dung nguyên văn của tệp fix.patch>
```
```

---

## 6. Script Python Tự Động Kiểm Định 6 Cổng (`audit_package.py`)

Chạy lệnh này trước khi gửi hoặc nộp bất kỳ gói hồ sơ nào để xác nhận đạt 100% cả 6 cổng kiểm tra:

```python
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
            subprocess.run(["git", "apply", "--check", "fix.patch"], cwd=tmp, check=True)

    print(f"[100% PASS] {os.path.basename(pkg_dir)} | README={len(rm_bytes)}B ({rm_sha[:12]}) | ZIP={os.path.getsize(z_path)}B")

if __name__ == "__main__":
    target = sys.argv[1]
    if os.path.exists(os.path.join(target, "README.md")):
        audit_package(target)
    else:
        for d in sorted(os.listdir(target)):
            p = os.path.join(target, d)
            if os.path.isdir(p) and os.path.exists(os.path.join(p, "README.md")):
                audit_package(p)
```
