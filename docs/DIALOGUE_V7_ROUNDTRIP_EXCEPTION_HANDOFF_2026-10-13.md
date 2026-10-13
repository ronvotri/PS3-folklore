# Folklore — V7: kiểm chứng bảo toàn byte và định vị 51 ngoại lệ CMC (13/10/2026)

## Tình trạng thực tế

Báo cáo V6 người dùng cung cấp đã xác nhận trên `BCUS98147`:

- **134** file CMC với **1.795** ứng viên nguồn, xác thực được từ archive gốc;
- **1.744/1.795** ứng viên khớp khung khả dĩ `00 04 00 XX` (**97,16%**);
- **51** ứng viên chưa khớp: 24 thiếu khung, 12 lệch mod1, 12 lệch mod2, 3 mod3 bắt đầu bằng ký tự không in được;
- Phần lớn (107/134 file) không có ứng viên ngoại lệ trong phạm vi catalog.
- `CMC800` và `CMC801` chiếm 16/51 ngoại lệ và có câu trích xuất cắt mảnh.

Chú ý: khớp khung **không** chứng minh đó là một message, speaker, opcode, branch, pointer hay chuỗi hiển thị. `source` và `vi` trong catalog vẫn là bản nháp, không được xóa ký tự đầu vì có thể thuộc phần hiển thị.

## Công cụ mới

`tools/cmc_exception_ids.py` mở rộng tokenizer đã có ở `tools/cmc_readonly_tokens.py`:

1. Tìm **duy nhất** cặp `etc.bin_` / `etc.fht_` trong thư mục game, rồi chỉ đọc.
2. Đối chiếu SHA-256 nguyên bản từng CMC, ID/hash/câu ASCII/NUL tại offset, ranh giới section và độ dài tệp.
3. Chạy `tokenize(...)`: tách các **khung ứng viên** khớp mẫu, giữ toàn bộ phần còn lại như **opaque bytes**, tái ghép và so sánh byte-for-byte với original.
4. Một thuật toán thứ hai độc lập phân loại từng ứng viên chưa khớp, rồi bắt buộc các bộ đếm và loại lỗi khớp với V6. Phát hiện sai hoặc bị chồng lấn sẽ **dừng**, không ghi báo cáo một phần.
5. **Chỉ sau khi toàn bộ 134 tệp qua kiểm tra**, ghi `local-data/cmc-exception-ids.json`. Báo cáo này chỉ chứa tên file, ID dạng `file@offset`, offset dạng số, mã loại lỗi và thống kê; **không chứa văn bản game, byte, hex hoặc nhạc/ảnh**.

Giao diện lệnh:

```powershell
python tools/cmc_exception_ids.py --game-root "E:\Game\Folklore"
```

Bản Windows 1-click: `Folklore-V7-KiemChung-BaoToan-CMC.zip` (được bàn giao trực tiếp trong chat). Giải nén, nhấp đúp `CHAY_KIEM_CHUNG_CMC_V7.cmd`, gửi **duy nhất** `GUI_CHO_CHATGPT_cmc-exception-ids.json` nếu hoàn thành. Giữ `etc.bin_`, `etc.fht_` và báo cáo raw khác trên máy local.

### Mức độ đã kiểm thử

- **4/4 bài kiểm thử mô phỏng PASS tại môi trường xây dựng** cho bộ phân loại mới: khung mod0/mod3, sai căn chỉnh/newline, thiếu chữ ký/ngoài giới hạn, đối chiếu độc lập và từ chối reassembly khác byte.
- ZIP gồm launcher .cmd, .ps1 và README đã vượt kiểm tra ZIP CRC/cấu trúc. **Chưa chạy launcher hoặc bộ đọc mới trên PC người dùng**, nên không khẳng định 134 file đã roundtrip V7 thật.
- **Chưa chạy toàn bộ `python tools/catalog.py validate` và `python -m unittest discover -s tests -v` trên checkout repo mới.**

### Mục đích và giới hạn

Đây là công cụ **read-only**, không có entrypoint thay chữ, không xuất `etc.bin_`, không cài font và không sửa game/save. Kiểm tra byte-exact là phép ghép các **khung ứng viên + các vùng opaque nguyên trạng**, chưa hiểu các lệnh ẩn. Không thể suy từ đó rằng parser message đã được chứng minh.

Một trường hợp cần xét kỹ khi nghiên cứu byte thứ tư: `LCmc800` ở offset thập phân `12071`, nguồn bắt đầu `beautiful...` và nháp `đẹp...`. Không tự ép giữ chữ `b` trong tiếng Việt hay xóa nó khỏi nguồn.

## Ưu tiên sau V7

1. Dùng 51 ID ngoại lệ cụ thể để nghiên cứu các record cắt mảnh và loại định dạng phụ; không sửa offset ứng viên đoán mò.
2. Xác minh vai trò trường 4 byte trên các đoạn có tiếng Anh thật và người nói/nhánh lựa chọn.
3. Xây grammar message có trường nhận diện được và trường opaque; cần thêm chứng cứ độc lập cho pointer/length/section alignment.
4. Chỉ thiết kế repacker **sau** khi parse/serialize byte-perfect ở cấp command/message và có quy tắc relocation, bảng mã chữ, font Merienda V3 và rollback đã thử.

**Bản dịch:** 11.886/11.886 mục mới ở mức có bản nháp trong 158 catalog; chưa phải tỷ lệ chơi được.
