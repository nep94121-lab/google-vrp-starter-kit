# Đạt, không đạt và chưa xác minh (Bản v3.0 — Cập nhật từ Triage thực tế của Google)

Mỗi verdict phải gắn với **một tiêu chí có tên, phạm vi và bằng chứng**. Đây là tiêu chuẩn kiểm định nội bộ, không phải thang điểm thưởng của Google.

## Bốn verdict

| Verdict | Khi dùng | Ví dụ |
|---|---|---|
| `PASS` | Bằng chứng đáp ứng đúng tiêu chí đã nêu | README ngoài và trong ZIP có cùng bytes |
| `FAIL` | Bằng chứng mâu thuẫn hoặc vi phạm cổng chặn bắt buộc | Chỉ có `GITHUB_TOKEN` bình luận PR trên repo phụ (sẽ bị đóng `Infeasible`) |
| `UNVERIFIED` | Chưa có dữ liệu cần để quyết định | Không biết IAM thực tế hay secret thuộc scope nào |
| `N/A` | Tiêu chí không áp dụng, kèm lý do | Không có bản vá nên không chấm patch compatibility |

`Conditional` là thuộc tính khẳng định, không thay thế verdict: câu “có thể lộ nếu secret ở repo/org” có thể PASS về độ chính xác câu chữ, trong khi khả năng lộ secret tại deployment đang xét vẫn UNVERIFIED.

## Ma trận quyết định (Bổ sung 4 Cổng Thực Tế Từ Google Bug Hunters)

| Mục | Điều kiện đạt (`PASS`) | Cần sửa / Loại bỏ (`FAIL`) khi | Thiếu bằng chứng (`UNVERIFIED`) khi |
|---|---|---|---|
| Định danh tệp | Hash tự tính trên tệp đã đọc | Manifest không khớp phiên bản được mô tả | Chỉ có đường dẫn hoặc hash do người gửi kể |
| Đồng bộ gói | Bản ngoài/trong đúng phiên bản, các khác biệt có chủ đích được giải thích | README/patch/bằng chứng của nhiều phiên bản bị trộn | Chưa đọc được ZIP |
| Nguồn và citation | Đúng repo/commit/file, code/comment khớp và vùng dòng dẫn đúng đoạn | Trích sai, sửa comment không ghi rõ, sai commit hoặc số dòng | Không lấy được nguồn hay mapping mơ hồ |
| **Cổng 1: Chống trùng lặp (`Canonical 1469`)** | Lỗi nằm ở bản vá mới merge (`<14 ngày`), hoặc trong logic code Python/JS/TS/Bash phụ trợ, hoặc workflow mới tinh | Lỗi chỉ là mẫu YAML bề mặt cũ (`workflow_run`/`pull_request_target` cơ bản) trên repo lớn mà `zizmor` quét thấy ngay | Chưa kiểm tra lịch sử commit/PR gần nhất của file bị ảnh hưởng |
| **Cổng 2: Chống `Infeasible` & Tuyến `Cloud VRP P2` / `Supply Chain`** | Repo thuộc `GoogleCloudPlatform/*` / có xác thực Google Cloud (`google-github-actions/auth`, WIF, `GCP_SA_KEY`, Vertex AI, GKE, Cloud Run) **HOẶC** chứng minh được tác động Supply Chain thật sự (chiếm quyền ghi nhánh `main`, lộ token phát hành gói PyPI/npm/Docker/Release) | Workflow chỉ có `GITHUB_TOKEN` thông thường để bình luận/đánh nhãn hoặc sửa biến nội bộ trên repo nhỏ không nối với Cloud hay hệ thống Release (sẽ bị đóng `Infeasible` vì coi là Product Vuln theo luật 01/10/2026) | Chưa kiểm tra xem workflow có kết nối với Cloud WIF, Release Secret hay quyền ghi nhánh chính hay không |
| **Cổng 3: Bằng chứng chạy trên `github.com` (Chống bị nhắc *"Try the attack on github.com"*)** | Có mô tả rõ luồng kích hoạt đầu-cuối trên `github.com` (Event $\rightarrow$ Workflow $\rightarrow$ Script $\rightarrow$ Sink) **VÀ** có bằng chứng chạy workflow thực tế trên repo fork cá nhân (`github.com/<user>/<repo-fork>`) kèm `reproduce.py` | Chỉ chạy unit-test gọi hàm Python/JS rời rạc ở máy local mà không chứng minh được cách kích hoạt qua GitHub Actions trên `github.com` | Mới chỉ có kết quả chạy hàm rời ở local, chưa chạy thử workflow trên repo fork cá nhân |
| **Cổng 4: Chống `WAI` do Rate Limit (`Outstanding Bugs <= 2`)** | Trước khi nộp, số bài đang ở trạng thái `New` + `Assigned` trên bảng Bug Hunters $\le 2$ bài | Đang có đủ 3 bài mở (`New` + `Assigned`) mà vẫn nộp tiếp bài thứ 4 (sẽ bị Bot tự động đóng `WAI` ngay lập tức) | Chưa kiểm tra số bài đang mở trên bảng Bug Hunters |
| Attacker control | Vai trò và input được chứng minh | Input bị producer ghi đè trước khi consumer đọc | Chưa có producer hoặc chưa biết artifact nào tới consumer |
| Ranh giới bảo vệ | Các gate/quyền liên quan được xét đủ trong phạm vi | Claim bỏ qua gate thật đang ngăn đường tấn công | Gate/IAM/private configuration chưa xác minh |
| Kết quả trái phép | Chứng minh được hành động ngoài quyền hoặc nêu đúng điều kiện chưa biết | Chỉ là chức năng thiết kế, hoặc bằng chứng phản bác kết quả tuyên bố | Chưa có observable outcome và điều kiện chưa giải quyết |
| Evidence runtime | Exact run/job/step và provenance hỗ trợ đúng câu | Suy từ run success sang secret exfiltration, hoặc bịa nguyên nhân skipped | Không liên kết được upstream và downstream |
| Patch applicability | Áp dụng sạch trên snapshot đúng | Hunk/base/path sai | Thiếu source base |
| Patch semantics | Chặn đường lỗi đã nêu, giữ các luồng hợp lệ đã kiểm tra | Bypass còn hoặc hồi quy cụ thể | Chưa kiểm tra hành vi/sự kiện cần thiết |
| Scope hiện hành | Nguồn chính thức có ngày, loại tác động và route phù hợp | Chọn sai chương trình hoặc đổi tên impact để lách điều kiện | Tier/route/điều kiện chưa rõ |
| Câu chữ | Kết luận bám mức bằng chứng, điều kiện hiện rõ | Nâng rủi ro giả định thành sự việc đã xảy ra | Chưa đọc nội dung thực tế |
| Nội dung sắp gửi | Queue/form/attachment khớp phiên bản đã duyệt | Mất điều kiện impact, gửi nhầm ZIP | Chưa có bản copy cuối để so |

## Khi nào kết luận sẵn sàng gửi?

1. Không còn `FAIL` làm sai câu chuyện kỹ thuật, chứng cứ hoặc lựa chọn chương trình.
2. Vượt qua đủ **4 Cổng Thực Tế**:
   - **Cổng 1:** Không phải lỗi YAML bề mặt cũ dễ bị `Duplicate (canonical: 1469)`.
   - **Cổng 2:** Có tác động **Google Cloud VRP (`P2`)** (xác thực GCP WIF / Cloud SA / `GoogleCloudPlatform`) hoặc **Supply Chain thật sự** (chiếm quyền ghi nhánh chính / lộ token phát hành gói), không bị rơi vào bẫy `Infeasible (Product Vuln)`.
   - **Cổng 3:** Đã chỉ rõ luồng kích hoạt trên `github.com` và có bằng chứng chạy thử trên repo fork cá nhân (tránh bị nhắc *"Try the attack on github.com"*).
   - **Cổng 4:** Tổng số bài đang mở (`New` + `Assigned`) hiện tại $\le 2$ bài (tránh bị đóng `WAI` do Rate Limit).
3. Các claim chính đủ bằng chứng; điều kiện chưa biết đã được nêu rõ.
