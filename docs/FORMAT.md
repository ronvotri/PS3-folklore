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

## Font — cần nghiên cứu tiếp

`lang_tex_a.bi5_` và `lang_tex_e.bi5_` đều 1.311.584 byte trong bản khảo sát.
Các tên phần có `font`, `font_e`, `font_tr`, `font300`, `font301`.
Đọc được metadata: `ITC Tempus Sans Com`, font height 36, image 1024×1024.
Có header giống DDS nhưng đảo byte theo từ 32-bit (` SDD`, `1TXD`), không
được coi ngay là DDS chuẩn để ghi đè. Chưa xác định đủ glyph table,
tọa độ texture, bảng mã hoặc quy tắc render.

## Các nguồn chữ khác

- `talk/en/tk*_en.bin_`: hội thoại, đọc được chữ ASCII.
- `cmc/en/LCmc*_en.bi5_`: có lời thoại cảnh truyện.
- `rtd/en/RTDscene*_en.bi5_`: dữ liệu cảnh, cần nghiên cứu định dạng.
- `bin/movie/movie_001_en.dat2_` và các tệp tương tự: phụ đề tiếng Anh,
  có bảng vị trí đầu tệp và tag thời gian như `<552,-1,70.5,73.5>`.
- `menu_tex/` và một số DDS: có thể chứa chữ vẽ sẵn trong hình.

Ngoài bản đĩa, thư mục giả lập `dev_hdd0/game/BCUS98147` có dữ liệu
update/DLC. Bản menu thử chỉ sửa kho etc của bản đĩa, chưa sửa DLC.
