# make-editorial-explainer — Hermes-first v1.0

Bộ skill hướng dẫn sản xuất explainer tiếng Việt theo bốn video tham chiếu của
người dùng: PNJ, Singapore, gym và hàng không. Không phải app tạo video có sẵn,
không bundle model/HyperFrames, không cấp API, không giả nối Gemini web.

## Cài Hermes (trên máy của anh, chưa được thực hiện trong chat)
Giải nén ZIP ra một thư mục tạm, xem file trước; copy thư mục
`make-editorial-explainer` vào `~/.hermes/skills/`. Không ghi đè skill có sẵn:
```bash
mkdir -p ~/.hermes/skills
test ! -e ~/.hermes/skills/make-editorial-explainer && \
  cp -R make-editorial-explainer ~/.hermes/skills/
```
Nếu profile có HERMES_HOME riêng, dùng skills directory của profile đó. Không
chạy cp khi đường dẫn đích đã tồn tại; backup/diff trước. Dùng phiên chat mới
nếu skill chưa hiện. Hermes hỗ trợ SKILL.md và slash command theo tên skill.

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
handoff, cấu hình Hermes, portability guide, schema, ví dụ, helper project,
VieNeu batch, measure và basic assembly, test tự động.
Chưa có: renderer scene library hoàn chỉnh, cài HyperFrames, đăng nhập Gemini,
bridge Muse/Hermes, forced alignment tiếng Việt, test end-to-end trên VM anh.
Các scene types là đặc tả để agent triển khai, KHÔNG phải component đã render.

## Kiểm tra helper
Python 3.10+; measure/assembly cần ffmpeg/ffprobe trên PATH. Không pip install.
```bash
python3 scripts/test_tools.py
```
Xem TEST_REPORT.md cho kiểm thử thực tế ở môi trường đóng gói. Scripts không
phải sandbox: vẫn review code/paths trước khi chạy ở máy sản xuất.

## Tính di động
SKILL.md dùng frontmatter name/description chuẩn. Core không gắn tên tool đặc
quyền của một hãng. Cần terminal/file tools để sản xuất; một chat chỉ có text
chỉ có thể lập kế hoạch/prompt, không tự render. Đọc references/portability.md.

## Cập nhật và bản quyền
Giữ version trong skill và dự án. Tài liệu là bản tổng hợp mới, không đóng gói
code/asset bên thứ ba. Tài nguyên của từng repo, font, nhạc, footage giữ giấy
phép riêng. Đọc references/source-notes.md trước khi copy component bên ngoài.
