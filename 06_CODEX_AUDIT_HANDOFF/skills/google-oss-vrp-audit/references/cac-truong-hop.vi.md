# Các quyết định mẫu từ những lỗi từng gặp

Đây là ví dụ đã khái quát từ quá trình rà soát, **không phải kết luận về một repo hiện tại**, không kèm dữ liệu hồ sơ riêng. Chỉ áp dụng khi có cùng ranh giới kỹ thuật.

| Quan sát | Suy luận chưa đủ / sai | Cách kiểm tra và quyết định |
|---|---|---|
| Action từ chối slash command rồi return | Mọi step phía sau cũng bị chặn | Đọc action pin và output; kiểm tra step sau có `if` authorization. Từ chối mà job success có thể vẫn đi tiếp |
| User là contributor/member | Đủ quyền write | Kiểm tra quyền hiệu lực; association và permission khác nhau |
| Consumer run trên main, conclusion success | Chắc chắn đã test mã fork và có secret | Gắn producer run, payload/artifact, checkout và từng step. Phần chưa gắn được là UNVERIFIED |
| Hai deploy job skipped | Do một gate cụ thể hoặc thiếu quyền | Cần biểu thức + context/log hỗ trợ nguyên nhân; trạng thái skipped riêng lẻ không đủ |
| Producer có `paths-ignore` | Chỉ chạy trên danh sách path cho phép | Đọc chính xác event filter; tránh diễn giải ngược nghĩa |
| Workflow dùng secret trong env | Đã chứng minh đọc hoặc lấy secret | Kiểm tra scope và đường sink. Dùng câu có điều kiện nếu giá trị runtime chưa biết |
| Có auth trên host, exploit chạy trong VM | Exploit đọc được credential host | Kiểm tra mount/forwarding/network/escape; host và guest là hai ranh giới |
| Dịch vụ chủ ý build exploit, xuất artifact theo run | Đây tự thân là supply chain compromise | Xem threat model; cần vượt boundary, sửa artifact tin cậy hay dữ liệu người khác |
| Tool của agent cho phép ghi file | Prompt injection đã thành công | Tách quyền tool, input tới model, ràng buộc đường dẫn và hành động ngoài quyền quan sát được |
| `urljoin` cho link ngoài | Token đã bị gửi tới host ngoài | Xem có HTTP request gì, header/auth, redirect; trả link khác không tự chứng minh leak |
| File trong `.git/hooks` được ghi | Hook mới chắc chắn chạy | Kiểm tra executable bit và Git operation. `.git/config`/fsmonitor là đường khác, cần xem riêng |
| Artifact có số PR do attacker viết | Consumer nhận đúng bytes đó | Tìm bước producer ghi đè metadata và binding với triggering PR/run |
| Run namespace có PR number | Không thể đụng baseline main | Kiểm tra mọi bước dùng branch name/key; metadata thật không làm tên branch tùy chọn trở nên an toàn |
| Parser trả chuỗi `triage` | Có job triage tương ứng | Lập ma trận output → job `if` → needs → fallthrough trong từng repo |
| Chuỗi `$()` đi vào GITHUB_OUTPUT | RCE chắc chắn | Theo output tới lệnh thực thi; shell không tự eval đệ quy nội dung biến |
| Patch sạch | Mọi sự kiện vẫn chạy và đã hết bypass | Kiểm tra các nhánh sự kiện, skipped/failure, aggregate `needs`, nguồn SHA và provisioning |

## Ví dụ guard đọc số PR

Nếu hợp đồng input là “toàn bộ file chỉ có chữ số ASCII và tối đa một LF kết thúc”, `IFS= read -r` chỉ đọc dòng đầu nên có thể bỏ sót `42\nEXTRA=sample` không LF cuối. Shell command substitution cũng có thể làm thay đổi bytes, như bỏ NUL. Kiểm tra bytes trước chuyển thành biến là cách kiểm chứng hợp đồng này:

```python
data = path.read_bytes()
valid = re.fullmatch(rb"[0-9]+\n?", data) is not None
```

Đây là minh họa validation, chưa phải toàn bộ bản vá: vẫn cần binding số PR với repo/run và xem consumer. Self-test kèm bộ bàn giao có 13 input giả, gồm hợp lệ, multiline, CRLF, NUL, Unicode và shell text. Đừng gọi chúng là kết quả của một workflow thật.

## Ví dụ verdict đúng mức

- **PASS — wording:** “Step tham chiếu secret; nếu secret được cấp tại repo/org thì mã không tin cậy có thể nhận nó.” Câu giữ đúng điều kiện.
- **UNVERIFIED — runtime secret exposure:** API công khai chưa chứng minh secret có giá trị hoặc scope thực tế.
- **FAIL — câu tuyệt đối:** “Run success chứng minh đã exfiltrate secret.” Không có chứng cứ cho bước suy luận đó.
- **PASS — patch applicability**, **UNVERIFIED — patch semantics:** Diff áp dụng được nhưng chưa kiểm tra event/failure paths.

Nếu bản được duyệt có điều kiện mà queue gửi bài bỏ mất điều kiện, phải nêu sự khác biệt để chủ hồ sơ quyết định. Không tự xác nhận rằng toàn bộ nội dung gửi vẫn đã qua kiểm định.
