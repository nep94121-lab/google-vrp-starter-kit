# Quy tắc Google: bản tóm tắt có nguồn

Đối chiếu **22/10/2026**; metadata tải nguồn: [policy-sources.json](policy-sources.json). Đây là tóm tắt, không phải toàn văn. Khi nộp, đọc lại nguồn chính thức và kiểm tra cập nhật mới.

## 1. Quy tắc OSS VRP đang hiển thị

Phạm vi gồm Google OSS bản mới và cấu hình kho. Supply chain cần chứng minh tổn hại mã/build/gói cùng khả năng vượt yêu cầu duyệt PR ngoài; chỉ chạy sau maintainer duyệt được xem là insider risk để xét credit. Từ **01/10/2026**, OSS VRP dừng nhận product vulnerability mới; hồ sơ cũ không bị ảnh hưởng. Một số repo tác động Cloud có thể chuyển Cloud VRP. Hẹn cập nhật Q1/2027 không phải ngày mở lại. Lỗ hổng nền tảng bên thứ ba khác lỗi tích hợp của Google; kiểm tra mục dependency và các giới hạn nghiên cứu trong toàn văn. [Nguồn chính thức](https://bughunters.google.com/about/rules/open-source/google-open-source-software-vulnerability-reward-program-rules).

## 2. Bài cập nhật OSS năm 2026

Google yêu cầu kiểm chứng đầu ra AI và tác động thực tế, xét đường mã có thể tới và mô hình bảo mật dự án. Bài nêu OT0–OT3 và thay đổi tháng 4: OT2/OT3 không thưởng hoặc credit cho product/other security issues. Đối chiếu bảng tier hiện hành; không tự suy tier từ tên repo. Đây là lịch sử cập nhật, phải đọc cùng quy tắc mới hơn. [Nguồn chính thức](https://bughunters.google.com/blog/ossvrp-rule-updates-2026); [bảng repo](https://github.com/google/bughunters/blob/main/oss-repository-tier/external_repositories.txtpb).

## 3. Khung chất lượng báo cáo năm 2025

Bài công bố nêu Google, Cloud, AI và Abuse VRP. Các chiều đánh giá gồm mô tả, tiền điều kiện, tác động, tái hiện/PoC, thông tin mục tiêu, đầu ra và phản hồi của researcher. Có thể dùng các chiều này để rà soát; không tự áp hệ số thưởng của bài cho OSS. [Nguồn chính thức](https://bughunters.google.com/blog/level-up-your-reports-introducing-our-updated-report-quality-framework).

## Cách cập nhật

Mở các liên kết trên, lưu URL, thời điểm UTC và nội dung liên quan vào hồ sơ kiểm định. Nếu trang chỉ trả vỏ JavaScript, các URL API công khai trong `policy-sources.json` cho phép đối chiếu bài viết trên chính tên miền Google. Hash trong JSON nhận diện phản hồi đã đọc, không xác thực quy tắc tương lai.

## Quy ước của bộ kiểm định

Các tiêu chí kỹ thuật ở tài liệu kế tiếp là phương pháp nội bộ. Không có căn cứ trong các nguồn đã đọc để gọi “bốn dấu hiệu AI”, không emoji, đúng năm/sáu mục, LF, hoặc xóa header công cụ là bộ luật Google tự động đánh trượt. Giữ nguyên license, comment và bytes nguồn khi trích dẫn.
