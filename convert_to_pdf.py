import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import textwrap

# ── フォント登録 ───────────────────────────────────────────
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))  # ゴシック（本文）
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))     # 明朝（見出し装飾）

FONT_GOTHIC = 'HeiseiKakuGo-W5'
FONT_MINCHO = 'HeiseiMin-W3'

W, H = A4
MARGIN_LEFT   = 22 * mm
MARGIN_RIGHT  = 22 * mm
MARGIN_TOP    = 25 * mm
MARGIN_BOTTOM = 20 * mm

# ── カラーパレット ─────────────────────────────────────────
NAVY     = colors.HexColor('#1B2A4A')
ACCENT   = colors.HexColor('#2E6BE6')
GOLD     = colors.HexColor('#D4A843')
LIGHT_BG = colors.HexColor('#F5F7FA')
BORDER   = colors.HexColor('#CBD5E1')
WHITE    = colors.white
DARK     = colors.HexColor('#1E293B')
MUTED    = colors.HexColor('#64748B')
CODE_BG  = colors.HexColor('#1E293B')
CODE_FG  = colors.HexColor('#E2E8F0')

# ── スタイル定義 ───────────────────────────────────────────
def make_styles():
    s = {}
    s['h2'] = ParagraphStyle('h2',
        fontName=FONT_GOTHIC, fontSize=18, leading=28,
        textColor=NAVY, spaceBefore=14*mm, spaceAfter=4*mm,
        borderPad=0, leftIndent=0)
    s['h3'] = ParagraphStyle('h3',
        fontName=FONT_GOTHIC, fontSize=13, leading=20,
        textColor=ACCENT, spaceBefore=7*mm, spaceAfter=2*mm)
    s['body'] = ParagraphStyle('body',
        fontName=FONT_GOTHIC, fontSize=10.5, leading=18,
        textColor=DARK, spaceBefore=3, spaceAfter=3,
        alignment=TA_JUSTIFY)
    s['bullet'] = ParagraphStyle('bullet',
        fontName=FONT_GOTHIC, fontSize=10.5, leading=17,
        textColor=DARK, leftIndent=12*mm, spaceBefore=1, spaceAfter=1,
        bulletIndent=6*mm)
    s['numbered'] = ParagraphStyle('numbered',
        fontName=FONT_GOTHIC, fontSize=10.5, leading=17,
        textColor=DARK, leftIndent=12*mm, spaceBefore=1, spaceAfter=1,
        bulletIndent=6*mm)
    s['quote'] = ParagraphStyle('quote',
        fontName=FONT_GOTHIC, fontSize=11, leading=19,
        textColor=NAVY, leftIndent=8*mm, rightIndent=8*mm,
        spaceBefore=4*mm, spaceAfter=4*mm, backColor=LIGHT_BG,
        borderPad=5, borderColor=ACCENT, borderWidth=0,
        borderRadius=4)
    s['code_block'] = ParagraphStyle('code_block',
        fontName=FONT_GOTHIC, fontSize=9, leading=15,
        textColor=CODE_FG, backColor=CODE_BG,
        leftIndent=5*mm, rightIndent=5*mm,
        spaceBefore=3*mm, spaceAfter=3*mm, borderPad=6)
    s['action_title'] = ParagraphStyle('action_title',
        fontName=FONT_GOTHIC, fontSize=11, leading=17,
        textColor=ACCENT, spaceBefore=2*mm, spaceAfter=1*mm)
    s['table_header'] = ParagraphStyle('table_header',
        fontName=FONT_GOTHIC, fontSize=10, leading=15,
        textColor=WHITE)
    s['table_cell'] = ParagraphStyle('table_cell',
        fontName=FONT_GOTHIC, fontSize=10, leading=15,
        textColor=DARK)
    s['caption'] = ParagraphStyle('caption',
        fontName=FONT_GOTHIC, fontSize=8.5, leading=13,
        textColor=MUTED, alignment=TA_CENTER, spaceBefore=1*mm)
    s['h4'] = ParagraphStyle('h4',
        fontName=FONT_GOTHIC, fontSize=10.5, leading=16,
        textColor=WHITE, backColor=ACCENT,
        spaceBefore=4*mm, spaceAfter=1*mm,
        leftIndent=0, borderPad=5)
    return s

STYLES = make_styles()

# ── カバーページ描画関数（onFirstPage コールバックとして使用） ──────
def draw_cover(canvas, doc):
    c = canvas
    w, h = W, H

    # 背景（ネイビー）
    c.setFillColor(NAVY)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # 上部ゴールドライン
    c.setFillColor(GOLD)
    c.rect(0, h - 8*mm, w, 8*mm, fill=1, stroke=0)

    # 下部アクセントライン
    c.setFillColor(ACCENT)
    c.rect(0, 0, w, 5*mm, fill=1, stroke=0)

    # 中央ホワイトカード
    card_y = h * 0.28
    card_h = h * 0.52
    card_x = 18*mm
    card_w = w - 36*mm
    c.setFillColor(WHITE)
    c.roundRect(card_x, card_y, card_w, card_h, 6, fill=1, stroke=0)

    # アクセント左バー
    c.setFillColor(ACCENT)
    c.rect(card_x, card_y, 3.5, card_h, fill=1, stroke=0)

    # タイトル（カード内）
    title_lines = ['節約より稼ぐ：', 'AIを使って月3万円の収入を作る', '最初の30日間ロードマップ']
    c.setFillColor(NAVY)
    c.setFont(FONT_GOTHIC, 20)
    y = card_y + card_h - 20*mm
    for line in title_lines:
        c.drawCentredString(w / 2, y, line)
        y -= 12*mm

    # サブタイトル帯
    sub_y = y - 6*mm
    c.setFillColor(LIGHT_BG)
    c.roundRect(card_x + 10*mm, sub_y - 6*mm, card_w - 20*mm, 14*mm, 3, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.setFont(FONT_GOTHIC, 12)
    c.drawCentredString(w / 2, sub_y - 0.5*mm, '〜税金に負けない収入を作る〜')

    # 区切り線
    line_y = sub_y - 14*mm
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(card_x + 10*mm, line_y, card_x + card_w - 10*mm, line_y)

    # キャッチコピー
    c.setFillColor(MUTED)
    c.setFont(FONT_GOTHIC, 10)
    catch = '固定資産税・住民税に削られた貯蓄を、AIの力で取り戻す。'
    c.drawCentredString(w / 2, line_y - 10*mm, catch)

    # 下部ラベル帯
    c.setFillColor(GOLD)
    c.rect(card_x, card_y, card_w, 14*mm, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont(FONT_GOTHIC, 11)
    c.drawCentredString(w / 2, card_y + 4*mm, '30〜50代の会社員・主婦のための副業入門書')

    # フッターテキスト
    c.setFillColor(WHITE)
    c.setFont(FONT_GOTHIC, 9)
    c.drawCentredString(w / 2, 12*mm, '© 2026  All rights reserved.')


# ── ヘッダー・フッター ─────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    # フッター：ページ番号
    canvas.setFont(FONT_GOTHIC, 9)
    canvas.setFillColor(MUTED)
    page_num = doc.page
    canvas.drawCentredString(W / 2, 12*mm, f'— {page_num} —')
    # フッター：書名
    canvas.setFont(FONT_GOTHIC, 8)
    canvas.drawString(MARGIN_LEFT, 12*mm, '節約より稼ぐ：AIを使って月3万円の収入を作る')
    # ヘッダーライン
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_LEFT, H - 16*mm, W - MARGIN_RIGHT, H - 16*mm)
    canvas.restoreState()

def on_cover(canvas, doc):
    pass  # カバーはフッターなし

# ── Markdown パーサー ──────────────────────────────────────
def escape_xml(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))

def apply_inline(text):
    """**bold**, `code` をタグに変換"""
    text = escape_xml(text)
    # bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # inline code
    text = re.sub(r'`([^`]+)`', r'<font name="HeiseiKakuGo-W5" color="#2E6BE6"><b>\1</b></font>', text)
    return text

def parse_table(lines):
    """マークダウンテーブルをReportLabのTableに変換"""
    rows = []
    for line in lines:
        if re.match(r'^\s*\|[-| :]+\|\s*$', line):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        rows.append(cells)
    if not rows:
        return None

    col_count = len(rows[0])
    col_width = (W - MARGIN_LEFT - MARGIN_RIGHT - 4*mm) / col_count

    table_data = []
    for i, row in enumerate(rows):
        if i == 0:
            table_data.append([
                Paragraph(apply_inline(c), STYLES['table_header']) for c in row
            ])
        else:
            table_data.append([
                Paragraph(apply_inline(c), STYLES['table_cell']) for c in row
            ])

    t = Table(table_data, colWidths=[col_width] * col_count, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t

def make_checklist_item(text):
    """- [ ] を✅チェックボックス付きリストに"""
    text = re.sub(r'^\[ \]\s*', '□ ', text)
    return Paragraph('　' + apply_inline(text), STYLES['bullet'])

def parse_md(md_text):
    """Markdown → Platypus Flowables リスト
    H4(####) ブロックは KeepTogether で囲み、ページ途中で分断されないようにする。
    """
    story = []
    sec_buf = []      # H4セクション用バッファ
    buf_is_h4 = False # バッファがH4で始まっているか

    def flush_buf(add_hr=False):
        """バッファをstoryに追加。H4始まりならKeepTogether で包む。"""
        nonlocal sec_buf, buf_is_h4
        if sec_buf:
            if buf_is_h4 and len(sec_buf) > 1:
                story.append(KeepTogether(sec_buf))
            else:
                story.extend(sec_buf)
        sec_buf = []
        buf_is_h4 = False
        if add_hr:
            story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER,
                                    spaceBefore=2*mm, spaceAfter=2*mm))

    def emit(flowable):
        sec_buf.append(flowable)

    lines = md_text.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    table_lines = []
    in_table = False

    while i < len(lines):
        line = lines[i]

        # ── コードブロック ──────────────────────────────
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lines = []
            else:
                in_code_block = False
                emit(Spacer(1, 1*mm))
                for cl in code_lines:
                    safe = escape_xml(cl) if cl.strip() else '　'
                    emit(Paragraph(safe, STYLES['code_block']))
                emit(Spacer(1, 1*mm))
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # ── テーブル ────────────────────────────────────
        if line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            i += 1
            continue
        else:
            if in_table:
                in_table = False
                t = parse_table(table_lines)
                if t:
                    emit(Spacer(1, 3*mm))
                    emit(t)
                    emit(Spacer(1, 3*mm))
                table_lines = []

        # ── H2：新章ページ ──────────────────────────────
        if line.startswith('## '):
            flush_buf()
            text = line[3:].strip()
            story.append(PageBreak())
            story.append(Spacer(1, 4*mm))
            story.append(HRFlowable(width='100%', thickness=3, color=ACCENT, spaceAfter=2*mm))
            story.append(Paragraph(apply_inline(text), STYLES['h2']))
            story.append(HRFlowable(width='100%', thickness=1, color=BORDER,
                                    spaceBefore=1*mm, spaceAfter=3*mm))
            i += 1
            continue

        # ── H3 ──────────────────────────────────────────
        if line.startswith('### '):
            flush_buf()
            text = line[4:].strip()
            story.append(Paragraph(apply_inline(text), STYLES['h3']))
            i += 1
            continue

        # ── H4：アクションブロック開始 ──────────────────
        if line.startswith('#### '):
            flush_buf()           # 前のバッファを先にflush
            buf_is_h4 = True
            text = line[5:].strip()
            emit(Spacer(1, 2*mm))
            emit(Paragraph(apply_inline(text), STYLES['h4']))
            i += 1
            continue

        # ── H1（表紙タイトルはskip） ─────────────────────
        if line.startswith('# '):
            i += 1
            continue

        # ── 水平線：バッファをflushしてHRを追加 ─────────
        if re.match(r'^---+$', line.strip()):
            flush_buf(add_hr=True)
            i += 1
            continue

        # ── 引用（blockquote） ──────────────────────────
        if line.startswith('> '):
            text = line[2:].strip()
            emit(Paragraph(apply_inline(text), STYLES['quote']))
            i += 1
            continue

        # ── チェックリスト ──────────────────────────────
        if re.match(r'^- \[[ x]\]', line):
            text = re.sub(r'^- \[[ x]\]\s*', '', line)
            emit(make_checklist_item(text))
            i += 1
            continue

        # ── 番号なしリスト ──────────────────────────────
        if line.startswith('- ') or line.startswith('* '):
            text = line[2:].strip()
            emit(Paragraph('・　' + apply_inline(text), STYLES['bullet']))
            i += 1
            continue

        # ── 番号付きリスト ──────────────────────────────
        m = re.match(r'^(\d+)\.\s+(.+)', line)
        if m:
            emit(Paragraph(f'{m.group(1)}.　' + apply_inline(m.group(2).strip()),
                           STYLES['numbered']))
            i += 1
            continue

        # ── 空行 ────────────────────────────────────────
        if line.strip() == '':
            emit(Spacer(1, 3*mm))
            i += 1
            continue

        # ── 通常段落 ────────────────────────────────────
        if line.strip():
            emit(Paragraph(apply_inline(line.strip()), STYLES['body']))

        i += 1

    # 末尾バッファとテーブルをflush
    flush_buf()
    if in_table and table_lines:
        t = parse_table(table_lines)
        if t:
            story.append(t)

    return story


# ── メイン ────────────────────────────────────────────────
def main():
    input_path  = '/Users/shiro/ebook-ai/ebook_draft.md'
    output_path = '/Users/shiro/ebook-ai/ebook_final.pdf'

    with open(input_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title='節約より稼ぐ：AIを使って月3万円の収入を作る最初の30日間ロードマップ',
        author='',
    )

    story = []

    # ページ1はカバー（draw_cover が onFirstPage で描画）
    # PageBreak でカバーページを確定し、本文をページ2から開始
    story.append(PageBreak())

    # ページ2〜：本文
    story.extend(parse_md(md_text))

    doc.build(
        story,
        onFirstPage=draw_cover,   # ページ1にカバーを描画
        onLaterPages=on_page,     # ページ2以降にヘッダー・フッター
    )
    print(f'✅ PDF生成完了: {output_path}')

if __name__ == '__main__':
    main()
