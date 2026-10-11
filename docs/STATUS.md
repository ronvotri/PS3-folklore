# Tiến độ — cập nhật 11/10/2026

## Đã xác nhận

- BCUS98147 PS3 trong E:\Game\Folklore, đóng cùng RPCS3.
- Menu thử: 118 cặp, thay 134 chuỗi EN và 132 UK, 2.998 tham chiếu mỗi tệp.
- Merienda Regular 400 được người dùng chọn.
- V1/V2 có khoảng hở sau ấ/ớ; V2 thu gọn glyph vẫn còn lỗi.
- V3 giữ nguyên hình chữ/độ rộng V2, gán 25 chữ Việt 3 byte vào ô UTF-8 2 byte.
  Người dùng báo “ok rồi” sau thử V3. Không khẳng định toàn bộ game/font đã đạt.
- Người dùng muốn tự mở/điều khiển game và báo bằng hình, không cần agent mở game.

## Sẵn sàng dịch trên cloud

158 catalog / 11.886 mục văn bản: 1.016 menu đã đọc bảng con trỏ, 10.870 ứng
viên hội thoại/tương tác/cảnh. Có 1.016 mục menu `draft`, 0 menu `todo`; 46 mục CMC `draft`; talk tk000, tk011, tk100–tk107, tk206, tk207 có tổng 3.273/3.273 `draft`. Toàn bộ **9.351 draft / 11.886** catalog entries, còn **2.535 todo** (10.870 mục dialogue/candidate tổng); chỉ là tiến độ bản nháp ứng viên, chưa phải bản vá chạy game.
Đã có 46 câu CMC draft; các tệp talk tk000/tk011, tk100–tk107, tk200–tk207, tk306 hoàn tất draft; tk307 và tk500 đã hoàn tất (811/811 và 528/528 draft). Speaker/metadata/parser/repacker chưa xác minh; tất cả vẫn chỉ draft.
Các catalog có ID theo tệp/offset, nguồn/hash, bản dịch/trạng thái/ghi chú.
Không cần ROM để dịch hoặc kiểm tra catalog. Cloud không truy cập ổ E:.

## Công cụ và kiểm tra

- Bộ 12 unittest đã qua local Windows/Python 3.12.
- Validator đã qua toàn bộ 11.886 mục.
- Công cụ font portable tạo đúng SHA-256 font V3 đã thử (cùng nguồn Merienda
  pinned, instantiate weight 400, Pillow 12.3.0). Metadata/hash ở font_baseline.json.
- CI Windows/Linux chạy unittest và validator. Không suy CI từ kết quả local;
  xem GitHub Actions của commit tương ứng.
- Legacy folklore.py vẫn là ASCII: không dùng nó cài đè trực tiếp game V3.

## Trọng tâm kỹ thuật mới — 11/10/2026

Theo xác nhận của người dùng, **ưu tiên đọc đúng cấu trúc và đóng gói hội thoại** thay vì chỉ tăng tổng số chuỗi `draft`. Đã commit `tools/dialogue_probe.py` và 6 test giả lập tại `tests/test_dialogue_probe.py`, thêm hướng dẫn `docs/DIALOGUE_BINARY_PROBE.md`. Bộ test probe độc lập 6/6 PASS trên fixture tổng hợp; **chưa chạy trên binary gốc từ máy người dùng**, chưa xác minh GitHub Actions, chưa có parser/serializer/repacker talk/CMC. Công cụ chỉ đọc archive, so SHA và mọi nguồn ASCII-NUL với catalog, kiểm tra ranh giới CMC, lấy mẫu bytes xung quanh và mẫu tham chiếu u32 (chưa khẳng định pointer). Báo cáo local nằm ở `local-data/` hoặc `dist/` được ignore. Tuyệt đối không vá ở offset nguồn.

Giữ nguyên **9.351/11.886 draft, 2.535 todo**, chưa có thay đổi dịch trong lượt này. Trước khi gọi một lời thoại là reviewed/tested phải xác minh speaker và scene, có parser lossless và in-game QA. Phân biệt rõ *đã dịch nháp* / *đã biên tập có ngữ cảnh* / *đã thử trong game* khi thông báo.

## Phần còn thiếu

Parser/repacker talk/cmc chưa có. Các tiền tố candidate chưa chắc là lời thoại.
Cần thêm glyph/alias cho toàn bộ chữ Việt, dấu câu và các câu mới. Phần menu
mẫu gần đầy; một câu dài có thể vượt vùng. Phim/chữ trong ảnh chưa dịch.
PS3 thật, ISO và Steam Deck chưa kiểm thử. Source font coverage != game coverage.

## Phục hồi local

Các gói payload chỉ lưu trên máy: Folklore-menu-thu, Folklore-menu-co-dau-demo,
Folklore-font-spacing-v2, Folklore-font-encoding-v3 trong outputs/ của phiên local.
Đóng RPCS3. Khôi phục ngược thứ tự V3 → V2 → demo có dấu nếu cần quay về font
ban đầu/menu không dấu. Giữ toàn bộ gói. Không đưa payload lên GitHub.

## Lượt menu 001 — 10/10/2026

- Đã dịch tiếp đúng 50 mục `todo` theo thứ tự catalog menu, giữ nguyên metadata/nguồn/offset và số ngắt dòng mỗi nguồn.
- 50 mục chuyển sang `draft`, chưa chuyển `reviewed` hay `tested`; chỉ xác minh cấu trúc dữ liệu, chưa thử hiển thị/chạy game. Bản font Merienda V3 được giữ nguyên.
- Tên kỹ năng/cõi `Siêu hóa`, `Cõi Faery`, `Cõi Địa Ngục` đang là thuật ngữ tạm; xem ghi chú trong từng entry và QUEUE.md.
- Kiểm tra trước ghi GitHub: đối chiếu ID và metadata, NFC, newline, placeholder. CI push sẽ chạy validator và 12 unittest trên Windows/Linux; xác nhận ở Actions của commit.

## Lượt menu 002 — 10/10/2026

- Hoàn tất thêm 50 bản dịch menu `draft` (`lang_en.bi5_@0000419f` → `lang_en.bi5_@00004bb3`), nâng tổng menu `draft` lên 234/1.016.
- Rà tóm tắt Ellen/Keats, áo choàng/hiệu ứng và địa danh. Chỉ đổi `vi/status/notes`, không sửa dữ liệu nguồn, offset, metadata hay tệp nhị phân/font.
- Kiểm soát 50 mục, số dòng, ký hiệu vòng tròn và xung đột bản dịch cùng nguồn trước commit; chạy GitHub Actions validator/unittest Windows/Linux sau khi đẩy. Chưa xác minh runtime/bố cục/font với các bản dịch mới.
- Checkpoint lượt tiếp ở `lang_en.bi5_@00004bc6`, xem QUEUE.md.

## Lượt menu 003 — 10/10/2026

- Đã dịch thêm 50 mục menu `todo` → `draft` từ `lang_en.bi5_@00004bc6` đến `lang_en.bi5_@00004e95`. Tổng menu có `284` draft, còn `732` todo; toàn dự án còn 11.602 todo.
- Nhóm địa danh Doolin/Thế giới, HP/EXP, loại sát thương/trạng thái, tên vật phẩm. Các từ ngữ mơ hồ được ghi chú để xác minh thực tế, nhất là Inquisition Bridge, Murk, Henge và tên các hiệu ứng.
- Chỉ sửa `vi/status/notes` cho đúng 50 mục, không sửa nguồn, ID, metadata, offset hay font Merienda V3. Đã rà token, NFC, ngắt dòng và xung đột nguồn trùng ở tầng dữ liệu.
- Chưa test trong game, chưa xác nhận bố cục/font mới. Validator và unittest được chạy qua GitHub Actions Windows/Linux sau commit; cần xác nhận trạng thái run.
- Lượt sau bắt đầu tại `lang_en.bi5_@00004ea3`.

## Lượt menu 004 — 10/10/2026

- 50 mục menu mới từ `lang_en.bi5_@00004ea3` đến `lang_en.bi5_@00005386` chuyển từ `todo` sang `draft`. Tổng menu `334` draft / 1.016, còn `682` todo.
- Dịch 16 tên vật phẩm và 34 nhãn trang sách thuộc Cõi Faery, Warcadia, Thành phố đáy biển, Hành lang Vô tận. Những vật phẩm có nghĩa/màu còn bất định được gắn notes để xác minh sau.
- Kiểm tra cấu trúc trước commit: giữ nguyên source/metadata/offset/source_review/order, chỉ đổi vi/status/notes; bảo toàn NFC, newline, control token; không có xung đột chuỗi nguồn trùng.
- Bản dịch chỉ ở mức catalog, chưa dựng patch hoặc thử trong RPCS3; font V3 vẫn nguyên vẹn. GitHub Actions tự chạy validator + unittest Windows/Linux sau push.
- Checkpoint tiếp theo: `lang_en.bi5_@000053ab`.

## Lượt menu 005 — 10/10/2026

- Chuyển 50 mục `todo` sang `draft` trong `translations/catalogs/menu/lang_en.bi5_.json`, từ `lang_en.bi5_@000053ab` đến `lang_en.bi5_@00005956`. Hiện menu `384` mục draft, `632` mục todo; toàn 158 catalog còn 11.502 todo.
- Dịch 26 trang sách tranh, 13 tên sách tranh, 7 áo choàng, 4 vật phẩm truyện; giữ nguyên tên người và tên riêng đã thống nhất.
- Corrupt Village và một số tên áo choàng còn cần đối chiếu trong game, đánh dấu notes. Bỏ khoảng trắng thừa ở bản dịch một nhãn nhưng không động vào nguồn tiếng Anh.
- QA trước commit: chỉ sửa trường vi/status/notes cho 50 entry, bất biến ID/source/hash/offset/metadata/thứ tự; đảm bảo Unicode NFC, bảo toàn newline và control tokens, không xung đột source lặp.
- Font Merienda V3 được giữ nguyên; chưa triển khai patch, chưa kiểm thử bố cục trong RPCS3. GitHub Actions chạy validator và unittest Windows/Linux sau commit.
- Lượt tiếp theo bắt đầu ở `lang_en.bi5_@00005982`.

## Lượt menu 006 — 10/10/2026

- Đã thêm 50 bản dịch nháp (`lang_en.bi5_@00005982` → `lang_en.bi5_@00006235`). Tổng `434`/1.016 menu đã có draft; `582` menu todo, 11.452 todo toàn bộ 158 catalog.
- Nhóm: mô tả vật phẩm, tác dụng áo choàng Sidhe, sách tranh Folk, nút kết thúc/lưu game. Giữ nguyên `[Link item]`, MC, tên nhân vật và tên cõi; tên chưa rõ có notes.
- Trước commit đã rà 50 ID, metadata bất biến, NFC, số dòng, token bảo vệ, nguồn lặp không xung đột; chỉ vi/status/notes được đổi. Font Merienda V3 không thay đổi.
- Chưa thử game hoặc bản build; GitHub Actions chạy validator + unittest Windows/Ubuntu. Lượt 007 tại `lang_en.bi5_@00006243`.

## Lượt menu 007 — 10/10/2026

- Đã hoàn tất thêm 50 bản dịch menu `draft` (`lang_en.bi5_@00006243` → `lang_en.bi5_@0000657d`): tổng `484`/1.016 draft, còn `532` todo menu; 11.402 todo toàn bộ catalog.
- Dịch nhóm thoát/lưu/tải, tiêu đề chủ đề cốt truyện, chọn nhân vật/cõi và thuộc tính/nhãn lưu dữ liệu. Các tên vùng giữ nhất quán với lượt trước; Corrupt Village/Làng Tha hóa và một số tiêu đề còn tạm.
- Soát 50 mục đúng thứ tự todo; chỉ vi/status/notes đổi, metadata, hash, offset, nguồn nguyên trạng; NFC, số xuống dòng, token đặc biệt và bản dịch nguồn trùng được kiểm tra. Font V3 giữ nguyên.
- Chưa có kiểm tra hiển thị/bố cục trong RPCS3. GitHub Actions thực hiện validator/unittest Windows/Linux; lượt 008 bắt đầu `lang_en.bi5_@00006583`.

## Lượt menu 008 — 10/10/2026

- 50 mục menu `todo` → `draft` từ `lang_en.bi5_@00006583` đến `lang_en.bi5_@00006821`. Tổng menu `534` draft / 1.016, còn `482` todo; 11.352 todo toàn bộ 158 catalog.
- Đã dịch hiệu ứng nguyên tố/trạng thái, thông báo Karma/nâng cấp Folk, nhiệm vụ và bộ đếm 20 → 1, giữ `%s`, MC, Folk, Karma, Malabaricus nguyên dạng. Từ chuyên môn cần rà được ghi notes.
- QA trước commit: giữ source/ID/sha/offset/order/metadata, chỉ vi/status/notes thay ở 50 mục; NFC, newline, placeholder và nguồn trùng đều kiểm tra đạt; Merienda V3 không đổi.
- Chưa xác nhận hiển thị trong RPCS3. CI GitHub Actions kiểm tra validator/unittest Windows/Linux. Lượt 009 bắt đầu `lang_en.bi5_@00006833`.

## Lượt menu 009 — 10/10/2026

- Dịch đúng 50 mục menu `todo` → `draft` từ `lang_en.bi5_@00006833` đến `lang_en.bi5_@00007030`. Menu hiện `584`/1.016 draft và `432` todo; còn 11.302 todo trong toàn bộ 158 catalog.
- Nội dung: PSP™ Link nhận/gửi Folk, trao đổi Id, 4 nhiệm vụ Herve, thiết bị Memory Stick™, dữ liệu lỗi và thông báo Rank up/HP của Keats/Ellen. Giữ placeholder `%s`, `%d`, ™/® và tên riêng; ghi chú các nguồn tiếng Anh có lỗi đánh máy nhưng không sửa source.
- Đã soát đúng 50 mục và các trường chỉ được sửa vi/status/notes; kiểm tra NFC, newline, token, nguồn trùng không xung đột; giữ Merienda V3 và metadata không đổi.
- Chưa build binary/patch hoặc test hiển thị RPCS3. GitHub Actions chạy validator/unittest Windows/Linux sau commit.
- Checkpoint lượt 010: `lang_en.bi5_@00007059`.

## Lượt menu 010 — 10/10/2026 (200 mục)

- Dịch 200 mục `todo` thành `draft` từ `lang_en.bi5_@00007059` đến `lang_en.bi5_@0000874e`; hiện `784`/1.016 menu draft, còn `232` menu todo và 11.102 todo trên 158 catalog.
- Nội dung: điều kiện tấn công nguyên tố/Folk, đá ký ức, sách tranh, cảnh báo HDD, menu tương tác/tùy chọn, tên nhân vật/vai, thoại Ellen–Keats–Livane, phụ đề và chế độ hầm ngục. Giữ đúng ngữ cảnh, tên riêng và thuật ngữ.
- QA theo bốn nhóm 50: bất biến ID/source/hash/offset/source_review/order, chỉ vi/status/notes thay đổi; NFC, newline, placeholder và kiểm tra trùng nguồn không có xung đột. Các mục chưa rõ ghi notes, font V3 vẫn giữ nguyên.
- Chưa áp patch và chưa test trực tiếp RPCS3. CI Windows/Linux chạy validator và unittest sau commit. Lượt 011 tại `lang_en.bi5_@00008757`.

## Lượt menu 011 — 10/10/2026 (200 mục)

- Hoàn tất 200 mục menu `todo` → `draft` (`lang_en.bi5_@00008757` đến `lang_en.bi5_@00009bbd`). Menu hiện `984`/1.016 bản nháp, còn `32` chưa dịch; toàn bộ catalog còn 10.902 todo.
- Nội dung: tạo và tải hầm ngục, chơi thử, tính điểm, màn xếp hạng, mạng/PSN, giới hạn phòng/vật phẩm, popup quản lý hầm ngục và các nhãn giao diện. Nhiều câu tiếng Anh được tách thành fragment, đã dịch có xét chuỗi liên tiếp mà không sửa source hay offset.
- QA bốn nhóm ~50: 200 mục thay đúng vi/status/notes; source, id, offset, hash, source_review và thứ tự bất biến; kiểm tra Unicode NFC, newline, placeholder và ký hiệu gamepad/trademark; kiểm tra source trùng không xung đột. Font Merienda V3 giữ nguyên.
- Chưa chạy RPCS3/cài patch, mọi mục vẫn draft; CI Windows/Linux chạy validator + unittest sau commit. Lượt 012 sẽ dịch nốt 32 mục menu tại `lang_en.bi5_@00009bd3`, sau đó chuyển sang CMC/talk.

## Lượt 012 — 10/10/2026 (200 mục mới)

- Dịch nốt 32 menu `todo→draft`, hoàn thành 1.016/1.016 mục menu nháp; QA sửa một fragment `corridor item.` cũ do nguồn lặp trong các cảnh có nghĩa khác nhau.
- Thêm 22 câu CMC (LCmc000 và LCmc002) và 146 ứng viên trong talk tk100. Nhiều câu bị quét thành mảnh có newline đầu hoặc tiền tố như `$`, `(`, `*`: đã giữ nguyên ở vi và notes, không tự đặt người nói.
- Tổng thêm 200 mục `draft`; còn 10.702 `todo` toàn bộ catalog. Giữ dữ liệu nguồn/ID/hash/offset/thứ tự/source_review, kiểm tra NFC/newline/token và source trùng trong từng catalog. Không sửa Merienda V3.
- Chưa thử hiển thị RPCS3; chưa có repacker talk/cmc. CI Windows/Ubuntu chạy validator + unittest sau commit. Lượt tới ở `talk/en/tk100_en.bin_@00008818`.

## Lượt 013 — 10/10/2026 (200 mục mới)

- Đã dịch nháp toàn bộ 168 mục còn lại của `tk100` (314/314 có draft), 24 mục CMC của `LCmc004` và 8 mục giao diện đầu `tk101` (8/447). CMC hiện 46 draft trong ba tệp, talk 322 draft; toàn dự án còn 10.502 todo.
- Rà tiền tố như `$`, `(`, chữ số 0/4/8, dấu câu đầu chuỗi, xuống dòng; không gán người nói, không chỉnh sửa source/offset/metadata. Đánh dấu notes cho các candidate thiếu ngữ cảnh; kiểm tra NFC/newline/tokens và không có xung đột bản dịch nguồn trùng.
- Khảo sát cấu trúc: `tools/catalog.py` mới quét mảnh ASCII kết thúc NUL; 217/314 ứng viên tk100 mở đầu bằng newline, 23/314 mở đầu bằng space. Chưa đủ bằng chứng để suy pointer table/speaker, và chưa có repacker. Phân tích chi tiết và kế hoạch xác minh trong `docs/DIALOGUE_CANDIDATE_AUDIT.md`.
- Chưa thử RPCS3, chưa thay font Merienda V3, không có patch/binary. Sau commit, CI Windows/Ubuntu chạy validator + unittest. Checkpoint tiếp theo: `talk/en/tk101_en.bin_@000016b4`.

## Lượt 014 — 10/10/2026 (200 câu/mảnh tk101)

- Thêm 200 mục `draft` trong `tk101`, từ `talk/en/tk101_en.bin_@000016b4` đến `talk/en/tk101_en.bin_@0000c427`; tk101 đạt 208/447, còn 239 todo. Tổng dự án: 1.584 draft, 10.302 todo.
- Rà xưng hô theo bối cảnh có thể suy từ chữ nguồn: mẹ/con, ký ức 17 năm, nhân vật điều tra, người dân Doolin, Gam/Gee. Không tự gán tên speaker hay quan hệ từ ID; dùng cách diễn đạt trung tính/lược đại từ khi mất chủ ngữ; đánh dấu notes cho mảnh không đủ nghĩa. Bổ sung quy tắc rõ trong TRANSLATION.md.
- QA NFC, số dòng, placeholder, tiền tố; không sửa source/hash/offset/metadata/source_review. Soát 12 cặp chuỗi lặp nội bộ và các source trùng với tk100, 0 mâu thuẫn.
- Không cập nhật font V3/binary và chưa thử RPCS3. CMC/talk chưa có repacker đã xác minh. Sau commit GitHub Actions kiểm tra Windows/Ubuntu.
- Checkpoint lượt 015: `talk/en/tk101_en.bin_@0000c5ec`.

## Lượt 015 — 10/10/2026

- 200 mục tk101 chuyển todo→draft, tệp đạt 408/447. 146 mục lặp với tk100/tk101 đã dịch trước được giữ y bản Việt hóa; 54 source mới dịch theo nội dung và đánh dấu điểm thiếu ngữ cảnh xưng hô.
- QA đủ 200 ID: metadata/source/hash/offset/source_review không đổi, NFC/newline/placeholder/ký hiệu đầu được bảo toàn; 0 bản dịch khác nhau cho nguồn trùng trong cả hai tệp.
- Tổng tiến độ hiện 1.784 draft và 10.102 todo (toàn 158 catalog). Chưa repack/run RPCS3; font Merienda V3 giữ nguyên. Chuyển lượt 016 tại `talk/en/tk101_en.bin_@000172c5`.

## Lượt 016 — 11/10/2026 (200 mục hội thoại)

- Thêm 39 bản nháp cuối của tk101 (447/447) và 161 mục đầu tk102 (161/494). 39 mục tk101 tái dùng từ tk100; trong tk102 24 mục trùng bản dịch đã có và 137 mảnh mới dịch theo ngữ cảnh án mạng/kỷ vật/nhà thờ/17 năm trước.
- Duy trì quy tắc xưng hô: không suy speaker, tên nhân vật hay tuổi từ mảnh bị quét; notes các vế thiếu nghĩa. Kiểm tra ID/source/hash/offset/source_review, Unicode NFC, newline, token và bản dịch source trùng; dữ liệu nguồn bất biến.
- Tổng 158 catalog: **1.984 draft / 11.886**, **9.902 todo**. Chưa có repacker hội thoại, chưa test trên RPCS3; Merienda V3 và các file game không thay đổi. Sau commit xác minh CI Windows/Ubuntu.
- Tiếp theo `talk/en/tk102_en.bin_@00009981`.

## Lượt 017 — 11/10/2026 (200 câu/mảnh tk102)

- Thêm 200 mục `draft` (`@00009981` → `@00016695`), tk102 đạt 361/494. 113 bản nháp dùng lại từ nguồn đã dịch để giữ thống nhất, 87 bản nháp nguồn mới. Tổng cộng **2.184 draft / 11.886**, còn **9.702 todo**.
- Rà xưng hô và diễn biến ở Doolin, Gam/Gee, tín ngưỡng linh hồn, trận chiến Folk; không gán speaker khi chỉ thấy mảnh câu, notes nêu các danh xưng/đại từ chưa chắc chắn. Giữ nguyên Halflive, Folk, Id; danh hiệu/chiêu thức chưa đủ bằng chứng chỉ là bản dịch nháp.
- Chỉ thay vi/status/notes; id/source/source_sha256/file_offset/source_review/order giữ nguyên. QA NFC, số ngắt dòng, ký hiệu đầu nguồn và chuỗi trùng không xung đột. Không chỉnh font Merienda V3 hoặc game binary; parser/repacker talk/cmc và kiểm tra RPCS3 vẫn chưa có.
- Checkpoint tiếp theo: `talk/en/tk102_en.bin_@0001670a`.

## Lượt 018 — 11/10/2026 (200 mục hội thoại)

- Hoàn thành 133 mục `tk102` (494/494 draft), tất cả có nguồn trùng `tk100/tk101` và dùng bản dịch đã thống nhất. Thêm 67 bản nháp trong `tk103` (67/578; 20 copy đúng nguồn cũ, 47 mảnh mới) có chủ đề bác sĩ/người chồng mất tích/Lãng quên. Tổng **2.384 draft**, **9.502 todo** trên 158 catalog.
- QA chỉ vi/status/notes, giữ nguyên id/source/hash/file_offset/source_review và thứ tự; đảm bảo NFC, dòng, marker và source trùng nhất quán. Đánh dấu chỗ xưng hô, danh xưng chưa rõ trong notes; không suy người nói từ offset.
- Chưa có repacker thoại và chưa chạy RPCS3/test font Merienda V3 cho các câu mới. Sau commit kiểm tra CI Windows/Ubuntu. Lượt 019 tiếp tại `talk/en/tk103_en.bin_@00004c8b`.

## Lượt 019 — 11/10/2026 (200 mục hội thoại tk103)

- `tk103` tăng 67→267 draft trên 578 ứng viên, còn 311 todo. Trong 200 lượt dịch, 34 nguồn trùng tái sử dụng bản Việt hóa, 166 lượt đầu tiên có bản nháp (tính lượt dịch, không phải 166 nguồn duy nhất). Tổng **2.584/11.886 draft**, còn **9.302 todo**.
- Ngữ cảnh: Herve, Đầm lầy, lãng quên, phóng viên, bác sĩ và các vụ án ở Doolin; đại từ chỉ tạm thời trong mảnh câu; ghi notes những từ/vai nói cần QA. 159/200 nguồn bắt đầu newline, cảnh chưa có parser xác minh.
- QA metadata immutable (source/ID/offset/hash/source_review), NFC/newline/placeholders/prefix, không có xung đột chuỗi trùng. Chỉ dịch catalog, chưa repack/test RPCS3; font Merienda V3 không đổi.
- Lượt 020 bắt đầu `talk/en/tk103_en.bin_@0000fe1a`. Sau push xác minh GitHub Actions validator + unittest trên Windows và Ubuntu.

## Lượt 020 — 11/10/2026 (200 mục tk103)

- 200 mục `tk103` đổi `todo→draft`, tệp đạt 467/578; toàn repo 2.784 `draft` và 9.102 `todo`. 161 mục kế thừa bản dịch có sẵn, 34 source mới khác nhau và 5 lần lặp trong lượt; không có xung đột source→vi.
- Nội dung: hướng dẫn trận chiến, điểm yếu hệ lửa, phong ấn, vương quốc dưới biển, `Oblivion` và những cuộc nói chuyện liên quan. Không suy tên người nói từ ID, giữ tên riêng chưa xác minh, ví dụ `Oblivion`, ở bản nháp; các fragment cần ráp có notes.
- Bảo toàn ID/offset/hash/source_review/English, Unicode NFC, newline và marker; chỉ cập nhật `vi/status/notes`. Không làm binary patch hay thay Merienda V3; parser/repacker cho talk/cmc và thử trong RPCS3 vẫn là blocker. CI Windows/Ubuntu chạy sau khi push.
- Checkpoint 021: `talk/en/tk103_en.bin_@0001c87d`.

## Lượt 021 — 11/10/2026 (200 ứng viên hội thoại)

- Hoàn thành 111 mục cuối tk103 (578/578 `draft`, đều tái dùng cùng source đã dịch), và 89 mục đầu tk104 (89/731 `draft`): 20 nguồn trùng với catalog trước, 13 bản lặp nội bộ, 56 nguồn tiếng Anh mới phân biệt. Tổng **2.984 draft/11.886** và **8.902 todo**.
- Nội dung tk104: nhà Harriet, cổ vật đồng thau, kỷ vật, người phụ nữ, bức ảnh và Faery. Giữ ngôi xưng trung tính tại câu thiếu speaker, đánh dấu notes cho `year to live`, `bare to watch`, `Anachronisms`, `acting`. Các source trùng đồng nhất vi trong tk100–104.
- Kiểm tra bất biến ID/hash/source/offset/source_review và thứ tự, NFC/newline/control marker/placeholder. Chỉ sửa `vi/status/notes`; chưa đóng gói game hay thử RPCS3, font Merienda V3 giữ nguyên. CI Windows/Ubuntu chạy validator và unittest sau push.
- Checkpoint tiếp theo: `talk/en/tk104_en.bin_@00004f2e`.

## Lượt 022 — 11/10/2026 (200 ứng viên tk104)

- `tk104` tăng 89→289 draft trên 731 ứng viên (còn 442 todo); toàn bộ 158 catalog có **3.184 draft** và **8.702 todo**. Trong lượt 200 mục: 18 bản nháp kế thừa source trùng trước đó, 3 lần lặp trong batch, 179 nguồn mới khác nhau.
- Nội dung: thư gửi bác sĩ Lester nhắc Cecilia, ký ức và chuyện chết chóc 17 năm trước, Faery, Thánh địa, nữ tư tế cổ và cổ vật. Các từ chuyên biệt chưa đủ chứng cứ hoặc fragment thiếu người nói đều có notes; không áp đặt đại từ, giữ giọng phù hợp bí ẩn/truyền thuyết.
- QA chỉ sửa vi/status/notes; ID/source/source_sha256/file_offset/source_review bất biến; NFC/newline/placeholder/tiền tố và bản dịch source trùng không mâu thuẫn. Vẫn là candidate/draft, chưa đóng gói/hỗ trợ parser/repacker talk/cmc hay thử RPCS3. Giữ nguyên font V3.
- Lượt 023 bắt đầu `talk/en/tk104_en.bin_@000108dc`. Sau commit CI Windows/Ubuntu chạy validator và unittest.

## Lượt 023 — 11/10/2026 (1.151 ứng viên hội thoại)

- Thay chính sách 200 mục cố định theo yêu cầu: xử lý được **1.151 todo→draft**, hoàn thành trọn `tk104` (731/731), `tk105` (595/595) và 6 tệp `tk000`, `tk011`, `tk106`, `tk107`, `tk206`, `tk207` (6×19=114). Trong đợt có 94 nguồn mới phân biệt tk104, 177 nguồn mới phân biệt tk105 (141+36), phần còn lại kế thừa và lặp trong đợt.
- QA của 12 tệp talk đủ draft: **3.273 mục**, không có source giống nhau mà bản Việt hóa khác nhau. Metadata English/source hash/ID/offset/source_review không thay; chỉ vi/status/notes. Kiểm tra newline, Unicode NFC, mã/placeholder/tiền tố. Những đoạn không xác minh speaker và thuật ngữ đều có notes.
- Tổng repo **4.335/11.886 draft**, **7.551 todo**. Đây là độ phủ ứng viên text, chưa có parser/repacker hay test RPCS3. Font Merienda V3 không thay. Cả 158 catalog còn rất nhiều CMC/talk chưa dịch.
- **Checkpoint kế tiếp:** `talk/en/tk200_en.bin_@00001158`, `tk200` có 280 todo. GitHub Actions Windows/Ubuntu chạy validator + unittest sau push.

## Lượt 023a — 11/10/2026 (100 mục tk200, đợt commit nhỏ)

- Xác minh main trước khi sửa: `tk104` đã có 731/731 draft và QUEUE chuyển sang tk200. Tránh làm lại công việc đã đẩy. Chọn **100 mục** thay vì ép dịch số lượng lớn theo yêu cầu tránh crash; `tk200` hiện 100/280 draft, còn 180.
- 29 bản dịch tái dùng từ nguồn đã dịch, 11 lần lặp nội bộ, 60 nguồn chưa có draft được dịch; ngữ cảnh Doolin, Halflive, người chết, quán rượu, Faery. Xưng hô tạm/notes cho fragment; chưa khẳng định speaker.
- QA bất biến ID/English/hash/offset/source_review, NFC/newline/placeholder/tiền tố, source trùng không mâu thuẫn; tất cả mới chỉ `candidate/draft`. Chưa repack thoại hay test RPCS3, giữ Merienda V3 nguyên.
- Tổng **4.435 draft/11.886**, **7.451 todo**. Tiếp `talk/en/tk200_en.bin_@00006cf8`. CI Windows/Ubuntu kiểm tra sau khi push.

## Lượt 023b — 11/10/2026 (tk200 hoàn tất)

- Chuyển 180 mục cuối tk200 từ todo sang draft (167 bản trùng nguồn tái sử dụng, 13 mảnh mới); **tk200 280/280 draft**. Toàn bộ 158 catalog: **4.615/11.886 draft**, còn **7.271 todo**.
- QA chỉ sửa vi/status/notes; ID, English, source hash, offset, source_review, thứ tự, Unicode NFC, newline, control markers và bản Việt của cùng nguồn đều nhất quán. Mọi câu vẫn là ASCII NUL candidate, chưa xác minh speaker; ghi notes chỗ cần ráp cảnh.
- Chưa có talk/cmc parser/repacker hoặc kiểm chứng RPCS3; không đụng Merienda V3, ISO/ROM/binary, không đánh dấu reviewed/tested.
- Chuyển hàng đợi sang `talk/en/tk201_en.bin_@00001158`; CI validator/unittest Windows/Linux chạy sau push.

## Lượt 024a — 11/10/2026 (50 mục đầu tk201)

- `tk201` bắt đầu: 50/496 bản nháp (19 trùng nguồn đã dịch, 31 mới), còn 446 todo. Toàn repo **4.665 draft / 11.886**, còn **7.221 todo**.
- QA metadata nguồn bất biến, NFC, newline, prefix/placeholder và bản dịch nhất quán; 31 mảnh thoại mới vẫn cần đối chiếu speaker/quan hệ sau khi có parser, đặc biệt `brother` có khả năng chỉ anh hoặc em trai. Chỉ thay vi/status/notes.
- Chưa sửa Merienda V3 hoặc đóng gói talk/cmc, chưa thử RPCS3. Sau push CI Windows/Linux validator + unittest.
- Lượt tiếp bắt đầu `talk/en/tk201_en.bin_@00003514`.

## Lượt 024b — 11/10/2026 (100 mục tk201)

- `tk201`: 100 mục liên tiếp **todo→draft** từ `talk/en/tk201_en.bin_@00003514` đến `talk/en/tk201_en.bin_@000087d1`; 2 bản trùng nguồn tái sử dụng, 98 lượt dịch nháp mới (có các mảnh lặp). Tệp đạt **150/496 draft**, còn **346 todo**. Toàn bộ 158 catalog: **4.765/11.886 draft**, **7.121 todo**.
- Các đoạn gồm cô nhi viện, ký ức từ nhỏ, hải đăng, Faery, thư từ/án mạng, mẹ và cha, người chết, câu chuyện bị bạo hành. Đa số source là fragment ASCII NUL nên không tự suy người nói hoặc quan hệ nhân vật. Đánh notes nơi đại từ hoặc nghĩa cần ráp cảnh.
- QA: chỉ vi/status/notes thay đổi, 100 ID theo đúng checkpoint; bảo toàn id/source/offset/hash/source_review/thứ tự, Unicode NFC, newline, ký hiệu đầu và placeholder; 0 xung đột khi câu nguồn trùng. Chưa có parser/repacker talk/cmc, chưa thử RPCS3, giữ Merienda V3/ROM/payload nguyên.
- **Tiếp theo:** `talk/en/tk201_en.bin_@0000884d` (`every thing we see in our dreams?`). GitHub Actions validator/unittest được kích hoạt qua commit.

## Lượt 024c — 11/10/2026 (100 mục tiếp tk201)

- `tk201`: dịch thêm **100 todo→draft**, từ `talk/en/tk201_en.bin_@0000884d` đến `talk/en/tk201_en.bin_@0000eca9`: **29** nguồn trùng catalog trước, **7** lặp nguồn trong lô, **64** mảnh mới khác nhau. `tk201` đạt **250/496 draft, 246 todo**. Toàn bộ 158 catalog đạt **4.865/11.886 draft**, còn **7.021 todo**.
- Nội dung: điều tra ở nhà thờ, dân làng/nhà nghiên cứu, người sống và người chết, gia đình, quán rượu, Gam/Gee, Sứ giả, hướng dẫn Faery và Folk. Giữ nguyên tên riêng đã thống nhất, không tự gán speaker/quan hệ.
- QA đúng vùng 100 ID, chỉ thay vi/status/notes; giữ source/ID/SHA/offset/source_review/order, NFC, newline, dấu đầu, placeholder và nguồn trùng đồng nhất. Những mảnh lược chủ ngữ và ngôi xưng nghi vấn đã ghi notes. Tất cả vẫn candidate/draft, không có parser/repacker hay test RPCS3; font Merienda V3, ROM/binary không đổi.
- **Tiếp:** `talk/en/tk201_en.bin_@0000ed26` (`Many different tricks to try!`) và phần còn lại của `tk201`. CI validator/unittest chạy trên GitHub Actions sau commit.

## Lượt 024d — 11/10/2026 (100 mảnh tk201, Folk/Faery/Cõi âm)

- Dịch tiếp `tk201` **100 todo→draft** từ `talk/en/tk201_en.bin_@0000ed26` đến `talk/en/tk201_en.bin_@000147df`: 33 mục tái dùng source cũ, 5 mục lặp trong lượt, 62 source mới. `tk201` đạt **350/496 draft**, còn **146 todo**. Tổng repo **4.965/11.886 draft**, còn **6.921 todo**.
- Nội dung: Sứ giả, khả năng Folk, chiến đấu theo hệ, Land of the Dead, ký ức, Mnemosyne, Oblivion (tên riêng tạm giữ) và Đại sảnh Tiếp kiến (Audience Hall, thuật ngữ tạm). Chỗ thiếu speaker/ngữ cảnh hoặc điều kiện phủ định cần xác minh có notes. Không áp đặt vai nhân vật theo offset.
- QA vùng đúng 100 ID, chỉ vi/status/notes thay đổi, id/source/source_sha256/offset/source_review/order bất biến; Unicode NFC, newline, ký tự đầu, placeholder và nguồn trùng không xung đột. Chưa có parser/repacker thoại, chưa thử RPCS3 và không đụng font Merienda V3, ISO/ROM/payload.
- **Tiếp theo:** `talk/en/tk201_en.bin_@00014b1b`; 146 mục cuối tk201 phần lớn nguồn trùng đã có bản dịch chuẩn từ tk200/tk100–105. CI validator/unittest sau commit.

## Lượt 024e — 11/10/2026 (hoàn tất 146 mục cuối tk201)

- Hoàn tất **146 todo→draft** trong `tk201`, từ `talk/en/tk201_en.bin_@00014b1b` đến `talk/en/tk201_en.bin_@0001b26b`: **146/146** source trùng hoàn toàn với bản dịch đã xác nhận nhất quán ở tk100–105, tk200 hoặc phần đầu tk201, đồng bộ nguyên văn, không viết lại làm lệch xưng hô. `tk201` đạt **496/496 draft**, còn 0 todo.
- Tổng toàn repo **5.111/11.886 draft**, còn **6.775 todo** của 158 catalog. Chỉ tính độ phủ bản nháp ứng viên trích xuất, không có nghĩa đã có patch hội thoại playable.
- QA trên 146 dòng cuối: id, source, sha256, file_offset, source_review, thứ tự giữ nguyên; chỉ vi/status/notes, Unicode NFC/newline/marker/placeholder; không source trùng được dịch mâu thuẫn. Không sửa Merienda V3, binary, ROM/ISO; talk/cmc chưa có parser/repacker và chưa thử RPCS3.
- **Lượt tiếp theo:** `talk/en/tk202_en.bin_@00001158` (`To Netherworld`); `tk202` có 518 todo. Ưu tiên xử lý source trùng trước, dịch các fragment mới theo ngữ cảnh, không tự gán speaker.
- Commit kích hoạt validator và unittest trên GitHub Actions Windows/Linux.

## Lượt 025a — 11/10/2026 (100 mục đầu tk202)

- Từ `talk/en/tk202_en.bin_@00001158` đến `talk/en/tk202_en.bin_@00006960`: dịch **100 mục todo→draft** (30 nguồn trùng tái dùng bản dịch, 70 mảnh mới); `tk202` hiện **100/518 draft**, còn 418 todo.
- Nội dung: ảnh bị xé, chuyện án mạng, quá khứ và phòng khám nhà thờ Doolin, Faery và cuộc xung đột các cõi. Không tự suy người nói/quan hệ từ offset; các fragment chỉ dịch phần ý chắc chắn, ghi notes.
- QA cục bộ: 100 ID đúng checkpoint, chỉ vi/status/notes được sửa, source/source_sha256/file_offset/source_review/order bất biến; NFC, ngắt dòng, tiền tố và placeholder không mất; nguồn trùng không mâu thuẫn. Chưa đóng gói talk/cmc, chưa test RPCS3, không sửa font Merienda V3 hoặc ROM/binary.
- Toàn bộ 158 catalog **5.211/11.886 draft, 6.675 todo**, chỉ là độ phủ dữ liệu trích xuất, không phải bản vá tiếng Việt playable.
- **Tiếp theo:** `talk/en/tk202_en.bin_@00006a5b` (`17 years ago.`); GitHub Actions chạy validator và unittest sau commit.

## Lượt 025b — 11/10/2026 (100 mục tiếp tk202)

- Dịch thêm `tk202` **100 todo→draft** từ `talk/en/tk202_en.bin_@00006a5b` đến `talk/en/tk202_en.bin_@0000d043`: 4 nguồn trùng catalog trước, 10 mảnh trùng nội bộ và 86 nguồn mới. `tk202` đạt **200/518 draft**, còn **318 todo**.
- Ngữ cảnh: 17 năm trước, vụ án ảnh xé và phòng khám Doolin, Cõi âm, quân lính, mẹ và quá khứ, truyền thuyết, nhà thờ, người gác hải đăng, lời đồn/dịch vụ của dân làng. Ghi chú ở các fragment có phụ thuộc ngôi xưng, thành ngữ và đối thoại chưa xác định speaker.
- QA cấu trúc: đúng 100 ID, chỉ vi/status/notes thay đổi; bất biến tiếng Anh/offset/source hash/source_review/order; NFC, số newline, prefix và placeholder, 0 nguồn trùng có hai bản dịch khác. Tất cả vẫn candidate/draft. Không đụng Merienda V3, game binary, ROM/ISO; talk/cmc chưa repack/test RPCS3.
- Tổng **5.311/11.886 draft**, còn **6.575 todo** trong dữ liệu trích xuất.
- **Tiếp theo:** `talk/en/tk202_en.bin_@0000d0d1`; GitHub Actions chạy validator/unittest sau commit.

## Lượt 025c — 11/10/2026 (hoàn tất 318 mục cuối tk202)

- Dịch **318 mục todo→draft** từ `talk/en/tk202_en.bin_@0000d0d1` đến `talk/en/tk202_en.bin_@0001daaf`; **273** nguồn trùng bản đã dịch (giữ nguyên từng chữ), **45** source mới dịch nháp có ghi chú khi ngữ cảnh thiếu. Rà cấu trúc theo sáu nhóm ~50. `tk202` đạt **518/518 draft**, còn 0 todo.
- Bối cảnh: Doolin, người chết, Sứ giả, vũ khí cổ, Lính Máy (tạm), lính máy hệ Sét, pháo đài, ký ức, hy sinh. Những từ máy/giáp/bình chứa, ngôi xưng, mảnh câu thiếu chủ ngữ được giữ draft+notes, không suy speaker.
- QA: chỉ sửa vi/status/notes của đúng 318 mục; English/source SHA/offset/source_review/order và mọi trường khác giữ nguyên; Unicode NFC, newline, mã đầu, placeholders, nguồn trùng không xung đột. Chưa có parser/repacker talk/cmc hoặc kiểm tra runtime RPCS3, không thay Merienda V3 hay binary/ROM/ISO.
- Tổng repo 158 catalog: **5.629/11.886 draft**, còn **6.257 todo**. Đây chỉ là độ phủ ứng viên text, không phải phần trăm patch đã chạy được.
- **Tiếp theo:** `talk/en/tk203_en.bin_@00001158` (`To Netherworld`), catalog tk203 có 663 mục. Bắt đầu theo nguồn trùng trước, sau đó mới dịch fragment mới; không có giới hạn cứng lô nhưng QA theo cảnh và commit vừa sức.
- GitHub Actions trên Windows/Linux chạy validator + unittest khi push.

## Lượt 026a — 11/10/2026 (100 ứng viên đầu tk203)

- Từ `talk/en/tk203_en.bin_@00001158` đến `talk/en/tk203_en.bin_@00005e10`: dịch **100 todo→draft**, gồm 20 câu trùng nguồn các catalog đã dịch được tái sử dụng nguyên văn và 80 mảnh mới; `tk203` **100/663 draft, còn 563 todo**.
- Ngữ cảnh: mật khẩu, người gác hải đăng, hồ sơ cái chết, nhà thờ và ký ức tập thể; Cõi âm và Oblivion. Chỉ dịch nghĩa có thể xác minh; tiền tố/nội dung thiếu speaker ghi notes, không ép anh-em, ông-cháu hoặc quan hệ người nói.
- QA trước commit: chỉ `vi/status/notes` được sửa ở 100 ID; source/hash/offset/source_review/order bất biến, Unicode NFC, newline, prefix và placeholders giữ nguyên; 0 source trùng mâu thuẫn. Chưa có parser/repacker talk/cmc hay thử hiển thị RPCS3; giữ Merienda V3/ROM/binary nguyên.
- Toàn bộ 158 catalog **5.729/11.886 draft**, còn **6.157 todo**. Đây là độ phủ nháp dữ liệu trích, không phải tỉ lệ playable.
- **Tiếp:** `talk/en/tk203_en.bin_@00005f9e` (`correct that aberration.`). CI Windows/Linux chạy validate + unittest sau commit.

## Lượt 026b — 11/10/2026 (100 mục tiếp theo tk203)

- Dịch 100 mục từ `talk/en/tk203_en.bin_@00005f9e` đến `talk/en/tk203_en.bin_@0000cb79`: 3 bản trùng nguồn catalog trước, 8 mảnh lặp nội bộ, 89 chuỗi tiếng Anh mới. `tk203` đạt **200/663 draft**, còn 463 todo.
- Chủ đề: Herve/Đầm lầy, phong ấn ngọn hải đăng, ký ức và linh hồn, hiện tượng Oblivion, các báo cáo nhân chứng và bí ẩn 17 năm ở Doolin. Các cụm như Eternal Suffering và cách gọi thế giới bên kia vẫn là nháp, cần kiểm tra scene/speaker khi có parser.
- QA: chỉ vi/status/notes tại 100 ID; bất biến ID, nguồn, source_sha256, file_offset, source_review, order, mã mở đầu/newline/placeholder/NFC. 0 xung đột nguồn trùng; không thay Merienda V3/ROM/binary. Talk/cmc chưa có parser/repacker hoặc test RPCS3.
- Tổng 158 catalog **5.829/11.886 draft**, còn **6.057 todo**. Không phải độ phủ bản patch chơi được.
- **Tiếp theo:** `talk/en/tk203_en.bin_@0000cccf` (`And for what reason?`). CI validator/unittest sau commit.

## Lượt 026c — 11/10/2026 (200 mục tk203: Doolin và Banshee)

- Từ `talk/en/tk203_en.bin_@0000cccf` đến `talk/en/tk203_en.bin_@000186a8` dịch **200 todo→draft** theo 4 nhóm QA: 130 nguồn trùng đã dịch, 12 nguồn trùng trong lô và 58 nguồn mới khác nhau. `tk203` đạt **400/663 draft**, còn **263 todo**.
- Ngữ cảnh: bác sĩ phá sản, điều tra người chết, vách đá, Banshee, điềm báo và bài hát, nhiệm vụ ở Doolin, hình bóng người chết và ký ức. Không gán speaker theo offset và chưa chốt đại từ dựa vào mảnh câu. Ghi notes cho các chỗ bị cắt hay thuật ngữ/giới tính chưa chắc.
- QA: chỉ vi/status/notes thay đổi ở 200 ID; English/source SHA/offset/source_review và thứ tự bất biến; NFC, newline, mã dẫn, ký tự kết thúc khoảng trắng, token và bản dịch nguồn trùng nhất quán. Tất cả candidate/draft; chưa có parser/repacker thoại hoặc kiểm tra RPCS3, giữ Merienda V3 và binary nguyên.
- Tổng 158 catalog: **6.029/11.886 draft**, còn **5.857 todo** của dữ liệu trích xuất, chưa phải phần trăm Việt hóa playable.
- **Tiếp theo:** `talk/en/tk203_en.bin_@00018773`; còn 263 mục tk203, trong đó nhiều nguồn trùng tk202/tk201. GitHub Actions validator + unittest được kích hoạt sau commit.

## Lượt 026d — 11/10/2026 (hoàn tất 263 mục tk203)

- Hoàn tất **263 mục todo→draft** từ `talk/en/tk203_en.bin_@00018773` đến `talk/en/tk203_en.bin_@00025ffb`, QA theo sáu lô. Trong đó **196 nguồn trùng** đã có bản Việt ở tk100–202/tk203, **1 nguồn trùng** ngay trong lượt và **66 mảnh nguồn mới** được dịch nháp. `tk203` hoàn tất **663/663 draft, 0 todo**.
- Nội dung: Cu Sidhe, cơ chế chiến đấu và vật phẩm, Oblivion, Cõi âm, chuyện ký ức người chết, người mẹ giả mạo, phòng khám và nhà thờ 17 năm trước. Dùng đại từ trung tính, ghi notes khi mảnh bị cắt hoặc cần soát bối cảnh; chưa tự xác minh người nói.
- QA: chỉ vi/status/notes thay đổi đúng 263 mục; giữ nguyên ID, tiếng Anh, source_sha256, offset, source_review và thứ tự. Đảm bảo NFC, số newline, tiền tố/trailing blank, protected tokens, đồng bộ tuyệt đối source trùng. Không thay font Merienda V3, ROM/ISO/binary và chưa test RPCS3. Dialogue vẫn thiếu parser/repacker.
- Toàn bộ 158 catalog: **6.292/11.886 draft (52,9%)**, còn **5.594 todo** trong dữ liệu trích xuất; đây không phải tỷ lệ bản vá playable.
- **Tiếp theo:** `talk/en/tk204_en.bin_@00001158` (`To Netherworld`); tk204 có 823 mục. Dùng lại nguồn trùng và dịch source mới theo cảnh; luôn lưu/QA theo batch an toàn.
- GitHub Actions validator và unittest Windows/Linux chạy sau khi push.

## Lượt 027a — 11/10/2026 (100 mục đầu tk204)

- Kiểm tra HEAD `f97ce76f11b7` và CI lượt tk203 PASS. Dịch `tk204` **100 todo→draft** từ `talk/en/tk204_en.bin_@00001158` đến `talk/en/tk204_en.bin_@00006642`: 24 nguồn trùng được tái sử dụng, 76 mảnh mới được dịch nháp, có ghi chú những câu chưa rõ người nói.
- Nội dung: Faery, điều ước và thế giới bên kia, ý thức/tâm thức, truyền thuyết ngôi làng, vụ sát hại thứ ba và những cuộc tìm kiếm. Giữ tên riêng, thuật ngữ và sắc thái kỳ bí; không tự gán quan hệ qua các fragment.
- QA: chỉ vi/status/notes đổi đúng 100 mục; ID, English, source hash, offset, source_review, order bất biến; NFC, newline, prefix, placeholders và duplicate source được soát. Chưa có parser/repacker thoại hoặc test RPCS3; không đụng font Merienda V3/ROM/ISO/binary.
- Tổng repo **6.392/11.886 draft**, còn **5.494 todo** (độ phủ bản nháp của dữ liệu trích).
- **Tiếp theo:** `talk/en/tk204_en.bin_@000066b3`; tiếp tục theo cảnh với QA/commit từng phần, CI Windows/Linux validator + unittest chạy sau push.

## Lượt 027b — 11/10/2026 (100 mục tiếp tk204)

- Dịch **100 ứng viên todo→draft** từ `talk/en/tk204_en.bin_@000066b3` đến `talk/en/tk204_en.bin_@0000c3b0`: 4 mảnh tái dùng nguồn trùng, 96 mảnh mới có ghi chú khi chưa rõ chủ thể. `tk204` đạt **200/823 draft**, còn **623 todo**.
- Nội dung: mộ đá Doolin, cái chết và ký ức, nỗi sợ, tự do ý chí và quan hệ giữa con người với Sứ giả. Tránh áp đặt đại từ vào fragment chưa xác minh; ưu tiên giọng nghiêm trang/u tối, thoại ngắn không cộc.
- QA: đúng 100 ID theo checkpoint; chỉ vi/status/notes, giữ ID/source/source_sha256/file_offset/source_review/order, NFC, newline, tiền tố và placeholders, không xung đột bản dịch nguồn trùng. Vẫn draft/candidate chưa có parser/repacker talk/cmc hoặc QA runtime RPCS3. Không thay Merienda V3/ROM/ISO/binary.
- Tổng 158 catalog **6.492/11.886 draft**, còn **5.394 todo** của nguồn đã trích. **Tiếp:** `talk/en/tk204_en.bin_@0000c430`. GitHub Actions Windows/Linux sẽ chạy validator/unittest sau commit.

## Lượt 027c — 11/10/2026 (100 mục tk204, mạch vách đá và ký ức)

- Từ `talk/en/tk204_en.bin_@0000c430` đến `talk/en/tk204_en.bin_@00011c5d`: **100 todo→draft**, gồm 4 nguồn trùng từ trước, 2 lần trùng trong batch và 94 mảnh mới. `tk204` đạt **300/823 draft**, còn 523 todo.
- Chủ đề: cô gái mất tích, vách đá, mộ đá Doolin, bất hòa giữa ký ức/quá khứ và thực tại, tuyệt vọng, nghi vấn án mạng 17 năm trước. Các câu cắt mảnh, đại từ và chỉ dẫn cơ chế chưa rõ được ghi notes thay vì xác nhận sai.
- QA: 100 ID đúng, chỉ sửa vi/status/notes; giữ source/ID/SHA/offset/source_review/order, Unicode NFC, newline, prefix, placeholders và source trùng nhất quán. Chưa có parser/repacker talk/cmc, chưa thử RPCS3; giữ nguyên Merienda V3/ROM/ISO/binary.
- Tổng dự án **6.592/11.886 draft**, còn **5.294 todo**. **Tiếp theo:** `talk/en/tk204_en.bin_@00011de6`. CI Windows/Linux validator/unittest sau push.

## Lượt 027d — 11/10/2026 (100 mục tk204, Sidhe và dân làng)

- Từ `talk/en/tk204_en.bin_@00011de6` đến `talk/en/tk204_en.bin_@00017ea4` xử lý **100 todo→draft**: 23 source trùng đã dịch từ các catalog/batch trước, 9 lần trùng nội bộ và 68 source mới. Tệp `tk204` hiện **400/823 draft**, còn 423 todo.
- Nội dung: truyền thuyết Sidhe/Faery, bài hát dân gian, ký ức 17 năm, người dân Doolin, các đoạn lời nói trong quán rượu. Không suy speaker hay mối quan hệ trong fragment; các đoạn mơ hồ ghi notes.
- QA: chỉ vi/status/notes ở đúng 100 ID thay đổi, source/hash/offset/source_review/order bất biến; Unicode NFC, newline, ký hiệu đầu, placeholder, bản dịch cùng source nhất quán. Vẫn draft/candidate, chưa có parser/repacker hay kiểm thử RPCS3, Merienda V3/ROM/ISO/binary không thay.
- Toàn repo **6.692/11.886 draft**, còn **5.194 todo**. **Tiếp theo:** `talk/en/tk204_en.bin_@0001813a`; validator/unittest chạy sau commit.

## Lượt 027e — 11/10/2026 (hoàn tất 423 mục cuối tk204)

- Từ `talk/en/tk204_en.bin_@0001813a` đến `talk/en/tk204_en.bin_@0002f8f7`, xử lý **423 todo→draft** theo 9 khối QA: **383** nguồn trùng đã có bản Việt ở tk100–203/tk204, **2** mục lặp trong lượt, **38** nguồn mới dịch nháp. **tk204 hoàn tất 823/823 draft, 0 todo**.
- Chủ đề: hướng dẫn/điều kiện nhiệm vụ, khóa I/II, đồng hồ, các cõi, Faery, người chết, nữ tư tế và nguồn hồi ức. Cụm gốc `Achilles' heal` có khả năng sai chính tả (`heel`), tạm dùng `gót chân Achilles` và ghi notes, không tự sửa nguồn.
- QA nội bộ: chỉ `vi/status/notes` của đúng 423 ID thay đổi; giữ nguyên English/source_sha256/file_offset/source_review/order, Unicode NFC, newline, leading prefix và placeholders; mọi nguồn trùng khớp bản Việt cũ. Không suy đoán người nói hay đánh dấu reviewed/tested.
- Tổng 158 catalog **7.115/11.886 draft**, **4.771 todo** (chỉ là ứng viên đã trích; chưa phải phần trăm game đã playable bằng tiếng Việt).
- Chưa có parser/repacker thoại/cmc, chưa test RPCS3; Merienda V3, ISO/ROM/binary không thay đổi. CI Windows/Linux validator+unittest chạy sau push.
- **Tiếp theo:** `talk/en/tk205_en.bin_@00001158` (`To Netherworld`), tk205 có 653 mục; đối chiếu nguồn trùng rồi tiếp tục phần mới theo bối cảnh.

## Lượt 028a — 11/10/2026 (100 mục đầu tk205)

- Đối chiếu HEAD và checkpoint mới nhất: tk203/tk204 đã hoàn tất, CI 2619056d PASS; bắt đầu `tk205`, không lặp việc cũ.
- Dịch 100 mục `todo→draft` từ `talk/en/tk205_en.bin_@00001158` đến `talk/en/tk205_en.bin_@000071eb`: **21** bản nguồn trùng tái sử dụng, **79** mảnh mới dịch nháp. `tk205` đạt **100/653 draft**, còn 553 todo.
- Nội dung: Doolin 17 năm trước, ký ức tuổi thơ, Faery, lời cầu nguyện, người chỉ còn một năm để sống, băng hình, tỉnh dậy và thương tích. `Handy Video` giữ nguyên làm tên tạm vì chưa có hình; các câu cắt mảnh có notes.
- QA đúng 100 ID, chỉ vi/status/notes thay đổi, ID/source/sha256/offset/source_review/order giữ nguyên; NFC, số newline, marker, placeholder và nguồn trùng nhất quán. Chưa có parser/repacker talk/cmc, chưa thử RPCS3; giữ Merienda V3/ROM/binary nguyên.
- Toàn repo **7.215/11.886 draft, 4.671 todo** (độ phủ nháp ứng viên, chưa phải phần trăm patch chơi được).
- **Tiếp theo:** `talk/en/tk205_en.bin_@000072f6` (`Things worked out for the best.`); CI validator/unittest sau commit.

## Lượt 028b — 11/10/2026 (100 ứng viên tiếp tk205)

- Từ `talk/en/tk205_en.bin_@000072f6` đến `talk/en/tk205_en.bin_@0000d759` dịch tiếp **100 todo→draft**: 16 bản đã dịch ở catalog trước, 10 bản lặp trong batch, 74 mảnh nguồn mới. `tk205` đạt **200/653 draft, còn 453 todo**.
- Chủ đề: ngọn hải đăng và mũi đất, gia đình và tuổi thơ, cuộc sống ở Doolin, nỗi sợ và những sinh vật Faery; nhóm câu trùng liên quan hướng dẫn và hồi phục máu. Ghi notes về quan hệ/speaker chưa thể xác minh; giữ khẩu khí tự nhiên mà không thêm tình tiết.
- QA: chỉ vi/status/notes của đúng 100 ID; source/sha256/offset/source_review/order không thay, NFC, newline, prefix, placeholder và nguồn lặp nhất quán. Mọi entry vẫn candidate/draft; chưa có parser/repacker talk/cmc hay QA RPCS3; Merienda V3/ROM/binary không đổi.
- Tổng 158 catalog: **7.315/11.886 draft**, còn **4.571 todo** (độ phủ ứng viên, chưa phải patch playable).
- **Tiếp:** `talk/en/tk205_en.bin_@0000d7d9` (`no matter how hard they're hit...`). CI GitHub Actions validator/unittest sau commit.

## Lượt 028c — 11/10/2026 (hoàn tất 453 mục cuối tk205)

- Từ `talk/en/tk205_en.bin_@0000d7d9` đến `talk/en/tk205_en.bin_@00026cc3` xử lý **453 todo→draft** theo chín nhóm QA: **413** nguồn trùng nguyên bản đã dịch ở các catalog trước và **40** mảnh nguồn mới dịch nháp. **tk205 hoàn tất 653/653 draft**, 0 todo.
- Nội dung bổ sung: hướng dẫn quái Folk/địa điểm, Cõi Địa Ngục, tội lỗi, phán xét, thang máy, y phục, những câu đùa/faery và các hội thoại tái sử dụng từ những vùng trước. Giữ nguồn trùng giống hệt; không tự gán speaker. Những từ `clerical duties` và ngữ cảnh phòng xử án có notes cần xác minh, giữ bản dịch nguồn trùng từ catalog trước thay vì tự chỉnh lệch.
- QA dữ liệu: chỉ `vi/status/notes` sửa ở 453 ID; source/SHA-256/offset/source_review/order bất biến, Unicode NFC, số newline, dấu đầu, placeholder, 0 xung đột giữa nguồn trùng; các mục đều `candidate/draft`, không đánh dấu reviewed/tested.
- Tổng **7.768/11.886 draft, còn 4.118 todo** trên 158 catalog nguồn trích, không phải phần trăm bản vá playable. Chưa parser/repacker talk/cmc, chưa test RPCS3; Merienda V3, ROM/ISO, binary không thay đổi.
- `tk206` và `tk207` đã hoàn tất sẵn; **tiếp theo:** `talk/en/tk306_en.bin_@00001158` của `tk306` (244 todo). CI GitHub Actions sẽ chạy validator/unittest sau khi push.

## Lượt 029 — 11/10/2026 (hoàn tất 244 mục tk306)

- Tiếp đúng checkpoint sau tk205: `tk206` và `tk207` đều đã được dịch nháp trước đó, nên làm `tk306`. Dịch **244 todo→draft**, từ `talk/en/tk306_en.bin_@00001158` đến `talk/en/tk306_en.bin_@0000c45f`: **184** mục nguồn trùng khớp với bản dịch tk204–205/các lượt trước, **60** lượt mảnh mới (có các lần lặp cùng nguồn) được soạn nháp.
- Mạch: Doolin thời quá khứ, người bạn vẽ tranh, ký ức tuổi nhỏ, người thân và nhà thờ, thương tích/vách đá, nỗi sợ và hướng dẫn chiến đấu. Không tự xác định speaker từ offset; những mảnh mơ hồ ghi notes.
- QA theo nhóm: chỉ `vi/status/notes` của 244 ID được sửa; id, source/source_sha256, offset, source_review, thứ tự giữ nguyên; NFC, newline, mã đầu/placeholder, 0 xung đột khi bản nguồn lặp. Tệp `tk306` **244/244 draft**. Chưa parser/repacker talk/cmc, chưa test RPCS3 hoặc sửa font Merienda V3/ROM/ISO/binary.
- Toàn repo **8.012/11.886 draft**, còn **3.874 todo**; chỉ phản ánh độ phủ nháp nguồn trích, không phải tỷ lệ bản vá chơi được.
- **Tiếp theo:** `talk/en/tk307_en.bin_@00001158` (nguồn `To Netherworld`), tk307 có 811 mục; CI GitHub Actions validator/unittest sau commit.

## Lượt 030a — 11/10/2026 (100 mục đầu tk307)

- Tiếp theo HEAD `3f4f5aeaa5b7`, không dịch lại tk204–206/tk306. Từ `talk/en/tk307_en.bin_@00001158` đến `talk/en/tk307_en.bin_@00005ecf`: chuyển **100 todo→draft**, gồm 21 mục trùng nguồn cũ và 79 câu/mảnh mới. `tk307` đạt **100/811 draft**, còn 711 todo.
- Nhóm nội dung: ký ức quá khứ, người mẹ/con, bí mật bác sĩ Doolin, Herve và Faery. `Pre-rendered movie 4` và `Play Movie 23` có thể là nhãn nội bộ, vẫn draft và notes; không xác minh được speaker/quan hệ từ mảnh ASCII.
- QA nội bộ: đúng 100 ID, chỉ vi/status/notes thay đổi; ID, source, SHA-256, file_offset, source_review, thứ tự, NFC, số newline, tiền tố điều khiển và placeholder giữ nguyên. Không sửa Merienda V3/ISO/ROM/binary; chưa parser/repacker và chưa test RPCS3.
- Tổng 158 catalog **8.112/11.886 draft**, còn **3.774 todo** của dữ liệu trích (không phải tỷ lệ bản vá chơi được).
- **Tiếp theo:** `talk/en/tk307_en.bin_@0000605c`; validator + unittest chạy qua GitHub Actions sau push.

## Lượt 030b — 11/10/2026 (tk307 100 mục)

- Đã lưu 100 ứng viên tiếp theo của tk307 (`@0000605c` đến `@0000a821`) thành draft; tổng **8.212/11.886**, còn **3.674 todo**. Kiểm tra bất biến metadata, Unicode NFC, số newline, tiền tố `$`, `*`, khoảng trắng và các bản dịch nguồn trùng ở tệp này.
- Các đoạn vẫn là mảnh NUL chưa ráp lời thoại/speaker; phim/cảnh kỹ thuật để notes trước khi quyết định `skip` hay dịch; xưng hô chưa thể duyệt cho đến khi có dữ liệu cảnh.
- Chưa repack/QA RPCS3, giữ Merienda V3 và toàn bộ game binary nguyên vẹn. Lượt tiếp tại `talk/en/tk307_en.bin_@0000a8a7`; cần CI Windows/Linux xác minh sau commit.

## Lượt 030c — 11/10/2026 (tk307 thêm 100 mục)

- Dịch 100 ứng viên từ `@0000a8a7` đến `@0000fbbc` thành draft, tăng tk307 lên **300/811**. Tổng repo **8.312/11.886 draft**, còn **3.574 todo**.
- Kiểm tra bảo toàn dữ liệu nguồn và metadata, Unicode NFC, newline, leading markers, trùng nguồn. Đây vẫn chỉ là các mảnh ASCII NUL candidate; cần parser/repacker/speaker, font full coverage và thử thực tế trên RPCS3. Không thay payload/ISO/ROM/Merienda V3.
- Tiếp mục 301 của `tk307`; xem `docs/QUEUE.md`. Validator và unittest trên Windows/Linux phải được xác minh qua CI sau push.

## Lượt 030d — 11/10/2026 (hoàn tất tk307)

- Đã chuyển 511 mục còn lại của `tk307` thành draft trong 5 commit, từ `@0000fc5d` đến `@0002bea7`. Tổng **8.823/11.886 draft**, **3.063 todo**; `tk307` **811/811 draft**.
- Phân loại 511 mục: 442 dùng lại nguồn trùng có bản Việt đã xác lập, 7 bản lặp trong batch, 62 nguồn mới. Rà bất biến source/ID/hash/offset/source_review, Unicode NFC, newline, tiền tố và bản dịch giống nguồn; các trường được thay đổi chỉ `vi/status/notes`.
- Chưa kiểm chứng runtime/đóng gói talk/cmc, cần parser, glyph/alias còn thiếu, giới hạn vùng và thử trong RPCS3; Merienda V3, payload và game binary không đổi. Không khẳng định CI PASS khi chưa đọc được kết quả workflow. Tệp tiếp theo `tk500` có 528 todo, bắt đầu `@00001158`.

## Lượt 031 — 11/10/2026 (hoàn tất talk tk500)

- `tk500` tăng **0→528/528 draft** trong 6 commit, từ `@00001158` đến `@0001a237`. Phân loại: 29 nguồn trùng được tái sử dụng, 5 bản lặp trong batch và 494 nguồn mới được dịch. Tổng **9.351/11.886 draft**, còn **2.535 todo**.
- Nội dung người cha/con trai, tạp chí UNKNOWN REALMS, linh hồn, vụ mất tích ở Doolin, chiến binh cổ, Ethersword và giấc mơ truyện cổ Faery đã có bản nháp, nhưng speaker/fragment chưa xác minh; tạm giữ các tên riêng/ký hiệu đặc thù. Có 2 mục cũ được QA lại về từ vựng trong đợt cuối.
- QA đối chiếu bất biến nguồn/ID/hash/offset/source_review/thứ tự, NFC/newline/prefix/placeholder/nguồn trùng trên dữ liệu qua GitHub; không sửa font V3 hoặc binary. **Chưa thực thi/xác minh** validator/unittest đầy đủ hoặc thử trong RPCS3, không coi dữ liệu nháp là patch chơi được.
- Bàn giao `tk600` tại `talk/en/tk600_en.bin_@00001158` (544 todo), kế đó `tk700` (242 todo). Xem `docs/QUEUE.md`.

## Lượt 032 — 11/10/2026 (triage định dạng và bảo đảm an toàn)

- Thêm probe read-only cho BCUS98147, 6 unit test fixture, hướng dẫn làm ở máy local. Kết quả 6/6 test fixture qua trong môi trường thử độc lập, chưa đủ chứng minh parser thật. Không có file binary gốc trên cloud nên chưa phát hiện opcode/pointer/speaker thật.
- Không sửa bất kỳ catalog, ROM/ISO/font/menu payload nào; vẫn 9.351 draft, 2.535 todo. Có khả năng phải biên tập lại một số fragment sau khi có cấu trúc cảnh và xác minh trực tiếp.
- Lượt sau đi theo docs/DIALOGUE_BINARY_PROBE.md, trước hết dùng báo cáo từ 2 talk + 1 CMC để xác lập byte structure, rồi parse→serialize roundtrip byte-for-byte; dừng nếu thiếu chứng cứ.

## Cập nhật công cụ read-only — 11/10/2026 (lượt 033)

Thêm kiểm tra toàn bộ catalog hội thoại với `--all-dialogue --verify-only` vào
`tools/dialogue_probe.py`, không dùng suy đoán pointer cho chế độ xác minh nguồn.
Có thêm test tổng hợp nhưng vẫn **chưa có** chạy đối chiếu binary thật hay
parser/serializer/repacker. Các catalog không đổi: **9.351 draft / 11.886**,
**2.535 todo**; số liệu này không phải % Việt hóa có thể chơi.

## Lượt 034 — 11/10/2026: CMC vỏ section roundtrip

Đã thêm kiểm tra tái tạo từng byte lớp vỏ CMC, kể cả vùng chưa giải mã và trailer.
Đây chỉ là **opaque container roundtrip**, không phải parser lệnh hay repacker
hội thoại. Chưa thử trên binary thật tại E:\\Game\\Folklore và không có patch
mới. Số mục dịch nháp giữ 9.351/11.886, còn 2.535 todo.

## Lượt 035 — 11/10/2026: tiếp tục tk600 ở mức bản nháp

`tk600` đạt **110/544 draft**, **434 todo** sau lượt dịch 110 mục; gồm 23
bản dịch nguồn trùng được tái sử dụng và 87 bản nháp mới. Rà prefix/Newline,
NFC và metadata bất biến. Các mảnh ASCII-NUL chưa có speaker/scene xác minh,
không đánh dấu reviewed/tested. Tổng catalog hiện **9.461/11.886 draft**,
**2.425 todo**. Chưa có patch hội thoại playable, font Merienda V3/binary
gốc không đổi. Parser/repacker vẫn là ưu tiên chính sau khi có báo cáo local.

## Lượt 036 — 11/10/2026: handoff thống kê cấu trúc

Thêm `tools/dialogue_summary.py` để người dùng tự xuất JSON metadata không
chứa nguyên văn câu thoại, các cửa sổ byte, hay dữ liệu binary game. Công cụ
chỉ giữ offset/ranh giới và mẫu u32, chưa xác nhận là pointer. Kiểm thử chỉ
bằng synthetic fixtures; **chưa chạy local trên game gốc**, chưa có message
parser hoặc repacker. Tổng bản nháp 9.461/11.886, còn 2.425 todo.

## Lượt 037 — 11/10/2026: 220 bản nháp tiếp theo trong tk600

Chuyển thêm 220 mục `tk600` từ todo→draft theo hai commit 100+120:
`@0000699d` → `@0001297d`. **tk600 330/544 draft, 214 todo**; tổng
catalog **9.681/11.886 draft, 2.205 todo**. Không gán speaker hay dựng
thứ tự câu từ offset quét; chỉ QA bản dịch nháp/ngắt dòng/prefix/NFC và
bảo toàn id/source/hash/offset/source_review. Font Merienda V3, dữ liệu
game, ISO và patch local không thay đổi. Chưa thể xác nhận lời thoại hiển thị
trong RPCS3 hay parser/repacker; lần tới tiếp `tk600@00012a71`.

## Lượt 038 — 11/10/2026: hoàn tất tk600 ở mức draft

Đã chuyển nốt **214 ứng viên** từ todo sang draft; `tk600` hiện
**544/544 draft**. QA sửa một lỗi `((` thành `(` trong bản dịch trùng
của `tk500@00011bb7`. Giữ nguyên source, ID, offset, SHA, `source_review`,
ngắt dòng và ký hiệu điều khiển; không xác minh hay đoán speaker từ thứ tự
ASCII. Tổng **9.895/11.886 draft**, còn **1.991 todo**. Chưa có patch
hội thoại playable; Merienda V3 và game binary không đổi. Bước dịch tiếp
`tk700@00001158`, song song ưu tiên phân tích binary thực tại local.

## Lượt 039 — 11/10/2026: hoàn tất tk700 ở mức dịch nháp

Đã dịch hết **242/242** ứng viên của `talk/en/tk700_en.bin_` trong hai batch,
đưa tổng dữ liệu trích lên **10.137/11.886 draft; 1.749 todo**. Giữ nguyên
metadata, source, ID, offset, tiền tố, số xuống dòng và font Merienda V3.
Câu nói lắp/fragment hoặc tên Folk vẫn cần QA theo bối cảnh; **không nâng
trạng thái reviewed/tested** và không tuyên bố đã vá vào game. File CMC đầu
tiên còn trống được kiểm tra là `cmc/en/LCmc005_en.bi5_` (16 mục).
Chưa có kiểm thử binary thật, command parser hay bản vá hội thoại playable.

## Lượt 040 — 11/10/2026: CMC đoạn đầu, 253 bản dịch nháp

Hoàn thành **253/253** mục trên 16 catalog CMC từ `LCmc005` đến
`LCmc029` (không liên tục; chỉ các file theo queue). QA bất biến các trường
nguồn/ID/SHA/offset/source_review; giữ nguyên cấu trúc xuống dòng và ký hiệu
đầu chuỗi có thể là mã nhị phân, Unicode NFC. Không đoán speaker từ catalog.
Tổng dự án **10.390/11.886 draft**, còn **1.496 todo**; số lượng không phản
ánh mức hoàn thành patch có thể chơi. Merienda V3 và tệp game không đổi.
Chưa có mẫu binary gốc để chứng minh parser command, con trỏ, repacker hoặc
chạy trong RPCS3. CMC tiếp theo: `LCmc030_en.bi5_@00002a98`.
