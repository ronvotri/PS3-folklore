# Tiến độ — 10/10/2026

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
viên hội thoại/tương tác/cảnh. Có 784 mục menu `draft` (134 mục mẫu + 650 mục từ 10 lượt ngày 10/10/2026); còn 11.102 `todo` toàn bộ catalog (trong đó 232 menu).
Chưa bắt đầu dịch hội thoại. Lượt menu 001 đã thêm 50 bản dịch dạng `draft` từ `@0000311b` đến `@00004124`; xem QUEUE.md và TRANSLATION.md.
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
