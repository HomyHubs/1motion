# Production

## Project
project.json (schema), capabilities.json, research.md, script.md, storyboard.md,
STYLE.md, sources/, assets/, audio/, scenes/, captions/, final/, logs/.
Lưu prompt/art direction, tool versions, output hashes, approval và render logs.

## Timing
Mỗi beat: WAV duration đo thật + tail có chủ đích. Shot duration cộng bằng beat
slot. Không để duration_s cũ ghi đè WAV mới. Không trim voice để chữa mismatch.
Subtitles theo clause/phrase, tối đa 2 dòng, font có tiếng Việt; ASS hoặc engine
caption. Chia theo ký tự chỉ là rough timing. Muốn karaoke cần alignment riêng,
kiểm tương thích tiếng Việt/CPU và được phép cài trước. Không tự tải Whisper.

## Voice batch
`tts_batch.py project --...` khởi tạo model một lần, serial. Nếu file đích đã có
thì fail thay vì âm thầm dùng lại file voice cũ. Với --only ID, chỉ chạy beat
được chọn; backup/delete riêng file stale sau khi kiểm dependency, không xóa
cả thư mục. Không sửa global VieNeu wrapper hay cache.

## Resume
Dùng hash từ narration, data, asset, scene code, font và renderer version.
Đổi source data → invalidate scene/chart tương ứng. Đổi voice → timing/cues và
shot liên quan. Đổi anchor/style → cảnh dùng anchor. Lưu manifest; existence
không đủ chứng minh asset hiện hành. Helpers chỉ ghi hash WAV/narration và
hash assembly inputs; agent chịu trách nhiệm full dependency manifest.

## Assembly helper
`project_tools.py assemble` dùng beat clip đã render và voice. Reject clip
ngắn hơn slot đáng kể; không slow-stretch. Chuẩn hóa 720×1280/30fps (hoặc format
trong project), pad/trim ngắn trong sai số cho phép, ghép serial. Không tạo
nhạc, subtitle, animation. Clip phải có overlay/caption trước hoặc hậu kỳ riêng.
Lưu final helper vào final/film.mp4; refuse overwrite nếu file đã có.

Helper mix có VO + silence tail, KHÔNG BGM. Khi có nhạc: xử lý riêng có quyền,
loop/crossfade/fade và ducking, nghe voice rõ; kiểm toàn track trước giao.
Không giả sidechaincompress là loudness normalization. Đo loudness không thay
nghe. Nếu tăng gain kiểm peak/clipping và dynamic range.
