# QUY TẮC ĐIỀN BIỂU MẪU GOOGLE VRP (`https://bughunters.google.com/report`) — BẢN v3.0

## 1. Quy Tắc Sống Còn Về Giới Hạn Tốc Độ Nộp Bài (Tránh Bị Đóng `WAI` Do Rate Limit)
- Với tài khoản mới chưa có lịch sử nhận thưởng, Google áp dụng giới hạn **tối đa 3 báo cáo đang mở (`New` + `Assigned` — `outstanding bugs`)** tại cùng một thời điểm.
- Nếu đã có 3 bài ở trạng thái `New` hoặc `Assigned` (ví dụ: 1 bài `New` + 1 bài `Assigned` là 2 bài, vẫn còn 1 slot; nhưng nếu đủ 3 bài đang mở) mà cố nộp bài thứ 4 ngay lập tức, `Google Security Bot` (`sp...@google.com`, `component: 310544`) sẽ tự động đóng bài thứ 4 thành `WAI (Intended Behavior)` kèm thông báo:
  > *"Whoa, slow down bughunting champion... Once your other outstanding bugs have been triaged or closed, you can submit additional reports."*
- **Chiến lược đúng:**
  1. Trước khi nộp bài mới, mở bảng `bughunters.google.com` đếm số bài đang có trạng thái **`New`** hoặc **`Assigned`**.
  2. Chỉ nộp khi tổng số bài `New` + `Assigned` hiện tại **$\le 2$ bài**.

---

## 2. Quy Tắc Tránh Bị Đóng `Infeasible` (Quy Định Mới Của Google OSS VRP Từ 01/10/2026)
- Từ **01/10/2026**, chương trình **OSS VRP** của Google đã ngừng nhận các lỗi `Product Vulnerability` thông thường và **chỉ nhận các lỗi thuộc 2 nhóm sau**:
  1. **Lỗi Chuỗi Cung Ứng (Supply Chain Compromise):** Phải chứng minh được khả năng sửa đổi code nhánh chính (`main`), chèn mã vào bản phát hành (Release / Package PyPI, npm, Docker), vượt cổng duyệt PR của maintainer để chạy trong ngữ cảnh có đặc quyền ghi repo hoặc lộ `secrets.*` của hệ thống CI/CD.
  2. **Lỗi Tác Động Sang Google Cloud VRP (Được nâng lên `P2` và chuyển sang `component: 1609699 → 1610896`):** Khi lỗ hổng nằm trong các kho của `GoogleCloudPlatform/*` hoặc các workflow có xác thực với hạ tầng Google Cloud (`google-github-actions/auth`, `workload_identity_provider`, `GCP_SA_KEY`, Vertex AI, GKE, Cloud Run).
- **Lưu ý khi viết mục `Impact analysis` ở Bước 4:**
  - Phải nêu rõ ràng **tác động lên Supply Chain hoặc Google Cloud / CI Secrets** ngay dòng đầu tiên của ô `Impact analysis`, tránh để hệ thống tự động phân류 nhầm thành lỗi sản phẩm thông thường (`Infeasible`).

---

## 3. Quy Tắc Tránh Bị Nhắc *"Try the attack on github.com"* Khi Báo Cáo Lỗi Code/Tool CI
- Khi lỗ hổng nằm trong một script Python/JS được gọi bởi GitHub Actions (như `tools.py`), nếu bạn chỉ mô tả hàm Python đó riêng lẻ, kỹ sư Triage có thể yêu cầu:
  > *"Feel free to update this report with additional details and ensure it includes: - Try the attack on github.com"*
- **Cách xử lý chuẩn & an toàn 100%:**
  1. Luôn ghi rõ **Luồng Kích Hoạt Đầy Đủ Trên `github.com` (End-to-End GitHub Trigger Flow)** ngay ở đầu bài: Sự kiện GitHub nào (`issues`, `pull_request`, `workflow_run`, `release`) $\rightarrow$ kích hoạt file `.github/workflows/<tên_file>.yml` nào $\rightarrow$ truyền biến nào vào script $\rightarrow$ chạm tới hàm lỗi nào.
  2. Để thuyết phục tuyệt đối 100%, hãy **Fork repo đó về tài khoản GitHub cá nhân của bạn (`github.com/<user-của-bạn>/<repo>`)**, chạy thử nghiệm workflow đó trên chính **repo fork của bạn** (tuyệt đối không chạy tấn công lên repo gốc của Google), và đính kèm link/log của lần chạy GitHub Actions trên fork vào báo cáo!

---

## 4. Năm Bước Điền Form Chuẩn Không Bao Giờ Lỗi

### Bước 1 (`About you`):
- Giữ nguyên thông tin cá nhân đã đăng ký $\rightarrow$ Nhấn **`CONTINUE`**.

### Bước 2 (`Report description`):
- Ô `Write here*` giới hạn **tối đa 200 ký tự**.
- Công thức tiêu đề chuẩn:
  `<org>/<repo>: <Cơ chế bị thiếu/lỗi> in <tên_file> allows <hậu quả Supply Chain / Cloud CI cụ thể>`
- Nhấn **`CONTINUE`**.

### Bước 3 (`Bug location`):
- Phần `Where do you want to report your vulnerability?`:
  - Chọn **nút tròn thứ 7 từ trên xuống**:
    `OSS VRP – Report security issues affecting open source software stored in the public repositories of Google-owned GitHub organizations and selected repositories hosted on other platforms. See program rules`
    *(Nếu repo thuộc `GoogleCloudPlatform/*` và ảnh hưởng trực tiếp tới tài nguyên Cloud/GCP, kỹ sư Triage sẽ tự động chuyển bài của bạn sang hàng đợi `Google Cloud VRP` ở mức `P2`).*
- Phần `Which URL (or repository) have you found the vulnerability in?`:
  - Dán đúng URL của repo chính (`https://github.com/<org>/<repo>`) — không có dấu `/` ở cuối.
- Nhấn **`CONTINUE`**.

### Bước 4 (`The problem`):
1. **Ô lớn 1 (`Please describe the technical details of the vulnerability`):**
   - Dán phần **`## Summary` + `## Affected Files` + `## Technical Details` + `## Verification Evidence`** từ file `README.md`.
2. **Ô lớn 2 (`Impact analysis`):**
   - **QUAN TRỌNG:** Xóa toàn bộ đoạn chữ mẫu mặc định trong ô trước khi dán!
   - Dán phần **`## Impact` + `## Suggested Fix`** từ file `README.md` (nêu rõ tác động Supply Chain / Cloud CI).
3. **Phần `Upload file`:**
   - Nhấn **`SELECT FILE`** và chọn đúng file **`<tên-gói>.zip`** đã qua kiểm định 100% PASS.
4. **Xử lý hộp thoại cảnh báo (nếu hiện ra):**
   - Nếu sau khi bấm `CONTINUE` mà trang web hiện hộp thoại hỏi xác nhận phạm vi (`Is this vulnerability in scope?` hoặc cảnh báo liên quan đến repo):
   - Tích chọn **dòng tròn thứ 2** (`Something else` / `Continue submitting`) rồi nhấn **`SUBMIT` / `CONTINUE`** để đi tiếp sang Bước 5.

### Bước 5 (`The cause`):
1. `Choose the type of vulnerability` (`Select vulnerability type*`):
   - Chọn `Permissions Bypass`, `Sandbox Escape`, hoặc `Command Injection` tùy đúng bản chất kỹ thuật của lỗ hổng.
2. `Does anyone else know about this vulnerability?`:
   - Tích chọn **dòng 1**: `No, this vulnerability is private.`
3. `Do you plan to disclose this vulnerability publicly?`:
   - Tích chọn **dòng 2**: `No, I am only notifying Google`
4. `Do you want to donate your reward to charity?`:
   - **Không tích** (bỏ trống).
5. Nhấn nút **`SUBMIT`** và chờ 3–5 giây để trang chuyển về `https://bughunters.google.com/` kèm thông báo `Report submitted`.
