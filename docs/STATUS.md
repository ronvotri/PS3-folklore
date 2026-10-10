# Tiến độ — 10/10/2026

## Đã xác nhận

- Game trong `E:\Game\Folklore` là dữ liệu PS3 BCUS98147 đóng cùng RPCS3.
- Đọc được bảng kê `etc.fht_`: 4.831 mục, mỗi mục 40 byte.
- Đọc được menu tiếng Anh trong `lang_en.bi5_` và `lang_uk.bi5_`.
- Đã áp dụng bản menu không dấu: 134 chuỗi EN, 132 chuỗi UK.
- Người dùng xác nhận game nhận bản dịch. Đây là xác nhận menu mẫu, không
  phải kiểm thử toàn bộ game hoặc mọi màn hình menu.
- Gói local cũ lưu nguyên dữ liệu gốc để khôi phục, ở đường dẫn ghi trong README.

## Bằng chứng kỹ thuật

`baseline.json` lưu kích thước, vị trí và SHA-256 hai menu gốc/bản đã thử,
không chứa dữ liệu nhị phân. Bản thử chỉ tái tạo vùng `system`, điều chỉnh
con trỏ tương đối và giữ nguyên kích thước mỗi tệp/kho dữ liệu. Mỗi tệp có
2.998 tham chiếu chuỗi được kiểm tra sau khi tái tạo.

## Kiểm tra bộ công cụ trong repo

- 6 bài kiểm thử tổng hợp đã qua trên Python 3.12/Windows tại máy phát triển.
- Đã trích bản gốc trong bộ nhớ từ gói local cũ, không khôi phục game đang chơi.
- Build từ công cụ portable và 118 cặp dịch tạo đúng SHA-256 của hai tệp
  đã áp dụng ở bản thử trước: 134 chuỗi EN, 132 chuỗi UK.
- Lệnh chỉ kiểm tra xác nhận game hiện tại khớp gói portable, không ghi game.
- GitHub Actions được cấu hình chạy kiểm thử trên Windows và Linux; kết quả
  CI cần xem trên repo, không suy ra từ lần chạy Windows local.

## Việc tiếp theo

1. Đã chọn **Merienda Regular 400** làm font nguồn; xem FONT.md và
   fonts/choice.json. Đã kiểm tra đủ 134 chữ Việt có dấu và 8 dấu kết hợp.
   Tiếp theo đọc `lang_tex_a.bi5_` và `lang_tex_e.bi5_`, xác định mapping
   ký tự/glyph và thử font texture có dấu trên menu nhỏ. Chưa thay font game.
2. Giải quyết tăng kích thước vùng/tệp nếu bản dịch dài vượt chỗ trống.
3. Trích hội thoại theo ID/ngữ cảnh, dịch từng chương và giữ control codes.
4. Thử trên Steam Deck, kiểm tra điều khiển và dữ liệu DLC/update.
5. Đóng gói bản vá riêng, kiểm tra nguồn gốc bằng hash và thêm hướng dẫn.
6. Kiểm thử PS3 thật nếu muốn công bố hỗ trợ phần cứng gốc.

## Giới hạn đã biết

- Encoder hiện chỉ chấp nhận ASCII. Chưa được đổi sang UTF-8 tùy ý.
- Menu là phần đầu của `lang_*.bi5_`; các phần overview/item/tutorial chưa dịch.
- Chữ có thể nằm trong hình ảnh ở `menu_tex/`; công cụ hiện không sửa ảnh.
- Các tệp `talk/en/*.bin_`, `cmc/en/*.bi5_` và phụ đề `movie_*_en.dat2_`
  có chữ tiếng Anh đọc được, nhưng chưa có công cụ đóng gói hoàn chỉnh.
- PS3 thật, ISO và hiệu năng Steam Deck chưa được kiểm thử.
- Cloud có thể chạy kiểm thử tổng hợp mà không có ROM; kiểm thử hình ảnh/game
  tiếp tục tại máy có game. Chưa thiết lập môi trường cloud từ repo này.
