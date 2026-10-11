# Folklore — khảo sát định dạng hội thoại (11/10/2026)

## Mục tiêu và mức độ đã chứng minh

11.886 mục catalog là nguồn trích, KHÔNG đồng nghĩa game có thể chạy tiếng Việt.
Phần lớn hội thoại là các ứng viên ASCII-NUL bị cắt mảnh; chưa biết opcode, speaker,
pointer, thứ tự phát thoại, giới hạn vùng và cách thay chữ có dấu.
Không chỉnh file_offset, source_review, game binary, Merienda V3 hay chuyển trạng
thái sang reviewed/tested nếu chưa có bằng chứng.

## Đã bổ sung vào repo

**tools/dialogue_probe.py** — công cụ khảo sát chỉ đọc, Python >=3.10:

- Đọc chỉ mục etc.fht_ và các vùng tương ứng trong etc.bin_ từ máy local.
- Kiểm tra SHA-256 của từng entry talk/CMC so với catalog gốc; đối chiếu toàn bộ
  nguồn ASCII + NUL tại đúng offset và ranh giới section. Sai thì dừng.
- Lập danh sách section CMC có tên bắt đầu bằng talk (chưa parse command).
- Chọn mẫu có ký tự $, dấu sao lựa chọn, dấu ngoặc, newline, khoảng trắng
  đầu câu; ghi hex/ASCII trước và sau nguồn để điều tra prefix/opcode.
- Thống kê mẫu 4 byte big-endian/little-endian trùng offset tính theo đầu file
  hoặc đầu section. Cảnh báo: đây chỉ là những VỊ TRÍ BYTE GIỐNG NHAU,
  hoàn toàn chưa chứng minh có pointer thật.
- Báo cáo dưới local-data/dialogue-probe.json (đã gitignore); từ chối ghi
  đường dẫn báo cáo ra ngoài local-data/ hoặc dist/. Không hề ghi game.
- 6 unittest mô phỏng trong tests/test_dialogue_probe.py: test khớp SHA/source,
  ranh giới CMC, mẫu tham chiếu, không ghi binary và dừng khi nguồn sai.

## Chạy tại máy có bản game gốc

Chỉ dùng bản sao nguồn lưu tại máy; tìm THƯ MỤC CHỨA etc.bin_ và etc.fht_.
Chạy PowerShell từ thư mục gốc repo:

    python tools/dialogue_probe.py --bin-dir "D:\DUONG-DAN\DEN-THU-MUC-BIN"

Mặc định kiểm tra talk/en/tk100_en.bin_, talk/en/tk101_en.bin_,
cmc/en/LCmc000_en.bi5_, cmc/en/LCmc004_en.bi5_.

Tùy chọn kiểm tra nhanh ít file:

    python tools/dialogue_probe.py --bin-dir "D:\DUONG-DAN\DEN-THU-MUC-BIN" --files talk/en/tk100_en.bin_ cmc/en/LCmc000_en.bi5_ --max-samples 16 --radius 96

Chạy QA không cần game:

    python -m unittest discover -s tests -v
    python tools/catalog.py validate

Báo cáo mẫu chứa các byte xung quanh nguồn; GIỮ LOCAL, không push vào
GitHub, không gửi ROM/ISO, font, texture hay kho etc.

## Cổng bắt buộc trước khi đưa lời thoại vào game

1. SOURCE: file nguyên bản đúng SHA, mọi chuỗi được đối chiếu byte-for-byte
   tại offset với 2 file talk và ít nhất 1 CMC.
2. LAYOUT: giải mã header, vùng text/control, bảng pointer/offset và byte
   điều khiển trên nhiều file; không tin kết quả dò mẫu u32 đơn lẻ.
3. MESSAGE: dựng được câu tiếng Anh nguyên vẹn, nhánh thoại và người nói;
   so trực tiếp với cảnh do người dùng tự chơi RPCS3.
4. LOSSLESS: parse -> serialize không dịch phải giữ ĐÚNG TỪNG BYTE nguồn;
   unit tests cho file thật ở máy local và fixtures tổng hợp.
5. SAFE BUILD: xác minh encoding/alias/glyph, số byte, giới hạn, alignment,
   toàn bộ pointer fixup; preflight hash, dry-run, sao lưu và khôi phục.
6. RUNTIME: thử rất ít câu trong game, rà người nói, cắt dòng, font và
   lựa chọn trước khi mở rộng phạm vi.

## Vướng mắc và bước tiếp

Cloud hiện KHÔNG có các file nhị phân gốc. Công cụ khảo sát chỉ là bước chuẩn
bị và được thử với dữ liệu tổng hợp; chưa chạy trên file thật, chưa có
parser, serializer hay repacker hội thoại. Bước tiếp là chạy probe ở local,
xác minh một bảng pointer/opcode có cấu trúc, rồi tạo parser đọc không
mất byte. Nếu chưa đạt cổng LOSSLESS thì tuyệt đối không vá dịch vào offset
của ứng viên JSON.

Khi tiếp tục dịch các phần còn thiếu, giữ nguyên trạng thái draft;
không dùng phần trăm bản nháp để tuyên bố Việt hóa đã có thể chơi.

## Rà đủ nguồn hội thoại — CLI bổ sung 11/10/2026

Chế độ mới **chỉ đọc** kiểm tra theo thứ tự toàn bộ tệp `kind=dialogue`
trong `translations/index.json`, đối chiếu SHA file, ID, offset ASCII-NUL,
và section CMC được nhận diện là talk. **Không** phân tích người nói, không
thử bản dịch trong game, không xây dựng bộ đóng gói.

Chạy trên bản sao gốc khi có `etc.bin_` và `etc.fht_`:

    python tools/dialogue_probe.py --bin-dir "D:\\DUONG-DAN\\DEN-THU-MUC-BIN" --all-dialogue --verify-only

`--verify-only` bỏ qua dò byte-pattern u32 để rà toàn bộ dữ liệu hiệu quả hơn;
báo cáo ghi `scan_mode=SOURCE_ONLY`, tổng số candidate đã xác minh và
trạng thái từng tệp. Muốn điều tra xung quanh chuỗi/pattern nghi là pointer,
dùng `--files` với 2–4 tên nguồn và bỏ `--verify-only`.
Hai tùy chọn `--files` và `--all-dialogue` không được dùng cùng nhau.
Kết quả có giá trị **chỉ khi đã chạy trên bản game gốc tại máy local**;
unit test tổng hợp hay CI không thay thế bước này. Không đăng báo cáo hex
hoặc dữ liệu nhị phân lên GitHub.

## Lượt 034: chứng minh roundtrip *vỏ section* CMC (11/10/2026)

`tools/dialogue_probe.py` nay có `parse_opaque_cmc` và
`OpaqueCMCContainer.serialize()`: đọc header đã xác định, bảng ranh giới
section, các ô tên 24 byte, byte đệm, payload nguyên khối và byte đuôi.
Trước khi ghi báo cáo CMC, công cụ phải tự tái tạo **byte-for-byte** mọi phần
đó, không được thay kích thước/vị trí section. Trường báo cáo
`opaque_cmc_container_roundtrip=true` chỉ nói **vỏ CMC** tái tạo không mất byte;
**không nói rằng đã hiểu opcode/nhánh thoại/speaker, hoặc talk raw đã parse**.
Chế độ này chạy tự động cho các file CMC trong `--all-dialogue --verify-only`.
Tệp talk/en vẫn chỉ kiểm tra hash và chuỗi nguồn; report ghi `null` cho
trường roundtrip CMC.

Unit test dùng fixture mô phỏng cả dữ liệu chưa biết trong header, padding,
command, trailer; thử sửa độ dài section/padding và count thì phải từ chối.
Chưa có binary gốc trong cloud nên chưa chứng minh roundtrip với game thật;
không có tính năng lưu/bơm phần tiếng Việt vào CMC. Mốc LOSSLESS ở cấp
**message command stream** vẫn chưa đạt, chưa được phép viết repacker.
