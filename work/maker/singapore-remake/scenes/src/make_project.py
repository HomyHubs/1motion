"""Writes project.json for the Singapore remake from the beat table below.
Narration follows hands' ASR of video-reference/singapore.mp4 with obvious slips fixed.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REF = 'ref-video'

SOURCES = [{
    'id': REF,
    'title': 'Video tham chiếu: video-reference/singapore.mp4 (118.5 s), phiên âm ASR large-v3-turbo của hands (work/hands/ref/singapore_transcript.txt)',
    'rights_note': 'Chỉ dùng lời và cấu trúc làm kịch bản mẫu. Không dùng lại footage, nhạc, đồ họa hay frame của video mẫu.',
}]

CLAIMS = [
    ('c1', '0.12-6.00', 'Singapore nhỏ hơn Sài Gòn, không giàu tài nguyên, nước uống phải mua của láng giềng'),
    ('c2', '6.66-9.72', 'người dân Singapore giàu ngang người Mỹ'),
    ('c3', '10.12-19.02', 'năm 1965 Singapore bị tách khỏi Malaysia và Thủ tướng Lý Quang Diệu khóc trên truyền hình'),
    ('c4', '19.58-28.20', 'Singapore ít đất, không tài nguyên, dân nghèo, nhưng có lợi thế vị trí'),
    ('c5', '28.20-40.30', 'đường ngắn nhất từ Trung Đông và châu Âu sang Trung Quốc, Nhật, Hàn đi qua eo biển Malacca, cửa ra nằm sát Singapore'),
    ('c6', '41.04-46.14', 'khoảng một phần tư hàng hóa buôn bán của thế giới đi ngang qua đây'),
    ('c7', '46.66-55.66', 'tàu chạy ngang không trả phí nên Singapore xây cảng lớn, bốc dỡ nhanh, phí hợp lý để tàu muốn ghé'),
    ('c8', '55.66-66.68', 'tàu lớn thả container, tàu nhỏ chở đi khu vực, hàng Việt Nam từng đổi tàu ở đây, nay là một trong những cảng container bận rộn nhất thế giới'),
    ('c9', '67.24-82.16', 'Singapore không có một giọt dầu nhưng là trung tâm lọc dầu lớn bậc nhất châu Á, mua dầu thô, lọc, bán lại cho khu vực'),
    ('c10', '82.16-89.76', 'luật lệ rõ ràng, tham nhũng bị xử nặng, dùng tiếng Anh, thuế thấp'),
    ('c11', '90.34-99.70', 'tập đoàn lớn đặt trụ sở châu Á tại Singapore, tiền ngân hàng và giới nhà giàu kéo về'),
    ('c12', '100.16-110.30', 'Singapore giàu nhờ ba thứ: đứng đúng chỗ, biến vị trí thành dịch vụ ai đi ngang cũng dùng, làm cho tiền thấy an toàn để ở lại'),
]

# (id, scene_type, claims, narration, purpose, layers [(id, role)], events [(target, trigger, action, meaning)])
BEATS = [
    ('01', 'stat_callout', ['c1', 'c2'],
     'Ê, hòn đảo bé xíu này còn nhỏ hơn Sài Gòn, không giàu, không mỏ, nước uống còn phải mua của hàng xóm. Vậy mà người dân ở đây giàu ngang người Mỹ, vì sao vậy nhỉ?',
     'Đặt câu hỏi trung tâm: vì sao nơi thiếu mọi thứ lại giàu.',
     [('dot', 'Điểm đánh dấu Singapore'), ('chips', 'Ba thẻ thiếu thốn có dấu gạch'), ('question', 'Thẻ câu hỏi giàu ngang người Mỹ, ghi theo video tham chiếu'), ('disclaimer', 'Dòng mở đầu: bản dựng lại để so sánh, số liệu theo video tham chiếu, chưa kiểm chứng')],
     [('chips', 'không giàu, không mỏ', 'reveal three deficit chips', 'Ba điều Singapore không có.'),
      ('question', 'vì sao vậy nhỉ', 'pop question card', 'Nghịch lý cần giải thích.')]),
    ('02', 'obligation_timeline', ['c3'],
     'Năm 1965, Singapore bị tách khỏi Malaysia. Thủ tướng Lý Quang Diệu khóc ngay trên truyền hình. Mà nói thật, nhìn hoàn cảnh lúc đó thì khóc cũng phải.',
     'Mốc thời gian 1965: xuất phát điểm khó khăn.',
     [('year', 'Năm 1965 cỡ lớn'), ('split', 'Hai khối Malaysia và Singapore tách nhau'), ('note', 'Chú thích Lý Quang Diệu khóc trên truyền hình')],
     [('year', 'Năm 1965', 'count-in year', 'Mốc thời gian.'),
      ('split', 'bị tách khỏi Malaysia', 'slide two blocks apart', 'Sự kiện chính trị: tách khỏi Malaysia.'),
      ('note', 'khóc ngay trên truyền hình', 'reveal note card', 'Lời kể của video tham chiếu.')]),
    ('03', 'asset_grid', ['c4'],
     'Đất thì ít, tài nguyên thì không, dân thì nghèo, nói chung là toang. Nhưng có một thứ Singapore có mà không ai giành được, đó là vị trí.',
     'Trừ ba thiếu thốn, chỉ ra thứ duy nhất còn lại: vị trí.',
     [('cards', 'Ba thẻ: đất ít, không tài nguyên, dân nghèo'), ('strike', 'Gạch ngang ba thẻ'), ('position', 'Thẻ vị trí nổi bật')],
     [('cards', 'Đất thì ít', 'deal three cards', 'Ba thiếu thốn.'),
      ('strike', 'nói chung là toang', 'strike through cards', 'Những thứ này không phải lợi thế.'),
      ('position', 'đó là vị trí', 'highlight position card', 'Lợi thế duy nhất.')]),
    ('04', 'map_route', ['c5'],
     'Các bạn nhìn nè, tàu chở dầu từ Trung Đông, tàu chở hàng từ châu Âu, muốn qua Trung Quốc, Nhật, Hàn thì đường ngắn nhất là đi qua eo biển Malacca. Và cửa ra của eo biển này nằm sát ngay Singapore.',
     'Sơ đồ minh họa tuyến tàu qua eo biển và vị trí Singapore ở cửa ra.',
     [('west', 'Điểm xuất phát Trung Đông và châu Âu'), ('east', 'Điểm đến Trung Quốc, Nhật, Hàn'), ('ships', 'Tàu minh họa chạy qua eo biển'), ('strait', 'Nút thắt eo biển Malacca'), ('sg', 'Ghim Singapore ở cửa ra')],
     [('ships', 'tàu chở dầu từ Trung Đông', 'ships travel west to east', 'Tuyến đường ngắn nhất.'),
      ('strait', 'eo biển Malacca', 'narrow the channel and label it', 'Nút thắt giao thông.'),
      ('sg', 'nằm sát ngay Singapore', 'drop pin at the exit', 'Cửa ra sát Singapore.')]),
    ('05', 'stat_callout', ['c6'],
     'Mỗi năm có rất nhiều chuyến tàu đi ngang, chở khoảng một phần tư hàng hóa buôn bán của cả thế giới.',
     'Nhấn quy mô: một phần tư thương mại thế giới, theo video tham chiếu.',
     [('stream', 'Dòng tàu đi ngang'), ('quarter', 'Một phần tư trên bốn ô')],
     [('stream', 'rất nhiều chuyến tàu', 'stream of ships', 'Lưu lượng lớn.'),
      ('quarter', 'một phần tư hàng hóa', 'fill one of four cells', 'Tỷ lệ một phần tư.')]),
    ('06', 'transaction_flow', ['c7'],
     'Có điều tàu chạy ngang thì không trả đồng nào, nên Singapore phải làm sao cho tàu muốn ghé vào. Họ xây cảng thật lớn, bốc dỡ thật nhanh, phí hợp lý.',
     'Vấn đề: tàu đi ngang không mang lại tiền; giải pháp: cảng hấp dẫn.',
     [('pass', 'Tàu đi ngang, nhãn không trả phí'), ('port', 'Cảng Singapore'), ('perks', 'Ba nhãn: lớn, nhanh, phí hợp lý')],
     [('pass', 'không trả đồng nào', 'ship passes by, zero label', 'Đi ngang không tạo doanh thu.'),
      ('port', 'xây cảng thật lớn', 'port builds up', 'Cảng là sản phẩm.'),
      ('perks', 'bốc dỡ thật nhanh', 'reveal three perks', 'Lý do tàu muốn ghé.')]),
    ('07', 'transaction_flow', ['c8'],
     'Tàu lớn ghé vào thả container, tàu nhỏ chở đi khắp khu vực. Hàng Việt Nam mình hồi trước cũng ghé đây đổi tàu rất nhiều. Giờ nó là một trong những cảng container bận rộn nhất thế giới.',
     'Mô hình trung chuyển: tàu lớn thả container, tàu nhỏ phân phối.',
     [('big', 'Tàu lớn thả container'), ('small', 'Tàu nhỏ chở đi khu vực'), ('vn', 'Nhãn hàng Việt Nam'), ('badge', 'Huy hiệu cảng bận rộn, ghi theo video tham chiếu')],
     [('big', 'Tàu lớn ghé vào thả container', 'big ship drops containers', 'Chuyển container vào cảng.'),
      ('small', 'tàu nhỏ chở đi khắp khu vực', 'small ships fan out', 'Phân phối đi khu vực.'),
      ('vn', 'Hàng Việt Nam', 'label one lane Việt Nam', 'Ví dụ trong video tham chiếu.'),
      ('badge', 'bận rộn nhất thế giới', 'pop badge', 'Kết luận về quy mô cảng, theo video tham chiếu.')]),
    ('08', 'transaction_flow', ['c9'],
     'Đoạn này mới hay nè, Singapore không có nổi một giọt dầu, vậy mà lại là trung tâm lọc dầu lớn bậc nhất châu Á. Dầu thô chạy ngang thì mua vào, lọc thành xăng, dầu máy bay, rồi bán ngược lại cho cả khu vực. Không có hàng thì đi mua hàng của người khác về gia công lại.',
     'Cơ chế lọc dầu: mua dầu thô, lọc, bán lại.',
     [('nowell', 'Giọt dầu bằng không'), ('crude', 'Dầu thô đi vào, nhãn mua'), ('refinery', 'Nhà máy lọc dầu'), ('products', 'Xăng và dầu máy bay đi ra, nhãn bán')],
     [('nowell', 'không có nổi một giọt dầu', 'show zero wells', 'Không có nguồn dầu nội địa.'),
      ('crude', 'Dầu thô chạy ngang thì mua vào', 'crude flows in with buy label', 'Dòng tiền mua vào.'),
      ('refinery', 'lọc thành xăng, dầu máy bay', 'refinery processes', 'Gia công tạo giá trị.'),
      ('products', 'bán ngược lại cho cả khu vực', 'products flow out with sell label', 'Dòng tiền bán ra.')]),
    ('09', 'asset_grid', ['c10'],
     'Bước cuối cùng là làm cho tiền muốn ở lại. Luật lệ rõ ràng, tham nhũng bị xử rất nặng. Ai cũng nói tiếng Anh, thuế lại thấp.',
     'Bốn điều kiện khiến tiền muốn ở lại.',
     [('title', 'Tiêu đề bước cuối cùng'), ('cards', 'Bốn thẻ: luật rõ, xử nặng tham nhũng, tiếng Anh, thuế thấp')],
     [('title', 'tiền muốn ở lại', 'reveal title', 'Mục tiêu của bước cuối.'),
      ('cards', 'Luật lệ rõ ràng', 'deal four cards', 'Bốn điều kiện.')]),
    ('10', 'cashflow', ['c11'],
     'Thế là các tập đoàn lớn đặt trụ sở châu Á ở đây, tiền của ngân hàng và giới nhà giàu cũng kéo về. Từ chỗ cho tàu ghé, Singapore thành chỗ cho tiền ghé.',
     'Tiền chảy về Singapore; chuyển từ chỗ cho tàu ghé sang chỗ cho tiền ghé.',
     [('hq', 'Thẻ tập đoàn đặt trụ sở'), ('money', 'Token tiền minh họa từ ngân hàng và nhà giàu'), ('swap', 'Biểu tượng tàu đổi thành đồng tiền')],
     [('hq', 'đặt trụ sở châu Á', 'card flies into hub', 'Trụ sở đặt tại Singapore.'),
      ('money', 'tiền của ngân hàng', 'tokens flow to hub', 'Dòng tiền minh họa, không theo số liệu.'),
      ('swap', 'Từ chỗ cho tàu ghé', 'ship icon turns into coin', 'Chuyển vai trò: tàu ghé thành tiền ghé.')]),
    ('11', 'asset_grid', ['c12'],
     'Tóm lại, Singapore giàu nhờ ba thứ. Một là đứng đúng chỗ. Hai là biến cái chỗ đó thành dịch vụ mà ai đi ngang cũng phải dùng. Ba là làm cho tiền thấy an toàn để ở lại.',
     'Tổng kết ba lý do.',
     [('one', 'Thẻ một: đứng đúng chỗ'), ('two', 'Thẻ hai: biến vị trí thành dịch vụ'), ('three', 'Thẻ ba: tiền thấy an toàn')],
     [('one', 'Một là', 'reveal card one', 'Lý do một.'),
      ('two', 'Hai là', 'reveal card two', 'Lý do hai.'),
      ('three', 'Ba là', 'reveal card three', 'Lý do ba.')]),
    ('12', 'stat_callout', [],
     'Có chỗ nào làm được như vậy không?',
     'Câu hỏi mở: mở rộng sang các nơi khác (không có lời kêu gọi của kênh gốc).',
     [('ask', 'Câu hỏi mở')],
     [('ask', 'Có chỗ nào', 'pop question', 'Mở rộng sang các nơi khác.')]),
]


def build():
    claim_rows = [{
        'id': cid, 'type': 'attributed', 'status': 'pending', 'source_ids': [REF],
        'text': f'Video tham chiếu nói rằng {what} (đoạn {ts} s, phiên âm ASR). Sự thật bên dưới chưa được đối chiếu nguồn khác.',
    } for cid, ts, what in CLAIMS]
    beats = []
    for bid, kind, claims, narration, purpose, layers, events in BEATS:
        beats.append({
            'id': bid, 'narration': narration, 'purpose': purpose, 'scene_type': kind,
            'claim_ids': claims, 'asset_ids': [],
            'audio_path': f'audio/beat_{bid}.wav', 'clip_path': f'scenes/beat_{bid}.mp4', 'tail_s': 0.35,
            'layers': [{'id': i, 'role': r} for i, r in layers],
            'events': [{'target': t, 'trigger_phrase': p, 'action': a, 'meaning': m} for t, p, a, m in events],
        })
    return {
        'version': '1.0', 'title': 'Vì sao Singapore giàu: dựng lại từ video tham chiếu singapore.mp4',
        'mode': 'full', 'format': {'width': 720, 'height': 1280, 'fps': 30},
        'approvals': {'story': 'approved', 'pilot': 'approved'},
        'sources': SOURCES, 'claims': claim_rows, 'assets': [], 'beats': beats,
    }


if __name__ == '__main__':
    doc = build()
    for b in doc['beats']:
        for e in b['events']:
            assert e['trigger_phrase'] in b['narration'], (b['id'], e['trigger_phrase'])
    (ROOT / 'project.json').write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('beats', len(doc['beats']), 'claims', len(doc['claims']))
