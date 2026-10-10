# Tiếp tục trên cloud hoặc phiên mới

Repo là nguồn lưu công cụ, bản dịch và tiến độ. Máy cloud không tự truy cập
ổ E: của máy Windows, và repo không chứa ROM/font. Mở repo này trong môi
trường cloud hỗ trợ GitHub, đọc AGENTS.md và chạy bộ kiểm thử Python.

## Việc làm được ngay không cần ROM

- Kiểm tra, cải thiện công cụ và các bài kiểm thử với dữ liệu tự tạo.
- Rà soát bản dịch menu không dấu, thống nhất thuật ngữ.
- Chuẩn bị bản dịch có dấu thành tệp riêng; chưa dùng để build ASCII.
- Chuẩn bị cấu trúc bản dịch theo chương, tài liệu định dạng và checklist QA.

Nghiên cứu định dạng thực tế hoặc build patch cần những dữ liệu gốc liên quan
được cung cấp trong môi trường riêng. Các tệp nguyên bản đang có ở máy local;
không được giả định cloud đã có chúng. Không dùng gói vá đã chỉnh sửa làm nguồn.

## Prompt bàn giao gợi ý

> Tiếp tục dự án Việt hóa Folklore BCUS98147. Đọc AGENTS.md,
> docs/STATUS.md và docs/FORMAT.md trước. Menu không dấu đã được người dùng
> xác nhận hoạt động trên RPCS3. Mục tiêu tiếp theo là hỗ trợ dấu tiếng Việt;
> trước tiên xác định dữ liệu font cần có và thiết kế thử nghiệm nhỏ.
> Chạy các kiểm thử hiện có, cập nhật STATUS.md với kết quả và phần cần
> kiểm tra tại máy local. Không tuyên bố chữ có dấu chạy được khi chưa thử game.

## Quy trình phối hợp

1. Cloud tạo thay đổi công cụ/bản dịch trên nhánh và pull request.
2. Máy local lấy thay đổi, build gói từ dữ liệu gốc đã kiểm tra hash.
3. Áp dụng bản mẫu, mở game, kiểm tra bố cục/font và chụp ảnh khi cần.
4. Ghi kết quả vào STATUS.md để phiên khác tiếp tục đúng trạng thái.

Repo không thay thế hạn mức sử dụng của tài khoản; mục đích là giữ tiến độ
và khiến công việc có thể tiếp tục qua nhiều phiên.
