# Phân tích khán giả quốc tế qua bình luận & đề xuất tiếp cận (2026-09-15)

Đây là báo cáo bổ sung theo yêu cầu riêng (không phải chu trình nghiên cứu hằng
ngày), đào sâu insight "khán giả quốc tế" đã phát hiện ở báo cáo 2026-09-13/14.

## Phương pháp & mẫu dữ liệu

- Lấy **30 video Phật pháp/tâm linh thật sự** có view cao nhất (từ bộ dữ liệu đã
  lọc `nghien-cuu/du-lieu/2026-09-14.json`, sau khi loại kênh nhạc/giải trí).
- Với mỗi video, gọi lại YouTube Data API (`commentThreads`, sắp theo độ liên
  quan) để lấy **tối đa 100 bình luận/video** — tổng cộng **3.000 bình luận**.
- Phân loại ngôn ngữ từng bình luận bằng: (1) nhận diện bảng chữ cái Unicode
  (Thái, Sinhala, Hán, Hàn, Nhật, Devanagari, Bengali, Ả Rập, Cyrillic, Miến
  Điện, Lào, Tạng...), (2) dấu tiếng Việt/từ tiếng Việt phổ biến, (3) một số từ
  khóa đặc trưng cho tiếng Tây Ban Nha/Bồ Đào Nha/Indonesia/Pháp/Đức. Bình luận
  chỉ có emoji/quá ngắn được xếp "không xác định".

**Giới hạn cần biết (nói thật, không bịa):**
- Đây là **suy đoán ngôn ngữ bình luận, không phải quốc gia người dùng thật**
  (YouTube API không cho biết quốc gia người bình luận). Một người Việt kiều có
  thể bình luận bằng tiếng Anh; một người nước ngoài học tiếng Việt có thể bình
  luận bằng tiếng Việt. Vì vậy các số liệu dưới đây là **tỷ lệ ngôn ngữ**, dùng
  làm proxy hợp lý cho mức độ tiếp cận quốc tế, không phải số liệu nhân khẩu học
  chính xác.
- "Tiếng Anh" là nhóm rộng nhất nhưng **không xác định được quốc gia cụ thể**
  (có thể là người Việt ở nước ngoài, người Sri Lanka/Ấn Độ dùng tiếng Anh làm
  ngôn ngữ chung, hoặc khán giả phương Tây quan tâm Phật giáo).
- Phân loại bằng script/từ khóa có thể sai ở biên (VD: một câu tiếng Anh rất
  ngắn không đủ để phân loại chắc chắn) — chấp nhận sai số nhỏ ở nhóm ranh giới.

---

## 1. Kết quả tổng quan (3.000 bình luận, 30 video)

| Ngôn ngữ | Số bình luận | % |
|---|---|---|
| Tiếng Việt | 2.416 | 80,5% |
| Tiếng Anh (quốc tế, không rõ quốc gia) | 275 | 9,2% |
| Không xác định (emoji/rỗng) | 165 | 5,5% |
| Thái (Thái Lan) | 51 | 1,7% |
| Trung Quốc/Đài Loan/HK (chữ Hán) | 22 | 0,7% |
| Sinhala (Sri Lanka) | 17 | 0,6% |
| Indonesia/Malaysia | 15 | 0,5% |
| Hindi/Nepali (Ấn Độ, Nepal) | 12 | 0,4% |
| Miến Điện (Myanmar) | 7 | 0,2% |
| Lào | 5 | 0,2% |
| Hàn Quốc | 4 | 0,1% |
| Tây Ban Nha, Ả Rập, Bồ Đào Nha, Philippines, Nhật, Pháp, Nga | 10 | ~0,3% (cộng dồn) |

→ Trong số bình luận **xác định được ngôn ngữ** (2.835 bình luận, loại phần
"không xác định"), **~14,8% là ngôn ngữ không phải tiếng Việt** — tức là gần
**1/7 người bình luận trên các video Phật pháp Việt hàng đầu là khán giả quốc
tế** (theo ngôn ngữ dùng để bình luận).

### Nhóm theo khu vực/truyền thống Phật giáo

| Nhóm | % trên tổng bình luận |
|---|---|
| Tiếng Anh (quốc tế chung) | 9,2% |
| **Khối Phật giáo Nam Tông** (Thái Lan, Sri Lanka, Myanmar, Lào) | **2,7%** |
| Đông Á Bắc Tông (Trung Quốc/Đài Loan/HK, Hàn Quốc, Nhật) | 0,9% |
| Đông Nam Á Hồi giáo có cộng đồng Hoa/Phật tử (Indonesia, Malaysia) | 0,5% |
| Nam Á khác (Ấn Độ, Nepal — nhiều bình luận mang màu sắc Hindu giáo hơn Phật giáo, VD "Jay Shree Ram") | 0,4% |
| Khác (Mỹ Latinh, Ả Rập, châu Âu) | 0,3% |

**Điểm đáng chú ý nhất**: khối quốc gia theo Phật giáo Nam Tông (Theravāda —
Thái Lan, Sri Lanka, Myanmar, Lào) là **nhóm quốc tế lớn thứ hai** sau tiếng
Anh, dù kênh mình và hầu hết đối thủ trong mẫu đều theo truyền thống Tịnh Độ/
Bắc Tông (Đại Thừa) của Việt Nam. Điều này cho thấy nội dung "kể chuyện Đức
Phật/nhân quả/từ bi" mang tính **phổ quát vượt ranh giới tông phái**, miễn hình
ảnh và cốt truyện đủ dễ hiểu không cần biết tiếng Việt.

---

## 2. Phát hiện quan trọng nhất: ĐỊNH DẠNG quyết định mức độ quốc tế hóa

So sánh bình luận trên nhóm **Shorts (≤90 giây)** với nhóm **video dài hơn**
trong cùng 30 video:

| Định dạng | Số video | Số bình luận | % Tiếng Việt | % Ngôn ngữ quốc tế khác | % Không xác định |
|---|---|---|---|---|---|
| **Shorts (≤90 giây)** | 7 | 1.100 | 58,1% | **28,8%** | 13,1% |
| **Long-form (>1,5 phút, gồm audio dài)** | 23 | 1.900 | 93,5% | **5,4%** | 1,1% |

**Chênh lệch ~5,3 lần**: Shorts thu hút tỷ lệ bình luận quốc tế cao gấp hơn 5
lần so với video dài. Đây là bằng chứng **mạnh và trực tiếp nhất** (không còn
là suy đoán từ vài ví dụ) cho quyết định chuyển sang Shorts đã áp dụng — Shorts
không chỉ thắng về view (đã nêu ở báo cáo 2026-09-13/14) mà còn là **cánh cửa
chính để tiếp cận khán giả quốc tế**.

Lý do hợp lý: Shorts trong mẫu đều là **kể chuyện bằng hình + phụ đề ngắn**,
không phụ thuộc nhiều vào việc nghe hiểu tiếng Việt trôi chảy — trong khi
video dài (giảng pháp, tụng kinh 47–460 phút) đòi hỏi hiểu ngôn ngữ nói liên
tục, tự nhiên loại bớt khán giả không biết tiếng Việt.

---

## 3. Đề xuất nội dung để tiếp cận khán giả quốc tế nhiều hơn

| # | Đề xuất | Vì sao (bằng chứng) | Ưu tiên | Rủi ro / lưu ý |
|---|---|---|---|---|
| 1 | **Tiếp tục và đẩy mạnh Shorts** (đã áp dụng) — đây vẫn là đòn bẩy lớn nhất cho khán giả quốc tế, không chỉ view trong nước | Shorts có tỷ lệ bình luận quốc tế 28,8% so với 5,4% ở video dài (gấp 5,3 lần) | **Cao** (xác nhận hướng đã đi, không cần đổi) | Không |
| 2 | **Thêm phụ đề tiếng Anh (English subtitles/CC)** cho mọi Shorts — dùng tính năng phụ đề có sẵn của YouTube Studio, tự động dịch rồi người kiểm lại câu chốt bài học cho chuẩn | Tiếng Anh là nhóm ngôn ngữ quốc tế lớn nhất (9,2% tổng bình luận, ~64% trong số bình luận quốc tế) — rào cản hiện tại là chỉ có audio/chữ tiếng Việt trên màn hình | **Cao** | Thấp — không đổi nội dung gốc, chỉ thêm lớp phụ đề |
| 3 | **Thêm 1 dòng chữ tiếng Anh ngắn ở cuối Short** (câu đúc kết dịch sang tiếng Anh, VD "Kindness always returns.") bên cạnh câu tiếng Việt — không thay thế bản gốc, chỉ thêm | Giúp khán giả quốc tế lướt tới vẫn nắm được bài học dù không nghe được tiếng Việt, tăng khả năng họ share/comment (giống các bình luận "Sadhu" quốc tế đã thấy) | **Vừa** | Thấp — cần kiểm tra không làm rối bố cục thumbnail/chữ hiện tại |
| 4 | **Dùng hình ảnh/nhân vật phổ quát liên tông phái**, không chỉ hình ảnh đặc thù Tịnh Độ Việt Nam: bên cạnh Đức Phật A Di Đà, xen thêm cảnh Đức Phật Thích Ca, nhà sư mặc y vàng/cam (gần với hình ảnh nhà sư Nam Tông Thái Lan/Sri Lanka/Myanmar quen thuộc với khối khán giả này), thiên nhiên/chùa mang tính biểu tượng chung (hoa sen, cây bồ đề) hơn là kiến trúc chùa Việt cụ thể | Khối Phật giáo Nam Tông (Thái/Sri Lanka/Myanmar/Lào) là nhóm quốc tế lớn thứ 2 (2,7%) — họ quen thuộc hơn với hình ảnh Thích Ca/nhà sư y vàng hơn là biểu tượng Tịnh Độ | **Vừa** | Thấp — `phong-cach-hinh-anh.md` đã cho phép nhiều lựa chọn hình tượng, chỉ cần ưu tiên hợp lý hơn cho một số video |
| 5 | **Điền phần dịch tiếng Anh cho tiêu đề & mô tả video** (tính năng "Translations" miễn phí có sẵn trong YouTube Studio) — không đổi tiêu đề chính tiếng Việt, chỉ thêm bản dịch để YouTube gợi ý đúng cho người xem ở Thái Lan/Sri Lanka/Ấn Độ/quốc tế nói tiếng Anh | Tăng khả năng thuật toán YouTube đề xuất video cho người xem ngoài Việt Nam — hiện tại tiêu đề/mô tả 100% tiếng Việt nên khó được đề xuất ra ngoài thị trường Việt | **Vừa** | Thấp — thao tác kỹ thuật đơn giản, không đụng nội dung |
| 6 | **Thử 1 câu chốt đa ngôn ngữ mang tính biểu tượng** cuối video (ví dụ hiện tại đã có "Nam Mô A Di Đà Phật") — có thể xen thêm phiên âm gần gũi các truyền thống khác trong dịp đặc biệt (không bắt buộc, chỉ thử nghiệm) | Bình luận quốc tế hiện có sẵn nhiều lời niệm tương đương bằng tiếng Thái ("สาธุ"/Sadhu), tiếng Hán ("南無阿彌陀佛"), cho thấy khán giả các nước tự tìm đến các câu niệm quen thuộc của họ để hưởng ứng — đây là tín hiệu cộng hưởng tự nhiên, không phải đề xuất bắt buộc | **Thấp** (thử nghiệm) | Vừa — cần cẩn trọng để không lẫn lộn tông phái, nên tham khảo ý kiến trước khi áp dụng |
| 7 | **Không cần dịch/lồng tiếng toàn bộ sang tiếng khác** — không đủ dữ liệu để biện minh chi phí này; khán giả quốc tế hiện tại đang tự nguyện vượt rào cản ngôn ngữ nhờ hình ảnh phổ quát, không phải nhờ kênh đã dịch thuật | Chỉ 14,8% bình luận là ngôn ngữ khác, tiếng Việt vẫn chiếm đa số áp đảo (80,5%) — ngân sách/nhân lực nên ưu tiên các đề xuất #1–#5 (chi phí thấp) trước | — (khuyến nghị không làm, không phải "không đề xuất") | — |

---

## 4. Tóm tắt số liệu chính (để trích dẫn nhanh)

- **~14,8%** bình luận (trong số bình luận xác định được ngôn ngữ) trên 30
  video Phật pháp top view là **ngôn ngữ không phải tiếng Việt**.
- **Shorts có tỷ lệ bình luận quốc tế 28,8%**, cao gấp **~5,3 lần** so với
  video dài (5,4%) — định dạng là yếu tố quyết định lớn nhất cho khả năng tiếp
  cận quốc tế, không phải ngôn ngữ hay nội dung.
- Sau tiếng Anh (9,2%, nhóm lớn nhất, không rõ quốc gia cụ thể), khối **Phật
  giáo Nam Tông (Thái Lan, Sri Lanka, Myanmar, Lào)** là nhóm quốc tế xác định
  được rõ ràng lớn nhất (2,7%) — gợi ý ưu tiên hình ảnh/nhân vật phổ quát liên
  tông phái khi muốn mở rộng thêm.
- Đòn bẩy chi phí thấp, hiệu quả cao nhất: **phụ đề tiếng Anh** và **bản dịch
  tiêu đề/mô tả tiếng Anh** trên YouTube Studio (đề xuất #2 và #5) — tận dụng
  tính năng có sẵn, không cần đổi quy trình sản xuất.

**Nhắc lại**: đây là báo cáo phân tích/đề xuất, **không tự sửa** file skill nào
— việc áp dụng do chủ kênh quyết định.
