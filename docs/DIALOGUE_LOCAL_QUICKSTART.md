# Folklore — chạy chẩn đoán hội thoại trên Windows (không vá game)

## Tình trạng

Công cụ `tools/dialogue_diagnose.py` là **lối vào một lệnh** cho hai
công cụ hiện có:

1. `dialogue_probe.py`: đọc nguyên bản `etc.bin_`/`etc.fht_`,
   xác minh SHA/offset/NUL của các candidate và, khi chọn mẫu,
   ghi byte lân cận + các *mẫu trùng u32* chưa được chứng minh là pointer.
2. `dialogue_summary.py`: lọc bỏ các đoạn văn bản/hex và tạo bản tổng kết
   cấu trúc nhỏ để người dùng có thể kiểm tra rồi chia sẻ nếu muốn.

**Không có game binary hoặc ROM nào được chỉnh sửa; không có bước upload tự động.**
Không dùng các report này làm bằng chứng rằng parser/repacker đã hoàn thiện.

## Sửa lỗi chẩn đoán CMC — 12/10/2026

Khi chạy launcher trước đây, một bản game gốc đã báo `Diagnosis refused: Invalid CMC section bounds`. Đây là **lỗi từ logic khảo sát, không có bằng chứng rằng game/ISO hỏng**. Công cụ `tools/dialogue_probe.py` trước đó yêu cầu các offset section tăng *nghiêm ngặt*; trong khi bộ trích xuất catalog `tools/catalog.py` vốn chấp nhận hai offset bằng nhau (section rỗng). Bản sửa:

- Cho phép section có `start == end` nhưng tiếp tục **từ chối** offset giảm ngược, chồng bảng tên hoặc vượt kích thước file.
- Cho phép tái tạo lossless section rỗng và xuất metadata tương ứng trong báo cáo lọc.
- Khi còn lỗi CMC khác, báo `cmc/en/LCmc...: Invalid CMC section bounds: ...` với vị trí và độ dài cụ thể; **không bỏ qua file lỗi, không ghi patch**.
- Thêm bài test section rỗng, negative test vượt/đảo offset, và kiểm tra báo cáo chỉ chứa cấu trúc.
- Đã chạy 4 trường hợp thử ranh giới trên dữ liệu tổng hợp; **chưa kiểm thử lại trên bản game thật**.

Bản launcher 1-click tải `main.zip` mỗi lần nên tự nhận mã mới. Nếu vẫn lỗi, gửi nguyên dòng có `LCmc...` và chi tiết offset; không cần gửi file game `etc.bin_` hoặc `etc.fht_`.

## Chẩn đoán thực tế thành công & khảo sát bổ sung (12/10/2026)

Người dùng đã chạy bản V2 trên `BCUS98147` và gửi `GUI_CHO_CHATGPT_dialogue-structure-summary.json`. Kết quả xác minh **796 chuỗi nguồn tại 4 file** (`tk100` 314; `tk101` 447; `LCmc000` 11; `LCmc004` 24). Hai CMC chứa 6 section rỗng cuối mỗi tệp. Nội dung chi tiết: `docs/DIALOGUE_REAL_PROBE_FINDINGS_2026-10-12.md`.

Bản **V3** bổ sung `tools/dialogue_gap_fingerprint.py` (4 unit test tổng hợp đạt) để tạo thêm `local-data/dialogue-gap-fingerprint.json`. Công cụ chỉ đọc **báo cáo probe đã ở máy local**, xuất độ dài khoảng trống giữa hai mẫu và phân loại byte thô thành nhóm `zero/control/space/printable/high`, **không xuất text/hex/byte values**. Khoảng cách dài hơn 32 byte không phân loại để tránh suy diễn phần chứa văn bản. Các khoảng ngắn này **chưa phải opcode đã chứng minh**.

Sau khi chạy launcher mới, chỉ chia sẻ hai tệp đã lọc:
- `dialogue-structure-summary.json`
- `dialogue-gap-fingerprint.json`

Bộ ZIP V3 tạo hai bản sao tiền tố `GUI_CHO_CHATGPT_` ngay trong thư mục giải nén. Tuyệt đối không gửi `dialogue-probe.json`, `etc.bin_`, `etc.fht_`. Cả hai cách chạy đều không sửa dữ liệu game.

## Cách dễ nhất (Windows, không cần gõ lệnh)

Trong bản repo mới nhất, nhấp đúp `RUN_DIALOGUE_DIAGNOSE.cmd` ở thư mục gốc. Launcher mặc định tìm game tại `E:\Game\Folklore`, rồi chạy công cụ đọc-only với tối đa 48 mẫu mỗi tệp. Nếu game đặt ở nơi khác, có thể kéo-thả **thư mục game** lên tệp `.cmd`. Không chạy khi đang ghi/sửa bản game; giữ backup nguyên gốc.

Launcher chỉ đọc `etc.bin_` và `etc.fht_`, tạo hai file trong `local-data/`:
- `dialogue-structure-summary.json`: bản cấu trúc đã lọc để xem trước khi chia sẻ.
- `dialogue-probe.json`: dữ liệu/hex thô **chỉ giữ riêng trên máy**; không đăng công khai.

Nếu PowerShell/Windows hiện lỗi thiếu Python, cài Python 3.10+ rồi chạy lại. Đây chỉ là **chẩn đoán**, không cài tiếng Việt hay thay đổi tệp game.

## Cách chạy nhanh

Cần Python 3.10+, mã nguồn repo mới nhất và thư mục game đã giải nén với
`etc.bin_` và `etc.fht_`. Mở PowerShell tại thư mục repo, nhập:

~~~powershell
python tools/dialogue_diagnose.py --game-root "E:\Game\Folklore"
~~~

Lệnh tự tìm cặp file trong các thư mục con (tối đa 8 cấp), không cần mò
`PS3_GAME`/`USRDIR` thủ công. Nếu có nhiều bản copy, chương trình **từ chối
đoán**. Khi đó chỉ rõ thư mục thực sự chứa cặp file:

~~~powershell
python tools/dialogue_diagnose.py --bin-dir "E:\Game\Folklore\PS3_GAME\USRDIR"
~~~

Đường dẫn thứ hai chỉ là ví dụ: phải trỏ đúng thư mục chứa cả hai file.
Công cụ kiểm tra SHA-256 gốc của các tệp trong catalog; nếu đang dùng bản
đã chỉnh sửa và không khớp, nó dừng, không thay thế file.

Có thể yêu cầu kiểm chứng **toàn bộ** catalog thoại/CMC trước, không dò
mẫu con trỏ (thường nhanh và dùng ít tài nguyên hơn):

~~~powershell
python tools/dialogue_diagnose.py --game-root "E:\Game\Folklore" --verify-all
~~~

## Kết quả trong thư mục `local-data/`

- `dialogue-probe.json`: **riêng tư**, chứa đoạn hex, văn bản nguồn
  và bằng chứng thô; không đăng lên GitHub hay đính kèm công khai.
- `dialogue-structure-summary.json`: bản **lọc cấu trúc**, không mang
  văn bản gốc hoặc byte-window. Có thể kiểm tra rồi gửi để phân tích
  giả thuyết về pointer và định dạng.

Cả hai đường dẫn đều được `.gitignore` loại khỏi Git. Lệnh chỉ đọc binary,
tạo hai JSON trong `local-data/`; không thử chạy RPCS3 hay vá lời thoại.

## Tiêu chuẩn để làm bước kế tiếp

Từ kết quả trên **ít nhất hai file talk và một CMC**, cần xác định được
đâu là metadata/đâu là chuỗi, cách lấy message, speaker/opcode và chỗ
tham chiếu thực sự. Mẫu u32 đơn thuần KHÔNG đủ. Sau đó mới có thể viết
parser/serializer message và chứng minh parse → serialize ra **đúng từng
byte gốc**. Repacker thay đổi text chỉ được xây tiếp khi đã xác minh pointer,
alignment, dung lượng, bảng font alias, khôi phục an toàn và chạy thử RPCS3.

Kiểm tra công cụ trên nguồn mã (không cần game):

~~~powershell
python -m unittest discover -s tests -v
python tools/catalog.py validate
~~~

Chưa có dữ liệu gốc trong môi trường cloud. Những unit test bằng fixture
tổng hợp không thay thế được lần chạy thật trên máy có game.
