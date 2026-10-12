# Folklore — V4: giả thuyết khung bản ghi CMC 4 byte (13/10/2026)

## Dữ liệu thật do người dùng cung cấp

Báo cáo `GUI_CHO_CHATGPT_dialogue-control-stats.json` (V4), kết hợp hai JSON V3 đã lọc và catalog gốc trong repo, cho biết **26/26** khoảng ngắn (≤8 byte) giữa candidate CMC000/004 có byte **thập phân 4 (0x04)**; trong **13** khoảng có một byte điều khiển, **13** khoảng có hai byte điều khiển. Byte điều khiển khác là 12, 16, 20, 24 hoặc 28.

- **13** khoảng có 1 control byte: văn bản trích xuất kế tiếp bắt đầu tại offset chia 4 dư 3; byte 0x04 nằm **cách text 2 byte**; ký tự đầu tiên là dấu/ký tự khả nghi (ví dụ `$`, `(`, `0`, `8`, `,` hoặc dấu cách).
- **13** khoảng có 2 control byte: candidate kế tiếp bắt đầu tại offset chia hết cho 4; byte 0x04 nằm **cách text 3 byte**; một control khác (12..28, bội số 4) nằm ngay trước text.

**Giả thuyết cụ thể cần chứng minh:** một trường 4 byte căn địa chỉ 4 có dạng `00 04 00 XX`. Trong 13 trường hợp đầu, `XX` dường như là ký tự hiển thị đầu tiên mà bộ trích xuất ASCII đã nhận làm phần văn bản. Ở 13 trường hợp sau, `XX` là mã không in được nên chuỗi được nhận từ byte ngay sau trường. Ký tự hiển thị đầu tiên của candidate có thể là metadata và KHÔNG phải lời thoại.

Giả thuyết này giải thích hợp lý vì sao các nhãn đầu dòng lạ `$`, `(`, `0`, `8` xuất hiện. **Không tự xóa hoặc thay đổi các tiền tố trong bản dịch hiện có.** Chưa xác thực trên cửa sổ byte thô, chưa xác định nghĩa của `XX`, speaker, lựa chọn, thứ tự phát hoặc relocation.

## Bộ kiểm chứng V5 (chỉ đọc, không quét lại game)

- `tools/dialogue_frame_hypothesis.py`: chỉ đọc tệp **riêng tư cũ** `local-data/dialogue-probe.json` đã tạo khi chạy V3. Dò chữ ký 4 byte từ vùng khoảng trống ngắn giữa hai candidate; ở trường hợp `offset%4==3` sử dụng **ký tự đầu tiên nguồn** như byte cuối nghi vấn. Chỉ xuất số lượng khớp/không khớp, không xuất chuỗi nguồn, byte hex, sample offset hoặc raw binary.
- `tests/test_dialogue_frame_hypothesis.py`: **4/4 unit tests PASS** ở môi trường làm việc trên dữ liệu tổng hợp (một frame có marker printable, một frame với mã không in được, lỗi chữ ký/padding và ranh giới output).
- File shareable mong đợi: `local-data/dialogue-frame-hypothesis.json` hay `GUI_CHO_CHATGPT_dialogue-frame-hypothesis.json` khi dùng gói V5 chạy một lần.
- **V5 chưa chạy trên cache V3 ở máy người dùng**, nên không có bằng chứng 26/26 khung hoàn chỉnh khớp byte-for-byte. Đây là kiểm chứng pattern nhỏ, **không phải** lossless parse→serialize toàn bộ message.

## Việc phải làm trước bản vá hội thoại

1. Xác minh V5 trên 2 CMC mẫu và nhiều CMC khác; nếu có case sai, kiểm tra nguồn, alignment/command mà không bỏ qua lỗi.
2. Phân loại `XX` có phải enum speaker/portrait/voice, prefix trường, độ dài hay label; phải đối chiếu chuỗi command/nhánh và cảnh thật.
3. Viết parser read-only có các lệnh xác định và opaque records chưa biết; kiểm tra byte-for-byte roundtrip toàn bộ CMC và talk trên game gốc.
4. Khi chứng minh được relocation/alignment/encoding, mới xây repacker an toàn và bản test ngắn RPCS3. Giữ Merienda Regular 400 V3 và backup game nguyên gốc.

**Trạng thái dịch:** 11.886/11.886 mục có bản nháp `draft` trong repo, không đại diện tỷ lệ bản vá chơi được.
