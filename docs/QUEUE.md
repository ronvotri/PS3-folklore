# Hàng đợi — 10/10/2026

## Bắt đầu ngay

1. translations/catalogs/menu/lang_en.bi5_.json: tiếp tục 40-80 mục `todo` theo thứ tự,
   bắt đầu từ `lang_en.bi5_@0000419f`. Các mục đã xử lý giữ `draft` cho đến khi được rà/test.
   118 cặp menu mẫu cũng ở menu_vi.json.
   Catalog là nơi ghi tiến độ từ đây. Khi xuất map source → vi để build,
   phát hiện bản dịch khác nhau cho cùng nguồn; không ghi đè âm thầm.
2. catalogs/cmc/LCmc000_en.bi5_.json rồi LCmc002_en.bi5_.json: cảnh có câu tìm
   mẹ. Rà candidate và tiền tố trước; chưa suy người nói.
3. catalogs/talk/tk100_en.bin_.json: câu tương tác/hội thoại, xem các mục lân cận.
4. Tiếp tục catalog còn lại theo index.json. Tên/số tệp chưa được xác minh là
   thứ tự chương truyện. Các đường dẫn catalog đều dưới translations/.

## Mốc bàn giao

Chưa bắt đầu dịch catalog hội thoại. Menu hiện có 184 mục `draft` (134 mẫu V3 + 50 mục mới), còn 832 mục `todo`.
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

## Lượt menu 001 — 10/10/2026

- Tệp: `translations/catalogs/menu/lang_en.bi5_.json`; đúng 50 mục `todo` đầu tiên → `draft`, từ `lang_en.bi5_@0000311b` đến `lang_en.bi5_@00004124` (không liên tục vì xen kẽ 134 bản nháp cũ).
- Chủ đề: cấu hình tay cầm, lưu/cài dữ liệu PS3, chọn ngôn ngữ, tóm tắt Ellen/Keats. Giữ nguyên ID/nguồn/hash/offset/order/source_review và số ngắt dòng mỗi mục; bản dịch NFC.
- Chú ý: thuật ngữ tạm `Transcension` → `Siêu hóa`, `Faery Realm` → `Cõi Faery`, `Hellrealm` → `Cõi Địa Ngục`; cần rà nhất quán trong các catalog tiếp theo.
- Đối chiếu chuỗi trùng trước khi build map nguồn → dịch; không âm thầm lấy bản sau đè bản trước. Trong game chưa được người dùng xác nhận lượt này.
- Kiểm tra trước commit: đối chiếu 50 ID, nguồn/metadata bất biến, NFC, số dòng và placeholder; GitHub Actions sẽ chạy validator/unittest Windows+Linux sau commit.
- **Tiếp theo:** xử lý `lang_en.bi5_@0000419f` (`Ellen traveled into the Faery Realm to discover the secret of her past.  The family bond that she discovers  brings Suzette to tears...`), rồi các mục `todo` phía sau; sau đó chuyển sang nhóm CMC theo thứ tự của hàng đợi.
