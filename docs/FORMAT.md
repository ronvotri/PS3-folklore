# Cấu trúc dữ liệu quan sát được

Các mô tả dưới đây đến từ bản BCUS98147 tại máy người dùng; không suy rộng
sang mọi phiên bản Folklore hoặc mọi tệp có đuôi BI5.

## Kho etc

`etc.bin_` có 2.498.514.097 byte. `etc.fht_` có 193.240 byte = 4.831 mục.
Mỗi mục gồm tên ASCII kết thúc bằng NUL trong 32 byte, rồi hai số unsigned
32-bit big-endian: kích thước tệp và vị trí tuyệt đối trong `etc.bin_`.
Tất cả mục đã kiểm tra nằm trong kho dữ liệu. Chi tiết hai menu ở baseline.json.

## Menu lang_en/uk

Header có kích thước tệp ở 0x00, số phần = 13 ở 0x04. Bảng ranh giới phần
bắt đầu ở 0x30; tên các phần bắt đầu ở 0x68. Phần đầu tên `system` bắt đầu
ở 0x1A0. Ranh giới tiếp theo ở 0x34 xác định điểm cuối vùng menu.

Đầu phần `system` là bảng con trỏ 32-bit big-endian, tương đối với đầu phần.
Giá trị con trỏ đầu tiên = 0x2ED8 = 11.992 byte, cũng là kích thước bảng;
đếm được 2.998 tham chiếu. Chuỗi kết thúc NUL. Các dấu điều khiển/ngắt dòng
và các byte ở phần khác cần được giữ nguyên.

Công cụ thử xây lại string pool, cập nhật từng con trỏ, giữ các byte từ NUL
đến con trỏ kế tiếp, và đệm vùng còn lại bằng NUL. Nếu pool tăng vượt vùng
ban đầu thì dừng. Chưa hỗ trợ tăng kho dữ liệu hoặc sửa toàn bộ các phần BI5.

## Font — cấu trúc đã kiểm tra

lang_tex_a/e.bi5_ đều 1.311.584 byte, section count 15. Lookup Unicode BMP
ở 0x1E0..0x801E0: 65.536 bản ghi 8 byte, >4H (x, y, width, font index).
Missing glyph = (0, 0xFC00, 0, 0). Ô glyph cao 36, atlas 1024×1024.
Width vừa xác định vùng crop vừa là phần tiến ngang quan sát từ bản thử.

Metadata ở 0x801E0..0x80260. DDS chính 0x80260..0x1002E0: 128 byte header
đảo từng word 32-bit, payload DXT1 little-endian chuẩn, linear block order.
Chỉ đảo HEADER để Pillow đọc, không đảo payload hoặc Morton unswizzle.
DDS thứ hai ở 0x1002E0..0x140360, 1024×512, giữ nguyên icon/kana.

Menu tiếng Pháp có UTF-8 Latin. Tiếng Việt 3 byte hiển thị glyph nhưng V1/V2
có hở sau ấ/ớ. V3 dùng alias 2 byte, được người dùng xác nhận ổn. Mapping
fonts/aliases.json; xem FONT.md. Từ bằng chứng này không suy engine hỗ trợ
mọi Unicode/NFD hay mọi đường render của game.

## Các nguồn chữ khác

- `talk/en/tk*_en.bin_`: hội thoại, đọc được chữ ASCII.
- `cmc/en/LCmc*_en.bi5_`: có lời thoại cảnh truyện.
- `rtd/en/RTDscene*_en.bi5_`: dữ liệu cảnh, cần nghiên cứu định dạng.
- `bin/movie/movie_001_en.dat2_` và các tệp tương tự: phụ đề tiếng Anh,
  có bảng vị trí đầu tệp và tag thời gian như `<552,-1,70.5,73.5>`.
- `menu_tex/` và một số DDS: có thể chứa chữ vẽ sẵn trong hình.

Ngoài bản đĩa, thư mục giả lập `dev_hdd0/game/BCUS98147` có dữ liệu
update/DLC. Bản menu thử chỉ sửa kho etc của bản đĩa, chưa sửa DLC.
