# Folklore BCUS98147 — kết quả chẩn đoán game gốc lần 1 (12/10/2026)

## Nguồn kiểm chứng
Người dùng chạy **Folklore Diagnostic V2** trên bản game local, gửi **chỉ** `GUI_CHO_CHATGPT_dialogue-structure-summary.json` (schema 1, kind `STRUCTURAL_METADATA_ONLY`). Báo cáo không chứa text/hex, nêu `parser_validated=false` và `repacker_available=false`.

Công cụ `dialogue_probe.run()` chỉ tạo báo cáo khi SHA-256 của tệp nguồn, offset chuỗi ASCII và NUL khớp với catalog của repo; 4 tệp đã đi qua bước xác thực đó và xuất summary. Không thể suy ra parser/serializer message đúng từ một báo cáo chỉ có offset.

| File | Kích thước (byte) | Chuỗi ứng viên đã xác thực | Mẫu khảo sát | Tổng section | Section talk |
|---|---:|---:|---:|---:|---:|
| `talk/en/tk100_en.bin_` | 67.416 | 314 | 48 | 1 vùng nguồn giả định | 1 |
| `talk/en/tk101_en.bin_` | 101.684 | 447 | 48 | 1 vùng nguồn giả định | 1 |
| `cmc/en/LCmc000_en.bi5_` | 1.362.336 | 11 | 11 | 16 | 1 |
| `cmc/en/LCmc004_en.bi5_` | 1.916.304 | 24 | 24 | 21 | 1 |
| **Tổng** | | **796** | **131** | | |

### CMC shell / empty section

- `LCmc000`: text-talk là section index **1**, ranh giới `[12.160, 13.344)`; có **6 section rỗng ở cuối** với offset start=end=1.362.336.
- `LCmc004`: text-talk là section index **1**, ranh giới `[15.136, 16.672)`; có **6 section rỗng ở cuối** với offset start=end=1.916.304.
- Đây là bằng chứng trực tiếp giải thích tại sao bản chẩn đoán V1 dừng ở điều kiện `x >= y`. Bản V2 cho phép `x == y` và đã chạy qua cả hai tệp. **Chưa chứng minh cấu trúc message/command**.

### Cấu trúc các khoảng trống được quan sát

- Ở hai CMC mẫu, các chuỗi hội thoại ứng viên thường rất sát nhau: trong `LCmc000` có 6/10 khoảng giữa hai **mẫu liên tiếp** dài không quá 8 byte; `LCmc004` có 20/23 khoảng tương ứng. Khoảng trung vị lần lượt khoảng **6** và **5** byte. Đây là vùng đáng ưu tiên khảo sát để tìm byte điều khiển / kết thúc lệnh, nhưng **chưa gọi là opcode đã xác minh**.
- Các mẫu `tk100` và `tk101` có khoảng cách lớn hơn: không có cặp mẫu liên tiếp nào trong 47 cặp mỗi tệp chỉ cách nhau ≤8 byte. Có **19 cặp mẫu trùng cả offset lẫn vị trí NUL** giữa hai tệp talk; có thể chứa cấu trúc chung, nhưng muốn giải mã phải xem byte điều khiển ở máy local.
- Trong cả hai file talk mẫu, bộ dò offset 32-bit file-relative **không phát hiện byte-pattern match** ở 48 ứng viên được chọn. Đây không phải bằng chứng không có con trỏ: có thể là base khác, kiểu dữ liệu khác hoặc script format khác.
- Một số match u32 ở CMC tồn tại nhưng phần lớn không căn 4 byte hoặc nằm ở section không phải talk; **không đủ bằng chứng** biến chúng thành pointer fixup.

## Điều đã đạt, và chưa đạt

**Đạt:** Người dùng đã xác minh bản gốc có ít nhất 796 ứng viên ASCII-NUL ở đúng vị trí và header/section của hai CMC mẫu được chấp nhận. Khung CMC còn có thể giữ nguyên byte khi chỉ tách/ghép vỏ opaque; chưa thay thế text.

**Chưa đạt:** speaker, opcode, branch/choice, thứ tự câu, length-field, encoding Vietnamese, pointer relocation, roundtrip message command stream, safe binary repack, RPCS3 gameplay proof. Không ghi vào offset của candidate tiếng Anh bằng chuỗi UTF-8 dài hơn.

## Bước kỹ thuật tiếp theo

1. Thêm công cụ **chỉ đọc** `tools/dialogue_gap_fingerprint.py` lấy mẫu raw probe **ở máy người dùng**, báo lại duy nhất số lượng/loại byte và độ dài trong **khoảng ngắn giữa hai candidate đã xác thực**. Không bao gồm text, dữ liệu hex, byte gốc, hash bytes, file game. Bộ kiểm thử giả lập gồm 4 trường hợp đạt.
2. Cho chạy công cụ sau V2, thu `dialogue-gap-fingerprint.json` đã lọc cùng summary hiện tại. V3 sẽ khảo sát các pattern khoảng trống, có thể xây giả thuyết về record message/prefix; mọi giả thuyết cần so trên nhiều file.
3. Chỉ khi đủ nguồn để dựng grammar command, viết parser read-only và kiểm tra **parse -> serialize byte-for-byte** trên nhiều file nguyên gốc mới mở nhánh repacker viết.
4. Giữ Merienda Regular 400 V3 và 25 alias, sao lưu game gốc, người dùng tự điều khiển RPCS3. Không upload `etc.bin_`, `etc.fht_`, `dialogue-probe.json`.

## Số liệu dịch

158 catalog / 11.886 bản nháp đã đồng bộ ở GitHub; **không đồng nghĩa 100% game playable**. Dữ liệu binary gốc không có trong repo.
