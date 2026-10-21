#!/usr/bin/env python3
"""Генератор детальної 3D-моделі магазину взуття та аксесуарів ТОВ «Взуття» для SketchUp.

За курсовою роботою: Г-подібна торговельна зала 360 м² — основна частина 16,0 × 18,5 м і виступ
праворуч 6,0 × 10,7 м, висота 3,0 м; обладнання — табл. 2.1 (94 од.); розміщення — планограма рис. 2.2.

Координати: X — уздовж фасаду (0 — ліва стіна), Y — углиб (0 — фасадна стіна), Z — вгору, метри.
Примітиви геометрії й експорт беруться з ../toy-store-3d/build_model.py.
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'toy-store-3d'))
import build_model as bm                                      # noqa: E402
from build_model import box, cyl, sphere, prism_x, prism_y, mat, shade, place, new_group  # noqa: E402

random.seed(360)
H = 3.0
WALL = 0.2
bm.H = H
MAIN_W, MAIN_D = 16.0, 18.5                  # основна частина
PRJ_X0, PRJ_X1, PRJ_Y0 = 16.0, 22.0, 7.8     # виступ праворуч: X 16–22, Y 7,8–18,5

M_FLOOR_A = mat('Керамограніт світло-сірий', '#E4E3DF')
M_FLOOR_B = mat('Керамограніт сірий', '#D3D2CD')
M_WALL = mat('Стіни', '#EFEBE4')
M_WALL_OUT = mat('Фасад', '#B9AE9E')
M_GLASS = mat('Скло', '#A8D8EA', 0.3)
M_FRAME = mat('Алюмінієвий профіль', '#5F6A72')
M_SHELF = mat('Обладнання білий', '#F6F6F4')
M_METAL = mat('Метал хром', '#B9BEC4')
M_DARK = mat('Метал чорний', '#2E3134')
M_WOOD = mat('Дерево (дуб)', '#B8895A')
M_PODIUM = mat('Подіум', '#FAFAFA')
M_SEAT = mat('Оббивка банкеток', '#6D4C41')
M_MIRROR = mat('Дзеркало', '#D6E4EA')
M_SCREEN = mat('Екран', '#1C2833')
M_PAVE = mat('Тротуарна плитка', '#BDB8AE')
M_SOLE = mat('Підошва', '#3A3A3A')
M_SOLE_W = mat('Підошва біла', '#F2F2F2')
M_SHOEBOX = mat('Коробки взуття', '#C9A27A')

DEPTS = {
    'women': ('Жіноче взуття', '#E8A0B4'),
    'men': ('Чоловіче взуття', '#8DB3E2'),
    'kids': ('Дитяче взуття', '#F4D06F'),
    'access': ('Аксесуари і сумки', '#B9A3D9'),
    'socks': ('Супутні товари', '#A8D5A2'),
    'cash': ('Касовий вузол', '#9AA3AD'),
    'fit': ('Банкетки, дзеркала', '#D9D9D9'),
}
for k, (n, c) in DEPTS.items():
    mat('Відділ — ' + n, c)
    mat('Відділ — ' + n + ' (світлий)', shade(c, 1.45))


def dm(d, light=False):
    return 'Відділ — ' + DEPTS[d][0] + (' (світлий)' if light else '')


SHOE_COLS = {
    'women': ['#7B1E3A', '#D8B48A', '#222222', '#B03A2E', '#E6C3A5', '#F5F5F5', '#8E5A3C', '#5B2333'],
    'men': ['#1F3A5F', '#6B4226', '#222222', '#5D6D7E', '#F2F2F2', '#8B5A2B', '#2C3E50'],
    'kids': ['#E53935', '#1E88E5', '#FDD835', '#43A047', '#FB8C00', '#EC407A', '#00ACC1', '#8E24AA'],
}


def cm(c):
    return mat('Шкіра ' + c, c)


# ---------------------------------------------------------------- взуття
def shoe(g, x, y, z, style, col, ln=0.27, w=0.09):
    """Один черевик/туфля: носок до -y, ширина вдовж x від x до x+w."""
    up = cm(col)
    sole = M_SOLE_W if style in ('sneaker', 'kids') and random.random() < 0.6 else M_SOLE
    if style == 'pump':                                          # туфлі на підборах
        hh = 0.07
        prism_x(g, sole, x, x + w, [(y, z), (y + ln * 0.45, z), (y + ln, z + hh), (y + ln, z + hh + 0.012),
                                     (y + ln * 0.45, z + 0.012), (y, z + 0.012)])
        box(g, sole, x + w * 0.35, y + ln - 0.025, z, x + w * 0.65, y + ln, z + hh)       # підбор
        prism_x(g, up, x + 0.005, x + w - 0.005, [(y + 0.005, z + 0.012), (y + ln * 0.45, z + 0.012),
                                                   (y + ln * 0.45, z + 0.045), (y + 0.02, z + 0.03)])
        prism_x(g, up, x + 0.005, x + w - 0.005, [(y + ln * 0.75, z + hh * 0.75), (y + ln - 0.005, z + hh + 0.012),
                                                   (y + ln - 0.005, z + hh + 0.06), (y + ln * 0.8, z + hh * 0.75 + 0.04)])
        return
    if style == 'boot':                                          # чоботи
        box(g, sole, x, y, z, x + w, y + ln, z + 0.025)
        box(g, sole, x + 0.01, y + ln - 0.07, z, x + w - 0.01, y + ln, z + 0.05)
        prism_x(g, up, x + 0.004, x + w - 0.004, [(y + 0.005, z + 0.025), (y + ln - 0.005, z + 0.05),
                                                   (y + ln - 0.005, z + 0.38), (y + ln - 0.1, z + 0.38),
                                                   (y + ln * 0.45, z + 0.1), (y + 0.02, z + 0.07)])
        return
    # кросівки, черевики, туфлі чоловічі, дитячі
    hgt = {'sneaker': 0.1, 'oxford': 0.08, 'ankle': 0.16, 'kids': 0.09}[style]
    box(g, sole, x, y, z, x + w, y + ln, z + 0.025)
    prism_x(g, up, x + 0.004, x + w - 0.004, [(y + 0.006, z + 0.025), (y + ln - 0.004, z + 0.025),
                                               (y + ln - 0.004, z + hgt), (y + ln * 0.55, z + hgt * 0.95),
                                               (y + ln * 0.25, z + hgt * 0.6), (y + 0.02, z + hgt * 0.45)])
    if style == 'sneaker':
        box(g, M_SOLE_W, x + w * 0.2, y + ln * 0.3, z + hgt * 0.62, x + w * 0.8, y + ln * 0.55, z + hgt * 0.9, False)


STYLES = {'women': ['pump', 'pump', 'boot', 'ankle', 'sneaker'], 'men': ['oxford', 'sneaker', 'ankle', 'boot'],
          'kids': ['kids']}


def shoes_row(g, dept, x0, x1, y0, z, d=0.3, styles=None, pairs=True):
    """Ряд взуття на полиці: пари (або поодинці) носками до покупця."""
    styles = styles or STYLES[dept]
    ln = 0.2 if dept == 'kids' else (0.28 if dept == 'men' else 0.26)
    ln = min(ln, d - 0.02)
    w = 0.075 if dept == 'kids' else (0.1 if dept == 'men' else 0.085)
    x = x0 + 0.03
    while True:
        style = random.choice(styles)
        col = random.choice(SHOE_COLS[dept])
        span = (2 * w + 0.015) if pairs else w
        if x + span > x1:
            break
        shoe(g, x, y0, z, style, col, ln, w)
        if pairs:
            shoe(g, x + w + 0.015, y0, z, style, col, ln, w)
        x += span + random.uniform(0.04, 0.09)


def handbag(g, x, y, z, w, d, h, col):
    m = cm(col)
    prism_x(g, m, x, x + w, [(y, z), (y + d, z), (y + d - 0.02, z + h), (y + 0.02, z + h)])
    box(g, m, x + w * 0.25, y + d / 2 - 0.006, z + h, x + w * 0.3, y + d / 2 + 0.006, z + h + 0.08)
    box(g, m, x + w * 0.7, y + d / 2 - 0.006, z + h, x + w * 0.75, y + d / 2 + 0.006, z + h + 0.08)
    box(g, m, x + w * 0.25, y + d / 2 - 0.006, z + h + 0.08, x + w * 0.75, y + d / 2 + 0.006, z + h + 0.095)
    box(g, M_METAL, x + w * 0.45, y - 0.003, z + h * 0.7, x + w * 0.55, y, z + h * 0.8, False)


BAG_COLS = ['#7B1E3A', '#D8B48A', '#222222', '#8E5A3C', '#C0392B', '#E6C3A5', '#4A235A', '#1F3A5F']


def accessories(g, x0, x1, y0, z, d):
    x = x0 + 0.03
    while x + 0.12 < x1:
        r = random.random()
        col = random.choice(BAG_COLS)
        if r < 0.4:
            handbag(g, x, y0 + 0.03, z, 0.24, min(0.1, d - 0.05), 0.17, col)
            x += 0.29
        elif r < 0.7:                                            # гаманці
            box(g, cm(col), x, y0 + 0.04, z, x + 0.12, y0 + 0.12, z + 0.025)
            x += 0.16
        else:                                                    # ремені (згорнуті)
            cyl(g, cm(col), (x + 0.05, y0 + 0.08, z), 0.05, 0.035, 'z', 10)
            x += 0.13


# ---------------------------------------------------------------- обладнання
def wall_hill(g, dept):
    """Пристінна гірка для взуття 1,25 × 0,60 × 2,20 (фронт — y=0)."""
    w, d, h = 1.25, 0.6, 2.2
    box(g, M_SHELF, 0.02, 0.05, 0, w - 0.02, d, 0.3)                       # цоколь-шухляда
    box(g, dm(dept), 0.02, 0.045, 0.06, w - 0.02, 0.05, 0.24, False)
    box(g, dm(dept, True), 0.02, d - 0.03, 0.3, w - 0.02, d, h)            # задня панель
    for xx in (0, w - 0.02):
        box(g, M_SHELF, xx, 0.05, 0, xx + 0.02, d, h)
    levels = [0.3, 0.68, 1.06, 1.44, 1.82]
    for i, z0 in enumerate(levels):
        dep = 0.42 - 0.03 * i
        y0 = d - 0.03 - dep
        if i:
            box(g, M_SHELF, 0.02, y0, z0 - 0.02, w - 0.02, d - 0.03, z0)
            box(g, M_METAL, 0.02, y0 - 0.01, z0, w - 0.02, y0, z0 + 0.025, False)      # бортик
        if i == 4 and random.random() < 0.6:                    # верхня полиця — коробки
            xx = 0.05
            while xx < w - 0.36:
                box(g, M_SHOEBOX, xx, y0 + 0.03, z0, xx + 0.33, y0 + 0.23, z0 + 0.12)
                box(g, M_SHOEBOX, xx, y0 + 0.03, z0 + 0.12, xx + 0.33, y0 + 0.23, z0 + 0.24)
                xx += 0.37
        else:
            shoes_row(g, dept, 0.03, w - 0.03, y0 + 0.03, z0, dep - 0.05)
    box(g, M_SHELF, 0, 0.05, h - 0.02, w, d, h)
    box(g, dm(dept), 0, d - 0.12, h + 0.12, w, d - 0.02, h + 0.42)        # фриз відділу


def island_hill(g, dept):
    """Острівна двостороння гірка 1,50 × 1,20 × 1,40 (ступінчаста, з двох боків)."""
    w, d, h = 1.5, 1.2, 1.4
    box(g, M_SHELF, 0.05, 0.1, 0, w - 0.05, d - 0.1, 0.12)
    box(g, dm(dept, True), 0.02, d / 2 - 0.03, 0.12, w - 0.02, d / 2 + 0.03, h)
    for xx in (0, w - 0.02):
        prism_x(g, M_SHELF, xx, xx + 0.02, [(0.05, 0), (d - 0.05, 0), (d / 2 + 0.05, h), (d / 2 - 0.05, h)])
    box(g, M_SHELF, 0, d / 2 - 0.12, h - 0.02, w, d / 2 + 0.12, h)
    for side in (0, 1):
        old = g.xf
        g.xf = (bm.Xf(w, d, 0, 180) if side else bm.Xf()).then(old)
        for i, (y0, z0) in enumerate(((0.08, 0.12), (0.27, 0.52), (0.42, 0.92))):
            if i:
                box(g, M_SHELF, 0.02, y0, z0 - 0.02, w - 0.02, d / 2 - 0.03, z0)
            box(g, dm(dept), 0.02, y0 - 0.005, z0 - 0.04, w - 0.02, y0, z0 + 0.0, False)
            shoes_row(g, dept, 0.02, w - 0.02, y0 + 0.02, z0 + (0.0 if i == 0 else 0.0), d / 2 - y0 - 0.06)
        g.xf = old
    shoes_row(g, dept, 0.05, w - 0.05, d / 2 - 0.13, h, 0.27, pairs=False)


def kids_table(g):
    """Низький стіл-гірка для дитячого взуття 1,20 × 0,60 × 0,70."""
    w, d = 1.2, 0.6
    box(g, M_WOOD, 0, 0, 0.4, w, d, 0.44)
    box(g, M_WOOD, 0, d / 2 - 0.1, 0.44, w, d / 2 + 0.1, 0.7)
    for xx in (0.03, w - 0.08):
        for yy in (0.03, d - 0.08):
            box(g, dm('kids'), xx, yy, 0, xx + 0.05, yy + 0.05, 0.4)
    shoes_row(g, 'kids', 0.0, w, 0.02, 0.44, 0.2)
    old = g.xf
    g.xf = bm.Xf(w, d, 0, 180).then(old)
    shoes_row(g, 'kids', 0.0, w, 0.02, 0.44, 0.2)
    g.xf = old
    shoes_row(g, 'kids', 0.05, w - 0.05, d / 2 - 0.1, 0.7, 0.2, pairs=False)


def podium(g, dept):
    """Подіум для промо-викладки 1,60 × 0,80 × 0,40."""
    w, d, h = 1.6, 0.8, 0.4
    box(g, M_PODIUM, 0, 0, 0, w, d, h)
    box(g, dm(dept), -0.004, -0.004, 0.03, w + 0.004, d + 0.004, 0.09, False)
    box(g, M_PODIUM, 0.9, 0.2, h, 1.5, 0.6, h + 0.25)                       # ступінь
    shoes_row(g, dept if dept != 'access' else 'women', 0.05, 0.85, 0.25, h, 0.3)
    shoes_row(g, dept if dept != 'access' else 'women', 0.9, 1.5, 0.27, h + 0.25, 0.3, pairs=False)
    cyl(g, M_METAL, (0.3, 0.65, h), 0.01, 0.6, 'z', 6, False)               # табличка «Новинки»
    box(g, dm(dept), 0.1, 0.64, h + 0.6, 0.5, 0.66, h + 0.85)


def glass_vitrine(g):
    """Скляна вітрина для аксесуарів 1,00 × 0,50 × 1,90."""
    w, d, h = 1.0, 0.5, 1.9
    box(g, M_SHELF, 0, 0, 0, w, d, 0.15)
    box(g, M_SHELF, 0, d - 0.02, 0.15, w, d, h)
    for xx in (0, w - 0.03):
        box(g, M_FRAME, xx, 0, 0.15, xx + 0.03, d, h)
    box(g, M_SHELF, 0, 0, h - 0.08, w, d, h)
    box(g, M_GLASS, 0.03, 0, 0.15, w - 0.03, 0.01, h - 0.08)
    box(g, M_GLASS, 0, 0.01, 0.15, 0.005, d - 0.02, h - 0.08, False)
    for z0 in (0.15, 0.6, 1.05, 1.45):
        box(g, M_GLASS, 0.03, 0.02, z0, w - 0.03, d - 0.03, z0 + 0.01)
        accessories(g, 0.03, w - 0.03, 0.04, z0 + 0.01, d - 0.08)
    box(g, dm('access'), 0, -0.003, h - 0.07, w, 0, h - 0.01, False)


def bag_counter(g):
    """Острівна вітрина-прилавок для сумок 1,20 × 1,20 × 1,10."""
    w, d = 1.2, 1.2
    box(g, M_WOOD, 0.03, 0.03, 0, w - 0.03, d - 0.03, 0.75)
    box(g, dm('access'), 0.03, 0.025, 0.5, w - 0.03, 0.03, 0.6, False)
    box(g, M_SHELF, 0, 0, 0.75, w, d, 0.78)
    for (a, b, c, e) in ((0, 0, w, 0.02), (0, d - 0.02, w, d), (0, 0, 0.02, d), (w - 0.02, 0, w, d)):
        box(g, M_GLASS, a, b, 0.78, c, e, 1.08)
    box(g, M_GLASS, 0, 0, 1.08, w, d, 1.1)
    for i in range(2):
        for j in range(2):
            handbag(g, 0.12 + i * 0.52, 0.12 + j * 0.52, 0.78, 0.4, 0.14, 0.17, random.choice(BAG_COLS))
    handbag(g, 0.35, 0.5, 1.1, 0.5, 0.18, 0.25, random.choice(BAG_COLS))   # сумка на склі


def spinner(g):
    """Обертова стійка для шкарпеток і панчіх 0,60 × 0,60 × 1,60."""
    c = (0.3, 0.3)
    cyl(g, M_METAL, (c[0], c[1], 0), 0.28, 0.04, 'z', 14)
    cyl(g, M_METAL, (c[0], c[1], 0.04), 0.02, 1.5, 'z', 8)
    box(g, dm('socks'), c[0] - 0.15, c[1] - 0.01, 1.5, c[0] + 0.15, c[1] + 0.01, 1.62)
    for z in (0.35, 0.65, 0.95, 1.25):
        for k in range(8):
            import math
            a = k * math.pi / 4
            px, py = c[0] + 0.2 * math.cos(a), c[1] + 0.2 * math.sin(a)
            col = mat('Упаковка ' + (cc := random.choice(['#FFFFFF', '#222222', '#E6C3A5', '#7B1E3A', '#1F3A5F', '#A8D5A2'])), cc)
            box(g, col, px - 0.04, py - 0.04, z - 0.2, px + 0.04, py + 0.04, z)


def care_stand(g):
    """Стійка для засобів догляду за взуттям 0,60 × 0,40 × 1,40."""
    w, d, h = 0.6, 0.4, 1.4
    box(g, M_SHELF, 0, d - 0.02, 0, w, d, h)
    for xx in (0, w - 0.02):
        box(g, M_SHELF, xx, 0, 0, xx + 0.02, d, h)
    for z0 in (0.1, 0.42, 0.74, 1.06):
        box(g, M_SHELF, 0.02, 0, z0 - 0.015, w - 0.02, d - 0.02, z0)
        x = 0.05
        while x < w - 0.08:
            col = mat('Упаковка ' + (cc := random.choice(['#222222', '#6B4226', '#B03A2E', '#1F3A5F', '#F5F5F5'])), cc)
            if random.random() < 0.6:
                cyl(g, col, (x + 0.03, 0.12, z0), 0.03, 0.17, 'z', 8)
            else:
                box(g, col, x, 0.06, z0, x + 0.07, 0.16, z0 + 0.1)
            x += 0.08
    box(g, dm('socks'), 0, d - 0.06, h, w, d - 0.02, h + 0.18)


def banquette(g):
    """Банкетка для приміряння 1,20 × 0,45 × 0,45."""
    w, d = 1.2, 0.45
    for xx in (0.04, w - 0.08):
        for yy in (0.04, d - 0.08):
            box(g, M_DARK, xx, yy, 0, xx + 0.04, yy + 0.04, 0.3)
    box(g, M_WOOD, 0, 0, 0.3, w, d, 0.34)
    box(g, M_SEAT, 0.01, 0.01, 0.34, w - 0.01, d - 0.01, 0.45)
    box(g, mat('Ріжок для взуття', '#B03A2E'), 0.05, 0.15, 0.45, 0.08, 0.35, 0.46)


def mirror(g):
    """Підлогове дзеркало 0,60 × 0,30 × 1,70 (дзеркальна площина — до y=0)."""
    w, d = 0.6, 0.3
    box(g, M_DARK, 0, 0.05, 0, w, d, 0.05)
    prism_x(g, M_WOOD, 0.03, w - 0.03, [(0.12, 0.05), (0.17, 0.05), (0.27, 1.7), (0.22, 1.7)])
    prism_x(g, M_MIRROR, 0.06, w - 0.06, [(0.115, 0.12), (0.125, 0.12), (0.22, 1.62), (0.21, 1.62)])
    box(g, M_DARK, 0.25, 0.2, 0.0, 0.35, 0.3, 0.9)


def cash_table(g):
    """Касовий стіл 1,60 × 0,70 × 1,00 (покупець — y=0, касир — y=d)."""
    w, d, h = 1.6, 0.7, 1.0
    box(g, M_WOOD, 0, 0, 0, w, 0.08, h)                                    # фронтальна панель
    box(g, dm('cash'), 0, -0.003, 0.65, w, 0, 0.8, False)
    box(g, M_SHELF, 0, 0, 0.75, w, d, 0.79)                                # стільниця касира
    box(g, M_SHELF, 0, 0, h - 0.03, w, 0.3, h)                             # прилавок для покупця
    for xx in (0, w - 0.04):
        box(g, M_WOOD, xx, 0.08, 0, xx + 0.04, d, 0.75)
    box(g, M_DARK, 0.5, 0.45, 0.79, 0.6, 0.55, 0.95)                       # монітор
    box(g, M_DARK, 0.3, 0.32, 0.95, 0.8, 0.35, 1.28)
    box(g, M_SCREEN, 0.32, 0.355, 0.97, 0.78, 0.36, 1.26, False)
    box(g, M_DARK, 0.95, 0.12, h, 1.05, 0.22, h + 0.05)                    # термінал
    box(g, M_DARK, 0.3, 0.45, 0.6, 0.75, 0.68, 0.72)                       # грошова скринька
    box(g, M_SHOEBOX, 1.15, 0.35, 0.79, 1.5, 0.6, 0.91)                    # коробка на пакування
    box(g, mat('Пакети', '#F5F5F5'), 1.2, 0.08, 0.79, 1.5, 0.25, 0.95)
    cyl(g, M_DARK, (0.55, d + 0.4, 0), 0.24, 0.04, 'z', 10)                # стілець касира
    cyl(g, M_METAL, (0.55, d + 0.4, 0.04), 0.03, 0.55, 'z', 6)
    cyl(g, mat('Сидіння', '#37474F'), (0.55, d + 0.4, 0.59), 0.2, 0.07, 'z', 12)


def cash_rack(g):
    """Стелаж касової зони 1,20 × 0,40 × 2,00 (запас коробок, пакети)."""
    w, d, h = 1.2, 0.4, 2.0
    for xx in (0, w - 0.03):
        box(g, M_DARK, xx, 0, 0, xx + 0.03, d, h)
    for z0 in (0.05, 0.45, 0.85, 1.25, 1.65):
        box(g, M_SHELF, 0.03, 0, z0, w - 0.03, d, z0 + 0.02)
        xx = 0.05
        while xx < w - 0.36:
            box(g, M_SHOEBOX if random.random() < 0.7 else mat('Пакети', '#F5F5F5'), xx, 0.04, z0 + 0.02,
                xx + 0.33, 0.36, z0 + 0.02 + random.uniform(0.12, 0.3))
            xx += 0.36


# ---------------------------------------------------------------- будівля
def floor_tiles(g, x0, y0, x1, y1):
    import math
    for i in range(int(math.floor(x0)), int(math.ceil(x1))):
        for j in range(int(math.floor(y0)), int(math.ceil(y1))):
            a, b = max(x0, i), min(x1, i + 1)
            c, e = max(y0, j), min(y1, j + 1)
            if b - a > 1e-6 and e - c > 1e-6:
                g.poly(M_FLOOR_A if (i + j) % 2 == 0 else M_FLOOR_B, [(a, c, 0), (b, c, 0), (b, e, 0), (a, e, 0)])


def build_shell():
    g = new_group('Підлога торговельної зали', 'Будівля')
    floor_tiles(g, 0, 0, MAIN_W, MAIN_D)
    floor_tiles(g, PRJ_X0, PRJ_Y0, PRJ_X1, MAIN_D)
    box(g, mat('Плита перекриття', '#8C8478'), -WALL, -WALL, -0.25, MAIN_W + WALL, MAIN_D + WALL, -0.02)
    box(g, mat('Плита перекриття', '#8C8478'), MAIN_W, PRJ_Y0 - WALL, -0.25, PRJ_X1 + WALL, MAIN_D + WALL, -0.02)
    box(g, mat('Килимок', '#3D3D3D'), 7.95, 0.05, 0, 10.05, 1.6, 0.012, False)
    g = new_group('Стіни', 'Будівля')
    box(g, M_WALL, -WALL, 0, 0, 0, MAIN_D + WALL, H)                          # ліва
    box(g, M_WALL, 0, MAIN_D, 0, PRJ_X1 + WALL, MAIN_D + WALL, H)             # верхня (тильна)
    box(g, M_WALL, PRJ_X1, PRJ_Y0 - WALL, 0, PRJ_X1 + WALL, MAIN_D, H)        # права стіна виступу
    box(g, M_WALL, MAIN_W, PRJ_Y0 - WALL, 0, PRJ_X1, PRJ_Y0, H)               # нижня стіна виступу
    box(g, M_WALL, MAIN_W, -WALL, 0, MAIN_W + WALL, PRJ_Y0 - WALL, H)         # права стіна нижньої ділянки
    g = new_group('Фасад із вітринами і вхідною групою', 'Будівля')
    for a, b in ((-WALL, 0.3), (7.6, 7.9), (10.1, 10.4), (15.7, MAIN_W + WALL)):
        box(g, M_WALL_OUT, a, -WALL, 0, b, 0, H)
    for a, b in ((0.3, 7.6), (10.4, 15.7)):
        box(g, M_WALL_OUT, a, -WALL, 0, b, 0, 0.5)
        box(g, M_WALL_OUT, a, -WALL, 2.6, b, 0, H)
        n = max(1, round((b - a) / 1.8))
        for i in range(n + 1):
            xx = a + (b - a) * i / n
            box(g, M_FRAME, xx - 0.04, -WALL, 0.5, xx + 0.04, -0.05, 2.6)
        for i in range(n):
            box(g, M_GLASS, a + (b - a) * i / n + 0.04, -0.13, 0.5, a + (b - a) * (i + 1) / n - 0.04, -0.11, 2.6)
    box(g, M_WALL_OUT, 7.9, -WALL, 2.4, 10.1, 0, H)
    box(g, M_FRAME, 7.9, -WALL, 2.32, 10.1, 0, 2.4)
    box(g, M_FRAME, 8.97, -WALL, 0, 9.03, 0, 2.32)                            # розділення вхід/вихід
    box(g, M_GLASS, 7.95, -0.16, 0.02, 8.4, -0.14, 2.32)
    box(g, M_GLASS, 9.6, -0.16, 0.02, 10.05, -0.14, 2.32)
    g = new_group('Вивіска «Взуття»', 'Навігація')
    box(g, mat('Вивіска фон', '#7B1E3A'), 3.0, -WALL - 0.12, 2.65, 13.0, -WALL, 2.97)
    bm.TEXTS.append(('ВЗУТТЯ ТА АКСЕСУАРИ', 8.0, -WALL - 0.125, 2.72, 0, 0.2, 'Вивіска', 'facade'))
    bm.TEXTS.append(('ВХІД', 9.55, -WALL - 0.03, 2.43, 0, 0.12, 'Вивіска', 'facade'))
    bm.TEXTS.append(('ВИХІД', 8.45, -WALL - 0.03, 2.43, 0, 0.12, 'Вивіска', 'facade'))
    mat('Вивіска', '#FFFFFF')
    g = new_group('Тротуар', 'Благоустрій')
    box(g, M_PAVE, -1.0, -5.0, -0.25, MAIN_W + 1.0, -WALL, -0.03)


def build_equipment():
    T = 'Обладнання'
    n = [0]

    def wall(x0, y0, facing, dept, label=''):
        n[0] += 1
        place(f'1.{n[0]} Пристінна гірка — {DEPTS[dept][0]}{label}', T, x0, y0, 1.25, 0.6, facing, wall_hill, dept)

    for i in range(8):                                         # верхня стіна, ліва частина — жіноче
        wall(0.6 + i * 1.25, MAIN_D - 0.6, '-y', 'women', ' (зимові чоботи)')
    for i in range(8):                                         # верхня стіна, права частина — чоловіче
        wall(11.0 + i * 1.25, MAIN_D - 0.6, '-y', 'men')
    for j in range(10):                                        # ліва стіна — жіноче
        wall(0, MAIN_D - 1.01 - (j + 1) * 1.25, '+x', 'women')
    for j in range(3):                                         # ліва стіна, низ — дитяче
        wall(0, 4.33 - (j + 1) * 1.25, '+x', 'kids')
    for j in range(7):                                         # права стіна виступу — чоловіче
        wall(PRJ_X1 - 0.6, 17.14 - (j + 1) * 1.25, '-x', 'men')
    for i in range(4):                                         # нижня стіна виступу — чоловіче
        wall(16.3 + i * 1.25, PRJ_Y0, '+y', 'men', ' (сланці, сандалети)')
    for j in range(5):                                         # стіна нижньої правої ділянки — жіноче літнє
        wall(MAIN_W - 0.6, 6.84 - (j + 1) * 1.25, '-x', 'women', ' (літнє)')
    # 2. Острівні гірки
    k = 0
    for y0 in (13.8, 9.8):
        for x0 in (2.8, 5.5, 8.2, 10.9, 13.6):
            k += 1
            place(f'2.{k} Острівна гірка — Жіноче взуття', T, x0, y0, 1.5, 1.2, '-y', island_hill, 'women')
    for y0 in (15.7, 13.3, 10.9):
        k += 1
        place(f'2.{k} Острівна гірка — Чоловіче взуття', T, 17.3, y0, 1.5, 1.2, '-y', island_hill, 'men')
    for x0 in (6.6, 9.3):
        k += 1
        place(f'2.{k} Острівна гірка — Дитяче взуття', T, x0, 6.0, 1.5, 1.2, '-y', island_hill, 'kids')
    # 3. Столи-гірки для дитячого взуття
    for i, x0 in enumerate((3.0, 4.6)):
        place(f'3.{i + 1} Стіл-гірка — Дитяче взуття', T, x0, 6.0, 1.2, 0.6, '-y', kids_table)
    # 4. Подіуми для промо-викладки
    place('4.1 Подіум — Жіноче взуття (новинки)', T, 5.0, 16.0, 1.6, 0.8, '-y', podium, 'women')
    place('4.2 Подіум — Чоловіче спортивне взуття', T, 17.3, 9.2, 1.6, 0.8, '-y', podium, 'men')
    place('4.3 Подіум — Новинки сезону біля входу', T, 10.6, 3.2, 1.6, 0.8, '-y', podium, 'women')
    # 5. Скляні вітрини для аксесуарів (фасадна стіна)
    for i in range(4):
        place(f'5.{i + 1} Скляна вітрина — Аксесуари', T, 11.0 + i * 1.0, 0.0, 1.0, 0.5, '+y', glass_vitrine)
    # 6. Острівні вітрини-прилавки для сумок
    place('6.1 Вітрина-прилавок — Сумки', T, 11.4, 5.2, 1.2, 1.2, '-y', bag_counter)
    place('6.2 Вітрина-прилавок — Сумки', T, 13.2, 3.0, 1.2, 1.2, '-y', bag_counter)
    # 7. Обертові стійки і 8. стійка для засобів догляду
    for i, x0 in enumerate((3.6, 5.6, 7.6)):
        place(f'7.{i + 1} Обертова стійка — Шкарпетки, панчохи', T, x0, 4.3, 0.6, 0.6, '-y', spinner)
    place('8.1 Стійка — Засоби догляду за взуттям', T, 2.6, 2.9, 0.6, 0.4, '+y', care_stand)
    # 9. Банкетки і 10. дзеркала
    ban = [(3.0, 12.1, 1.2, 0.45, '-y'), (8.0, 12.1, 1.2, 0.45, '-y'), (12.4, 12.1, 1.2, 0.45, '-y'),
           (1.4, 7.8, 0.45, 1.2, '+x'), (1.5, 5.2, 1.2, 0.45, '+y'), (20.0, 14.2, 0.45, 1.2, '-x'),
           (20.0, 11.6, 0.45, 1.2, '-x')]
    for i, (x0, y0, a, b, f) in enumerate(ban):
        place(f'9.{i + 1} Банкетка для приміряння', T, x0, y0, 1.2, 0.45, f, banquette)
    mir = [(4.6, 12.2, '-y'), (9.6, 12.2, '-y'), (14.0, 12.2, '-y'), (1.4, 9.2, '+x'), (2.9, 5.2, '+y'),
           (20.0, 15.5, '-x'), (20.0, 12.9, '-x')]
    for i, (x0, y0, f) in enumerate(mir):
        place(f'10.{i + 1} Підлогове дзеркало', T, x0, y0, 0.6, 0.3, f, mirror)
    # 11. Касові столи (3) і 12. стелажі касової зони (2)
    for i, x0 in enumerate((3.4, 5.0, 6.6)):
        place(f'11.{i + 1} Касовий стіл (робоче місце касира {i + 1})', T, x0, 2.8, 1.6, 0.7, '+y', cash_table)
    for i, x0 in enumerate((4.0, 6.0)):
        place(f'12.{i + 1} Стелаж касової зони', T, x0, 0.0, 1.2, 0.4, '+y', cash_rack)


def sign(g, dept, cx, cy, width, along, z=2.4):
    t = 0.03
    if along == 'x':
        box(g, dm(dept), cx - width / 2, cy - t, z, cx + width / 2, cy + t, z + 0.35)
        for xx in (cx - width / 2 + 0.1, cx + width / 2 - 0.1):
            cyl(g, M_METAL, (xx, cy, z + 0.35), 0.004, H - z - 0.35, 'z', 4, False)
    else:
        box(g, dm(dept), cx - t, cy - width / 2, z, cx + t, cy + width / 2, z + 0.35)
        for yy in (cy - width / 2 + 0.1, cy + width / 2 - 0.1):
            cyl(g, M_METAL, (cx, yy, z + 0.35), 0.004, H - z - 0.35, 'z', 4, False)


def build_navigation():
    g = new_group('Підвісні покажчики відділів', 'Навігація')
    signs = [('women', 8.0, 12.7, 2.6, 'x', 'ЖІНОЧЕ ВЗУТТЯ'), ('men', 19.0, 12.7, 2.6, 'x', 'ЧОЛОВІЧЕ ВЗУТТЯ'),
             ('kids', 5.5, 7.6, 2.4, 'x', 'ДИТЯЧЕ ВЗУТТЯ'), ('access', 13.0, 1.6, 2.2, 'x', 'АКСЕСУАРИ І СУМКИ'),
             ('cash', 5.0, 3.9, 1.6, 'x', 'КАСИ'), ('women', 14.2, 6.0, 2.4, 'y', 'ЛІТНЄ ВЗУТТЯ')]
    for dept, cx, cy, wd, along, txt in signs:
        sign(g, dept, cx, cy, wd, along)
        if along == 'x':
            bm.TEXTS.append((txt, cx, cy - 0.035, 2.47, 0, 0.13, 'Вивіска', 'y-'))
        else:
            bm.TEXTS.append((txt, cx - 0.035, cy, 2.47, 0, 0.13, 'Вивіска', 'x-'))
    # написи на фризах пристінних гірок (2,32–2,62 м)
    W_ = 'Вивіска'
    bm.TEXTS += [('ЖІНОЧІ ЗИМОВІ ЧОБОТИ', 5.6, MAIN_D - 0.125, 2.39, 0, 0.15, W_, 'y-'),
                 ('ЧОЛОВІЧІ ЧЕРЕВИКИ, ТУФЛІ, ЧОБОТИ', 16.0, MAIN_D - 0.125, 2.39, 0, 0.15, W_, 'y-'),
                 ('ЖІНОЧІ ЧЕРЕВИКИ ТА ТУФЛІ', 0.125, 11.2, 2.39, 0, 0.15, W_, 'x+'),
                 ('ДИТЯЧЕ ВЗУТТЯ', 0.125, 2.45, 2.39, 0, 0.15, W_, 'x+'),
                 ('СПОРТИВНЕ ВЗУТТЯ', PRJ_X1 - 0.125, 12.8, 2.39, 0, 0.15, W_, 'x-'),
                 ('ЖІНОЧЕ ЛІТНЄ ВЗУТТЯ', MAIN_W - 0.125, 3.7, 2.39, 0, 0.15, W_, 'x-')]


SCENES_RB = '''    scene(model, 'Загальний вигляд', [-7.0, -12.0, 17.0], [10.0, 9.5, 0.0])
    scene(model, 'Вигляд від входу', [9.0, 0.6, 1.65], [9.0, 14.0, 0.8])
    scene(model, 'План зверху', [11.0, 9.25, 38.0], [11.0, 9.26, 0.0])
    scene(model, 'Жіночий відділ', [12.5, 8.4, 1.8], [3.0, 16.0, 0.8])
    scene(model, 'Чоловічий відділ (виступ)', [16.5, 9.0, 1.9], [21.0, 17.5, 0.8])
    scene(model, 'Каси та дитячий відділ', [10.5, 6.5, 2.4], [3.5, 2.0, 0.6])
    scene(model, 'Аксесуари біля входу', [9.0, 6.5, 2.0], [14.5, 0.5, 0.8])
'''


def main():
    bm.GROUPS.clear()
    bm.TEXTS.clear()
    build_shell()
    build_equipment()
    build_navigation()
    eq = [g for g in bm.GROUPS if g.tag == 'Обладнання']
    print(f'Груп: {len(bm.GROUPS)}, одиниць обладнання: {len(eq)}, полігонів: {sum(g.nfaces() for g in bm.GROUPS)}')
    dae = os.path.join(HERE, 'vzuttia.dae')
    rb = os.path.join(HERE, 'vzuttia.rb')
    bm.export_dae(dae)
    s = open(dae, encoding='utf-8').read()
    s = s.replace('build_model.py — ТОВ «Дитячий світ»', 'build_model.py — ТОВ «Взуття»').replace('name="Дитячий світ"', 'name="Взуття"')
    open(dae, 'w', encoding='utf-8').write(s)
    bm.export_rb(rb)
    s = open(rb, encoding='utf-8').read()
    a = s.index("    scene(model, 'Загальний вигляд'")
    b = s.index('    model.pages.selected_page')
    s = s[:a] + SCENES_RB + s[b:]
    s = (s.replace('DytiachyiSvit', 'Vzuttia').replace('магазину ТОВ «Дитячий світ» (курсова робота, розділ 4)',
                                                         'магазину взуття ТОВ «Взуття» (курсова робота, підрозділ 2.3)')
         .replace('dytiachyi_svit.rb', 'vzuttia.rb').replace('Дитячий світ', 'Взуття'))
    open(rb, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    main()
