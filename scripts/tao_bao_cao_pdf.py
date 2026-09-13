# -*- coding: utf-8 -*-
"""
tao_bao_cao_pdf.py — Ghép dữ liệu thu thập được (JSON) + báo cáo phân tích
(Markdown, do Claude viết) thành MỘT file PDF trực quan: có biểu đồ, bảng số
liệu, và toàn bộ nội dung phân tích/đề xuất — để chủ kênh xem trên điện thoại
và ra quyết định nhanh, không cần đọc JSON hay markdown thô.

CÁCH DÙNG:
  python tao_bao_cao_pdf.py --json <duong-dan>/du-lieu/<ngay>.json \
      --markdown <duong-dan>/bao-cao/<ngay>.md \
      --out <duong-dan>/bao-cao/<ngay>.pdf \
      [--thumb-dir <duong-dan>/thumbnail-doi-thu/<ngay>/]

Không có internet, không cần API key — chỉ xử lý file đã có sẵn tại chỗ.
"""
import argparse
import io
import json
import os
import re
import sys
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from fpdf import FPDF
from PIL import Image
from fpdf.enums import XPos, YPos

# multi_cell trong fpdf2 (mới) mặc định KHÔNG đưa con trỏ về lề trái sau khi in
# xong (khác hành vi fpdf cổ điển) — bọc lại để mọi đoạn văn/tiêu đề luôn xuống
# dòng và về lề trái, tránh lỗi "Not enough horizontal space" ở đoạn kế tiếp.
def mc(pdf, h, txt, **kw):
    return pdf.multi_cell(0, h, txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT, **kw)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(SCRIPT_DIR, "assets", "fonts")
FONT_REGULAR = os.path.join(FONT_DIR, "DejaVuSans.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

MAU_CHINH = "#B8860B"    # vàng nghệ, đồng bộ tông kênh
MAU_PHU = "#8B4513"      # nâu ấm
MAU_NHAN = "#C8102E"     # đỏ đậm (đồng bộ thumbnail)


def _dat_font_bieu_do():
    """Dùng DejaVu Sans cho matplotlib để chữ tiếng Việt trong biểu đồ không vỡ."""
    fm.fontManager.addfont(FONT_REGULAR)
    fm.fontManager.addfont(FONT_BOLD)
    plt.rcParams["font.family"] = fm.FontProperties(fname=FONT_REGULAR).get_name()
    plt.rcParams["axes.unicode_minus"] = False


def dinh_dang_so(n):
    try:
        return f"{int(n):,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(n)


def phan_loai_dinh_dang(phut):
    if phut < 1.5:
        return "Shorts (<1.5p)"
    if phut <= 4:
        return "Mid-form (1.5–4p)"
    if phut <= 30:
        return "Long-form ngắn (4–30p)"
    return "Long-form dài (>30p)"


def ve_bieu_do(data, out_dir):
    """Sinh các file PNG biểu đồ, trả về list (đường_dẫn, chú_thích)."""
    _dat_font_bieu_do()
    os.makedirs(out_dir, exist_ok=True)
    bieu_do = []
    videos = data.get("top_video", [])
    kenh = sorted(data.get("kenh_noi_bat", []), key=lambda c: -c.get("tong_view", 0))

    # 1. Top kênh theo tổng view
    if kenh:
        top_k = kenh[:10][::-1]
        ten = [k["channel_title"][:28] for k in top_k]
        view = [k["tong_view"] for k in top_k]
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(ten, view, color=MAU_CHINH)
        ax.set_xlabel("Tổng view trong mẫu thu thập")
        ax.set_title("Top 10 kênh theo tổng view")
        for i, v in enumerate(view):
            ax.text(v, i, f" {dinh_dang_so(v)}", va="center", fontsize=8)
        fig.tight_layout()
        p = os.path.join(out_dir, "bieu_do_top_kenh.png")
        fig.savefig(p, dpi=150)
        plt.close(fig)
        bieu_do.append((p, "Top 10 kênh theo tổng view trong đợt thu thập này."))

    # 2. So sánh theo định dạng (độ dài video)
    if videos:
        nhom = {}
        for v in videos:
            loai = phan_loai_dinh_dang(v.get("duration_minutes", 0))
            nhom.setdefault(loai, []).append(v)
        thu_tu = ["Shorts (<1.5p)", "Mid-form (1.5–4p)", "Long-form ngắn (4–30p)", "Long-form dài (>30p)"]
        nhan, view_tb, like_tb, so_luong = [], [], [], []
        for loai in thu_tu:
            vids = nhom.get(loai, [])
            if not vids:
                continue
            nhan.append(f"{loai}\n(n={len(vids)})")
            view_tb.append(sum(v["view_count"] for v in vids) / len(vids))
            like_tb.append(sum(v.get("engagement_like_pct", 0) for v in vids) / len(vids))
            so_luong.append(len(vids))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
        ax1.bar(nhan, view_tb, color=MAU_CHINH)
        ax1.set_title("View trung bình theo định dạng")
        ax1.set_yscale("log")
        ax1.tick_params(axis="x", labelsize=8)
        for i, v in enumerate(view_tb):
            ax1.text(i, v, dinh_dang_so(v), ha="center", va="bottom", fontsize=7)

        ax2.bar(nhan, like_tb, color=MAU_NHAN)
        ax2.set_title("%like trung bình theo định dạng")
        ax2.tick_params(axis="x", labelsize=8)
        for i, v in enumerate(like_tb):
            ax2.text(i, v, f"{v:.2f}%", ha="center", va="bottom", fontsize=7)

        fig.tight_layout()
        p = os.path.join(out_dir, "bieu_do_dinh_dang.png")
        fig.savefig(p, dpi=150)
        plt.close(fig)
        bieu_do.append((p, "So sánh view trung bình và %like trung bình theo từng nhóm độ dài video — "
                           "cho thấy định dạng nào đang hiệu quả nhất trong ngách."))

    # 3. Phân tán view theo thời lượng (để thấy khoảng trống định dạng)
    if videos:
        durs = [max(v.get("duration_minutes", 0.01), 0.01) for v in videos]
        views = [max(v.get("view_count", 1), 1) for v in videos]
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(durs, views, alpha=0.5, color=MAU_PHU, edgecolors="none")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Thời lượng video (phút, log scale)")
        ax.set_ylabel("Lượt xem (log scale)")
        ax.set_title("Phân tán: Lượt xem theo thời lượng video")
        ax.axvspan(8, 25, color=MAU_CHINH, alpha=0.15)
        ax.text(11, ax.get_ylim()[1] * 0.5, "Khoảng độ dài\nkênh hiện tại\n(8–25 phút)",
                fontsize=8, color=MAU_PHU)
        fig.tight_layout()
        p = os.path.join(out_dir, "bieu_do_phan_tan.png")
        fig.savefig(p, dpi=150)
        plt.close(fig)
        bieu_do.append((p, "Mỗi chấm là một video. Vùng tô vàng là khoảng độ dài kênh đang làm — "
                           "xem có đối thủ nào cùng khoảng đó đạt view cao không."))

    # 4. Top 15 video theo view
    if videos:
        top_v = sorted(videos, key=lambda v: -v["view_count"])[:15][::-1]
        nhan = [f"{v['title'][:38]}…" if len(v['title']) > 38 else v['title'] for v in top_v]
        view = [v["view_count"] for v in top_v]
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.barh(nhan, view, color=MAU_NHAN)
        ax.set_xlabel("Lượt xem")
        ax.set_title("Top 15 video theo lượt xem (đợt thu thập này)")
        ax.tick_params(axis="y", labelsize=7)
        fig.tight_layout()
        p = os.path.join(out_dir, "bieu_do_top_video.png")
        fig.savefig(p, dpi=150)
        plt.close(fig)
        bieu_do.append((p, "Top 15 video nhiều view nhất — có thể lẫn vài video ngoài ngách do trùng từ khóa, "
                           "xem tên kênh để tự lọc."))

    return bieu_do


def ghep_luoi_thumbnail(thumb_dir, out_path, max_images=12, cols=3):
    """Ghép các ảnh thumbnail đối thủ đã tải (nếu có) thành một bảng ảnh (contact
    sheet) để nhúng vào PDF. Chỉ hoạt động khi thumb_dir tồn tại và có ảnh — khi
    chạy trên cloud (mạng bị chặn tải ảnh), hàm này tự trả None, PDF bỏ qua
    trang này chứ không báo lỗi."""
    if not thumb_dir or not os.path.isdir(thumb_dir):
        return None
    files = sorted(
        [f for f in os.listdir(thumb_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))],
        reverse=True,
    )[:max_images]
    if not files:
        return None

    cell_w, cell_h, pad = 320, 180, 10
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cell_w + pad) + pad, rows * (cell_h + pad) + pad), "white")
    for idx, fname in enumerate(files):
        try:
            img = Image.open(os.path.join(thumb_dir, fname)).convert("RGB")
        except Exception:
            continue
        img.thumbnail((cell_w, cell_h))
        x = pad + (idx % cols) * (cell_w + pad)
        y = pad + (idx // cols) * (cell_h + pad)
        offset_x = x + (cell_w - img.width) // 2
        offset_y = y + (cell_h - img.height) // 2
        sheet.paste(img, (offset_x, offset_y))
    sheet.save(out_path, quality=85)
    return out_path


# ---------- Xử lý markdown đơn giản (đủ dùng cho báo cáo có cấu trúc cố định) ----------

def parse_markdown(text):
    blocks = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith("### "):
            blocks.append(("h3", line[4:].strip()))
        elif line.startswith("## "):
            blocks.append(("h2", line[3:].strip()))
        elif line.startswith("# "):
            blocks.append(("h1", line[2:].strip()))
        elif line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            rows = [
                [c.strip() for c in l.strip("|").split("|")]
                for l in table_lines
                if not re.match(r"^\|?[\s\-:|]+\|?$", l)
            ]
            if rows:
                blocks.append(("table", rows))
            continue
        elif line.strip().startswith(("- ", "* ")):
            bullets = []
            while i < len(lines) and lines[i].strip().startswith(("- ", "* ")):
                bullets.append(lines[i].strip()[2:].strip())
                i += 1
            blocks.append(("bullets", bullets))
            continue
        elif line.strip() == "---":
            blocks.append(("hr", None))
        else:
            para = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "-", "*", "|")) and lines[i].strip() != "---":
                para.append(lines[i].rstrip())
                i += 1
            blocks.append(("p", " ".join(para)))
            continue
        i += 1
    return blocks


def _sach_markdown_inline(s):
    """Bỏ ký hiệu **đậm**/*nghiêng*/`code` cho gọn (fpdf2 không cần rich text)."""
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    return s


class BaoCaoPDF(FPDF):
    def __init__(self):
        super().__init__(format="A4")
        self.add_font("DejaVu", "", FONT_REGULAR)
        self.add_font("DejaVu", "B", FONT_BOLD)
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVu", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, "Báo cáo nghiên cứu xu hướng — phatgiao-nghien-cuu", align="R")
        self.ln(12)

    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Trang {self.page_no()}", align="C")


def trang_bia(pdf, data, ngay):
    pdf.add_page()
    pdf.set_font("DejaVu", "B", 22)
    pdf.set_text_color(139, 69, 19)
    pdf.ln(30)
    mc(pdf, 12, "Báo cáo nghiên cứu xu hướng\nngách Phật giáo YouTube", align="C")
    pdf.ln(6)
    pdf.set_font("DejaVu", "", 13)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, ngay, align="C")
    pdf.ln(20)
    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(0, 0, 0)
    so_video = data.get("so_video_tong", len(data.get("top_video", [])))
    so_kenh = len(data.get("kenh_noi_bat", []))
    so_tukhoa = len(data.get("tu_khoa_dung", []))
    mc(pdf, 8,
        f"Nguồn dữ liệu: YouTube Data API v3\n"
        f"Số video phân tích: {dinh_dang_so(so_video)}\n"
        f"Số kênh nổi bật: {so_kenh}\n"
        f"Số từ khóa tìm kiếm: {so_tukhoa}\n",
        align="C")


def trang_bieu_do(pdf, bieu_do):
    for path, chu_thich in bieu_do:
        pdf.add_page()
        pdf.set_font("DejaVu", "B", 13)
        pdf.ln(2)
        w = 180
        pdf.image(path, x=(210 - w) / 2, w=w)
        pdf.ln(4)
        pdf.set_font("DejaVu", "", 9)
        pdf.set_text_color(90, 90, 90)
        mc(pdf, 5, chu_thich, align="C")
        pdf.set_text_color(0, 0, 0)


def _ve_hang_dau_bang(pdf, header_cells, col_w):
    pdf.set_font("DejaVu", "B", 8)
    pdf.set_fill_color(184, 134, 11)
    pdf.set_text_color(255, 255, 255)
    x0, y0 = pdf.l_margin, pdf.get_y()
    for j, c in enumerate(header_cells):
        pdf.set_xy(x0 + j * col_w, y0)
        pdf.cell(col_w, 7, c[:40], border=1, fill=True)
    pdf.set_xy(x0, y0 + 7)
    pdf.set_font("DejaVu", "", 7.5)
    pdf.set_text_color(0, 0, 0)


def render_table(pdf, rows, so_dong_toi_da=60):
    """Vẽ bảng, tự ngắt trang THỦ CÔNG (không dựa vào auto_page_break của fpdf2 —
    auto_page_break giữa lúc đang vẽ dở một dòng sẽ làm mỗi ô văng ra một trang
    riêng, tạo hàng chục trang gần như trắng). Bảng quá dài bị cắt bớt kèm ghi
    chú, để PDF luôn gọn và đọc được trên điện thoại."""
    if not rows:
        return
    n_col = len(rows[0])
    page_w = pdf.w - 2 * pdf.l_margin
    col_w = page_w / n_col
    body_rows = rows[1:]
    bi_cat_bot = len(body_rows) > so_dong_toi_da
    if bi_cat_bot:
        body_rows = body_rows[:so_dong_toi_da]

    auto_cu = pdf.auto_page_break, pdf.b_margin
    pdf.set_auto_page_break(auto=False)

    _ve_hang_dau_bang(pdf, rows[0], col_w)
    fill = False
    for row in body_rows:
        pdf.set_fill_color(245, 240, 230) if fill else pdf.set_fill_color(255, 255, 255)
        cell_texts = [_sach_markdown_inline(c)[:120] for c in row[:n_col]]
        max_h = 6
        for txt in cell_texts:
            lines = pdf.multi_cell(col_w, 4.5, txt, border=0, dry_run=True, output="LINES")
            max_h = max(max_h, 4.5 * len(lines))

        # Hết chỗ trên trang hiện tại -> sang trang mới, vẽ lại tiêu đề bảng
        if pdf.get_y() + max_h > pdf.h - pdf.b_margin:
            pdf.add_page()
            _ve_hang_dau_bang(pdf, rows[0], col_w)

        x_start, y_start = pdf.l_margin, pdf.get_y()
        for j, txt in enumerate(cell_texts):
            pdf.set_xy(x_start + j * col_w, y_start)
            pdf.multi_cell(col_w, 4.5, txt, border=1, fill=True)
        pdf.set_xy(x_start, y_start + max_h)
        fill = not fill

    pdf.set_auto_page_break(auto=auto_cu[0], margin=auto_cu[1])

    if bi_cat_bot:
        pdf.ln(2)
        pdf.set_font("DejaVu", "", 8)
        pdf.set_text_color(120, 120, 120)
        mc(pdf, 5, f"(đã cắt bớt — chỉ hiện {so_dong_toi_da}/{len(rows) - 1} dòng đầu để PDF gọn)")
        pdf.set_text_color(0, 0, 0)


def render_markdown_blocks(pdf, blocks):
    pdf.add_page()
    for kind, content in blocks:
        if kind == "h1":
            pdf.set_font("DejaVu", "B", 16)
            pdf.set_text_color(139, 69, 19)
            pdf.ln(4)
            mc(pdf, 9, _sach_markdown_inline(content))
            pdf.set_text_color(0, 0, 0)
        elif kind == "h2":
            pdf.set_font("DejaVu", "B", 13)
            pdf.set_text_color(184, 134, 11)
            pdf.ln(3)
            mc(pdf, 8, _sach_markdown_inline(content))
            pdf.set_text_color(0, 0, 0)
        elif kind == "h3":
            pdf.set_font("DejaVu", "B", 11)
            pdf.ln(2)
            mc(pdf, 7, _sach_markdown_inline(content))
        elif kind == "p":
            pdf.set_font("DejaVu", "", 10)
            mc(pdf, 5.5, _sach_markdown_inline(content))
            pdf.ln(1)
        elif kind == "bullets":
            pdf.set_font("DejaVu", "", 10)
            for b in content:
                pdf.set_x(pdf.l_margin + 4)
                mc(pdf, 5.5, f"•  {_sach_markdown_inline(b)}")
            pdf.ln(1)
        elif kind == "table":
            render_table(pdf, content)
            pdf.ln(3)
        elif kind == "hr":
            pdf.ln(2)
            y = pdf.get_y()
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.ln(4)


def main():
    ap = argparse.ArgumentParser(description="Ghép JSON + báo cáo Markdown thành PDF trực quan.")
    ap.add_argument("--json", required=True, help="File JSON snapshot từ thu_thap_youtube.py")
    ap.add_argument("--markdown", default=None, help="File .md báo cáo phân tích (nếu có)")
    ap.add_argument("--out", required=True, help="Đường dẫn file .pdf xuất ra")
    ap.add_argument("--thumb-dir", default=None,
                     help="Thư mục ảnh thumbnail đã tải (nghien-cuu/thumbnail-doi-thu/<ngay>/). "
                          "Có ảnh thì PDF thêm trang bảng ảnh; không có/rỗng thì tự bỏ qua "
                          "(vd. khi chạy trên cloud bị chặn tải ảnh).")
    args = ap.parse_args()

    with open(args.json, "r", encoding="utf-8") as f:
        data = json.load(f)

    ngay = data.get("ngay_thu_thap", datetime.now().isoformat())[:10]
    out_dir = os.path.dirname(os.path.abspath(args.out))
    charts_dir = os.path.join(out_dir, f"_charts_{ngay}")

    print("Đang vẽ biểu đồ...")
    bieu_do = ve_bieu_do(data, charts_dir)
    print(f"  -> {len(bieu_do)} biểu đồ")

    print("Đang ghép bảng ảnh thumbnail đối thủ (nếu có)...")
    luoi_anh = ghep_luoi_thumbnail(args.thumb_dir, os.path.join(charts_dir, "luoi_thumbnail.png"))
    if luoi_anh:
        bieu_do.append((luoi_anh, "Thumbnail của các video nhiều view nhất trong đợt thu thập — "
                                    "tham khảo màu sắc, bố cục chữ, kiểu ảnh nền đang được dùng nhiều."))
        print("  -> đã ghép")
    else:
        print("  -> không có ảnh (bỏ qua trang này)")

    pdf = BaoCaoPDF()
    trang_bia(pdf, data, ngay)
    trang_bieu_do(pdf, bieu_do)

    if args.markdown and os.path.exists(args.markdown):
        with open(args.markdown, "r", encoding="utf-8") as f:
            md_text = f.read()
        blocks = parse_markdown(md_text)
        render_markdown_blocks(pdf, blocks)
    else:
        print("  (không có file markdown phân tích kèm theo — PDF chỉ có biểu đồ + số liệu thô)")

    os.makedirs(out_dir, exist_ok=True)
    pdf.output(args.out)
    print(f"✔ Đã tạo PDF: {args.out}")

    # dọn ảnh biểu đồ tạm sau khi đã nhúng vào PDF
    import shutil
    shutil.rmtree(charts_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
