---
name: google-vrp-reporting
description: Use this skill whenever finishing a Google VRP bug hunt, evidence creation, PoC verification, or report update. Enforces a mandatory 5-part structured Vietnamese handoff report designed for instant, zero-guessing cross-AI verification by Codex/ChatGPT (Official Rules & Bounded Scope, Execution Truth & Step-by-Step Trace, Exact File Locations & SHA-256 Manifest, Finding Closure & Zero-Guessing Reproduction Commands, and Cross-AI Audit Prompt).
---

## Mandatory actionable review findings

Follow [the findings and closure contract](references/review-findings-contract.vi.md) for every review. Each unresolved item needs a stable ID, exact file/line or ABSENT evidence location, current statement, checked counterevidence, unmet condition, concrete revision, expected observation, handoff artifacts and a measurable closure check. Include these in the user-facing findings table; do not end with only “missing PoC/E2E” or an unexplained readiness percentage. Use [assets/FINDING_TEMPLATE.md](assets/FINDING_TEMPLATE.md) and [assets/FINDINGS_HANDOFF.csv](assets/FINDINGS_HANDOFF.csv). Keep rechecks bounded to agreed closure criteria; label new findings with their new evidence. “All agreed checks closed” is not a Google acceptance or reward guarantee.


# Skill Báo Cáo Bàn Giao & Kiểm Tra Chéo Google VRP (`google-vrp-reporting`)

> **Khi nào kích hoạt Skill này:**
> Bất cứ khi nào hoàn thành việc tìm lỗi mới, làm bằng chứng thực nghiệm (`reproduce.py` / `unittest`), viết bản vá (`fix.patch`), hoặc cập nhật hồ sơ phản hồi cho Kỹ sư Google, Agent **BẮT BUỘC** trình bày báo cáo tổng kết theo đúng **Mô-típ 5 Phần Chuẩn Kiểm Định Nhanh** dưới đây (ĐÃ BỎ phần copy-paste văn bản tiếng Anh dài dòng; thay bằng Bảng Sự Thật Thực Thi, Bảng SHA-256 Manifest & Dòng Code để Codex kiểm tra tức thì không cần mò).

---

## 📋 MÔ-TÍP BÁO CÁO 5 PHẦN BẮT BUỘC SAU KHI LÀM XONG

### 📜 Phần 1: Yêu Cầu Kỹ Thuật, Căn Cứ Luật Google & Bảng Sự Thật Thực Thi (Zero-Overclaim)
1. **Nguyên văn yêu cầu từ Google / Mục tiêu bài toán:**
   - Trích dẫn nguyên văn thông báo trên Buganizer (kèm trạng thái thực tế của snapshot, ví dụ `Assigned / P2` hoặc `New / P2`) hoặc cơ chế bảo mật mục tiêu.
2. **Các đường link Luật chính thức của Google VRP áp dụng cho bài này:**
   - 🔗 **Quy tắc Google OSS VRP:** `https://bughunters.google.com/about/rules/open-source/google-open-source-software-vulnerability-reward-program-rules`
   - 🔗 **Cập nhật Quy tắc OSS VRP 2026 (Impact & Reachability):** `https://bughunters.google.com/blog/ossvrp-rule-updates-2026`
   - 🔗 **Khung Chất Lượng Báo Cáo (Report Quality Framework):** `https://bughunters.google.com/blog/level-up-your-reports-introducing-our-updated-report-quality-framework`
   - 🔗 **Chương trình Thưởng Bản Vá (Google Patch Rewards Program):** `https://bughunters.google.com/about/rules/4928084514701312/patch-rewards-program-rules`
3. **Bảng Sự Thật Thực Thi (`Execution Truth Table` — Giúp Codex biết ngay cái gì Thật / Mock / Chưa chạy mà không cần mò code):**
   - **Thao tác Thật (Real):** Liệt kê rõ (VD: `git init`, `git init --bare`, `_run_git_command`, ghi file thật trong temp dir...).
   - **Thao tác Giả lập (Mocked/Stubbed):** Liệt kê chính xác hàm nào đang dùng `mock.patch` và giá trị trả về (VD: `tools.post_request` mock trả về `mocked-local-test-no-network`).
   - **Phần Chưa Thực Hiện / Điều Kiện Biên (Unverified / Preconditions):** Ghi rõ có GitHub Actions run thực tế hay chưa (`total_count=0` hay có link run), có gate nhãn nào (`'docs updates'`, `release: [published]`), và giữ impact hạ tầng/Cloud ở mức `Conditional / Unverified` nếu chưa chạy E2E qua gate.

---

### 🛠️ Phần 2: Các Bước Thực Tế Agent Đã Làm & Lệnh Tái Hiện Tức Thì (Zero-Guessing Reproduction)
1. **5 Bước Kỹ Thuật Đã Thực Thi:**
   - **Bước 1 — Đối chiếu Commit & Nguồn Upstream:** Ghi rõ Commit SHA 40 ký tự, ngày committer UTC (`YYYY-MM-DDTHH:MM:SSZ`), đúng nguyên văn Commit Subject, và trạng thái so với `HEAD` hiện tại.
   - **Bước 2 — Tải nguyên bản File Upstream:** Liệt kê số lượng file upstream trong `.zip` và xác nhận giữ nguyên 100% bytes/license.
   - **Bước 3 — Xây dựng Bộ Kiểm Thử (`unittest` / `reproduce.py`) & Bản Vá (`fix.patch`):** Liệt kê từng hàm test (bao gồm cả ca `happy-path` hợp lệ và các ca kiểm tra lỗ hổng / kiểm tra nguyên vẹn bytes sau khi từ chối).
   - **Bước 4 — Kết quả chạy Trước & Sau Khi Vá:** Ghi rõ `Exit Code`, số test chạy, số test `FAIL` / `ok`, và tên file log (`unit-before.log`, `unit-after.log`).
   - **Bước 5 — Kiểm định Cơ học (`audit_package.py` & `audit_packages_strict.py`):** Ghi đúng kết quả cơ học thực tế (số file khớp upstream, `patch=PASS`, `crlf=0`, `0` file `.pyc`/`__pycache__`).
2. **Khối Lệnh Tái Hiện Tức Thì Cho Reviewer (Đủ cả Windows PowerShell & POSIX `bash`):**
   - Ghi rõ **Thư mục đứng chạy (`cwd`)**, **Lệnh cài thư viện (`pip install ...`)**, và **Lệnh chạy Trước vá → Áp dụng Patch → Chạy Sau vá** để Codex copy chạy được ngay trong 1 bước.

---

### 📂 Phần 3: Vị Trí Chính Xác Của Toàn Bộ Bằng Chứng & Bảng Băm `SHA-256` (`OUTPUT_MANIFEST.json`)
Liệt kê đầy đủ liên kết clickable kèm **Kích thước (`bytes`)** và **Mã băm `SHA-256`** của từng tệp để Codex đối chiếu tức thì:
- 📁 **Thư mục hồ sơ chính:** `[Tên_Thư_Mục](file:///...)`
- 📄 **Báo cáo chính (`README.md`):** `[README.md](file:///...)` (`... bytes`, `SHA-256: ...`)
- 💬 **File nội dung trả lời / điền form (`COMMENT_REPLY_*.md`):** `[COMMENT_REPLY_*.md](file:///...)` (`... bytes`, `SHA-256: ...`)
- 🧪 **File kiểm thử (`test_*.py` / `reproduce.py`):** `[Tên_File_Test](file:///...)` (`... bytes`, `SHA-256: ...`)
- 🩹 **Bản vá (`fix.patch`):** `[fix.patch](file:///...)` (`... bytes`, `SHA-256: ...`)
- 📊 **File Log & JSON Evidence (`unit-before.log`, `unit-after.log`, `*.json`):** Kèm link, `bytes`, `SHA-256`.
- 📦 **Gói nén `.zip`:** `[Tên_Gói.zip](file:///...)` (`... bytes`, `SHA-256: ...`)
- 🗂️ **File Manifest & Bảng Bàn Giao (`OUTPUT_MANIFEST.json`, `FINDINGS_HANDOFF.csv`):** Kèm link trực tiếp.

---

### 🔍 Phần 4: Bảng Định Vị Dòng Code & Trạng Thái Đóng Lỗi (`F1` → `Fn` Pinpoint Table)
*(Thay thế hoàn toàn phần copy-paste văn bản dài dòng trước đây. Giúp Codex nhảy thẳng tới đúng dòng cần kiểm tra mà không phải đọc mò từ đầu)*

Lập bảng gồm 5 cột bắt buộc cho mọi mục kiểm tra hoặc sửa lỗi:
1. **Mã mục (`F1`, `F2`... / Hạng mục kiểm tra)**
2. **Trạng thái (`FIXED_PENDING_REVIEW` / `CLOSED` / `UNVERIFIED`)**
3. **Toạ độ chính xác (`File` + `#Lstart-Lend` + `SHA-256` mới)**
4. **Thay đổi cụ thể / Bằng chứng tại dòng đó**
5. **Phép kiểm tra đóng mục (`Closure Check` đo lường được)**

---

### 🤖 Phần 5: Prompt Bàn Giao Cho Bên Kiểm Định Độc Lập (Codex ChatGPT 6.1.0 Mức 2)
Kết thúc bằng một khung ` ```text ` chứa câu Prompt chỉ rõ đường dẫn tuyệt đối của `OUTPUT_MANIFEST.json`, `FINDINGS_HANDOFF.csv`, thư mục hồ sơ, lệnh chạy kiểm thử và danh sách tọa độ dòng `#L...` để người dùng copy gửi ngay cho Codex kiểm tra chéo.
