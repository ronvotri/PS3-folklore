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
viên hội thoại/tương tác/cảnh. Có 284 mục menu `draft` (134 mục mẫu + 150 mục từ 3 lượt ngày 10/10/2026); còn 11.602 `todo` toàn bộ catalog (trong đó 732 menu).
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
