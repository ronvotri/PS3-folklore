# Folklore — QA hội thoại nháp lần 2 (12/10/2026)

## Phạm vi

Toàn bộ **158 catalog / 11.886 mục** có bản nháp trong GitHub, nhưng đây là **độ phủ bản nháp ứng viên**, không có nghĩa game đã Việt hóa chơi được.

Đã bổ sung công cụ QA chỉ đọc `tools/dialogue_draft_qa.py` và 4 unit test mới `tests/test_dialogue_draft_qa.py`. Chạy tại thư mục repo:

```powershell
python tools/dialogue_draft_qa.py
python tools/catalog.py validate
python -m unittest discover -s tests -v
```

Lệnh đầu đọc `translations/index.json` và catalog, ghi báo cáo `local-data/dialogue-draft-qa.json` (được .gitignore). Không sửa `vi`, `status`, font, game binary hay dữ liệu nguồn; cảnh báo chỉ là gợi ý biên tập. **4 unit test QA mới đã qua trên fixture mô phỏng** tại môi trường làm việc; **chưa khẳng định validator/test suite toàn repo đã chạy trên checkout mới**.

### QA dòng dài (đã commit, vẫn là draft)

| CMC | Ghi chú |
|---|---|
| 116 | Giảm độ dài dòng chứa Samhain, Vách đá Sidhe, Doolin từ 42 xuống 39 ký tự |
| 227 | Rút gọn câu bị văn hóa/chiến tranh đè nặng từ 41 xuống 35 ký tự |
| 800 | Rút gọn lời mời nhận bạn đồng hành từ 50 xuống 36 ký tự |
| 801 | Rút gọn mảnh câu về chiến trường từ 39 xuống 34 ký tự |

**Lưu ý:** Độ dài ký tự Unicode không tương đương độ rộng glyph/khung phụ đề thật. Chưa được xác nhận hiển thị trên RPCS3.

### Câu nguồn trùng nhau: đừng thay hàng loạt

Danh sách trùng nguồn từng phát hiện trong 1.162 nháp CMC mới:

1. `$Can you really\ngrant my wish?` (CMC 073, 235): **đã đồng bộ cùng bản dịch**, vì hai đoạn cùng hồi tưởng Cecilia/Herve.
2. `What...\nshould I do?` (CMC 073, 235): **đã đồng bộ cùng bản dịch**, cùng bối cảnh.
3. `Aiieeeegh!` (CMC 075, 211): cách diễn đạt tiếng kêu khác số chữ; cần nghe/nhìn cảnh trước khi xác định có nên thống nhất.
4. `That's it.` (CMC 105, 235): **giữ khác ngữ cảnh**; một lời hướng dẫn và một lời xác nhận câu chuyện.
5. `You!` (CMC 131, 210): **giữ khác ngữ cảnh/người đối thoại**, không tự động thống nhất ngôi.
6. `Where is she?!?` (CMC 206, 212): **giữ khác ngữ cảnh**. 206 hỏi tìm Cecilia bằng lời xưng hô thông thường; 212 là lời của người đang tức giận và đe dọa cô bé, nên gọi `nó` là lựa chọn có chủ ý.

Mọi thay đổi xưng hô ở trên vẫn là bản nháp, cần đối chiếu speaker/message order khi có dữ liệu gốc.

### CMC 800 / 801

Chuỗi ASCII bị tách mảnh, ví dụ bắt đầu bằng ký tự xuống dòng hoặc khoảng trắng, **không thể ghép hay sửa cấu trúc một cách chắc chắn** chỉ từ thứ tự `file_offset`. Chờ phân tích message opcode/pointer/speaker từ `etc.bin_` / `etc.fht_` gốc. Tuyệt đối không đặt văn bản tiếng Việt dài vào offset ứng viên gốc.

## Bước tiếp theo — không phụ thuộc dịch thêm

1. Trên máy có game gốc, chạy `RUN_DIALOGUE_DIAGNOSE.cmd` trong bản repo mới. Công cụ chỉ đọc archive và tạo `local-data/dialogue-structure-summary.json`. Không công khai `dialogue-probe.json` chứa byte/hex thô.
2. Đối chiếu ít nhất hai talk và một CMC, dựng layout command/speaker/pointer thực, chứng minh **byte-perfect parse → serialize** từng message trước khi có repacker ghi.
3. Chạy validator, toàn bộ unittest trên checkout mới và test bản dịch trong RPCS3 do người dùng điều khiển.
4. Giữ nguyên Merienda Regular 400 V3, 25 alias và bản sao nguyên gốc.

Không đánh dấu bất kỳ hội thoại nào `reviewed` hoặc `tested` chỉ vì các kiểm tra QA tĩnh ở đây.
