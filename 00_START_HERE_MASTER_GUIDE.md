# 🚀 BỘ CÔNG CỤ & QUY TRÌNH SĂN LỖI BẢO MẬT GOOGLE OSS VRP (`GOOGLE_VRP_STARTER_KIT`)

> **Mục đích:** Bộ tài nguyên đóng gói trọn gói (All-in-One) dành cho bạn hoặc một AI Agent khác trên máy mới có thể **cài đặt môi trường, nạp Skills & Rules, tự động đi săn lỗ hổng bảo mật không trùng lặp trên các kho mã nguồn mở của Google, đóng gói bằng chứng `.zip` đạt chuẩn 100% QA, và nộp lên `bughunters.google.com`**.
>
> **Bảo mật & Tuân thủ Google VRP:** Bộ Starter Kit này chỉ chứa **quy trình, công thức, skills, công cụ kiểm định và hồ sơ giả lập mẫu (`01_sample-ci-confinement-demo`)** — tuyệt đối không chứa bất kỳ lỗ hổng thực tế nào đang chờ Google vá hoặc thông tin tài khoản cá nhân.

---

## 📂 1. Sơ Đồ Cấu Trúc Thư Mục Này

```text
GOOGLE_VRP_STARTER_KIT/
├── 00_START_HERE_MASTER_GUIDE.md          # [FILE NÀY] Hướng dẫn tổng thể từ A-Z + Prompt giao việc cho AI
│
├── 01_SETUP_AND_INSTALL/                  # CÀI ĐẶT & KIỂM TRA MÔI TRƯỜNG
│   ├── install_tools.ps1                  # Script PowerShell tự động cài Git, GitHub CLI (gh), Python, zizmor, pyyaml, requests
│   └── check_environment.py               # Script kiểm tra toàn bộ công cụ & chạy thử kiểm định 6 cổng trên hồ sơ mẫu
│
├── 02_SKILLS_AND_RULES/                   # SKILLS CHO AI & QUY TẮC VIẾT BÁO CÁO / ĐIỀN FORM
│   ├── google-oss-vrp-hunter-skill/       # Skill dạy AI cách săn lỗi sâu (Bypass PR mới merge, logic JS/Python) né Duplicate
│   │   └── SKILL.md
│   ├── google-oss-vrp-audit/              # Skill kiểm định độc lập (kiểm tra cả cơ học lẫn logic bảo mật & đối chiếu upstream)
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   ├── references/policy-and-evidence.md
│   │   └── scripts/audit_packages.py
│   ├── MASTER_VRP_FORMULA.md              # Công thức chuẩn cấu trúc gói .zip, 5 quy tắc chống AI Slop & khung README.md
│   └── FORM_SUBMISSION_RULES.md           # Quy tắc điền 5 bước trên Google Product Form, cách né cảnh báo & giới hạn 3 bài New
│
├── 03_HUNTER_AND_SCANNER_TOOLS/           # CÔNG CỤ QUÉT & THU THẬP MỤC TIÊU
│   ├── targets.json                       # Danh sách các tổ chức GitHub mục tiêu của Google (google, GoogleCloudPlatform, google-gemini...)
│   └── hunter.py                          # Script tải & quét ban đầu các GitHub Actions workflows
│
├── 04_QA_AND_MAIL_AUTOMATION/             # CÔNG CỤ KIỂM ĐỊNH GÓI NỘP & THEO DÕI EMAIL TỰ ĐỘNG
│   ├── audit_package.py                   # Script kiểm định nhanh 6 cổng (SHA-256 README, LF, JSON, diff block, git apply --check)
│   ├── audit_packages_strict.py           # Script kiểm định nghiêm ngặt đối chiếu byte-for-byte với GitHub Upstream
│   └── check_vrp_mail.py                  # Script tự động đọc email từ buganizer-system@google.com và lập bảng theo dõi trạng thái
│
├── 05_GOLD_STANDARD_EXAMPLES/             # KHUNG BÁO CÁO & BỘ HỒ SƠ GIẢ LẬP MẪU ĐẠT CHUẨN 6 CỔNG QA
│   ├── REPORT_TEMPLATE.md                 # Khung sườn báo cáo chuẩn 6 phần
│   └── 01_sample-ci-confinement-demo/     # Bộ hồ sơ giả lập (Synthetic Demo) minh họa cấu trúc README.md + .zip đạt 100% PASS
│
└── 06_CODEX_AUDIT_HANDOFF/                # BỘ BÀN GIAO RIÊNG CHO CODEX / CHATGPT (BẬT CHATGPT 6.1.0 Ở MỨC 2)
    ├── GOOGLE_VRP_AUDIT_HANDOFF.zip       # File ZIP nguyên bản gửi cho Codex / ChatGPT kiểm định độc lập
    ├── README_VI.md                       # Hướng dẫn sử dụng bộ kiểm định của Codex
    ├── PROMPT_BAN_GIAO.md                 # Prompt chuẩn để dán cho Codex (ChatGPT 6.1.0 mức 2) chấm bài
    ├── MANIFEST.sha256.json               # Bảng băm SHA-256 toàn bộ bộ công cụ kiểm định
    ├── skills/google-oss-vrp-audit/       # Skill, tài liệu tham chiếu Tiếng Việt, REVIEW_TEMPLATE.md, CLAIM_EVIDENCE.csv
    ├── tools/verify_bundle.py             # Công cụ kiểm tra tính toàn vẹn của gói bàn giao
    └── validation/RESULTS.json            # Kết quả tự kiểm thử của bộ công cụ
```

---

## 🤝 1.5. Mô Hình Phối Hợp 2 AI Độc Lập (Antigravity + Codex ChatGPT 6.1.0 Mức 2)

1. **Bên 1 — Antigravity (Cài đặt môi trường & Đi săn lỗi & Đóng gói `.zip`):**
   - Dùng các thư mục `01_SETUP_AND_INSTALL` đến `05_GOLD_STANDARD_EXAMPLES`.
   - Cài đặt công cụ trên máy, đi săn các lỗ hổng chiều sâu theo chiến lược "3 Mỏ Vàng Chống Duplicate", viết `README.md` + `reproduce.py` + `fix.patch` và đóng gói `<tên-gói>.zip`.
2. **Bên 2 — Codex / ChatGPT (BẮT BUỘC BẬT `ChatGPT 6.1.0` Ở `MỨC 2` — Đóng vai Giám khảo Kiểm định độc lập):**
   - Dùng thư mục `06_CODEX_AUDIT_HANDOFF/` (hoặc file `06_CODEX_AUDIT_HANDOFF/GOOGLE_VRP_AUDIT_HANDOFF.zip`).
   - Dán nội dung `06_CODEX_AUDIT_HANDOFF/PROMPT_BAN_GIAO.md` kèm đường dẫn tới các hồ sơ do Antigravity vừa tạo để Codex kiểm định chéo, soi từng dòng code/bản vá/điều kiện chương trình cho tới khi đạt chuẩn gửi Triage.

---

## 🛠️ 2. Hướng Dẫn Cài Đặt, Tải Tài Nguyên & Kiểm Tra (Cho Máy Mới)

### Bước 1: Chạy Script Tự Động Cài Đặt Công Cụ
Mở **PowerShell** tại thư mục `GOOGLE_VRP_STARTER_KIT` và chạy:
```powershell
powershell -ExecutionPolicy Bypass -File .\01_SETUP_AND_INSTALL\install_tools.ps1
```
*(Script sẽ tự động kiểm tra và cài đặt: `Git`, `GitHub CLI (gh)`, `Python 3.12`, cùng các gói `requests`, `pyyaml`, `zizmor`).*

### Bước 2: Đăng Nhập GitHub CLI (`gh`)
Để các script săn lỗi và kiểm định có thể tải mã nguồn gốc và truy vấn GitHub API (không bị giới hạn 60 request/giờ), hãy chạy:
```powershell
gh auth login
```
*(Chọn `GitHub.com` $\rightarrow$ `HTTPS` $\rightarrow$ `Login with a web browser` và xác nhận).*

### Bước 3: Cài Đặt 2 Skills Vào Hệ Thống AI Của Bạn (Codex / Antigravity / Claude)
Nếu dùng **Codex** hoặc **Antigravity**, chạy lệnh sau trong PowerShell để nạp cả 2 Skills (`google-oss-vrp-hunter` và `google-oss-vrp-audit`) vào thư mục Skills của AI:
```powershell
# Cài cho Codex (~/.codex/skills)
New-Item -ItemType Directory -Force -Path "$HOME\.codex\skills" | Out-Null
Copy-Item -Path ".\02_SKILLS_AND_RULES\google-oss-vrp-audit" -Destination "$HOME\.codex\skills\google-oss-vrp-audit" -Recurse -Force
Copy-Item -Path ".\02_SKILLS_AND_RULES\google-oss-vrp-hunter-skill" -Destination "$HOME\.codex\skills\google-oss-vrp-hunter" -Recurse -Force

# Cài cho Antigravity / Gemini (~/.gemini/config/skills)
New-Item -ItemType Directory -Force -Path "$HOME\.gemini\config\skills" | Out-Null
Copy-Item -Path ".\02_SKILLS_AND_RULES\google-oss-vrp-audit" -Destination "$HOME\.gemini\config\skills\google-oss-vrp-audit" -Recurse -Force
Copy-Item -Path ".\02_SKILLS_AND_RULES\google-oss-vrp-hunter-skill" -Destination "$HOME\.gemini\config\skills\google-oss-vrp-hunter" -Recurse -Force
```

### Bước 4: Chạy Lệnh Kiểm Tra Toàn Bộ Môi Trường
```powershell
python .\01_SETUP_AND_INSTALL\check_environment.py
```
Khi màn hình hiện dòng:
`KẾT LUẬN: MÔI TRƯỜNG ĐÃ SẴN SÀNG 100% ĐỂ BẮT ĐẦU SĂN BUG GOOGLE VRP!`
và bộ hồ sơ mẫu (`01_sample-ci-confinement-demo`) hiện `[100% PASS]`, bạn đã sẵn sàng bắt đầu!

---

## 🎯 3. Quy Trình 5 Giai Đoạn Săn Bug & Nộp Bài Thành Công

### Giai đoạn 1: Chọn Mục Tiêu Không Trùng Lặp (Tránh Bẫy `Duplicate`)
- **KHÔNG** nộp các lỗi cấu hình `.yml` bề mặt (`workflow_run` / `pull_request_target` cũ kỹ) trên các repo quá đông người quét vì các trình quét tự động đã báo cáo từ trước.
- **TẬP TRUNG VÀO 3 MỎ VÀNG** (xem chi tiết trong `02_SKILLS_AND_RULES/google-oss-vrp-hunter-skill/SKILL.md`):
  1. **Săn các PR bảo mật vừa được Google merge trong 1–7 ngày gần nhất** (`gh search prs --owner google --owner GoogleCloudPlatform "security OR traversal OR injection OR harden" --merged`) để tìm **lỗi vá sót (Incomplete Fix / Patch Bypass)**.
  2. **Săn lỗi logic bên trong code Python/JS/Bash được gọi từ GitHub Actions** (mà máy quét YAML không đọc hiểu được).
  3. **Săn lỗi truyền dữ liệu không kiểm tra vào `$GITHUB_OUTPUT` / `$GITHUB_ENV` / GraphQL mutations ở các repo mới hoặc repo ngách**.

### Giai đoạn 2: Xác Minh Thực Chứng & Viết Script Tái Hiện (`reproduce.py`)
- Luôn tải đúng file gốc tại Commit SHA 40 ký tự hex mới nhất trên nhánh `main`.
- Viết script `reproduce.py` chạy độc lập ở local (với dữ liệu giả lập an toàn, tuyệt đối không tấn công lên hệ thống thật của Google) để xuất ra file kết quả `evidence/*.json`.

### Giai đoạn 3: Đóng Gói Hồ Sơ (`README.md` + `<tên-gói>.zip`)
- Tuân thủ đúng cấu trúc trong `02_SKILLS_AND_RULES/MASTER_VRP_FORMULA.md` và đối chiếu với mẫu trong `05_GOLD_STANDARD_EXAMPLES/`.

### Giai đoạn 4: Kiểm Định Kép 100% Trước Khi Nộp
Chạy lần lượt 2 lệnh:
```powershell
python .\04_QA_AND_MAIL_AUTOMATION\audit_package.py <thư_mục_chứa_các_bộ_hồ_sơ>
python .\04_QA_AND_MAIL_AUTOMATION\audit_packages_strict.py <thư_mục_chứa_các_bộ_hồ_sơ> --profiles 01 --fetch-upstream
```

### Giai đoạn 5: Nộp Bài Trên `bughunters.google.com/report`
- Đọc kỹ `02_SKILLS_AND_RULES/FORM_SUBMISSION_RULES.md`.
- Nhớ quy tắc: **Mỗi đợt chỉ giữ tối đa 3 bài đang ở trạng thái `New` (`🟨 SUBMITTED`)** để không bị chạm trần Rate Limit của tài khoản mới!

---

## 🤖 4. Prompt Mẫu Để Giao Việc Ngay Cho AI Khác (Copy & Dán)

### 4.1. Prompt Giao Cho Antigravity (Bên Cài Đặt & Đi Săn Lỗi)
```text
Tôi đã chuẩn bị sẵn bộ công cụ, quy tắc, skills và hồ sơ mẫu săn lỗi Google OSS VRP tại thư mục `GOOGLE_VRP_STARTER_KIT`.

Hãy thực hiện ngay các bước sau theo thứ tự:
1. Đọc toàn bộ các file hướng dẫn và quy tắc trong thư mục này:
   - `00_START_HERE_MASTER_GUIDE.md`
   - `02_SKILLS_AND_RULES/google-oss-vrp-hunter-skill/SKILL.md`
   - `02_SKILLS_AND_RULES/google-oss-vrp-audit/SKILL.md`
   - `02_SKILLS_AND_RULES/google-oss-vrp-audit/references/policy-and-evidence.md`
   - `02_SKILLS_AND_RULES/MASTER_VRP_FORMULA.md`
   - `02_SKILLS_AND_RULES/FORM_SUBMISSION_RULES.md`
2. Đọc `05_GOLD_STANDARD_EXAMPLES/REPORT_TEMPLATE.md` và `05_GOLD_STANDARD_EXAMPLES/01_sample-ci-confinement-demo/README.md` để nắm vững tiêu chuẩn cấu trúc của một bộ hồ sơ chuẩn 6 cổng QA.
3. Chạy `python 01_SETUP_AND_INSTALL/check_environment.py` để kiểm tra môi trường máy tính của tôi (nếu thiếu công cụ nào hãy chạy `01_SETUP_AND_INSTALL/install_tools.ps1` để cài đặt).
4. Sau khi môi trường đạt 100% PASS, hãy áp dụng chiến lược "3 Mỏ Vàng Chống Duplicate" trong `02_SKILLS_AND_RULES/google-oss-vrp-hunter-skill/SKILL.md` để tìm kiếm các lỗ hổng CI/CD & Supply-Chain mới trên các tổ chức `google`, `GoogleCloudPlatform`, `google-gemini`.
5. Với mỗi lỗ hổng tìm được, hãy đóng gói đầy đủ `README.md` và `<tên-gói>.zip` (kèm `fix.patch`, `reproduce.py`, `evidence/*.json`, `workflows/`, `src/`) và chạy cả 2 script kiểm định `04_QA_AND_MAIL_AUTOMATION/audit_package.py` và `04_QA_AND_MAIL_AUTOMATION/audit_packages_strict.py --fetch-upstream` đạt 100% PASS trước khi báo cáo cho tôi.
```

### 4.2. Prompt Giao Cho Codex (Bật ChatGPT 6.1.0 Ở Mức 2 — Bên Kiểm Định Độc Lập)
Xem chi tiết trong file `06_CODEX_AUDIT_HANDOFF/PROMPT_BAN_GIAO.md`.
