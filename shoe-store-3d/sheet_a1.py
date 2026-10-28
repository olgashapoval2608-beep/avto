"""Аркуш А1 (841×594 мм) для курсової «Взуття»: план М 1:100, види моделі, експлікація, штамп."""
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image

F, OUT = sys.argv[1], sys.argv[2]
pdfmetrics.registerFont(TTFont('Serif', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('SerifB', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Sans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('SansB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
W, H = 841, 594
c = canvas.Canvas(OUT, pagesize=(W * mm, H * mm))
c.setTitle('Аркуш А1 — торговельна зала ТОВ «Взуття»')


def Y(y, h=0):          # верхній лівий кут (мм) -> координата reportlab
    return (H - y - h) * mm


def rect(x, y, w, h, lw=0.5, fill=None):
    c.setLineWidth(lw)
    if fill:
        c.setFillColor(fill)
    c.rect(x * mm, Y(y, h), w * mm, h * mm, stroke=1, fill=1 if fill else 0)
    c.setFillColorRGB(0, 0, 0)


def text(s, x, y, size=11, font='Serif', anchor='l'):
    c.setFont(font, size)
    yy = Y(y) - size * 0.35 * mm / mm * 1.0 - size * 0.62
    if anchor == 'c':
        c.drawCentredString(x * mm, Y(y) - size * 0.8, s)
    elif anchor == 'r':
        c.drawRightString(x * mm, Y(y) - size * 0.8, s)
    else:
        c.drawString(x * mm, Y(y) - size * 0.8, s)


def image_fit(path, x, y, w, h):
    im = Image.open(path).convert('RGB')
    iw, ih = im.size
    ar, br = w / h, iw / ih
    if br > ar:                     # обрізати по ширині
        nw = int(ih * ar); im = im.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
    else:
        nh = int(iw / ar); im = im.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))
    c.drawImage(ImageReader(im), x * mm, Y(y, h), w * mm, h * mm)


# рамка
rect(20, 5, 816, 584, 1.4)
text('ПРОЄКТ ТОРГОВЕЛЬНОЇ ЗАЛИ МАГАЗИНУ ВЗУТТЯ ТА АКСЕСУАРІВ ТОВ «ВЗУТТЯ»', 30, 10, 24, 'SerifB')
text('Тривимірна модель торговельної зали у SketchUp (п. 2.3, рис. 2.3–2.5). Г-подібна зала 360 м²: 16,0 × 18,5 м + виступ 6,0 × 10,7 м, висота 3,0 м',
     30, 21, 13)

# ---------- план М 1:100: ортогональний рендер 23,0 × 19,5 м -> 230 × 195 мм
px0, py0 = 37.5, 39.0                   # верхній лівий кут зображення на аркуші, мм
WX0, WY1 = 11.15 - 11.5, 9.15 + 9.75    # світові координати верхнього лівого кута
rect(30, 34, 245, 205, 0.35)
c.drawImage(ImageReader(Image.open(F + '/vz_plan.png').convert('RGB')), px0 * mm, Y(py0, 195), 230 * mm, 195 * mm)


def P(X, Yw):                            # світові м -> мм аркуша
    return px0 + (X - WX0) * 10, py0 + (WY1 - Yw) * 10


labels = [('Жіноче взуття', 8.2, 12.2, '#C2185B'), ('Чоловіче взуття', 19.1, 13.0, '#1F4E79'),
          ('Дитяче взуття', 4.4, 7.7, '#B7950B'), ('Аксесуари', 13.0, 1.9, '#6C3483'), ('Каси', 5.8, 2.2, '#333333'),
          ('Супутні товари', 5.9, 5.3, '#1E8449'), ('Літнє взуття', 14.3, 7.6, '#C2185B'), ('Вхід / вихід', 9.0, 1.9, '#000000')]
for t, X, Yw, col in labels:
    x, y = P(X, Yw)
    c.setFont('SansB', 8.5)
    tw = c.stringWidth(t, 'SansB', 8.5) / mm
    c.setFillColorRGB(1, 1, 1); c.setStrokeColor(col); c.setLineWidth(0.8)
    c.roundRect((x - tw / 2 - 1.5) * mm, Y(y - 2.2, 4.6), (tw + 3) * mm, 4.6 * mm, 1 * mm, stroke=1, fill=1)
    c.setFillColor(col); c.drawCentredString(x * mm, Y(y + 1.2), t); c.setFillColorRGB(0, 0, 0); c.setStrokeColorRGB(0, 0, 0)


def dim_h(X0, X1, Yw, off, label):       # горизонтальний розмір
    x0, y = P(X0, Yw); x1, _ = P(X1, Yw); y -= off
    c.setLineWidth(0.3); c.line(x0 * mm, Y(y), x1 * mm, Y(y))
    for xx in (x0, x1):
        c.line(xx * mm, Y(y - 1.5), xx * mm, Y(y + 1.5 + off - 2))
        c.line((xx - 1) * mm, Y(y + 1), (xx + 1) * mm, Y(y - 1))
    c.setFont('Sans', 7); c.drawCentredString((x0 + x1) / 2 * mm, Y(y - 0.8), label)


def dim_v(Y0, Y1, Xw, off, label):       # вертикальний розмір
    x, y0 = P(Xw, Y0); _, y1 = P(Xw, Y1); x -= off
    c.setLineWidth(0.3); c.line(x * mm, Y(y0), x * mm, Y(y1))
    for yy in (y0, y1):
        c.line((x - 1.5) * mm, Y(yy), (x + off - 1) * mm, Y(yy))
        c.line((x - 1) * mm, Y(yy + 1), (x + 1) * mm, Y(yy - 1))
    c.saveState(); c.translate((x - 1.2) * mm, Y((y0 + y1) / 2)); c.rotate(90)
    c.setFont('Sans', 7); c.drawCentredString(0, 0, label); c.restoreState()


dim_h(0, 22, 18.5, 3.2, '22 000')
dim_h(16, 22, 7.8, -6, '6 000')
dim_v(0, 18.5, 0, 3.5, '18 500')
dim_v(7.8, 18.5, 22, -6.5, '10 700')
dim_h(0, 16, 0, -6, '16 000')
# масштабна лінійка 0–5 м
sx, sy = 37.5, 236.5
for i in range(5):
    c.setFillColorRGB(0, 0, 0) if i % 2 == 0 else c.setFillColorRGB(1, 1, 1)
    c.rect((sx + i * 10) * mm, Y(sy, 1.6), 10 * mm, 1.6 * mm, stroke=1, fill=1)
c.setFillColorRGB(0, 0, 0); c.setFont('Sans', 6.5)
for i in range(6):
    c.drawCentredString((sx + i * 10) * mm, Y(sy + 4.2), f'{i} м' if i in (0, 5) else str(i))
text('План торговельної зали з розміщенням обладнання, М 1:100', 30, 241, 11)

# ---------- види моделі
views = [('vz_23', 290, 34, 300, 205, 'Загальний вигляд моделі (рис. 2.3)'),
         ('vz_25', 605, 34, 221, 205, 'Вигляд торговельної зали від входу (рис. 2.5)'),
         ('vzB2', 30, 255, 260, 180, 'Жіночий відділ і зона приміряння'),
         ('vz_B1', 300, 255, 260, 180, 'Чоловічий відділ у правому виступі (рис. Б.1)'),
         ('vzB5', 570, 255, 256, 180, 'Розрахунковий вузол і дитячий відділ')]
for n, x, y, w, h, cap in views:
    image_fit(f'{F}/{n}.png', x, y, w, h)
    rect(x, y, w, h, 0.35)
    text(cap, x, y + h + 2, 11)

# ---------- експлікація
tx, ty, rh = 30, 462, 7.4
text('Експлікація торговельно-технологічного обладнання', tx, ty - 8, 12, 'SerifB')
cols = [10, 138, 52, 22]
rows = [['№', 'Найменування обладнання', 'Габарити, мм', 'К-сть'],
        [1, 'Пристінна гірка для взуття', '1250×600×2200', 45], [2, 'Острівна двостороння гірка', '1500×1200×1400', 15],
        [3, 'Низький стіл-гірка для дитячого взуття', '1200×600×700', 2], [4, 'Подіум для промо-викладки', '1600×800×400', 3],
        [5, 'Скляна вітрина для аксесуарів', '1000×500×1900', 4], [6, 'Острівна вітрина-прилавок для сумок', '1200×1200×1100', 2],
        [7, 'Обертова стійка для шкарпеток і панчіх', '600×600×1600', 3], [8, 'Стійка для засобів догляду за взуттям', '600×400×1400', 1],
        [9, 'Банкетка для приміряння', '1200×450×450', 7], [10, 'Підлогове дзеркало', '600×300×1700', 7],
        [11, 'Касовий стіл (робоче місце касира)', '1600×700×1000', 3], [12, 'Стелаж касової зони', '1200×400×2000', 2],
        ['', 'Разом', '', 94]]
for ri, row in enumerate(rows):
    cx = tx
    for ci, cw in enumerate(cols):
        rect(cx, ty + ri * rh, cw, rh, 0.3, '#E6E6E6' if ri == 0 else None)
        bold = ri == 0 or ri == len(rows) - 1
        s = str(row[ci])
        if ci in (0, 3):
            text(s, cx + cw / 2, ty + ri * rh + 1.5, 9, 'SerifB' if bold else 'Serif', 'c')
        else:
            text(s, cx + 1.5, ty + ri * rh + 1.5, 9, 'SerifB' if bold else 'Serif')
        cx += cw

# ---------- умовні позначення
lx, ly = 265, 462
text('Умовні позначення', lx, ly - 8, 12, 'SerifB')
legend = [('Жіноче взуття', '#E8A0B4'), ('Чоловіче взуття', '#8DB3E2'), ('Дитяче взуття', '#F4D06F'),
          ('Аксесуари і сумки', '#B9A3D9'), ('Супутні товари', '#A8D5A2'), ('Розрахунковий вузол', '#9AA3AD'),
          ('Зона приміряння (банкетки, дзеркала)', '#D9D9D9')]
for i, (n, col) in enumerate(legend):
    rect(lx, ly + i * 9, 12, 6, 0.3, col)
    text(n, lx + 15, ly + i * 9 + 0.8, 10)
text('Площа зали 360 м²; установча площа 81,59 м²;', lx, ly + 66, 10)
text('Ку = 81,59 / 360 = 0,227 (норматив для зали 251–650 м² — 0,30).', lx, ly + 72, 10)
text('Ширина основних проходів 2,2–3,0 м.', lx, ly + 78, 10)

# ---------- основний напис 185 × 55 мм
sx, sy = 651, 534
rect(sx, sy, 185, 55, 1.0)
for dy in (11, 22, 33, 44):
    c.setLineWidth(0.3); c.line(sx * mm, Y(sy + dy), (sx + 185) * mm, Y(sy + dy))
stamp = [('Курсова робота з дисципліни «Проєктування торговельних об’єктів»', 'Serif'),
         ('Магазин взуття та аксесуарів ТОВ «Взуття». Тривимірна модель зали', 'SerifB'),
         ('Розробив(ла): ____________________   Перевірив(ла): ____________________', 'Serif'),
         ('ДТЕУ, кафедра торговельного підприємництва та логістики', 'Serif'),
         ('Аркуш А1 (841 × 594)      Масштаб плану 1:100      Київ 2026', 'Serif')]
for i, (t, f) in enumerate(stamp):
    text(t, sx + 3, sy + 3 + i * 11, 9.5, f)
c.showPage(); c.save()
print('ok', OUT)
