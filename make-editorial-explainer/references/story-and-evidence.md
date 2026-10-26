# Story và bằng chứng

## Viết
Bắt đầu bằng một câu hỏi thực: vì sao kết quả ngược trực giác, chuyện gì đã
thay đổi, một giao dịch hoạt động như thế nào? Viết 3 hook khác lập luận.
Mạch: hook → bối cảnh tối thiểu → cơ chế từng bước → giới hạn → kết quay về hook.
Không bắt buộc 3 lý do/twist/CTA. Không mở “trong video hôm nay”.

Viết tiếng Việt nói tự nhiên, câu chủ động, một ý/câu hoặc beat, thuật ngữ giải
thích ngay. Dùng so sánh đời thường không làm sai bản chất. Giữ số hiển thị ở
dạng digits; narration viết cách đọc phù hợp, không đọc URL/ghi chú.
Không dùng một chỉ tiêu words-per-minute tiếng Anh cho tiếng Việt. Timing là
ước lượng cho tới khi WAV được đo. Không tự hứa 200 từ = 60 giây.

## Claim ledger
Mỗi claim có id, text, type (fact/attributed/allegation/analysis/forecast),
status (verified/pending/illustrative), sources và kỳ/đơn vị nếu cần.
Mỗi source có id, title, URL hoặc file local, ngày truy cập, quyền dùng/note.
Verified nghĩa đã đối chiếu nguồn hỗ trợ đúng claim, KHÔNG phải chỉ có URL.
Bài báo cùng sao chép một nguồn không được coi là nhiều bằng chứng độc lập.

Phân biệt doanh thu/lợi nhuận/tiền mặt; dư nợ/khoản bị yêu cầu/phán quyết;
trả trước/nghĩa vụ dịch vụ; số liệu quý/năm và danh nghĩa/đã điều chỉnh.
Luôn ghi đơn vị, ngày, phạm vi, denominator. Nếu dữ liệu “dưới 20%” thì đừng
vẽ cột như giá trị chính xác 20%; dùng ký hiệu/bound/caption đúng bản chất.

## Pháp lý và địa lý
Dùng “theo ...”, “bên A yêu cầu ...” khi đó là phát biểu/cáo buộc. Không tự kết
luận gian lận, vỡ nợ hay vi phạm. Ghi cấp tòa/ngày/tình trạng hiệu lực nếu dùng.
Map phải có nguồn địa giới/nhãn phù hợp, attribution, không AI tự bịa địa danh.
Minh họa cơ chế không được giả thành bằng chứng sự kiện.

## Video tham chiếu
Video có sẵn làm nguồn kịch bản được, không phải nguồn sự thật. Phiên âm lời kèm timestamp vào research.md.
Mỗi claim lấy từ video: type `attributed`, source = file video + timestamp, status `pending` (sự thật bên dưới chưa đối chiếu; `verified` chỉ khi đã đối chiếu nguồn độc lập). Bản dựng lại để so sánh là `pilot`: `check --assets --final --pilot` và `assemble --pilot` cho claim `pending` đi qua, manifest ghi `unverified_claims`; `--final` không `--pilot` vẫn chặn. Bản đó không công bố. Giọng đọc nói chính sự thật bên dưới, nên phải có một dòng mở đầu trên màn hình: bản dựng lại để so sánh, số liệu theo video tham chiếu, chưa kiểm chứng.
Không dùng lại footage, nhạc hay đồ họa của video khi chưa có quyền; dựng lại bằng tài sản riêng.
Số liệu lấy từ video chỉ hiển thị kèm “theo video tham chiếu” cho tới khi đối chiếu được nguồn gốc.

## Đầu ra
research.md (ledger + giới hạn), script.md (hook/beat map/narration sạch),
storyboard.md (ý → hình → motion → câu kích hoạt → nguồn).
