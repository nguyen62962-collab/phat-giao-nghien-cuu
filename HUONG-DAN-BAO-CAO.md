# Hướng dẫn viết báo cáo (cho bản chạy trên cloud)

Đây là bản rút gọn của mục "Sau khi thu thập" trong skill `phatgiao-nghien-cuu`,
dành cho routine cloud. Cloud đọc file này rồi làm theo.

## Triết lý (bất di bất dịch)
- **Học từ thị trường, không từ ý thích ban đầu của chủ kênh.** Nếu kênh nhiều
  view làm khác mặc định hiện tại → đề xuất đổi theo thị trường.
- **Tìm ĐIỂM HỘI TỤ**: điều gì lặp lại giống nhau ở nhiều kênh top → công thức
  ăn khách, ưu tiên bắt chước.
- **Học FORMAT/PHONG CÁCH, không sao chép NỘI DUNG** (không chép kịch bản, không
  tải tài sản của họ).
- **2 lằn ranh BẤT BIẾN, thị trường không ghi đè:** (1) chuẩn xác giáo lý,
  (2) faceless (không lộ mặt).

## Giới hạn dữ liệu khi chạy trên cloud (nói thật, đừng bịa)
- **Tệp khán giả đối thủ**: API không cho lấy nhân khẩu học kênh người khác →
  chỉ **suy đoán** từ `top_comments` + tiêu đề nhắm tuổi + `country` của kênh.
  Luôn ghi rõ "suy đoán".
- **Giọng đọc / nhạc nền / cách edit / b-roll**: cloud KHÔNG xem được video mẫu
  (không có trình duyệt). Ghi các mục này là **"chưa kiểm — cần bước xem mẫu thủ
  công trên máy"**, KHÔNG bịa nhận xét.
- **Thumbnail**: PHÂN TÍCH ĐƯỢC — dùng tool Read để mở từng ảnh trong
  `nghien-cuu/thumbnail-doi-thu/<ngay>/` và nhận xét bằng vision.

## Các bước
1. Tìm file JSON mới nhất trong `nghien-cuu/du-lieu/` (tên `<ngay>.json`), đọc.
2. Đọc các file trong `references/` để biết hiện trạng kênh đang làm gì
   (giọng/phong cách, bố cục, hình ảnh, thumbnail).
3. Mở và phân tích từng ảnh thumbnail trong `nghien-cuu/thumbnail-doi-thu/<ngay>/`.
4. Viết báo cáo (cũng lưu ra `nghien-cuu/bao-cao/<ngay>.md` trong checkout để
   tham chiếu) gồm các mục:
   - **1. Top video theo view** — bảng: tiêu đề, kênh, view, %like, phút, ngày, link.
   - **2. Kênh nổi bật & tệp khán giả (suy đoán)** — subs/quốc gia + đọc
     `top_comments`: khán giả có vẻ là ai, tâm đắc câu gì (câu được like nhiều).
   - **3. Điểm hội tụ theo từng yếu tố** — với mỗi yếu tố nêu *điều nhiều kênh
     top cùng làm*: tiêu đề (khuôn/từ mở đề/lợi ích), chủ đề, độ dài, văn phong/
     hook, thumbnail (từ vision). Giọng/nhạc/edit/b-roll: ghi "chưa kiểm".
   - **4. Đối chiếu hiện trạng kênh** — mỗi điểm hội tụ: kênh mình giống hay khác
     (so với `references/`).
   - **5. Đề xuất cập nhật cụ thể** (quan trọng nhất) — bảng: File đích | Sửa gì |
     Bằng chứng (hội tụ ở mấy kênh, view TB) | Ưu tiên (cao/vừa/thấp) | Rủi ro.
     File đích là các skill: phatgiao-script (references/*.md), phatgiao-tts,
     phatgiao-visual, phatgiao-video, phatgiao-thumbnail.
5. **KHÔNG tự sửa** bất kỳ file skill nào — chỉ ra đề xuất. Việc áp dụng do chủ
   kênh duyệt ở một phiên riêng trên máy.

## Mức rủi ro (giúp chủ kênh duyệt nhanh)
- **Thấp** (duyệt gộp): màu/bố cục thumbnail, công thức tiêu đề, ngân hàng chủ
  đề, độ dài mục tiêu, gợi ý nhạc nền, tham số zoom/pan, tốc độ giọng.
- **Cao** (xem kỹ từng cái): đụng giáo lý/nội dung Phật pháp, tông giọng thương
  hiệu, bỏ một lằn ranh gốc.

## Giao báo cáo
Cloud không ghi được vào máy cá nhân, nên **IN TOÀN BỘ BÁO CÁO trong tin nhắn
kết quả cuối phiên** để chủ kênh đọc trên điện thoại. Kết bằng tóm tắt <150 từ:
3–5 phát hiện đáng chú ý nhất + các đề xuất ưu tiên cao.
