---
name: google-oss-vrp-hunter
description: Hunt, verify, package, and audit non-duplicate CI/CD and supply-chain security vulnerabilities in Google-owned GitHub repositories (google, GoogleCloudPlatform, google-gemini, etc.) for Google OSS VRP and Cloud VRP.
---

# Google OSS & Cloud VRP Deep Hunter Skill (v3.0 — Real Triage Hardened)

> **Cập nhật v3.0 từ kết quả Triage thực tế của Kỹ sư Google (`wo...@google.com`, `ki...@google.com`, `Google Security Bot`):**
> Tích hợp đầy đủ 4 cổng chặn để không bao giờ bị đóng `Duplicate (canonical: 1469)`, `Infeasible (Product Vuln)`, `WAI (Rate Limit)`, hay bị yêu cầu *"Try the attack on github.com"*.

---

## 0. Bốn Cổng Sống Còn Trước Khi Đi Săn & Đóng Gói (`4 MANDATORY GATES`)

### 🚫 CỔNG 1: Chặn Trùng Lặp (`Anti-Duplicate Gate — Canonical 1469`)
- **Nguyên nhân bị `Duplicate` sau 6–10 phút:** `Google Security Bot` (`component: 310543`, `canonical: 1469`) tự động khớp cặp **`(Repository URL + Đường dẫn file .github/workflows/*.yml)`**. Nếu file `.yml` đó đã có người báo cáo trước, bài của bạn bị đóng tự động ngay.
- **Quy tắc bắt buộc:**
  - **BỎ QUA 100%** các lỗi cấu hình `.yml` bề mặt (`workflow_run` thiếu gate, `pull_request_target` cơ bản, `slash-command-dispatch`, đọc `event.json` đơn thuần) đã tồn tại `> 14 ngày` trên các repo lớn mà công cụ tĩnh (`zizmor`, `actionlint`, `octoscan`) quét thấy được.
  - **CHỈ SĂN:**
    1. **Bản vá bảo mật vừa mới merge (`1–14 ngày`) bị vá sót (`Incomplete Fix / Patch Bypass`)** trong code Python/JS/TS/Go.
    2. **Lỗi logic thứ tự câu lệnh (`if / else if`) hoặc thiếu confinement bên trong script phụ trợ CI/CD (`tools.py`, `*.js`, `actions/github-script`)** nơi máy quét YAML bị mù hoàn toàn.
    3. **Workflow/Script mới tinh vừa được commit trong `1–14 ngày` gần nhất.**

### 🌩️ CỔNG 2: Chặn Lỗi `Infeasible` — Chỉ Đánh Mục Tiêu Có Tác Động `Cloud VRP` Hoặc `Supply Chain` Thật Sự
- **Thực tế từ Triage (`576464468` vs `576454169`):**
  - Hồ sơ `576464468` (`automotive-design-compose`) bị đóng `Infeasible` vì chỉ ghi vào `$GITHUB_OUTPUT` trong một workflow phụ chỉ có `GITHUB_TOKEN` thông thường $\rightarrow$ bị coi là lỗi sản phẩm nội bộ (`product vulnerability`), mà từ **01/10/2026 Google OSS VRP chỉ nhận lỗi Supply Chain**.
  - Ngược lại, hồ sơ `576454169` (`GoogleCloudPlatform/gemini-cloud-assist-mcp`, `genmedia-creative-studio`) được Kỹ sư Google **nâng thẳng từ `P4` lên `P2` và chuyển sang hàng đợi `Google Cloud VRP` (`component: 1609699 → 1610896`)** vì workflow đó nằm trên `GoogleCloudPlatform` và kết nối với tài nguyên Google Cloud / Gemini!
- **Quy tắc chọn mục tiêu (Target Selection Rule):**
  Workflow hoặc CI Tool bị lỗi **BẮT BUỘC** phải gắn với ít nhất 1 trong 3 đặc quyền lớn sau:
  1. **Tuyến Google Cloud VRP (Ưu tiên số 1 — Lên thẳng `P2`):** Repo thuộc `GoogleCloudPlatform/*` hoặc workflow có bước xác thực `google-github-actions/auth` (`workload_identity_provider`, `credentials_json`, `GCP_SA_KEY`, Vertex AI, Cloud Run, GKE, Artifact Registry).
  2. **Tuyến Supply Chain Release / Package Publishing:** Workflow có quyền phát hành gói (`PYPI_TOKEN`, `NPM_TOKEN`, `CARGO_REGISTRY_TOKEN`, `release` creation, signing keys) hoặc có quyền push trực tiếp/mở PR tự động bằng `PAT` / `BOT_GITHUB_TOKEN` vào nhánh chính.
  3. **Tuyến Self-Hosted Runner / Khai thác hạ tầng Build:** Workflow chạy trên `runs-on: self-hosted` hoặc custom runner của Google.

### 🧪 CỔNG 3: Chứng Minh Thực Tế Trên Fork GitHub Cá Nhân (Tránh Bị Nhắc *"Try the attack on github.com"*)
- **Thực tế từ Triage (`576452571`):** Dù bài được nâng lên `P2` (`Assigned`), kỹ sư Google vẫn có thể yêu cầu *"Try the attack on github.com"* nếu bạn chỉ gửi kết quả chạy hàm Python cắt rời ở máy local mà chưa cho thấy toàn bộ luồng chạy trên GitHub Actions.
- **Quy tắc thực hiện PoC An Toàn 100% Trên `github.com`:**
  - **TUYỆT ĐỐI KHÔNG** tấn công vào repo gốc của Google (`google/*`, `GoogleCloudPlatform/*`).
  - Thay vào đó, **Fork repo mục tiêu về tài khoản GitHub cá nhân của bạn (`github.com/<tài-khoản-của-bạn>/<repo-fork>`)**, bật GitHub Actions trên repo fork của bạn, và kích hoạt đúng workflow/script lỗi trên **repo fork của chính bạn** (với secret giả lập `DUMMY_SECRET` của bạn).
  - Đính kèm **đường link GitHub Actions Run trên repo fork của bạn** + log thực thi thật vào mục `## Verification Evidence` và vào gói `.zip`! Khi đó kỹ sư Google bấm vào là thấy ngay bằng chứng chạy thật trên `github.com` mà không vi phạm bất kỳ quy tắc nào.

### 🚦 CỔNG 4: Quản Lý Hạn Mức Tối Đa 3 Bài Đang Mở (`Anti-WAI Rate Limit Gate`)
- **Thực tế từ Triage (`576467236`):** Khi bạn đang có **3 bài ở trạng thái mở (`New` hoặc `Assigned`)**, bài thứ 4 nộp lên sẽ bị `Google Security Bot` đóng tự động thành `WAI (Intended Behavior)` kèm thông báo *"Whoa, slow down bughunting champion..."*.
- **Quy tắc:** Trước khi bấm Submit trên web, luôn kiểm tra trang `bughunters.google.com`: tổng số bài có trạng thái **`New` + `Assigned`** phải **$\le 2$ bài** thì mới được nộp bài tiếp theo.

---

## 1. Quy Trình 5 Bước Tạo Bộ Hồ Sơ Hạng Nặng (`P2 / Cloud VRP & Supply Chain`)

### Bước 1: Quét Mục Tiêu Theo 3 Bộ Lọc Chiều Sâu
1. **Bộ lọc A — Săn các PR bảo mật vừa mới merge trong 1–14 ngày qua (`Incomplete Security Fix`):**
   ```bash
   gh search prs --owner google --owner GoogleCloudPlatform --owner google-gemini "harden OR traversal OR injection OR confine OR sanitize OR security" --merged --sort updated --order desc --limit 30
   ```
2. **Bộ lọc B — Săn các Workflow có xác thực Google Cloud (`google-github-actions/auth`) kết hợp gọi script `.py` / `.js` / `github-script`:**
   ```bash
   gh search code --owner GoogleCloudPlatform --owner google --owner google-gemini "google-github-actions/auth" --filename ".yml" --limit 50
   ```
3. **Bộ lọc C — Săn các AI Agent CI/CD Workflows (`gemini-dispatch`, `adk`, `triage`, `agent`) mới cập nhật:**
   ```bash
   gh search code --owner GoogleCloudPlatform --owner google "actions/github-script" "author_association" path:.github/workflows --limit 50
   ```

### Bước 2: Tái Hiện Thực Tế (Local `reproduce.py` + Fork trên `github.com`)
1. Lấy đúng Commit SHA 40 ký tự hex mới nhất trên nhánh `main`.
2. Tải nguyên bản từng byte các file workflow và script phụ trợ vào `workflows/` và `src/`.
3. Viết `reproduce.py` kiểm chứng cả trước và sau khi áp dụng `fix.patch`.
4. *(Khuyên dùng cho các lỗi phức tạp)* Fork repo về GitHub cá nhân hoặc tạo repo test riêng trên `github.com` để chạy thử nghiệm luồng GitHub Actions end-to-end và lưu log vào `evidence/`.

### Bước 3: Viết `fix.patch` và Kiểm Chứng Bằng `git apply --check`
- Tạo Unified Diff chuẩn và chạy `git apply --check fix.patch` đạt `Exit Code: 0`.

### Bước 4: Viết `README.md` Theo Đúng 6 Mục Chuẩn Kỹ Sư Google
- Nêu rõ luồng dữ liệu đầu-cuối (End-to-End Trace): từ **GitHub Event / Trigger nào** $\rightarrow$ đi qua **điều kiện `if:` nào** $\rightarrow$ chạm tới **hàm/dòng code nào** $\rightarrow$ tác động lên **Cloud WIF / Supply Chain Secret nào**.

### Bước 5: Chạy 2 Script Kiểm Định Độc Lập Trước Khi Nộp
```bash
python 04_QA_AND_MAIL_AUTOMATION/audit_package.py <đường_dẫn_thư_mục_hồ_sơ>
python 04_QA_AND_MAIL_AUTOMATION/audit_packages_strict.py <thư_mục_cha> --profiles <ID> --fetch-upstream
```
