# Prompt gửi cho bên kiểm tra

Copy phần dưới đây và điền ba dòng đầu:

---

THƯ MỤC BỘ BÀN GIAO: <đường dẫn thực tế hoặc ZIP đã đính kèm>
ĐẦU VÀO CẦN KIỂM TRA: <thư mục/tệp README và ZIP đã cung cấp>
PHẠM VI: <ID hồ sơ; tệp phải giữ nguyên; có yêu cầu đề xuất/sửa bản vá hay chỉ rà soát>

Hãy dùng skill `google-oss-vrp-audit` trong bộ bàn giao để kiểm định các hồ sơ này. Nếu môi trường không cài skill, đọc trực tiếp `skills/google-oss-vrp-audit/SKILL.md` rồi làm theo các tài liệu được dẫn ở đó.

Đọc quy trình, tiêu chí verdict và giới hạn helper trước khi kết luận. Đối chiếu quy tắc Google hiện hành từ nguồn chính thức, ghi ngày truy cập và phân biệt rõ quy tắc Google với checklist nội bộ. Không sử dụng bản tóm tắt cũ làm căn cứ duy nhất cho điều kiện chương trình hôm nay.

Trước tiên đọc tệp thực tế, ghi kích thước và SHA-256. Đừng xác nhận hash, nội dung hoặc test chỉ vì tôi đã mô tả chúng. Khi không truy cập được tệp, nguồn, API hoặc cấu hình cần thiết, ghi rõ phần đó chưa kiểm chứng.

Kiểm tra gói đính kèm và nguồn ở commit cố định; sau đó tự lần theo input của attacker → producer → artifact/metadata → consumer → quyền/phê duyệt → hành động trái phép được tuyên bố. Xem mã của action bên thứ ba và các cổng bảo vệ liên quan. Phân biệt kết quả job, step thực thi, secret được tham chiếu và secret thực sự khả dụng.

Yêu cầu này bao gồm kiểm tra cơ học và các phép thử offline an toàn cần để xác minh bộ phân tích/guard/bản vá, bằng dữ liệu giả trong thư mục tạm. Không chạy mù mã PoC đính kèm. Không kích hoạt workflow upstream, khai thác tài nguyên thật, gửi thông báo hoặc nộp báo cáo ra ngoài nếu chưa có chỉ dẫn riêng cho hành động đó. Nếu môi trường cấm một phép kiểm tra, ghi giới hạn và tiếp tục phần còn lại.

Với bản vá, kiểm tra cả khả năng áp dụng và hành vi: sự kiện được hỗ trợ, đường lỗi/skipped, aggregate `needs`, nguồn REPO/SHA, quyền token, gate và luồng hợp lệ. Không coi `git apply --check` là chứng minh bản vá an toàn.

Với mỗi mục, trả `PASS`, `FAIL`, `UNVERIFIED` hoặc `N/A` kèm bằng chứng. Phân biệt: đóng gói; độ chính xác khẳng định; tác động; bản vá; điều kiện chương trình. Một câu mô tả rủi ro có điều kiện có thể đúng trong khi tác động runtime vẫn chưa xác minh. Không tự bỏ điều kiện để làm hồ sơ mạnh hơn và không đưa tỷ lệ “100% Google nhận”.

Xuất REVIEW theo mẫu trong `assets`, bảng claim–evidence, kết quả helper, manifest trước/sau nếu có sửa, cùng danh sách việc sửa cụ thể: tệp/dòng, lý do, thay thế tối thiểu và bằng chứng nào sẽ đủ để đóng mục đó. Không tự sửa hồ sơ đã được yêu cầu giữ nguyên. Kết luận rõ sẵn sàng gửi, cần sửa hoặc thiếu bằng chứng, và xếp ưu tiên theo tác động đã có bằng chứng cùng điều kiện chương trình.

Nếu kiểm tra lại: bám danh sách lỗi đã thống nhất; đóng các lỗi đã sửa đúng. Chỉ mở thêm mục khi có bằng chứng mới, nêu rõ lý do. Nếu có queue hoặc nội dung điền form, so sánh với bản được duyệt để tránh tái đưa các claim đã thu hẹp vào nội dung nộp.

---
