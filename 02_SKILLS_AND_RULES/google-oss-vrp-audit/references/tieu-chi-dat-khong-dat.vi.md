# Đạt, không đạt và chưa xác minh

Mỗi verdict phải gắn với **một tiêu chí có tên, phạm vi và bằng chứng**. Đây là tiêu chuẩn kiểm định nội bộ, không phải thang điểm thưởng của Google.

## Bốn verdict

| Verdict | Khi dùng | Ví dụ |
|---|---|---|
| `PASS` | Bằng chứng đáp ứng đúng tiêu chí đã nêu | README ngoài và trong ZIP có cùng bytes |
| `FAIL` | Bằng chứng mâu thuẫn hoặc có phản ví dụ cho tiêu chí | Câu nói step đã chạy nhưng API step ghi skipped |
| `UNVERIFIED` | Chưa có dữ liệu cần để quyết định | Không biết IAM thực tế hay secret thuộc scope nào |
| `N/A` | Tiêu chí không áp dụng, kèm lý do | Không có bản vá nên không chấm patch compatibility |

`Conditional` là thuộc tính khẳng định, không thay thế verdict: câu “có thể lộ nếu secret ở repo/org” có thể PASS về độ chính xác câu chữ, trong khi khả năng lộ secret tại deployment đang xét vẫn UNVERIFIED.

## Ma trận quyết định

| Mục | Điều kiện đạt | Cần sửa khi | Thiếu bằng chứng khi |
|---|---|---|---|
| Định danh tệp | Hash tự tính trên tệp đã đọc | Manifest không khớp phiên bản được mô tả | Chỉ có đường dẫn hoặc hash do người gửi kể |
| Đồng bộ gói | Bản ngoài/trong đúng phiên bản, các khác biệt có chủ đích được giải thích | README/patch/bằng chứng của nhiều phiên bản bị trộn | Chưa đọc được ZIP |
| Nguồn và citation | Đúng repo/commit/file, code/comment khớp và vùng dòng dẫn đúng đoạn | Trích sai, sửa comment không ghi rõ, sai commit hoặc số dòng | Không lấy được nguồn hay mapping mơ hồ |
| Chống trùng lặp (`Canonical 1469`) | Lỗi nằm ở bản vá mới merge (<14 ngày), hoặc trong logic code Python/JS/TS/Bash phụ trợ, hoặc chuỗi đa tầng ở repo ngách | Lỗi chỉ là mẫu YAML bề mặt cũ (`workflow_run`/`pull_request_target` cơ bản) trên repo lớn mà `zizmor` quét thấy ngay | Chưa kiểm tra lịch sử commit/PR gần nhất của file bị ảnh hưởng |
| Attacker control | Vai trò và input được chứng minh | Input bị producer ghi đè trước khi consumer đọc | Chưa có producer hoặc chưa biết artifact nào tới consumer |
| Ranh giới bảo vệ | Các gate/quyền liên quan được xét đủ trong phạm vi | Claim bỏ qua gate thật đang ngăn đường tấn công | Gate/IAM/private configuration chưa xác minh |
| Kết quả trái phép | Chứng minh được hành động ngoài quyền hoặc nêu đúng điều kiện chưa biết | Chỉ là chức năng thiết kế, hoặc bằng chứng phản bác kết quả tuyên bố | Chưa có observable outcome và điều kiện chưa giải quyết |
| Evidence runtime | Exact run/job/step và provenance hỗ trợ đúng câu | Suy từ run success sang secret exfiltration, hoặc bịa nguyên nhân skipped | Không liên kết được upstream và downstream |
| Patch applicability | Áp dụng sạch trên snapshot đúng | Hunk/base/path sai | Thiếu source base |
| Patch semantics | Chặn đường lỗi đã nêu, giữ các luồng hợp lệ đã kiểm tra | Bypass còn hoặc hồi quy cụ thể | Chưa kiểm tra hành vi/sự kiện cần thiết |
| Scope hiện hành | Nguồn chính thức có ngày, loại tác động và route phù hợp | Chọn sai chương trình hoặc đổi tên impact để lách điều kiện | Tier/route/điều kiện chưa rõ |
| Câu chữ | Kết luận bám mức bằng chứng, điều kiện hiện rõ | Nâng rủi ro giả định thành sự việc đã xảy ra | Chưa đọc nội dung thực tế |
| Nội dung sắp gửi | Queue/form/attachment khớp phiên bản đã duyệt | Mất điều kiện impact, gửi nhầm ZIP | Chưa có bản copy cuối để so |

LF, emoji, tên mục, số file, số link và scanner marker là quan sát QA. Chỉ kết luận lỗi chặn khi có sai lệch thực tế hoặc vi phạm yêu cầu cụ thể; không biến lựa chọn trình bày thành lỗi bảo mật hay quy định Google.

## Khi nào kết luận sẵn sàng gửi?

- Không còn FAIL làm sai câu chuyện kỹ thuật, chứng cứ hoặc lựa chọn chương trình.
- Vượt qua bộ lọc **Chống trùng lặp (`Canonical 1469`)**: không nộp các lỗi cấu hình `.yml` bề mặt đã tồn tại lâu ngày trên các repo phổ biến vốn đã bị các máy quét tự động (`zizmor`, `actionlint`) báo cáo trước.
- Các claim chính đủ bằng chứng; điều kiện chưa biết đã được nêu rõ và không phải tiền đề bị thiếu của kết luận chính.
- Những giới hạn còn lại được liệt kê, tệp cuối đã nhận diện, và nếu có bản vá thì mức kiểm chứng của nó được nói đúng.
- Nếu tác động chính còn UNVERIFIED: kết luận **cần bổ sung bằng chứng** hoặc **chỉ sẵn sàng ở phạm vi claim đã thu hẹp**, nêu chính xác phạm vi. Không ép đạt bằng cách đổi nhãn thành PASS.

“Tất cả kiểm tra cơ học PASS” chỉ có nghĩa ở lớp cơ học. Không gộp các lớp thành “100% nhận thưởng”; duplicate, novelty, mức ảnh hưởng và quyết định triage không thể bảo đảm từ bộ này.

## Thứ tự ưu tiên

Ưu tiên:
1. Lỗi bypass bản vá bảo mật mới merge gần đây (`Incomplete Security Fix`) hoặc lỗi logic trong mã nguồn phụ trợ CI/CD (`Python/JS/TS/Go`) có bằng chứng thực thi rõ ràng, ít giả định, tác động ngoài quyền rõ và route hiện hành phù hợp.
2. Sau đó đến claim có điều kiện được nêu trung thực.
3. Loại bỏ sớm các lỗi cấu hình YAML bề mặt dễ trùng lặp (`canonical: 1469`) hoặc hành vi đúng thiết kế.
