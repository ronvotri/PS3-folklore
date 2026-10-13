# BÀN GIAO CHO CODEX — HOÀN THIỆN VIỆT HÓA FOLKLORE PS3 (14/10/2026)

> **Ưu tiên cao nhất:** Làm ra **bản vá Việt hóa chơi được và có thể khôi phục**, tiến tới FULL; không tiếp tục chuỗi vòng dò byte V1–V7, không bắt người dùng xác nhận lại font hoặc gửi lại cùng báo cáo. Đây là dự án thực hiện lâu dài qua nhiều commit, không phải tác vụ chỉ dịch vài câu.

## 1. Môi trường và repo

- **GitHub:** https://github.com/ronvotri/PS3-folklore — dùng **nhánh mặc định `main`**; tất cả mã, bản dịch, tài liệu và checkpoint ở đây.
- **Game:** `Folklore` trên PS3, **mã đĩa `BCUS98147` (Mỹ)**. KHÔNG giả định bản `BCES00050` của châu Âu có cùng offset.
- **Game gốc trên PC người dùng (đường dẫn đã dùng):** `E:\Game\Folklore`. Hai archive `etc.bin_` và `etc.fht_` nằm ở đâu đó trong cây thư mục này; các tiện ích `--game-root` hiện có thể tìm đệ quy. Không suy rằng mọi máy Codex thấy ổ E:.
- **Nếu Codex chạy local trên Windows có quyền đọc game:** tự tìm duy nhất cặp archive và làm việc **trên bản sao**. Không sửa game gốc, save hoặc các bản vá font đã xác nhận.
- **Nếu Codex Cloud không đọc được E:** tiếp tục viết parser, serializer, builder, test và CI với fixture; cung cấp runner local sử dụng đúng game của người dùng. **Đừng yêu cầu upload ROM/ISO, 2,5 GB archive gốc lên GitHub hay gửi lại toàn bộ file game.**
- Python 3.10+; phần đọc/dịch/test thuần dùng standard library. Các công cụ font có dependencies riêng ở `requirements-font.txt`.

### Thứ tự đọc ưu tiên

1. `AGENTS.md` (nguyên tắc an toàn và mong muốn của người dùng), **tài liệu này**.
2. `README.md`, `docs/STATUS.md`, `docs/QUEUE.md`, `docs/TRANSLATION.md`, `translations/glossary.json`.
3. `docs/FORMAT.md`, `docs/FONT.md`, `fonts/choice.json`, `fonts/aliases.json`, `docs/font_baseline.json`.
4. `docs/DIALOGUE_V6_FULL_AUDIT_RESULTS_2026-10-13.md` và **`docs/CMC_V7_EXCEPTION_IDS_REDACTED.json`** (51 ID cụ thể, đã chạy trên file game thật). Cũng xem `docs/DIALOGUE_V7_ROUNDTRIP_EXCEPTION_HANDOFF_2026-10-13.md`.
5. `docs/CMC_FIXED_BATCH_02_2026-10-14.md`, `docs/FOLKLORE_ALLIANCE_FORMAT_LEAD_2026-10-14.md`.

Những tài liệu `STATUS.md` / `QUEUE.md` rất dài vì lịch sử; các phần ở **đầu file** mới nhất. Nếu tài liệu cũ nói “chưa chạy probe trên game thật”, đó là phát biểu đã lỗi thời, bị ghi đè bởi V2–V7 thực đo và bàn giao này.

## 2. Thành quả đã có — KHÔNG LÀM LẠI

| Mục | Tình trạng |
|---|---|
| Catalog | **158 tệp, 11.886 mục có nháp Việt ngữ** theo checkpoint; chỉ là *draft*, không phải 100% in-game |
| Menu | **1.016** mục trong catalog menu; menu UTF-8 có dấu đã có demo |
| Talk script | **23** tệp `talk/en/tk*_en.bin_`, thuộc tổng 10.870 ứng viên hội thoại, **chưa có serializer / repacker** |
| CMC | **134** tệp `cmc/en/LCmc*_en.bi5_` với **1.795** ứng viên ASCII-NUL |
| Font | **Merienda Regular 400 V3**; người dùng đã xác nhận dấu tiếng Việt, sửa lỗi giãn cách `ấ`/`ớ` trong menu RPCS3. Giữ nguyên tất cả 25 alias đã chốt |
| Khung CMC | V6 đo trên **134/134 file thật**, **1.744/1.795** ứng viên khớp `00 04 00 XX`, **51** ngoại lệ |
| V7 | Người dùng chạy thật, **134 file tái tạo byte-exact ở mức token khung+opaque**; **không** phải parser message có nghĩa |
| Patch test | `tools/cmc_alpha01.py` thay một câu CMC000 cùng độ dài; `tools/cmc_batch_fixed.py` vá một số câu cùng độ dài byte và có backup/restore. **Chưa xác nhận runtime** và **KHÔNG phải patch full** |

**Điều kiện được người dùng khẳng định:** font V3 **đã hiển thị tiếng Việt có dấu**, tuyệt đối **không yêu cầu họ chứng minh lại**. Nếu toàn bộ tập dịch có chữ chưa có glyph thì mở rộng **dựa trên V3 đã đúng**, không thay font, không bỏ dấu, không reset 25 alias; font thành công trên menu không chứng minh mọi đường render/gameplay đã được test.

**Về 51 ngoại lệ:** xem `docs/CMC_V7_EXCEPTION_IDS_REDACTED.json`. Tổng hợp: 24 `not_000400_frame`, 12 `unexpected_mod1`, 12 `unexpected_mod2`, 3 `mod3_nonprintable_source_prefix`. CMC800/801 chiếm 16. Ở CMC800 decimal offset 12071, source mở bằng `beautiful...`, bản nháp mở bằng `đẹp...`; **không mặc định byte đầu là metadata để ép/bỏ chữ**, không đổi offset hoặc ID bừa.

**Điều kiện kỹ thuật đã quan sát:** `etc.bin_` 2.498.514.097 byte, `etc.fht_` gồm 4.831 entry, 40 byte/entry (tên 32 byte, size và absolute offset big-endian). `docs/baseline.json` và catalog có SHA-256 cho bản Mỹ. Một số byte trong CMC có frame pattern 4 byte nhưng **chưa giải được ngữ nghĩa message, branch, speaker, length, relocation**. Talk có cấu trúc khác — đừng áp khung CMC vào talk theo cảm giác.

## 3. Lý do chưa có patch FULL

**Không thiếu bản nháp.** Nút thắt là chưa có **parser → editable representation → serializer/repacker** đủ tin cậy để thay câu tiếng Anh bằng tiếng Việt **độ dài byte khác nhau**, cập nhật mọi tham chiếu/section/FHT, giữ command/branch, không crash.

`tools/cmc_batch_fixed.py` rất hạn chế: phép đối chiếu dự thảo **30/134 CMC đầu** cho thấy chỉ **4/437** hàng vừa độ dài byte sau mã hóa (đây **chỉ là mẫu 30 catalog**, không phải dự đoán tỷ lệ toàn game). Nhiều bản dịch có thêm byte UTF-8 hoặc glyph/alias chưa có. Dùng fixed-byte tool làm lớp nền cho backup, preflight và rollback, **không tiếp tục kéo dài hướng vá micro-patch một dòng**.

Các catalog hiện xuất từ `tools/catalog.py` là quét **ASCII-NUL candidates**, có thể gồm mảnh câu, marker/prefix bị gom nhầm và có thể **sót văn bản**. Đã dịch hết các candidate **không đảm bảo full game**. Phải tìm/ghép đúng message, speaker, thứ tự phát, placeholder, tên, chọn nhánh. RTD, movie subtitles (`bin/movie/movie_*_en.dat2_`), chữ trong menu texture/ảnh và patch/DLC cũng cần inventory.

## 4. Mã nguồn nên tái sử dụng

- `tools/catalog.py` và `translations/index.json`, `translations/catalogs/{menu,talk,cmc}/`: nguồn/ngữ cảnh/tiến độ; **không đè source, ID, hash, file_offset**.
- `tools/text_codec.py`: encode/decode tiếng Việt NFC qua **25 glyph alias V3**. Thêm alias/glyph chưa có theo cách tránh va chạm nếu cần; kiểm thử đầy đủ.
- `tools/font_atlas.py`, `tools/font_probe.py`: tạo/QA font Merienda, không viết lại tùy tiện.
- `tools/dialogue_probe.py`, `tools/dialogue_diagnose.py`, `tools/cmc_frame_audit.py`, `tools/cmc_readonly_tokens.py`, `tools/cmc_exception_ids.py`: source verification / section parsing / byte-roundtrip metadata; tận dụng parser nền và ngoại lệ đã biết, **không chạy lại V1–V7 chỉ để xin cùng loại báo cáo**.
- `tools/cmc_batch_fixed.py` + `tests/test_cmc_batch_fixed.py`: preflight/backup/apply/restore *same-byte* (bộ công cụ mới nhất nhưng chỉ thử mô phỏng).
- `tools/cmc_alpha01.py`: minh họa patch 1 câu, không phải kiến trúc full.
- `tools/folklore.py`: **ASCII menu legacy**, không dùng làm codec/cài đè font có dấu V3.
- `docs/DIALOGUE_BINARY_PROBE.md` và `docs/FORMAT.md`: bằng chứng format và những giả thuyết cần kiểm tra.

**Nguồn tham khảo ngoài repo (chưa có tool đã kiểm chứng):** nhóm **Alliance**, tác giả kỹ thuật **RangerRus**, từng làm bản dịch Folklore châu Âu `BCES00050` vào 2013 (xem `docs/FOLKLORE_ALLIANCE_FORMAT_LEAD_2026-10-14.md`). Có thể tìm **mã/công cụ/tài liệu được công khai hợp lệ**, nhưng không coi tool BCES dùng ngay được cho BCUS và không tải/chia sẻ game chứa bản quyền.

## 5. Hướng triển khai Codex phải thực hiện theo thứ tự

### A — Nền tảng FULL CMC, không lặp probe

1. Đọc source code và **tự kiểm định lại** unit test/validator trong repo. Xây test trên fixture tổng hợp và local regression cho source hash, zero-length CMC sections, endian, dữ liệu opaque, biến thể marker.
2. Viết model biểu diễn **record/message có trường xác định và trường opaque**: parse→serialize **byte-for-byte khi chưa dịch**, trên nhiều CMC thật và trên 51 case bất thường. **Opaque roundtrip đơn thuần không phải kết quả cuối.**
3. Xác định các trường liên quan độ dài, bảng con trỏ/offset, căn chỉnh, script command và các tham chiếu vượt section trước khi cho thay câu đổi độ dài.
4. Làm **repacker CMC variable-length**, có kiểm tra relocation/fixup/section size và FHT/archive offset nếu cần; preserve mọi byte/chunk không liên quan; fail-closed khi không hiểu. Không làm “viết thẳng UTF-8 vào file_offset”.
5. Áp dụng nhóm bản dịch CMC có cấu trúc đã xác minh; xuất manifest số câu được thay/skip với **ID+nguyên nhân**. Test cài và restore trên **bản sao** game, rồi người dùng tự chạy RPCS3 kiểm tra.

### B — Repacker `talk/en`

1. Giải ngữ pháp 23 file `tk*_en.bin_` **riêng**, không giả định cùng record layout với CMC.
2. Lập message ordering/choice/speaker, nối fragment từ nguồn đúng ngữ cảnh. Parse→serialize không dịch phải byte-perfect; rồi hỗ trợ relocation và câu độ dài biến đổi.
3. Áp hết nháp đủ điều kiện; thống kê untranslated/skipped, không giấu bản dịch chưa đưa vào game.

### C — Font, inventory chữ ngoài catalog, biên tập

- Kiểm tra tập toàn bộ chữ Việt cần xuất từ 11.886 draft; mở rộng V3 từng glyph/alias chưa có, giữ 25 slot đã xác nhận, đảm bảo không lỗi giãn chữ; không yêu cầu xác nhận lại **nền font V3**.
- Quét UI, RTD, subtitle movie, hình có chữ, update/DLC và các câu ngắn chưa vào catalog; tạo catalog bổ sung thực tế khi cần, không lẫn debug/internal.
- Rà tiếng Việt **đúng không khí huyền bí, tự nhiên**, phân biệt người nói, thống nhất thuật ngữ; giữ tag/placeholder/control, dòng và byte metadata đúng nghĩa. Không tự gán xưng hô dựa vào thứ tự candidate.
- Tạo **patch delta/build script + bộ cài Windows một-click**, chế độ verify/apply/restore, sao lưu có SHA, tính đến người dùng không muốn chạy lệnh dài. Đóng RPCS3 khi ghi. Không đóng gói ROM/ISO/font game nguyên bản lên GitHub.

### D — Phát hành

- Có số lượng câu/scene thực sự được áp dụng và danh sách còn sót, kèm lý do.
- Có kiểm thử nguồn gốc/khôi phục/lặp lại build, không thay file lạ; thông báo rõ những phần chưa thử trong game. Runtime RPCS3 chỉ coi là xác nhận **sau khi người dùng tự kiểm tra**, không từ unit test.
- Cập nhật README, `docs/STATUS.md`, `docs/QUEUE.md`, changelog, hướng dẫn cài đặt **dễ dùng**, checkpoint/commit thường xuyên lên `main` (hoặc PR rõ ràng). Không tuyên bố “FULL” chỉ dựa trên draft-count.

## 6. Lệnh QA tiêu chuẩn và mục tiêu sản phẩm

```bash
python tools/catalog.py validate
python -m unittest discover -s tests -v
```

Tùy tình hình bổ sung CI roundtrip CMC/talk, golden fixture, encoder alias, FHT index, binary patch checks, rollback checksum; test **không cần bản game thật** ở CI và test **có bản game gốc local** cho format xác thực.

**Sản phẩm người dùng cần:** `Folklore BCUS98147 Việt hóa có dấu — Patch FULL` với bộ cài đơn giản, không cần người dùng tự trích game, tự chạy hàng chục script, hoặc liên tục gửi báo cáo JSON. Đi theo mốc cụ thể **CMC variable-length → talk repacker → font completeness & nguồn còn sót → QA runtime → FULL**. Nếu chưa đủ dữ liệu để làm một mốc, **ghi blocker và triển khai phần tiếp theo có giá trị**, đừng hứa ngày hoàn thành hoặc lặp vô tận chẩn đoán.

## 7. Phần việc đầu tiên khi nhận bàn giao

**Hãy làm ngay, không hỏi lại yêu cầu đã rõ:**

1. Clone/đọc repo, mở `docs/CMC_V7_EXCEPTION_IDS_REDACTED.json`; chạy validator và tests; kiểm tra code của batch 0.2 và message grammar hiện có.
2. Lập `docs/REPACKER_IMPLEMENTATION_PLAN.md` *ngắn, có tiêu chí nghiệm thu* cho CMC variable-length và talk; viết/commit **mã parser/serializer có kiểm thử** cho một họ record thực tế. Đừng chỉ viết kế hoạch.
3. Nếu không có bản game thật trong Codex Cloud, xây fixture + runner offline test cho máy local; không yêu cầu upload 2,5 GB ROM.
4. Mỗi lượt: chạy QA, commit lên repo, cập nhật `docs/QUEUE.md` và `docs/STATUS.md`, nói rõ file/commit, số test và blocker thật. Làm tiếp từ checkpoint qua các lượt sau.

---

**Sự thật cần giữ:** CMC V7 byte-exact source reconstruction **đã chạy trên game thật**, nhưng **chưa có** editable message grammar, full repacker, full in-game confirmation. Font V3 đã được xác nhận trong menu; không quay lại kiểm tra từ đầu. Tập draft 11.886 mục là tài sản dự án, phải bảo toàn.
