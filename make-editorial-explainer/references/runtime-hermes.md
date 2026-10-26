# Hermes + môi trường của anh

## Cấu hình người dùng cung cấp — phải xác minh lại khi chạy
- Muse chat web: nhận prompt và trả file. Chưa xác minh bridge với Hermes.
- Hermes dùng Gemini qua 9router. Chưa xác minh media endpoint hay browser control.
- VM: 2 vCPU AMD EPYC 9D25, RAM khoảng 7.7 GB, không GPU.
- VieNeu-TTS v3 Turbo ONNX/CPU, thư viện báo là vieneu 3.8.3.
- Interpreter: ~/.venvs/vieneu/bin/python
- Wrapper: ~/workspace/tts-vi/tts-vi.sh "text" out.wav
- Script: ~/workspace/tts-vi/vieneu/synth.py
- Voice: VIENEU_VOICE, mặc định Mai Anh. Wrapper cuối được gửi không có fallback.
- Cache model khoảng 540 MB theo log người dùng, không bảo đảm cache còn đủ.

## Discovery
Dùng terminal/file/web tools mà Hermes phiên này thực sự cung cấp; không bịa tên
MCP/tool. Skill không tự bật browser, media hay quyền đọc file ngoài workspace.
Chạy doctor; kiểm tra path thật, version Python/ffmpeg/HyperFrames và disk free.
Dùng `command -v hyperframes` trước; kiểm tra executable local trong project nếu có.
Chỉ chạy --help/version của công cụ đã có, không npx tự download.
Ghi tất cả vào capabilities.json, trạng thái unverified cho thứ chưa test.

## Voice
Review wrapper trước, bảo đảm không fallback ngoài. Kiểm tra cache đầy đủ và
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
