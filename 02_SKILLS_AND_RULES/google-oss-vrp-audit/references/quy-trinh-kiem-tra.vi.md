# Quy trình kiểm định để bên khác làm lại được

Tài liệu này là **phương pháp nội bộ**. Tiêu chí verdict: [tieu-chi-dat-khong-dat.vi.md](tieu-chi-dat-khong-dat.vi.md). Không yêu cầu mọi hồ sơ có cùng số tệp, số link hoặc cùng bố cục.

## 1. Chốt đầu vào và phạm vi

- Đọc các tệp thật; ghi vị trí tương đối, bytes, SHA-256 và thời gian. Không lấy manifest do người gửi kể lại làm kết quả tự kiểm chứng.
- Ghi ID hồ sơ, điều được phép sửa và tệp phải giữ nguyên. Kiểm tra lại thì đọc REVIEW vòng trước và tạo bảng mục cần đóng.
- Tách nguồn upstream nguyên bản, bằng chứng API, bản trích đã lọc, log offline và bản vá đề xuất. Không gọi một JSON tự tổng hợp là raw/full response.
- Làm trên bản sao hoặc thư mục tạm; giữ snapshot đầu vào. Bản sửa, nếu được yêu cầu, có manifest riêng.

## 2. Xác định chương trình và thời điểm

- Đọc bản tóm tắt Google rồi cập nhật nguồn chính thức tại ngày rà soát. Ghi URL, phần quy tắc liên quan, ngày áp dụng và ngày truy cập.
- Phân loại theo tác động có bằng chứng: product, supply chain, credential, insider risk hoặc hardening. Tên “supply chain” trong tiêu đề không tự tạo ra tác động supply chain.
- Kiểm tra repo/tier/phiên bản hiện tại và kênh gửi phù hợp. Nguồn không truy cập được hoặc tier chưa rõ: ghi `UNVERIFIED`, không tự điền giá trị.

## 3. Kiểm tra gói và nhận diện phiên bản nguồn

- Kiểm tra tên member, trùng lặp, đường dẫn vượt thư mục, symlink, dung lượng; xem danh sách trước khi giải nén.
- So sánh bytes README ngoài/trong ZIP. Kiểm tra JSON, encoding, line endings và metadata thu thập. Ghi khác biệt; không xóa comment/license/emoji nguyên bản của upstream.
- Chạy helper theo hướng dẫn. Đọc JSON chi tiết, không lấy exit code hoặc dòng tổng hợp làm verdict cuối.
- Mỗi tệp nguồn: xác định repo + commit cố định + đường dẫn. Kiểm tra mapping suy đoán của helper; basename trùng không đủ xác định nguồn.
- Tải nguồn tại commit và so bytes. Với mỗi trích dẫn quan trọng, tự so đúng đoạn với đúng file và vùng `#L...`; “range nằm trong file” khác “range dẫn đúng đoạn”.
- Nêu rõ nguồn tại commit báo cáo và tình trạng mới nhất khác nhau nếu upstream đã sửa. Không dùng `main` thay cho commit để chứng minh câu trích lịch sử.

## 4. Lập hợp đồng cho từng khẳng định

Mỗi claim có một dòng trong `assets/CLAIM_EVIDENCE.csv`, với chuỗi:

```text
Vai trò attacker + trường điều khiển được
  → sự kiện và phiên bản workflow thực thi
  → producer: bước nào ghi lại dữ liệu, bước nào ghi đè
  → artifact/cache/metadata: run nào, bytes nào, định danh nào
  → consumer: chọn đúng nguồn, repo, PR và SHA ra sao
  → gate/permissions/environment/secret/IAM tại đúng job
  → lệnh hoặc API đặc quyền
  → tài sản và hành động trái phép quan sát được
```

- Đọc cả producer và consumer, workflow tái sử dụng, action bên thứ ba ở SHA được pin. Khi repo có quy tắc dùng graph, kiểm tra project/generation/coverage rồi bổ sung exact source khi thiếu.
- Liệt kê sẵn gate `if:`, nhãn, role, reviewer, environment, giới hạn sự kiện và quyền token. Kiểm tra gate có ràng buộc revision đang chạy hay chỉ là nhãn cũ.
- Có lệnh checkout/test không đồng nghĩa có secret. Có tham chiếu secret không đồng nghĩa secret có giá trị hoặc đã bị đọc. Có quyền host không suy ra quyền trong VM.
- Thành công job không chứng minh step nhạy cảm chạy. `skipped` không tự chỉ ra nguyên nhân. `head_branch: main` của consumer không chứng minh code đến từ fork.
- Đổi label/comment hoặc ghi artifact riêng có thể nằm trong chức năng dự kiến. Chứng minh vượt ranh giới quyền trước khi gán mức tác động cao hơn.

## 5. Xác minh bằng chứng trong giới hạn được phép

- Ưu tiên exact source, đọc API công khai, metadata run/job/step và bằng chứng có sẵn. Gắn run/PR/artifact bằng định danh cụ thể; tương quan actor/thời gian chỉ hỗ trợ liên kết.
- PoC offline dùng dữ liệu giả để kiểm tra parser, traversal, guard và các nhánh; không gửi secret hay kích hoạt CI thật. Nếu cần kiểm chứng runtime còn thiếu quyền hoặc thông tin riêng, ghi rõ điều kiện và phần chưa xác minh.
- Với LLM, tách tool được cấp, chuỗi input tới model, boundary của công cụ và hành động sai thực sự. Không biến một prompt gợi ý thành kết quả agent đã thực hiện.
- Lưu lệnh, đầu vào, đầu ra, phiên bản công cụ và giới hạn. Báo đúng số ca đã chạy; không dùng số test của tác giả làm số test do reviewer chạy.

## 6. Kiểm tra bản vá

- So khối diff trong README với `fix.patch`. Áp dụng kiểm tra trên snapshot đúng base; ghi mapping đầy đủ khi đường dẫn trong ZIP được rút gọn.
- Đánh giá các sự kiện thực sự được workflow hỗ trợ: push, merge queue, PR, dispatch, workflow_run, reusable call. Không tự yêu cầu hỗ trợ sự kiện vốn không có.
- Kiểm tra success/failure/cancel/skipped, aggregate `needs`, output thiếu, nguồn REPO/SHA và approval. Guard phải ngăn hành động sau đó; action từ chối rồi return success không đủ.
- Gate mới có chặn CI hợp lệ hay yêu cầu admin provisioning chưa nêu? Bản vá bảo toàn workflow_call phải xét `github.event_name` kế thừa caller.
- Nếu kiểm thử được yêu cầu, chọn ca hợp lệ, ca tấn công, ca biên và hồi quy dựa vào input thật; xem xét bytes, NUL, LF/CRLF, symlink hoặc branch namespace khi liên quan. Ghi nền tảng chạy; Windows và Linux có thể khác.
- `git apply --check` chỉ chứng minh diff áp dụng. Không nâng thành xác nhận tương thích YAML/Actions hay hết lỗ hổng.

## 7. Kết luận và đóng vòng sửa

- Trả REVIEW và claim–evidence; mỗi lỗi có vị trí, bằng chứng, ảnh hưởng đến kết luận, sửa tối thiểu và điều kiện đóng rõ ràng.
- Phân biệt câu mô tả đã đúng có điều kiện với tác động vẫn chưa chứng minh. Có thể giữ báo cáo hẹp hơn thay vì thêm claim lớn thiếu bằng chứng.
- Xác nhận hash cuối và tệp phải giữ nguyên. Nếu có queue/form, so lại từng trường và ZIP trước khi gửi để tránh lệch với bản được duyệt.
- Vòng sau chỉ đóng các mục đã thống nhất và ghi riêng phát hiện mới có bằng chứng. Không hứa “sửa nốt một câu là Google chắc chắn nhận”.
