# Hàng đợi — 10/10/2026

## Bắt đầu ngay

1. `translations/catalogs/talk/tk101_en.bin_.json`: tiếp tục từ `talk/en/tk101_en.bin_@0000c5ec` (` / spirits in your world.`), còn 239 `todo`. Giữ phương án xưng hô trung tính khi chưa xác minh speaker; ghi chú các mảnh câu trước khi xét sửa theo bối cảnh.
2. `translations/catalogs/talk/tk100_en.bin_.json`: đã đủ 314/314 `draft`; `LCmc000`, `LCmc002`, `LCmc004` có 46/46 `draft`. Các ứng viên cần được parser xác minh trước khi nâng `source_review`.
3. Trước khi build talk/cmc: đọc `docs/DIALOGUE_CANDIDATE_AUDIT.md`; khảo sát vùng byte trước/sau string và bảng con trỏ ở local (nguyên bản), phân định prefix text/control/metadata; chưa có repacker an toàn.
4. Menu `lang_en.bi5_`: 1.016/1.016 `draft`; cần QA độ dài/glyph/alias và hiển thị RPCS3. Tiếp tục các catalog theo `translations/index.json`; ID tệp không nhất thiết là thứ tự truyện.

## Mốc bàn giao

Menu đã đủ 1.016/1.016 `draft`; CMC 46 `draft`; tk100 314/314 `draft`; tk101 208/447 `draft`. Còn 10.302 mục `todo` trên 158 catalog. Tất cả hội thoại vẫn là draft, chưa parser/repacker/test.
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
