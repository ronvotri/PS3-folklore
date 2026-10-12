# Folklore CMC — checkpoint đồng bộ 12/10/2026

## Đã xác minh qua GitHub

- Tất cả **1.162/1.162** mục nháp CMC trong gói bàn giao (90 catalog) đã được đồng bộ lên nhánh mặc định của `ronvotri/PS3-folklore`.
- Năm catalog bị chặn ở lượt trước nay đã ghi thành công và **được fetch lại**: `LCmc206` 9 mục (commit `d61278f7`), `LCmc221` 31 mục (`37b08fa4`), `LCmc232` 12 mục (`3cab62b6`), `LCmc234` 17 mục (`c50521a7`), `LCmc301` 9 mục (`1dd487c2`). Tổng 78 mục, mỗi file đều hiện **0 todo**.
- Các catalog trước đó (85 file, 1.084 mục) được cập nhật qua commit riêng từng file. Việc đồng bộ chỉ đổi các trường `vi`, `status`, `notes`, giữ `source`, `source_sha256`, `id`, `file_offset`, `source_review` và thứ tự.
- **Đã kiểm kê thực tế toàn bộ 158 catalog trong `translations/index.json`** bằng GitHub `fetch_file`: tổng đúng **11.886/11.886 mục có bản nháp**, **0 todo, 0 mục thiếu `vi`**, số mục từng file và `file` khớp manifest. Kiểm kê gồm 1 menu và 157 catalog thoại; không còn là số ước tính.
- Bản nháp là **candidate/draft**, không phải `reviewed` hay `tested`, và không thể suy ra game đã Việt hóa chơi được.

## Kiểm tra đã thực hiện

- Đối chiếu chính xác các câu tiếng Anh, số lượng mục, số xuống dòng trước khi ghi từng catalog; không ghi đè bản dịch không trùng.
- Trên gói nháp tích lũy 1.162 mục: số dòng, Unicode NFC, 646 tiền tố có nguy cơ metadata được rà bằng script độc lập; **0 lỗi cấu trúc** được phát hiện trong các kiểm tra đó.
- Còn cần QA khẩu khí/xưng hô, 6 nhóm câu nguồn trùng có bản dịch khác nhau và các mảnh câu `CMC 800/801`; khác biệt chưa hẳn là lỗi vì có thể do ngữ cảnh.
- **Chưa xác minh** run `python tools/catalog.py validate` và `python -m unittest discover -s tests -v` trên checkout cập nhật; không khẳng định CI đã qua.
- Lưu ý: readback kiểm trạng thái/số mục không thay thế validator kiểm source SHA, NFC và placeholder của toàn bộ dữ liệu.

## Điều kiện để có bản dịch chơi được

1. Trên máy có **bản game nguyên gốc**, chạy chế độ chỉ đọc: `python tools/dialogue_diagnose.py --game-root "E:\Game\Folklore" --verify-all`. File `local-data/dialogue-probe.json` chứa byte/hex thô và phải ở máy cá nhân; chỉ bản lọc `local-data/dialogue-structure-summary.json` được cân nhắc chia sẻ sau khi kiểm tra.
2. Xác định chắc cấu trúc message, speaker/command/opcode, pointer, alignment và chỗ tái định vị string; không suy ra pointer từ trùng khớp u32 đơn thuần.
3. Chứng minh `parse → serialize` **giống byte-for-byte** trên các talk/CMC gốc, sau đó mới xây repacker thay thế text.
4. Thử và chụp ảnh trong RPCS3 theo điều khiển của người dùng; giữ bản gốc để rollback.

## Không thay đổi

- Font **Merienda Regular 400 V3** và 25 alias UTF-8 hai byte.
- Không sửa `etc.bin_`, `etc.fht_`, ISO/ROM, save, firmware hay các file game gốc.

Checkpoint này thay thế nội dung cũ nói còn 78 mục chưa đồng bộ.
