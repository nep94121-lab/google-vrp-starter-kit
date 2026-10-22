# Công cụ, cách đọc và giới hạn

## audit_packages.py

Chạy từ gốc bộ bàn giao, Python 3.10+ và Git trong PATH:

```powershell
python .\skills\google-oss-vrp-audit\scripts\audit_packages.py "D:\reports" --profiles 02 03 --output ".\audit-result\mechanical.json" --cache ".\audit-result\cache" --fetch-upstream
```

Các thư mục con được chọn theo hai ký tự đầu. Mỗi thư mục cần README và đúng một ZIP. Nếu cấu trúc khác, tạo bản sao đầu vào đúng cấu trúc hoặc điều chỉnh mapping có ghi nhận; không sửa bản gốc âm thầm.

| Phần JSON | Cách hiểu |
|---|---|
| `error` | Hồ sơ không hoàn tất lượt helper; đọc lỗi |
| `readme_identical` | So bytes README ngoài/trong ZIP |
| `entries` | Kích thước/hash/newline/marker của từng member |
| `evidence_json` | JSON parse được; không xác thực dữ liệu API |
| `patch.block_matches` | Có khối diff khớp, bỏ qua số LF cuối |
| `patch.apply_check` | Áp dụng kiểm tra trên cây tạm và mapping đã ghi |
| `source_checks` | So nguồn tải về và member tại commit được map |
| `reference_ranges` | Kiểm tra giới hạn số dòng, không kiểm tra nghĩa citation |
| `excerpt_checks` | Đoạn YAML/Python tìm thấy trong nguồn đã tải; chưa gắn đúng từng citation |

### Những giới hạn phải nói rõ

- Exit code **0 không có nghĩa mọi mục PASS**. Chương trình có thể hoàn tất nhưng JSON chứa error/FAIL/UNVERIFIED.
- Không có `--fetch-upstream` thì các kiểm tra mạng không chạy. Danh sách rỗng không phải tất cả nguồn đạt.
- Cache tái sử dụng bytes cũ. Khi cần tải lại dùng thư mục cache mới hoặc ghi rõ lần lấy nguồn. Commit bất biến vẫn cần xác định mapping đúng.
- Chỉ nhận một số định dạng nguồn và đoạn fenced YAML/Python; không phát hiện hết nguồn hoặc mọi inline quote. Tệp bỏ qua phải được xét thủ công nếu quan trọng.
- Mapping có thể dựa basename hoặc suy `.github/workflows/`. Kiểm tra `path_inferred`, `mapping` và candidates; không xem suy đoán là provenance đã chứng minh.
- So diff bằng cách bỏ LF cuối không phải phép so byte-for-byte toàn bộ patch. Muốn tuyên bố exact bytes, trích khối diff và so lại bytes bao gồm newline kết thúc.
- Các marker chỉ là gợi ý xem xét. Không xóa metadata upstream hợp lệ. CRLF có thể là bytes thật của nguồn.
- Helper chặn một số lỗi ZIP phổ biến, tổng dung lượng khai báo trên 100 MB và symlink. Nó không thay thế sandbox/antivirus, không xác thực chữ ký và không phải bộ phân tích ZIP thù địch toàn diện. Không thực thi mã đính kèm.
- `git apply --check` không chạy workflow, parser sản phẩm hay PoC. Không xác minh quyền token/IAM, giá trị secret, branch protection, approval thực tế, exploitability, YAML compatibility, route chương trình hoặc độ mới.
- Không có Git/network/quyền API là giới hạn kiểm chứng; không tự gọi đó là lỗi của hồ sơ.

## Xác nhận công cụ không hỏng

```powershell
python -B .\skills\google-oss-vrp-audit\scripts\self_test.py
```

Self-test dùng fixture tạm, không gọi Google/GitHub, không chạy mã từ hồ sơ. Kiểm tra ZIP, patch đúng/sai base, lệch README/newline, mapping mơ hồ và 13 ca byte guard minh họa. Các ca này xác nhận helper/case minh họa; không phải 13 phép thử runtime trên hồ sơ của bạn.

## Kiểm tra toàn vẹn bộ bàn giao

```powershell
python .\tools\verify_bundle.py
```

So tệp hiện có với `MANIFEST.sha256.json`; tệp thêm sẽ được liệt kê nhưng không tự gây lỗi. Manifest không ký số, dùng để phát hiện hỏng/lệch phiên bản khi chuyển tệp. Nó không chứng minh người phát hành đáng tin hoặc an toàn của nội dung.
