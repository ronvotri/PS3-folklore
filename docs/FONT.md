# Font đã chọn: Merienda Regular, weight 400

Quyết định ngày 10/10/2026: ưu tiên Merienda Regular 400 làm nguồn tạo glyph
cho bản Việt hóa. Font có nét viết tay phù hợp với hướng truyện cổ của game.
Noto Serif Regular 400 là phương án dự phòng nếu chữ nhỏ khó đọc khi thử game.
Không trộn hai font trong bản thử đầu để giảm số biến cần kiểm tra.

## Đã kiểm tra

- Đối chiếu cmap của tệp font thực: đủ 134 chữ Việt có dấu dạng dựng sẵn
  (67 thường + 67 hoa) và 8 dấu kết hợp; không thiếu glyph trong bộ này.
- Đã dựng mẫu chữ ở 22, 28 và 36 px, xem menu, hội thoại và các dấu khó.
- Merienda và Noto Serif đều qua kiểm tra bộ chữ Việt. Lựa chọn Merienda
  dựa trên hình thức của mẫu, không phải Noto Serif thiếu tiếng Việt.
- Nguồn Google Fonts ghi Vietnamese subset và giấy phép OFL. Tệp tải được
  khóa bằng commit upstream và SHA-256 trong `fonts/choice.json`.

## Kiểm tra lại trong phiên khác

Kiểm tra font cần thêm thư viện fonttools; các công cụ menu vẫn chỉ dùng
Python standard library. Có thể dùng Python 3.10+ trên Windows hoặc Linux:

```sh
python -m pip install fonttools
python tools/font_probe.py --download --report local-data/fonts/coverage.json
```

Font tải về là font nguồn mở của tác giả, không phải font trích từ game.
Lệnh trên lưu tệp cục bộ, không cài font vào hệ điều hành và không sửa game.
Mang theo OFL và thông tin tác giả khi phân phối font. Giấy phép có Reserved
Font Name "Merienda"; nếu phân phối font đã sửa, phải tuân thủ điều kiện đổi
tên. Raster hóa để tạo texture và phân phối texture vẫn cần xét điều kiện
giấy phép cho gói phát hành cụ thể.

## Phần chưa hoàn thành

Chọn được font TTF có đủ ký tự chưa đồng nghĩa font đã chạy trong PS3.
Game dùng font texture/glyph table riêng. Công việc tiếp theo:

1. Đọc texture và glyph metrics trong `lang_tex_a/e.bi5_`.
2. Xác định byte/codepoint mà game dùng để chọn glyph. Không tự đổi encoder
   sang UTF-8: cần kiểm chứng đường đọc ký tự của game.
3. Tạo atlas mẫu từ Merienda 400, căn dấu phía trên và dấu nặng phía dưới;
   cỡ raster cụ thể sẽ dựa vào metrics của game, chưa chốt 36 px.
4. Thử chữ “Chơi mới”, “Cài đặt”, “Tiếp tục”, “Đồng ý”, “Trở về” trong game.
5. Kiểm tra clipping, khoảng cách chữ, xuống dòng và đọc ở màn hình nhỏ.

Chuỗi dịch lưu Unicode NFC. Dấu kết hợp được kiểm tra trong font để hiểu
coverage; chưa chứng minh engine PS3 có thể ghép dấu NFD khi render.

Nguồn: [Google Fonts Merienda](https://github.com/google/fonts/tree/main/ofl/merienda),
[giấy phép OFL](https://github.com/google/fonts/blob/main/ofl/merienda/OFL.txt).
