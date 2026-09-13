# Thiết lập chạy trên cloud (làm MỘT LẦN)

Ba việc cần làm, theo thứ tự. Việc 1 và 2 cần tài khoản của bạn nên bạn tự làm;
việc 3 (tạo routine) Claude làm hộ khi đã có link repo.

## Việc 1 — Đưa repo này lên GitHub
Repo đã được `git init` + commit sẵn ở thư mục `cloud-nghien-cuu`. Bạn chỉ cần
tạo một repo trống trên GitHub rồi push lên.

1. Vào https://github.com/new → tạo repo tên vd. `phatgiao-nghien-cuu`
   → chọn **Private** (khuyên dùng, vì chứa chiến lược từ khóa của bạn)
   → KHÔNG tích "Add README" (repo này đã có sẵn file) → Create.
2. GitHub hiện lệnh "push an existing repository". Chạy trong thư mục
   `cloud-nghien-cuu` (mở terminal tại đó):
   ```
   git remote add origin https://github.com/<tên-bạn>/phatgiao-nghien-cuu.git
   git branch -M main
   git push -u origin main
   ```
   Lần đầu push sẽ hỏi đăng nhập GitHub (mở trình duyệt hoặc nhập Personal Access
   Token) — đây là đăng nhập của bạn, Claude không làm hộ.

> Nếu chọn **Private**: môi trường cloud phải được cấp quyền đọc repo này (cài
> GitHub App của Claude Code cho repo/tổ chức đó khi tạo routine — làm theo hướng
> dẫn hiện ra). Nếu muốn đơn giản nhất và không ngại lộ danh sách từ khóa, chọn
> **Public** thì cloud clone được ngay không cần cấp quyền.

## Việc 2 — Nạp YOUTUBE_API_KEY vào môi trường cloud
Cloud không đọc được biến `setx` trên máy bạn, nên phải đặt key như một **secret
của môi trường cloud**:
1. Vào https://claude.ai/code (phần Environments / Cài đặt môi trường).
2. Mở môi trường **Default** (env cloud đang dùng cho routine).
3. Thêm một biến môi trường / secret:
   - Tên: `YOUTUBE_API_KEY`
   - Giá trị: API key YouTube Data API v3 của bạn (`AIzaSy...`)
     (cách tạo key: xem mục "Chuẩn bị" trong
     `.claude/skills/phatgiao-nghien-cuu/SKILL.md`).
4. Lưu lại.

> Vì sao không nhét key vào prompt routine: prompt được lưu trong cấu hình
> routine và có thể lọt vào log — đặt làm secret của môi trường là cách an toàn.

## Việc 3 — Tạo routine (Claude làm khi có link repo)
Sau khi xong Việc 1 & 2, đưa Claude **link repo GitHub** (vd.
`https://github.com/<tên-bạn>/phatgiao-nghien-cuu`) và nói "tạo routine cloud".
Claude sẽ tạo routine chạy hàng tuần (thứ Hai sáng, giờ VN), với prompt:
- clone repo, `pip install -r requirements.txt`
- chạy script thu thập với `YOUTUBE_API_KEY` từ secret
- viết báo cáo + đề xuất, **in ra trong tin nhắn kết quả** (không tự sửa skill)
- gửi thông báo hoàn thành → bạn đọc trên iPhone

Sau khi routine tạo xong, nên bấm **Run now** một lần để kiểm tra chạy trơn
(đúng key, đúng quyền repo) trước khi trông cậy vào lịch tự động.
