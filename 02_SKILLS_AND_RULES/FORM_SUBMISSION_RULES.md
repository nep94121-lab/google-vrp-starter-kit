# QUY TẮC VÀNG KHI ĐIỀN FORM NỘP BÀI TRÊN `bughunters.google.com/report`

> Tài liệu này đúc kết các quy tắc thực chiến trên giao diện **Google Product Form** để không bị vướng bộ lọc cảnh báo tự động (`Out of Scope` / `Open redirect`) và không bị chạm giới hạn tốc độ (`Rate Limit`).

---

## 1. Quy Tắc Số Lượng Nộp Cùng Lúc (Rate Limit 3 Bài `New`)

- Với tài khoản mới trên Google Bug Hunters, hệ thống giới hạn tối đa **3 báo cáo đang ở trạng thái `New` (`🟨 SUBMITTED` / `outstanding bugs`) cùng một lúc** (hoặc giới hạn số bài gửi liên tiếp trong 1 giờ).
- **Quy tắc bắt buộc:**
  1. Chỉ nộp tối đa **3 bài chất lượng nhất** trong một đợt.
  2. Nếu có bài bị Bot đóng `Duplicate` ngay sau 6–10 phút thì chỗ trống đó được trả lại, có thể nộp bù bài khác để duy trì đủ **3 bài đang ở trạng thái `New` (`🟨 SUBMITTED`)**.
  3. **Khi đã có đủ 3 bài đang giữ trạng thái `New` quá 15 phút:** **DỪNG LẠI NGAY**, không nộp thêm bài thứ 4! Nếu cố nộp thêm khi đã có 3 bài `New`, hệ thống sẽ tự động đóng bài mới bằng trạng thái `WAI (Intended Behavior)` kèm thông báo:
     > *"Whoa, slow down bughunting champion... Once your other outstanding bugs have been triaged or closed, you can submit additional reports."*
  4. Đợi khi ít nhất 1 trong 3 bài `New` được kỹ sư Google duyệt xong (`Assigned` / `Accepted` hoặc `Closed`) mới nộp tiếp bài tiếp theo.

---

## 2. Cấu Trúc 5 Mục Cố Định Trên Giao Diện `Google Product Form`

Truy cập: `https://bughunters.google.com/report` $\rightarrow$ Nhấn nút **`REPORT SECURITY VULNERABILITY`**.

### Mục 1: `About you`
- Kiểm tra Tên và Email $\rightarrow$ Nhấn **`CONTINUE`**.

### Mục 2: `Report description` (Giới hạn cứng 200 ký tự!)
- Ô `Write here*` chỉ cho phép tối đa **200 ký tự** (`0 / 200`).
- Luôn viết tiêu đề gọn trong khoảng **130 – 190 ký tự** theo mẫu:
  `<org>/<repo>: <Cơ chế bị lỗi> in <tên_file> allows <hậu quả kỹ thuật trong CI/CD>`
- Nhấn **`CONTINUE`**.

### Mục 3: `Bug location`
1. Phần **`Where do you want to report your vulnerability?`**:
   - Tích chọn **nút tròn thứ 7 từ trên xuống dưới**:
     ```text
     OSS VRP – Report security issues affecting open source software stored in the public repositories of Google-owned GitHub organizations and selected repositories hosted on other platforms. See program rules
     ```
2. Phần **`Which URL (or repository) have you found the vulnerability in?`**:
   - Dán đường dẫn repo GitHub: `https://github.com/<org>/<repo>`
- Nhấn **`CONTINUE`**.

### Mục 4: `The problem` (Gồm 2 ô văn bản lớn + 1 nút Upload file)
1. **Ô lớn thứ 1 (`Please describe the technical details of the vulnerability`):**
   - Dán phần `## Summary`, `## Affected Files`, `## Technical Details`, `## Verification Evidence`, và `## Suggested Fix`.
2. **Ô lớn thứ 2 (`Impact analysis`):**
   - **BẮT BUỘC xóa dòng chữ gợi ý mặc định** `[Please remove this hint and the guidance below before submitting your report.] Briefly explain who can exploit the vulnerability, and what they gain when doing so.` trước khi dán!
   - Dán đúng 3 gạch đầu dòng chuẩn sau:
     ```markdown
     - **Who can exploit the vulnerability:** ...
     - **Privileged CI/CD Token Scope Abused:** ...
     - **What the attacker gains:** ...
     ```
3. **Phần `Upload file` (`SELECT FILE`):**
   - Tải lên file `<tên-gói>.zip` (dưới 50MB).
- Nhấn **`CONTINUE`**.

### Mục 5: `The cause`
1. **`Choose the type of vulnerability` (`Select vulnerability type*`):**
   - Chọn **dòng thứ 5 từ trên xuống dưới**: `Permissions Bypass`
   - Hoặc **dòng thứ 11 từ trên xuống dưới**: `Sandbox Escape` (nếu là lỗi thoát vùng confinement/sandbox)
   - Hoặc **dòng thứ 26 cuối cùng**: `Other`
2. **`Does anyone else know about this vulnerability?`:**
   - Chọn **nút tròn thứ 1 từ trên xuống dưới**: `No, this vulnerability is private.`
3. **`Do you plan to disclose this vulnerability publicly?`:**
   - Chọn **dòng thứ 2 từ trên xuống dưới**: `No, I am only notifying Google`
- Nhấn **`SUBMIT`**!

---

## 3. Hai Bẫy Từ Khóa Của Bộ Lọc Tự Động Trước Khi Nộp (Pre-Submit Checker Traps)

Khi bạn nhấn `CONTINUE` ở Mục 4 hoặc `SUBMIT` ở Mục 5, trang web của Google có một bộ lọc từ khóa tự động. Hãy tránh 2 bẫy từ khóa sau để không bị hiện bảng cảnh báo:

1. **Bẫy 1 — Câu phủ định trong ô `Impact analysis` gây báo `Out of Scope`:**
   - Không viết các câu phủ định kiểu *"This bug does not execute arbitrary code..."* hay *"does not bypass..."* trong ô `Impact analysis`, vì bộ lọc tự động sẽ bắt cụm từ *"does not..."* và bật popup hỏi `Is this vulnerability in scope?`.
   - Thay vào đó, hãy nêu rõ các điều kiện tiên quyết dưới dạng khẳng định (`If <secret/condition> is configured...`, `When triggered via...`).
2. **Bẫy 2 — Từ khóa `redirect` / `allow_redirects` gây báo nhầm lỗi Web `Open redirect`:**
   - Khi mô tả các hàm HTTP Python/JS trong CI/CD (như `requests.head`), tránh dùng từ `redirect` hoặc `allow_redirects=True` vì bộ lọc từ khóa sẽ tưởng nhầm bạn đang báo lỗi chuyển hướng URL trên trình duyệt (`Open redirect`) và cảnh báo từ chối. Hãy dùng thuật ngữ `outbound HTTP request origin replacement` hoặc `host confinement`.
