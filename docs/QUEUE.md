## V6 QA — 13/10/2026: review prefix trên toàn bộ 134 CMC

- Đã rà trên GitHub toàn bộ 134 CMC: với candidate ở offset mod4=3 có ký tự đầu ASCII in được, so sánh ký tự đầu của `source` và `vi`. **Một ngoại lệ duy nhất**: CMC800 decimal offset **12071**, `beautiful...` / `đẹp...`. Không sửa vì chưa chứng minh byte thứ 4 là ký tự hiển thị hay metadata.
- Chỉnh `tools/cmc_readonly_tokens.py` dùng **`fourth_byte`** và **`remaining_ascii`** (trung tính), giữ nguyên byte thay vì mặc định đó là speaker/selector; 4/4 unit test tổng hợp chạy đạt trong môi trường mô phỏng. Chưa có kết quả chạy tokenizer trên game gốc, không có binary patch.
- Báo cáo: `docs/DIALOGUE_V6_FULL_AUDIT_RESULTS_2026-10-13.md`. Ưu tiên vẫn là 51 trường hợp ngoài khung và xác minh parser thật, không tiếp tục yêu cầu người dùng chạy công cụ chỉ để tăng số lần probe.

---

## Checkpoint 13/10/2026 — V6 full CMC frame audit & safe tokenizer

- Người dùng cung cấp V6 report thật: **134 CMC files, 1.795 source candidates đã kiểm tra**, 1.744 khớp khung `00 04 00 XX` (**97,16%**), 51 không khớp ở 27 files; 107/134 files khớp hết. Đã phân loại: 24 `not_000400_frame`, 12 `unexpected_mod1`, 12 `unexpected_mod2`, 3 `mod3_nonprintable_source_prefix`.
- CMC800 (10/14 bất thường) và CMC801 (6/18 bất thường) chiếm **16/51** ngoại lệ, ưu tiên rà mảnh câu. Không xóa/kéo offset, không tự sửa tiền tố. Chứng cứ đầy đủ: `docs/DIALOGUE_V6_FULL_AUDIT_RESULTS_2026-10-13.md`, gồm 24 offset mod1/mod2 xác định từ catalog GitHub.
- Đã tạo `tools/cmc_readonly_tokens.py` và `tests/test_cmc_readonly_tokens.py`: phân rã các frame ứng viên khớp và giữ byte opaque cho các vùng còn lại; kiểm byte-exact tái tạo, kiểm SHA/source. **4/4 test fixture tổng hợp PASS** (kiểm thử cục bộ với shim xác thực tương thích V6); **chưa chạy trên 134 CMC thực của user**, chưa có parser/speaker/opcode/pointer và không có chức năng ghi bản vá.
- Bước tới: byte-exact roundtrip toàn bộ CMC trên máy có bản gốc, chứng minh metadata/selector thực sự và xử lý 51 ngoại lệ; giải mã talk/en riêng. Sau đó mới cân nhắc repacker an toàn, thử RPCS3.
- **11.886/11.886 mục ở mức bản nháp trên repo**, KHÔNG phải game Việt hóa playable. Giữ nguyên Merienda V3.

---

## 13/10/2026 — V5 xác nhận frame 26/26, V6 audit toàn bộ CMC

- **Dữ liệu thật V5:** `GUI_CHO_CHATGPT_dialogue-frame-hypothesis.json` báo `LCmc000` khớp 6/6, `LCmc004` khớp 20/20 chữ ký `00 04 00 XX` tại candidate gần nhau (≤8 byte), 13 marker printable tại vị trí mod4=3, 13 marker control ngay trước text mod4=0; **không lỗi trong tập đã khảo sát**, song còn 7 gap CMC dài hơn 8 byte chưa kiểm tra.
- Hai `tk100/101` không áp dụng V5, không có bằng chứng frame của script talk. Giả thuyết metadata prefix `$/(,0,8...` đáng chú ý nhưng chưa biết speaker/command grammar; **giữ nguyên dữ liệu dịch nháp và font Merienda V3**.
- **Bước kiểm tra chính:** `tools/cmc_frame_audit.py` đọc nguyên bản `etc.bin_`/`etc.fht_`, kiểm chứng 134 catalog CMC / 1.795 candidate SHA/source/NUL trước khi thống kê frame toàn CMC. Fail-closed trên nguồn sai, báo lý do khung không khớp, chỉ xuất metadata. 4/4 unit test fixture PASS. Chưa chạy trên PC người dùng, không có parser message hoặc repacker.
- ZIP Windows chạy một lần `Folklore-V6-KiemChung-ToanBo-CMC.zip`: giải nén, chạy `CHAY_KIEM_TRA_FOLKLORE_V6.cmd`, trả `GUI_CHO_CHATGPT_cmc-frame-audit.json`. Code/README `docs/DIALOGUE_V5_FRAME_RESULTS_2026-10-13.md`.
- Sau V6: nghiên cứu quy luật trên CMC bất thường, thiết kế parser read-only cho từng record, đối chiếu grammar với lựa chọn/speaker rồi mới làm byte-perfect parse→serialize và repacker. Không tuyên bố 11.886 mục bản nháp đã playable.

---

## 13/10/2026 — V4 control-values & V5 giả thuyết khung CMC

- Đã nhận báo cáo `GUI_CHO_CHATGPT_dialogue-control-stats.json` từ người dùng: ở CMC000/004, **26/26 gap ngắn** có đúng một byte giá trị 4; 13 gap có thêm byte control 12/16/20/24/28, 13 gap không thêm control. Tương quan vị trí text theo mod4 và tiền tố lạ rất mạnh.
- **Giả thuyết đang kiểm chứng, KHÔNG phải kết luận:** một trường aligned 4 byte `00 04 00 XX`; nếu `XX` là ký tự ASCII, bộ trích xuất có thể đã gom byte metadata vào text. Chưa biết `XX` là speaker, opcode hay tham số nào; chưa sửa catalog để bỏ prefix.
- Tạo `tools/dialogue_frame_hypothesis.py` và `tests/test_dialogue_frame_hypothesis.py` (4/4 unit test mô phỏng PASS). Bộ V5 1-click chỉ đọc `local-data/dialogue-probe.json` private cache từ V3, xuất thống kê `dialogue-frame-hypothesis.json` đã lọc, không đụng game/font.
- Báo cáo chi tiết `docs/DIALOGUE_V4_FRAME_HYPOTHESIS_2026-10-13.md`. Cần chạy V5 thật, rồi xác minh nhiều CMC / command grammar / message roundtrip trước khi viết repacker.
- Tổng repo 11.886 mục có bản nháp vẫn không đồng nghĩa game playable.

---

## Mốc 13/10/2026 — V3 thực đo trên game, mẫu gap CMC, V4 nhanh

- Người dùng gửi **hai JSON V3 đã lọc**. Chạy chéo `tools/dialogue_gap_crosscheck.py` trên dữ liệu thực: **PASS 127/127 cặp mẫu**, 4/4 test synthetic PASS.
- **26/26 gap ngắn ≤8 byte trong CMC000/004** chỉ gồm zero + control; đúng quy luật: 13 gap có 1 control byte, text tiếp theo ở `offset % 4 == 3`; 13 gap có 2 control byte, text tiếp theo ở `offset % 4 == 0`. Đây chỉ là dấu hiệu header/căn chỉnh, **không phải parser hay pointer đã xác minh**.
- 31/33 gap CMC ≤32 byte: 28 chỉ zero/control, **3 còn byte printable/space** (gap 23, 31 ở CMC000 và 19 ở CMC004), cần khảo sát trước khi khẳng định catalog có hết mọi văn bản người chơi thấy.
- `tk100/101` mới chọn 48 mẫu mỗi file, không thể suy ra khoảng cách mọi candidate/record từ các cặp mẫu này.
- Tạo công cụ V4 `tools/dialogue_control_stats.py` (4/4 unit tests synthetic PASS; chung hai tool mới 8/8 PASS) đọc **báo cáo raw đã lưu cục bộ từ V3**, chỉ xuất tần suất numeric control byte trong gap ngắn, không ghi game. Bản ZIP Windows một-click sử dụng cache V3 được chuẩn bị; **chưa thử launcher trên máy người dùng**.
- Báo cáo chứng cứ: `docs/DIALOGUE_V3_GAP_FINDINGS_2026-10-13.md`. Điều kiện viết repacker không đổi: message parser grammar + byte-perfect roundtrip trên binary thật trước khi thay chuỗi UTF-8.
- **Còn 11.886/11.886 mục nháp, chưa có bản dịch hội thoại playable; giữ nguyên font Merienda V3.**

---

## Mốc binary gốc và chẩn đoán V3 (12/10/2026)

- Đã nhận báo cáo thật `GUI_CHO_CHATGPT_dialogue-structure-summary.json` cho 4 tệp: `tk100` (314), `tk101` (447), `LCmc000` (11), `LCmc004` (24), tổng **796 nguồn ASCII-NUL**; báo cáo chỉ có metadata, không chứa hex/text.
- Hai CMC có lần lượt 16 và 21 section, mỗi tệp gồm 6 section rỗng ở cuối; lỗi V1 đã được sửa. Bộ dò U32 chưa cho phép xác nhận pointer/message grammar.
- Tạo công cụ `tools/dialogue_gap_fingerprint.py` chỉ đọc probe local và xuất `local-data/dialogue-gap-fingerprint.json` (độ dài/nhóm byte xen giữa, không dữ liệu text/hex), 4 unit test synthetic đã đạt.
- `RUN_DIALOGUE_DIAGNOSE.cmd` hiện chạy thêm công cụ V3; đã đóng gói launcher tự tải mã mới, trả về hai summary đã lọc. Chưa chạy V3 trên máy người dùng.
- Nghiên cứu: `docs/DIALOGUE_REAL_PROBE_FINDINGS_2026-10-12.md`, hướng dẫn `docs/DIALOGUE_LOCAL_QUICKSTART.md`. Bước tiếp: phân tích gap fingerprint, giả thuyết grammar; message parse→serialize byte-perfect trước khi cho phép repacker.
- **Không đổi game, font Merienda V3, save, catalog status. 11.886/11.886 bản nháp vẫn không đồng nghĩa patch playable.**

---

## Chẩn đoán CMC — 12/10/2026 (khắc phục lỗi người dùng)

- Người dùng chạy bộ chẩn đoán 1-click trên bản game local; công cụ dừng với `Diagnosis refused: Invalid CMC section bounds`. **Không có thay đổi lên file game**.
- Mã `tools/catalog.py` cho phép hai offset CMC bằng nhau (section rỗng), trong khi `tools/dialogue_probe.py` trước đó lại cấm. Sửa cho phép `start == end`, vẫn chặn đầu section đè bảng tên, offset giảm hoặc vượt file; `tools/dialogue_summary.py` cũng chấp nhận section rỗng. Lỗi kế tiếp (nếu có) sẽ kèm tên file CMC và chi tiết ranh giới.
- Thêm unit test hồi quy ở `tests/test_dialogue_probe.py`, `tests/test_dialogue_summary.py`. Đã xác minh 4 tình huống kiểm tra biên trên fixture tổng hợp; **chưa có xác nhận chạy lại trên binary game thật hoặc full suite checkout mới**.
- Launcher ZIP 1-click tải mã nguồn `main.zip` mỗi lượt nên sẽ nhận fix. Chạy lại; nếu vẫn lỗi, gửi đầy đủ dòng lỗi chi tiết. Không upload game/hex thô, không thay font Merienda V3.
- Tài liệu: `docs/DIALOGUE_LOCAL_QUICKSTART.md`.

---

## QA2 — 12/10/2026

- Đã đối chiếu 1.162 bản nháp CMC mới trong gói tích lũy, phát hiện 6 nhóm cùng nguồn có cách dịch khác nhau; chỉnh 2 câu cùng bối cảnh hồi tưởng Cecilia/Herve, **giữ những khác biệt có lý do ngữ cảnh** (đặc biệt lời tìm Cecilia ở CMC206 so với đe dọa ở CMC212).
- Đã rút ngắn 4 câu tiềm ẩn tràn khung (CMC116, CMC227, CMC800, CMC801); chưa thử trên giao diện thật.
- Tạo `tools/dialogue_draft_qa.py` báo cáo QA chỉ đọc, gồm bản dịch trùng/xưng hô, độ dài dòng, mảnh câu, marker, SHA ID và xuống dòng; tạo 4 unit test, **4/4 đạt trên dữ liệu mô phỏng**. Chạy bằng `python tools/dialogue_draft_qa.py`, report nằm `local-data/dialogue-draft-qa.json`.
- Hướng dẫn/ngoại lệ tại `docs/DIALOGUE_QA_REVIEW.md`. **Không** đánh dấu reviewed/tested. Chưa chạy full suite trên checkout mới, chưa có dữ liệu binary thực, chưa có parser/repacker hội thoại.
- Cần báo cáo chẩn đoán game gốc sau `RUN_DIALOGUE_DIAGNOSE.cmd` để bắt đầu giải mã command stream và chứng minh roundtrip message.

---

# Ưu tiên hiện tại — 12/10/2026 (mốc mới nhất)

**Mốc mới:** Đã đồng bộ 1.162/1.162 mục CMC còn thiếu lên GitHub; gói 90 catalog giờ toàn bộ là `draft`. Đã đọc lại toàn bộ 158 catalog từ GitHub và xác nhận 11.886/11.886 mục có bản nháp, 0 todo. **Không đồng nghĩa game playable.** Xem `docs/CMC_SYNC_CHECKPOINT_2026-10-12.md`.

1. **Chặn kỹ thuật thực sự:** cần khảo sát `etc.bin_` + `etc.fht_` gốc từ máy người dùng bằng `python tools/dialogue_diagnose.py --game-root "E:\Game\Folklore" --verify-all`. Chỉ chia sẻ báo cáo cấu trúc đã lọc, không đưa file binary/hex thô lên GitHub.
2. Xác định speaker/opcode/pointer/định dạng message, chứng minh serialize byte-perfect trước khi viết repacker và thử RPCS3. Không dùng phép gán offset cũ để ghi câu Việt dài tùy ý.
3. Chạy lại `python tools/catalog.py validate` và `python -m unittest discover -s tests -v` trên checkout mới; chưa có kết quả CI được xác nhận.
4. QA 6 xung đột nguồn trùng, câu tách mảnh ở CMC 800/801, xưng hô, độ dài UI; chỉ đánh dấu reviewed/tested khi có chứng cứ phù hợp.
5. Giữ nguyên Merienda V3, 25 alias, dữ liệu game gốc và cách người dùng tự điều khiển RPCS3.

---

# Hàng đợi — cập nhật 11/10/2026

## Bắt đầu ngay

1. **ƯU TIÊN KỸ THUẬT:** Bộ khảo sát hiện có `tools/dialogue_probe.py`, lọc metadata `tools/dialogue_summary.py`; thêm lệnh tiện dụng `tools/dialogue_diagnose.py` (tự tìm archive local và chạy cả hai) cùng 6 unit test mới, hướng dẫn `docs/DIALOGUE_LOCAL_QUICKSTART.md`. **Chưa thử binary game gốc, chưa có parser/repacker.** Cần báo cáo cấu trúc local để định danh opcode/pointer/speaker, sau đó mới parse→serialize message byte-for-byte.
2. **Việc dịch nháp còn lại (thứ yếu đến khi hiểu format):** talk `tk600` và `tk700` đã đủ draft. Tiếp theo `cmc/en/LCmc063_en.bi5_@000028e7` rồi `LCmc064`, `LCmc065` và các CMC chưa dịch. Không coi độ phủ draft là tỷ lệ game playable.
3. Trước khi build talk/CMC: đọc `docs/DIALOGUE_CANDIDATE_AUDIT.md` và `docs/DIALOGUE_BINARY_PROBE.md`. Chạy probe với archive nguồn **chỉ ở máy local**; báo cáo nằm trong `local-data/`, không push lên GitHub. Các mẫu u32 chỉ là giả thuyết, không cho phép ghi patch.
4. Menu `lang_en.bi5_` đã 1.016/1.016 bản nháp; cần QA glyph/alias, độ dài và hiển thị thực tế. ID tệp và ID offset **không quyết định** thứ tự hội thoại.

## Mốc bàn giao

Menu **1.016/1.016 draft**; CMC **633 draft**; các talk `tk000`, `tk011`, `tk100`–`tk107`, `tk200`–`tk207`, `tk306`, `tk307`, `tk500`, `tk600`, `tk700` đã hoàn tất nháp. Tổng toàn repo **10.724/11.886 draft**, còn **1.162 todo** trong 158 catalog. Hội thoại vẫn `candidate`/`draft`, chưa parser/repacker/test.
Người dùng xác nhận V3 “ok rồi” sau thử sửa khoảng hở sau ấ/ớ.
Người dùng tự mở game/test/gửi ảnh; không tự điều khiển giả lập.

## Chưa giải quyết

- Parser hội thoại, metadata/prefix, repacker talk/cmc.
- Mở rộng vùng menu khi câu dịch dài vượt chỗ trống.
- Mở rộng 251 glyph/25 alias cho đủ chữ Việt và dấu câu.
- Phụ đề phim, chữ trong ảnh, PS3 thật và Steam Deck.

## Ghi sau mỗi lượt

Theo cập nhật yêu cầu người dùng ngày 11/10/2026: **không giới hạn cứng 200
mục/lượt**; làm nhiều nhất khi vẫn giữ chất lượng/QA. Ưu tiên hoàn tất catalog,
tránh dịch lại nguồn trùng, rà ngữ cảnh, xưng hô, newline và control markers.
Chia nhóm kiểm tra nội bộ theo độ khó, commit sau khi hoàn thành một khối nhất
quán. **Ưu tiên nhóm 50–100 mục khi phiên dễ bị gián đoạn/crash**, không cố gom
hàng trăm mục chưa commit. Có thể làm ít hơn khi thiếu speaker/metadata hoặc phát hiện lỗi thật.
Ghi tệp, ID đầu/cuối hoặc danh sách ID, số mục đổi trạng thái, ngữ cảnh còn
thiếu, kết quả kiểm tra, việc kế tiếp. Giữ lại mốc font V3 khi thêm lịch sử.

## Lượt menu 001 — 10/10/2026

- Tệp: `translations/catalogs/menu/lang_en.bi5_.json`; đúng 50 mục `todo` đầu tiên → `draft`, từ `lang_en.bi5_@0000311b` đến `lang_en.bi5_@00004124` (không liên tục vì xen kẽ 134 bản nháp cũ).
- Chủ đề: cấu hình tay cầm, lưu/cài dữ liệu PS3, chọn ngôn ngữ, tóm tắt Ellen/Keats. Giữ nguyên ID/nguồn/hash/offset/order/source_review và số ngắt dòng mỗi mục; bản dịch NFC.
- Chú ý: thuật ngữ tạm `Transcension` → `Siêu hóa`, `Faery Realm` → `Cõi Faery`, `Hellrealm` → `Cõi Địa Ngục`; cần rà nhất quán trong các catalog tiếp theo.
- Đối chiếu chuỗi trùng trước khi build map nguồn → dịch; không âm thầm lấy bản sau đè bản trước. Trong game chưa được người dùng xác nhận lượt này.
- Kiểm tra trước commit: đối chiếu 50 ID, nguồn/metadata bất biến, NFC, số dòng và placeholder; GitHub Actions sẽ chạy validator/unittest Windows+Linux sau commit.
- **Tiếp theo:** xử lý `lang_en.bi5_@0000419f` (`Ellen traveled into the Faery Realm to discover the secret of her past.  The family bond that she discovers  brings Suzette to tears...`), rồi các mục `todo` phía sau; sau đó chuyển sang nhóm CMC theo thứ tự của hàng đợi.

## Lượt menu 002 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: dịch đúng 50 mục `todo` kế tiếp → `draft`, từ `lang_en.bi5_@0000419f` đến `lang_en.bi5_@00004bb3` (IDs không liên tục do xen kẽ mục đã có bản dịch).
- Nội dung: 7 tóm tắt/câu chọn truyện Ellen–Keats; đi lại, áo choàng, hiệu ứng; các cõi và tên vùng trên bản đồ.
- Giữ nguyên nguồn, thứ tự, hash, offset, ID và `source_review`; giữ số ngắt dòng và ký hiệu ○○○○○○○○○. Bản dịch NFC, chưa kiểm thử RPCS3.
- Tham chiếu tên: `Faery Realm` → `Cõi Faery`; `Hellrealm` → `Cõi Địa Ngục`; `Netherworld` → `Cõi âm`; `Undersea City` → `Thành phố đáy biển`; `Endless Corridor` → `Hành lang Vô tận`. Giữ nguyên các tên riêng Daru/Gesh/Avalon/Brahma/Warcadia/Fleshrum. Thuật ngữ hiệu ứng Bond/Destroy, MC, KB, Eternal Regress và Cromlech còn cần rà; xem notes từng mục.
- QA: kiểm soát 50 ID kế tiếp, chỉ đổi vi/status/notes, giữ newline/control tokens, kiểm tra bản dịch trùng không có xung đột. Sau commit, đối chiếu GitHub Actions (validator + unittest trên Windows/Linux).
- **Tiếp theo:** `lang_en.bi5_@00004bc6` — `Inquisition Bridge`. Tiếp tục 50 mục `todo` theo thứ tự, chưa đánh dấu mục nào `reviewed`/`tested` nếu chưa kiểm thử.

## Lượt menu 003 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: xử lý 50 mục `todo` kế tiếp → `draft`, từ `lang_en.bi5_@00004bc6` đến `lang_en.bi5_@00004e95`, một số mục xen kẽ đã có bản nháp từ V3.
- Chủ đề: 19 địa danh bản đồ (gồm 7 tên Doolin lặp hai lần), HP/EXP, 12 loại hệ/hiệu ứng, 17 tên vật phẩm. Giữ HP/EXP nguyên viết tắt; đồng bộ Doolin/Sidhe với lượt trước.
- Các tên cần kiểm chứng: Inquisition Bridge → Cầu Thẩm vấn, Murk → Vùng Mù mịt, Henge → Vòng đá cổ; Guard/Barrier → Đỡ đòn/Kết giới; Memento Key → Chìa khóa Kỷ vật, Epigraph fragment → Mảnh văn khắc. Ghi chú cụ thể từng ID trong catalog.
- QA trước commit: 50 ID liên tiếp trong dãy `todo`, 50 mục đổi đúng `vi/status/notes`; tất cả nguồn/hash/offset/`source_review` giữ nguyên; NFC, số dòng, placeholder/token; không có xung đột khi hai mục trùng nguồn; không sửa font hay binary.
- Chưa có kiểm thử hiển thị RPCS3; chỉ `draft`, chưa `reviewed/tested`. GitHub Actions chạy validator + unittest trên Windows/Linux sau commit.
- **Tiếp theo:** bắt đầu `lang_en.bi5_@00004ea3` (`Yellow liquid`), dịch 50 mục `todo` tiếp theo; sau menu tiếp tục CMC/talk theo hàng đợi.

## Lượt menu 004 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: dịch đúng 50 mục `todo` kế tiếp → `draft`, từ `lang_en.bi5_@00004ea3` đến `lang_en.bi5_@00005386`.
- Nhóm: 16 tên vật phẩm/nguyên liệu (chất lỏng, đá/quặng, bụi, hạt cây); 34 nhãn trang sách tranh thuộc 4 cõi, có các chuỗi lặp tại nhiều vị trí.
- Bản dịch trang sách thống nhất `Sách tranh <tên cõi>, tr. N`; giữ các tên cõi đã chốt từ lượt 002. Nhãn lặp dùng cùng bản dịch, không tự ghi đè nguồn.
- Chưa xác minh hình ảnh: `Pulse Tree Nut` → `Hạt cây Mạch đập` (tạm), `Aqua liquid` → `Chất lỏng màu xanh ngọc` (tạm), `Golden Ore` → `Quặng ánh vàng` (tạm). Có notes tại ID tương ứng.
- QA trên dữ liệu: 50 ID đúng checkpoint; chỉ chỉnh `vi/status/notes`, giữ nguyên thứ tự/source/hash/offset/`source_review`; NFC, số ngắt dòng và control token; không có xung đột bản dịch cho cùng source. GitHub Actions chạy `python tools/catalog.py validate` và `python -m unittest discover -s tests -v` trên Windows/Linux sau khi push.
- Không đụng font Merienda V3, ROM/ISO hay payload; 50 mục mới là `draft`, chưa được thử trực tiếp trong RPCS3.
- **Tiếp theo:** `lang_en.bi5_@000053ab` — `Endless Corridor picture book, pg. 5`, dịch 50 mục `todo` kế tiếp.

## Lượt menu 005 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: dịch đúng 50 mục `todo` kế tiếp → `draft`, từ `lang_en.bi5_@000053ab` đến `lang_en.bi5_@00005956`.
- Gồm 26 nhãn trang sách tranh (Endless Corridor, Hellrealm, Corrupt Village, Netherworld Core), 13 tên sách, 7 áo choàng và 4 vật phẩm cốt truyện liên quan Ellen/Suzette/Renaldo/Regine/Herve.
- Thuật ngữ nhất quán với lượt trước: Endless Corridor → Hành lang Vô tận; Hellrealm → Cõi Địa Ngục; Netherworld Core → Lõi Cõi âm; các sách cùng nguồn dùng bản dịch trùng khớp. Corrupt Village → Làng Tha hóa là tên **tạm** cần xác minh trong game.
- `Endless Corridor picture book ` có khoảng trắng cuối bất thường trong nguồn: không sửa nguồn; lược trong bản dịch, ghi chú tại entry. Không được tự gộp/ghi đè các nguồn khi build.
- QA cấu trúc trước commit: 50 ID và thứ tự `todo` đúng checkpoint, chỉ thay `vi/status/notes`, giữ source/hash/offset/source_review; NFC, số ngắt dòng, placeholder/control token; 0 source trùng có bản dịch xung đột.
- Không can thiệp font Merienda V3, ROM/ISO, payload; các mục mới vẫn `draft`, chưa test trong RPCS3. CI GitHub Actions chạy validator + unittest cho Windows/Ubuntu sau khi push.
- **Tiếp theo:** `lang_en.bi5_@00005982` — `Left side of a photo / that was torn in half`, rồi 49 mục `todo` kế tiếp.

## Lượt menu 006 — 10/10/2026

- `translations/catalogs/menu/lang_en.bi5_.json`: dịch đúng 50 mục `todo` kế tiếp thành `draft`, từ `lang_en.bi5_@00005982` đến `lang_en.bi5_@00006235`.
- Nội dung: 28 mô tả vật phẩm, tranh/đồ liên kết; 6 áo choàng Sidhe; 13 sách tranh Folk; 3 nhãn Game Over/Continue/Save and exit.
- Giữ nguyên các tên Herve, Cecilia, Lester, Sidhe, Faery, Folk; các cõi Cõi Faery, Cõi Địa Ngục, Lõi Cõi âm, Hành lang Vô tận và Làng Tha hóa (tạm) đã dùng. Giữ nguyên chỉ dấu `[Link item]` và MC. Có ghi chú trong các mục chưa rõ.
- QA: kiểm soát đúng 50 ID, chỉ đổi vi/status/notes, không đụng source/hash/offset/order/source_review; NFC, newline, tokens, bản dịch nguồn trùng: 0 xung đột.
- Không đụng font V3, payload, ROM/ISO; chưa thử hiển thị trong RPCS3, không đánh dấu tested. GitHub Actions chạy validator/unittest trên Windows/Linux khi push.
- **Tiếp theo:** `lang_en.bi5_@00006243` — `Exit`, dịch tiếp 50 mục menu.

## Lượt menu 007 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: dịch đúng 50 mục `todo` kế tiếp → `draft` từ `lang_en.bi5_@00006243` đến `lang_en.bi5_@0000657d`, không liên tục do các bản mẫu V3 xen giữa.
- Chủ đề: giao diện thoát/lưu/tiếp tục; 12 tiêu đề chương/chủ đề (Mirage, Familial Warmth, Lamplight, Only one Wish, Oblivion, Youth, Labyrinth, Darkness, Judgment, Guilt, Memory, Fear); Ellen/Keats, 9 nhãn thế giới/địa danh và nhãn trạng thái/dữ liệu hệ thống.
- Thuật ngữ giữ nhất quán: Làng Doolin, Cõi Faery, Warcadia, Thành phố đáy biển, Hành lang Vô tận, Cõi Địa Ngục, Làng Tha hóa (tạm), Lõi Cõi âm; Destroy → Hủy diệt, Slash → Chém, Guard → Đỡ đòn. Giữ Ellen/Keats nguyên tên. Tiêu đề chưa có ngữ cảnh chương đầy đủ nên đánh dấu `draft`.
- QA cấu trúc trước commit: đúng 50 ID từ todo; chỉ chỉnh vi/status/notes, nguồn/ID/hash/offset/order/source_review bất biến; kiểm tra NFC, newline, mã đặc biệt, 0 source trùng có bản dịch xung đột.
- Không thay đổi Merienda V3, ROM, ISO, alias/font payload; chưa thử runtime RPCS3, giữ `draft`. CI Windows/Linux chạy `python tools/catalog.py validate` và `python -m unittest discover -s tests -v` sau commit.
- **Tiếp theo:** `lang_en.bi5_@00006583` (`Barrier`), thêm 50 mục menu kế tiếp.

## Lượt menu 008 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: xử lý đúng 50 mục `todo` thành `draft`, từ `lang_en.bi5_@00006583` đến `lang_en.bi5_@00006821`.
- Nội dung: 9 chỉ số/hệ/hiệu ứng (Barrier, Earth, Ice, Fire, Thunder, Wind, Bond, Charm, Sleep); 12 thông báo nâng cấp Folk/Karma; 4 mục nhiệm vụ; 20 nhãn bộ đếm còn lại từ 20 đến 1; 5 thông báo phát hiện Folk/lối ra/liên kết vật phẩm/Karma.
- Giữ nguyên thuật ngữ chuẩn Folk, Karma, MC, Malabaricus và placeholder `%s`; khớp Barrier → Kết giới, Bond → Trói buộc, Charm → Mê hoặc, Thunder → Sét với các lượt cũ. Thuật ngữ Charge Level, Element Ability, Ammo count và Link item còn cần xác minh hiển thị/cơ chế: có notes.
- QA: đối chiếu 50 ID theo `todo`, chỉ thay vi/status/notes; bất biến source/hash/offset/order/source_review, bảo toàn NFC/newline/token; 0 xung đột giữa bản dịch cùng nguồn. Không can thiệp font V3, ROM, ISO hoặc payload.
- Chưa thử runtime RPCS3, mọi mục vẫn `draft`. GitHub Actions chạy `python tools/catalog.py validate` và `python -m unittest discover -s tests -v` trên Windows/Linux sau commit.
- **Tiếp theo:** `lang_en.bi5_@00006833` — `Receive Folk` và 49 mục `todo` kế tiếp.

## Lượt menu 009 — 10/10/2026

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: dịch đúng 50 mục menu `todo` kế tiếp thành `draft`, từ `lang_en.bi5_@00006833` đến `lang_en.bi5_@00007030`.
- Chủ đề: nhận/gửi Folk và vật phẩm liên kết, 4 nhiệm vụ Herve có điều kiện mở theo Keats/Ellen, trao đổi Id/dữ liệu quái vật, Karma, trình tự PSP™ Link/Memory Stick™, lỗi giao tiếp và tăng hạng Keats/Ellen.
- Giữ các mã `%s`, `%d`, ký hiệu `™`/`®` và tên `PSP™`, `PlayStation®Portable`, `Memory Stick™`, `Pied Piper`, `Folk`, `Id`, `Karma`, `Keats`, `Ellen`, `Herve`. Ghi notes cho các chỗ nghĩa UI chưa chắc (Linked item/Give Id/Increased Id), nguồn có typo `has bee` và khoảng trắng thừa: không sửa source.
- QA cấu trúc trước commit: đúng 50 ID tiếp theo, chỉ vi/status/notes thay đổi; source/hash/offset/order/source_review giữ nguyên; NFC, số xuống dòng và protected tokens giữ nguyên; 0 xung đột chuỗi English trùng. Không can thiệp font Merienda V3, ROM/ISO/binary/payload.
- Vẫn ở mức `draft`, chưa hiển thị/test với RPCS3. GitHub Actions chạy `python tools/catalog.py validate` và `python -m unittest discover -s tests -v` (Windows/Ubuntu) sau commit.
- **Tiếp theo:** `lang_en.bi5_@00007059` — `Level up for Keats! / Maximum HP increased!`, tiếp 50 mục menu.

## Lượt menu 010 — 10/10/2026 (200 mục)

- Đã xử lý **200 mục** `todo` → `draft` trong `translations/catalogs/menu/lang_en.bi5_.json`, từ `lang_en.bi5_@00007059` đến `lang_en.bi5_@0000874e`. Chia bốn nhóm 50 để QA nhưng chỉ commit/bàn giao một lượt.
- Nội dung: lên cấp, sách tranh, đá ký ức/hệ chiến đấu, điều kiện mở đường, các địa điểm, UI tương tác, cảnh báo HDD, trang phục/chỉ số, tên nhân vật/Folk, đoạn thoại Ellen–Keats–Livane, menu phụ đề và chế độ hầm ngục.
- Đồng bộ các thuật ngữ Folk, Id, Karma, MC, HP, HDD, tên nhân vật/cõi; dấu cách thừa tại nguồn Gam, tên vai Scarecrow, Special 1, FF và diễn giải hệ hiệu ứng vẫn có notes cần xác minh. Giữ riêng quan hệ và lời thoại theo nội dung nguồn, không tự suy diễn.
- QA: đúng 200 ID `todo`, chỉ sửa vi/status/notes, nguồn/sha/offset/order/source_review bất biến; NFC, newline, placeholder/control token giữ nguyên; 0 xung đột ở các English source trùng. Không can thiệp font Merienda V3 hoặc binary/payload game.
- Chưa test trong RPCS3, vẫn `draft`. Chạy GitHub Actions validator + unittest Windows/Ubuntu sau commit.
- **Tiếp theo:** `lang_en.bi5_@00008757` — `  Creating Dungeons`; còn 232 mục menu, tiếp tục ~200 mục lượt 011.

## Lượt menu 011 — 10/10/2026 (200 mục)

- Tệp `translations/catalogs/menu/lang_en.bi5_.json`: hoàn tất 200 mục `todo` → `draft`, từ `lang_en.bi5_@00008757` đến `lang_en.bi5_@00009bbd`; QA bốn nhóm 50, commit một lượt.
- Nội dung: hướng dẫn tạo hầm ngục, Download Play, thưởng điểm, quy tắc hầm ngục/thử nghiệm, tải lên và xếp hạng, lỗi mạng, dữ liệu phòng/vật phẩm tăng cường, mã thưởng %s, cảnh báo PSN, giao diện chỉnh sửa, cấu hình phòng/điều kiện hoàn thành, thoát/bỏ cuộc.
- Các mảnh văn bản cùng thông báo được dịch để đọc liền mạch nhưng giữ từng ID và nguồn nguyên vẹn. Thống nhất Boost → Tăng cường, Quota → Chỉ tiêu (tạm), CampaignPt → Điểm chiến dịch (cần QA bố cục), Dungeon → hầm ngục, Test Play → Chơi thử, Folk nguyên danh xưng. Có ghi chú cho câu nguồn sai 'Dungeon Dungeon' và mảnh thông báo bị chia nhỏ.
- QA: chỉ đổi vi/status/notes của đúng 200 mục; bất biến id/source/sha256/offset/source_review/order; NFC, newline, mã đặc biệt %s, △○×□, ™/® và khoảng trắng đầu/fullwidth; không có source trùng dịch xung đột. Không thay font V3 hoặc ROM/binary/payload.
- Chưa test trong RPCS3; các mục vẫn draft. Chạy validator/unittest Windows và Ubuntu qua GitHub Actions sau commit.
- **Tiếp theo:** `lang_en.bi5_@00009bd3` (`Play current Dungeon?`), còn đúng 32 mục menu; hoàn tất menu, rồi bắt đầu kiểm tra CMC/talk như hàng đợi.

## Lượt 012 — 10/10/2026 (200 mục mới: menu + CMC/talk)

- **Menu:** 32 mục cuối (`lang_en.bi5_@00009bd3` → `lang_en.bi5_@00009f3d`) chuyển `todo→draft`; **1.016/1.016 menu hoàn tất ở mức nháp**. Sửa một bản dịch cũ ở `@0000943b` (fragment `corridor item.`) thành trung tính `hành lang.` do source lặp trong ngữ cảnh khác.
- **CMC:** 11 câu `LCmc000` + 11 câu `LCmc002` được dịch nháp; giữ tiền tố `$`/`(` và newline, không tự gán người nói.
- **Talk:** 146 candidate đầu trong `tk100_en.bin_` (`talk/en/tk100_en.bin_@00001158` → `talk/en/tk100_en.bin_@00008727`) được dịch nháp; nhiều câu chỉ là mảnh ASCII NUL, chưa thể xác minh speaker/trật tự nên ghi notes ở từng mục.
- Tổng 200 mục `todo→draft` (32+22+146), cộng 1 chỉnh sửa bản dịch cũ có lý do. Kiểm tra ID/source/sha/offset/source_review/order bất biến; Unicode NFC, số newline, ký hiệu đặc biệt và bản dịch nguồn trùng. Font V3 không đổi, không commit ROM/ISO/payload.
- **Chưa kiểm thử game:** menu cần kiểm tra bố cục và đủ glyph; CMC/talk hiện không có parser/repacker và không thể trực tiếp tích hợp vào game. Sau push CI Windows/Ubuntu chạy validator và unittest.
- **Tiếp theo:** `talk/en/tk100_en.bin_@00008818` (`. We won't attack you.`), sau đó làm các ứng viên hội thoại tiếp theo và nghiên cứu ghép fragment.

## Lượt 013 — 10/10/2026 (200 ứng viên talk/CMC)

- 168 mục `todo → draft` còn lại trong `translations/catalogs/talk/tk100_en.bin_.json` (`talk/en/tk100_en.bin_@00008818` → `@000106cf`): **314/314 tk100 đã có bản dịch nháp**. Có ghi chú theo từng ID về những mảnh lời thoại bị cắt, ký hiệu chưa rõ và các tên riêng cần xác minh.
- 24 mục CMC của `LCmc004_en.bi5_.json` (`@00003c70` → `@000040cc`): bản dịch tự nhiên hơn, giữ ký hiệu đầu `(`, `$`, `0`, `4`, `8`, dấu phẩy và ngắt dòng. Halflive/Faery giữ danh xưng.
- 8 nhãn giao diện đầu tiên của `tk101_en.bin_` (`@00001158` → `@00001650`) dùng bản dịch thống nhất từ `tk100`; tiếp tục ở `@000016b4`.
- **Tổng 200 mục mới** (168 + 24 + 8), toàn bộ dự án còn **10.502 `todo`**. QA: ID, source, hash, file_offset, source_review, order bất biến; chỉ vi/status/notes, Unicode NFC, số ngắt dòng, placeholder/tiền tố không mất; 0 source trùng có bản dịch mâu thuẫn trong tk100, tk101 hoặc giữa hai tệp.
- Phân tích scanner `tools/catalog.py`: `candidate_runs` lấy ASCII dài ≥4 kết thúc NUL, không xác định bảng speaker hay đầy đủ câu; trong 314 ứng viên tk100 có 217 source bắt đầu bằng newline và 23 source bắt đầu bằng khoảng trắng. Xem `docs/DIALOGUE_CANDIDATE_AUDIT.md`. **Không** coi bản nháp là văn bản đã sẵn sàng repack.
- Font Merienda V3, binary/ROM/ISO không đổi; chưa kiểm thử RPCS3. Sau commit chạy GitHub Actions trên Windows/Ubuntu (validator + unittest).
- **Tiếp theo:** `talk/en/tk101_en.bin_@000016b4` và nghiên cứu parser dựa trên byte dữ liệu local trước khi tạo repacker.

## Lượt 014 — 10/10/2026 (200 ứng viên tk101, QA xưng hô)

- Dịch 200 mục `todo → draft` của `translations/catalogs/talk/tk101_en.bin_.json`, từ `talk/en/tk101_en.bin_@000016b4` đến `talk/en/tk101_en.bin_@0000c427`. Tệp hiện 208/447 draft, còn 239 todo.
- Trọng tâm: quá khứ của Ellen và mẹ, nhà thờ và biến cố 17 năm trước, các cuộc điều tra/hỏi chuyện ở Doolin, lời người dân địa phương, Gam và Gee. Chỉ dùng `tôi/bạn` trung tính khi thật sự cần; lược chủ ngữ ở mảnh thoại thiếu speaker, không áp đặt `anh/em`, `ông/cháu`, `mày/tao` và không gán người nói từ offset.
- Giữ câu Gam/Gee tự giới thiệu và danh xưng, trạng thái cảm xúc, mẫu `$`/`(`, số newline, dấu cách đầu nguồn. 12 source trùng trong lượt và 11 source trùng tk100 được kiểm tra, 0 mâu thuẫn bản dịch; các cụm khó xác minh ghi notes riêng.
- QA: đúng 200 ID todo theo thứ tự, chỉ chỉnh vi/status/notes, giữ English/source sha256/file_offset/source_review/metadata; Unicode NFC, placeholder và newline; font Merienda V3/ROM/payload không thay. Các mảnh vẫn chưa sẵn sàng repack.
- Bổ sung chính sách xưng hô vào `docs/TRANSLATION.md`: đại từ phải theo người nói/quan hệ đã xác minh; không nhất loạt dùng một cặp cho mọi nhân vật; tiếng Ireland khẩu ngữ dịch tự nhiên nhưng không suy thân thiết; đặc biệt các fragment phải giữ draft + notes.
- Chưa chạy game; sau commit kiểm tra CI Windows/Ubuntu validator + unittest.
- **Tiếp theo:** `talk/en/tk101_en.bin_@0000c5ec` — ` / spirits in your world.`.

## Lượt 015 — 10/10/2026 (200 candidate tk101)

- Xử lý đúng 200 mục `todo→draft` từ `talk/en/tk101_en.bin_@0000c5ec` đến `talk/en/tk101_en.bin_@00017241`; tk101 đạt 408/447, còn 39 todo. Toàn dự án đạt 1.784 draft, còn 10.102 todo.
- **146/200 source trùng các bản draft đã có trong tk100 hoặc tk101**, tái sử dụng nguyên bản tiếng Việt nhằm không làm lệch xưng hô/thuật ngữ; **54 mảnh chưa từng dịch** được soạn mới và ghi notes theo vị trí. Trong những chuỗi mới: nhắc Sứ giả, vùng đất của người chết, Id, Folk, kỹ năng và các cảnh trò chuyện Doolin.
- Rà đại từ theo ngữ cảnh: khi thiếu người nói/đầu câu thì dùng câu trung tính hoặc lược đại từ, không tự gán quan hệ. Notes chỉ rõ những chỗ còn cần soát trong cảnh như Messengers, Audience Hall, Freezing Id và những tiếng lắp bắp.
- QA trước commit: chỉ vi/status/notes đổi ở đúng 200 ID; bảo toàn source/source_sha256/file_offset/source_review, số newline, ký hiệu đầu, Unicode NFC, placeholders; **0 xung đột nguồn trùng** giữa tk100/tk101. Font V3 và binary game không thay đổi.
- CMC/talk vẫn chưa có parser/repacker hoặc kiểm thử RPCS3; không được coi là bản dịch đã tích hợp. Sau commit xác minh CI Windows/Ubuntu validator và unittest.
- **Lượt 016:** tiếp `talk/en/tk101_en.bin_@000172c5` (39 mục cuối tk101), rồi theo hàng đợi catalog tiếp theo.

## Lượt 016 — 11/10/2026 (200 ứng viên hội thoại)

- Hoàn tất 39 mục cuối `tk101` (`talk/en/tk101_en.bin_@000172c5` → `@00018cab`) theo đúng bản dịch `tk100` vì nguồn trùng, đưa `tk101` lên 447/447 `draft`.
- Tiếp tục 161 mục đầu `tk102` (`talk/en/tk102_en.bin_@00001158` → `@0000987f`): **24 mục nguồn trùng** dùng bản nháp đã dịch trong các tệp/trong nhóm, **137 mục nguồn mới** dịch theo sắc thái điều tra. Tệp hiện có 161/494 draft, còn 333 todo.
- Nội dung mới: Doolin, án mạng, đồng đội cũ, bức ảnh kỷ vật, nhà thờ, biến cố 17 năm trước, thần thoại Celtic và những lời đối thoại về Cõi âm. Không gán nhân vật cho câu chỉ có fragment; dùng cách xưng hô trung tính/lược đại từ khi chưa có chứng cứ. Ghi notes riêng cho nguồn mơ hồ (`close?`, `all Faerys`, `my mother`, `The photo was of that?`).
- QA: đúng 200 mục `todo → draft`, giữ metadata, source, source_sha256, file_offset, source_review= `candidate`; Unicode NFC, số newline, token/tiền tố được giữ nguyên; kiểm tra bản dịch trùng không mâu thuẫn. Font Merienda V3 không đổi, chưa cài patch, chưa test RPCS3.
- Toàn bộ **1.984/11.886** mục có bản dịch nháp, còn **9.902** mục todo. Đây là tiến độ *dữ liệu trích xuất*, không phải ước lượng phần game đã Việt hóa chạy được. Sau commit GitHub Actions chạy validator + unittest Windows/Ubuntu.
- **Lượt 017:** `talk/en/tk102_en.bin_@00009981` (`devastated. They were close.`).

## Lượt 017 — 11/10/2026 (200 ứng viên tk102)

- Dịch **200 mục** `todo→draft` trong `translations/catalogs/talk/tk102_en.bin_.json` từ `talk/en/tk102_en.bin_@00009981` đến `@00016695`; tk102 hiện **361/494 draft**, còn 133 mục chưa dịch.
- **113 mục** tái dùng bản dịch từ chuỗi tiếng Anh trùng đã dịch trong tk100/tk101/tk102, **87 mục** lần đầu có draft. Không có nguồn trùng nhận hai bản Việt hóa khác nhau trong ba tệp.
- Chủ đề: người phụ nữ ngồi xe lăn, tín ngưỡng về linh hồn, Halflive, quán rượu Doolin, lời Gam/Gee tranh cãi, Sứ giả, hướng dẫn Folk và giáp phòng thủ. Những phần không rõ ngôi nói, thân phận hoặc tên skill (Ultimate Spear), địa danh đều được ghi chú vào `notes`. Giọng Việt tự nhiên, không áp đặt quan hệ nhân vật khi nguồn chỉ là fragment.
- QA: đúng 200 item `todo→draft`, chỉ `vi/status/notes` được sửa; bất biến ID/source/hash/offset/source_review/order, Unicode NFC, số newline, placeholder và ký hiệu đầu câu. Font Merienda V3 không đổi, chưa build binary và chưa test RPCS3.
- Tiến độ catalog trích xuất: **2.184/11.886 draft**, còn **9.702 todo**. Đây là dữ liệu nháp chưa phải phần trăm game đã chơi được bằng tiếng Việt.
- Sau commit CI Windows/Ubuntu chạy `python tools/catalog.py validate` và unittest. **Lượt 018:** `talk/en/tk102_en.bin_@0001670a` (`an end to this.`).

## Lượt 018 — 11/10/2026 (200 ứng viên hội thoại)

- Hoàn thành **133 mục cuối `tk102`** (`@0001670a` đến `@0001c28b`), tất cả nguồn trùng bản nháp `tk100`/`tk101`; tái dùng nguyên văn bản dịch để giữ xưng hô và thuật ngữ thống nhất. **`tk102` 494/494 draft, 0 todo**.
- Dịch **67 mục đầu `tk103`** (`@00001158` đến `@00004bdb`), 20 mục dùng lại nguồn/bản dịch có sẵn và 47 mảnh mới. Nội dung điều tra người chồng mất tích, nhân vật bác sĩ, chuyện người sống/người chết, thế giới Lãng quên. `tk103` hiện 67/578 draft, còn 511 todo.
- QA xưng hô: giữ `tôi` hoặc lược đại từ với mảnh lời chưa xác định speaker; chưa suy quan hệ của nữ nhân vật đang tìm chồng hoặc cách gọi `son`. Những câu cần soát như `your husband's death`, `taste then, son`, `Oblivion` đã được ghi notes; `Lãng quên` tạm dịch theo nghĩa, chưa chốt tên riêng.
- Kiểm tra chỉ thay `vi/status/notes`, ID/English/source hash/offset/metadata/order/source_review bất biến; Unicode NFC, newline, dấu `$`/`(`/`*` và bản dịch nguồn trùng. Font Merienda V3 không đổi; CMC/talk chưa repack và chưa test RPCS3.
- Tiến độ 158 catalog: **2.384/11.886 draft**, còn **9.502 todo**. Đây là độ phủ nháp của dữ liệu được trích, chưa phải tỷ lệ Việt hóa game chơi được.
- CI sau push kiểm tra validator + unittest trên Windows/Ubuntu. Lượt tiếp theo: `talk/en/tk103_en.bin_@00004c8b`.

## Lượt 019 — 11/10/2026 (200 câu/mảnh tk103)

- Dịch **200 mục `todo→draft`** từ `talk/en/tk103_en.bin_@00004c8b` đến `@0000fc9a`. `tk103` đạt **267/578 draft**, còn 311 todo. Trong lượt có **166 lượt nguồn mới** và **34 lượt dùng lại bản dịch nguồn trùng** (từ catalog trước hoặc trong lượt). Nguồn tiếng Anh trùng không có bản dịch đối nghịch.
- Chủ đề: Herve và Đầm lầy, chuyện biến mất khỏi ký ức, phóng viên và tòa soạn, Hag/vụ án 17 năm trước, người gác hải đăng, bác sĩ, Halflive, Cung điện Lãng quên, sinh vật và câu nói lắp về châu báu. Không tự gán speaker; `Herve`, `Hag`, `Faery`, `Folk` giữ nguyên danh xưng; chỗ không chắc nghĩa `will`, quyền lực của kẻ cai trị, lắp bắp/vai nói ghi notes.
- QA: 200 source ứng viên gồm **159 đoạn mở đầu newline**, **11 đoạn mở đầu dấu cách**, và **172 chuỗi tiếng Anh khác nhau**. Vì không có đủ message boundary, tất cả tiếp tục `source_review=candidate` và `status=draft`, không chốt xưng hô cuối cùng.
- Bất biến ID, English, offset, source_sha256, thứ tự catalog, source_review; chỉ vi/status/notes thay đổi. Kiểm tra NFC, số newline, ký hiệu tiền tố, placeholder và source trùng. Không sửa font Merienda V3, ISO hoặc payload.
- **Parser/repacker:** tiếp tục cần byte vùng lân cận, pointer table, opcode/speaker từ bản gốc local; catalog trên cloud chỉ chứng minh đoạn ASCII NUL, không có căn cứ vá bằng offset trực tiếp. Chưa tạo/tuyên bố có repacker hoặc patch chạy được.
- Tổng 158 catalog: **2.584 draft / 11.886**, còn **9.302 todo**. Sau commit GitHub Actions chạy validator và unittest Windows/Ubuntu. **Lượt 020** ở `talk/en/tk103_en.bin_@0000fe1a` (`in any way you like.`).

## Lượt 020 — 11/10/2026 (200 ứng viên tk103)

- Dịch nháp 200 mục `todo→draft` từ `talk/en/tk103_en.bin_@0000fe1a` đến `@0001c740`. `tk103` đạt **467/578 draft**, còn 111 `todo`. Trong 200 lượt có **161 bản dịch tái sử dụng từ các catalog trước**, **5 lần lặp của những câu mới ngay trong lượt**, và **34 chuỗi nguồn mới phân biệt** được dịch. Không có source trùng nhận hai bản `vi` khác nhau.
- Chủ đề: chiến thuật Folk (điểm yếu hệ lửa, đông băng nước, các cánh cổng), Bogle, phòng ngự, phong ấn, cung điện, `Oblivion` xuất hiện trở lại. `Oblivion` được giữ tên gốc trong bản nháp `@00019885`, vì chưa chứng minh đó là thực thể/địa danh/trạng thái; chưa quy đổi vội thành Lãng quên. Xưng hô theo nguồn rõ nghĩa, không tự đặt speaker ở những mảnh thiếu trước/sau.
- QA: 200 mục theo thứ tự, chỉ `vi/status/notes`; bất biến ID/source/offset/source_sha256/source_review/order; kiểm tra NFC, số newline, placeholder và dấu đầu, 0 bản dịch trùng nguồn mâu thuẫn. Những mục khó hiểu có notes, vẫn `candidate`/`draft`.
- Tài liệu `docs/DIALOGUE_CANDIDATE_AUDIT.md` đã bổ sung các chuỗi còn cần parser xác minh ở `tk103`, không tự tạo repacker từ JSON; công cụ `tools/catalog.py` vẫn quét ASCII NUL, chưa có bảng người nói/pointer table đủ tin cậy. Chưa thử RPCS3, không thay binary/font Merienda V3.
- Toàn 158 catalog: **2.784/11.886 bản nháp**, còn **9.102 todo**. CI sau push sẽ chạy validator và unittest Windows/Ubuntu.
- **Lượt 021:** `talk/en/tk103_en.bin_@0001c87d` (`saxophone! Yeah, saxophone.`), dịch nốt 111 mục tk103 rồi qua catalog tiếp theo.

## Lượt 021 — 11/10/2026 (200 ứng viên tk103/tk104)

- Hoàn tất **111 mục cuối `tk103`** từ `talk/en/tk103_en.bin_@0001c87d` đến `@0002141f`; cả 111 mục có nguồn trùng với các bản dịch talk trước đó, tái dùng nguyên văn để đồng bộ ngôi xưng và thuật ngữ. `tk103` đạt **578/578 `draft`**, không còn `todo`.
- Dịch **89 mục đầu `tk104`** từ `@00001158` đến `@00004e98`: 20 mục tái dùng nguồn trước, 13 mục lặp trong batch, **56 source mới phân biệt** dịch nháp; `tk104` đạt **89/731 `draft`**, còn 642 todo.
- Ngữ cảnh: nhà Harriet, vật phẩm bằng đồng thau và kỷ vật, ghi chú bí ẩn, câu chuyện người chết và Doolin, người nhìn thấy Faery, bức ảnh và những người được che chở. Câu thiếu speaker được ghi notes; các nguồn `year to live`, `bare to watch` (nghi lỗi chính tả tiếng Anh), `Anachronisms` và `acting` còn cần kiểm chứng khi ghép lời thoại hoàn chỉnh.
- QA: đúng 200 `todo→draft` ở hai tệp, chỉ thay vi/status/notes; ID/source/offset/source_sha256/source_review/order giữ nguyên; NFC, số newline, placeholders và tiền tố kỹ thuật đã soát. 0 xung đột source trùng trong các catalog tk100–104. Tất cả talk vẫn `source_review=candidate`, không phải câu đã xác minh trong game.
- Toàn 158 catalog: **2.984/11.886 mục `draft`**, còn **8.902 `todo`**. Font Merienda V3/game binary không đổi; chưa có parser/repacker talk và chưa test RPCS3. Sau push xác minh CI Windows/Ubuntu validator/unittest.
- **Tiếp lượt 022:** `talk/en/tk104_en.bin_@00004f2e` (`world, at least.`).

## Lượt 022 — 11/10/2026 (200 ứng viên tk104)

- Dịch 200 mục `todo→draft` trong `translations/catalogs/talk/tk104_en.bin_.json` từ `talk/en/tk104_en.bin_@00004f2e` đến `@000106e8`. `tk104` đạt **289/731 draft**, còn 442 todo.
- **179 source mới phân biệt** có bản nháp lần đầu, 18 lượt tái dùng bản dịch từ catalog trước và 3 lượt trùng ngay trong batch. Không có source giống nhau mà nhận hai bản `vi` khác nhau trong tk100–104.
- Nội dung: lá thư đề `31/01/1990` gửi bác sĩ Lester nhắc Cecilia; ký ức, Faery, biến đổi mặt dây chuyền, mộ đá dolmen, lối vào Lõi, nữ tư tế cổ, Thánh địa và cuộc điều tra 17 năm trước. Giữ đúng lời thư trang trọng, cảm xúc lo âu và giọng bí ẩn; không tự thêm quan hệ nhân vật khi thiếu speaker. Các địa danh/vật phẩm `Divine Sanctuary`, `Faery Prayers`, `medallion`, `dolmen` chỉ là lựa chọn thuật ngữ tạm, đã ghi `notes` cần QA.
- QA trước commit: đúng 200 ID, chỉ `vi/status/notes` thay đổi; English/source_sha256/file_offset/source_review/order và hash danh mục bất biến; Unicode NFC, số newline, placeholder, tiền tố `$`/`(`/`*` được soát. Font Merienda V3 và dữ liệu PS3 không đổi.
- Tất cả vẫn chỉ `source_review=candidate` và `status=draft`, chưa có parser/repacker thoại hay kiểm thử RPCS3. Độ phủ dữ liệu trích xuất toàn repo: **3.184/11.886 mục draft**, còn **8.702 todo** (không phải tỷ lệ bản patch playable).
- GitHub Actions sau push kiểm tra unittest và validator Windows/Ubuntu. **Lượt 023:** `talk/en/tk104_en.bin_@000108dc` (`dead. Just what's going on here?`).

## Lượt 023 — 11/10/2026 (1.151 ứng viên; thay quy định 200/lượt)

- Theo yêu cầu mới **không bắt buộc 200 mục**, đã hoàn thành **1.151 mục `todo→draft`** trong một đợt kiểm tra: 442 mục còn lại của `tk104` (`@000108dc` → `@00029a13`), toàn bộ 595 mục `tk105` (`@00001158` → `@00023717`), và 6 tệp 19 mục `tk000`, `tk011`, `tk106`, `tk107`, `tk206`, `tk207` (114 mục). Cả **8 catalog đều hiện đủ draft**.
- `tk104`: 323 mục dùng lại bản `vi` nguồn trùng đã có, 25 lần lặp nội bộ, 94 nguồn mới phân biệt. `tk105`: 47 mục tái dùng nguồn trước trong 200 mục đầu, 12 lần lặp nội bộ, 141 nguồn mới; 395 mục sau gồm 358 lần trùng với tk104/tk105 đã dịch, một lần lặp nội bộ, 36 nguồn mới. 6 tệp nhỏ có 114/114 câu điều hướng/map/nhãn trùng nguyên văn `tk100`.
- Ngữ cảnh mới: cư dân Doolin, quán rượu, tiền nhân/Thánh địa, cảnh câu đố phong ấn, bí mật về mẹ, thôi miên hồi quy, phóng viên, thành phố/cõi Địa Ngục, Tòa án và Sứ giả. Những câu bị cắt/mơ hồ như `Forebears`, `clerical duties`, `lift`, `ash tree`, `big fish in a small pond` được ghi notes; không tự gán speaker hay khóa cứng ngôi xưng.
- QA trên bản dự thảo sau khi ghép cây Git: cả 12 tệp talk hoàn chỉnh có **3.273/3.273 draft**, không có source trùng được dịch khác nhau; bảo toàn ID, source, hash, file_offset, source_review và thứ tự. Kiểm tra NFC, số newline, tiền tố `$`/`(`/`*`, token/placeholder; tất cả talk vẫn `candidate/draft`.
- Toàn bộ 158 catalog: **4.335/11.886 draft (36,5%)**, còn **7.551 todo**. Tỷ lệ này chỉ tính dữ liệu đã trích, **không phải bản vá Folklore playable**. Không có parser/repacker talk/cmc hoặc thử RPCS3; giữ nguyên Merienda V3, ISO và game binary.
- Cập nhật quy định batch lớn không có mốc cứng ở `AGENTS.md`, `docs/CLOUD.md`, `docs/TRANSLATION.md`, `docs/QUEUE.md`; tài liệu tiếp nhận được đồng bộ.
- **Tiếp theo:** `talk/en/tk200_en.bin_@00001158` (280 mục). Sau push xem GitHub Actions validator + unittest Windows/Ubuntu.

## Lượt 023a — 11/10/2026 (100 ứng viên tk200, commit nhỏ an toàn)

- Kiểm tra main trước khi làm: HEAD `8d4ff23f7672` đã hoàn tất `tk104`, `tk105`, `tk106`, `tk107`, `tk206`, `tk207`; không đụng vào các file đã dịch. Vòng chat trước bị ngắt và chưa lưu phần đang thao tác, nên dựa trên trạng thái GitHub thật.
- Dịch **100 mục `todo→draft`** đầu `translations/catalogs/talk/tk200_en.bin_.json` từ `@00001158` đến `@00006c15`: 29 mục tái dùng bản dịch của các catalog hoàn thành, 11 lần lặp nội bộ, 60 nguồn mới khác nhau. `tk200` 100/280 draft, còn 180 todo.
- Nội dung: chỉ đường tới quán rượu Doolin, những người đưa tin Halflive, lễ tưởng niệm người chết, biểu cảm tiếng cười/kêu, hướng dẫn cổng dịch chuyển/Faery. Giữ ngôi xưng trung tính ở câu khuyết đầu/vế, ghi `notes` cho `mantle`, `mother`, `soft spot`, mốc **2 tháng 11**, `Land of the Dead`, những lời lắp bắp và chữ đầu nghi mã điều khiển.
- QA: đúng 100 ID, chỉ `vi/status/notes` thay đổi; bảo toàn nguồn English, SHA-256, offset, source_review=candidate, thứ tự; Unicode NFC, số newline, prefix và khoảng trắng cuối, placeholder; không có mâu thuẫn bản Việt của source trùng giữa các catalog được rà.
- **Chính sách theo yêu cầu mới:** không cố đạt 200 hay hơn trong một lượt khi có nguy cơ crash; ưu tiên commit có kiểm tra sau mỗi khối 50–100. Parser/repacker talk chưa có; không vá ROM/binary/font Merienda V3.
- Tổng **4.435/11.886 draft**, còn **7.451 todo**. Tiếp từ `talk/en/tk200_en.bin_@00006cf8`.

## Lượt 023b — 11/10/2026 (180 mục còn lại tk200; hoàn tất catalog)

- Tiếp tục từ checkpoint GitHub `7219d5fbd100`, đúng `talk/en/tk200_en.bin_@00006cf8` đến `talk/en/tk200_en.bin_@0000f6b3`, không lặp lại 100 mục lượt 023a.
- Hoàn tất **180 mục `todo→draft`**: **167** câu/mảnh trùng nguyên nguồn đã có bản Việt tk100–105/tk200 được tái sử dụng để đồng nhất cách xưng hô/thuật ngữ; **13** mảnh mới dịch nháp, ghi notes khi ngữ cảnh thiếu. **tk200 280/280 draft, 0 todo.**
- Nội dung: đá bí ẩn, chiến đấu với Folk, Sứ giả, người chết; các câu điều tra Doolin, bác sĩ, quán rượu, thư từ và bí ẩn gia đình. Không đoán speaker, giữ dấu tiền tố/ngắt dòng/source tiếng Anh.
- QA cấu trúc trước commit: chỉ `vi/status/notes` thay đổi trong 180 mục; ID, source, SHA-256, offset, source_review, thứ tự giữ nguyên; NFC/newline/placeholder/tiền tố không thất lạc; 0 xung đột với bản Việt của nguồn trùng tk100–105. Chưa có parser/repacker dialogue hay thử RPCS3; giữ `source_review=candidate`, `status=draft` và Merienda V3 không đổi.
- Tổng **4.615/11.886 draft**, còn **7.271 todo** trong dữ liệu trích xuất; không phải tỷ lệ tiếng Việt đã tích hợp trong game.
- **Tiếp theo:** `talk/en/tk201_en.bin_@00001158` (`To Netherworld`), tệp tk201 có 496 mục todo. GitHub Actions chạy validator/unittest sau commit.

## Lượt 024a — 11/10/2026 (50 mục đầu tk201, commit an toàn)

- Sau khi hoàn tất `tk200` và xác nhận CI lượt 023b **PASS**, bắt đầu `translations/catalogs/talk/tk201_en.bin_.json`.
- Dịch **50 mục `todo→draft`** liên tiếp từ `talk/en/tk201_en.bin_@00001158` đến `talk/en/tk201_en.bin_@00003378`: **19** nhãn nguồn trùng tái sử dụng đúng bản đã thống nhất, **31** mảnh thoại mới dịch nháp. **tk201 hiện 50/496 draft, còn 446 todo**.
- Nội dung: 19 nhãn cổng/địa điểm giữ nguyên tên Doolin, Ellen, Keats, Faery, Warcadia, Cõi âm; thoại về mẹ, bạo hành gia đình, vách đá, chuyện án mạng, bác sĩ và lễ vật. Giữ cách kể u tối, không tự suy speaker từ offset. `my brother` chưa biết anh/em: bản dịch tạm đã ghi notes để rà lại, không khóa xưng hô.
- QA nội bộ: đúng 50 mục đầu, chỉ sửa vi/status/notes; ID/source/hash/offset/source_review/order bất biến, NFC/newline/dấu đầu/placeholder giữ nguyên; các nguồn trùng không mâu thuẫn. Chưa có parser/repacker và chưa test RPCS3; không đụng Merienda V3/ROM/binary.
- Toàn bộ 158 catalog: **4.665/11.886 draft**, còn **7.221 todo** (chỉ phản ánh bản nháp của dữ liệu trích).
- **Tiếp:** `talk/en/tk201_en.bin_@00003514` (`to that person while alive.`), tiếp dịch nháp theo đoạn và QA xưng hô, chạy GitHub Actions validator/unittest sau commit.

## Lượt 024b — 11/10/2026 (100 mục tk201)

- `tk201`: 100 mục liên tiếp **todo→draft** từ `talk/en/tk201_en.bin_@00003514` đến `talk/en/tk201_en.bin_@000087d1`; 2 bản trùng nguồn tái sử dụng, 98 lượt dịch nháp mới (có các mảnh lặp). Tệp đạt **150/496 draft**, còn **346 todo**. Toàn bộ 158 catalog: **4.765/11.886 draft**, **7.121 todo**.
- Các đoạn gồm cô nhi viện, ký ức từ nhỏ, hải đăng, Faery, thư từ/án mạng, mẹ và cha, người chết, câu chuyện bị bạo hành. Đa số source là fragment ASCII NUL nên không tự suy người nói hoặc quan hệ nhân vật. Đánh notes nơi đại từ hoặc nghĩa cần ráp cảnh.
- QA: chỉ vi/status/notes thay đổi, 100 ID theo đúng checkpoint; bảo toàn id/source/offset/hash/source_review/thứ tự, Unicode NFC, newline, ký hiệu đầu và placeholder; 0 xung đột khi câu nguồn trùng. Chưa có parser/repacker talk/cmc, chưa thử RPCS3, giữ Merienda V3/ROM/payload nguyên.
- **Tiếp theo:** `talk/en/tk201_en.bin_@0000884d` (`every thing we see in our dreams?`). GitHub Actions validator/unittest được kích hoạt qua commit.

## Lượt 024c — 11/10/2026 (100 mục tiếp tk201)

- `tk201`: dịch thêm **100 todo→draft**, từ `talk/en/tk201_en.bin_@0000884d` đến `talk/en/tk201_en.bin_@0000eca9`: **29** nguồn trùng catalog trước, **7** lặp nguồn trong lô, **64** mảnh mới khác nhau. `tk201` đạt **250/496 draft, 246 todo**. Toàn bộ 158 catalog đạt **4.865/11.886 draft**, còn **7.021 todo**.
- Nội dung: điều tra ở nhà thờ, dân làng/nhà nghiên cứu, người sống và người chết, gia đình, quán rượu, Gam/Gee, Sứ giả, hướng dẫn Faery và Folk. Giữ nguyên tên riêng đã thống nhất, không tự gán speaker/quan hệ.
- QA đúng vùng 100 ID, chỉ thay vi/status/notes; giữ source/ID/SHA/offset/source_review/order, NFC, newline, dấu đầu, placeholder và nguồn trùng đồng nhất. Những mảnh lược chủ ngữ và ngôi xưng nghi vấn đã ghi notes. Tất cả vẫn candidate/draft, không có parser/repacker hay test RPCS3; font Merienda V3, ROM/binary không đổi.
- **Tiếp:** `talk/en/tk201_en.bin_@0000ed26` (`Many different tricks to try!`) và phần còn lại của `tk201`. CI validator/unittest chạy trên GitHub Actions sau commit.

## Lượt 024d — 11/10/2026 (100 mảnh tk201, Folk/Faery/Cõi âm)

- Dịch tiếp `tk201` **100 todo→draft** từ `talk/en/tk201_en.bin_@0000ed26` đến `talk/en/tk201_en.bin_@000147df`: 33 mục tái dùng source cũ, 5 mục lặp trong lượt, 62 source mới. `tk201` đạt **350/496 draft**, còn **146 todo**. Tổng repo **4.965/11.886 draft**, còn **6.921 todo**.
- Nội dung: Sứ giả, khả năng Folk, chiến đấu theo hệ, Land of the Dead, ký ức, Mnemosyne, Oblivion (tên riêng tạm giữ) và Đại sảnh Tiếp kiến (Audience Hall, thuật ngữ tạm). Chỗ thiếu speaker/ngữ cảnh hoặc điều kiện phủ định cần xác minh có notes. Không áp đặt vai nhân vật theo offset.
- QA vùng đúng 100 ID, chỉ vi/status/notes thay đổi, id/source/source_sha256/offset/source_review/order bất biến; Unicode NFC, newline, ký tự đầu, placeholder và nguồn trùng không xung đột. Chưa có parser/repacker thoại, chưa thử RPCS3 và không đụng font Merienda V3, ISO/ROM/payload.
- **Tiếp theo:** `talk/en/tk201_en.bin_@00014b1b`; 146 mục cuối tk201 phần lớn nguồn trùng đã có bản dịch chuẩn từ tk200/tk100–105. CI validator/unittest sau commit.

## Lượt 024e — 11/10/2026 (hoàn tất 146 mục cuối tk201)

- Hoàn tất **146 todo→draft** trong `tk201`, từ `talk/en/tk201_en.bin_@00014b1b` đến `talk/en/tk201_en.bin_@0001b26b`: **146/146** source trùng hoàn toàn với bản dịch đã xác nhận nhất quán ở tk100–105, tk200 hoặc phần đầu tk201, đồng bộ nguyên văn, không viết lại làm lệch xưng hô. `tk201` đạt **496/496 draft**, còn 0 todo.
- Tổng toàn repo **5.111/11.886 draft**, còn **6.775 todo** của 158 catalog. Chỉ tính độ phủ bản nháp ứng viên trích xuất, không có nghĩa đã có patch hội thoại playable.
- QA trên 146 dòng cuối: id, source, sha256, file_offset, source_review, thứ tự giữ nguyên; chỉ vi/status/notes, Unicode NFC/newline/marker/placeholder; không source trùng được dịch mâu thuẫn. Không sửa Merienda V3, binary, ROM/ISO; talk/cmc chưa có parser/repacker và chưa thử RPCS3.
- **Lượt tiếp theo:** `talk/en/tk202_en.bin_@00001158` (`To Netherworld`); `tk202` có 518 todo. Ưu tiên xử lý source trùng trước, dịch các fragment mới theo ngữ cảnh, không tự gán speaker.
- Commit kích hoạt validator và unittest trên GitHub Actions Windows/Linux.

## Lượt 025a — 11/10/2026 (100 mục đầu tk202)

- Từ `talk/en/tk202_en.bin_@00001158` đến `talk/en/tk202_en.bin_@00006960`: dịch **100 mục todo→draft** (30 nguồn trùng tái dùng bản dịch, 70 mảnh mới); `tk202` hiện **100/518 draft**, còn 418 todo.
- Nội dung: ảnh bị xé, chuyện án mạng, quá khứ và phòng khám nhà thờ Doolin, Faery và cuộc xung đột các cõi. Không tự suy người nói/quan hệ từ offset; các fragment chỉ dịch phần ý chắc chắn, ghi notes.
- QA cục bộ: 100 ID đúng checkpoint, chỉ vi/status/notes được sửa, source/source_sha256/file_offset/source_review/order bất biến; NFC, ngắt dòng, tiền tố và placeholder không mất; nguồn trùng không mâu thuẫn. Chưa đóng gói talk/cmc, chưa test RPCS3, không sửa font Merienda V3 hoặc ROM/binary.
- Toàn bộ 158 catalog **5.211/11.886 draft, 6.675 todo**, chỉ là độ phủ dữ liệu trích xuất, không phải bản vá tiếng Việt playable.
- **Tiếp theo:** `talk/en/tk202_en.bin_@00006a5b` (`17 years ago.`); GitHub Actions chạy validator và unittest sau commit.

## Lượt 025b — 11/10/2026 (100 mục tiếp tk202)

- Dịch thêm `tk202` **100 todo→draft** từ `talk/en/tk202_en.bin_@00006a5b` đến `talk/en/tk202_en.bin_@0000d043`: 4 nguồn trùng catalog trước, 10 mảnh trùng nội bộ và 86 nguồn mới. `tk202` đạt **200/518 draft**, còn **318 todo**.
- Ngữ cảnh: 17 năm trước, vụ án ảnh xé và phòng khám Doolin, Cõi âm, quân lính, mẹ và quá khứ, truyền thuyết, nhà thờ, người gác hải đăng, lời đồn/dịch vụ của dân làng. Ghi chú ở các fragment có phụ thuộc ngôi xưng, thành ngữ và đối thoại chưa xác định speaker.
- QA cấu trúc: đúng 100 ID, chỉ vi/status/notes thay đổi; bất biến tiếng Anh/offset/source hash/source_review/order; NFC, số newline, prefix và placeholder, 0 nguồn trùng có hai bản dịch khác. Tất cả vẫn candidate/draft. Không đụng Merienda V3, game binary, ROM/ISO; talk/cmc chưa repack/test RPCS3.
- Tổng **5.311/11.886 draft**, còn **6.575 todo** trong dữ liệu trích xuất.
- **Tiếp theo:** `talk/en/tk202_en.bin_@0000d0d1`; GitHub Actions chạy validator/unittest sau commit.

## Lượt 025c — 11/10/2026 (hoàn tất 318 mục cuối tk202)

- Dịch **318 mục todo→draft** từ `talk/en/tk202_en.bin_@0000d0d1` đến `talk/en/tk202_en.bin_@0001daaf`; **273** nguồn trùng bản đã dịch (giữ nguyên từng chữ), **45** source mới dịch nháp có ghi chú khi ngữ cảnh thiếu. Rà cấu trúc theo sáu nhóm ~50. `tk202` đạt **518/518 draft**, còn 0 todo.
- Bối cảnh: Doolin, người chết, Sứ giả, vũ khí cổ, Lính Máy (tạm), lính máy hệ Sét, pháo đài, ký ức, hy sinh. Những từ máy/giáp/bình chứa, ngôi xưng, mảnh câu thiếu chủ ngữ được giữ draft+notes, không suy speaker.
- QA: chỉ sửa vi/status/notes của đúng 318 mục; English/source SHA/offset/source_review/order và mọi trường khác giữ nguyên; Unicode NFC, newline, mã đầu, placeholders, nguồn trùng không xung đột. Chưa có parser/repacker talk/cmc hoặc kiểm tra runtime RPCS3, không thay Merienda V3 hay binary/ROM/ISO.
- Tổng repo 158 catalog: **5.629/11.886 draft**, còn **6.257 todo**. Đây chỉ là độ phủ ứng viên text, không phải phần trăm patch đã chạy được.
- **Tiếp theo:** `talk/en/tk203_en.bin_@00001158` (`To Netherworld`), catalog tk203 có 663 mục. Bắt đầu theo nguồn trùng trước, sau đó mới dịch fragment mới; không có giới hạn cứng lô nhưng QA theo cảnh và commit vừa sức.
- GitHub Actions trên Windows/Linux chạy validator + unittest khi push.

## Lượt 026a — 11/10/2026 (100 ứng viên đầu tk203)

- Từ `talk/en/tk203_en.bin_@00001158` đến `talk/en/tk203_en.bin_@00005e10`: dịch **100 todo→draft**, gồm 20 câu trùng nguồn các catalog đã dịch được tái sử dụng nguyên văn và 80 mảnh mới; `tk203` **100/663 draft, còn 563 todo**.
- Ngữ cảnh: mật khẩu, người gác hải đăng, hồ sơ cái chết, nhà thờ và ký ức tập thể; Cõi âm và Oblivion. Chỉ dịch nghĩa có thể xác minh; tiền tố/nội dung thiếu speaker ghi notes, không ép anh-em, ông-cháu hoặc quan hệ người nói.
- QA trước commit: chỉ `vi/status/notes` được sửa ở 100 ID; source/hash/offset/source_review/order bất biến, Unicode NFC, newline, prefix và placeholders giữ nguyên; 0 source trùng mâu thuẫn. Chưa có parser/repacker talk/cmc hay thử hiển thị RPCS3; giữ Merienda V3/ROM/binary nguyên.
- Toàn bộ 158 catalog **5.729/11.886 draft**, còn **6.157 todo**. Đây là độ phủ nháp dữ liệu trích, không phải tỉ lệ playable.
- **Tiếp:** `talk/en/tk203_en.bin_@00005f9e` (`correct that aberration.`). CI Windows/Linux chạy validate + unittest sau commit.

## Lượt 026b — 11/10/2026 (100 mục tiếp theo tk203)

- Dịch 100 mục từ `talk/en/tk203_en.bin_@00005f9e` đến `talk/en/tk203_en.bin_@0000cb79`: 3 bản trùng nguồn catalog trước, 8 mảnh lặp nội bộ, 89 chuỗi tiếng Anh mới. `tk203` đạt **200/663 draft**, còn 463 todo.
- Chủ đề: Herve/Đầm lầy, phong ấn ngọn hải đăng, ký ức và linh hồn, hiện tượng Oblivion, các báo cáo nhân chứng và bí ẩn 17 năm ở Doolin. Các cụm như Eternal Suffering và cách gọi thế giới bên kia vẫn là nháp, cần kiểm tra scene/speaker khi có parser.
- QA: chỉ vi/status/notes tại 100 ID; bất biến ID, nguồn, source_sha256, file_offset, source_review, order, mã mở đầu/newline/placeholder/NFC. 0 xung đột nguồn trùng; không thay Merienda V3/ROM/binary. Talk/cmc chưa có parser/repacker hoặc test RPCS3.
- Tổng 158 catalog **5.829/11.886 draft**, còn **6.057 todo**. Không phải độ phủ bản patch chơi được.
- **Tiếp theo:** `talk/en/tk203_en.bin_@0000cccf` (`And for what reason?`). CI validator/unittest sau commit.

## Lượt 026c — 11/10/2026 (200 mục tk203: Doolin và Banshee)

- Từ `talk/en/tk203_en.bin_@0000cccf` đến `talk/en/tk203_en.bin_@000186a8` dịch **200 todo→draft** theo 4 nhóm QA: 130 nguồn trùng đã dịch, 12 nguồn trùng trong lô và 58 nguồn mới khác nhau. `tk203` đạt **400/663 draft**, còn **263 todo**.
- Ngữ cảnh: bác sĩ phá sản, điều tra người chết, vách đá, Banshee, điềm báo và bài hát, nhiệm vụ ở Doolin, hình bóng người chết và ký ức. Không gán speaker theo offset và chưa chốt đại từ dựa vào mảnh câu. Ghi notes cho các chỗ bị cắt hay thuật ngữ/giới tính chưa chắc.
- QA: chỉ vi/status/notes thay đổi ở 200 ID; English/source SHA/offset/source_review và thứ tự bất biến; NFC, newline, mã dẫn, ký tự kết thúc khoảng trắng, token và bản dịch nguồn trùng nhất quán. Tất cả candidate/draft; chưa có parser/repacker thoại hoặc kiểm tra RPCS3, giữ Merienda V3 và binary nguyên.
- Tổng 158 catalog: **6.029/11.886 draft**, còn **5.857 todo** của dữ liệu trích xuất, chưa phải phần trăm Việt hóa playable.
- **Tiếp theo:** `talk/en/tk203_en.bin_@00018773`; còn 263 mục tk203, trong đó nhiều nguồn trùng tk202/tk201. GitHub Actions validator + unittest được kích hoạt sau commit.

## Lượt 026d — 11/10/2026 (hoàn tất 263 mục tk203)

- Hoàn tất **263 mục todo→draft** từ `talk/en/tk203_en.bin_@00018773` đến `talk/en/tk203_en.bin_@00025ffb`, QA theo sáu lô. Trong đó **196 nguồn trùng** đã có bản Việt ở tk100–202/tk203, **1 nguồn trùng** ngay trong lượt và **66 mảnh nguồn mới** được dịch nháp. `tk203` hoàn tất **663/663 draft, 0 todo**.
- Nội dung: Cu Sidhe, cơ chế chiến đấu và vật phẩm, Oblivion, Cõi âm, chuyện ký ức người chết, người mẹ giả mạo, phòng khám và nhà thờ 17 năm trước. Dùng đại từ trung tính, ghi notes khi mảnh bị cắt hoặc cần soát bối cảnh; chưa tự xác minh người nói.
- QA: chỉ vi/status/notes thay đổi đúng 263 mục; giữ nguyên ID, tiếng Anh, source_sha256, offset, source_review và thứ tự. Đảm bảo NFC, số newline, tiền tố/trailing blank, protected tokens, đồng bộ tuyệt đối source trùng. Không thay font Merienda V3, ROM/ISO/binary và chưa test RPCS3. Dialogue vẫn thiếu parser/repacker.
- Toàn bộ 158 catalog: **6.292/11.886 draft (52,9%)**, còn **5.594 todo** trong dữ liệu trích xuất; đây không phải tỷ lệ bản vá playable.
- **Tiếp theo:** `talk/en/tk204_en.bin_@00001158` (`To Netherworld`); tk204 có 823 mục. Dùng lại nguồn trùng và dịch source mới theo cảnh; luôn lưu/QA theo batch an toàn.
- GitHub Actions validator và unittest Windows/Linux chạy sau khi push.

## Lượt 027a — 11/10/2026 (100 mục đầu tk204)

- Kiểm tra HEAD `f97ce76f11b7` và CI lượt tk203 PASS. Dịch `tk204` **100 todo→draft** từ `talk/en/tk204_en.bin_@00001158` đến `talk/en/tk204_en.bin_@00006642`: 24 nguồn trùng được tái sử dụng, 76 mảnh mới được dịch nháp, có ghi chú những câu chưa rõ người nói.
- Nội dung: Faery, điều ước và thế giới bên kia, ý thức/tâm thức, truyền thuyết ngôi làng, vụ sát hại thứ ba và những cuộc tìm kiếm. Giữ tên riêng, thuật ngữ và sắc thái kỳ bí; không tự gán quan hệ qua các fragment.
- QA: chỉ vi/status/notes đổi đúng 100 mục; ID, English, source hash, offset, source_review, order bất biến; NFC, newline, prefix, placeholders và duplicate source được soát. Chưa có parser/repacker thoại hoặc test RPCS3; không đụng font Merienda V3/ROM/ISO/binary.
- Tổng repo **6.392/11.886 draft**, còn **5.494 todo** (độ phủ bản nháp của dữ liệu trích).
- **Tiếp theo:** `talk/en/tk204_en.bin_@000066b3`; tiếp tục theo cảnh với QA/commit từng phần, CI Windows/Linux validator + unittest chạy sau push.

## Lượt 027b — 11/10/2026 (100 mục tiếp tk204)

- Dịch **100 ứng viên todo→draft** từ `talk/en/tk204_en.bin_@000066b3` đến `talk/en/tk204_en.bin_@0000c3b0`: 4 mảnh tái dùng nguồn trùng, 96 mảnh mới có ghi chú khi chưa rõ chủ thể. `tk204` đạt **200/823 draft**, còn **623 todo**.
- Nội dung: mộ đá Doolin, cái chết và ký ức, nỗi sợ, tự do ý chí và quan hệ giữa con người với Sứ giả. Tránh áp đặt đại từ vào fragment chưa xác minh; ưu tiên giọng nghiêm trang/u tối, thoại ngắn không cộc.
- QA: đúng 100 ID theo checkpoint; chỉ vi/status/notes, giữ ID/source/source_sha256/file_offset/source_review/order, NFC, newline, tiền tố và placeholders, không xung đột bản dịch nguồn trùng. Vẫn draft/candidate chưa có parser/repacker talk/cmc hoặc QA runtime RPCS3. Không thay Merienda V3/ROM/ISO/binary.
- Tổng 158 catalog **6.492/11.886 draft**, còn **5.394 todo** của nguồn đã trích. **Tiếp:** `talk/en/tk204_en.bin_@0000c430`. GitHub Actions Windows/Linux sẽ chạy validator/unittest sau commit.

## Lượt 027c — 11/10/2026 (100 mục tk204, mạch vách đá và ký ức)

- Từ `talk/en/tk204_en.bin_@0000c430` đến `talk/en/tk204_en.bin_@00011c5d`: **100 todo→draft**, gồm 4 nguồn trùng từ trước, 2 lần trùng trong batch và 94 mảnh mới. `tk204` đạt **300/823 draft**, còn 523 todo.
- Chủ đề: cô gái mất tích, vách đá, mộ đá Doolin, bất hòa giữa ký ức/quá khứ và thực tại, tuyệt vọng, nghi vấn án mạng 17 năm trước. Các câu cắt mảnh, đại từ và chỉ dẫn cơ chế chưa rõ được ghi notes thay vì xác nhận sai.
- QA: 100 ID đúng, chỉ sửa vi/status/notes; giữ source/ID/SHA/offset/source_review/order, Unicode NFC, newline, prefix, placeholders và source trùng nhất quán. Chưa có parser/repacker talk/cmc, chưa thử RPCS3; giữ nguyên Merienda V3/ROM/ISO/binary.
- Tổng dự án **6.592/11.886 draft**, còn **5.294 todo**. **Tiếp theo:** `talk/en/tk204_en.bin_@00011de6`. CI Windows/Linux validator/unittest sau push.

## Lượt 027d — 11/10/2026 (100 mục tk204, Sidhe và dân làng)

- Từ `talk/en/tk204_en.bin_@00011de6` đến `talk/en/tk204_en.bin_@00017ea4` xử lý **100 todo→draft**: 23 source trùng đã dịch từ các catalog/batch trước, 9 lần trùng nội bộ và 68 source mới. Tệp `tk204` hiện **400/823 draft**, còn 423 todo.
- Nội dung: truyền thuyết Sidhe/Faery, bài hát dân gian, ký ức 17 năm, người dân Doolin, các đoạn lời nói trong quán rượu. Không suy speaker hay mối quan hệ trong fragment; các đoạn mơ hồ ghi notes.
- QA: chỉ vi/status/notes ở đúng 100 ID thay đổi, source/hash/offset/source_review/order bất biến; Unicode NFC, newline, ký hiệu đầu, placeholder, bản dịch cùng source nhất quán. Vẫn draft/candidate, chưa có parser/repacker hay kiểm thử RPCS3, Merienda V3/ROM/ISO/binary không thay.
- Toàn repo **6.692/11.886 draft**, còn **5.194 todo**. **Tiếp theo:** `talk/en/tk204_en.bin_@0001813a`; validator/unittest chạy sau commit.

## Lượt 027e — 11/10/2026 (hoàn tất 423 mục cuối tk204)

- Từ `talk/en/tk204_en.bin_@0001813a` đến `talk/en/tk204_en.bin_@0002f8f7`, xử lý **423 todo→draft** theo 9 khối QA: **383** nguồn trùng đã có bản Việt ở tk100–203/tk204, **2** mục lặp trong lượt, **38** nguồn mới dịch nháp. **tk204 hoàn tất 823/823 draft, 0 todo**.
- Chủ đề: hướng dẫn/điều kiện nhiệm vụ, khóa I/II, đồng hồ, các cõi, Faery, người chết, nữ tư tế và nguồn hồi ức. Cụm gốc `Achilles' heal` có khả năng sai chính tả (`heel`), tạm dùng `gót chân Achilles` và ghi notes, không tự sửa nguồn.
- QA nội bộ: chỉ `vi/status/notes` của đúng 423 ID thay đổi; giữ nguyên English/source_sha256/file_offset/source_review/order, Unicode NFC, newline, leading prefix và placeholders; mọi nguồn trùng khớp bản Việt cũ. Không suy đoán người nói hay đánh dấu reviewed/tested.
- Tổng 158 catalog **7.115/11.886 draft**, **4.771 todo** (chỉ là ứng viên đã trích; chưa phải phần trăm game đã playable bằng tiếng Việt).
- Chưa có parser/repacker thoại/cmc, chưa test RPCS3; Merienda V3, ISO/ROM/binary không thay đổi. CI Windows/Linux validator+unittest chạy sau push.
- **Tiếp theo:** `talk/en/tk205_en.bin_@00001158` (`To Netherworld`), tk205 có 653 mục; đối chiếu nguồn trùng rồi tiếp tục phần mới theo bối cảnh.

## Lượt 028a — 11/10/2026 (100 mục đầu tk205)

- Đối chiếu HEAD và checkpoint mới nhất: tk203/tk204 đã hoàn tất, CI 2619056d PASS; bắt đầu `tk205`, không lặp việc cũ.
- Dịch 100 mục `todo→draft` từ `talk/en/tk205_en.bin_@00001158` đến `talk/en/tk205_en.bin_@000071eb`: **21** bản nguồn trùng tái sử dụng, **79** mảnh mới dịch nháp. `tk205` đạt **100/653 draft**, còn 553 todo.
- Nội dung: Doolin 17 năm trước, ký ức tuổi thơ, Faery, lời cầu nguyện, người chỉ còn một năm để sống, băng hình, tỉnh dậy và thương tích. `Handy Video` giữ nguyên làm tên tạm vì chưa có hình; các câu cắt mảnh có notes.
- QA đúng 100 ID, chỉ vi/status/notes thay đổi, ID/source/sha256/offset/source_review/order giữ nguyên; NFC, số newline, marker, placeholder và nguồn trùng nhất quán. Chưa có parser/repacker talk/cmc, chưa thử RPCS3; giữ Merienda V3/ROM/binary nguyên.
- Toàn repo **7.215/11.886 draft, 4.671 todo** (độ phủ nháp ứng viên, chưa phải phần trăm patch chơi được).
- **Tiếp theo:** `talk/en/tk205_en.bin_@000072f6` (`Things worked out for the best.`); CI validator/unittest sau commit.

## Lượt 028b — 11/10/2026 (100 ứng viên tiếp tk205)

- Từ `talk/en/tk205_en.bin_@000072f6` đến `talk/en/tk205_en.bin_@0000d759` dịch tiếp **100 todo→draft**: 16 bản đã dịch ở catalog trước, 10 bản lặp trong batch, 74 mảnh nguồn mới. `tk205` đạt **200/653 draft, còn 453 todo**.
- Chủ đề: ngọn hải đăng và mũi đất, gia đình và tuổi thơ, cuộc sống ở Doolin, nỗi sợ và những sinh vật Faery; nhóm câu trùng liên quan hướng dẫn và hồi phục máu. Ghi notes về quan hệ/speaker chưa thể xác minh; giữ khẩu khí tự nhiên mà không thêm tình tiết.
- QA: chỉ vi/status/notes của đúng 100 ID; source/sha256/offset/source_review/order không thay, NFC, newline, prefix, placeholder và nguồn lặp nhất quán. Mọi entry vẫn candidate/draft; chưa có parser/repacker talk/cmc hay QA RPCS3; Merienda V3/ROM/binary không đổi.
- Tổng 158 catalog: **7.315/11.886 draft**, còn **4.571 todo** (độ phủ ứng viên, chưa phải patch playable).
- **Tiếp:** `talk/en/tk205_en.bin_@0000d7d9` (`no matter how hard they're hit...`). CI GitHub Actions validator/unittest sau commit.

## Lượt 028c — 11/10/2026 (hoàn tất 453 mục cuối tk205)

- Từ `talk/en/tk205_en.bin_@0000d7d9` đến `talk/en/tk205_en.bin_@00026cc3` xử lý **453 todo→draft** theo chín nhóm QA: **413** nguồn trùng nguyên bản đã dịch ở các catalog trước và **40** mảnh nguồn mới dịch nháp. **tk205 hoàn tất 653/653 draft**, 0 todo.
- Nội dung bổ sung: hướng dẫn quái Folk/địa điểm, Cõi Địa Ngục, tội lỗi, phán xét, thang máy, y phục, những câu đùa/faery và các hội thoại tái sử dụng từ những vùng trước. Giữ nguồn trùng giống hệt; không tự gán speaker. Những từ `clerical duties` và ngữ cảnh phòng xử án có notes cần xác minh, giữ bản dịch nguồn trùng từ catalog trước thay vì tự chỉnh lệch.
- QA dữ liệu: chỉ `vi/status/notes` sửa ở 453 ID; source/SHA-256/offset/source_review/order bất biến, Unicode NFC, số newline, dấu đầu, placeholder, 0 xung đột giữa nguồn trùng; các mục đều `candidate/draft`, không đánh dấu reviewed/tested.
- Tổng **7.768/11.886 draft, còn 4.118 todo** trên 158 catalog nguồn trích, không phải phần trăm bản vá playable. Chưa parser/repacker talk/cmc, chưa test RPCS3; Merienda V3, ROM/ISO, binary không thay đổi.
- `tk206` và `tk207` đã hoàn tất sẵn; **tiếp theo:** `talk/en/tk306_en.bin_@00001158` của `tk306` (244 todo). CI GitHub Actions sẽ chạy validator/unittest sau khi push.

## Lượt 029 — 11/10/2026 (hoàn tất 244 mục tk306)

- Tiếp đúng checkpoint sau tk205: `tk206` và `tk207` đều đã được dịch nháp trước đó, nên làm `tk306`. Dịch **244 todo→draft**, từ `talk/en/tk306_en.bin_@00001158` đến `talk/en/tk306_en.bin_@0000c45f`: **184** mục nguồn trùng khớp với bản dịch tk204–205/các lượt trước, **60** lượt mảnh mới (có các lần lặp cùng nguồn) được soạn nháp.
- Mạch: Doolin thời quá khứ, người bạn vẽ tranh, ký ức tuổi nhỏ, người thân và nhà thờ, thương tích/vách đá, nỗi sợ và hướng dẫn chiến đấu. Không tự xác định speaker từ offset; những mảnh mơ hồ ghi notes.
- QA theo nhóm: chỉ `vi/status/notes` của 244 ID được sửa; id, source/source_sha256, offset, source_review, thứ tự giữ nguyên; NFC, newline, mã đầu/placeholder, 0 xung đột khi bản nguồn lặp. Tệp `tk306` **244/244 draft**. Chưa parser/repacker talk/cmc, chưa test RPCS3 hoặc sửa font Merienda V3/ROM/ISO/binary.
- Toàn repo **8.012/11.886 draft**, còn **3.874 todo**; chỉ phản ánh độ phủ nháp nguồn trích, không phải tỷ lệ bản vá chơi được.
- **Tiếp theo:** `talk/en/tk307_en.bin_@00001158` (nguồn `To Netherworld`), tk307 có 811 mục; CI GitHub Actions validator/unittest sau commit.

## Lượt 030a — 11/10/2026 (100 mục đầu tk307)

- Tiếp theo HEAD `3f4f5aeaa5b7`, không dịch lại tk204–206/tk306. Từ `talk/en/tk307_en.bin_@00001158` đến `talk/en/tk307_en.bin_@00005ecf`: chuyển **100 todo→draft**, gồm 21 mục trùng nguồn cũ và 79 câu/mảnh mới. `tk307` đạt **100/811 draft**, còn 711 todo.
- Nhóm nội dung: ký ức quá khứ, người mẹ/con, bí mật bác sĩ Doolin, Herve và Faery. `Pre-rendered movie 4` và `Play Movie 23` có thể là nhãn nội bộ, vẫn draft và notes; không xác minh được speaker/quan hệ từ mảnh ASCII.
- QA nội bộ: đúng 100 ID, chỉ vi/status/notes thay đổi; ID, source, SHA-256, file_offset, source_review, thứ tự, NFC, số newline, tiền tố điều khiển và placeholder giữ nguyên. Không sửa Merienda V3/ISO/ROM/binary; chưa parser/repacker và chưa test RPCS3.
- Tổng 158 catalog **8.112/11.886 draft**, còn **3.774 todo** của dữ liệu trích (không phải tỷ lệ bản vá chơi được).
- **Tiếp theo:** `talk/en/tk307_en.bin_@0000605c`; validator + unittest chạy qua GitHub Actions sau push.

## Lượt 030b — 11/10/2026 (100 ứng viên tiếp tk307)

- Đọc lại HEAD và `AGENTS.md`, xử lý đúng **100 todo→draft** từ `talk/en/tk307_en.bin_@0000605c` đến `talk/en/tk307_en.bin_@0000a821`, giữ `tk307` ở **200/811 draft**, còn **611 todo**. Ba nguồn trùng nội bộ tk307 được giữ nguyên bản dịch.
- Nội dung: kẻ bị truy đuổi, trùm Lõi Cõi âm, lời từ biệt, ký ức, người mẹ đã mất, hung thủ, cuộc trở về Doolin. Nhãn `(Play Mov...)`/`NETHERWORLD CORE BOSS` là candidate kỹ thuật chưa chứng minh sẽ hiển thị; giữ tiền tố và ghi notes.
- QA trước push: đúng 100 ID; chỉ thay `vi/status/notes`, giữ nguồn/hash/offset/source_review/order, NFC, newline, tiền tố `$`, `* `, khoảng trắng và placeholder; đối chiếu source trùng không xung đột. Chưa có parser/repacker hay thử RPCS3; không sửa Merienda V3 hoặc payload.
- Tổng **8.212/11.886 draft**, còn **3.674 todo** trong 158 catalog ứng viên, không phải tỷ lệ bản vá playable.
- **Tiếp theo:** `talk/en/tk307_en.bin_@0000a8a7` (mục 201, `hardly failures of yours.`). Xác minh GitHub Actions validator/unittest Windows/Ubuntu sau commit.

## Lượt 030c — 11/10/2026 (100 ứng viên tiếp tk307)

- Từ `talk/en/tk307_en.bin_@0000a8a7` đến `talk/en/tk307_en.bin_@0000fbbc`, chuyển **100 todo→draft**; `tk307` đạt **300/811 draft**, còn 511 todo. Rà 2 source trùng tk101/tk204 và các nguồn lặp trong batch; dùng bản Việt trùng khớp.
- Nội dung: tiễn biệt người mẹ, lễ tang, câu chuyện gia đình, hung thủ và cuộc điều tra, dân làng sau biến cố, lời hẹn gặp lại, Cõi âm, niềm tin và các ký ức. Nhiều candidate bị cắt mảnh; ghi notes, chưa gán speaker/quan hệ.
- QA dữ liệu: chỉ sửa `vi/status/notes` cho 100 ID, bất biến English, ID, SHA, offset, source_review, order; NFC/newline/marker/placeholder và source trùng trong tk307 đều hợp lệ. Giữ nguyên font Merienda V3, game binary, trạng thái draft (chưa test RPCS3/repacker).
- Tổng **8.312/11.886 draft**, **3.574 todo** trong 158 catalog ứng viên, không tương đương game đã playable bằng tiếng Việt.
- **Tiếp theo:** `talk/en/tk307_en.bin_@0000fc5d` (mục 301, `strife, unite them with nature!`), đã đối chiếu source và offset. GitHub Actions validator + unittest cần kiểm tra kết quả sau push.

## Lượt 030d — 11/10/2026 (hoàn tất 511 mục cuối tk307)

- Từ `talk/en/tk307_en.bin_@0000fc5d` đến `talk/en/tk307_en.bin_@0002bea7`, chuyển **511 todo→draft** trong 5 commit riêng (100 + 100 + 100 + 100 + 111). `tk307` hoàn tất **811/811 draft, 0 todo**.
- Gồm **442** mục khớp nguồn đã có bản dịch ở các catalog trước, **7** lượt trùng ngay trong batch, **62** nguồn mới được dịch nháp. Phần mới chủ yếu ở các hướng dẫn Faery, sinh vật, bản thể gốc, giáp, thuộc tính tương khắc, Cõi âm, vô thức tập thể và các mảnh hướng dẫn có tiền tố đặc biệt. Chỗ thiếu chủ ngữ hoặc ngữ cảnh đã ghi `notes`.
- QA từng commit: chỉ `vi/status/notes` được đổi, English, ID, SHA nguồn, offset, source_review, thứ tự bất biến; NFC/newline/tiền tố/placeholder và nguồn trùng không xung đột. Không thay font Merienda V3, payload, ROM, ISO hoặc metadata nhị phân; không đánh dấu reviewed/tested.
- Tổng 158 catalog **8.823/11.886 draft**, còn **3.063 todo** (chỉ là độ phủ nháp nguồn trích, chưa phản ánh patch playable). Parser/repacker talk/cmc và kiểm tra trên RPCS3 vẫn còn thiếu.
- **Tiếp theo:** `talk/en/tk500_en.bin_@00001158`, có 528 todo; `tk600` có 544 todo và `tk700` 242 todo. Các tệp CMC chưa hoàn thành còn lại vẫn cần rà sau nhóm talk. Không suy CI PASS nếu chưa có kết quả xác minh trên GitHub Actions.

## Lượt 031 — 11/10/2026 (hoàn tất 528 mục tk500)

- Tiếp đúng `tk500` từ `talk/en/tk500_en.bin_@00001158` (`To Netherworld`) đến `talk/en/tk500_en.bin_@0001a237` (`I have no business this way.`). Chuyển **528 todo→draft** qua 6 commit riêng (100 + 100 + 100 + 100 + 100 + 28); **tk500 528/528 draft, 0 todo**. Tái dùng **29** nguồn đã dịch, **5** mục lặp nội bộ và dịch **494** nguồn mới.
- Ngữ cảnh: người cha và cậu bé, tạp chí UNKNOWN REALMS, quán rượu Doolin, linh hồn/hội thoại nhiệm vụ, sự biến mất của trẻ em, tình cảm Faery, truyền thuyết chiến binh cổ, Ellen, và phân đoạn truyện cổ trong cuốn sách của cậu bé (châm biếm mô-típ Chén Thánh). Giữ tên riêng như Frizzie, Ethersword, Oblivion và mã ngoặc vuông `[Truffid]`, `[Rannunculus]`. Các fragment chưa rõ chủ thể/vai nói có notes để rà sau.
- QA từng batch: chỉ sửa `vi/status/notes` của ứng viên mới, thêm **2 chỉnh sửa từ vựng** tại mục 61 và 473; ID/source/SHA/offset/source_review/thứ tự bất biến; Unicode NFC, newline, prefix `$`, `(`, space và các placeholder được soát, không có nguồn trùng mâu thuẫn trong tk500. Đây là QA cấu trúc trên dữ liệu GitHub, **chưa chạy xác minh được** `python tools/catalog.py validate` và unittest Windows/Linux trong môi trường hiện tại; cần đối chiếu CI.
- Tổng **9.351/11.886 draft, còn 2.535 todo** của ứng viên đã trích, không phải tỷ lệ bản vá có thể chơi được. Chưa có parser/repacker talk/cmc hay kiểm tra RPCS3; giữ font Merienda V3, game binary, ROM/ISO và payload nguyên vẹn.
- **Tiếp theo:** `talk/en/tk600_en.bin_@00001158` (544 todo); sau tk600 đến `tk700` (242 todo), rồi các CMC còn lại. Không cần user cung cấp ROM để dịch dữ liệu catalog.

## Lượt 032 — 11/10/2026 (đổi ưu tiên từ đếm câu sang parser/repacker)

- Người dùng xác nhận cần ưu tiên đưa tiếng Việt vào game, hạn chế dịch nháp lại theo cảm giác. **Không thay đổi các catalog hoặc trạng thái** trong lượt này; mốc vẫn **9.351/11.886 draft, 2.535 todo**.
- Đưa `tools/dialogue_probe.py`, `tests/test_dialogue_probe.py` (6 synthetic unittest) và `docs/DIALOGUE_BINARY_PROBE.md` vào repo. QA tổng hợp chạy 6/6; **không** thay thế kiểm thử với binary gốc hay CI.
- Công cụ **chỉ đọc**, đối chiếu hash và toàn bộ candidate tại offset, báo lỗi nếu lệch nguồn, lấy mẫu byte quanh chuỗi và dò *khả năng* u32 references; không đóng gói, vá, sửa font, cập nhật ISO hoặc tự gán speaker. Báo cáo chỉ ở `local-data/` hoặc `dist/` đã gitignore.
- **Checkpoint tiếp:** (1) chạy probe ở local trên bản gốc 2 talk + 1 CMC; (2) so byte/offset/section; (3) xác định cấu trúc opcode/pointer; (4) parser/serializer roundtrip lossless; (5) repacker dry-run/backup/rollback rồi mới thử một vài lời thoại. Trong khi đó `tk600` vẫn còn 544 mục dịch nháp khi có thời gian.

## Lượt 033 — 11/10/2026 (cổng kiểm tra nguồn talk/CMC toàn bộ)

- Thêm chế độ `--all-dialogue --verify-only` vào `tools/dialogue_probe.py`: chọn toàn bộ catalog `kind=dialogue` trong index, kiểm tra SHA/source/offset/NUL/CMC section, bỏ dò u32 để rà nguồn nhanh và tách kiểm tra dữ liệu khỏi suy đoán pointer.
- Bổ sung 2 unittest tổng hợp cho chế độ source-only, thứ tự chọn catalog và chặn xung đột tham số; mở rộng test chạy read-only. Không cập nhật `draft/reviewed/tested`, không sửa font Merienda V3 hay tệp game.
- **Chưa chạy trên binary gốc**, chưa xây parser/serializer/repacker; không tuyên bố có patch playable. Tiến độ bản nháp giữ nguyên **9.351/11.886, còn 2.535 todo**.
- **Tiếp theo:** chạy `python tools/dialogue_probe.py --bin-dir <thư_mục_bin> --all-dialogue --verify-only` tại máy có bản gốc; đọc các lỗi source/section thật rồi mới nghiên cứu pointer/opcode và roundtrip lossless. Khi chưa có binary, dịch `tk600` chỉ là nhánh công việc phụ.

## Lượt 034 — 11/10/2026 (CMC opaque container roundtrip)

- Bổ sung parser/serializer **chỉ cho lớp vỏ CMC**: header, bảng edges, name slots, padding, section payload giữ nguyên byte, trailer; tự kiểm tra tái tạo đúng bytes trước khi xuất báo cáo.
- Đưa cờ `opaque_cmc_container_roundtrip` vào report khi đọc CMC; riêng talk raw là `null`. Thêm kiểm thử synthetic gồm byte chưa hiểu, độ dài section/padding sai và header count sai; không suy đoán opcode/speaker.
- Chỉ nâng an toàn khảo sát, **không phải parser command/message hoặc repacker**, chưa có file nhị phân gốc trong cloud để xác minh. Tiến độ catalog vẫn 9.351/11.886 draft, 2.535 todo; Merienda V3 và game không thay đổi.
- **Tiếp theo:** xác minh `--all-dialogue --verify-only` trên bản sao `etc.bin_` + `etc.fht_` tại local; phân tích chính xác command stream trong CMC và raw talk, rồi kiểm tra roundtrip đến cấp thông điệp trước khi viết patch.

## Lượt 035 — 11/10/2026 (110 ứng viên đầu tk600)

- Tiếp từ checkpoint parser-first lượt 034, dịch **110 todo→draft** trong `translations/catalogs/talk/tk600_en.bin_.json`, ID `@00001158` tới `@0000692c`; `tk600` có **110/544 draft, 434 todo**. Tái dùng **23** nguồn tiếng Anh trùng đã có bản dịch thống nhất ở tk100/101/204/205/307/500; **87** mục mới có bản nháp tiếng Việt.
- Nội dung gồm 19 nhãn địa điểm/di chuyển, mảnh thoại về Cõi âm, người vô hình, Guardian, công việc và âm nhạc quán rượu (lưỡi gà làm từ gỗ Faery). Không đoán ai đang nói hoặc tự nối những mảnh rời thành câu đầy đủ; note ở từng mục ứng viên mới.
- Rà bất biến 110 ID/source/SHA-256/offset/source_review/thứ tự; chỉ sửa `vi/status/notes`, giữ tiền tố, số ngắt dòng, NFC và bản Việt trùng nguồn. **Chưa thử game** hoặc xác nhận parser/repacker; Merienda V3 và binary/payload giữ nguyên.
- Tổng bản nháp **9.461/11.886**, còn **2.425 todo**; đây không phải phần trăm game đã Việt hóa chạy được.
- **Tiếp theo (dịch):** `talk/en/tk600_en.bin_@0000699d` (`\nyou for your trouble.`), tiếp tục đối chiếu nguồn trùng và xử lý các mảnh mới theo QA. **Ưu tiên kỹ thuật chính:** chạy probe trên archive gốc, xác định command/pointer, rồi lossless message roundtrip trước khi thử patch.

## Lượt 036 — 11/10/2026 (báo cáo cấu trúc không chứa văn bản nguồn)

- Thêm `tools/dialogue_summary.py` và 4 synthetic unittest; biến báo cáo probe local thành tóm tắt số học cấu trúc, chỉ dùng danh sách trường cho phép, bỏ tiếng Anh, các ô hex/ASCII quanh chuỗi, tên section và mọi payload.
- Giữ các mẫu vị trí tham chiếu u32 ở dạng **dấu vết byte**, chưa coi là pointer thật; chỉ chấp nhận đầu vào read-only đúng `BCUS98147` và đường dẫn output trong `local-data/` hoặc `dist/`.
- Cung cấp thao tác local trong `docs/DIALOGUE_BINARY_PROBE.md` để sau này có thể rà cấu trúc mà không cần đưa ROM/ISO lên cloud. Không can thiệp game, font V3 hoặc catalog trong lượt kỹ thuật này.
- **Tiếp theo:** chạy probe thực trên bản gốc và đọc JSON tóm tắt; sau khi có đủ chứng cứ mới thiết kế parser lệnh thoại, lossless roundtrip cấp message và repacker an toàn. Mốc bản dịch vẫn 9.461/11.886 draft, 2.425 todo.

## Lượt 037 — 11/10/2026 (220 mục tiếp theo tk600)

- Tiếp đúng sau lượt 036 ở `talk/en/tk600_en.bin_@0000699d`; dịch **220 todo → draft** đến `talk/en/tk600_en.bin_@0001297d`. Hai commit kiểm soát rủi ro: 100 + 120 mục. **tk600 đạt 330/544 draft**, còn **214 todo**.
- Chủ đề: lời cầu nguyện, sự thật về tai nạn/sát hại, Cõi âm và ký ức, giả thuyết về linh hồn/hạt vật chất, hai anh em và điều ước để họ ngừng đánh nhau, người mẹ và lời từ biệt. Giữ Faery/Oblivion làm tên riêng; không bịa speaker hoặc quan hệ từ các mảnh quét bị cắt.
- Mục có `source_review=candidate` vẫn chỉ `draft`; từng câu mới đều có ghi chú về nguy cơ thiếu scene/speaker. Hai nguồn lặp trong khối 120 được tái sử dụng nguyên bản dịch đã có. Không thay metadata/offset/ID/source/hash hay font V3; bảo toàn Unicode NFC, ký hiệu đầu chuỗi và số xuống dòng.
- **Tổng 9.681/11.886 draft, còn 2.205 todo** từ dữ liệu quét, KHÔNG phải tỉ lệ bản vá game chạy được. Hội thoại chưa thể đóng gói nếu chưa xác thực binary/command/pointer và lossless roundtrip.
- **Tiếp theo:** `talk/en/tk600_en.bin_@00012a71` (`\\nto get work.`), còn 214 ứng viên của `tk600`; sau đó `tk700`, CMC và QA theo cảnh. Ưu tiên kỹ thuật độc lập: chạy `dialogue_probe.py` thật và dùng `dialogue_summary.py` để gửi báo cáo cấu trúc đã lọc.

## Lượt 038 — 11/10/2026 (hoàn tất toàn bộ bản nháp tk600)

- Đã xử lý hết **214/214 todo còn lại** của `talk/en/tk600_en.bin_.json`, từ `@00012a71` đến `@0001ca1f`, chia batch 114+100 để QA; **tk600 hoàn tất 544/544 draft**. Trong lượt cũng sửa bản nháp nguồn trùng `(I haven't seen all the memories.` tại `tk500@00011bb7` từ `((Tôi...` thành `(Tôi...` (lỗi dư ngoặc mở).
- Nội dung gồm ký ức người thân, lòng thù hận và hoàn cảnh gia đình, phần lựa chọn cuối, cùng truyện kỳ ảo trong sách (Pied Piper / Charafrius). Hai tên trong `[...]` được giữ nguyên khi chưa rõ đây là nhãn riêng hay mã. Các ứng viên chưa xác minh người nói/cảnh/tuổi vẫn là `draft`, có notes và không nhận là runtime-ready.
- QA ở tầng catalog: giữ nguyên `id/file_offset/source/source_sha256/source_review`, không sửa thứ tự, giữ tiền tố/ngắt dòng, Unicode NFC; không đụng Merienda V3, binary gốc, bản vá local, RPCS3.
- **Tổng 9.895/11.886 mục draft**, còn **1.991 todo**. Mọi tỉ lệ chỉ mô tả bản nháp trong text catalog, KHÔNG chứng minh patch tiếng Việt chơi được; talk/CMC command parser & repacker vẫn chưa có bằng chứng từ binary gốc.
- **Tiếp theo nhánh dịch:** `talk/en/tk700_en.bin_@00001158` (242 todo); sau đó các CMC chưa dịch và QA theo cảnh. **Ưu tiên kỹ thuật chính:** chạy probe thật trên `etc.bin_` + `etc.fht_` tại local, dùng summary đã lọc để kiểm nghiệm header/opcode/pointer, đạt roundtrip cấp thông điệp trước khi vá.

## Lượt 039 — 11/10/2026 (hoàn tất toàn bộ bản nháp tk700)

- Đã hoàn tất trọn `talk/en/tk700_en.bin_.json`: **242/242 todo→draft**, chia 2 commit 122 + 120, đầu `@00001158`, cuối `@0000fbb3`. 21 nguồn trùng tk100/101/204/205/307/500/600 được tái dùng trong đợt đầu, 2 nguồn trùng ngoài đợt đầu và 20 lần lặp trong batch cuối được nhất quán. (Tổng **23 lượt tái sử dụng xuyên catalog**, 20 lượt lặp nội bộ, còn 199 mục nguồn mới trước khi trừ trùng nội bộ.)
- Nội dung gồm 19 nhãn điểm đến/giao diện, nhiệm vụ tìm đường tại Hành lang Vô tận, hoa cho người đã khuất, các trận đấu với Folk, mật ong, phần thưởng và tên sinh vật `[Tathlum]`, `[Yarthkins]`, `[Alonedite]`, `[Coropuna]`, `[Alhazred]`, `[Grindylow]`, `[Cyhyraeth]`, `[Langelaan]` giữ nguyên. `Denizen` giữ nguyên chờ xác minh là tên chủng loài hay danh từ thường.
- Rà bất biến ID/offset/source/source_sha256/source_review, NFC, tiền tố (`$ / ( / space / newline`), số xuống dòng, câu lặp. Có mảnh có dấu hiệu nói lắp, tiền tố chưa rõ (`ON. Hmm...`) nên chỉ để draft và ghi notes; KHÔNG tự suy người nói hoặc thay cấu trúc.
- Tổng catalog đạt **10.137/11.886 bản dịch nháp**, còn **1.749 todo** (chỉ số chuẩn bị dữ liệu, **chưa phải patch playable**). Không sửa font Merienda V3, game binary/ISO hoặc bản vá local.
- **Tiếp theo nhánh dịch:** `cmc/en/LCmc005_en.bi5_@00004377` (16 todo); sau đó `LCmc007` 15 todo, `LCmc008` 17 todo và các CMC còn lại. **Ưu tiên kỹ thuật:** chưa có kiểm chứng `etc.bin_`/`etc.fht_` thật, cần probe + roundtrip parser message + safe repacker trước khi đưa thoại vào RPCS3.

## Lượt 040 — 11/10/2026 (16 file CMC, 253 ứng viên thoại)

- Từ checkpoint 039 `tk700` đã đủ bản nháp, chuyển sang CMC. **253 mục todo→draft** trên 16 tệp: `LCmc005` (16), `007` (15), `008` (17), `012` (8), `013` (20), `014` (20), `016` (20), `017` (3), `018` (19), `019` (21), `020` (18), `021` (16), `023` (29), `027` (11), `028` (2), `029` (18).
- Làm theo ba commit độc lập (96+97+60). Nội dung chủ yếu Ellen tìm mẹ, Samhain, Áo choàng, ký ức người đã khuất, tháp/hải đăng, cùng điều tra Regine–Renaldo–Ryan–Herve–Suzette. Không định danh người nói từ thứ tự offset. Những nguồn quét có tiền tố `0/4/8/D/H/@/</$/(/,` giữ nguyên byte ký hiệu; bảo toàn số ngắt dòng, SHA gốc/ID/offset/source_review và NFC bản Việt. `Id`, `Folk`, `Folklore`, `Samhain`, `CERNUNNOS` giữ như tên/thuật ngữ.
- Tất cả mới chỉ đạt **draft** và ghi cảnh báo trong notes: chưa xác minh opcode/speaker, chưa roundtrip hội thoại trên binary gốc, chưa thử RPCS3. Không sửa Merienda V3, etc.bin_, etc.fht_, ROM/ISO hoặc patch.
- **Tổng 10.390/11.886 bản nháp; còn 1.496 todo**. Đây không phải 87,4% bản Việt hóa chạy được. Đợt tiếp theo của nhánh dịch là `cmc/en/LCmc030_en.bi5_@00002a98` (14 todo), kế tiếp `LCmc031` (14), `LCmc032` (9), `LCmc033` (11)... 
- **Ưu tiên kỹ thuật thực sự:** chạy `tools/dialogue_probe.py` trên bản sao dữ liệu gốc tại máy, xuất `tools/dialogue_summary.py`, xác lập message/pointer/opcode và byte-perfect roundtrip trước khi có write-capable repacker và patch playable.

## Lượt 041 — 11/10/2026 (334 ứng viên CMC qua 25 file)

- Hoàn thiện bản dịch nháp cho **334 ứng viên `todo→draft`** thuộc 25 catalog CMC: `LCmc030, 031, 032, 033, 034, 035, 036, 037, 039, 040, 041, 042` (164 mục); `LCmc046, 047, 048` (69 mục); `LCmc050, 051, 052, 054, 055, 056, 057, 058, 060, 062` (101 mục). Chia **3 commit** để cô lập lỗi.
- Nội dung: Keats/Ryan, bí ẩn nhà thờ và hồ sơ bác sĩ Lester, lựa chọn của Ellen tại Cõi âm; Herve và Cecilia, lời nhắn trên băng; Lulu, ký ức và sự thật về Cecilia. Giữ tên riêng/tên địa danh, ngắt dòng nguồn và tiền tố có thể là mã điều khiển, không đoán người nói từ thứ tự chuỗi.
- Kiểm tra trong phiên: đúng số mục từng catalog, chỉ ghi `vi/status/notes`, không sửa `source/id/source_sha256/file_offset/source_review`; kiểm tra tiền tố, số newline, Unicode NFC và các nguồn trùng trong batch. Các mục **chỉ ở trạng thái `draft`**, chưa xác minh bối cảnh, giới tính/người nói hoặc chạy trong game.
- **Tổng 10.724/11.886 bản nháp; còn 1.162 todo**. Tỉ lệ bản nháp KHÔNG đo mức độ playable. Font Merienda V3, binary game và patch local không thay đổi.
- **Đầu việc dịch tiếp:** `cmc/en/LCmc063_en.bi5_@000028e7` (10 todo), rồi `LCmc064`, `LCmc065` và các catalog còn thiếu theo index. **Ưu tiên kỹ thuật:** chạy read-only dialogue_probe tại máy có `etc.bin_` / `etc.fht_`, phân tích bảng opcode/pointer từ báo cáo cấu trúc, dựng lossless message roundtrip rồi mới cân nhắc repacker an toàn.

## Lượt 042 — 11/10/2026: lối vào chẩn đoán hội thoại tự động (chỉ đọc)

- Thêm `tools/dialogue_diagnose.py` nhận `--game-root` để tự tìm `etc.bin_` + `etc.fht_` (tối đa 8 cấp) hoặc `--bin-dir` để trỏ chính xác. Nếu thiếu hoặc thấy nhiều kho, **từ chối đoán**. Công cụ chỉ gọi probe gốc + redacted summary, tạo `local-data/dialogue-probe.json` (riêng tư) và `local-data/dialogue-structure-summary.json` (metadata đã lọc); không upload, không sửa game/ROM/ISO/font V3.
- Thêm 6 unit test dữ liệu tổng hợp ở `tests/test_dialogue_diagnose.py`, hướng dẫn một lệnh PowerShell tại `docs/DIALOGUE_LOCAL_QUICKSTART.md`. Kiểm tra Python unittest/GitHub Actions thực tế **chưa được xác minh trong lượt này**; không gọi đây là parser/repacker hoặc đã kiểm thử binary gốc.
- **Chốt việc kỹ thuật tiếp theo:** cần kết quả chạy thật trên bản gốc để phân loại metadata, opcode, speaker, offset và nguồn tham chiếu (u32 byte match không đủ chứng minh pointer). Sau đó mới viết message parser/lossless roundtrip, dry-run repacker an toàn. **Nhánh dịch tiếp:** `LCmc063@000028e7`.
