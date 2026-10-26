# Hermes adapter

## Cài và gọi
- Cài: liên kết thư mục skill vào skills dir của Hermes, không copy (một nguồn duy nhất, sửa là thấy ngay). Windows: `mklink /J "<hermes skills>\make-editorial-explainer" "<đường dẫn gói>"`; Linux/macOS: `ln -s`. Chỉ copy khi Hermes không đi theo link. Skills dir: `${HERMES_HOME:-~/.hermes}/skills/`; trên Windows đã thấy `%LOCALAPPDATA%\hermes\skills\` (Hermes v0.22.5). Không ghi đè skill có sẵn.
- VieNeu, ffmpeg, HyperFrames phải nằm cùng phía với terminal của Hermes: tool trong WSL không phải tool Windows.
- Gọi: `/make-editorial-explainer <brief>`. ASSUMPTION: Hermes v0.22.5 đã liệt kê skill (`hermes skills list`), nhưng chưa ai chạy lệnh gọi này trong Hermes. Dùng phiên chat mới nếu skill chưa hiện.
- Terminal: mọi bước là lệnh shell qua terminal tool Hermes thực sự cung cấp. Core không dùng tên MCP/tool đặc quyền.

## Biến môi trường (doctor đọc)
| Biến | Ý nghĩa | Mặc định |
|---|---|---|
| VIENEU_PYTHON | interpreter có thư viện vieneu | `~/.venvs/vieneu/Scripts/python.exe` (Windows), `~/.venvs/vieneu/bin/python` (POSIX) |
| VIENEU_VOICE | tên giọng, một giọng xuyên video | Mai Anh |
| HYPERFRAMES_CMD | lệnh HyperFrames khi không nằm trên PATH | `hyperframes` trên PATH |

Mẫu ở `examples/runtime.env.example`. Đường dẫn máy cụ thể không viết vào tài liệu của gói. ASSUMPTION: Hermes nạp `<hermes home>/.env` vào terminal; xác minh khi chạy.

## Cấu hình người dùng cung cấp — phải xác minh lại khi chạy
- Muse chat web: nhận prompt và trả file. Chưa xác minh bridge với Hermes.
- Hermes dùng Gemini qua 9router. Chưa xác minh media endpoint hay browser control.
- VieNeu-TTS v3 Turbo ONNX/CPU, thư viện báo là vieneu 3.8.3. Cache model khoảng 540 MB theo log người dùng, không bảo đảm cache còn đủ.

## Discovery
Dùng terminal/file/web tools mà Hermes phiên này thực sự cung cấp; không bịa tên
MCP/tool. Skill không tự bật browser, media hay quyền đọc file ngoài workspace.
Chạy doctor: nó là probe duy nhất, chạy lại ở mỗi gate cần công cụ; output lần chạy đó là sự thật duy nhất, không lưu bản sao. Trình duyệt cho HyperFrames do `hyperframes doctor` kiểm.
Doctor báo đường dẫn thật, version Python, ffmpeg, HyperFrames và cpu_count.
Chỉ chạy --help/version của công cụ đã có, không npx tự download.
Ghi tất cả vào capabilities.json, trạng thái unverified cho thứ chưa test.

## Voice
Hai đường tạo voice, chọn một cho cả video:
1. `project_tools.py voice <project> --cache-confirmed`: chạy `scripts/tts_batch.py` (import trực tiếp `from vieneu import Vieneu`) bằng interpreter mà doctor chọn (`VIENEU_PYTHON`). Đường mặc định, không cần shell riêng.
2. Wrapper `tts-vi.sh` / `synth.py` của anh. Tùy chọn, chỉ khi tồn tại; doctor không kiểm. Cùng model và giọng nhưng không bảo đảm cùng tham số với đường 1.

Review wrapper hoặc script trước, bảo đảm không fallback ngoài. Kiểm tra cache đầy đủ và
đặt HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1 trước khi import VieNeu.
Các biến offline là guard cho thư viện HF, không phải network sandbox tuyệt đối.
Không có quyền outbound thì dùng sandbox/network policy của môi trường.
Batch helper dùng Vieneu(), infer(text, voice=...), save(audio,path) như script
người dùng đã gửi. API có thể đổi; fail nếu không tương thích, không tự thay engine.

Lần chạy đầu: nếu model chưa có trong cache, tải một lần khi anh đồng ý (model công khai, không cần tài khoản),
rồi mới bật chế độ offline và dùng `--cache-confirmed`. Không tải ngầm.

Lỗi ONNX external .data qua symlink từng gặp theo báo cáo trên VM Linux (Windows: HF cache copy file nên không gặp, theo hands): không tự thay cả HF
snapshot. Kiểm tra lỗi/path/version; nếu cần, đề xuất copy model sang cache riêng,
đủ các external data file, kiểm hash và dung lượng; xin phép trước khi thay cache.

## Budget và compute
Không phát sinh phí media ngoài khi chưa duyệt. Không dùng nhiều account để né
hạn mức. Chạy serial, benchmark pilot. Tách install/download lần đầu khỏi thời
gian TTS/render thường kỳ. Không suy ra thời gian full video bằng lời hứa.
