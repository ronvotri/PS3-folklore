# Hàng đợi — 10/10/2026

## Bắt đầu ngay

1. translations/catalogs/menu/lang_en.bi5_.json: tiếp tục 40-80 mục `todo` theo thứ tự,
   bắt đầu từ `lang_en.bi5_@00005982`. Các mục đã xử lý giữ `draft` cho đến khi được rà/test.
   118 cặp menu mẫu cũng ở menu_vi.json.
   Catalog là nơi ghi tiến độ từ đây. Khi xuất map source → vi để build,
   phát hiện bản dịch khác nhau cho cùng nguồn; không ghi đè âm thầm.
2. catalogs/cmc/LCmc000_en.bi5_.json rồi LCmc002_en.bi5_.json: cảnh có câu tìm
   mẹ. Rà candidate và tiền tố trước; chưa suy người nói.
3. catalogs/talk/tk100_en.bin_.json: câu tương tác/hội thoại, xem các mục lân cận.
4. Tiếp tục catalog còn lại theo index.json. Tên/số tệp chưa được xác minh là
   thứ tự chương truyện. Các đường dẫn catalog đều dưới translations/.

## Mốc bàn giao

Chưa bắt đầu dịch catalog hội thoại. Menu hiện có 384 mục `draft` (134 mẫu V3 + 250 mục qua 5 lượt), còn 632 mục `todo`.
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

## Lượt menu 002 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: dịch đúng 50 mục `todo` kế tiếp → `draft`, từ `lang_en.bi5_@0000419f` đến `lang_en.bi5_@00004bb3` (IDs không liên tục do xen kẽ mục đã có bản dịch).
- Nội dung: 7 tóm tắt/câu chọn truyện Ellen–Keats; đi lại, áo choàng, hiệu ứng; các cõi và tên vùng trên bản đồ.
- Giữ nguyên nguồn, thứ tự, hash, offset, ID và `source_review`; giữ số ngắt dòng và ký hiệu ○○○○○○○○○. Bản dịch NFC, chưa kiểm thử RPCS3.
- Tham chiếu tên: `Faery Realm` → `Cõi Faery`; `Hellrealm` → `Cõi Địa Ngục`; `Netherworld` → `Cõi âm`; `Undersea City` → `Thành phố đáy biển`; `Endless Corridor` → `Hành lang Vô tận`. Giữ nguyên các tên riêng Daru/Gesh/Avalon/Brahma/Warcadia/Fleshrum. Thuật ngữ hiệu ứng Bond/Destroy, MC, KB, Eternal Regress và Cromlech còn cần rà; xem notes từng mục.
- QA: kiểm soát 50 ID kế tiếp, chỉ đổi vi/status/notes, giữ newline/control tokens, kiểm tra bản dịch trùng không có xung đột. Sau commit, đối chiếu GitHub Actions (validator + unittest trên Windows/Linux).
- **Tiếp theo:** `lang_en.bi5_@00004bc6` — `Inquisition Bridge`. Tiếp tục 50 mục `todo` theo thứ tự, chưa đánh dấu mục nào `reviewed`/`tested` nếu chưa kiểm thử.

## Lượt menu 003 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: xử lý 50 mục `todo` kế tiếp → `draft`, từ `lang_en.bi5_@00004bc6` đến `lang_en.bi5_@00004e95`, một số mục xen kẽ đã có bản nháp từ V3.
- Chủ đề: 19 địa danh bản đồ (gồm 7 tên Doolin lặp hai lần), HP/EXP, 12 loại hệ/hiệu ứng, 17 tên vật phẩm. Giữ HP/EXP nguyên viết tắt; đồng bộ Doolin/Sidhe với lượt trước.
- Các tên cần kiểm chứng: Inquisition Bridge → Cầu Thẩm vấn, Murk → Vùng Mù mịt, Henge → Vòng đá cổ; Guard/Barrier → Đỡ đòn/Kết giới; Memento Key → Chìa khóa Kỷ vật, Epigraph fragment → Mảnh văn khắc. Ghi chú cụ thể từng ID trong catalog.
- QA trước commit: 50 ID liên tiếp trong dãy `todo`, 50 mục đổi đúng `vi/status/notes`; tất cả nguồn/hash/offset/`source_review` giữ nguyên; NFC, số dòng, placeholder/token; không có xung đột khi hai mục trùng nguồn; không sửa font hay binary.
- Chưa có kiểm thử hiển thị RPCS3; chỉ `draft`, chưa `reviewed/tested`. GitHub Actions chạy validator + unittest trên Windows/Linux sau commit.
- **Tiếp theo:** bắt đầu `lang_en.bi5_@00004ea3` (`Yellow liquid`), dịch 50 mục `todo` tiếp theo; sau menu tiếp tục CMC/talk theo hàng đợi.

## Lượt menu 004 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: dịch đúng 50 mục `todo` kế tiếp → `draft`, từ `lang_en.bi5_@00004ea3` đến `lang_en.bi5_@00005386`.
- Nhóm: 16 tên vật phẩm/nguyên liệu (chất lỏng, đá/quặng, bụi, hạt cây); 34 nhãn trang sách tranh thuộc 4 cõi, có các chuỗi lặp tại nhiều vị trí.
- Bản dịch trang sách thống nhất `Sách tranh <tên cõi>, tr. N`; giữ các tên cõi đã chốt từ lượt 002. Nhãn lặp dùng cùng bản dịch, không tự ghi đè nguồn.
- Chưa xác minh hình ảnh: `Pulse Tree Nut` → `Hạt cây Mạch đập` (tạm), `Aqua liquid` → `Chất lỏng màu xanh ngọc` (tạm), `Golden Ore` → `Quặng ánh vàng` (tạm). Có notes tại ID tương ứng.
- QA trên dữ liệu: 50 ID đúng checkpoint; chỉ chỉnh `vi/status/notes`, giữ nguyên thứ tự/source/hash/offset/`source_review`; NFC, số ngắt dòng và control token; không có xung đột bản dịch cho cùng source. GitHub Actions chạy `python tools/catalog.py validate` và `python -m unittest discover -s tests -v` trên Windows/Linux sau khi push.
- Không đụng font Merienda V3, ROM/ISO hay payload; 50 mục mới là `draft`, chưa được thử trực tiếp trong RPCS3.
- **Tiếp theo:** `lang_en.bi5_@000053ab` — `Endless Corridor picture book, pg. 5`, dịch 50 mục `todo` kế tiếp.

## Lượt menu 005 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: dịch đúng 50 mục `todo` kế tiếp → `draft`, từ `lang_en.bi5_@000053ab` đến `lang_en.bi5_@00005956`.
- Gồm 26 nhãn trang sách tranh (Endless Corridor, Hellrealm, Corrupt Village, Netherworld Core), 13 tên sách, 7 áo choàng và 4 vật phẩm cốt truyện liên quan Ellen/Suzette/Renaldo/Regine/Herve.
- Thuật ngữ nhất quán với lượt trước: Endless Corridor → Hành lang Vô tận; Hellrealm → Cõi Địa Ngục; Netherworld Core → Lõi Cõi âm; các sách cùng nguồn dùng bản dịch trùng khớp. Corrupt Village → Làng Tha hóa là tên **tạm** cần xác minh trong game.
- `Endless Corridor picture book ` có khoảng trắng cuối bất thường trong nguồn: không sửa nguồn; lược trong bản dịch, ghi chú tại entry. Không được tự gộp/ghi đè các nguồn khi build.
- QA cấu trúc trước commit: 50 ID và thứ tự `todo` đúng checkpoint, chỉ thay `vi/status/notes`, giữ source/hash/offset/source_review; NFC, số ngắt dòng, placeholder/control token; 0 source trùng có bản dịch xung đột.
- Không can thiệp font Merienda V3, ROM/ISO, payload; các mục mới vẫn `draft`, chưa test trong RPCS3. CI GitHub Actions chạy validator + unittest cho Windows/Ubuntu sau khi push.
- **Tiếp theo:** `lang_en.bi5_@00005982` — `Left side of a photo / that was torn in half`, rồi 49 mục `todo` kế tiếp.
