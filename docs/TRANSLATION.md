# Quy tắc dịch

Tiếng Việt tự nhiên, có không khí truyện cổ u tối; menu rõ ràng, ngắn gọn.
Hội thoại xét các câu trước/sau; chưa biết người nói thì ghi chú, không tự gán
quan hệ nhân vật. Giữ tên riêng và từ chốt trong translations/glossary.json.

## Dữ liệu

translations/index.json liệt kê 158 catalog, 11.886 mục trích được: 1.016 mục
menu từ bảng system, 10.870 ứng viên từ 23 tệp talk và 134 tệp cmc có phần talk.
Chưa chứng minh đây là toàn bộ game: câu ngắn, Unicode, phim và các vùng khác
có thể chưa trích được. Câu lặp tại vị trí khác nhau có ID riêng.

Mỗi mục có id, file_offset, source, source_sha256, vi, status, source_review,
notes. Giữ nguyên nguồn/ID/order/metadata. Chỉ điền bản dịch và tiến độ.
NFC, không nhập ký tự alias font vào trường vi.

Trạng thái: todo → draft → reviewed → tested. skip dành cho mục không phải
văn bản cần dịch, phải giải thích trong notes. 134 mục menu mẫu đang draft:
đã dịch thử, nhưng không phải tất cả đã được người dùng xem trong game.

## Xưng hô và khẩu khí nhân vật

- **Không đặt đại từ theo một công thức cố định.** Dùng tên, người nói, người nghe, tuổi/quan hệ, mức độ thân thiết và sắc thái tình huống *chỉ khi đã xác minh trong cảnh*. Không gán “anh–em”, “ông–cháu”, “mày–tao”, “ta–ngươi” theo cảm giác hoặc vì nhân vật thuộc Cõi âm.
- Khi người kể tự nói về mẹ/quá khứ (như các câu có “my mother”), giữ nội dung gốc; chưa xác minh speaker thì tạm dùng “tôi/mẹ tôi”, không khẳng định đó là Ellen. “I” thường là “tôi” trong đối thoại với người lạ; “mình” chỉ khi biết đó là độc thoại/ý nghĩ tự nhiên.
- Với đối tượng chưa rõ, ưu tiên lược đại từ khi câu vẫn tự nhiên, hoặc “bạn” ở bản nháp khi ngôi thứ hai là bắt buộc; đánh dấu cần QA. Từ “he/she” chỉ giới tính ngữ pháp chứ không đủ để đoán nhân vật, độ tuổi hoặc quan hệ.
- Khẩu ngữ Doolin (ye/yer/askin') giữ chất thân thiện địa phương bằng nhịp nói, “nào/nhé/chứ” và ngữ điệu; không tự chuyển sang “mày/tao” hay tạo phương ngữ Việt gây lệch không khí truyện cổ u tối.
- Câu ngắn không được cộc lốc như văn máy: linh hoạt hư từ khi **đã đủ ngữ cảnh**; nhưng với candidate cắt mảnh, tuyệt đối không thêm chủ ngữ, lời mời, động cơ hoặc tình tiết chưa có trong tiếng Anh.
- Kiểm tra các lựa chọn đại từ lặp trên toàn **cảnh đã dựng lại**, không chỉ các ID kế nhau. Bản `source_review=candidate` chưa có parser/speaker phải giữ `draft` kèm notes, không chuyển reviewed/tested theo suy đoán.

## Mã điều khiển và tiền tố chưa rõ

Giữ tag <...>, placeholder %s/%d, {0}, dấu $ và các ngắt dòng nguồn.
Nguồn candidate được quét từ ASCII kết thúc NUL, chưa có parser hội thoại đầy
đủ. Dấu đầu câu như $, (, số 0/4, chữ D... có thể là byte metadata đứng sát chữ.
Không dịch tiền tố như lời nhân vật. Giữ lại trong draft và ghi chú phần chưa
xác minh; không cắt nguồn, nối mục hay sửa offset để làm câu trông đẹp hơn.

## Mỗi lượt

Đối với menu đã xác minh: dịch khoảng 200 mục mỗi lượt (hoặc tất cả mục còn lại
nếu ít hơn), rà thành từng nhóm nội bộ ~50 mục, kiểm tra từ vựng và source
trùng nhau; chỉ bàn giao sau khi hoàn tất lượt lớn. Đối với hội thoại dài,
cảnh có nhiều người nói hoặc dữ liệu chưa rõ metadata, chia lượng nhỏ hơn khi
cần để giữ ngữ cảnh và chất lượng.
Chạy python tools/catalog.py validate và unittest; xem diff để chắc chỉ
trường dịch/tiến độ thay đổi. Cập nhật
QUEUE.md với tệp/ID đã làm, vấn đề còn mở và điểm bắt đầu lượt sau.
Không suy phần trăm game hoàn tất từ số mục đã dịch.

Hội thoại có thể dịch trên cloud ngay, nhưng cần parser/repacker trước khi đưa
vào game. Câu mới có thể cần bổ sung glyph/alias và kiểm tra tràn vùng local.
