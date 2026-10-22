# REVIEW — <tên/phạm vi>

## Kết luận

**Sẵn sàng gửi / Cần sửa / Cần bổ sung bằng chứng / Chỉ hardening** — chọn và giải thích theo phạm vi đã kiểm tra. Không dùng tỷ lệ bảo đảm Google chấp nhận.

## Phạm vi và phiên bản

- Ngày UTC, reviewer, môi trường/công cụ:
- Tệp thực đọc và manifest kèm theo:
- Phạm vi được yêu cầu; tệp phải giữ nguyên:
- Nguồn Google đã đọc, ngày áp dụng/truy cập và route còn chưa rõ:
- Hành động/nguồn không kiểm tra được:

## Bảng kết quả

| Hồ sơ | Gói | Nguồn/citation | Claim chính | Tác động runtime | Patch apply | Patch semantics | Program | Kết luận |
|---|---|---|---|---|---|---|---|---|
| <ID> | <verdict> | <verdict> | <verdict> | <verdict> | <verdict> | <verdict> | <verdict> | <phạm vi> |

Verdict: PASS / FAIL / UNVERIFIED / N/A. Dẫn bằng chứng ở các mục dưới, không chỉ để nhãn.

## Các mục phải sửa hoặc làm rõ

### <ID lỗi> — <tên>

- Tiêu chí và verdict:
- Tệp/dòng/câu hiện tại:
- Nguồn đối chiếu: repo@commit:path#lines hoặc URL/API + UTC:
- Bằng chứng/ca phản ví dụ:
- Vì sao ảnh hưởng kết luận:
- Sửa tối thiểu hoặc phạm vi claim có thể giữ:
- Bằng chứng/kiểm tra đủ để đóng mục:

## Chuỗi tấn công và các điều kiện

Vai trò attacker → input → producer → dữ liệu được chuyển → consumer → gate/quyền → sink → tài sản/hành động ngoài quyền.

Liệt kê điều đã xác minh, điều có điều kiện, điều bị phản bác và điều chưa xác minh. Chi tiết theo `CLAIM_EVIDENCE.csv`.

## Kiểm tra cơ học

- README ngoài/trong, hash/bytes, ZIP members:
- Nguồn exact bytes và mapping đã kiểm tra thủ công:
- Citation exact đoạn và dòng:
- JSON/log provenance, dữ liệu full hay extract:
- Khối diff so patch (newline cuối có được so không):
- Git apply base/mapping/output:
- Helper JSON và giới hạn/cache/skipped checks:

## Kiểm tra hành vi bản vá / PoC offline

| Case | Input/event | Mong đợi theo hợp đồng | Quan sát | Verdict | Giới hạn |
|---|---|---|---|---|---|
| <ID> | <fixture> | <kết quả> | <output đã chạy> | <verdict> | <môi trường> |

Phân biệt test đã tự chạy, kết quả tác giả cung cấp và mục chưa chạy.

## Đóng lỗi từ vòng trước

| Mục cũ | Bản sửa/bằng chứng | Đóng/chưa đóng | Lý do |
|---|---|---|---|
| <ID> | <nguồn> | <trạng thái> | <cụ thể> |

Phát hiện mới chỉ thêm khi có bằng chứng; nêu vì sao nằm trong phạm vi.

## Bản cuối và ưu tiên

- Manifest cuối và xác nhận các tệp yêu cầu giữ nguyên:
- Queue/form/attachment đã đối chiếu hay chưa áp dụng:
- Còn blocker nào; thiếu bằng chứng cụ thể nào:
- Thứ tự gửi đề xuất và lý do theo tác động/route đã xác minh:
- Giới hạn: quyết định triage, duplicate, novelty và reward thuộc Google.
