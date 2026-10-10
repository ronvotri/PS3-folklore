# Hàng đợi — 10/10/2026

## Bắt đầu ngay

1. translations/catalogs/menu/lang_en.bi5_.json: rà các mục draft, dịch todo
   theo thứ tự, 40-80 mục/lượt. 118 cặp menu mẫu cũng ở menu_vi.json.
   Catalog là nơi ghi tiến độ từ đây. Khi xuất map source → vi để build,
   phát hiện bản dịch khác nhau cho cùng nguồn; không ghi đè âm thầm.
2. catalogs/cmc/LCmc000_en.bi5_.json rồi LCmc002_en.bi5_.json: cảnh có câu tìm
   mẹ. Rà candidate và tiền tố trước; chưa suy người nói.
3. catalogs/talk/tk100_en.bin_.json: câu tương tác/hội thoại, xem các mục lân cận.
4. Tiếp tục catalog còn lại theo index.json. Tên/số tệp chưa được xác minh là
   thứ tự chương truyện. Các đường dẫn catalog đều dưới translations/.

## Mốc bàn giao

Chưa bắt đầu dịch catalog hội thoại. Đã nạp 134 mục menu mẫu ở trạng thái draft.
Người dùng xác nhận V3 “ok rồi” sau thử sửa khoảng hở sau ấ/ớ.
Người dùng tự mở game/test/gửi ảnh; không tự điều khiển giả lập.

## Chưa giải quyết

- Parser hội thoại, metadata/prefix, repacker talk/cmc.
- Mở rộng vùng menu khi câu dịch dài vượt chỗ trống.
- Mở rộng 251 glyph/25 alias cho đủ chữ Việt và dấu câu.
- Phụ đề phim, chữ trong ảnh, PS3 thật và Steam Deck.

## Ghi sau mỗi lượt

Ghi tệp, ID đầu/cuối hoặc danh sách ID, số mục đổi trạng thái, ngữ cảnh còn
thiếu, kết quả kiểm tra, việc kế tiếp. Giữ lại mốc font V3 khi thêm lịch sử.
