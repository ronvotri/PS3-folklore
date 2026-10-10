# Folklore — đánh giá ứng viên hội thoại ASCII (10/10/2026)

## Phạm vi và kết quả có thể xác nhận

- Theo `tools/catalog.py`, `candidate_runs` tìm dãy byte ASCII hiển thị/whitespace dài từ 4 ký tự trở lên, theo sau là byte NUL, cần ít nhất 3 chữ ASCII và có dấu cách/?/!. Điều này **không** chứng minh chuỗi là câu thoại hoàn chỉnh hoặc chuỗi có thể được ghi đè tại offset đó.
- Với `talk/en/tk100_en.bin_`, extractor quét toàn vùng byte (không dựng lại bảng câu hay metadata). Với CMC, code đọc header và chỉ quét những section có tên `talk...`; đây là giới hạn phạm vi, **không phải** parser đầy đủ của lệnh thoại.
- Sau lượt 013, `tk100` có 314/314 candidate `draft`. Trong 314 nguồn có **217** mục bắt đầu bằng ký tự newline, **23** bắt đầu bằng khoảng trắng và **19** có ký hiệu đầu bị nghi là tiền tố (heuristic). Các dạng này là dấu hiệu quan trọng của văn bản phân mảnh; các tập có thể chồng lấn, không cộng làm tổng.
- Những ví dụ thực tế: `\nmother. I wonder what happened.` (chỉ phần cuối), `$Looks like nothing happened...` (tiền tố chưa rõ), `(I don't need any favors for now.` (mở ngoặc chưa có phần đóng), `* Stay awake` (mục lựa chọn), `FF` (nhãn mơ hồ). Không được tự coi `$`, dấu `(` hoặc chữ số ở đầu là lời thoại hay loại bỏ khỏi nguồn.
- Chỉ dịch trong các trường `vi`/`notes`, giữ nguyên `source`, `source_sha256`, `id`, `file_offset`, `source_review='candidate'`. Không suy người nói từ dãy offset; dãy ID không tương đương trật tự phát thoại.

## Chưa đủ bằng chứng để viết repacker

Catalog JSON không kèm bytes xung quanh chuỗi, bảng tham chiếu, opcode, pointer relocation hay số byte dự phòng. Không thể chứng minh offset có thể ghi dài hơn, string hiện là đơn vị UI độc lập hay mảnh của một khối được cấu trúc. Các bản nháp tiếng Việt có thể dài hơn nguồn và Unicode cần đúng alias font. **Không viết biến thể thay chuỗi trực tiếp ở offset, không chạy encoder ASCII cũ, không tuyên bố đã làm repacker.**

## Quy trình xác minh tại môi trường local (không cần đưa ROM lên GitHub)

1. Với bản gốc sao lưu, kiểm tra vùng byte khoảng 64–128 byte trước/sau các offset candidate trong `tk100`, `tk101`, `LCmc000` và `LCmc004`; kiểm tra đối chiếu dữ liệu nguyên gốc trong `etc.bin_`/entry `etc.fht_`, cùng hash từng tệp đã ghi ở catalog.
2. Lập bảng các vị trí tham chiếu tới offset/string block và phân loại opcode/prefix: byte điều khiển, bảng speaker, lựa chọn, ngắt trang, khóa nhánh. Kiểm tra bằng ít nhất hai tệp talk và một CMC; không suy định dạng chung từ một đoạn mẫu.
3. Tái dựng thông điệp nguyên tiếng Anh theo control flow và so với màn hiển thị RPCS3 do người dùng tự test. Chỉ khi trùng mới nâng `source_review` từ candidate và chuẩn hóa các mảnh dịch.
4. Thiết kế repacker an toàn: xây pool riêng hoặc vùng mở rộng có pointer fixup/relocation được xác minh, kiểm tra hash nguồn, byte control, độ dài, alignment và alias/glyph; phải hỗ trợ dry-run + backup + rollback. Không thay ROM/ISO/payload cloud.
5. Bổ sung regression tests cho parse→serialize bản gốc **byte-for-byte**, giới hạn vùng và xung đột pointer. Khi đạt mới thử một vài câu tiếng Việt có dấu trong game, kiểm tra speaker, popup, dòng thoại và font/tràn khung.

## Điểm khởi đầu sau lượt 013

- Hoàn tất nháp `tk100` và ba catalog `LCmc000/002/004`, không đánh dấu `reviewed`/`tested`.
- `tk101` mới có 8/447 `draft`; mục kế tiếp `talk/en/tk101_en.bin_@000016b4`.
- Toàn bộ 158 catalog: 11.886 mục, 1.384 `draft`, còn 10.502 `todo` — đây là tiến độ ứng viên đã trích, **không phải tỷ lệ Việt hóa có thể chơi được của toàn game**.

## Bổ sung lượt 019 (11/10/2026)

- `tk103` đã được dịch nháp đến `@0000fc9a` (267/578), còn 311 candidate; 200 mục mới trong lượt có **159 nguồn mở đầu newline**, **11 nguồn mở đầu dấu cách** và chỉ **172 nguồn tiếng Anh phân biệt**. Nhiều source xuất hiện lặp lại ngay trong một tệp; đây không phải bằng chứng chúng nằm chung một lời thoại.
- Các trường hợp cần parser kiểm chứng: `@000051d2` (bị xóa khỏi ký ức mọi người?), `@000065f5` (will: di nguyện hay ý chí?), `@000074bd` (chủ ngữ/động từ thiếu), `@0000b30d` (Hag là tên riêng hay danh từ?), `@0000e9c5` (nhịp nói lắp của nhân vật). Giữ các bản Việt hóa dạng draft và notes, không khẳng định speaker.
- Phạm vi cloud: `tools/catalog.py` vẫn chỉ quét ASCII-NUL; đã xác minh không có trong dữ liệu catalog cấu trúc pointer/speaker đủ an toàn để tạo repacker. Việc phân tích dữ liệu byte nguyên gốc và vòng parse→serialize byte-for-byte vẫn là việc còn thiếu. **Không dựng patch dựa vào `file_offset` của candidate.**

## Lượt 020 — 11/10/2026: ghi chú kiểm tra parser

- 200 mục `tk103` (`@0000fe1a` đến `@0001c740`) đã có bản dịch nháp; 161 lượt trùng với nguồn cũ, 5 lượt lặp ngay trong batch, 34 nguồn mới. Một số câu cần dựng message đầy đủ: `@00016b6e` (mức hiểm nguy), `@00017c9f` (phong ấn), `@000181fc` (đóng băng nước), `@00019885` (`Oblivion` là gì?). Bản nháp vẫn `source_review=candidate`.
- JSON mới chỉ lưu chuỗi ASCII NUL/offset và metadata tối thiểu; không có chứng cứ xác minh pointer/speaker, nên chưa thể thiết kế bộ thay chuỗi vào binary an toàn. Bước tiếp theo là kiểm tra bytes nguyên gốc + parse→serialize byte-for-byte trên bản sao local, không vá thẳng tại `file_offset`.
