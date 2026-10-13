# Folklore — CMC Fixed Batch 0.2 (14/10/2026)

## Mục đích

Chuyển từ kiểm tra metadata sang **bộ vá nhiều câu CMC có phục hồi**. Công cụ `tools/cmc_batch_fixed.py` xử lý 134 catalog CMC đã có dịch, chỉ dùng **thay thế cùng độ dài byte** sau mã hóa bằng Merienda V3 hiện tại. Nó không giải mã script talk hoặc tạo bản Việt hóa full.

## Những điều được bảo toàn

- Đọc cặp `etc.bin_` / `etc.fht_`, kiểm tra archive size của BCUS98147 và SHA-256 file CMC gốc / vị trí source ASCII+NUL / ranh giới section trước khi tạo bất kỳ byte vá nào.
- Chỉ cho phép ứng viên CMC có tiền tố khung `00 04 00 XX` xác nhận ở `mod0` hoặc `mod3`. Với `mod3`, ký tự đầu candidate được **giữ nguyên** vì ý nghĩa byte cuối khung chưa xác minh; không tự gọi đó là speaker.
- Dịch đích phải ở NFC, không NUL, giữ thẻ đặc biệt, số dấu xuống dòng và số byte bằng source khi qua `text_codec.encode_text` / 25 alias Merienda V3. Nếu thiếu glyph/alias, độ dài khác hoặc khung bất thường → **skip**, không ép bỏ dấu/rút gọn/chèn padding.
- Không viết khi lập kế hoạch; chỉ `apply --confirm-test-copy` mới ghi. Sau preflight toàn bộ các file CMC, sao lưu **đủ từng CMC sẽ thay** bên cạnh archive, gồm manifest SHA và các vùng thay thế. Kiểm tra lại file ngay trước và ngay sau khi ghi; rollback khi có exception ghi bình thường.
- Lệnh `restore` chỉ chạy trên đúng patched bytes khớp manifest và backup SHA; từ chối sửa trạng thái lạ; backup giữ nguyên.
- Không đụng `lang_en`, `lang_uk`, font texture, `talk/en`, `rtd`, phụ đề phim, hoặc FHT; không đánh dấu draft là tested.

## CLI

```powershell
python tools/cmc_batch_fixed.py --game-root "E:\Game\Folklore-TEST-COPY" --action plan
python tools/cmc_batch_fixed.py --game-root "E:\Game\Folklore-TEST-COPY" --action apply --confirm-test-copy
python tools/cmc_batch_fixed.py --game-root "E:\Game\Folklore-TEST-COPY" --action restore --confirm-test-copy
```

Báo cáo read-only `dist/cmc-fixed-batch-plan.json` ghi số câu *eligible*, số file vá và thống kê lý do bỏ qua; đó **không phải số câu game đã hiển thị đúng**. Gói Windows giao diện menu `Folklore-CMC-Batch-0.2-TEST.zip` chỉ dành cho **bản sao game**, không phải patch cài đại trà.

## Kiểm thử

- `tests/test_cmc_batch_fixed.py`: **5/5 bài thử mô phỏng đạt** tại container (có dependency stub để chạy khi không có file game). Đã kiểm: 2 câu/1 CMC, mod0/mod3, giữ header/NUL, từ chối độ dài khác, kiểm tra SHA, bản kế hoạch không ghi, quy trình backup→apply→restore, từ chối backup sai checksum.
- Chưa chạy toàn bộ test repo hoặc chạy bản vá này trên game PS3 thật tại local. Chưa xác nhận tương thích RPCS3, encoding của đường render CMC hay mọi glyph cần thiết.
- Các nguồn `talk/en` gồm hơn 9.000 bản dịch nháp vẫn **chưa có trình đóng gói**. Đây là trở ngại lớn nhất để đạt FULL, cùng với câu CMC cần relocation và các nguồn chữ khác.

## Bước tiếp theo để đạt full

1. Đưa cơ chế kiểm tra/backup/khôi phục này trở thành lớp nền của bộ đóng gói về sau.
2. Ưu tiên giải mã khuôn record CMC (length/alignment/offset/nhánh) để chấp nhận **câu thay đổi độ dài byte**, không viết thẳng theo offset.
3. Tách luồng nghiên cứu riêng cho 23 file talk/en, rồi RTD/movie. Kiểm soát glyph có dấu theo tập bản dịch thực tế chứ không thử lại font V3 từ đầu.
4. Chỉ gọi “bản full” sau khi người dùng kiểm thử game trên RPCS3 và rà thiếu chữ thực tế.
