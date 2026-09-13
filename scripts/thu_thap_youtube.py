# -*- coding: utf-8 -*-
"""
thu_thap_youtube.py — Thu thập video nổi bật (nhiều view) từ các kênh cùng ngách
Phật giáo trên YouTube, dùng YouTube Data API v3, để làm dữ liệu tham khảo cho
các skill viết kịch bản / làm hình / làm thumbnail của kênh.

AN TOÀN: script KHÔNG chứa API key. Đọc key từ biến môi trường YOUTUBE_API_KEY
(hoặc truyền --api-key). Đây là API KEY (không phải OAuth) — chỉ đọc dữ liệu
công khai (video, thống kê view), KHÔNG đăng nhập vào tài khoản nào, không đụng
tới kênh của bạn. Xem SKILL.md để biết cách tạo API key.

CÁCH DÙNG:
  python thu_thap_youtube.py --out-dir "<duong-dan-du-an>\\nghien-cuu"
  python thu_thap_youtube.py --out-dir "...\\nghien-cuu" --config tu-khoa-khac.json
  python thu_thap_youtube.py --resolve-handle "@phatphaplinhung"   # tra channelId từ @handle
"""
import argparse
import io
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone

import requests

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

API_BASE = "https://www.googleapis.com/youtube/v3"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(SCRIPT_DIR, "tu-khoa-va-kenh.json")

DURATION_RE = re.compile(
    r"PT(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?"
)


def parse_duration_to_seconds(duration):
    m = DURATION_RE.match(duration or "")
    if not m:
        return 0
    parts = m.groupdict()
    h = int(parts["hours"] or 0)
    mi = int(parts["minutes"] or 0)
    s = int(parts["seconds"] or 0)
    return h * 3600 + mi * 60 + s


def api_get(path, api_key, params, max_retries=3, soft=False):
    """Gọi API. soft=True: gặp lỗi thì trả None (không dừng cả chương trình) —
    dùng cho phần phụ như bình luận (video có thể tắt bình luận -> 403)."""
    params = dict(params)
    params["key"] = api_key
    for attempt in range(max_retries):
        resp = requests.get(f"{API_BASE}/{path}", params=params, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code in (403, 429) and attempt < max_retries - 1 and not soft:
            print(f"  ⚠ Lỗi {resp.status_code} (có thể do quota), thử lại sau 2s...")
            time.sleep(2)
            continue
        if soft:
            return None
        try:
            detail = resp.json().get("error", {}).get("message", resp.text)
        except Exception:
            detail = resp.text
        raise SystemExit(
            f"Lỗi gọi YouTube API ({path}): {resp.status_code} — {detail}\n"
            f"Kiểm tra lại YOUTUBE_API_KEY và xem đã bật 'YouTube Data API v3' chưa (xem SKILL.md)."
        )
    return {}


def resolve_handle(api_key, handle):
    handle = handle.lstrip("@")
    data = api_get("channels", api_key, {"part": "id,snippet", "forHandle": handle})
    items = data.get("items", [])
    if not items:
        print(f"Không tìm thấy kênh cho @{handle}")
        return None
    channel_id = items[0]["id"]
    title = items[0]["snippet"]["title"]
    print(f"@{handle} -> channelId: {channel_id}  ({title})")
    return channel_id


def search_video_ids(api_key, query, order, max_results, published_after=None, channel_id=None):
    params = {
        "part": "id",
        "q": query,
        "type": "video",
        "order": order,
        "maxResults": min(max_results, 50),
        "relevanceLanguage": "vi",
        "regionCode": "VN",
        "safeSearch": "none",
    }
    if published_after:
        params["publishedAfter"] = published_after
    if channel_id:
        params["channelId"] = channel_id
    data = api_get("search", api_key, params)
    return [item["id"]["videoId"] for item in data.get("items", []) if item.get("id", {}).get("videoId")]


def fetch_video_details(api_key, video_ids):
    results = []
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i + 50]
        data = api_get("videos", api_key, {
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(chunk),
        })
        results.extend(data.get("items", []))
    return results


def build_record(item):
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    content = item.get("contentDetails", {})
    duration_s = parse_duration_to_seconds(content.get("duration", ""))
    thumbs = snippet.get("thumbnails", {})
    best_thumb = thumbs.get("maxres") or thumbs.get("high") or thumbs.get("medium") or thumbs.get("default") or {}
    view = int(stats.get("viewCount", 0) or 0)
    like = int(stats.get("likeCount", 0) or 0)
    comment = int(stats.get("commentCount", 0) or 0)
    return {
        "video_id": item.get("id"),
        "title": snippet.get("title", ""),
        "channel_id": snippet.get("channelId", ""),
        "channel_title": snippet.get("channelTitle", ""),
        "published_at": snippet.get("publishedAt", ""),
        "description_excerpt": (snippet.get("description", "") or "")[:300],
        "tags": snippet.get("tags", []),
        "view_count": view,
        "like_count": like,
        "comment_count": comment,
        "engagement_like_pct": round(100 * like / view, 3) if view else 0,
        "engagement_comment_pct": round(100 * comment / view, 3) if view else 0,
        "duration_seconds": duration_s,
        "duration_minutes": round(duration_s / 60, 1),
        "thumbnail_url": best_thumb.get("url", ""),
        "url": f"https://www.youtube.com/watch?v={item.get('id')}",
        "top_comments": [],
    }


def fetch_top_comments(api_key, video_id, n):
    """Top bình luận (theo độ liên quan) của một video — proxy cho tệp khán giả
    và điều khán giả tâm đắc. Video tắt bình luận sẽ trả rỗng (không lỗi)."""
    data = api_get("commentThreads", api_key, {
        "part": "snippet",
        "videoId": video_id,
        "order": "relevance",
        "maxResults": min(n, 100),
        "textFormat": "plainText",
    }, soft=True)
    if not data:
        return []
    out = []
    for it in data.get("items", []):
        top = it.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
        out.append({
            "text": (top.get("textDisplay", "") or "").replace("\n", " ")[:400],
            "like_count": int(top.get("likeCount", 0) or 0),
            "author": top.get("authorDisplayName", ""),
        })
    return out


def fetch_channel_stats(api_key, channel_ids):
    """Thông số kênh (subs, tổng video, tổng view, quốc gia, ngày lập) — để hiểu
    quy mô kênh và gợi ý vùng khán giả (country nếu kênh có khai báo)."""
    stats = {}
    ids = [c for c in channel_ids if c]
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        data = api_get("channels", api_key, {
            "part": "snippet,statistics",
            "id": ",".join(chunk),
        }, soft=True)
        if not data:
            continue
        for it in data.get("items", []):
            st = it.get("statistics", {})
            sn = it.get("snippet", {})
            stats[it["id"]] = {
                "subscriber_count": int(st.get("subscriberCount", 0) or 0),
                "video_count": int(st.get("videoCount", 0) or 0),
                "view_count_total": int(st.get("viewCount", 0) or 0),
                "country": sn.get("country", ""),
                "channel_created": sn.get("publishedAt", ""),
            }
    return stats


def download_thumbnails(records, out_dir, count):
    os.makedirs(out_dir, exist_ok=True)
    saved = []
    for rec in records[:count]:
        url = rec.get("thumbnail_url")
        if not url:
            continue
        safe_title = re.sub(r"[^\w\-]+", "_", rec["title"])[:60]
        fname = f"{rec['view_count']:012d}_{safe_title}.jpg"
        path = os.path.join(out_dir, fname)
        try:
            resp = requests.get(url, timeout=20)
            if resp.status_code == 200:
                with open(path, "wb") as f:
                    f.write(resp.content)
                saved.append(path)
        except Exception as e:
            print(f"  ⚠ Không tải được thumbnail của '{rec['title'][:40]}...': {e}")
    return saved


def main():
    ap = argparse.ArgumentParser(description="Thu thập video nổi bật cùng ngách Phật giáo từ YouTube Data API v3.")
    ap.add_argument("--config", default=DEFAULT_CONFIG, help="File JSON từ khóa/kênh hạt giống")
    ap.add_argument("--out-dir", default=None, help="Thư mục 'nghien-cuu' của dự án để lưu kết quả")
    ap.add_argument("--api-key", default=None, help="YouTube Data API key (mặc định lấy từ biến môi trường YOUTUBE_API_KEY)")
    ap.add_argument("--resolve-handle", default=None, help="Chỉ tra channelId từ @handle rồi thoát (tiện ích, không thu thập)")
    args = ap.parse_args()

    api_key = args.api_key or os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        sys.exit("Chưa có API key. Đặt biến môi trường YOUTUBE_API_KEY (xem SKILL.md mục Chuẩn bị) "
                 "hoặc truyền --api-key.")

    if args.resolve_handle:
        resolve_handle(api_key, args.resolve_handle)
        return

    if not args.out_dir:
        sys.exit("Thiếu --out-dir (đường dẫn tới thư mục 'nghien-cuu' của dự án).")

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    keywords = config.get("tu_khoa", [])
    seed_channels = config.get("kenh_hat_giong", [])
    excluded_channels = set(config.get("loai_tru_kenh", []))
    per_keyword = int(config.get("so_video_moi_tu_khoa", 15))
    recent_days = int(config.get("so_ngay_gan_day", 90))
    thumb_count = int(config.get("so_thumbnail_tai_ve", 12))
    comment_per_video = int(config.get("so_binh_luan_moi_video", 20))
    videos_for_comments = int(config.get("so_video_lay_binh_luan", 15))

    published_after = (datetime.now(timezone.utc) - timedelta(days=recent_days)).strftime("%Y-%m-%dT%H:%M:%SZ")

    all_ids = set()
    print(f"Tìm theo {len(keywords)} từ khóa (mỗi từ khóa lấy {per_keyword} video theo lượt xem)...")
    for kw in keywords:
        print(f"  - '{kw}' (mọi thời điểm, sắp theo view)...")
        all_ids.update(search_video_ids(api_key, kw, order="viewCount", max_results=per_keyword))
        print(f"  - '{kw}' ({recent_days} ngày gần đây, sắp theo view)...")
        all_ids.update(search_video_ids(api_key, kw, order="viewCount", max_results=per_keyword,
                                         published_after=published_after))

    for ch_id in seed_channels:
        print(f"  - kênh hạt giống {ch_id} (video mới nhất)...")
        all_ids.update(search_video_ids(api_key, "", order="date", max_results=per_keyword, channel_id=ch_id))

    all_ids = list(all_ids)
    print(f"Tổng cộng {len(all_ids)} video duy nhất, đang lấy chi tiết thống kê...")
    items = fetch_video_details(api_key, all_ids)
    records = [build_record(item) for item in items]
    records = [r for r in records if r["channel_id"] not in excluded_channels]
    records.sort(key=lambda r: r["view_count"], reverse=True)

    channel_agg = {}
    for r in records:
        agg = channel_agg.setdefault(r["channel_id"], {
            "channel_title": r["channel_title"], "so_video": 0, "tong_view": 0, "view_cao_nhat": 0,
        })
        agg["so_video"] += 1
        agg["tong_view"] += r["view_count"]
        agg["view_cao_nhat"] = max(agg["view_cao_nhat"], r["view_count"])
    channels_ranked = sorted(
        [{"channel_id": cid, **agg} for cid, agg in channel_agg.items()],
        key=lambda c: c["tong_view"], reverse=True,
    )

    print("Đang lấy thông số kênh (subs, quốc gia)...")
    ch_stats = fetch_channel_stats(api_key, [c["channel_id"] for c in channels_ranked])
    for c in channels_ranked:
        c.update(ch_stats.get(c["channel_id"], {}))

    print(f"Đang lấy top {comment_per_video} bình luận cho {videos_for_comments} video nhiều view nhất "
          f"(để suy ra tệp khán giả)...")
    for r in records[:videos_for_comments]:
        r["top_comments"] = fetch_top_comments(api_key, r["video_id"], comment_per_video)

    now = datetime.now()
    date_tag = now.strftime("%Y-%m-%d")
    data_dir = os.path.join(args.out_dir, "du-lieu")
    thumb_dir = os.path.join(args.out_dir, "thumbnail-doi-thu", date_tag)
    os.makedirs(data_dir, exist_ok=True)

    snapshot = {
        "ngay_thu_thap": now.isoformat(),
        "tu_khoa_dung": keywords,
        "so_video_tong": len(records),
        "top_video": records,
        "kenh_noi_bat": channels_ranked[:20],
    }
    out_path = os.path.join(data_dir, f"{date_tag}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"✔ Đã lưu dữ liệu: {out_path}")

    saved_thumbs = download_thumbnails(records, thumb_dir, thumb_count)
    print(f"✔ Đã tải {len(saved_thumbs)} thumbnail tham khảo vào: {thumb_dir}")

    print("\nTop 10 video nhiều view nhất trong đợt thu thập này:")
    for r in records[:10]:
        print(f"  {r['view_count']:>10,} view | {r['duration_minutes']:>5.1f} phút | "
              f"{r['channel_title'][:25]:<25} | {r['title'][:60]}")


if __name__ == "__main__":
    main()
