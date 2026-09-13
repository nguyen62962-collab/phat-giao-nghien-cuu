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

## Bước bắt buộc: xuất PDF trực quan (sau khi viết xong .md)
Chủ kênh xem báo cáo trên điện thoại để RA QUYẾT ĐỊNH nhanh — không muốn đọc
markdown/JSON thô. Sau khi file `.md` ở bước 4 đã hoàn chỉnh, chạy:
```
python scripts/tao_bao_cao_pdf.py \
  --json nghien-cuu/du-lieu/<ngay>.json \
  --markdown nghien-cuu/bao-cao/<ngay>.md \
  --out nghien-cuu/bao-cao/<ngay>.pdf
```
Script tự vẽ biểu đồ (top kênh theo view, so sánh view/%like theo định dạng
video, phân tán view-theo-thời lượng, top 15 video) và ghép với toàn bộ nội
dung phân tích trong file `.md` thành MỘT file PDF nhiều trang, có trang bìa,
bảng, biểu đồ màu. Không cần internet, không cần API key ở bước này — chỉ xử
lý file JSON/Markdown đã có sẵn. Nếu script lỗi, đọc thông báo lỗi, sửa nếu là
lỗi rõ ràng (thiếu thư viện: `pip install matplotlib fpdf2`); nếu không sửa
được nhanh, vẫn giữ lại file `.md` làm bản dự phòng và báo rõ lỗi cho chủ kênh.

## Lưu kết quả lại (BẮT BUỘC — nếu không làm, báo cáo sẽ mất khi sandbox đóng)
`nghien-cuu/bao-cao/` KHÔNG bị `.gitignore` (chỉ `du-lieu/` và
`thumbnail-doi-thu/` bị ignore vì là dữ liệu thô tái tạo được). Sau khi có cả
`.md` và `.pdf`, commit và đẩy thẳng lên `main`:
```
git add nghien-cuu/bao-cao/
git commit -m "Báo cáo nghiên cứu xu hướng <ngay>"
git push origin HEAD:main
```
Nếu `git push` bị chặn (branch protection, quyền ghi hạn chế...), đừng thử lại
nhiều lần — báo rõ cho chủ kênh biết đã commit local nhưng chưa push được, và
nêu lý do lỗi cụ thể.

## Giao báo cáo
1. Sau khi push thành công, thông báo rõ **đường dẫn file PDF trong repo**
   (dạng `nghien-cuu/bao-cao/<ngay>.pdf`) để chủ kênh mở bằng app GitHub hoặc
   trình duyệt trên điện thoại.
2. Cloud không gửi file đính kèm được qua tin nhắn, nên vẫn **IN TOÀN BỘ NỘI
   DUNG file `.md`** (nguyên văn, không rút gọn/tóm tắt thay thế) ngay trong
   tin nhắn kết quả cuối phiên — để chủ kênh có bản dự phòng đọc ngay cả khi
   chưa mở được PDF. Đây là yêu cầu bắt buộc, không được thay bằng bản tóm tắt.
3. Kết thúc bằng một tóm tắt <150 từ: 3–5 phát hiện đáng chú ý nhất + các đề
   xuất ưu tiên cao — đặt SAU phần nguyên văn ở mục 2, không thay thế nó.
