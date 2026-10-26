# BACKLOG — vá skill make-editorial-explainer

Nguồn: lượt audit read-only (zero-trust) ngày 2026-10-26 trên skill `make-editorial-explainer`. 6 phát hiện H1–H6, không có lỗi chí mạng. Đây là plan vá, tách khỏi lượt audit.

Vị trí file: đặt ở gốc repo `1motion/` (ngoài gói skill) để không làm bẩn gói phân phối và không phải cập nhật `MANIFEST.sha256` cho một tài liệu quy trình.

Trạng thái: `[ ]` chưa làm · `[x]` đã vá · `[?]` cần anh chốt hướng trước khi sửa code.

## Release & Mốc gốc

- **v1.0.0-initial** (commit `bd1cdb3`): Tag snapshot ban đầu khi vừa import skill, kịch bản ghi chép và 5 video tham khảo vào repo [HomyHubs/1motion](https://github.com/HomyHubs/1motion). Đã push lên GitHub ngày 2026-10-27.

## Bảng ưu tiên

| Mã | Ưu tiên | Trạng thái | Loại | Vấn đề (1 dòng) | Hướng vá |
|----|---------|-----------|------|-----------------|----------|
| H1 | Cao | [x] | bug | `scripts/check_schema.py` đọc JSON không `encoding='utf-8'`: trên Windows (cp1252) dễ `UnicodeDecodeError` hoặc đọc sai `project.json` tiếng Việt; lệch chuẩn với `project_tools.py` (luôn utf-8) | thêm `encoding='utf-8'` cho mọi `read_text()` |
| H3 | TB | [x] | test | `test_path_traversal` tạo symlink không guard: Windows thiếu quyền sẽ **error** (không skip); 2 test khác cần ffmpeg. "8 PASS" thực chất là Linux + ffmpeg | bọc tạo symlink trong try/except rồi `skipTest` kèm lý do; ghi rõ điều kiện trong `TEST_REPORT.md` |
| H4 | TB | [x] doc / [x] code: giữ import trực tiếp, `project_tools.py voice` là đường duy nhất gọi `tts_batch.py` | doc + design | Runtime mô tả wrapper `tts-vi.sh`/`synth.py`; `tts_batch.py` lại `from vieneu import Vieneu` trực tiếp, bỏ qua wrapper | vá doc: ghi rõ 2 đường và điều kiện tương đương; hợp nhất code = quyết định để sau |
| H5 | Thấp | [x] | robustness | `check_schema.py` `kinds[s['type']]`: KeyError không bắt nếu schema thêm type lạ (boolean/null/union) | báo lỗi sạch "type không hỗ trợ" thay vì crash |
| H6 | Thấp | [x] | doc | Version skill `1.0.0` (frontmatter) vs version project `1.0` (schema/validator/pilot) gây nhầm | README làm rõ 2 namespace khác nhau |
| H2 | Cao | [x] (a) `templates/project.template.json`, `init()` copy khung trắng | design | `init()` copy nguyên `examples/pilot.project.json`: project mới mang sẵn dữ liệu minh họa, mâu thuẫn cam kết "không bịa số liệu". Có backstop: `assemble --final` chặn vì asset `money` đang `waiting` | cần anh chốt (xem mục dưới) |

## Đợt thực thi này (an toàn, có thể đảo ngược)

- H1, H5: sửa `scripts/check_schema.py` (encoding + guard KeyError), không đổi hành vi đúng.
- H3: sửa `scripts/test_tools.py` (guard symlink skip) + ghi caveat vào `TEST_REPORT.md`.
- H4 (doc): ghi chú 2 đường tạo voice trong `references/runtime-hermes.md`.
- H6 (doc): làm rõ 2 namespace version trong `README.md`.
- Regen `MANIFEST.sha256` cho đúng các file đã đổi (giữ nguyên định dạng, giữ LF).

## Chờ anh chốt (không tự sửa code)

- H2 — chọn 1 hướng:
  - (a) [khuyến nghị] thêm `templates/project.template.json` trắng (cấu trúc hợp lệ, mảng rỗng, approvals pending, không số liệu), `init()` copy từ template; `examples/pilot.project.json` chỉ còn làm ví dụ.
  - (b) giữ `init()` copy pilot nhưng blank hoá các field minh họa (title, claims, assets, beats) sau khi copy.
  - (c) chỉ thêm cảnh báo rõ trong SKILL/README, không đổi code.
  - Lý do cần hỏi: cả ba đổi hành vi onboarding đã ghi trong `SKILL.md` Bước 0.5.
- H4 (phần code) — có hợp nhất `tts_batch.py` gọi qua wrapper không, hay giữ import trực tiếp kèm ghi chú? Em nghiêng giữ import trực tiếp (đỡ phụ thuộc shell), chỉ cần doc rõ.
