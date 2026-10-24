---
name: google-vrp-reporting
description: Use this skill whenever finishing a Google VRP bug hunt, evidence creation, PoC verification, or report update. Enforces a mandatory 5-part structured Vietnamese handoff report (Official Rules & Links, Step-by-Step Technical Execution Trace, Exact File Locations, Ready-to-Paste Google Submission/Comment Text, and Cross-AI Audit Prompt).
---

# Skill Báo Cáo Bàn Giao & Kiểm Tra Chéo Google VRP (`google-vrp-reporting`)

> **Khi nào kích hoạt Skill này:**
> Bất cứ khi nào hoàn thành việc tìm lỗi mới, làm bằng chứng thực nghiệm (`reproduce.py` / `unittest`), viết bản vá (`fix.patch`), hoặc cập nhật phản hồi cho Kỹ sư Google trên Buganizer, Agent **BẮT BUỘC** phải trình bày báo cáo tổng kết cho người dùng theo đúng **Mô-típ 5 Phần Cố Định** dưới đây để người dùng dễ kiểm tra và chuyển giao cho AI khác chấm chéo.

---

## 📋 MÔ-TÍP BÁO CÁO 5 PHẦN BẮT BUỘC SAU KHI LÀM XONG

### 📜 Phần 1: Yêu Cầu Kỹ Thuật & Căn Cứ Luật Chính Thức Của Google (Kèm Link)
1. **Nguyên văn yêu cầu từ Google / Mục tiêu bài toán:**
   - Trích dẫn nguyên văn email phản hồi của Google trên Buganizer (nếu là bài đang `Assigned` / cần bổ sung bằng chứng) hoặc nêu rõ cơ chế bảo mật mục tiêu bị vượt qua.
2. **Các đường link Luật chính thức của Google VRP áp dụng cho bài này:**
   - 🔗 **Quy tắc Google OSS VRP (Supply Chain & Giới hạn thử nghiệm):** `https://bughunters.google.com/about/rules/open-source/google-open-source-software-vulnerability-reward-program-rules`
   - 🔗 **Cập nhật Quy tắc OSS VRP 2026 (Reachable Code Path & AI Verification):** `https://bughunters.google.com/blog/ossvrp-rule-updates-2026`
   - 🔗 **Khung Chất Lượng Báo Cáo (Report Quality Framework — Tiêu chí chấm PoC):** `https://bughunters.google.com/blog/level-up-your-reports-introducing-our-updated-report-quality-framework`
   - 🔗 **Chương trình Thưởng Bản Vá (Google Patch Rewards Program):** `https://bughunters.google.com/about/rules/patch-rewards-program/google-patch-rewards-program-rules`
3. **Giải thích vì sao cách làm bằng chứng này hợp lệ 100% và đủ điều kiện nhận thưởng:**
   - Nêu rõ thuộc tuyến nào (`Google Cloud VRP P2` hay `Supply Chain Release/Repo Write`) và khẳng định 100% thử nghiệm diễn ra trên bản sao độc lập (Local Unit-Test / Repo cá nhân), tuyệt đối không tấn công repo thật của Google.

---

### 🛠️ Phần 2: Các Bước Thực Tế Agent Đã Làm Để Tạo Ra Bằng Chứng (Step-by-Step Execution Trace)
Trình bày rõ ràng 5 bước kỹ thuật mà Agent đã thực thi trên máy để người dùng nắm rõ từng thao tác:
1. **Bước 1 — Khám phá & Xác định điểm hở:** Đã dùng lệnh `gh api` nào, đọc commit/PR nào và phát hiện ra điểm sót nào trong code/test của Google.
2. **Bước 2 — Tải nguyên bản File Upstream:** Đã tải những file nào ở đúng Commit SHA 40 ký tự hex nào từ nhánh `main` của Google.
3. **Bước 3 — Xây dựng Bộ Kiểm Thử (`unittest` / `reproduce.py`) & Bản Vá (`fix.patch`):** Giải thích ngắn gọn từng hàm kiểm thử đã viết (kế thừa đúng chuẩn test của dự án gốc như thế nào).
4. **Bước 4 — Chạy Thực Nghiệm Trước & Sau Khi Vá:**
   - Kết quả chạy lệnh thực tế **TRƯỚC khi vá** (chứng minh lỗ hổng tái hiện thành công).
   - Kết quả chạy lệnh thực tế **SAU khi áp dụng `fix.patch`** (chứng minh lỗ hổng bị chặn hoàn toàn, đạt `OK` / `Exit Code: 0`).
5. **Bước 5 — Kiểm Định 6 Cổng Cơ Học (`audit_package.py`):** In rõ dòng kết quả `[100% PASS] <tên-gói> | README=... | ZIP=...`.

---

### 📂 Phần 3: Vị Trí Chính Xác Của Toàn Bộ Bằng Chứng & Hồ Sơ (Clickable Links)
Liệt kê đầy đủ đường dẫn clickable `[Tên File](file:///...)` tới từng tệp trên máy tính của người dùng:
- 📁 **Thư mục hồ sơ chính:** `[Tên_Thư_Mục](file:///...)`
- 📄 **Báo cáo chính (`README.md`):** `[README.md](file:///...)`
- 🧪 **File kiểm thử / tái hiện (`test_*.py` / `reproduce.py`):** `[Tên_File_Test](file:///...)`
- 🩹 **Bản vá (`fix.patch`):** `[fix.patch](file:///...)`
- 📦 **Gói nén `.zip` chuẩn nộp Google:** `[Tên_Gói.zip](file:///...)`
- 💬 **File nội dung trả lời / điền form (`COMMENT_REPLY_*.md`):** `[Tên_File_Reply](file:///...)`

---

### 📋 Phần 4: Nội Dung Copy-Paste Để Gửi Lên Google Bug Hunters / Buganizer
Đóng khung ` ````markdown ` nguyên văn nội dung (Tiêu đề, Technical Details, Impact, hoặc Comment Reply) để người dùng chỉ cần copy 1 lần và dán thẳng lên trang web của Google.

---

### 🤖 Phần 5: Prompt Bàn Giao Cho Bên Kiểm Định Độc Lập (Codex ChatGPT 6.1.0 Mức 2)
Luôn kết thúc bằng một khung ` ```text ` chứa câu Prompt chỉ rõ đường dẫn tuyệt đối của các file vừa tạo và các yêu cầu kiểm tra khắt khe để người dùng copy gửi ngay cho AI thứ 2 (Codex) kiểm tra chéo.
