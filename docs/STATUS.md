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
viên hội thoại/tương tác/cảnh. Có 1.016 mục menu `draft`, 0 menu `todo`; 46 mục CMC `draft`, 314/314 mục tk100 `draft`, 447/447 mục tk101 `draft`, 494/494 mục tk102 `draft`, 578/578 mục tk103 `draft` và 89/731 mục tk104 `draft`. Còn 8.902 mục `todo` toàn bộ 158 catalog (10.870 mục dialogue/candidate tổng).
Đã có 46 câu CMC và 1.922 ứng viên talk có bản nháp (314 tk100, 447 tk101, 494 tk102, 578 tk103, 89 tk104). Speaker/metadata/parser/repacker chưa xác minh; tất cả vẫn chỉ draft.
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
