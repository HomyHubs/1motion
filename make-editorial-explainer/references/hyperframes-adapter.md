# HyperFrames adapter

HyperFrames là dependency ngoài, không nằm trong ZIP. Đọc core skill/CLI/docs
của phiên bản cài thực, kiểm --help. Không chạy installer/npx tải gói chưa phép.
Chọn engine một lần trong project; không trộn renderer Barty, Remotion, Manim
và HyperFrames cho từng scene mà không có lý do và conform rõ.

Hợp đồng dự án:
- index.html làm root, một composition cho mỗi scene.
- Assets/font local; thời gian hiển thị và duration explicit.
- Timeline paused/seekable đăng ký đúng API của bản cài.
- Không Date.now/timer/network/random không seed trong render.
- Mọi cảnh phải render được ở timestamp bất kỳ, cả khi seek lùi.
- Text/asset/data chỉnh được, id ổn định. Giữ safe areas.
- Preview, check/lint, snapshot rồi xem thật trước render delivery.

Khởi đầu: HTML/CSS/SVG và timeline GSAP khi engine hỗ trợ. Dùng existing
registry component sau khi review license/quality. Dùng asset AI thật đẹp cho
cutout/illustration, không bắt agent vẽ mọi thứ bằng primitive.

Map vector: projection/coordinate array tách khỏi camera. Với vệ tinh, kiểm
quyền cache/export/attribution của provider, không tải tile hàng loạt vô phép.

Local HyperFrames rendering và dịch vụ media/cloud/hosted là hai thứ khác.
Không chạy cloud/media trả phí dù CLI gợi ý. Không tạo account mới tự động.
Local chỉ là cơ chế render, không bảo đảm miễn phí subscription/server.

Tích hợp repo khác: lấy speech-trigger planning và review loop của Barty,
lấy quy tắc map/data/type từ iart; triển khai lại theo contract HyperFrames.
NullMotion chỉ phục vụ reference-vs-draft review nếu cần. Không tuyên bố nó
tự tái tạo motion từ video, không phụ thuộc hosted Null Studio.
