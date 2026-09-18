# -*- coding: utf-8 -*-
"""
ket_noi_youtube_analytics.py — Kết nối YouTube Analytics API bằng OAuth để
phân tích DỮ LIỆU RIÊNG TƯ của chính kênh bạn (watch time, subscriber gained/
lost, traffic source, top video theo kênh của bạn...).

KHÁC VỚI thu_thap_youtube.py: script đó dùng API KEY, chỉ đọc dữ liệu công
khai của kênh ĐỐI THỦ (view, thống kê kênh). Script NÀY dùng OAuth 2.0 đăng
nhập bằng chính tài khoản Google quản lý kênh của bạn, vì dữ liệu Analytics là
riêng tư — API key thường không đọc được.

BƯỚC 1 — Tạo OAuth Client (làm 1 lần, trên trình duyệt bất kỳ):
  1. Vào https://console.cloud.google.com/ , chọn đúng project đã tạo
     YOUTUBE_API_KEY trước đó (hoặc tạo project mới).
  2. Vào "APIs & Services" > "Library" > bật thêm "YouTube Analytics API"
     (bên cạnh "YouTube Data API v3" đã bật sẵn).
  3. Vào "APIs & Services" > "Credentials" > "Create Credentials" >
     "OAuth client ID" > chọn loại ứng dụng "Desktop app" > đặt tên tuỳ ý.
  4. Nếu được hỏi cấu hình "OAuth consent screen": chọn "External", điền tên
     ứng dụng bất kỳ, email của bạn — không cần gửi duyệt Google vì chỉ bạn
     tự dùng (chọn "Testing" và thêm chính email Gmail quản lý kênh vào danh
     sách "Test users").
  5. Tải file JSON credentials về, đổi tên thành "client_secret.json", đặt
     vào thư mục "secrets/" ở gốc repo (tạo thư mục này nếu chưa có). File
     này KHÔNG được đẩy lên GitHub (đã có trong .gitignore).

BƯỚC 2 — Đăng nhập (BẮT BUỘC LÀM TRÊN MÁY CÓ TRÌNH DUYỆT, đăng nhập đúng
tài khoản Google quản lý kênh YouTube của bạn — máy tính cá nhân, KHÔNG chạy
được trên phiên cloud này vì cloud không có trình duyệt):
    python scripts/ket_noi_youtube_analytics.py --dang-nhap
  Lệnh sẽ tự mở trình duyệt, bạn đăng nhập + bấm "Cho phép". Sau khi xong,
  token được lưu vào "secrets/youtube_analytics_token.json" (cũng không được
  đẩy lên GitHub). Chỉ cần làm bước này 1 lần (token tự làm mới sau đó).
  Nếu muốn phiên cloud sau này tự phân tích được, hãy copy thủ công file
  token đó lên môi trường cloud (coi như mật khẩu, không dán vào chat/commit).

BƯỚC 3 — Phân tích (chạy được cả trên máy cá nhân lẫn cloud, sau khi đã có
token từ Bước 2):
    python scripts/ket_noi_youtube_analytics.py --so-ngay 28
  Xuất báo cáo tổng quan (view, watch time, subscriber, top video, nguồn
  traffic) ra nghien-cuu/du-lieu-kenh-minh/<ngay>.json (thư mục này bị
  .gitignore vì là dữ liệu riêng tư, tái tạo được bằng cách chạy lại).
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
SECRETS_DIR = os.path.join(REPO_ROOT, "secrets")
CLIENT_SECRET_PATH = os.path.join(SECRETS_DIR, "client_secret.json")
TOKEN_PATH = os.path.join(SECRETS_DIR, "youtube_analytics_token.json")

SCOPES = [
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube.readonly",
]


def dang_nhap():
    """Chạy luồng OAuth — chỉ chạy được trên máy có trình duyệt."""
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        sys.exit("Thiếu thư viện. Chạy: pip install -r requirements.txt")

    if not os.path.exists(CLIENT_SECRET_PATH):
        sys.exit(
            f"Không tìm thấy {CLIENT_SECRET_PATH}.\n"
            "Xem hướng dẫn BƯỚC 1 ở đầu file script này để tạo OAuth client "
            "trên Google Cloud Console rồi tải client_secret.json vào đúng "
            "đường dẫn trên."
        )
    os.makedirs(SECRETS_DIR, exist_ok=True)
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
    print("Sắp mở trình duyệt để bạn đăng nhập bằng tài khoản Google quản lý kênh YouTube...")
    creds = flow.run_local_server(port=0)
    with open(TOKEN_PATH, "w", encoding="utf-8") as f:
        f.write(creds.to_json())
    print(f"✔ Đăng nhập thành công. Token đã lưu vào {TOKEN_PATH}")
    print("  (Giữ kín file này như mật khẩu — không đẩy lên GitHub, không dán vào chat.)")


def lay_creds():
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
    except ImportError:
        sys.exit("Thiếu thư viện. Chạy: pip install -r requirements.txt")

    if not os.path.exists(TOKEN_PATH):
        sys.exit(
            f"Chưa có token ở {TOKEN_PATH}.\n"
            "Chạy trước: python scripts/ket_noi_youtube_analytics.py --dang-nhap "
            "(nhớ làm trên máy có trình duyệt, xem BƯỚC 2 ở đầu file)."
        )
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return creds


def phan_tich(so_ngay):
    from googleapiclient.discovery import build

    creds = lay_creds()
    yt_analytics = build("youtubeAnalytics", "v2", credentials=creds)
    yt_data = build("youtube", "v3", credentials=creds)

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=so_ngay)
    s, e = start_date.isoformat(), end_date.isoformat()

    print(f"Đang lấy dữ liệu kênh từ {s} đến {e}...")

    # Thông tin kênh (tên, subs hiện tại) — dùng Data API, "mine=True"
    ch = yt_data.channels().list(part="snippet,statistics", mine=True).execute()
    channel_info = ch.get("items", [{}])[0]

    # Tổng quan theo ngày
    overview = yt_analytics.reports().query(
        ids="channel==MINE",
        startDate=s, endDate=e,
        metrics="views,estimatedMinutesWatched,averageViewDuration,"
                "subscribersGained,subscribersLost,likes,comments,shares",
        dimensions="day",
        sort="day",
    ).execute()

    # Top video theo view trong khoảng thời gian
    top_video = yt_analytics.reports().query(
        ids="channel==MINE",
        startDate=s, endDate=e,
        metrics="views,estimatedMinutesWatched,averageViewDuration,likes,comments",
        dimensions="video",
        sort="-views",
        maxResults=25,
    ).execute()

    # Nguồn traffic (Shorts feed, tìm kiếm, đề xuất, bên ngoài...)
    traffic_source = yt_analytics.reports().query(
        ids="channel==MINE",
        startDate=s, endDate=e,
        metrics="views,estimatedMinutesWatched",
        dimensions="insightTrafficSourceType",
        sort="-views",
    ).execute()

    # Loại thiết bị xem
    device = yt_analytics.reports().query(
        ids="channel==MINE",
        startDate=s, endDate=e,
        metrics="views",
        dimensions="deviceType",
        sort="-views",
    ).execute()

    result = {
        "ngay_phan_tich": datetime.now().isoformat(),
        "khoang_thoi_gian": {"tu": s, "den": e, "so_ngay": so_ngay},
        "kenh": {
            "ten": channel_info.get("snippet", {}).get("title", ""),
            "subscriber_count": channel_info.get("statistics", {}).get("subscriberCount", ""),
            "view_count_total": channel_info.get("statistics", {}).get("viewCount", ""),
            "video_count": channel_info.get("statistics", {}).get("videoCount", ""),
        },
        "tong_quan_theo_ngay": {
            "cot": overview.get("columnHeaders", []),
            "du_lieu": overview.get("rows", []),
        },
        "top_video": {
            "cot": top_video.get("columnHeaders", []),
            "du_lieu": top_video.get("rows", []),
        },
        "nguon_traffic": {
            "cot": traffic_source.get("columnHeaders", []),
            "du_lieu": traffic_source.get("rows", []),
        },
        "loai_thiet_bi": {
            "cot": device.get("columnHeaders", []),
            "du_lieu": device.get("rows", []),
        },
    }

    out_dir = os.path.join(REPO_ROOT, "nghien-cuu", "du-lieu-kenh-minh")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{end_date.isoformat()}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✔ Đã lưu: {out_path}")
    print(f"\nKênh: {result['kenh']['ten']} — {result['kenh']['subscriber_count']} subs")
    print(f"Dữ liệu {so_ngay} ngày gần đây ({s} -> {e})")


def main():
    ap = argparse.ArgumentParser(description="Kết nối & phân tích YouTube Analytics API cho kênh của bạn.")
    ap.add_argument("--dang-nhap", action="store_true", help="Chạy luồng đăng nhập OAuth (làm trên máy có trình duyệt)")
    ap.add_argument("--so-ngay", type=int, default=28, help="Số ngày gần đây cần phân tích (mặc định 28)")
    args = ap.parse_args()

    if args.dang_nhap:
        dang_nhap()
    else:
        phan_tich(args.so_ngay)


if __name__ == "__main__":
    main()
