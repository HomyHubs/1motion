# Chọn visual và provider

| Nội dung | Ưu tiên | Không làm |
|---|---|---|
| Người/sự kiện thật | ảnh/clip có nguồn | tạo ảnh người thật làm bằng chứng sự kiện |
| Số liệu | data + chart lớp riêng | cho AI vẽ số/đường chart |
| Địa lý | GeoJSON/SVG + imagery hợp lệ | lấy map AI làm địa giới |
| Tài liệu pháp lý/báo | bản thật, highlight | dựng tài liệu giả có vẻ xác thực |
| Cutout/ẩn dụ/background | Muse/Gemini image nếu có | Pillow minh họa sơ sài làm fallback im lặng |
| Chuyển động tự nhiên | footage/AI video phù hợp | image-to-video cho toàn bộ sơ đồ dữ liệu |
| Chữ/nhãn | local font + timeline | bake chữ vào ảnh rồi warp qua video AI |

Provider contract trong capabilities.json:
name, available, verified_at, tool_or_command, auth_owner, cost_policy,
capabilities (image_generate/image_edit/video_from_image/local_render),
reference_image_support, duration_options, quota (unknown hợp lệ), handoff.
Không coi tài khoản Pro bảo đảm model/quota cụ thể. Kiểm UI/tool thực.
Không nhầm Gemini chat qua 9router với media trên web.

Nếu manual: tạo asset_requests.md gồm asset_id, beat/shot, kích thước, prompt,
ảnh tham chiếu có quyền dùng, negative constraints, file đích, tiêu chí đạt.
Dừng ở waiting_for_asset; khi nhận file kiểm resolution/duration/content rồi
mới đi tiếp. Không xuất final với placeholder chưa được duyệt.

Art direction: tạo vài đề xuất hình có chi phí được duyệt, chọn anchor; giữ
palette/texture/đường viền. Hình AI quan trọng: xem lỗi giả chữ/logo, tay/mặt,
độ chính xác chủ thể. Không tạo lại hàng loạt cảnh trước khi anchor đạt.
