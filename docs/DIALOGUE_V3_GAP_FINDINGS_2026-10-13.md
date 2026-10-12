# Folklore — kiểm chứng hai báo cáo V3 từ game gốc (13/10/2026)

## Nguồn và phạm vi

Người dùng cung cấp hai báo cáo **đã lọc**, không chứa văn bản game hoặc cửa sổ byte/hex:
- `GUI_CHO_CHATGPT_dialogue-structure-summary(1).json` — `STRUCTURAL_METADATA_ONLY`.
- `GUI_CHO_CHATGPT_dialogue-gap-fingerprint.json` — `REDACTED_GAP_CLASS_STATISTICS`.

Cùng `schema=1`, `game_id=BCUS98147`. Báo cáo V3 dựa trên kiểm chứng source SHA/ASCII-NUL của bản gốc đã chạy ở PC người dùng, nhưng hai JSON chỉ là **metadata**; chúng không chứa payload để tự giải mã opcode/pointer.

Dùng `tools/dialogue_gap_crosscheck.py` mới để kiểm tra chéo nội dung hai JSON: tệp phải cùng thứ tự, số mẫu và cặp nội-section khớp, histogram độ dài phải đúng `right.file_offset - (left.nul_at+1)`, nhóm byte phải cộng đúng bằng số byte mỗi gap, không nhận report chưa lọc, không chấp nhận mẫu chồng lấn. **Đã chạy thực tế đối với hai JSON gửi lên: PASS, 127/127 cặp được khớp**. Unit tests mới ở `tests/test_dialogue_gap_crosscheck.py`: **4/4 PASS trên fixture tổng hợp**. Đây là kiểm tra thống kê, không phải kiểm thử in-game.

## Số liệu đối chiếu

| File | Sample khảo sát | Cặp sample cùng section | Gap ≤8 byte | Gap ≤32 byte |
|---|---:|---:|---:|---:|
| `tk100_en.bin_` | 48 (trên 314 source đã xác minh) | 47 | 0 | 0 |
| `tk101_en.bin_` | 48 (trên 447 source đã xác minh) | 47 | 0 | 0 |
| `LCmc000_en.bi5_` | 11/11 | 10 | 6 | 9 |
| `LCmc004_en.bi5_` | 24/24 | 23 | 20 | 22 |
| **Tổng** | **131 mẫu** | **127 cặp** | **26** | **31** |

**Quan trọng:** `tk100/101` là các **mẫu được lựa chọn**, không phải toàn bộ ứng viên; độ dài giữa hai mẫu được chọn không đồng nghĩa khoảng cách giữa các record thật. Không được kết luận talk không có command ngắn chỉ vì 94 cặp mẫu đều cách nhau trên 32 byte.

### Một quy luật CMC cần kiểm chứng

Trong **26/26 khoảng gap ngắn ≤8 byte** của hai CMC:
- 13 gap có **đúng 1 byte control** (giá trị trong 0x01–0x1f hoặc 0x7f) và các byte còn lại đều là 0; `right_text_at % 4 == 3`.
- 13 gap có **đúng 2 byte control** và còn lại toàn 0; `right_text_at % 4 == 0`.
- Không có byte `printable`/`space`/`high` trong nhóm 26 gap này.

Cặp `(control_count, alignment)` khớp **100% trên tập mẫu hiện có**. Điều này **gợi ý** các chuỗi CMC có metadata/control và căn chỉnh 4 byte theo một khuôn, **KHÔNG chứng minh** byte nào là speaker, opcode, length, branch hay con trỏ. Không tự động bơm UTF-8 vào các slot gốc.

### Ngoại lệ cần điều tra

- **31/33** cặp mẫu CMC có gap ≤32 byte; 2 gap dài hơn lần lượt **33** (CMC000) và **356** (CMC004), không được phân loại byte bởi V3.
- Trong 31 gap ≤32, có **28 gap chỉ chứa zero/control**. **3 gap chứa byte chữ in được**: hai gap CMC000 dài **23 và 31 byte** (tổng 19 printable + 2 space) và một gap CMC004 dài **19 byte** (1 printable).
- Những byte in được có thể là mảnh chuỗi ngắn, tên biến, tên hiệu ứng hay metadata của engine; **chưa đủ bằng chứng** để khẳng định là hội thoại bị sót. Không thêm vào catalog nếu chưa xác minh bản gốc và vai trò phát trên màn hình.
- Các match giá trị u32 trùng offset trong báo cáo V2 vẫn chỉ là **byte pattern**, phần lớn thiếu đối chứng cấu trúc. Không dùng làm pointer fixup.

## Công cụ đã tạo

```powershell
python tools/dialogue_gap_crosscheck.py --gap "GUI_CHO_CHATGPT_dialogue-gap-fingerprint.json" --structure "GUI_CHO_CHATGPT_dialogue-structure-summary(1).json" --out "local-data/dialogue-v3-crosscheck.json"
python -m unittest discover -s tests -p "test_dialogue_gap_crosscheck.py" -v
```

Công cụ so hai báo cáo JSON, không cần truy cập file game gốc, không đọc/sửa `etc.bin_`, `etc.fht_`, save, font, catalog dịch hay `dialogue-probe.json`. Kết quả **chỉ chứng minh hai report nhất quán**, không chứng minh format đã giải mã.

## Ưu tiên nghiên cứu tiếp

1. Đặt giả thuyết record boundary / 4-byte alignment cho khoảng ≤8 byte; xác minh trên **nhiều CMC khác**, đặc biệt các ngoại lệ ≥9 byte.
2. Đối chiếu **control byte value + vị trí byte** trên bản game gốc **chỉ ở máy local**, sau đó xuất thống kê tối thiểu đã lọc, tránh văn bản/hex/copy game.
3. Dựng grammar có giới hạn và fail-closed; chứng minh **message parse → serialize khớp byte-for-byte** trên nhiều file thật, test lựa chọn và speaker. Chỉ khi đó mới thiết kế sửa độ dài/căn chỉnh/pointer và bản patch.
4. Dùng `python tools/catalog.py validate`, unit tests đầy đủ và UI QA trong RPCS3 với font Merienda V3 sau khi có thử nghiệm an toàn.

**Tình trạng:** Toàn repo có **11.886/11.886 câu nháp**; vẫn **không có parser message đã xác minh hoặc repacker**; không có thay đổi game binary.

## Điều tra V4 — thống kê giá trị control byte (không đọc lại game)

Mã nguồn: `tools/dialogue_control_stats.py`, unit tests: `tests/test_dialogue_control_stats.py` (**4/4 PASS fixture**; 8/8 PASS nếu tính cả kiểm tra chéo V3). Công cụ chỉ đọc tệp riêng tư `local-data/dialogue-probe.json` do V3 tạo trên máy người dùng. Chỉ thống kê những gap dài **1–8 byte** và toàn bộ byte trong gap thuộc `0x00..0x1f`: cho ra **tần suất code control dạng số thập phân**, quan hệ khoảng cách tới text tiếp theo, phân bố số lượng control/độ dài gap. Không xuất nguyên dãy byte, hex, lời thoại, offset game, hay file game.

Tệp xuất **đã lọc**: `local-data/dialogue-control-stats.json` hoặc bản sao `GUI_CHO_CHATGPT_dialogue-control-stats.json`. Công cụ này **chưa được chạy trên dữ liệu raw gốc của người dùng**; hiện chỉ có kết quả V3 đã lọc ở cloud, không thể dựng lại giá trị byte control bằng cách đoán.

Gói V4 1-click đã chuẩn bị để tự tìm raw V3 còn trên PC trong thư mục `Folklore-Source-v3\PS3-folklore-main\local-data`; **không đọc lại game**, không Internet, không thay đổi file game. Launcher PowerShell cần được thử trên Windows thực tế và có thể phải chọn đúng báo cáo raw nếu vị trí đã đổi.

Chỉ từ tần suất mã điều khiển vẫn **chưa** thể xác nhận speaker/record grammar: cần soi tương quan các khoảng ngắn và kiểm thử parser byte-for-byte trước khi repack.

