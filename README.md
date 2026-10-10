# Folklore — Việt hóa PS3

Dự án Việt hóa Folklore, bản **BCUS98147**, phát triển và kiểm thử ban đầu
trên RPCS3. Bản menu thử không dấu đã được người dùng xác nhận hoạt động.

Repo lưu công cụ, bản dịch và tiến độ để tiếp tục qua nhiều phiên local/cloud.
Game gốc, font, firmware và các gói vá chứa dữ liệu game được giữ cục bộ.

## Hiện trạng

- 118 cặp câu nguồn/bản dịch trong `translations/menu_ascii.json`.
- Bản đã thử thay 134 chuỗi trong `lang_en.bi5_` và 132 trong `lang_uk.bi5_`.
  Một câu có thể xuất hiện nhiều lần, nên số chuỗi thay lớn hơn số cặp dịch.
- Công cụ di chuyển và kiểm tra 2.998 tham chiếu chuỗi menu ở mỗi tệp.
- Chưa hỗ trợ tiếng Việt có dấu; hội thoại và nhiều phần khác chưa dịch.
- Chưa thử trên PS3 thật hoặc Steam Deck.

Xem [tiến độ và bàn giao](docs/STATUS.md), [cấu trúc dữ liệu](docs/FORMAT.md),
và [cách tiếp tục trên cloud](docs/CLOUD.md).

## Sử dụng tại máy có game

Cần Python 3.10 trở lên; không cần cài thêm thư viện. Đóng RPCS3 trước khi
áp dụng hoặc khôi phục bản vá. `--bin-dir` trỏ thẳng đến thư mục có `etc.bin_`
và `etc.fht_`, không trỏ đến thư mục giả lập.

Ví dụ PowerShell trên máy đang phát triển:

```powershell
$binDir = 'E:\Game\Folklore\games\BCUS98147\PS3_GAME\USRDIR\bin'
python tools/folklore.py inspect --bin-dir $binDir
python tools/folklore.py extract-menu --bin-dir $binDir
python tools/folklore.py build-menu
python tools/folklore.py apply-menu --bin-dir $binDir --package dist/menu/menu-patch.json --check
python tools/folklore.py apply-menu --bin-dir $binDir --package dist/menu/menu-patch.json
```

**Game hiện tại đã được vá.** Để trích bản gốc mà không đổi game đang chơi,
thay lệnh `extract-menu` bằng lệnh có gói khôi phục cũ đang lưu trên máy:

```powershell
python tools/folklore.py extract-menu --bin-dir $binDir --original-package 'C:\Users\win\Documents\Codex\2026-10-10\e-game-folklore\outputs\Folklore-menu-thu\menu-patch.json'
```

Khôi phục menu gốc bằng gói đã tạo:

```powershell
python tools/folklore.py apply-menu --bin-dir $binDir --package dist/menu/menu-patch.json --restore
```

Trên Linux/Steam Deck, dùng cùng công cụ với `python3` và đường dẫn `--bin-dir`
tương ứng. Các tệp game được vá vẫn là dữ liệu PS3; không cần trình khởi chạy
Windows. Khả năng chạy mượt và điều khiển cần kiểm tra trên thiết bị thực tế.

## Kiểm thử không cần game

```sh
python -m unittest discover -s tests -v
```

Các bài kiểm thử dùng dữ liệu tự tạo để kiểm tra di chuyển chuỗi, tham chiếu
trùng, giới hạn vùng dữ liệu, kiểm tra trước khi ghi và khôi phục nguyên trạng.
GitHub Actions chạy cùng bộ kiểm thử trên Windows và Linux.

## Định hướng bản vá

Gói thử hiện dùng dữ liệu hai tệp menu để áp dụng/khôi phục tại máy có game.
Gói này không được đưa vào repo. Bản phát hành cuối dự kiến là bản vá chênh
lệch kèm kiểm tra phiên bản/hash; chưa có bản phát hành xdelta hoặc công cụ ISO.
