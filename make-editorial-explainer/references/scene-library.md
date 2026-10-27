# Scene library — đặc tả, KHÔNG phải component đã lập trình

Implementation status: `stack`, `map_route`, and `transaction_flow` have bundled kit primitives. The remaining scene types are schema-supported and `status: planned` until a dedicated renderer sample is added; docs do not claim code that is not present.

| Type | Ý nghĩa | Motion và kiểm tra |
|---|---|---|
| map_route | nơi chốn, hành trình, mạng lưới | camera, vẽ tuyến, pin; đúng tọa độ/projection |
| data_compare | chênh lệch/quy mô/xu hướng | reveal cột/đường; đơn vị/scale/period đúng |
| source_card | đưa bằng chứng | trượt/crop/highlight đoạn thật; đọc được nguồn |
| stat_callout | nhấn một số | nhãn trước/số sau, hold đủ đọc; đúng claim |
| cashflow | tiền vào, quỹ, chi | chuyển token có legend; không nhầm revenue/cash |
| transaction_flow | tài sản/quyền/nghĩa vụ giữa các bên | node/edge có nhãn; hướng giao dịch đúng |
| obligation_timeline | phát sinh, đến hạn, hoãn, tích lũy | mốc thời gian/hồ sơ; trạng thái phân biệt |
| document_desk | cơ chế qua giấy tờ/bàn tay | asset layer, highlight; không bịa chứng cứ |
| asset_grid | mạng lưới nhiều cơ sở/đối tượng | grid/reveal/state; số lượng không giả precision |
| footage_overlay | tư liệu + ý cần nhấn | dim/crop/cutout + type; không che subject |

Mỗi scene cần: purpose, claim_ids, layers, object_ids, focal order,
motion events (trigger phrase + target + meaning), planned timing, renderer,
asset ids và acceptance. “Làm đẹp”, “thêm hiệu ứng” không phải storyboard.

Bài thử nên có map_route + source_card + cashflow/transaction_flow để kiểm cả
địa lý, bằng chứng và cơ chế. Tạo pilot 15–30 giây; không làm ngay cả video 4 phút.
