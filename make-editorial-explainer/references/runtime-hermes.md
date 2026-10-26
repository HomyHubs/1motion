# Hermes adapter

## Cài và gọi
- Cài: chép thư mục skill vào `${HERMES_HOME:-~/.hermes}/skills/` ở phía chạy terminal của Hermes (Linux/WSL: `~/.hermes/skills/`; Windows native: `%USERPROFILE%\.hermes\skills\`). Không ghi đè skill có sẵn; backup/diff trước.
- VieNeu, ffmpeg, HyperFrames phải nằm cùng phía với terminal của Hermes: tool trong WSL không phải tool Windows.
- Gọi: `/make-editorial-explainer <brief>`. Dùng phiên chat mới nếu skill chưa hiện.
- Terminal: mọi bước là lệnh shell qua terminal tool Hermes thực sự cung cấp. Core không dùng tên MCP/tool đặc quyền.

## Biến môi trường (doctor đọc)
| Biến | Ý nghĩa | Mặc định |
|---|---|---|
| VIENEU_PYTHON | interpreter có thư viện vieneu | `~/.venvs/vieneu/Scripts/python.exe` (Windows), `~/.venvs/vieneu/bin/python` (POSIX) |
| VIENEU_VOICE | tên giọng, một giọng xuyên video | Mai Anh |
| HYPERFRAMES_CMD | lệnh HyperFrames khi không nằm trên PATH | `hyperframes` trên PATH |

Mẫu ở `examples/runtime.env.example`. Đường dẫn máy cụ thể không viết vào tài liệu của gói. ASSUMPTION: Hermes nạp `~/.hermes/.env` vào terminal; xác minh khi chạy.

## Cấu hình người dùng cung cấp — phải xác minh lại khi chạy
- Muse chat web: nhận prompt và trả file. Chưa xác minh bridge với Hermes.
- Hermes dùng Gemini qua 9router. Chưa xác minh media endpoint hay browser control.
- VieNeu-TTS v3 Turbo ONNX/CPU, thư viện báo là vieneu 3.8.3. Cache model khoảng 540 MB theo log người dùng, không bảo đảm cache còn đủ.

## Discovery
Dùng terminal/file/web tools mà Hermes phiên này thực sự cung cấp; không bịa tên
MCP/tool. Skill không tự bật browser, media hay quyền đọc file ngoài workspace.
Chạy doctor: nó là probe duy nhất, kết quả JSON nằm trong `capabilities.json` mục `runtime` và là sự thật của dự án.
Doctor báo đường dẫn thật, version Python, ffmpeg, HyperFrames, cpu_count và disk free.
Chỉ chạy --help/version của công cụ đã có, không npx tự download.
Ghi tất cả vào capabilities.json, trạng thái unverified cho thứ chưa test.

## Voice
Hai đường tạo voice, chọn một cho cả video:
1. `scripts/tts_batch.py` import trực tiếp `from vieneu import Vieneu` bằng `$VIENEU_PYTHON`. Đường mặc định, không cần shell.
2. Wrapper `tts-vi.sh` / `synth.py` của anh. Tùy chọn, chỉ khi tồn tại; doctor không kiểm. Cùng model và giọng nhưng không bảo đảm cùng tham số với đường 1.

Review wrapper hoặc script trước, bảo đảm không fallback ngoài. Kiểm tra cache đầy đủ và
đặt HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1 trước khi import VieNeu.
Các biến offline là guard cho thư viện HF, không phải network sandbox tuyệt đối.
Không có quyền outbound thì dùng sandbox/network policy của môi trường.
Batch helper dùng Vieneu(), infer(text, voice=...), save(audio,path) như script
người dùng đã gửi. API có thể đổi; fail nếu không tương thích, không tự thay engine.

Lỗi ONNX external .data qua symlink từng gặp theo báo cáo: không tự thay cả HF
snapshot. Kiểm tra lỗi/path/version; nếu cần, đề xuất copy model sang cache riêng,
đủ các external data file, kiểm hash và dung lượng; xin phép trước khi thay cache.

## Budget và compute
Không phát sinh phí media ngoài khi chưa duyệt. Không dùng nhiều account để né
hạn mức. Chạy serial, benchmark pilot. Tách install/download lần đầu khỏi thời
gian TTS/render thường kỳ. Không suy ra thời gian full video bằng lời hứa.
