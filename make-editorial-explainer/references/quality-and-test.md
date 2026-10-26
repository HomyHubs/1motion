# QC và validation

## Gate và human review
Gate 1 = nguồn/câu chuyện. Gate 2 = pilot hoàn chỉnh. Ghi phản hồi thật.
Khi viết skill trong chat, không tự spawn agent hoặc chạy validation session
ở tài khoản anh. Chỉ chạy test helper local; hỏi trước nếu muốn pilot end-to-end.

## Test kỹ thuật
- Metadata/schema: name, description, file references tồn tại; example đúng schema.
- Helpers: init không overwrite, check rejects malformed project, measure cập
  nhật timing, paths không thoát project, assemble không cắt lời/overwrite.
- Render: deterministic seek, frames đầu/giữa/cuối và transition; no blank/overflow.
- MP4: decode toàn file, dimension/fps/audio, duration gần timeline trong sai số
  tối đa một frame mỗi beat cộng sai số mux nhỏ; điều tra sai số lớn.

## Review nội dung
Nguồn thực hỗ trợ claim; chart đúng units/scale/bounds; map đúng địa giới;
legal claim có attribution/status; minh họa khác bằng chứng.
Motion phải giúp hiểu cơ chế. Chữ không nhòe/warp; giữ safe area; cùng object
không đổi hình vô lý. Xem ở kích thước điện thoại.

## Review audio và motion
Chỉ ghi pass nghe khi đã nghe; chỉ ghi pass animation khi xem playback/chuỗi
frames đủ để kiểm chuyển động, không chỉ xem một contact sheet. Nếu host không
có tool, ghi chưa kiểm và xin người dùng xác nhận. Không gọi file final-reviewed
khi phần bắt buộc còn pending.

## Benchmark VM
Ghi wall time và peak RAM riêng TTS/render/encode; ghi versions, resolution,
fps, độ dài và số layer. Không dùng benchmark máy đóng gói thay máy người dùng.
Skill bundle test không đồng nghĩa đã test HyperFrames/VieNeu/Gemini integration.
