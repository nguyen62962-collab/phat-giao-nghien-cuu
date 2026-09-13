# Hướng dẫn viết kịch bản Shorts (cho routine cloud "viet-kich-ban-shorts")

Routine này là **Chạm 1** của dây chuyền sản xuất Shorts: chọn chủ đề → viết
kịch bản → đưa cho chủ kênh duyệt. Đọc kỹ, làm đúng từng bước.

## Triết lý (bám theo skill gốc — không được tự ý đổi)
- Kênh **chỉ làm Shorts 20–50 giây** từ 2026-09-13 (xem
  `references/giong-va-phong-cach-nganh.md` và `references/cau-truc-va-mau.md`
  mục 0).
- Dàn ý bắt buộc: **Hook 1 câu → Tình huống (nhân vật cụ thể) → Kết bất ngờ
  mang tính phước báo → 1 câu đúc kết**.
- Chuẩn xác giáo lý là bắt buộc: không bịa trích dẫn, không gán sai cho Đức
  Phật/thiền sư nếu không chắc nguồn (dùng "tương truyền rằng…").
- **TUYỆT ĐỐI KHÔNG** viết về nhân vật/tin đồn thời sự có thật chưa kiểm chứng
  (xem mục "Chủ đề CẤM" trong `references/giong-va-phong-cach-nganh.md` và
  trong `hang-doi-chu-de.md`).
- Giọng văn: ấm, tĩnh tại, xưng "bạn"/"chúng ta", có thể kết bằng nửa câu niệm
  "Nam Mô A Di Đà Phật" thay cho hồi hướng dài.

## Các bước

### Bước 1 — Chọn chủ đề
Đọc `san-xuat/hang-doi-chu-de.md`. Lấy **chủ đề đầu tiên trong mục "Chưa dùng"
chưa có dấu ✅**. Nếu mục "Chưa dùng" rỗng, tự nghĩ 1 chủ đề mới bám theo "Ngân
hàng chủ đề đã kiểm chứng" trong `references/giong-va-phong-cach-nganh.md`
(nhân quả, phước lành, từ bi, khẩu nghiệp...), nhưng **kiểm tra chéo với mục
"Chủ đề CẤM"** trước khi dùng.

### Bước 2 — Viết kịch bản
Theo đúng dàn ý mục 0 trong `references/cau-truc-va-mau.md` và định dạng đầu ra
trong skill gốc (`phatgiao-script/SKILL.md`, phần "Định dạng đầu ra" — rút gọn
3 mục HOOK/TÌNH HUỐNG/KẾT cho Shorts). Canh **20–50 giây** (~45–110 chữ, xem
bảng trong SKILL.md). Chèn `[HÌNH: ...]` ở mỗi đoạn cho khâu dựng hình. Đưa kèm
**3–5 phương án tiêu đề** theo khuôn `Lời Phật Dạy: [hành động] – [kết quả]`
(đã xác nhận đúng thị trường, xem `giong-va-phong-cach-nganh.md`).

### Bước 3 — Lưu file
Lưu vào `san-xuat/cho-duyet/<ngay-hom-nay YYYY-MM-DD>-<slug-chu-de>.md` (slug:
chữ thường, gạch nối, bỏ dấu). Nội dung file gồm:
```
# [Chủ đề gốc]

**Trạng thái:** Chờ duyệt
**Ngày tạo:** <ngay>

## Kịch bản
<toàn bộ kịch bản theo định dạng chuẩn>

## Ghi chú cho người duyệt
<1-2 câu: vì sao chọn chủ đề này, có gì cần lưu ý không (vd nguồn tích chưa
chắc chắn, dùng "tương truyền")>
```

### Bước 4 — Cập nhật hàng đợi
Trong `san-xuat/hang-doi-chu-de.md`: xoá chủ đề vừa dùng khỏi mục "Chưa dùng",
thêm dòng vào mục "Đã dùng" theo mẫu đã ghi sẵn trong file đó.

### Bước 5 — Lưu lên GitHub (bắt buộc)
```
git add san-xuat/
git commit -m "Kịch bản chờ duyệt: <ngay> — <chu-de>"
git push origin HEAD:main
```
Nếu push lỗi quyền (403), báo rõ cho chủ kênh, đừng thử lại nhiều lần (đã có
tiền lệ lỗi này — xem lịch sử commit, thường do GitHub App mất quyền ghi).

### Bước 6 — Giao cho chủ kênh duyệt
In **toàn bộ nội dung kịch bản** (nguyên văn, không tóm tắt) trong tin nhắn kết
quả cuối phiên, kèm dòng hướng dẫn rõ ràng:

> "Để duyệt kịch bản này, nhắn cho Claude (ở bất kỳ phiên nào trong dự án):
> **'duyệt kịch bản `<ten-file>`'**. Muốn sửa thì nói rõ cần đổi gì."

Không tự động coi là "đã duyệt" — việc duyệt luôn cần chủ kênh xác nhận rõ bằng
lời, ở một lượt trò chuyện khác (có thể từ điện thoại, nói với Claude trong dự
án — không nhất thiết phải là phiên cloud này).

## Ranh giới
- **KHÔNG** tự động chuyển file sang `da-duyet/` — đó là hành động chỉ làm khi
  có xác nhận "duyệt" từ chủ kênh (xem skill `phatgiao-duyet-kich-ban` trong dự
  án local).
- **KHÔNG** sửa file trong `references/` hay bất kỳ skill nào khác.
- Chỉ ghi trong `san-xuat/cho-duyet/` và cập nhật `hang-doi-chu-de.md`.
