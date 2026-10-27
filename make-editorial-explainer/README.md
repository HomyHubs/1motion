# make-editorial-explainer — Hermes-first v1.2.0

Bộ skill hướng dẫn sản xuất explainer tiếng Việt theo bốn video tham chiếu của
người dùng: PNJ, Singapore, gym và hàng không. Không phải app tạo video có sẵn,
không bundle model/HyperFrames, không cấp API, không giả nối Gemini web.

## Cài Hermes
Liên kết thư mục `make-editorial-explainer` vào skills directory của Hermes (một nguồn, không lệch bản):
Windows `mklink /J "<hermes skills>\make-editorial-explainer" "<đường dẫn gói>"`, Linux/macOS `ln -s`.
Hermes v0.22.5 trên máy này có skills dir `%LOCALAPPDATA%\hermes\skills\`; nơi khác lấy đúng dir mà Hermes báo
(mặc định `${HERMES_HOME:-~/.hermes}/skills/`). Không ghi đè skill có sẵn; backup/diff trước.
Copy chỉ khi Hermes không đi theo link (`cp -R`, chỉ khi đích chưa tồn tại).
Hermes, VieNeu, ffmpeg và HyperFrames phải cùng phía (Windows hoặc WSL).
Dùng phiên chat mới nếu skill chưa hiện. `hermes skills list` thấy skill; lệnh slash chưa ai chạy.

## Biến môi trường
Doctor đọc VIENEU_PYTHON, VIENEU_VOICE, HYPERFRAMES_CMD. Mẫu: `examples/runtime.env.example`.
Bảng mặc định ở `references/runtime-hermes.md`.

## Gọi
```text
/make-editorial-explainer Làm pilot 20–30 giây về [chủ đề].
Chỉ kiểm công cụ, nghiên cứu, kịch bản và beat map trước để tôi duyệt.
Dùng VieNeu local; không API trả phí; không tự cài gói hay đăng nhập.
Giữ mục tiêu motion editorial nhiều lớp, không tự thay bằng slideshow.
```
Để chỉ viết: thêm “mode script_only; chưa tạo voice/hình/video”.

## Có gì và chưa có gì
Có: workflow, 3 nhóm visual, 10 scene types, nguồn/semantic QC, Gemini/Muse
handoff, capability contract, HyperFrames kit contract, cấu hình Hermes, portability guide,
schema, ví dụ, helper project, VieNeu batch, measure và basic assembly, test tự động.
Chưa có: renderer scene library hoàn chỉnh, bridge Muse/Hermes, forced alignment tiếng Việt,
test end-to-end trên máy anh. HyperFrames kit chỉ cung cấp composition primitives; Muse/Gemini
media vẫn phải kiểm capability thật và có thể cần bước web thủ công. Các scene types là đặc tả
để agent triển khai, KHÔNG phải component đã render.

## Kiểm tra helper
Python 3.10+; measure/assembly cần ffmpeg/ffprobe trên PATH. Không pip install.
```bash
<py> scripts/test_tools.py
```
`<py>` = `python3` trên Linux/WSL, `py -3` trên Windows.
Xem TEST_REPORT.md cho kiểm thử thực tế ở môi trường đóng gói. Scripts không
phải sandbox: vẫn review code/paths trước khi chạy ở máy sản xuất.

## Tính di động
SKILL.md dùng frontmatter name/description chuẩn. Core không gắn tên tool đặc
quyền của một hãng. Cần terminal/file tools để sản xuất; một chat chỉ có text
chỉ có thể lập kế hoạch/prompt, không tự render. Đọc references/portability.md.

## Cập nhật và bản quyền
Hai version độc lập: `1.2.0` trong frontmatter SKILL.md là version của skill (đổi khi sửa skill); `1.0` trong project.json là version schema dự án (`templates/project.schema.json`, `check` từ chối giá trị khác). Không bump chung. Tài liệu là bản tổng hợp mới, không đóng gói
code/asset bên thứ ba. Tài nguyên của từng repo, font, nhạc, footage giữ giấy
phép riêng. Đọc references/source-notes.md trước khi copy component bên ngoài.
