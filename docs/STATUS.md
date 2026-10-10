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
viên hội thoại/tương tác/cảnh. Có 1.016 mục menu `draft`, 0 menu `todo`; 46 mục CMC `draft`; talk tk000, tk011, tk100–tk107, tk206, tk207 có tổng 3.273/3.273 `draft`. Toàn bộ **4.435 draft / 11.886** catalog entries, còn **7.451 todo** (10.870 mục dialogue/candidate tổng).
Đã có 46 câu CMC và 3.373 ứng viên talk có bản nháp (tk000 19, tk011 19, tk100 314, tk101 447, tk102 494, tk103 578, tk104 731, tk105 595, tk106 19, tk107 19, tk206 19, tk207 19, tk200 100). Speaker/metadata/parser/repacker chưa xác minh; tất cả vẫn chỉ draft.
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
