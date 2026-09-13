# cloud-nghien-cuu — Nghiên cứu xu hướng ngách Phật giáo (bản chạy trên cloud)

Repo này là **bản đóng gói để chạy trên cloud** của skill `phatgiao-nghien-cuu`,
để flow nghiên cứu xu hướng đối thủ **tự chạy hàng tuần mà không cần bật laptop**
— hợp cho những ngày bạn đi làm không mang máy.

Cloud routine (đặt ở https://claude.ai/code/routines) sẽ:
1. Clone repo này.
2. Cài `requests`, chạy `scripts/thu_thap_youtube.py` (dùng `YOUTUBE_API_KEY` từ
   secret của môi trường cloud) để thu thập video nhiều view của các kênh cùng
   ngách.
3. Đọc dữ liệu + đối chiếu với các file trong `references/` (giọng/phong cách,
   bố cục, phong cách hình ảnh, phong cách thumbnail hiện tại của kênh).
4. **In toàn bộ báo cáo xu hướng + đề xuất cập nhật ngay trong tin nhắn kết quả
   phiên** → bạn nhận thông báo trên iPhone, mở app Claude đọc thẳng, không cần
   laptop.

## Ranh giới (giống bản local)
- Chỉ đọc dữ liệu công khai qua YouTube Data API v3 (API key, không đăng nhập).
- **KHÔNG tự sửa** file skill nào. Cloud chỉ ra báo cáo + đề xuất; việc áp dụng
  vào skill vẫn làm ở phiên trên laptop, có bạn duyệt.

## Nội dung
- `scripts/thu_thap_youtube.py` — script thu thập (giống bản local).
- `scripts/tu-khoa-va-kenh.json` — cấu hình từ khóa/kênh (sửa để tinh chỉnh).
- `references/` — bản chụp phong cách hiện tại của kênh để cloud đối chiếu.
  **Lưu ý đồng bộ:** khi bạn cập nhật các file reference gốc trong skill (sau
  khi duyệt đề xuất), nhớ copy bản mới vào đây rồi push, để cloud so sánh với
  chuẩn mới nhất (nếu không, cloud vẫn so với bản cũ).
- `requirements.txt` — chỉ cần `requests`.

## Chạy thử tại máy (giống bản local)
```
pip install -r requirements.txt
set YOUTUBE_API_KEY=AIzaSy...
python scripts/thu_thap_youtube.py --out-dir ./nghien-cuu
```

Xem `SETUP-CLOUD.md` để biết cách đưa repo lên GitHub + nạp API key vào cloud +
tạo routine.
