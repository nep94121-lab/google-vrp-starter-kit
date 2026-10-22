---
name: google-oss-vrp-hunter
description: Hunt, verify, package, and audit non-duplicate CI/CD and supply-chain security vulnerabilities in Google-owned GitHub repositories (google, GoogleCloudPlatform, google-gemini, etc.) for Google OSS VRP.
---

# Google OSS VRP Deep Hunter & Packager Skill (v2.0 — Anti-Duplicate Hardened)

## 0. Cổng Chặn Trùng Lặp Bắt Buộc (`CỔNG 0: ANTI-DUPLICATE PRE-FILTER`)

Từ dữ liệu thực nghiệm thực tế trên hệ thống `Google Security Bot` (`sp...@google.com`, `component: 310543`, `canonical: 1469`), Bot của Google tự động đối chiếu cặp **`(Repository URL + Đường dẫn file .github/workflows/*.yml)`** với cơ sở dữ liệu Buganizer nội bộ và đóng `Duplicate` chỉ trong **6–10 phút** nếu file `.yml` đó đã có người báo cáo trước.

Vì vậy, **TRƯỚC KHI** bắt tay vào đóng gói bất kỳ lỗ hổng nào, bắt buộc phải lọc qua **Bảng Chặn Trùng Lặp** sau:

### ❌ DANH SÁCH ĐEN (BLACKLIST — TUYỆT ĐỐI BỎ QUA, KHÔNG ĐÓNG GÓI):
1. **Lỗi YAML bề mặt (`Surface YAML Patterns`) mà `zizmor` / `actionlint` / `octoscan` quét ra được ngay:**
   - Workflow dùng `workflow_run` thiếu `environment:` gate đơn thuần.
   - Workflow dùng `pull_request_target` checkout nhánh PR đơn thuần đã tồn tại trên nhánh `main` > 14 ngày.
   - Workflow dùng `peter-evans/slash-command-dispatch` hoặc truyền `event.json` qua artifact theo mẫu cơ bản.
2. **File `.yml` cũ trên các Repo "Quốc Dân" (>1,000 stars):**
   - Kiểm tra ngày sửa đổi gần nhất của file `.yml` bằng lệnh:
     ```bash
     gh api "repos/<org>/<repo>/commits?path=.github/workflows/<file>&per_page=1" --jq ".[0].commit.committer.date"
     ```
   - Nếu lỗ hổng chỉ nằm thuần túy trong file `.yml` và file đó đã không thay đổi suốt nhiều tuần/tháng trên một repo lớn $\rightarrow$ **Chắc chắn 99% đã bị người khác quét bằng tool và nộp trước (`canonical: 1469`) $\rightarrow$ BỎ QUA NGAY!**

---

### ✅ DANH SÁCH TRẮNG (WHITELIST — 3 MỎ VÀNG VƯỢT QUA BOT DUPLICATE 100%):

Chỉ chọn mục tiêu khi lỗ hổng thuộc **ít nhất 1 trong 3 nhóm chiều sâu** dưới đây (nơi các máy quét YAML tự động bị mù hoàn toàn):

1. **Mỏ vàng số 1 — Săn Bản Vá Bảo Mật Vừa Merge Trong 1–14 Ngày Qua (`Incomplete Security Fix / Patch Bypass`):**
   - **Cách tìm:** Quét các PR vừa được merge gần đây trong `google`, `GoogleCloudPlatform`, `google-gemini` có từ khóa bảo mật:
     ```bash
     gh search prs --owner google --owner GoogleCloudPlatform --owner google-gemini "harden OR traversal OR injection OR confine OR sanitize OR security" --merged --sort updated --order desc --limit 30
     ```
   - **Cách khai thác chiều sâu:** Đọc trực tiếp commit diff của bản vá đó để tìm:
     - Hàm thứ N bị bỏ quên không gọi hàm kiểm tra (ví dụ: thêm `_confine_path()` cho 3 hàm đầu nhưng quên gọi ở hàm thứ 4).
     - Cho phép ghi đè file cấu hình nhạy cảm bên trong thư mục được phép (như `.git/config` với `core.fsmonitor` hoặc `.git/hooks/`).
     - Regex/check mới thêm vào bị lệch nhánh điều kiện.

2. **Mỏ vàng số 2 — Săn Lỗi Logic Bên Trong Mã Nguồn Phụ Trợ CI/CD (`Python / JS / TS / Go Tools` & `actions/github-script`):**
   - **Cách tìm:** Tìm các workflow gọi script Python (`python -m ...`, `python scripts/...`), NodeJS, hoặc viết khối JavaScript phức tạp trong `actions/github-script`.
   - **Cách khai thác chiều sâu:**
     - Máy quét YAML thấy có từ khóa `author_association` hoặc `COLLABORATOR` ở `if:` cấp job sẽ tưởng là an toàn và bỏ qua.
     - Hãy đọc sâu vào **thứ tự câu lệnh `if / else if`** trong JS/Python (ví dụ: kiểm tra `request.startsWith("@bot")` **trước** khi kiểm tra `eventType === 'issues.opened'`, làm lộ nhánh thực thi lệnh cho người ngoài).
     - Hoặc đọc vào các **tool cấp cho AI Agent trong CI/CD** (như GraphQL mutations, Git helpers, File writers): System prompt có dặn AI không được chạm vào issue/file khác, nhưng hàm Python bên dưới (`tools.py`) lại không kiểm tra khóa phạm vi (confinement) trong code!

3. **Mỏ vàng số 3 — Săn File Workflow / Script Mới Tinh (Vừa Được Commit Trong 1–14 Ngày Gần Nhất) Hoặc Ở Repo Ngách:**
   - **Cách tìm:** Tìm các file `.github/workflows/*.yml` hoặc script CI vừa mới được tạo hoặc sửa đổi trong vài ngày gần nhất, hoặc nằm ở các repo chuyên biệt ít người biết, kết hợp chuỗi lỗi đa tầng (ví dụ: vừa truyền dữ liệu chưa lọc vào `$GITHUB_OUTPUT`, vừa có lỗi unquoted bash globbing `for f in $files; do git add "$f"`).

---

## 1. Quy Trình 5 Bước Tạo Bộ Hồ Sơ Chuẩn (`README.md` + `.zip`)

### Bước 1: Kiểm tra Tuổi Commit & Thu thập Bằng chứng Bất biến (Immutable Evidence)
1. Kiểm tra lịch sử commit của file mục tiêu để đảm bảo không rơi vào Danh Sách Đen:
   ```bash
   gh api "repos/<org>/<repo>/commits?path=<đường_dẫn_file>&per_page=3" --jq ".[] | {sha: .sha, date: .commit.committer.date, msg: .commit.message}"
   ```
2. Lấy đúng mã Commit SHA 40 ký tự hex mới nhất trên nhánh `main` của repo mục tiêu:
   ```bash
   gh api repos/<org>/<repo>/commits/main --jq .sha
   ```
3. Tải nguyên bản từng byte (raw bytes) các file `.github/workflows/*.yml` và các file mã nguồn liên quan (`tools.py`, `*.js`, ...) tại đúng Commit SHA đó lưu vào thư mục `workflows/` và `src/`.
4. Thu thập bằng chứng thực thi từ GitHub API (`actions/runs`, `environments`, hoặc kết quả chạy script `reproduce.py` offline) lưu vào `evidence/`.

### Bước 2: Viết bản vá `fix.patch` và script kiểm chứng `reproduce.py`
1. Tạo bản vá Unified Diff (`fix.patch`) từ file gốc trong `workflows/` hoặc `src/`.
2. Chạy `git init` trong thư mục tạm và chạy `git apply --check fix.patch` để đảm bảo bản vá áp dụng sạch 100% (`Exit Code: 0`).
3. Viết script `reproduce.py` chạy offline chứng minh:
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
Chỉ khi cả 2 script đều báo **`PASS`** tuyệt đối và vượt qua **`CỔNG 0: ANTI-DUPLICATE PRE-FILTER`** mới được phép nộp lên Google Bug Hunters.
