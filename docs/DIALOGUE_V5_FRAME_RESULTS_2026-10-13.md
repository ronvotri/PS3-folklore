# Folklore — V5 đã kiểm chứng, mở rộng V6 trên toàn bộ CMC (13/10/2026)

## Báo cáo thực từ PC người dùng

Đã nhận `GUI_CHO_CHATGPT_dialogue-frame-hypothesis.json` (`schema=1`, `game_id=BCUS98147`, `kind=REDACTED_CMC_FRAME_HYPOTHESIS`). Đây là kết quả công cụ V5 đọc báo cáo private đã tạo từ dữ liệu game gốc, **không mang source text hoặc raw hex**.

| File | Candidate samples | Cặp gap ≤8 byte kiểm tra | Khớp `00 04 00 XX` | Loại marker |
|---|---:|---:|---:|---|
| `tk100_en.bin_` | 48 | 0 | 0 | không áp dụng (tool chỉ khảo sát CMC) |
| `tk101_en.bin_` | 48 | 0 | 0 | không áp dụng |
| `LCmc000_en.bi5_` | 11 | 6 | **6/6** | 3 marker printable ở source mod3; 3 control mod0 |
| `LCmc004_en.bi5_` | 24 | 20 | **20/20** | 10 printable ở source mod3; 10 control mod0 |
| **Tổng CMC** | 35 | **26** | **26/26** | 13 + 13 |

V5 không ghi nhận mismatch trong tập khảo sát, nhưng **7 cặp CMC có gap >8 byte không được kiểm tra** (4 ở CMC000, 3 ở CMC004). Các file talk không được tool này khảo sát; số 0 ở talk **không đồng nghĩa không tồn tại frame**.

### Giả thuyết cần giữ và cần bác bỏ nếu sai

- Bằng chứng được tăng cường cho một khung 4-byte căn 4 có dạng `00 04 00 XX` ngay sát văn bản ASCII-NUL của nhiều câu CMC.
- Với 13 marker printable, chính ký tự đầu của `source` ở vị trí mod4=3 là byte cuối của khung, **có khả năng là metadata bị trích xuất nhầm vào văn bản**. Với 13 marker control, ký tự source bắt đầu ở mod4=0, 4 byte trước đó chứa `00 04 00 XX` và `XX` có giá trị control. Chưa chứng minh `XX` thể hiện speaker, điều khiển nhánh, hiệu ứng hoặc length field.
- **Không tự động xóa prefix trong catalog, không viết lại offset, không coi khung này là message grammar hoàn chỉnh.**

## V6: kiểm toán toàn bộ CMC (chỉ đọc, FAIL-CLOSED)

Mã mới: `tools/cmc_frame_audit.py`; hồi quy: `tests/test_cmc_frame_audit.py` (**4/4 synthetic tests PASS**). V6 mở rộng từ cặp mẫu ngắn sang **tất cả 134 catalog CMC / 1.795 ứng viên gốc** theo `translations/index.json`, gồm những candidate có khoảng cách dài hơn 8 byte.

Trên máy người dùng, bộ chạy V6:
1. Tự tải mã mới nhất từ repo GitHub.
2. Chỉ đọc `etc.bin_` và `etc.fht_` trong game gốc. Trước khi tính match, kiểm tra kích thước archive baseline, SHA-256 tệp CMC, ID catalog, source hash, byte ASCII+NUL tại offset và section talk hợp lệ.
3. Với mỗi candidate: kiểm tra vị trí `file_offset % 4` và khung trước đó; lưu **thống kê tổng và lý do không khớp** theo từng file CMC, không xuất câu tiếng Anh, byte hex hay chuỗi gốc.
4. Chỉ tạo `local-data/dialogue-cmc-frame-audit.json` **nếu tất cả 134 file qua kiểm tra nguồn**. Launcher sao chép báo cáo an toàn thành `GUI_CHO_CHATGPT_cmc-frame-audit.json` để người dùng gửi.

Nếu xuất hiện khác biệt, **giữ nguyên dữ liệu và báo cáo lý do**; nếu SHA/source sai, từ chối tiếp tục và không tạo report. Không có mã nào ghi/sửa game, không liên quan font Merienda V3 hoặc save.

**Giới hạn:** V6 là candidate frame **audit**, không phải parser hoàn chỉnh hay serializer message; chỉ có thể mở giai đoạn thiết kế grammar khi thống kê quy luật trên nhiều CMC thực tế đạt độ tin cậy. File talk cần luồng giải mã khác, vì cách đóng gói chưa được xác định.

### Kiểm thử và bước tiếp theo

- `python -m unittest discover -s tests -p test_cmc_frame_audit.py -v`: 4/4 PASS trên fixture tổng hợp gồm frame printable/control, CMC section rỗng, SHA fail-closed, báo cáo ở đường dẫn an toàn và không thay đổi archive.
- **Chưa kiểm thử V6 trên bản game thật hoặc toàn bộ unit test cũ trên checkout GitHub mới.**
- Khi có báo cáo V6, phân tích mismatch và chọn các case có nguồn rõ để xây parser read-only cho record, rồi kiểm chứng roundtrip byte-exact; chỉ sau đó mới triển khai repacker an toàn cho hội thoại.
- 158 catalog / 11.886 mục Việt hóa vẫn ở trạng thái có bản nháp; **không đồng nghĩa 100% playable**.
