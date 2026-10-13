# CODEX — START HERE: HOÀN THIỆN FOLKLORE VIỆT HÓA FULL

**Mục tiêu người dùng:** Bản vá *có tiếng Việt có dấu* chơi được cho Folklore PS3 **BCUS98147**, tiến tới **FULL**, bộ cài dễ dùng, backup/restore, không bắt người dùng lặp lại V1–V7.

**Đọc trước:** [docs/CODEX_FULL_HANDOFF_2026-10-14.md](docs/CODEX_FULL_HANDOFF_2026-10-14.md) — bản bàn giao chi tiết, hiện là **đầu mối kỹ thuật ưu tiên**.

**Báo cáo ngoại lệ thật (đã lọc):** [docs/CMC_V7_EXCEPTION_IDS_REDACTED.json](docs/CMC_V7_EXCEPTION_IDS_REDACTED.json). Có **51 ID** CMC không khớp trong 1.795 ứng viên; V7 đã xác thực source và ghép khung+opaque **134** CMC byte-exact. Điều đó **không chứng minh message repacker**.

**Các mốc:** 11.886 bản dịch **draft**, gồm 1.016 menu + 10.870 hội thoại trong 23 talk scripts và 134 CMC; V3 Merienda dấu Việt **đã được người dùng xác nhận trên menu RPCS3**. Không thử lại font, không reset aliases.

**Ngừng hướng micro-patch:** Batch 0.2 chỉ sửa câu có cùng số byte (mẫu 30/134 CMC đầu chỉ 4/437 hợp lệ), **không phải đường đến FULL**. Hãy ưu tiên **repacker CMC variable-length**, sau đó **talk/en**, rồi kiểm tra RTD/movie/subtitles/UI và glyph cần bổ sung. Khung 4 byte `00 04 00 XX` có bằng chứng nhưng chưa xác minh opcode/branch/speaker. Không tự bỏ marker hoặc viết đè UTF-8 dài hơn vào offset.

**Làm ngay:** đọc toàn bộ handoff + AGENTS.md, chạy `python tools/catalog.py validate` và `python -m unittest discover -s tests -v`, tìm blocker thật, viết và commit parser/serializer có test thay vì thêm một vòng báo cáo. Chỉ chạy binary trên **bản sao game local** có `etc.bin_`/`etc.fht_` (người dùng từng dùng `E:\Game\Folklore`). Nếu ở cloud, phát triển với fixture; không xin upload ROM/2,5GB lên repo.

**Mỗi lượt:** commit code và update `docs/STATUS.md`+`docs/QUEUE.md`; báo rõ chức năng, kiểm thử, phần đã áp và phần chưa đạt. Không nhận định 11.886/11.886 draft nghĩa là patch FULL.
