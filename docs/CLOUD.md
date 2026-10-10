# Tiếp tục dịch trên cloud

Chọn repo ronvotri/PS3-folklore trong môi trường Codex Cloud có quyền GitHub.
Tạo/chọn môi trường một lần; plain translation chỉ cần Python 3.10+, không cần
ROM, RPCS3, API key hay thư viện font. Setup kiểm tra có ở scripts/cloud-check.sh.
Repo đã có nguồn câu để dịch; đừng yêu cầu người dùng tải ROM chỉ để bắt đầu.

## Tin nhắn bắt đầu

Tiếp tục Việt hóa Folklore BCUS98147. Đọc AGENTS.md, STATUS.md, TRANSLATION.md
và QUEUE.md. Font Merienda V3 đã được người dùng xác nhận sửa khoảng hở.
Hãy theo docs/QUEUE.md, dịch lượng ứng viên hội thoại lớn nhất có thể kiểm tra
tử tế trong một lượt, không có giới hạn cứng 200 mục; ưu tiên hoàn tất từng
catalog và đồng bộ nguồn trùng, chia nhóm QA khi cần. Không chạy theo số lượng
nếu câu thiếu ngữ cảnh hoặc có rủi ro sai speaker.
Menu đã có đủ bản nháp. Giữ nguyên nguồn/ID/control codes và thuật ngữ đã chốt,
không tự suy speaker hoặc quan hệ xưng hô khi câu chỉ là fragment. Chạy validator và unittest, cập nhật tiến độ,
rồi lưu thay đổi vào GitHub qua commit hoặc PR để tôi tiếp tục phiên sau.

Sau đó có thể nói “dịch tiếp menu”, “dịch nhóm cảnh tìm mẹ”, “rà lại xưng hô”.
Agent đọc queue/catalog để tiếp tục, không phụ thuộc lịch sử chat này.

## Cloud và local

Cloud dịch/rà văn bản, kiểm tra dữ liệu, lưu bản dịch/tiến độ vào GitHub.
Local lấy phiên bản đã lưu, bổ sung glyph nếu cần, build có kiểm tra nguồn/hash,
đóng RPCS3 trước khi cài. Người dùng tự mở game và gửi ảnh. Ghi phản hồi vào
STATUS/QUEUE để phiên khác hiểu trạng thái.

Hội thoại đã có nguồn để dịch nhưng chưa có parser/repacker hoàn chỉnh;
không hứa dịch trên cloud xong là tự áp dụng được vào game. Mã font mới chỉ
được thử trên menu mẫu. Việc mở rộng vùng menu và glyph vẫn cần local QA.

## Công cụ

python tools/catalog.py validate
python -m unittest discover -s tests -v

Font work optional: pip install -r requirements-font.txt, rồi xem FONT.md.
Không chạy encoder ASCII cũ cho bản dịch có dấu. Không commit ROM/font texture/
payload patch. translations/index.json là danh mục, catalog là tiến độ từng câu.

Hướng dẫn sản phẩm chính thức (đã kiểm tra ngày 10/10/2026):
https://learn.chatgpt.com/docs/cloud
Chọn Work in > Cloud, tạo/chọn môi trường và repo, rà setup rồi Publish nếu
là môi trường mới. Sau đó mở task để dịch. Repo chuẩn bị được ở đây; môi trường
cloud của tài khoản chưa được agent tạo hoặc kiểm thử trong phiên local này.
