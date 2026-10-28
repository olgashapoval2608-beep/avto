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
LOW = 0.9                                    # занижені фасадна стіна і стіни нижньої правої ділянки
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
# ---------------------------------------------------------------- компоненти
# Кожен тип обладнання будується один раз (визначення компонента), а всі одиниці цього типу
# є його копіями — як описано в п. 2.3 курсової («зміна одного екземпляра змінює всі копії»).
DEF_TITLES = {
    'wall_hill': 'Пристінна гірка для взуття 1250×600×2200', 'island_hill': 'Острівна двостороння гірка 1500×1200×1400',
    'kids_table': 'Низький стіл-гірка для дитячого взуття 1200×600×700', 'podium': 'Подіум для промо-викладки 1600×800×400',
    'glass_vitrine': 'Скляна вітрина для аксесуарів 1000×500×1900', 'bag_counter': 'Острівна вітрина-прилавок для сумок 1200×1200×1100',
    'spinner': 'Обертова стійка для шкарпеток і панчіх 600×600×1600', 'care_stand': 'Стійка для засобів догляду 600×400×1400',
    'banquette': 'Банкетка для приміряння 1200×450×450', 'mirror': 'Підлогове дзеркало 600×300×1700',
    'cash_table': 'Касовий стіл 1600×700×1000', 'cash_rack': 'Стелаж касової зони 1200×400×2000',
}
DEFS = {}          # ключ -> (назва визначення, локальна геометрія)
INSTANCES = []     # (ключ, назва копії, тег, tx, ty, кут)


def place(name, tag, x0, y0, w, d, facing, builder, *args):
    rot = {'-y': 0, '+x': 90, '+y': 180, '-x': 270}[facing]
    key = (builder.__name__,) + args
    if key not in DEFS:
        title = DEF_TITLES[builder.__name__] + (f' — {DEPTS[args[0]][0]}' if args else '')
        local = bm.Group(title, tag)
        builder(local, *args)
        DEFS[key] = local
    r = bm.Xf(0, 0, 0, rot)
    cs = [r((0, 0, 0)), r((w, 0, 0)), r((0, d, 0)), r((w, d, 0))]
    tx, ty = x0 - min(c[0] for c in cs), y0 - min(c[1] for c in cs)
    xf = bm.Xf(0, 0, 0, rot).then(bm.Xf(tx, ty, 0))
    g = new_group(name, tag)                     # розгорнута копія — для DAE і рендерів
    for k, polys in DEFS[key].parts.items():
        g.parts[k] = [([xf(p) for p in pts], [r(n) for n in ns] if ns else None) for pts, ns in polys]
    g.instance = True
    INSTANCES.append((key, name, tag, tx, ty, rot))
    return g


def floor_tiles(g, x0, y0, x1, y1):
    import math
    for i in range(int(math.floor(x0)), int(math.ceil(x1))):
        for j in range(int(math.floor(y0)), int(math.ceil(y1))):
            a, b = max(x0, i), min(x1, i + 1)
            c, e = max(y0, j), min(y1, j + 1)
            if b - a > 1e-6 and e - c > 1e-6:
                g.poly(M_FLOOR_A if (i + j) % 2 == 0 else M_FLOOR_B, [(a, c, 0), (b, c, 0), (b, e, 0), (a, e, 0)])


def build_shell():
    g = new_group('Підлога торговельної зали', 'Підлога')
    floor_tiles(g, 0, 0, MAIN_W, MAIN_D)
    floor_tiles(g, PRJ_X0, PRJ_Y0, PRJ_X1, MAIN_D)
    box(g, mat('Плита перекриття', '#8C8478'), -WALL, -WALL, -0.25, MAIN_W + WALL, MAIN_D + WALL, -0.02)
    box(g, mat('Плита перекриття', '#8C8478'), MAIN_W, PRJ_Y0 - WALL, -0.25, PRJ_X1 + WALL, MAIN_D + WALL, -0.02)
    box(g, mat('Килимок', '#3D3D3D'), 8.0, 0.05, 0, 10.0, 1.6, 0.012, False)
    g = new_group('Стіни', 'Стіни')
    box(g, M_WALL, -WALL, 0, 0, 0, MAIN_D + WALL, H)                          # ліва
    box(g, M_WALL, 0, MAIN_D, 0, PRJ_X1 + WALL, MAIN_D + WALL, H)             # верхня (тильна)
    box(g, M_WALL, PRJ_X1, PRJ_Y0 - WALL, 0, PRJ_X1 + WALL, MAIN_D, H)        # права стіна виступу
    # для зручності огляду фасадну стіну і стіни нижньої правої ділянки знижено до 0,9 м (п. 2.3 курсової)
    box(g, M_WALL, MAIN_W, PRJ_Y0 - WALL, 0, PRJ_X1 + WALL, PRJ_Y0, LOW)      # нижня стіна виступу
    box(g, M_WALL, MAIN_W, -WALL, 0, MAIN_W + WALL, PRJ_Y0 - WALL, LOW)       # права стіна нижньої ділянки
    g = new_group('Фасадна стіна з вхідною групою 2,0 м', 'Стіни')
    for a, b in ((-WALL, 8.0), (10.0, MAIN_W + WALL)):
        box(g, M_WALL_OUT, a, -WALL, 0, b, 0, LOW)
    for xx in (8.0, 8.97, 9.94):                                              # стійки вхід / вихід
        box(g, M_FRAME, xx, -WALL, 0, xx + 0.06, 0, LOW + 0.05)
    box(g, M_GLASS, 8.06, -0.16, 0.02, 8.5, -0.14, LOW)                      # розсунуті стулки
    box(g, M_GLASS, 9.5, -0.16, 0.02, 9.94, -0.14, LOW)
    mat('Вивіска', '#FFFFFF')
    bm.TEXTS.append(('ВИХІД', 8.5, -WALL - 0.03, 0.5, 0, 0.12, 'Вивіска', 'facade'))
    bm.TEXTS.append(('ВХІД', 9.47, -WALL - 0.03, 0.5, 0, 0.12, 'Вивіска', 'facade'))
    g = new_group('Тротуар', 'Благоустрій')
    box(g, M_PAVE, -1.0, -5.0, -0.25, MAIN_W + 1.0, -WALL, -0.03)


def build_equipment():
    TAG = {'women': 'Жіночий відділ', 'men': 'Чоловічий відділ', 'kids': 'Дитячий відділ',
           'access': 'Аксесуари і супутні товари', 'cash': 'Розрахунковий вузол', 'fit': 'Зона приміряння'}
    n = [0]

    def wall(x0, y0, facing, dept, label=''):
        n[0] += 1
        place(f'1.{n[0]} Пристінна гірка — {DEPTS[dept][0]}{label}', TAG[dept], x0, y0, 1.25, 0.6, facing, wall_hill, dept)

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
            place(f'2.{k} Острівна гірка — Жіноче взуття', TAG['women'], x0, y0, 1.5, 1.2, '-y', island_hill, 'women')
    for y0 in (15.7, 13.3, 10.9):
        k += 1
        place(f'2.{k} Острівна гірка — Чоловіче взуття', TAG['men'], 17.3, y0, 1.5, 1.2, '-y', island_hill, 'men')
    for x0 in (6.6, 9.3):
        k += 1
        place(f'2.{k} Острівна гірка — Дитяче взуття', TAG['kids'], x0, 6.0, 1.5, 1.2, '-y', island_hill, 'kids')
    # 3. Столи-гірки для дитячого взуття
    for i, x0 in enumerate((3.0, 4.6)):
        place(f'3.{i + 1} Стіл-гірка — Дитяче взуття', TAG['kids'], x0, 6.0, 1.2, 0.6, '-y', kids_table)
    # 4. Подіуми для промо-викладки
    place('4.1 Подіум — Жіноче взуття (новинки)', TAG['women'], 5.0, 16.0, 1.6, 0.8, '-y', podium, 'women')
    place('4.2 Подіум — Чоловіче спортивне взуття', TAG['men'], 17.3, 9.2, 1.6, 0.8, '-y', podium, 'men')
    place('4.3 Подіум — Новинки сезону біля входу', TAG['women'], 10.6, 3.2, 1.6, 0.8, '-y', podium, 'women')
    # 5. Скляні вітрини для аксесуарів (фасадна стіна)
    for i in range(4):
        place(f'5.{i + 1} Скляна вітрина — Аксесуари', TAG['access'], 11.0 + i * 1.0, 0.0, 1.0, 0.5, '+y', glass_vitrine)
    # 6. Острівні вітрини-прилавки для сумок
    place('6.1 Вітрина-прилавок — Сумки', TAG['access'], 11.4, 5.2, 1.2, 1.2, '-y', bag_counter)
    place('6.2 Вітрина-прилавок — Сумки', TAG['access'], 13.2, 3.0, 1.2, 1.2, '-y', bag_counter)
    # 7. Обертові стійки і 8. стійка для засобів догляду
    for i, x0 in enumerate((3.6, 5.6, 7.6)):
        place(f'7.{i + 1} Обертова стійка — Шкарпетки, панчохи', TAG['cash'], x0, 4.3, 0.6, 0.6, '-y', spinner)
    place('8.1 Стійка — Засоби догляду за взуттям', TAG['cash'], 2.6, 2.9, 0.6, 0.4, '+y', care_stand)
    # 9. Банкетки і 10. дзеркала
    ban = [(3.0, 12.1, 1.2, 0.45, '-y'), (8.0, 12.1, 1.2, 0.45, '-y'), (12.4, 12.1, 1.2, 0.45, '-y'),
           (1.4, 7.8, 0.45, 1.2, '+x'), (1.5, 5.2, 1.2, 0.45, '+y'), (20.0, 14.2, 0.45, 1.2, '-x'),
           (20.0, 11.6, 0.45, 1.2, '-x')]
    for i, (x0, y0, a, b, f) in enumerate(ban):
        place(f'9.{i + 1} Банкетка для приміряння', TAG['fit'], x0, y0, 1.2, 0.45, f, banquette)
    mir = [(4.6, 12.2, '-y'), (9.6, 12.2, '-y'), (14.0, 12.2, '-y'), (1.4, 9.2, '+x'), (2.9, 5.2, '+y'),
           (20.0, 15.5, '-x'), (20.0, 12.9, '-x')]
    for i, (x0, y0, f) in enumerate(mir):
        place(f'10.{i + 1} Підлогове дзеркало', TAG['fit'], x0, y0, 0.6, 0.3, f, mirror)
    # 11. Касові столи (3) і 12. стелажі касової зони (2)
    for i, x0 in enumerate((3.4, 5.0, 6.6)):
        place(f'11.{i + 1} Касовий стіл (робоче місце касира {i + 1})', TAG['cash'], x0, 2.8, 1.6, 0.7, '+y', cash_table)
    for i, x0 in enumerate((4.0, 6.0)):
        place(f'12.{i + 1} Стелаж касової зони', TAG['cash'], x0, 0.0, 1.2, 0.4, '+y', cash_rack)


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
    scene(model, 'План зверху', [11.0, 9.25, 38.0], [11.0, 9.25, 0.0], false, 20.5)
    scene(model, 'Жіночий відділ', [12.5, 8.4, 1.8], [3.0, 16.0, 0.8])
    scene(model, 'Чоловічий відділ (виступ)', [16.5, 9.0, 1.9], [21.0, 17.5, 0.8])
    scene(model, 'Каси та дитячий відділ', [10.5, 6.5, 2.4], [3.5, 2.0, 0.6])
    scene(model, 'Аксесуари біля входу', [9.0, 6.5, 2.0], [14.5, 0.5, 0.8])
'''


RB_HELPERS = r"""
  def self.defn(model, name, parts)
    d = model.definitions.add(name)
    parts.each do |mname, smooth, polys|
      mesh = Geom::PolygonMesh.new
      polys.each do |flat|
        pts = []
        (0...flat.length).step(3) { |i| pts << Geom::Point3d.new(flat[i] * M, flat[i + 1] * M, flat[i + 2] * M) }
        mesh.add_polygon(pts) rescue nil
      end
      d.entities.fill_from_mesh(mesh, true, smooth ? 12 : 0, @m[mname], @m[mname])
    end
    d
  end

  def self.inst(model, d, name, tagname, tx, ty, rot)
    tr = Geom::Transformation.translation([tx * M, ty * M, 0]) * Geom::Transformation.rotation(ORIGIN, Z_AXIS, rot.degrees)
    i = model.active_entities.add_instance(d, tr)
    i.name = name
    i.layer = tag(model, tagname)
    i
  end

  # ---------------- аркуш А1 у LayOut (841 × 594 мм, альбомний)
  def self.mm(v)
    v / 25.4
  end

  def self.lo_style(e)
    st = e.style
    yield st
    e.style = st
  rescue StandardError
    nil
  end

  def self.lo_text(doc, layer, page, str, x, y, size = 12, bold = false)
    t = Layout::FormattedText.new(str, Geom::Point2d.new(mm(x), mm(y)), Layout::FormattedText::ANCHOR_TYPE_TOP_LEFT)
    doc.add_entity(t, layer, page)
    lo_style(t) { |st| st.text_size = size; st.text_bold = bold; st.font_family = 'Times New Roman' }
    t
  end

  def self.lo_rect(doc, layer, page, x, y, w, h, fill = nil, stroke = 0.5)
    r = Layout::Rectangle.new(Geom::Bounds2d.new(mm(x), mm(y), mm(w), mm(h)))
    doc.add_entity(r, layer, page)
    lo_style(r) do |st|
      st.stroke_width = stroke
      if fill
        st.solid_filled = true
        st.fill_color = Sketchup::Color.new(fill)
      else
        st.solid_filled = false
      end
    end
    r
  end

  def self.lo_view(doc, layer, page, skp, scene, x, y, w, h, caption, scale = nil)
    vp = Layout::SketchUpModel.new(skp, Geom::Bounds2d.new(mm(x), mm(y), mm(w), mm(h)))
    idx = vp.scenes.index(scene)
    vp.current_scene = idx if idx
    begin
      vp.render_mode = Layout::SketchUpModel::HYBRID_RENDER
    rescue StandardError
      nil
    end
    if scale
      begin
        vp.perspective = false
        vp.scale = scale
        vp.preserve_scale_on_resize = true
      rescue StandardError
        nil
      end
    end
    doc.add_entity(vp, layer, page)
    begin
      vp.render if vp.render_needed?
    rescue StandardError
      nil
    end
    lo_rect(doc, layer, page, x, y, w, h, nil, 0.35)
    lo_text(doc, layer, page, caption, x, y + h + 2, 11)
    vp
  end

  def self.make_layout(skp, layout_path, pdf_path)
    begin
      require 'layout'
    rescue LoadError
      nil
    end
    doc = Layout::Document.new
    doc.page_info.width = mm(841)
    doc.page_info.height = mm(594)
    page = doc.pages[0]
    layer = doc.layers[0]
    lo_rect(doc, layer, page, 20, 5, 816, 584, nil, 1.4)                       # рамка
    lo_text(doc, layer, page, SHEET_TITLE, 30, 10, 26, true)
    lo_text(doc, layer, page, SHEET_SUBTITLE, 30, 22, 15)
    SHEET_VIEWS.each { |sc, x, y, w, h, cap, sca| lo_view(doc, layer, page, skp, sc, x, y, w, h, cap, sca) }
    # експлікація обладнання
    tx, ty = 30, 462
    lo_text(doc, layer, page, 'Експлікація торговельно-технологічного обладнання', tx, ty - 8, 13, true)
    cols = [[10, '№'], [138, 'Найменування обладнання'], [52, 'Габарити, мм'], [22, 'К-сть']]
    rh = 7.4
    ([['№', 'Найменування обладнання', 'Габарити, мм', 'К-сть']] + SHEET_EQUIP).each_with_index do |row, ri|
      cx = tx
      cols.each_with_index do |(cw, _), ci|
        lo_rect(doc, layer, page, cx, ty + ri * rh, cw, rh, ri.zero? ? '#E6E6E6' : nil, 0.3)
        lo_text(doc, layer, page, row[ci].to_s, cx + 1.5, ty + ri * rh + 1.3, 9, ri.zero?)
        cx += cw
      end
    end
    # умовні позначення відділів
    lx, ly = 265, 462
    lo_text(doc, layer, page, 'Умовні позначення', lx, ly - 8, 13, true)
    SHEET_LEGEND.each_with_index do |(name, col), i|
      lo_rect(doc, layer, page, lx, ly + i * 9, 12, 6, col, 0.3)
      lo_text(doc, layer, page, name, lx + 15, ly + i * 9 + 0.6, 10)
    end
    # основний напис (штамп) 185 × 55 мм
    sx, sy = 651, 534
    lo_rect(doc, layer, page, sx, sy, 185, 55, nil, 1.0)
    [11, 22, 33, 44].each { |dy| lo_rect(doc, layer, page, sx, sy + dy, 185, 0.01, nil, 0.3) }
    SHEET_STAMP.each_with_index do |(txt, size, bold), i|
      lo_text(doc, layer, page, txt, sx + 3, sy + 2 + i * 11, size, bold)
    end
    doc.save(layout_path)
    puts "Збережено: #{layout_path}"
    begin
      doc.export(pdf_path)
      puts "Збережено: #{pdf_path}"
    rescue StandardError => e
      puts "PDF не експортовано (#{e.message}). Відкрийте .layout у LayOut: Файл → Експорт → PDF."
    end
  end
"""


def rb_parts(g):
    out = []
    for (m, smooth), polys in g.parts.items():
        out.append(f'      [{bm.rb_str(m)}, {"true" if smooth else "false"}, [\n')
        for pts, _n in polys:
            out.append('        [' + ','.join('%.4f,%.4f,%.4f' % p for p in pts) + '],\n')
        out.append('      ]],\n')
    return ''.join(out)


def rb_val(v):
    if isinstance(v, str):
        return bm.rb_str(v)
    if v is None:
        return 'nil'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (list, tuple)):
        return '[' + ', '.join(rb_val(x) for x in v) + ']'
    return repr(v)


SHEET = {
    'SHEET_TITLE': 'ПРОЄКТ ТОРГОВЕЛЬНОЇ ЗАЛИ МАГАЗИНУ ВЗУТТЯ ТА АКСЕСУАРІВ ТОВ «ВЗУТТЯ»',
    'SHEET_SUBTITLE': 'Тривимірна модель торговельної зали у SketchUp (п. 2.3, рис. 2.3–2.5). Г-подібна зала 360 м²: 16,0 × 18,5 м + виступ 6,0 × 10,7 м, висота 3,0 м',
    # сцена, x, y, w, h (мм), підпис, масштаб (лише для ортогонального плану)
    'SHEET_VIEWS': [
        ['План зверху', 30, 34, 245, 205, 'План торговельної зали з розміщенням обладнання, М 1:100', 0.01],
        ['Загальний вигляд', 290, 34, 300, 205, 'Загальний вигляд моделі (рис. 2.3)', None],
        ['Вигляд від входу', 605, 34, 221, 205, 'Вигляд торговельної зали від входу (рис. 2.5)', None],
        ['Жіночий відділ', 30, 255, 260, 180, 'Жіночий відділ і зона приміряння', None],
        ['Чоловічий відділ (виступ)', 300, 255, 260, 180, 'Чоловічий відділ у правому виступі (рис. Б.1)', None],
        ['Каси та дитячий відділ', 570, 255, 256, 180, 'Розрахунковий вузол і дитячий відділ', None],
    ],
    'SHEET_EQUIP': [
        [1, 'Пристінна гірка для взуття', '1250×600×2200', 45], [2, 'Острівна двостороння гірка', '1500×1200×1400', 15],
        [3, 'Низький стіл-гірка для дитячого взуття', '1200×600×700', 2], [4, 'Подіум для промо-викладки', '1600×800×400', 3],
        [5, 'Скляна вітрина для аксесуарів', '1000×500×1900', 4], [6, 'Острівна вітрина-прилавок для сумок', '1200×1200×1100', 2],
        [7, 'Обертова стійка для шкарпеток і панчіх', '600×600×1600', 3], [8, 'Стійка для засобів догляду за взуттям', '600×400×1400', 1],
        [9, 'Банкетка для приміряння', '1200×450×450', 7], [10, 'Підлогове дзеркало', '600×300×1700', 7],
        [11, 'Касовий стіл (робоче місце касира)', '1600×700×1000', 3], [12, 'Стелаж касової зони', '1200×400×2000', 2],
        ['', 'Разом', '', 94]],
    'SHEET_LEGEND': [['Жіноче взуття', '#E8A0B4'], ['Чоловіче взуття', '#8DB3E2'], ['Дитяче взуття', '#F4D06F'],
                     ['Аксесуари і сумки', '#B9A3D9'], ['Супутні товари', '#A8D5A2'], ['Розрахунковий вузол', '#9AA3AD'],
                     ['Зона приміряння (банкетки, дзеркала)', '#D9D9D9']],
    'SHEET_STAMP': [['Курсова робота з дисципліни «Проєктування торговельних об’єктів»', 9, False],
                    ['Магазин взуття та аксесуарів ТОВ «Взуття». Тривимірна модель торговельної зали', 9, True],
                    ['Розробив(ла): ______________________   Перевірив(ла): ______________________', 9, False],
                    ['ДТЕУ, кафедра торговельного підприємництва та логістики', 9, False],
                    ['Аркуш А1 (841 × 594)        Масштаб плану 1:100        Київ 2026', 9, False]],
}


def main():
    bm.GROUPS.clear()
    bm.TEXTS.clear()
    build_shell()
    build_equipment()
    build_navigation()
    eq = [g for g in bm.GROUPS if getattr(g, 'instance', False)]
    print(f'Груп: {len(bm.GROUPS)}, одиниць обладнання: {len(eq)}, визначень компонентів: {len(DEFS)}, '
          f'полігонів: {sum(g.nfaces() for g in bm.GROUPS)}')
    dae = os.path.join(HERE, 'vzuttia.dae')
    rb = os.path.join(HERE, 'vzuttia.rb')
    bm.export_dae(dae)
    s = open(dae, encoding='utf-8').read()
    s = s.replace('build_model.py — ТОВ «Дитячий світ»', 'build_model.py — ТОВ «Взуття»').replace('name="Дитячий світ"', 'name="Взуття"')
    open(dae, 'w', encoding='utf-8').write(s)
    # Ruby: будівля і навігація — групами, обладнання — компонентами
    all_groups = list(bm.GROUPS)
    bm.GROUPS[:] = [g for g in all_groups if not getattr(g, 'instance', False)]
    for g in DEFS.values():                         # матеріали визначень мають потрапити до списку
        bm.GROUPS.append(g)
    bm.export_rb(rb)
    bm.GROUPS[:] = all_groups
    s = open(rb, encoding='utf-8').read()
    # прибрати групи-визначення, додані лише заради матеріалів
    for g in DEFS.values():
        a = s.index(f"    grp(model, {bm.rb_str(g.name)}, ")
        b = s.index('    ])\n', a) + len('    ])\n')
        s = s[:a] + s[b:]
    comps = ['    # обладнання: визначення компонентів і їхні копії\n', '    defs = {}\n']
    for i, (key, g) in enumerate(DEFS.items()):
        comps.append(f'    defs[{i}] = defn(model, {bm.rb_str(g.name)}, [\n{rb_parts(g)}    ])\n')
    keys = list(DEFS)
    for key, name, tag, tx, ty, rot in INSTANCES:
        comps.append(f'    inst(model, defs[{keys.index(key)}], {bm.rb_str(name)}, {bm.rb_str(tag)}, {tx:.4f}, {ty:.4f}, {rot})\n')
    a = s.index("    scene(model, 'Загальний вигляд'")
    b = s.index('    model.pages.selected_page')
    s = s[:a] + ''.join(comps) + SCENES_RB + s[b:]
    consts = ''.join(f'  {k} = {rb_val(v)}.freeze\n' for k, v in SHEET.items())
    s = s.replace('  def self.build\n', consts + RB_HELPERS + '\n  def self.build\n', 1)
    s = s.replace("""  def self.scene(model, name, eye, target)
    cam = Sketchup::Camera.new(eye.map { |v| v * M }, target.map { |v| v * M }, Z_AXIS)
    cam.fov = 50
""", """  def self.scene(model, name, eye, target, persp = true, height = nil)
    up = persp ? Z_AXIS : Y_AXIS
    cam = Sketchup::Camera.new(eye.map { |v| v * M }, target.map { |v| v * M }, up)
    if persp
      cam.fov = 50
    else
      cam.perspective = false
      cam.height = height * M
    end
""")
    s = s.replace("""      model.options['UnitsOptions']['LengthUnit'] = 4  # метри""",
                  """      model.options['UnitsOptions']['LengthUnit'] = 2       # міліметри (п. 2.3)
      model.options['UnitsOptions']['LengthPrecision'] = 0""")
    s = s.replace("""    model.commit_operation
""", """    model.commit_operation
    dir = File.dirname(__FILE__)
    skp = File.join(dir, 'vzuttia.skp')
    model.save(skp)
    puts "Збережено: #{skp}"
    begin
      make_layout(skp, File.join(dir, 'vzuttia_A1.layout'), File.join(dir, 'vzuttia_A1.pdf'))
    rescue StandardError, LoadError => e
      puts "Аркуш LayOut не створено: #{e.message}"
    end
""", 1)
    s = (s.replace('DytiachyiSvit', 'Vzuttia').replace('магазину ТОВ «Дитячий світ» (курсова робота, розділ 4)',
                                                       'магазину взуття ТОВ «Взуття» (курсова робота, підрозділ 2.3)')
         .replace('dytiachyi_svit.rb', 'vzuttia.rb').replace('Дитячий світ', 'Взуття'))
    s = s.replace("# Згенеровано build_model.py; одиниці — метри.",
                  "# Згенеровано build_model.py. Після побудови скрипт зберігає поруч vzuttia.skp,\n"
                  "# створює аркуш А1 vzuttia_A1.layout у LayOut і експортує його у vzuttia_A1.pdf.")
    open(rb, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    main()
