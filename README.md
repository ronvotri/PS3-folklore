# Folklore — Việt hóa PS3 BCUS98147

**Đang Việt hóa theo từng đợt lớn.** Repo có 158 catalog / 11.886 mục nguồn,
thuật ngữ và checkpoint. Menu đã có 1.016/1.016 bản dịch nháp; các tệp talk/cmc
chứa ứng viên từ quét dữ liệu chưa có parser hoàn chỉnh. Mỗi đợt ưu tiên khoảng
nhiều mục nhất có thể kiểm tra chất lượng trong một lượt; không giới hạn cứng 200 mục; xem docs/QUEUE.md.

Font **Merienda Regular 400 V3** được người dùng xác nhận sửa khoảng hở sau
chữ có dấu. Đây là bản menu mẫu đã thử trong RPCS3; chưa xác minh toàn game,
PS3 thật hoặc Steam Deck.

## Bắt đầu

Đọc AGENTS.md, docs/STATUS.md, docs/QUEUE.md và docs/TRANSLATION.md.
Dịch trong translations/catalogs/; giữ nguyên nguồn/ID/metadata, điền vi và
trạng thái. Có 1.016 mục menu, 10.870 ứng viên từ talk/cmc; không chứng minh
đã trích đủ mọi câu. Menu đã có 1.016 mục draft; hội thoại đang được dịch nháp theo QUEUE.md.

python tools/catalog.py validate
python -m unittest discover -s tests -v

Dịch/kiểm tra chỉ cần Python 3.10+, không cần ROM hay API key. Font optional
cần requirements-font.txt. GitHub Actions kiểm tra Windows/Linux.

## Tài liệu

- docs/CLOUD.md: cách bắt đầu, prompt và phối hợp cloud/local.
- docs/QUEUE.md: lượt dịch kế tiếp và bàn giao.
- docs/TRANSLATION.md + translations/glossary.json: giọng văn/thuật ngữ.
- docs/STATUS.md: kết quả đã xác nhận và phần chưa làm.
- docs/FORMAT.md + docs/FONT.md: cấu trúc game, font, alias V3.

## Phạm vi công cụ

catalog.py trích văn bản local và kiểm tra catalog trên cloud. Scanner hội thoại
chưa phải parser/repacker; offset catalog chỉ định nguồn, không cho phép ghi
đè bằng câu dịch dài hơn. Cloud có thể dịch ngay, việc đóng gói hội thoại còn
phải phát triển và kiểm thử. font_atlas.py dựng lại font V3; text_codec.py giữ
mapping chữ Việt → alias đã thử. folklore.py là bản ASCII legacy, không dùng
cài đè trực tiếp V3. Xem FORMAT.md trước mọi thay đổi nhị phân.

ROM/ISO, emulator, firmware, saves, font textures, TTF và payload patch chỉ giữ
local trong local-data/ hoặc dist/. Repo chứa catalog văn bản được người dùng
cho phép chuẩn bị để dịch. Không có quyền tự truy cập E: từ cloud. Người dùng
tự mở/test game và báo ảnh. Chưa tạo/kiểm thử môi trường cloud tài khoản từ đây.
