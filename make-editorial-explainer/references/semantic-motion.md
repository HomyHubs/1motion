# Semantic motion và object continuity

Lập object registry trước khi animate: id, role, label, visual asset, colour,
owner/state. Cùng entity giữ id/asset xuyên cảnh. Bổ sung nhãn nếu màu chưa đủ.

Định nghĩa edge: cash_payment, asset_transfer, ownership_transfer,
service_obligation, information, chronology. Mỗi edge có source, target,
label, thời điểm và claim support. Tiền đi A→B không có nghĩa sở hữu đi A→B.
Chuyển màu/chồng giấy/đổi nhãn phải đúng trạng thái chứ không chỉ để đẹp.

Timeline có 3 lớp: chuyện đã xảy ra, nghĩa vụ tương lai, giả định minh họa.
Không biến forecast thành fact bằng cách cho nó chạy cùng timeline không nhãn.
Nếu chồng tiền chỉ tượng trưng, ghi illustrative; nếu biểu diễn tỷ lệ, định
nghĩa một token = bao nhiêu và giữ đúng trong mọi frame.

Entry → explain → hold → exit. Một hành động có lý do: route để chỉ đường,
arrow để chỉ quan hệ, pulse để chỉ vị trí, crop để đọc chứng cứ. Không làm tất
cả nhấp nháy. Tách lớp chữ khỏi chuyển động camera khi chữ cần ổn định.

Căn sự kiện vào cue đã đo. Phrase cue chỉ dự kiến trước alignment/nghe kiểm;
không gọi proportional-by-characters là timestamp chính xác từng từ.
