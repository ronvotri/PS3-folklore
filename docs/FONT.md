# Merienda Regular 400 — bản V3

Người dùng chọn Merienda vì nét viết tay phù hợp game. Nguồn/hash/OFL pinned
trong fonts/choice.json. TTF đủ 134 chữ Việt có dấu + 8 dấu kết hợp; atlas game
thử mới có 251 glyph, không được coi đủ toàn bộ chữ Việt.

## Kết quả thử

Ảnh V1/V2 có “Nhấ n”, “mớ i”. V2 giảm bearing/space vẫn còn hở sau ký tự
3 byte như ấ/ớ. V3 không đổi hình chữ/width V2, dùng 25 ô Unicode trống
U+0500 trở đi, mỗi ô encoded UTF-8 2 byte, trỏ vào hình chữ Việt tương ứng.
Người dùng báo V3 đã ổn. Điều này ủng hộ lỗi đọc/advance ký tự 3 byte trong
đường render đang thử; chưa reverse-engineer executable để khẳng định lỗi nội bộ.

fonts/aliases.json lưu chính xác mapping đã thử. KHÔNG đổi các ô đã dùng.
Nguồn bản dịch luôn NFC thông thường; alias chỉ dùng lúc encode payload game.
text_codec.py encode/decode và thêm mapping vào bảng font. Thiếu alias/glyph
phải dừng build hoặc mở rộng có kiểm tra, không bỏ dấu để che lỗi.

## Dựng lại font V3 tại local

Cần original lang_tex_a/e.bi5_ có hash trong docs/font_baseline.json.
Không dùng tệp đang vá làm original. Trích/bảo quản nguồn ở local-data/.

python -m pip install -r requirements-font.txt
python tools/font_probe.py --download
python tools/font_atlas.py --original local-data/lang_tex_a.bi5_ --out dist/font/lang_tex_a.bi5_

Chạy tương tự cho lang_tex_e. Builder instantiate Merienda pinned ở weight
400, raster 27 px, common extent 42px cho bộ mẫu, co dọc còn 34px trong ô 36px;
thu gọn bearing, khoảng trắng 5. Giữ texture icon thứ hai nguyên trạng.
Với menu_vi.json hiện tại và Pillow 12.3.0, output A khớp đúng hash V3 đã thử.
Builder không tự cài game. Câu mới có thể đổi extent/layout: phải kiểm tra hình
và thử local, không coi font output mới đạt vì cùng tên Merienda.

## Giới hạn

Không có kerning theo cặp trong bảng glyph đang đọc. Unicode NFD chưa chứng
minh được engine ghép dấu. Các tag/ký tự 3 byte khác cần khảo sát riêng.
Muốn dịch toàn game cần mở rộng glyph/alias, kiểm tra dấu hoa/độ đọc ở chữ nhỏ.
Không tự chuyển Noto Serif. OFL ở fonts/Merienda-OFL.txt; tệp TTF và texture game
không có trong repo. Xét giấy phép gói phát hành khi đến bước phân phối.
