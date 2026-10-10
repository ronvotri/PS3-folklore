# Hàng đợi — cập nhật 11/10/2026

## Bắt đầu ngay

1. `translations/catalogs/talk/tk104_en.bin_.json`: tiếp tục từ `talk/en/tk104_en.bin_@00004f2e` (` / world, at least.`), còn 642 `todo`. Ưu tiên câu về Harriet, kỷ vật, bức ảnh và linh hồn; giữ speaker/cách xưng hô ở mức nháp khi thiếu ngữ cảnh.
2. Các tệp `tk100`, `tk101`, `tk102`, `tk103` đã lần lượt đạt 314/314, 447/447, 494/494, 578/578 `draft`. Ba CMC `LCmc000`, `LCmc002`, `LCmc004` có tổng 46/46 `draft`. Chưa có repacker hội thoại hoặc kiểm thử runtime.
3. Trước khi build talk/cmc: đọc `docs/DIALOGUE_CANDIDATE_AUDIT.md`; khảo sát vùng byte trước/sau string và bảng con trỏ ở local (nguyên bản), phân định prefix text/control/metadata; chưa có repacker an toàn.
4. Menu `lang_en.bi5_`: 1.016/1.016 `draft`; cần QA độ dài/glyph/alias và hiển thị RPCS3. Tiếp tục các catalog theo `translations/index.json`; ID tệp không nhất thiết là thứ tự truyện.

## Mốc bàn giao

Menu 1.016/1.016 `draft`; CMC 46 `draft`; tk100 314/314, tk101 447/447, tk102 494/494, tk103 578/578, tk104 89/731 `draft`. Còn 8.902 mục `todo` trên 158 catalog. Hội thoại vẫn `candidate`/`draft`, chưa parser/repacker/test.
Người dùng xác nhận V3 “ok rồi” sau thử sửa khoảng hở sau ấ/ớ.
Người dùng tự mở game/test/gửi ảnh; không tự điều khiển giả lập.

## Chưa giải quyết

- Parser hội thoại, metadata/prefix, repacker talk/cmc.
- Mở rộng vùng menu khi câu dịch dài vượt chỗ trống.
- Mở rộng 251 glyph/25 alias cho đủ chữ Việt và dấu câu.
- Phụ đề phim, chữ trong ảnh, PS3 thật và Steam Deck.

## Ghi sau mỗi lượt

Theo yêu cầu người dùng ngày 10/10/2026: menu dịch khoảng **200 mục/lượt**,
chia kiểm tra nội bộ mỗi ~50 mục nhưng chỉ bàn giao/commit sau khi hoàn tất cả
lượt. Không tự dừng ở 50 nếu không có lỗi thật. Nếu hội thoại dài hoặc cần rà
ngữ cảnh, giảm kích cỡ hợp lý nhưng giải thích trong checkpoint.
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

## Lượt menu 006 — 10/10/2026

- `translations/catalogs/menu/lang_en.bi5_.json`: dịch đúng 50 mục `todo` kế tiếp thành `draft`, từ `lang_en.bi5_@00005982` đến `lang_en.bi5_@00006235`.
- Nội dung: 28 mô tả vật phẩm, tranh/đồ liên kết; 6 áo choàng Sidhe; 13 sách tranh Folk; 3 nhãn Game Over/Continue/Save and exit.
- Giữ nguyên các tên Herve, Cecilia, Lester, Sidhe, Faery, Folk; các cõi Cõi Faery, Cõi Địa Ngục, Lõi Cõi âm, Hành lang Vô tận và Làng Tha hóa (tạm) đã dùng. Giữ nguyên chỉ dấu `[Link item]` và MC. Có ghi chú trong các mục chưa rõ.
- QA: kiểm soát đúng 50 ID, chỉ đổi vi/status/notes, không đụng source/hash/offset/order/source_review; NFC, newline, tokens, bản dịch nguồn trùng: 0 xung đột.
- Không đụng font V3, payload, ROM/ISO; chưa thử hiển thị trong RPCS3, không đánh dấu tested. GitHub Actions chạy validator/unittest trên Windows/Linux khi push.
- **Tiếp theo:** `lang_en.bi5_@00006243` — `Exit`, dịch tiếp 50 mục menu.

## Lượt menu 007 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: dịch đúng 50 mục `todo` kế tiếp → `draft` từ `lang_en.bi5_@00006243` đến `lang_en.bi5_@0000657d`, không liên tục do các bản mẫu V3 xen giữa.
- Chủ đề: giao diện thoát/lưu/tiếp tục; 12 tiêu đề chương/chủ đề (Mirage, Familial Warmth, Lamplight, Only one Wish, Oblivion, Youth, Labyrinth, Darkness, Judgment, Guilt, Memory, Fear); Ellen/Keats, 9 nhãn thế giới/địa danh và nhãn trạng thái/dữ liệu hệ thống.
- Thuật ngữ giữ nhất quán: Làng Doolin, Cõi Faery, Warcadia, Thành phố đáy biển, Hành lang Vô tận, Cõi Địa Ngục, Làng Tha hóa (tạm), Lõi Cõi âm; Destroy → Hủy diệt, Slash → Chém, Guard → Đỡ đòn. Giữ Ellen/Keats nguyên tên. Tiêu đề chưa có ngữ cảnh chương đầy đủ nên đánh dấu `draft`.
- QA cấu trúc trước commit: đúng 50 ID từ todo; chỉ chỉnh vi/status/notes, nguồn/ID/hash/offset/order/source_review bất biến; kiểm tra NFC, newline, mã đặc biệt, 0 source trùng có bản dịch xung đột.
- Không thay đổi Merienda V3, ROM, ISO, alias/font payload; chưa thử runtime RPCS3, giữ `draft`. CI Windows/Linux chạy `python tools/catalog.py validate` và `python -m unittest discover -s tests -v` sau commit.
- **Tiếp theo:** `lang_en.bi5_@00006583` (`Barrier`), thêm 50 mục menu kế tiếp.

## Lượt menu 008 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: xử lý đúng 50 mục `todo` thành `draft`, từ `lang_en.bi5_@00006583` đến `lang_en.bi5_@00006821`.
- Nội dung: 9 chỉ số/hệ/hiệu ứng (Barrier, Earth, Ice, Fire, Thunder, Wind, Bond, Charm, Sleep); 12 thông báo nâng cấp Folk/Karma; 4 mục nhiệm vụ; 20 nhãn bộ đếm còn lại từ 20 đến 1; 5 thông báo phát hiện Folk/lối ra/liên kết vật phẩm/Karma.
- Giữ nguyên thuật ngữ chuẩn Folk, Karma, MC, Malabaricus và placeholder `%s`; khớp Barrier → Kết giới, Bond → Trói buộc, Charm → Mê hoặc, Thunder → Sét với các lượt cũ. Thuật ngữ Charge Level, Element Ability, Ammo count và Link item còn cần xác minh hiển thị/cơ chế: có notes.
- QA: đối chiếu 50 ID theo `todo`, chỉ thay vi/status/notes; bất biến source/hash/offset/order/source_review, bảo toàn NFC/newline/token; 0 xung đột giữa bản dịch cùng nguồn. Không can thiệp font V3, ROM, ISO hoặc payload.
- Chưa thử runtime RPCS3, mọi mục vẫn `draft`. GitHub Actions chạy `python tools/catalog.py validate` và `python -m unittest discover -s tests -v` trên Windows/Linux sau commit.
- **Tiếp theo:** `lang_en.bi5_@00006833` — `Receive Folk` và 49 mục `todo` kế tiếp.

## Lượt menu 009 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: dịch đúng 50 mục menu `todo` kế tiếp thành `draft`, từ `lang_en.bi5_@00006833` đến `lang_en.bi5_@00007030`.
- Chủ đề: nhận/gửi Folk và vật phẩm liên kết, 4 nhiệm vụ Herve có điều kiện mở theo Keats/Ellen, trao đổi Id/dữ liệu quái vật, Karma, trình tự PSP™ Link/Memory Stick™, lỗi giao tiếp và tăng hạng Keats/Ellen.
- Giữ các mã `%s`, `%d`, ký hiệu `™`/`®` và tên `PSP™`, `PlayStation®Portable`, `Memory Stick™`, `Pied Piper`, `Folk`, `Id`, `Karma`, `Keats`, `Ellen`, `Herve`. Ghi notes cho các chỗ nghĩa UI chưa chắc (Linked item/Give Id/Increased Id), nguồn có typo `has bee` và khoảng trắng thừa: không sửa source.
- QA cấu trúc trước commit: đúng 50 ID tiếp theo, chỉ vi/status/notes thay đổi; source/hash/offset/order/source_review giữ nguyên; NFC, số xuống dòng và protected tokens giữ nguyên; 0 xung đột chuỗi English trùng. Không can thiệp font Merienda V3, ROM/ISO/binary/payload.
- Vẫn ở mức `draft`, chưa hiển thị/test với RPCS3. GitHub Actions chạy `python tools/catalog.py validate` và `python -m unittest discover -s tests -v` (Windows/Ubuntu) sau commit.
- **Tiếp theo:** `lang_en.bi5_@00007059` — `Level up for Keats! / Maximum HP increased!`, tiếp 50 mục menu.

## Lượt menu 010 — 10/10/2026 (200 mục)

- Đã xử lý **200 mục** `todo` → `draft` trong `translations/catalogs/menu/lang_en.bi5_.json`, từ `lang_en.bi5_@00007059` đến `lang_en.bi5_@0000874e`. Chia bốn nhóm 50 để QA nhưng chỉ commit/bàn giao một lượt.
- Nội dung: lên cấp, sách tranh, đá ký ức/hệ chiến đấu, điều kiện mở đường, các địa điểm, UI tương tác, cảnh báo HDD, trang phục/chỉ số, tên nhân vật/Folk, đoạn thoại Ellen–Keats–Livane, menu phụ đề và chế độ hầm ngục.
- Đồng bộ các thuật ngữ Folk, Id, Karma, MC, HP, HDD, tên nhân vật/cõi; dấu cách thừa tại nguồn Gam, tên vai Scarecrow, Special 1, FF và diễn giải hệ hiệu ứng vẫn có notes cần xác minh. Giữ riêng quan hệ và lời thoại theo nội dung nguồn, không tự suy diễn.
- QA: đúng 200 ID `todo`, chỉ sửa vi/status/notes, nguồn/sha/offset/order/source_review bất biến; NFC, newline, placeholder/control token giữ nguyên; 0 xung đột ở các English source trùng. Không can thiệp font Merienda V3 hoặc binary/payload game.
- Chưa test trong RPCS3, vẫn `draft`. Chạy GitHub Actions validator + unittest Windows/Ubuntu sau commit.
- **Tiếp theo:** `lang_en.bi5_@00008757` — `  Creating Dungeons`; còn 232 mục menu, tiếp tục ~200 mục lượt 011.

## Lượt menu 011 — 10/10/2026 (200 mục)

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: hoàn tất 200 mục `todo` → `draft`, từ `lang_en.bi5_@00008757` đến `lang_en.bi5_@00009bbd`; QA bốn nhóm 50, commit một lượt.
- Nội dung: hướng dẫn tạo hầm ngục, Download Play, thưởng điểm, quy tắc hầm ngục/thử nghiệm, tải lên và xếp hạng, lỗi mạng, dữ liệu phòng/vật phẩm tăng cường, mã thưởng %s, cảnh báo PSN, giao diện chỉnh sửa, cấu hình phòng/điều kiện hoàn thành, thoát/bỏ cuộc.
- Các mảnh văn bản cùng thông báo được dịch để đọc liền mạch nhưng giữ từng ID và nguồn nguyên vẹn. Thống nhất Boost → Tăng cường, Quota → Chỉ tiêu (tạm), CampaignPt → Điểm chiến dịch (cần QA bố cục), Dungeon → hầm ngục, Test Play → Chơi thử, Folk nguyên danh xưng. Có ghi chú cho câu nguồn sai 'Dungeon Dungeon' và mảnh thông báo bị chia nhỏ.
- QA: chỉ đổi vi/status/notes của đúng 200 mục; bất biến id/source/sha256/offset/source_review/order; NFC, newline, mã đặc biệt %s, △○×□, ™/® và khoảng trắng đầu/fullwidth; không có source trùng dịch xung đột. Không thay font V3 hoặc ROM/binary/payload.
- Chưa test trong RPCS3; các mục vẫn draft. Chạy validator/unittest Windows và Ubuntu qua GitHub Actions sau commit.
- **Tiếp theo:** `lang_en.bi5_@00009bd3` (`Play current Dungeon?`), còn đúng 32 mục menu; hoàn tất menu, rồi bắt đầu kiểm tra CMC/talk như hàng đợi.

## Lượt 012 — 10/10/2026 (200 mục mới: menu + CMC/talk)

- **Menu:** 32 mục cuối (`lang_en.bi5_@00009bd3` → `lang_en.bi5_@00009f3d`) chuyển `todo→draft`; **1.016/1.016 menu hoàn tất ở mức nháp**. Sửa một bản dịch cũ ở `@0000943b` (fragment `corridor item.`) thành trung tính `hành lang.` do source lặp trong ngữ cảnh khác.
- **CMC:** 11 câu `LCmc000` + 11 câu `LCmc002` được dịch nháp; giữ tiền tố `$`/`(` và newline, không tự gán người nói.
- **Talk:** 146 candidate đầu trong `tk100_en.bin_` (`talk/en/tk100_en.bin_@00001158` → `talk/en/tk100_en.bin_@00008727`) được dịch nháp; nhiều câu chỉ là mảnh ASCII NUL, chưa thể xác minh speaker/trật tự nên ghi notes ở từng mục.
- Tổng 200 mục `todo→draft` (32+22+146), cộng 1 chỉnh sửa bản dịch cũ có lý do. Kiểm tra ID/source/sha/offset/source_review/order bất biến; Unicode NFC, số newline, ký hiệu đặc biệt và bản dịch nguồn trùng. Font V3 không đổi, không commit ROM/ISO/payload.
- **Chưa kiểm thử game:** menu cần kiểm tra bố cục và đủ glyph; CMC/talk hiện không có parser/repacker và không thể trực tiếp tích hợp vào game. Sau push CI Windows/Ubuntu chạy validator và unittest.
- **Tiếp theo:** `talk/en/tk100_en.bin_@00008818` (`. We won't attack you.`), sau đó làm các ứng viên hội thoại tiếp theo và nghiên cứu ghép fragment.

## Lượt 013 — 10/10/2026 (200 ứng viên talk/CMC)

- 168 mục `todo → draft` còn lại trong `translations/catalogs/talk/tk100_en.bin_.json` (`talk/en/tk100_en.bin_@00008818` → `@000106cf`): **314/314 tk100 đã có bản dịch nháp**. Có ghi chú theo từng ID về những mảnh lời thoại bị cắt, ký hiệu chưa rõ và các tên riêng cần xác minh.
- 24 mục CMC của `LCmc004_en.bi5_.json` (`@00003c70` → `@000040cc`): bản dịch tự nhiên hơn, giữ ký hiệu đầu `(`, `$`, `0`, `4`, `8`, dấu phẩy và ngắt dòng. Halflive/Faery giữ danh xưng.
- 8 nhãn giao diện đầu tiên của `tk101_en.bin_` (`@00001158` → `@00001650`) dùng bản dịch thống nhất từ `tk100`; tiếp tục ở `@000016b4`.
- **Tổng 200 mục mới** (168 + 24 + 8), toàn bộ dự án còn **10.502 `todo`**. QA: ID, source, hash, file_offset, source_review, order bất biến; chỉ vi/status/notes, Unicode NFC, số ngắt dòng, placeholder/tiền tố không mất; 0 source trùng có bản dịch mâu thuẫn trong tk100, tk101 hoặc giữa hai tệp.
- Phân tích scanner `tools/catalog.py`: `candidate_runs` lấy ASCII dài ≥4 kết thúc NUL, không xác định bảng speaker hay đầy đủ câu; trong 314 ứng viên tk100 có 217 source bắt đầu bằng newline và 23 source bắt đầu bằng khoảng trắng. Xem `docs/DIALOGUE_CANDIDATE_AUDIT.md`. **Không** coi bản nháp là văn bản đã sẵn sàng repack.
- Font Merienda V3, binary/ROM/ISO không đổi; chưa kiểm thử RPCS3. Sau commit chạy GitHub Actions trên Windows/Ubuntu (validator + unittest).
- **Tiếp theo:** `talk/en/tk101_en.bin_@000016b4` và nghiên cứu parser dựa trên byte dữ liệu local trước khi tạo repacker.

## Lượt 014 — 10/10/2026 (200 ứng viên tk101, QA xưng hô)

- Dịch 200 mục `todo → draft` của `translations/catalogs/talk/tk101_en.bin_.json`, từ `talk/en/tk101_en.bin_@000016b4` đến `talk/en/tk101_en.bin_@0000c427`. Tệp hiện 208/447 draft, còn 239 todo.
- Trọng tâm: quá khứ của Ellen và mẹ, nhà thờ và biến cố 17 năm trước, các cuộc điều tra/hỏi chuyện ở Doolin, lời người dân địa phương, Gam và Gee. Chỉ dùng `tôi/bạn` trung tính khi thật sự cần; lược chủ ngữ ở mảnh thoại thiếu speaker, không áp đặt `anh/em`, `ông/cháu`, `mày/tao` và không gán người nói từ offset.
- Giữ câu Gam/Gee tự giới thiệu và danh xưng, trạng thái cảm xúc, mẫu `$`/`(`, số newline, dấu cách đầu nguồn. 12 source trùng trong lượt và 11 source trùng tk100 được kiểm tra, 0 mâu thuẫn bản dịch; các cụm khó xác minh ghi notes riêng.
- QA: đúng 200 ID todo theo thứ tự, chỉ chỉnh vi/status/notes, giữ English/source sha256/file_offset/source_review/metadata; Unicode NFC, placeholder và newline; font Merienda V3/ROM/payload không thay. Các mảnh vẫn chưa sẵn sàng repack.
- Bổ sung chính sách xưng hô vào `docs/TRANSLATION.md`: đại từ phải theo người nói/quan hệ đã xác minh; không nhất loạt dùng một cặp cho mọi nhân vật; tiếng Ireland khẩu ngữ dịch tự nhiên nhưng không suy thân thiết; đặc biệt các fragment phải giữ draft + notes.
- Chưa chạy game; sau commit kiểm tra CI Windows/Ubuntu validator + unittest.
- **Tiếp theo:** `talk/en/tk101_en.bin_@0000c5ec` — ` / spirits in your world.`.

## Lượt 015 — 10/10/2026 (200 candidate tk101)

- Xử lý đúng 200 mục `todo→draft` từ `talk/en/tk101_en.bin_@0000c5ec` đến `talk/en/tk101_en.bin_@00017241`; tk101 đạt 408/447, còn 39 todo. Toàn dự án đạt 1.784 draft, còn 10.102 todo.
- **146/200 source trùng các bản draft đã có trong tk100 hoặc tk101**, tái sử dụng nguyên bản tiếng Việt nhằm không làm lệch xưng hô/thuật ngữ; **54 mảnh chưa từng dịch** được soạn mới và ghi notes theo vị trí. Trong những chuỗi mới: nhắc Sứ giả, vùng đất của người chết, Id, Folk, kỹ năng và các cảnh trò chuyện Doolin.
- Rà đại từ theo ngữ cảnh: khi thiếu người nói/đầu câu thì dùng câu trung tính hoặc lược đại từ, không tự gán quan hệ. Notes chỉ rõ những chỗ còn cần soát trong cảnh như Messengers, Audience Hall, Freezing Id và những tiếng lắp bắp.
- QA trước commit: chỉ vi/status/notes đổi ở đúng 200 ID; bảo toàn source/source_sha256/file_offset/source_review, số newline, ký hiệu đầu, Unicode NFC, placeholders; **0 xung đột nguồn trùng** giữa tk100/tk101. Font V3 và binary game không thay đổi.
- CMC/talk vẫn chưa có parser/repacker hoặc kiểm thử RPCS3; không được coi là bản dịch đã tích hợp. Sau commit xác minh CI Windows/Ubuntu validator và unittest.
- **Lượt 016:** tiếp `talk/en/tk101_en.bin_@000172c5` (39 mục cuối tk101), rồi theo hàng đợi catalog tiếp theo.

## Lượt 016 — 11/10/2026 (200 ứng viên hội thoại)

- Hoàn tất 39 mục cuối `tk101` (`talk/en/tk101_en.bin_@000172c5` → `@00018cab`) theo đúng bản dịch `tk100` vì nguồn trùng, đưa `tk101` lên 447/447 `draft`.
- Tiếp tục 161 mục đầu `tk102` (`talk/en/tk102_en.bin_@00001158` → `@0000987f`): **24 mục nguồn trùng** dùng bản nháp đã dịch trong các tệp/trong nhóm, **137 mục nguồn mới** dịch theo sắc thái điều tra. Tệp hiện có 161/494 draft, còn 333 todo.
- Nội dung mới: Doolin, án mạng, đồng đội cũ, bức ảnh kỷ vật, nhà thờ, biến cố 17 năm trước, thần thoại Celtic và những lời đối thoại về Cõi âm. Không gán nhân vật cho câu chỉ có fragment; dùng cách xưng hô trung tính/lược đại từ khi chưa có chứng cứ. Ghi notes riêng cho nguồn mơ hồ (`close?`, `all Faerys`, `my mother`, `The photo was of that?`).
- QA: đúng 200 mục `todo → draft`, giữ metadata, source, source_sha256, file_offset, source_review= `candidate`; Unicode NFC, số newline, token/tiền tố được giữ nguyên; kiểm tra bản dịch trùng không mâu thuẫn. Font Merienda V3 không đổi, chưa cài patch, chưa test RPCS3.
- Toàn bộ **1.984/11.886** mục có bản dịch nháp, còn **9.902** mục todo. Đây là tiến độ *dữ liệu trích xuất*, không phải ước lượng phần game đã Việt hóa chạy được. Sau commit GitHub Actions chạy validator + unittest Windows/Ubuntu.
- **Lượt 017:** `talk/en/tk102_en.bin_@00009981` (`devastated. They were close.`).

## Lượt 017 — 11/10/2026 (200 ứng viên tk102)

- Dịch **200 mục** `todo→draft` trong `translations/catalogs/talk/tk102_en.bin_.json` từ `talk/en/tk102_en.bin_@00009981` đến `@00016695`; tk102 hiện **361/494 draft**, còn 133 mục chưa dịch.
- **113 mục** tái dùng bản dịch từ chuỗi tiếng Anh trùng đã dịch trong tk100/tk101/tk102, **87 mục** lần đầu có draft. Không có nguồn trùng nhận hai bản Việt hóa khác nhau trong ba tệp.
- Chủ đề: người phụ nữ ngồi xe lăn, tín ngưỡng về linh hồn, Halflive, quán rượu Doolin, lời Gam/Gee tranh cãi, Sứ giả, hướng dẫn Folk và giáp phòng thủ. Những phần không rõ ngôi nói, thân phận hoặc tên skill (Ultimate Spear), địa danh đều được ghi chú vào `notes`. Giọng Việt tự nhiên, không áp đặt quan hệ nhân vật khi nguồn chỉ là fragment.
- QA: đúng 200 item `todo→draft`, chỉ `vi/status/notes` được sửa; bất biến ID/source/hash/offset/source_review/order, Unicode NFC, số newline, placeholder và ký hiệu đầu câu. Font Merienda V3 không đổi, chưa build binary và chưa test RPCS3.
- Tiến độ catalog trích xuất: **2.184/11.886 draft**, còn **9.702 todo**. Đây là dữ liệu nháp chưa phải phần trăm game đã chơi được bằng tiếng Việt.
- Sau commit CI Windows/Ubuntu chạy `python tools/catalog.py validate` và unittest. **Lượt 018:** `talk/en/tk102_en.bin_@0001670a` (`an end to this.`).

## Lượt 018 — 11/10/2026 (200 ứng viên hội thoại)

- Hoàn thành **133 mục cuối `tk102`** (`@0001670a` đến `@0001c28b`), tất cả nguồn trùng bản nháp `tk100`/`tk101`; tái dùng nguyên văn bản dịch để giữ xưng hô và thuật ngữ thống nhất. **`tk102` 494/494 draft, 0 todo**.
- Dịch **67 mục đầu `tk103`** (`@00001158` đến `@00004bdb`), 20 mục dùng lại nguồn/bản dịch có sẵn và 47 mảnh mới. Nội dung điều tra người chồng mất tích, nhân vật bác sĩ, chuyện người sống/người chết, thế giới Lãng quên. `tk103` hiện 67/578 draft, còn 511 todo.
- QA xưng hô: giữ `tôi` hoặc lược đại từ với mảnh lời chưa xác định speaker; chưa suy quan hệ của nữ nhân vật đang tìm chồng hoặc cách gọi `son`. Những câu cần soát như `your husband's death`, `taste then, son`, `Oblivion` đã được ghi notes; `Lãng quên` tạm dịch theo nghĩa, chưa chốt tên riêng.
- Kiểm tra chỉ thay `vi/status/notes`, ID/English/source hash/offset/metadata/order/source_review bất biến; Unicode NFC, newline, dấu `$`/`(`/`*` và bản dịch nguồn trùng. Font Merienda V3 không đổi; CMC/talk chưa repack và chưa test RPCS3.
- Tiến độ 158 catalog: **2.384/11.886 draft**, còn **9.502 todo**. Đây là độ phủ nháp của dữ liệu được trích, chưa phải tỷ lệ Việt hóa game chơi được.
- CI sau push kiểm tra validator + unittest trên Windows/Ubuntu. Lượt tiếp theo: `talk/en/tk103_en.bin_@00004c8b`.

## Lượt 019 — 11/10/2026 (200 câu/mảnh tk103)

- Dịch **200 mục `todo→draft`** từ `talk/en/tk103_en.bin_@00004c8b` đến `@0000fc9a`. `tk103` đạt **267/578 draft**, còn 311 todo. Trong lượt có **166 lượt nguồn mới** và **34 lượt dùng lại bản dịch nguồn trùng** (từ catalog trước hoặc trong lượt). Nguồn tiếng Anh trùng không có bản dịch đối nghịch.
- Chủ đề: Herve và Đầm lầy, chuyện biến mất khỏi ký ức, phóng viên và tòa soạn, Hag/vụ án 17 năm trước, người gác hải đăng, bác sĩ, Halflive, Cung điện Lãng quên, sinh vật và câu nói lắp về châu báu. Không tự gán speaker; `Herve`, `Hag`, `Faery`, `Folk` giữ nguyên danh xưng; chỗ không chắc nghĩa `will`, quyền lực của kẻ cai trị, lắp bắp/vai nói ghi notes.
- QA: 200 source ứng viên gồm **159 đoạn mở đầu newline**, **11 đoạn mở đầu dấu cách**, và **172 chuỗi tiếng Anh khác nhau**. Vì không có đủ message boundary, tất cả tiếp tục `source_review=candidate` và `status=draft`, không chốt xưng hô cuối cùng.
- Bất biến ID, English, offset, source_sha256, thứ tự catalog, source_review; chỉ vi/status/notes thay đổi. Kiểm tra NFC, số newline, ký hiệu tiền tố, placeholder và source trùng. Không sửa font Merienda V3, ISO hoặc payload.
- **Parser/repacker:** tiếp tục cần byte vùng lân cận, pointer table, opcode/speaker từ bản gốc local; catalog trên cloud chỉ chứng minh đoạn ASCII NUL, không có căn cứ vá bằng offset trực tiếp. Chưa tạo/tuyên bố có repacker hoặc patch chạy được.
- Tổng 158 catalog: **2.584 draft / 11.886**, còn **9.302 todo**. Sau commit GitHub Actions chạy validator và unittest Windows/Ubuntu. **Lượt 020** ở `talk/en/tk103_en.bin_@0000fe1a` (`in any way you like.`).

## Lượt 020 — 11/10/2026 (200 ứng viên tk103)

- Dịch nháp 200 mục `todo→draft` từ `talk/en/tk103_en.bin_@0000fe1a` đến `@0001c740`. `tk103` đạt **467/578 draft**, còn 111 `todo`. Trong 200 lượt có **161 bản dịch tái sử dụng từ các catalog trước**, **5 lần lặp của những câu mới ngay trong lượt**, và **34 chuỗi nguồn mới phân biệt** được dịch. Không có source trùng nhận hai bản `vi` khác nhau.
- Chủ đề: chiến thuật Folk (điểm yếu hệ lửa, đông băng nước, các cánh cổng), Bogle, phòng ngự, phong ấn, cung điện, `Oblivion` xuất hiện trở lại. `Oblivion` được giữ tên gốc trong bản nháp `@00019885`, vì chưa chứng minh đó là thực thể/địa danh/trạng thái; chưa quy đổi vội thành Lãng quên. Xưng hô theo nguồn rõ nghĩa, không tự đặt speaker ở những mảnh thiếu trước/sau.
- QA: 200 mục theo thứ tự, chỉ `vi/status/notes`; bất biến ID/source/offset/source_sha256/source_review/order; kiểm tra NFC, số newline, placeholder và dấu đầu, 0 bản dịch trùng nguồn mâu thuẫn. Những mục khó hiểu có notes, vẫn `candidate`/`draft`.
- Tài liệu `docs/DIALOGUE_CANDIDATE_AUDIT.md` đã bổ sung các chuỗi còn cần parser xác minh ở `tk103`, không tự tạo repacker từ JSON; công cụ `tools/catalog.py` vẫn quét ASCII NUL, chưa có bảng người nói/pointer table đủ tin cậy. Chưa thử RPCS3, không thay binary/font Merienda V3.
- Toàn 158 catalog: **2.784/11.886 bản nháp**, còn **9.102 todo**. CI sau push sẽ chạy validator và unittest Windows/Ubuntu.
- **Lượt 021:** `talk/en/tk103_en.bin_@0001c87d` (`saxophone! Yeah, saxophone.`), dịch nốt 111 mục tk103 rồi qua catalog tiếp theo.

## Lượt 021 — 11/10/2026 (200 ứng viên tk103/tk104)

- Hoàn tất **111 mục cuối `tk103`** từ `talk/en/tk103_en.bin_@0001c87d` đến `@0002141f`; cả 111 mục có nguồn trùng với các bản dịch talk trước đó, tái dùng nguyên văn để đồng bộ ngôi xưng và thuật ngữ. `tk103` đạt **578/578 `draft`**, không còn `todo`.
- Dịch **89 mục đầu `tk104`** từ `@00001158` đến `@00004e98`: 20 mục tái dùng nguồn trước, 13 mục lặp trong batch, **56 source mới phân biệt** dịch nháp; `tk104` đạt **89/731 `draft`**, còn 642 todo.
- Ngữ cảnh: nhà Harriet, vật phẩm bằng đồng thau và kỷ vật, ghi chú bí ẩn, câu chuyện người chết và Doolin, người nhìn thấy Faery, bức ảnh và những người được che chở. Câu thiếu speaker được ghi notes; các nguồn `year to live`, `bare to watch` (nghi lỗi chính tả tiếng Anh), `Anachronisms` và `acting` còn cần kiểm chứng khi ghép lời thoại hoàn chỉnh.
- QA: đúng 200 `todo→draft` ở hai tệp, chỉ thay vi/status/notes; ID/source/offset/source_sha256/source_review/order giữ nguyên; NFC, số newline, placeholders và tiền tố kỹ thuật đã soát. 0 xung đột source trùng trong các catalog tk100–104. Tất cả talk vẫn `source_review=candidate`, không phải câu đã xác minh trong game.
- Toàn 158 catalog: **2.984/11.886 mục `draft`**, còn **8.902 `todo`**. Font Merienda V3/game binary không đổi; chưa có parser/repacker talk và chưa test RPCS3. Sau push xác minh CI Windows/Ubuntu validator/unittest.
- **Tiếp lượt 022:** `talk/en/tk104_en.bin_@00004f2e` (`world, at least.`).
