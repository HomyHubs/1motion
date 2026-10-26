# Portability — core và adapter

| Host | Core dùng lại | Phần cần ánh xạ |
|---|---|---|
| Hermes | SKILL.md + references + scripts | terminal, filesystem, media/browser thực có |
| Claude Code | Cùng thư mục SKILL.md | cài theo cơ chế skills đúng bản đang dùng; permissions |
| Gemini CLI | Cùng nội dung workflow | xác minh hỗ trợ skills của bản đó; tên tool và provider |
| ChatGPT web/custom GPT | Instructions + tài liệu tham chiếu | không mặc định có filesystem bền vững, CLI hay VieNeu |
| ChatGPT qua API/agent runner | Core + schema | host triển khai shell/file/browser adapters có quyền |

Không viết lại logic kể chuyện khi chuyển model. Đổi adapter và capability map.
Giữ 3 lớp: core workflow / provider contracts / runtime config. Không nhét
credential vào skill. Với host chỉ đọc được text: xuất script/storyboard/prompt
handoff và trạng thái blocked; không tuyên bố đã tạo video.

Khi port: (1) kiểm schema/frontmatter; (2) ánh xạ file/terminal/media; (3) kiểm
đường dẫn; (4) test helper; (5) pilot render; (6) human review; (7) ghi version.
Model thông minh hơn không tự cung cấp công cụ tạo video hoặc quota.
