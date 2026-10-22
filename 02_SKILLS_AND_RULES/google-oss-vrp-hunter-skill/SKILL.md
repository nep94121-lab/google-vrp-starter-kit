---
name: google-oss-vrp-hunter
description: Hunt, verify, package, and audit non-duplicate CI/CD and supply-chain security vulnerabilities in Google-owned GitHub repositories (google, GoogleCloudPlatform, google-gemini, etc.) for Google OSS VRP.
---

# Google OSS VRP Deep Hunter & Packager Skill

## 1. Chiến Lược Săn Lỗi Không Bị Trùng Lặp (Anti-Duplicate Hunting Strategy)

Thực tế từ hệ thống Triage tự động của Google (`sp...@google.com` / `Google Security Bot` — `component: 310543`, `canonical: 1469`):
- **Những gì BỊ TRÙNG LẶP (`Duplicate` trong 6–10 phút đầu):**
  - Các lỗi cấu hình YAML bề mặt (`pull_request_target` hoặc `workflow_run` kinh điển trên các repo quá nổi tiếng) mà các công cụ quét tự động công khai (`zizmor`, `actionlint`, `octoscan`) có thể quét ra chỉ trong vài giây.
- **3 Mỏ Vàng VƯỢT QUA Bot Trùng Lặp (`Status: New / SUBMITTED`):**
  1. **Mỏ vàng số 1 — Săn Bản Vá Bảo Mật Vừa Merge Trong 24h–72h Qua (Incomplete Security Fix / Patch Bypass):**
     - Tìm các PR vừa được merge trong các tổ chức `google`, `GoogleCloudPlatform`, `google-gemini` có từ khóa: `fix: harden`, `security`, `path traversal`, `injection`, `confine`, `sanitize`, `workflow_run`.
     - Đọc trực tiếp commit diff của bản vá đó để tìm **hàm bị bỏ quên** hoặc **nhánh logic chưa khóa hết**!
     - *Mẫu điển hình:* Một PR bảo mật thêm hàm `_confine_path()` cho 3 tool đọc file nhưng quên gọi `_confine_path(local_path)` trong hàm thứ 4 hoặc quên chặn các đường dẫn cấu hình nhạy cảm bên trong workspace.
  2. **Mỏ vàng số 2 — Săn Lỗi Logic Trong Script Nội Tuyến (`actions/github-script`, Python/JS/Bash CI Tools):**
     - Các công cụ quét tĩnh YAML không hiểu được thứ tự câu lệnh `if / else if` bên trong khối JavaScript của `actions/github-script` hoặc trong các script Python được gọi bởi GitHub Actions.
     - *Mẫu điển hình:* Biểu thức `if:` cấp job dùng phép `||` cho phép sự kiện từ người ngoài đi qua, sau đó đoạn JS phân tích lệnh lại ưu tiên nhánh prefix trước khi kiểm tra `author_association`.
  3. **Mỏ vàng số 3 — Săn Lỗi Truyền Dữ Liệu Qua `$GITHUB_OUTPUT` / `$GITHUB_ENV` Ở Các Repo Ngách + Kiểm Chứng Byte-Level:**
     - Tập trung vào các repo mới hoặc chuyên biệt, kết hợp viết script kiểm chứng offline chạy thật (`reproduce.py`) chứng minh cả lỗi lẫn bản vá.

---

## 2. Quy Trình 5 Bước Tạo Bộ Hồ Sơ Chuẩn (`README.md` + `.zip`)

### Bước 1: Thu thập bằng chứng bất biến (Immutable Evidence)
1. Lấy đúng mã Commit SHA 40 ký tự hex mới nhất trên nhánh `main` của repo mục tiêu:
   ```bash
   gh api repos/<org>/<repo>/commits/main --jq .sha
   ```
2. Tải nguyên bản từng byte (raw bytes) các file `.github/workflows/*.yml` và các file mã nguồn liên quan tại đúng Commit SHA đó lưu vào thư mục `workflows/` và `src/`.
3. Thu thập bằng chứng thực thi từ GitHub API (`actions/runs`, `environments`, hoặc kết quả chạy script `reproduce.py` offline) lưu vào `evidence/`.

### Bước 2: Viết bản vá `fix.patch` và kiểm chứng bằng `git apply --check`
1. Tạo bản vá Unified Diff (`fix.patch`) từ file gốc trong `workflows/` hoặc `src/`.
2. Chạy `git init` trong thư mục tạm và chạy `git apply --check fix.patch` để đảm bảo bản vá áp dụng sạch 100% (`Exit Code: 0`).
3. Nếu lỗ hổng nằm trong code Python/JS, viết script `reproduce.py` chứng minh:
   - Trước khi vá: Tái hiện lỗi thành công trong môi trường giả lập cô lập.
   - Sau khi vá: Bị chặn hoàn toàn.

### Bước 3: Viết `README.md` theo đúng 6 mục chuẩn Kỹ sư Google
1. `# Title`: `<org>/<repo>: <Cơ chế bị thiếu/lỗi> in <tên_file> allows <hậu quả kỹ thuật>` (Dưới 200 ký tự).
2. `## Summary`: Nêu rõ cơ chế bảo vệ dự kiến và các điểm lỗi cụ thể (1, 2, 3).
3. `## Affected Files`: Mọi đường link GitHub phải gắn cứng Commit SHA 40 ký tự hex và số dòng (`#L10-L50`).
4. `## Technical Details`: Trích dẫn nguyên văn đoạn code lỗi (khớp 100% từng ký tự với file trong `.zip`).
5. `## Verification Evidence`: Trích dẫn kết quả từ `evidence/*.json` và `reproduce.py`.
6. `## Impact` & `## Suggested Fix`: Nêu rõ điều kiện (`if ...`), phạm vi ảnh hưởng và đính kèm khối ` ```diff ` khớp từng ký tự với `fix.patch`.

### Bước 4: Đóng gói `.zip` không có CRLF
- Mọi file (`README.md`, `fix.patch`, `reproduce.py`, `evidence/*.json`, `workflows/*`, `src/*`) phải dùng ký tự xuống dòng `LF` (`\n`).
- File `README.md` bên ngoài và `README.md` bên trong `.zip` phải giống hệt nhau từng byte (cùng mã SHA-256).

### Bước 5: Chạy 2 Script Kiểm Định Độc Lập Trước Khi Nộp
```bash
python 04_QA_AND_MAIL_AUTOMATION/audit_package.py <đường_dẫn_thư_mục_hồ_sơ>
python 04_QA_AND_MAIL_AUTOMATION/audit_packages_strict.py <thư_mục_cha> --profiles <ID> --fetch-upstream
```
Chỉ khi cả 2 script đều báo **`PASS`** tuyệt đối mới được phép nộp lên Google Bug Hunters.
