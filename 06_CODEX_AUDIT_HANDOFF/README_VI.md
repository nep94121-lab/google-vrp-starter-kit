# Bộ bàn giao kiểm định Google OSS VRP

Phiên bản đóng gói: **22/10/2026**. Ngôn ngữ hướng dẫn: tiếng Việt; skill giữ tên `google-oss-vrp-audit`.

## Bắt đầu

1. Đưa **toàn bộ thư mục này hoặc ZIP tương ứng** cho bên kiểm tra, cùng README/ZIP thực tế của các hồ sơ cần rà soát.
2. Dán nội dung [PROMPT_BAN_GIAO.md](PROMPT_BAN_GIAO.md), thay đường dẫn đầu vào và phạm vi cho đúng.
3. Yêu cầu bên nhận trả về báo cáo theo mẫu, danh sách lỗi cụ thể và manifest của chính những tệp đã đọc.

Đây là bộ phương pháp và công cụ dùng lại. Không kèm hồ sơ riêng, tài khoản, email, tracker nộp bài hay dữ liệu đăng nhập. Bên nhận không thể đọc đường dẫn trên máy gửi nếu chưa được cung cấp tệp hoặc quyền truy cập thực tế.

## Có gì trong thư mục

| Thành phần | Dùng để làm gì |
|---|---|
| [Skill](skills/google-oss-vrp-audit/SKILL.md) | Hướng dẫn chính cho AI |
| [Quy tắc Google và nguồn](skills/google-oss-vrp-audit/references/google-rules-snapshot.vi.md) | Bản tóm tắt có ngày đối chiếu và liên kết chính thức |
| [Quy trình kiểm tra](skills/google-oss-vrp-audit/references/quy-trinh-kiem-tra.vi.md) | Cách đi từ tệp gốc đến kết luận |
| [Đạt / không đạt / chưa xác minh](skills/google-oss-vrp-audit/references/tieu-chi-dat-khong-dat.vi.md) | Tiêu chí kết luận từng mục |
| [Công cụ và giới hạn](skills/google-oss-vrp-audit/references/cong-cu-va-gioi-han.vi.md) | Cách chạy và đọc kết quả đúng |
| [Các trường hợp thực tế đã khái quát](skills/google-oss-vrp-audit/references/cac-truong-hop.vi.md) | Các suy luận thường gây kết luận sai |
| [Mẫu REVIEW](skills/google-oss-vrp-audit/assets/REVIEW_TEMPLATE.md) | Đầu ra thống nhất để bên gửi sửa được |
| [Bảng claim–evidence](skills/google-oss-vrp-audit/assets/CLAIM_EVIDENCE.csv) | Theo dõi từng khẳng định và khoảng trống bằng chứng |
| `MANIFEST.sha256.json` | Kích thước và SHA-256 của các tệp trong bộ bàn giao |
| `validation/RESULTS.json` | Các kiểm tra đã chạy trên chính bộ công cụ |

## Dùng trong Codex

Sao chép riêng thư mục `skills/google-oss-vrp-audit` vào thư mục skill của môi trường nhận, thường là `~/.codex/skills/`. Nếu đã có skill cùng tên, đối chiếu và sao lưu trước khi thay thế. Khởi động lại phiên nếu môi trường chưa nhận skill mới. Gọi bằng `$google-oss-vrp-audit`.

Không cần cài skill để đọc bộ này: AI khác có thể đọc `SKILL.md` cùng các tài liệu tham chiếu như hướng dẫn làm việc. Việc hỗ trợ chạy Python, Git hoặc tải nguồn tùy môi trường; mục nào không thực hiện được phải ghi `UNVERIFIED`.

## Chạy công cụ từ thư mục bộ bàn giao

Yêu cầu: **Python 3.10+**, **Git CLI** có trong PATH. Helper chỉ dùng thư viện chuẩn Python; không cần API key. Ví dụ PowerShell:

```powershell
python .\skills\google-oss-vrp-audit\scripts\audit_packages.py "D:\reports" --profiles 02 03 --output ".\audit-result\mechanical.json" --cache ".\audit-result\cache" --fetch-upstream
```

Đổi `D:\reports` thành thư mục cha chứa các thư mục hồ sơ. Mỗi thư mục hồ sơ bắt đầu bằng ID hai chữ số, có `README.md` và đúng một `.zip`. Có thể dùng ID khác qua `--profiles`. Chi tiết và hạn chế ở tài liệu công cụ; helper không có kết luận tổng thể tự động.

Để xác nhận bộ bàn giao không hỏng khi chuyển máy:

```powershell
python .\tools\verify_bundle.py
```

Các kiểm tra offline của công cụ, nếu muốn chạy lại:

```powershell
python -B .\skills\google-oss-vrp-audit\scripts\self_test.py
```

## Hiểu đúng kết quả cuối cùng

“Hoàn tất kiểm định” nghĩa là các mục trong phạm vi đã có kết quả, lỗi đã được xử lý hoặc ghi rõ, và tệp được nhận diện bằng hash. Chỉ kết luận **sẵn sàng gửi với phạm vi đã nêu** khi không còn lỗi chặn, các khẳng định chính có bằng chứng đủ và cách chọn chương trình đã được đối chiếu. Không có phép kiểm tra cục bộ nào bảo đảm Google nhận, trả thưởng hoặc xác nhận không trùng.

Bản quy tắc trong bộ là bản tóm tắt để đọc sẵn; liên kết chính thức là căn cứ để cập nhật. Không coi các quy ước LF, số mục README, số liên kết, emoji hoặc chữ “Executive Summary” là quy định tự động đánh trượt của Google.
