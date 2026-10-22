#!/usr/bin/env python3
"""Генератор детальної 3D-моделі продовольчого магазину ТОВ «Аеро-Експрес» для SketchUp.

За курсовою роботою: будівля 25,0 × 25,0 м, торговельна зала 25,0 × 16,0 м (висота 3,6 м),
тильний блок підсобних приміщень глибиною 9,0 м (рис. 3.1, табл. 3.1),
обладнання — табл. 3.4 (49 од.), розміщення — планограма рис. 3.2.

Координати: X — уздовж фасаду (0 — ліва стіна, 25 — права), Y — углиб (0 — фасад,
16 — перегородка між залою і підсобним блоком, 25 — тильна стіна), Z — вгору, метри.

Примітиви геометрії й експорт беруться з ../toy-store-3d/build_model.py.
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'toy-store-3d'))
import build_model as bm                                      # noqa: E402
from build_model import box, cyl, sphere, prism_x, prism_y, mat, shade, place, new_group  # noqa: E402

random.seed(637)
L, D_HALL, D_ALL, H = 25.0, 16.0, 25.0, 3.6
WALL = 0.2
LOW = 1.0                                                     # занижені стіни
bm.H = H                                                      # для підвісних табличок

# ---------------------------------------------------------------- матеріали
M_FLOOR_A = mat('Керамограніт світлий', '#E9E9E6')
M_FLOOR_B = mat('Керамограніт сірий', '#D5D6D3')
M_FLOOR_S = mat('Підлога підсобних приміщень', '#C9CCCF')
M_PANEL = mat('Сендвіч-панель', '#E4E6E8')
M_PANEL_OUT = mat('Сендвіч-панель фасад', '#B7BEC5')
M_PART = mat('Перегородки', '#F2F1EC')
M_GLASS = mat('Скло', '#A8D8EA', 0.3)
M_FRAME = mat('Алюмінієвий профіль', '#5F6A72')
M_METAL = mat('Метал оцинкований', '#B9BEC4')
M_RACK = mat('Стелаж Колумб (RAL 7035)', '#D7DADC')
M_DARK = mat('Метал чорний', '#2E3134')
M_WHITE = mat('Білий пластик', '#F7F7F5')
M_WOOD = mat('Дерево', '#B88A5A')
M_CRATE = mat('Ящики для фруктів', '#C69C6D')
M_ASPH = mat('Асфальт', '#8E9093')
M_PAVE = mat('Тротуарна плитка', '#BDB8AE')
M_GRASS = mat('Газон', '#8DB86B')
M_MARK = mat('Розмітка', '#F4F4F0')
M_SCREEN = mat('Екран', '#1C2833')
M_BELT = mat('Стрічка транспортера', '#222426')
M_CASH = mat('Касовий бокс Magellan', '#C8372D')
M_LIGHT = mat('Світильник', '#FFFBE6')
M_DOOR = mat('Двері', '#9AA4AD')
M_COLD_DOOR = mat('Двері холодильних камер', '#DDE3E8')

DEPTS = {
    'gastro':  ('Гастрономія та сири', 'A', '#E8A87C'),
    'meat':    ('М’ясо-ковбасні вироби', 'A', '#D9534F'),
    'dairy':   ('Молочні вироби та яйця', 'A/C', '#7FB3D5'),
    'confect': ('Кондитерські вироби', 'A', '#C39BD3'),
    'alco':    ('Алкогольні напої', 'A/B/C', '#8B5A3C'),
    'drinks':  ('Пиво, соки та безалкогольні напої', 'A/B/C', '#F4D03F'),
    'frozen':  ('Заморожені продукти', 'A/B/C', '#AED6F1'),
    'fish':    ('Рибна продукція', 'A', '#48C9B0'),
    'bakal':   ('Бакалія, кава, чай', 'A/B/C', '#F0B27A'),
    'bread':   ('Хлібобулочні вироби', 'A/C', '#DBB98B'),
    'fruit':   ('Фрукти та овочі свіжі', 'B', '#82E0AA'),
    'other':   ('Супутні та непродовольчі товари', 'A/B/C', '#BFC9CA'),
    'checkout': ('Прикасова зона', 'A/C', '#F5B7B1'),
    'cash':    ('Розрахунковий вузол', '-', '#E74C3C'),
    'entry':   ('Вхідна зона', '-', '#95A5A6'),
}
for k, (n, g, c) in DEPTS.items():
    mat('Відділ — ' + n, c)
    mat('Відділ — ' + n + ' (світлий)', shade(c, 1.4))


def dm(d, light=False):
    return 'Відділ — ' + DEPTS[d][0] + (' (світлий)' if light else '')


PALETTE = ['#E53935', '#FB8C00', '#FDD835', '#43A047', '#1E88E5', '#8E24AA',
           '#00ACC1', '#F06292', '#6D4C41', '#FFFFFF', '#263238', '#C0CA33']


def pm(c):
    return mat('Упаковка ' + c, c)


def rnd(lst=PALETTE):
    return pm(random.choice(lst))


# ---------------------------------------------------------------- товари
def bottle(g, x, y, z, r, h, glass, label):
    cyl(g, glass, (x, y, z), r, h * 0.68, 'z', 6, caps=False)
    cyl(g, glass, (x, y, z + h * 0.68), r, h * 0.12, 'z', 6, caps=False, r2=r * 0.35)
    box(g, glass, x - r * 0.35, y - r * 0.35, z + h * 0.8, x + r * 0.35, y + r * 0.35, z + h, False)
    box(g, label, x - r * 0.95, y - r * 1.02, z + h * 0.25, x + r * 0.95, y - r * 0.9, z + h * 0.5, False)


def food(g, kind, x0, x1, y0, y1, z, hmax, base='#999999'):
    """Заповнює ділянку полиці [x0,x1]×[y0,y1] (фронт — y0) на висоті z."""
    d = y1 - y0
    x = x0 + 0.02
    hmax = max(0.06, hmax)
    if kind in ('wine', 'vodka', 'beer'):
        glasses = {'wine': ['#3E6B2F', '#5B2333', '#2F4F2F'], 'vodka': ['#DCEAF0', '#E8F1F5'],
                   'beer': ['#6B3E1F', '#3E6B2F', '#8A5A2B']}[kind]
        hb = {'wine': 0.31, 'vodka': 0.3, 'beer': 0.24}[kind]
        r = 0.036 if kind != 'beer' else 0.03
        while x + 2 * r < x1:
            gm = mat('Скло пляшок ' + (c := random.choice(glasses)), c, 0.85 if kind == 'vodka' else 1.0)
            bottle(g, x + r, y0 + 0.06, z, r, min(hb, hmax - 0.02), gm, rnd())
            x += 2 * r + 0.012
        box(g, pm('#7F8C8D'), x0 + 0.02, y0 + 0.14, z, x1 - 0.02, y1 - 0.02, z + min(hb, hmax) * 0.7, False)
        return
    if kind == 'cartons':                                   # молоко, кефір, соки
        while x + 0.075 < x1:
            h = min(hmax - 0.02, random.choice([0.2, 0.2, 0.24, 0.12]))
            body = pm(random.choice(['#FFFFFF', '#FFFFFF', '#F7F3E8', '#FFF59D'])) if base != 'juice' else rnd()
            for yy in (y0 + 0.04, y0 + 0.13):
                box(g, body, x, yy, z, x + 0.07, yy + 0.07, z + h, False)
            box(g, rnd(['#1E88E5', '#43A047', '#E53935', '#FB8C00']), x, y0 + 0.037, z + h * 0.45, x + 0.07, y0 + 0.04, z + h * 0.8, False)
            x += 0.078
        if y1 - y0 > 0.3:
            box(g, pm('#ECEFF1'), x0 + 0.02, y0 + 0.22, z, x1 - 0.02, y1 - 0.03, z + min(0.2, hmax - 0.02), False)
        return
    if kind == 'cups':                                       # йогурти, сметана
        while x + 0.08 < x1:
            col = rnd(['#FFFFFF', '#F8BBD0', '#FFF59D', '#C8E6C9', '#BBDEFB'])
            for yy in (y0 + 0.06, y0 + 0.15):
                cyl(g, col, (x + 0.04, yy, z), 0.038, min(0.09, hmax - 0.01), 'z', 8)
            x += 0.085
        return
    if kind == 'eggs':
        while x + 0.3 < x1:
            for k in range(2):
                box(g, pm('#D7CCC8'), x, y0 + 0.04, z + k * 0.07, x + 0.28, y0 + 0.16, z + k * 0.07 + 0.065)
            x += 0.31
        return
    if kind == 'sausage':
        while x + 0.06 < x1:
            col = rnd(['#C0392B', '#A93226', '#D98880', '#922B21', '#E6B0AA'])
            if random.random() < 0.6:
                cyl(g, col, (x + 0.03, y0 + 0.03, z + 0.035), 0.033, min(0.32, d - 0.05), 'y', 8)
                x += 0.07
            else:
                box(g, col, x, y0 + 0.03, z, x + 0.16, y0 + 0.2, z + 0.04)
                box(g, M_GLASS, x, y0 + 0.03, z + 0.04, x + 0.16, y0 + 0.2, z + 0.045, False)
                x += 0.17
        return
    if kind == 'cheese':
        while x + 0.2 < x1:
            col = pm(random.choice(['#F7DC6F', '#F9E79F', '#F5CBA7', '#FAD7A0']))
            if random.random() < 0.5:
                cyl(g, col, (x + 0.1, y0 + 0.15, z), 0.1, 0.09, 'z', 12)
            else:
                prism_x(g, col, x, x + 0.18, [(y0 + 0.05, z), (y0 + 0.28, z), (y0 + 0.28, z + 0.1)])
            x += 0.22
        return
    if kind == 'fish':
        while x + 0.08 < x1:
            if random.random() < 0.5:
                for k in range(3):
                    cyl(g, rnd(['#B0BEC5', '#90A4AE', '#FFD54F']), (x + 0.04, y0 + 0.08, z + k * 0.035), 0.04, 0.034, 'z', 8)
                x += 0.09
            else:
                box(g, rnd(['#E59866', '#F5B041', '#D35400']), x, y0 + 0.03, z, x + 0.2, y0 + 0.22, z + 0.035)
                x += 0.21
        return
    if kind == 'bread':
        while x + 0.12 < x1:
            col = pm(random.choice(['#C68E4E', '#A0662E', '#D9A066', '#8D5A2B', '#E8C07D']))
            r = random.random()
            if r < 0.4:                                      # буханка
                box(g, col, x, y0 + 0.05, z, x + 0.12, y0 + 0.3, z + 0.07)
                cyl(g, col, (x + 0.06, y0 + 0.05, z + 0.07), 0.06, 0.25, 'y', 8)
                x += 0.14
            elif r < 0.7:                                    # батон
                cyl(g, col, (x + 0.045, y0 + 0.03, z + 0.045), 0.045, min(0.4, d - 0.05), 'y', 8)
                x += 0.1
            else:                                            # булочки
                for yy in (y0 + 0.07, y0 + 0.19):
                    sphere(g, col, (x + 0.05, yy, z + 0.03), 0.05, 8, 4, zscale=0.6)
                x += 0.11
        return
    if kind == 'frozen':
        while x + 0.15 < x1:
            for k in range(random.randint(1, 3)):
                box(g, rnd(['#1E88E5', '#E53935', '#FFFFFF', '#43A047', '#FDD835', '#90CAF9']),
                    x, y0 + 0.02, z + k * 0.05, x + 0.15, y1 - 0.02, z + k * 0.05 + 0.045)
            x += 0.16
        return
    if kind == 'jars':
        while x + 0.09 < x1:
            col = pm(random.choice(['#E74C3C', '#F39C12', '#27AE60', '#8E44AD', '#D35400']))
            for yy in (y0 + 0.06, y0 + 0.16):
                cyl(g, col, (x + 0.04, yy, z), 0.04, 0.11, 'z', 8, caps=False)
                cyl(g, pm('#BDC3C7'), (x + 0.04, yy, z + 0.11), 0.042, 0.02, 'z', 8)
            x += 0.09
        return
    if kind == 'bags':                                      # крупи, борошно, цукор
        while x + 0.12 < x1:
            h = min(hmax - 0.02, random.uniform(0.18, 0.28))
            col = rnd(['#FFF8E1', '#FFFFFF', '#FFE082', '#D7CCC8', '#C5E1A5'])
            for yy in (y0 + 0.04, y0 + 0.14):
                box(g, col, x, yy, z, x + 0.11, yy + 0.08, z + h, False)
            x += 0.12
        return
    # 'boxes' — кондитерка, чай, кава, побутова хімія тощо
    while True:
        w = random.uniform(0.08, 0.24)
        if x + w > x1:
            break
        h = random.uniform(0.35, 0.9) * (hmax - 0.02)
        col = rnd() if random.random() < 0.7 else pm(shade(base, random.choice([0.7, 0.85, 1.0, 1.2])))
        box(g, col, x, y0 + 0.03, z, x + w, y0 + 0.03 + d * random.uniform(0.55, 0.9), z + h, False)
        x += w + random.uniform(0.006, 0.02)


DEPT_KIND = {'alco': ['wine', 'vodka'], 'drinks': ['beer', 'cartons_juice'], 'confect': ['boxes'],
             'bakal': ['bags', 'jars', 'boxes'], 'other': ['boxes'], 'bread': ['bread'],
             'checkout': ['boxes']}


def kind_for(dept, level):
    ks = DEPT_KIND[dept]
    return ks[level % len(ks)]


def food_k(g, kind, dept, *a):
    if kind == 'cartons_juice':
        return food(g, 'cartons', *a, base='juice')
    return food(g, kind, *a, base=DEPTS[dept][2])


# ---------------------------------------------------------------- обладнання
def price_strip(g, dept, x0, x1, y, z):
    box(g, dm(dept), x0, y - 0.02, z - 0.04, x1, y, z, False)


def island_rack(g, dept_front, dept_back, n=5):
    """Острівний двосторонній стелаж «Колумб» n × 1250 мм, 1200 × 1625 мм (фронт — y=0)."""
    w, d, h = 1.25 * n, 1.2, 1.625
    box(g, M_RACK, 0, 0.08, 0, w, d - 0.08, 0.1)
    box(g, M_RACK, 0, d / 2 - 0.02, 0.1, w, d / 2 + 0.02, h)              # перфопанель
    for i in range(n + 1):
        xx = min(i * 1.25, w - 0.04)
        box(g, M_DARK, xx, d / 2 - 0.05, 0, xx + 0.04, d / 2 + 0.05, h)  # стійки
    levels = [0.1, 0.45, 0.8, 1.15, 1.48]
    for side, dept in ((0, dept_front), (1, dept_back)):
        old = g.xf
        g.xf = (bm.Xf(w, d, 0, 180) if side else bm.Xf()).then(old)
        for li, z0 in enumerate(levels):
            depth = 0.5 if li < 2 else 0.4
            y0 = d / 2 - 0.02 - depth
            if z0 > 0.1:
                box(g, M_RACK, 0.02, y0, z0 - 0.02, w - 0.02, d / 2 - 0.02, z0)
            top = levels[li + 1] if li + 1 < len(levels) else h + 0.2
            kind = kind_for(dept, li)
            for s in range(n):
                food_k(g, kind, dept, s * 1.25 + 0.05, s * 1.25 + 1.21, y0 + 0.01, d / 2 - 0.04, z0, top - z0 - 0.03)
            if z0 > 0.1:
                price_strip(g, dept, 0.02, w - 0.02, y0, z0)
        box(g, dm(dept), 0, -0.002, 0.02, w, 0.0, 0.09, False)            # цоколь у кольорі відділу
        g.xf = old
    for xx in (-0.03, w):                                                  # торцеві панелі
        box(g, dm(dept_front), xx, 0.05, 0.1, xx + 0.03, d / 2, h + 0.1)
        box(g, dm(dept_back), xx, d / 2, 0.1, xx + 0.03, d - 0.05, h + 0.1)


def wall_rack(g, dept):
    """Пристінний стелаж «Колумб», секція 1250 × 500 × 2080 (фронт — y=0)."""
    w, d, h = 1.25, 0.5, 2.08
    box(g, M_RACK, 0, 0.06, 0, w, d, 0.1)
    box(g, M_RACK, 0, d - 0.03, 0.1, w, d, h)
    for xx in (0, w - 0.04):
        box(g, M_DARK, xx, d - 0.06, 0, xx + 0.04, d, h)
    levels = [0.1, 0.45, 0.8, 1.15, 1.5, 1.82]
    for li, z0 in enumerate(levels):
        if z0 > 0.1:
            box(g, M_RACK, 0.02, 0.02, z0 - 0.02, w - 0.02, d - 0.03, z0)
        top = levels[li + 1] if li + 1 < len(levels) else h + 0.15
        food_k(g, kind_for(dept, li), dept, 0.05, w - 0.05, 0.02, d - 0.05, z0, top - z0 - 0.03)
        if z0 > 0.1:
            price_strip(g, dept, 0.02, w - 0.02, 0.02, z0)
    box(g, dm(dept), 0, d - 0.12, h + 0.05, w, d - 0.04, h + 0.3)          # фриз


def multideck(g, dept, kinds):
    """Холодильна гірка (регал) 2500 × 900 × 2000 (фронт — y=0)."""
    w, d, h = 2.5, 0.9, 2.0
    body = mat('Холодильне обладнання корпус', '#ECEFF1')
    box(g, body, 0, 0.12, 0, w, d, 0.42)                                   # нижня частина
    box(g, dm(dept), 0, 0.12, 0.05, w, 0.125, 0.38, False)
    box(g, body, 0, d - 0.12, 0.42, w, d, h)                               # задня стінка
    box(g, body, 0, 0.25, h - 0.18, w, d, h)                               # козирок
    box(g, M_LIGHT, 0.05, 0.25, h - 0.19, w - 0.05, d - 0.15, h - 0.18, False)
    box(g, dm(dept), 0, 0.24, h - 0.16, w, 0.25, h - 0.02, False)          # кольорова панель
    for xx in (0, w - 0.03):                                               # бокові скляні панелі
        box(g, body, xx, 0.12, 0.42, xx + 0.03, d, 0.5)
        box(g, M_GLASS, xx, 0.15, 0.5, xx + 0.03, d - 0.12, h - 0.18)
    box(g, M_METAL, 0.03, 0.05, 0.42, w - 0.03, 0.12, 0.47)                # бортик
    levels = [0.47, 0.82, 1.14, 1.46]
    for li, z0 in enumerate(levels):
        depth = 0.66 - li * 0.06
        y0 = d - 0.12 - depth
        if li:
            box(g, M_METAL, 0.03, y0, z0 - 0.02, w - 0.03, d - 0.12, z0)
            box(g, dm(dept), 0.03, y0 - 0.02, z0 - 0.045, w - 0.03, y0, z0, False)
        top = levels[li + 1] if li + 1 < len(levels) else h - 0.2
        food(g, kinds[li % len(kinds)], 0.06, w - 0.06, y0 + 0.01, d - 0.14, z0, top - z0 - 0.03, DEPTS[dept][2])


def counter(g, dept):
    """Холодильна вітрина-прилавок 2500 × 1100 × 1250 (покупець — y=0, продавець — y=d)."""
    w, d = 2.5, 1.1
    body = mat('Вітрина гастрономії корпус', '#ECEFF1')
    box(g, body, 0, 0.1, 0, w, d, 0.85)
    box(g, dm(dept), 0, 0.095, 0.15, w, 0.1, 0.6, False)
    box(g, M_WOOD, 0, 0.0, 0.85, w, 0.12, 0.9)                             # полиця для покупця
    box(g, M_METAL, 0.03, 0.15, 0.85, w - 0.03, d - 0.25, 0.88)            # викладка
    box(g, M_WHITE, 0, d - 0.25, 0.85, w, d, 0.95)                         # робоче місце продавця
    for xx in (0, w - 0.03):
        prism_y(g, body, 0.1, d - 0.25, [(xx, 0.85), (xx + 0.03, 0.85), (xx + 0.03, 1.25), (xx, 1.25)])
    prism_x(g, M_GLASS, 0.03, w - 0.03, [(0.12, 0.86), (0.16, 0.86), (0.48, 1.25), (0.44, 1.25)])
    box(g, M_GLASS, 0.03, 0.44, 1.23, w - 0.03, d - 0.25, 1.25)
    box(g, M_LIGHT, 0.05, 0.6, 1.21, w - 0.05, d - 0.3, 1.23, False)
    old = g.xf
    for i, kind in enumerate(['cheese', 'sausage', 'cheese'] if dept == 'gastro' else ['sausage'] * 3):
        food(g, kind, 0.08 + i * 0.8, 0.08 + i * 0.8 + 0.75, 0.18, d - 0.3, 0.88, 0.3, DEPTS[dept][2])
    g.xf = old
    for xx in (0.5, 1.6):                                                  # ваги
        box(g, M_WHITE, xx, d - 0.2, 0.95, xx + 0.3, d - 0.05, 1.0)
        box(g, M_DARK, xx + 0.1, d - 0.12, 1.0, xx + 0.2, d - 0.1, 1.15)


def wall_shelf_staff(g):
    """Пристінний стелаж за прилавком 6000 × 500 × 1800."""
    w, d, h = 6.0, 0.5, 1.8
    box(g, M_RACK, 0, d - 0.03, 0, w, d, h)
    for i in range(5):
        xx = min(i * 1.5, w - 0.04)
        box(g, M_DARK, xx, d - 0.06, 0, xx + 0.04, d, h)
    for li, z0 in enumerate([0.1, 0.5, 0.9, 1.3, 1.65]):
        box(g, M_RACK, 0, 0.02, z0 - 0.02, w, d - 0.03, z0)
        if z0 < 1.6:
            food(g, ['boxes', 'jars', 'wine', 'boxes'][li], 0.05, w - 0.05, 0.03, d - 0.05, z0, 0.36, '#E8A87C')


def fridge_cabinet(g, dept):
    """Холодильна шафа 700 × 750 × 2000 зі скляними дверима (фронт — y=0)."""
    w, d, h = 0.7, 0.75, 2.0
    body = mat('Холодильна шафа корпус', '#F5F5F5')
    box(g, body, 0, 0.05, 0, w, d, h)
    box(g, dm(dept), 0, 0.045, h - 0.28, w, 0.05, h - 0.03, False)         # лайтбокс
    box(g, M_FRAME, 0.02, 0.0, 0.1, w - 0.02, 0.05, 0.14)
    box(g, M_FRAME, 0.02, 0.0, h - 0.33, w - 0.02, 0.05, h - 0.29)
    for xx in (0.02, w - 0.06):
        box(g, M_FRAME, xx, 0.0, 0.1, xx + 0.04, 0.05, h - 0.29)
    box(g, M_GLASS, 0.06, 0.015, 0.14, w - 0.06, 0.025, h - 0.33)
    box(g, M_DARK, w - 0.1, -0.03, 0.8, w - 0.08, 0.0, 1.4)                # ручка
    for li, z0 in enumerate([0.15, 0.5, 0.85, 1.2]):
        box(g, M_METAL, 0.06, 0.06, z0 - 0.015, w - 0.06, d - 0.06, z0)
        food_k(g, kind_for('drinks', li), 'drinks', 0.07, w - 0.07, 0.07, d - 0.08, z0, 0.32)


def freezer(g):
    """Морозильна бонета 2000 × 900 × 900, доступ з обох довгих боків."""
    w, d, h = 2.0, 0.9, 0.9
    body = mat('Бонета корпус', '#F4F6F7')
    box(g, body, 0, 0, 0.05, w, d, 0.4)                                    # дно ванни
    box(g, M_DARK, 0.04, 0.04, 0, w - 0.04, d - 0.04, 0.05)
    for yy in (0, d):
        box(g, dm('frozen'), 0, yy - 0.002, 0.1, w, yy + 0.002, 0.5, False)
    box(g, body, 0, 0, 0.4, w, 0.04, h)                                    # борти
    box(g, body, 0, d - 0.04, 0.4, w, d, h)
    box(g, body, 0, 0, 0.4, 0.04, d, h)
    box(g, body, w - 0.04, 0, 0.4, w, d, h)
    box(g, body, 0.04, d / 2 - 0.015, 0.4, w - 0.04, d / 2 + 0.015, h)    # розділювач
    box(g, M_GLASS, 0.04, 0.04, h - 0.02, w / 2, d - 0.04, h)              # розсувне скло
    box(g, M_GLASS, w / 2, 0.04, h - 0.04, w - 0.04, d - 0.04, h - 0.02)
    for y0, y1 in ((0.05, d / 2 - 0.02), (d / 2 + 0.02, d - 0.05)):
        x = 0.06
        while x + 0.12 < w - 0.06:                                         # стоси пачок і пакетів
            ww = random.uniform(0.12, 0.2)
            for k in range(random.randint(3, 5)):
                box(g, rnd(['#1565C0', '#C62828', '#2E7D32', '#F9A825', '#6A1B9A', '#EF6C00', '#00838F']),
                    x, y0, 0.42 + k * 0.06, x + ww, y1, 0.42 + k * 0.06 + 0.055)
            x += ww + 0.01


FRUITS = [('#C62828', 0.04), ('#7CB342', 0.04), ('#FB8C00', 0.045), ('#FDD835', 0.035),
          ('#6A1B9A', 0.03), ('#E53935', 0.03), ('#8D6E63', 0.04), ('#F9A825', 0.05), ('#33691E', 0.06)]


def fruit_island(g):
    """Острівна гірка для фруктів та овочів 2000 × 1200 × 1100 (ящики з двох боків)."""
    w, d = 2.0, 1.2
    box(g, M_WOOD, 0, 0.1, 0, w, d - 0.1, 0.45)
    prism_x(g, M_WOOD, 0, w, [(0.1, 0.45), (d - 0.1, 0.45), (d / 2, 0.95)])
    box(g, dm('fruit'), 0, d / 2 - 0.02, 0.9, w, d / 2 + 0.02, 1.1)        # табличка-гребінь
    for side in (0, 1):
        old = g.xf
        g.xf = (bm.Xf(w, d, 0, 180) if side else bm.Xf()).then(old)
        for tier, (y0, z0) in enumerate(((0.0, 0.45), (0.3, 0.72))):
            for i in range(4):
                x0 = 0.03 + i * 0.49
                box(g, M_CRATE, x0, y0, z0 - 0.12, x0 + 0.45, y0 + 0.3, z0, True)
                col, r = random.choice(FRUITS)
                fm = mat('Фрукти ' + col, col)
                for a in range(int(0.4 / (2 * r))):
                    for b in range(int(0.26 / (2 * r))):
                        sphere(g, fm, (x0 + 0.03 + r + a * 2 * r, y0 + 0.02 + r + b * 2 * r, z0 + r * 0.6), r, 6, 4)
                box(g, M_WHITE, x0 + 0.15, y0 - 0.01, z0 - 0.1, x0 + 0.3, y0, z0 - 0.04, False)  # цінник
        g.xf = old


def checkout_box(g):
    """Касовий бокс Magellan 2105-000: 1115 × 2248 × 900; покупці рухаються від y=d до y=0."""
    w, d, h = 1.115, 2.248, 0.9
    box(g, M_CASH, 0.45, 0.0, 0.0, w, d, h - 0.05)                         # тумба з транспортером
    box(g, M_METAL, 0.45, 0.0, h - 0.05, w, d, h)
    box(g, M_BELT, 0.5, 1.15, h, w - 0.05, d - 0.05, h + 0.01, False)      # стрічка
    box(g, M_METAL, 0.48, 1.12, h, w - 0.02, 1.15, h + 0.06)               # розділювач
    box(g, M_DARK, 0.6, 0.85, h, 0.95, 1.1, h + 0.03)                      # сканер
    box(g, M_GLASS, 0.62, 0.87, h + 0.03, 0.93, 1.08, h + 0.032, False)
    box(g, M_METAL, 0.45, 0.0, h - 0.2, w, 0.75, h - 0.15)                 # накопичувач
    box(g, M_CASH, 0.0, 0.75, 0.0, 0.45, 1.5, 0.75)                        # робоче місце касира
    box(g, M_METAL, 0.0, 0.75, 0.75, 0.45, 1.5, 0.78)
    box(g, M_DARK, 0.05, 0.95, 0.78, 0.3, 1.3, 0.88)                       # грошова скринька
    cyl(g, M_DARK, (0.25, 1.15, 0.78), 0.02, 0.3, 'z', 6, False)
    box(g, M_DARK, 0.12, 1.05, 1.08, 0.38, 1.25, 1.1)
    box(g, M_DARK, 0.12, 1.07, 1.1, 0.38, 1.09, 1.3)                       # монітор
    box(g, M_SCREEN, 0.13, 1.065, 1.11, 0.37, 1.07, 1.29, False)
    box(g, M_DARK, 0.85, 0.5, h, 0.95, 0.6, h + 0.12)                      # POS-термінал
    cyl(g, M_DARK, (-0.3, 1.1, 0), 0.25, 0.04, 'z', 10)                    # крісло касира
    cyl(g, M_METAL, (-0.3, 1.1, 0.04), 0.03, 0.45, 'z', 6)
    cyl(g, mat('Сидіння', '#37474F'), (-0.3, 1.1, 0.49), 0.2, 0.08, 'z', 12)
    box(g, mat('Сидіння', '#37474F'), -0.5, 1.28, 0.55, -0.1, 1.32, 0.9)
    cyl(g, M_METAL, (0.75, 1.6, h), 0.012, 0.9, 'z', 5, False)             # номер каси
    box(g, M_CASH, 0.65, 1.58, h + 0.9, 0.85, 1.62, h + 1.1)


def checkout_rack(g):
    """Прикасовий стелаж 600 × 400 × 1400."""
    w, d, h = 0.6, 0.4, 1.4
    box(g, M_RACK, 0, d - 0.03, 0, w, d, h)
    for xx in (0, w - 0.03):
        box(g, M_RACK, xx, 0, 0, xx + 0.03, d, h)
    for z0 in (0.1, 0.38, 0.66, 0.94, 1.2):
        box(g, M_RACK, 0.03, 0.0, z0 - 0.015, w - 0.03, d - 0.03, z0)
        food(g, 'boxes', 0.04, w - 0.04, 0.02, d - 0.05, z0, 0.22, '#F5B7B1')
    box(g, dm('checkout'), 0, d - 0.06, h, w, d - 0.02, h + 0.18)


def pack_table(g):
    """Стіл для пакування покупок 1500 × 600 × 850."""
    w, d, h = 1.5, 0.6, 0.85
    box(g, M_METAL, 0, 0, h - 0.04, w, d, h)
    for xx in (0.03, w - 0.07):
        for yy in (0.03, d - 0.07):
            box(g, M_DARK, xx, yy, 0, xx + 0.04, yy + 0.04, h - 0.04)
    box(g, M_METAL, 0.05, 0.05, 0.15, w - 0.05, d - 0.05, 0.17)
    box(g, pm('#ECEFF1'), 0.1, 0.1, h, 0.4, 0.3, h + 0.15)                 # пакети


def locker(g):
    """Камера схову 1000 × 500 × 1800 (8 комірок)."""
    w, d, h = 1.0, 0.5, 1.8
    box(g, mat('Камера схову', '#90A4AE'), 0, 0.01, 0, w, d, h)
    for i in range(2):
        for j in range(4):
            x0, z0 = 0.02 + i * 0.48, 0.05 + j * 0.43
            box(g, mat('Дверцята камери схову', '#B0BEC5'), x0, 0.0, z0, x0 + 0.46, 0.01, z0 + 0.41, False)
            box(g, M_DARK, x0 + 0.38, -0.015, z0 + 0.15, x0 + 0.41, 0.0, z0 + 0.25, False)


# ---------------------------------------------------------------- підсобні приміщення
def pallet_stack(g, x, y, w=1.2, d=0.8, n=3):
    box(g, M_WOOD, x, y, 0, x + w, y + d, 0.14)
    for k in range(n):
        for a in range(3):
            for b in range(2):
                box(g, pm(random.choice(['#C8A27A', '#B8926A', '#D7B98E'])), x + 0.02 + a * w / 3, y + 0.02 + b * d / 2,
                    0.14 + k * 0.3, x + (a + 1) * w / 3 - 0.02, y + (b + 1) * d / 2 - 0.02, 0.14 + (k + 1) * 0.3 - 0.01)


def storage_rack(g, x, y, length, depth=0.6, along='x', levels=(0.0, 0.7, 1.4, 2.1), h=2.4):
    if along == 'x':
        x1, y1 = x + length, y + depth
    else:
        x1, y1 = x + depth, y + length
    for cx in (x, x1 - 0.05):
        for cy in (y, y1 - 0.05):
            box(g, M_DARK, cx, cy, 0, cx + 0.05, cy + 0.05, h)
    for z in levels:
        box(g, M_METAL, x, y, z + 0.08, x1, y1, z + 0.11)
        n = int((x1 - x if along == 'x' else y1 - y) / 0.45)
        for i in range(n):
            if random.random() < 0.8:
                if along == 'x':
                    box(g, pm(random.choice(['#C8A27A', '#B8926A', '#D7B98E', '#ECEFF1'])), x + 0.03 + i * 0.45, y + 0.05,
                        z + 0.11, x + 0.43 + i * 0.45, y1 - 0.05, z + 0.11 + random.uniform(0.25, 0.5))
                else:
                    box(g, pm(random.choice(['#C8A27A', '#B8926A', '#D7B98E', '#ECEFF1'])), x + 0.05, y + 0.03 + i * 0.45,
                        z + 0.11, x1 - 0.05, y + 0.43 + i * 0.45, z + 0.11 + random.uniform(0.25, 0.5))


def desk(g, x, y, w=1.4, d=0.7, monitor=True):
    box(g, M_WOOD, x, y, 0.72, x + w, y + d, 0.75)
    for xx in (x + 0.03, x + w - 0.07):
        box(g, M_DARK, xx, y + 0.05, 0, xx + 0.04, y + d - 0.05, 0.72)
    if monitor:
        box(g, M_DARK, x + w / 2 - 0.25, y + d - 0.15, 0.75, x + w / 2 + 0.25, y + d - 0.12, 1.1)
        box(g, M_SCREEN, x + w / 2 - 0.23, y + d - 0.152, 0.77, x + w / 2 + 0.23, y + d - 0.15, 1.08, False)
    cyl(g, mat('Сидіння', '#37474F'), (x + w / 2, y - 0.35, 0.42), 0.22, 0.07, 'z', 10)
    cyl(g, M_DARK, (x + w / 2, y - 0.35, 0), 0.03, 0.42, 'z', 6)


ROOMS = [  # назва, x0, y0, x1, y1  (за рис. 3.1)
    ('Тарна', 0, 21.0, 6.0, 25), ('Приймальна', 0, 16, 6.0, 21.0), ('Комора сухих товарів', 6.0, 19.0, 14.0, 25),
    ('Камера молочних', 14.0, 22.0, 17.0, 25), ('Камера м’ясо-ковбасних', 17.0, 22.0, 20.0, 25),
    ('Фасувальна', 20.0, 22.0, 25, 25), ('Низькотемп. камера', 14.0, 19.0, 17.0, 22.0),
    ('Камера фруктів і овочів', 17.0, 19.0, 20.0, 22.0), ('Кабінет директора', 20.0, 19.0, 22.5, 22.0),
    ('Бухгалтерія', 22.5, 19.0, 25, 22.0), ('Кімната персоналу', 6.0, 16, 10.0, 19.0),
    ('Гардероби', 10.0, 16, 12.5, 19.0), ('Санвузли', 12.5, 16, 14.5, 19.0), ('Коридор', 14.5, 17.6, 25, 19.0),
    ('Електрощитова', 14.5, 16, 17.0, 17.6), ('Машинне відділення', 17.0, 16, 19.5, 17.6),
    ('Вентиляційна камера', 19.5, 16, 21.5, 17.6), ('Охорона, інвентар', 21.5, 16, 25, 17.6),
]
DOORS = [  # (вісь 'x'|'y', координата лінії, від, до) — прорізи у перегородках
    ('x', 6.0, 19.6, 20.6), ('y', 21.0, 2.4, 3.6), ('y', 19.0, 7.0, 8.0), ('x', 10.0, 17.0, 17.9),
    ('x', 12.5, 17.0, 17.9), ('x', 14.5, 17.9, 18.8), ('y', 19.0, 15.0, 16.2), ('y', 19.0, 18.0, 19.2),
    ('y', 19.0, 20.8, 21.7), ('y', 19.0, 23.2, 24.1), ('y', 22.0, 21.0, 21.9), ('y', 22.0, 15.0, 16.2),
    ('y', 22.0, 18.0, 19.2), ('y', 17.6, 15.2, 16.0), ('y', 17.6, 17.8, 18.6), ('y', 17.6, 20.0, 20.8),
    ('y', 17.6, 22.6, 23.5), ('y', 16.0, 22.1, 23.4),
]
COLD = {'Камера молочних', 'Камера м’ясо-ковбасних', 'Низькотемп. камера', 'Камера фруктів і овочів'}


def build_partitions():
    """Перегородки за ребрами кімнат мінус дверні прорізи."""
    segs = {}
    for _, x0, y0, x1, y1 in ROOMS:
        for (ax, c, a, b) in (('y', y0, x0, x1), ('y', y1, x0, x1), ('x', x0, y0, y1), ('x', x1, y0, y1)):
            if (ax == 'x' and c in (0, L)) or (ax == 'y' and c in (D_ALL,)):
                continue                                             # зовнішні стіни окремо
            segs.setdefault((ax, round(c, 3)), []).append((a, b))
    g = new_group('Перегородки підсобного блоку', 'Будівля')
    t = 0.12
    for (ax, c), iv in segs.items():
        iv.sort()
        merged = []
        for a, b in iv:
            if merged and a <= merged[-1][1] + 1e-6:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        for a, b in merged:
            cuts = sorted((d0, d1) for (dax, dc, d0, d1) in DOORS if dax == ax and abs(dc - c) < 1e-6)
            pos = a
            pieces = []
            for d0, d1 in cuts:
                if d1 <= a or d0 >= b:
                    continue
                pieces.append((pos, d0, True))
                pieces.append((d0, d1, False))
                pos = d1
            pieces.append((pos, b, True))
            for p0, p1, solid in pieces:
                if p1 - p0 < 1e-3:
                    continue
                zb = 0 if solid else 2.2
                m = M_PANEL if c == D_HALL and ax == 'y' else M_PART
                hh = H
                if ax == 'y':
                    box(g, m, p0, c - t / 2 if c != D_HALL else c, zb, p1, c + t / 2 if c != D_HALL else c + WALL, hh)
                else:
                    box(g, m, c - t / 2, p0, zb, c + t / 2, p1, hh)


def build_back_rooms():
    g = new_group('Підлога підсобних приміщень', 'Будівля')
    box(g, M_FLOOR_S, 0, D_HALL, -0.02, L, D_ALL, 0.0, False)
    build_partitions()
    # двері холодильних камер
    g = new_group('Двері холодильних камер', 'Будівля')
    for (_, c, a, b) in [d for d in DOORS if d[1] in (19.0, 22.0) and d[2] in (15.0, 18.0)]:
        box(g, M_COLD_DOOR, a + 0.05, c - 0.1, 0, a + 0.6, c - 0.06, 2.15)
    # наповнення
    g = new_group('Приймальна: піддони, ваги, візок', 'Підсобні приміщення')
    pallet_stack(g, 1.0, 17.0); pallet_stack(g, 2.5, 17.0, n=2); pallet_stack(g, 1.0, 19.0, n=4)
    box(g, M_METAL, 3.8, 19.3, 0, 4.8, 20.3, 0.08); box(g, M_DARK, 4.6, 19.3, 0.08, 4.65, 20.3, 1.0)
    box(g, mat('Гідравлічний візок', '#F39C12'), 3.9, 17.2, 0, 4.5, 18.4, 0.12)
    cyl(g, M_DARK, (4.2, 18.45, 0.12), 0.02, 1.0, 'z', 6)
    g = new_group('Тарна: ящики і контейнери', 'Підсобні приміщення')
    for i in range(6):
        for j in range(2):
            for k in range(random.randint(3, 7)):
                box(g, pm(random.choice(['#1565C0', '#2E7D32', '#C62828', '#F9A825'])), 0.5 + i * 0.85, 22.0 + j * 1.6,
                    k * 0.25, 1.1 + i * 0.85, 22.4 + j * 1.6, k * 0.25 + 0.24)
    g = new_group('Комора сухих товарів: стелажі', 'Підсобні приміщення')
    for i in range(3):
        storage_rack(g, 7.0 + i * 2.2, 20.0, 4.5, along='y')
    storage_rack(g, 6.3, 24.3, 7.3, along='x')
    for name, x0, y0 in (('молочних', 14, 22), ('м’ясо-ковбасних', 17, 22), ('низькотемп.', 14, 19), ('фруктів', 17, 19)):
        g = new_group(f'Камера {name}: стелажі', 'Підсобні приміщення')
        storage_rack(g, x0 + 0.2, y0 + 2.2, 2.6, depth=0.6, along='x', levels=(0.0, 0.6, 1.2, 1.8), h=2.1)
        if 'фрукт' in name:
            pallet_stack(g, x0 + 1.5, y0 + 0.4, 1.0, 0.8, 2)
    g = new_group('Фасувальна: столи, ваги, пакувальник', 'Підсобні приміщення')
    for xx in (20.5, 22.4):
        box(g, M_METAL, xx, 24.2, 0.86, xx + 1.6, 24.9, 0.9)
        for cx in (xx + 0.05, xx + 1.5):
            box(g, M_METAL, cx, 24.25, 0, cx + 0.05, 24.85, 0.86)
        box(g, M_WHITE, xx + 0.2, 24.4, 0.9, xx + 0.55, 24.75, 0.98)
    box(g, M_METAL, 24.2, 22.3, 0, 24.9, 23.5, 1.2)
    g = new_group('Кабінет директора та бухгалтерія', 'Підсобні приміщення')
    desk(g, 20.4, 20.9); desk(g, 22.8, 20.9); desk(g, 23.9, 19.5, 0.9, 0.6, False)
    box(g, M_WOOD, 20.2, 21.5, 0, 20.6, 21.9, 1.9)
    g = new_group('Кімната персоналу', 'Підсобні приміщення')
    box(g, M_WOOD, 7.2, 17.0, 0.72, 8.8, 17.9, 0.75)
    for xx in (7.3, 8.6):
        box(g, M_DARK, xx, 17.05, 0, xx + 0.05, 17.85, 0.72)
    for xx in (7.4, 8.2):
        for yy in (16.6, 18.2):
            box(g, mat('Стільці', '#5D6D7E'), xx, yy, 0.42, xx + 0.4, yy + 0.4, 0.46)
            box(g, M_DARK, xx + 0.18, yy + 0.18, 0, xx + 0.22, yy + 0.22, 0.42)
    box(g, M_WHITE, 6.2, 18.3, 0, 7.0, 18.9, 0.9); box(g, M_METAL, 9.2, 18.3, 0, 9.85, 18.9, 1.8)
    g = new_group('Гардероби: шафи', 'Підсобні приміщення')
    for i in range(4):
        box(g, mat('Шафи для одягу', '#AAB7B8'), 10.1 + i * 0.55, 18.35, 0, 10.6 + i * 0.55, 18.88, 1.9)
    g = new_group('Санвузли', 'Підсобні приміщення')
    box(g, M_PART, 13.5, 17.6, 0, 13.56, 18.94, 2.1)
    for xx in (12.8, 13.8):
        box(g, M_WHITE, xx, 18.4, 0, xx + 0.4, 18.9, 0.42)
    box(g, M_WHITE, 12.65, 16.2, 0.8, 13.2, 16.6, 0.88)
    g = new_group('Технічні приміщення: щити, агрегати, вентиляція', 'Підсобні приміщення')
    for i in range(3):
        box(g, mat('Електрощити', '#BDC3C7'), 14.8 + i * 0.7, 16.15, 0, 15.4 + i * 0.7, 16.5, 1.9)
    for i in range(2):
        box(g, M_METAL, 17.3 + i * 1.1, 16.3, 0, 18.2 + i * 1.1, 17.2, 0.9)
        cyl(g, M_DARK, (17.75 + i * 1.1, 16.75, 0.9), 0.25, 0.2, 'z', 12)
    box(g, M_METAL, 19.7, 16.3, 0, 21.3, 17.3, 1.4)
    box(g, M_METAL, 20.2, 16.6, 1.4, 20.8, 17.2, H)
    desk(g, 22.5, 16.4, 1.2, 0.6)
    # підписи приміщень (лише в Ruby)
    for name, x0, y0, x1, y1 in ROOMS:
        bm.TEXTS.append((name.upper() if len(name) < 14 else name, (x0 + x1) / 2, (y0 + y1) / 2, 0.01,
                         0, 0.22 if (x1 - x0) > 3 else 0.14, 'Відділ — Вхідна зона', 'floor'))


def build_shell():
    g = new_group('Підлога торговельної зали', 'Будівля')
    for i in range(int(L)):
        for j in range(int(D_HALL)):
            g.poly(M_FLOOR_A if (i + j) % 2 == 0 else M_FLOOR_B,
                   [(i, j, 0), (i + 1, j, 0), (i + 1, j + 1, 0), (i, j + 1, 0)])
    box(g, mat('Фундаментна плита', '#8C8478'), -WALL, -WALL, -0.3, L + WALL, D_ALL + WALL, -0.03)
    g = new_group('Зовнішні стіни (сендвіч-панелі)', 'Будівля')
    # для зручності огляду передні та бокові стіни занижено до LOW, покрівлю не показано (п. 4.1 курсової)
    box(g, M_PANEL_OUT, -WALL, 0, 0, 0, D_ALL + WALL, LOW)                # ліва
    box(g, M_PANEL_OUT, L, 0, 0, L + WALL, D_ALL + WALL, LOW)             # права
    box(g, M_PANEL_OUT, 0, D_ALL, 0, L, D_ALL + WALL, H)                  # тильна (повна висота)
    # фасад: вихід 14,9–17,08 м, вхід через тамбур 20,9–24,08 м
    g = new_group('Фасад (занижений)', 'Будівля')
    for a, b in [(-WALL, 14.9), (17.08, 20.9), (24.08, L + WALL)]:
        box(g, M_PANEL_OUT, a, -WALL, 0, b, 0, LOW)
        box(g, M_FRAME, a, -WALL, LOW, b, 0, LOW + 0.04)
    for a, b in ((14.9, 17.08), (20.9, 24.08)):
        for xx in (a, b - 0.06):
            box(g, M_FRAME, xx, -WALL, 0, xx + 0.06, 0, LOW + 0.04)
        box(g, M_GLASS, a + 0.06, -0.16, 0.02, a + 0.6, -0.14, LOW)       # розсунуті стулки
        box(g, M_GLASS, b - 0.6, -0.16, 0.02, b - 0.06, -0.14, LOW)
    # тамбур 4,0 × 3,0 м
    g = new_group('Тамбур', 'Будівля')
    for xx in (20.5, 24.42):
        box(g, M_FRAME, xx, -3.0, 0, xx + 0.08, -WALL, 0.1)
        box(g, M_GLASS, xx + 0.02, -3.0, 0.1, xx + 0.06, -WALL, LOW)
        box(g, M_FRAME, xx, -3.0, LOW, xx + 0.08, -WALL, LOW + 0.04)
    for a, b in ((20.5, 21.45), (23.5, 24.5)):
        box(g, M_GLASS, a, -3.02, 0.1, b, -2.98, LOW)
        box(g, M_FRAME, a, -3.06, LOW, b, -2.94, LOW + 0.04)
    box(g, mat('Килимок', '#3D3D3D'), 20.7, -2.8, 0, 24.3, -0.4, 0.015)
    mat('Вивіска', '#FFFFFF')
    bm.TEXTS.append(('ВХІД', 22.98, -3.08, 0.55, 0, 0.18, 'Вивіска', 'facade'))
    bm.TEXTS.append(('ВИХІД', 15.99, -WALL - 0.03, 0.55, 0, 0.16, 'Вивіска', 'facade'))


def build_route():
    """Основний маршрут покупців (рис. 3.2) — пунктирні стрілки на підлозі."""
    g = new_group('Маршрут покупців (стрілки на підлозі)', 'Навігація')
    red = mat('Маршрут покупців', '#C0392B')
    pts = [(22.6, -2.4), (22.6, 12.6), (1.65, 12.6), (1.65, 4.0), (5.6, 4.0)]
    t, z = 0.06, 0.006
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dx, dy = x1 - x0, y1 - y0
        ln = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / ln, dy / ln
        s = 0.3
        while s < ln - 0.9:
            ax, ay = x0 + ux * s, y0 + uy * s
            bx, by = x0 + ux * min(s + 0.5, ln), y0 + uy * min(s + 0.5, ln)
            box(g, red, min(ax, bx) - (t if uy else 0), min(ay, by) - (t if ux else 0), 0.001,
                max(ax, bx) + (t if uy else 0), max(ay, by) + (t if ux else 0), z, False)
            s += 0.8
        hx, hy = x1 - ux * 0.25, y1 - uy * 0.25                      # стрілка
        px, py = -uy, ux
        g.poly(red, [(x1 - ux * 0.05, y1 - uy * 0.05, z), (hx - ux * 0.35 + px * 0.25, hy - uy * 0.35 + py * 0.25, z),
                     (hx - ux * 0.35 - px * 0.25, hy - uy * 0.35 - py * 0.25, z)][::(1 if (ux * py - uy * px) > 0 else -1)])


def build_site():
    g = new_group('Благоустрій: тротуар, стоянка, велопарковка', 'Благоустрій')
    box(g, M_PAVE, -1.5, -9.0, -0.3, L + 3.0, -WALL, -0.05)               # пішохідний майданчик
    box(g, M_ASPH, -22.0, -9.0, -0.31, -1.5, D_ALL + 4.0, -0.06)           # автостоянка
    box(g, M_ASPH, -1.5, D_ALL + WALL, -0.31, L + 3.0, D_ALL + 4.0, -0.06)  # господарський проїзд
    box(g, M_GRASS, L + WALL, -WALL, -0.31, L + 3.0, D_ALL + WALL, -0.07)
    for row, y0 in enumerate((-7.5, 2.0, 11.5)):
        for i in range(8 if row else 7):
            xx = -21.0 + i * 2.5
            box(g, M_MARK, xx, y0, -0.06, xx + 0.1, y0 + 5.0, -0.055, False)
        if row:
            for i in range(8):
                box(g, M_MARK, -21.0 + i * 2.5, y0 - 4.5, -0.06, -20.9 + i * 2.5, y0 - 0.5, -0.055, False)
    for i in range(6):                                                    # велопарковка
        xx = 18.0 + i * 0.6
        for yy in (-7.0, -6.3):
            cyl(g, M_DARK, (xx, yy, -0.05), 0.022, 0.75, 'z', 6, False)
        cyl(g, M_DARK, (xx, -7.0, 0.7), 0.022, 0.7, 'y', 6, False)
    # рампа
    box(g, mat('Рампа', '#A6A39C'), -3.5, 17.2, -0.3, -WALL, 20.8, 1.0)
    # кілька автомобілів
    car_cols = ['#B71C1C', '#ECEFF1', '#263238', '#1565C0', '#9E9E9E', '#F5F5F5', '#455A64']
    spots = [(-21.0, -7.5), (-16.0, -7.5), (-11.0, -7.5), (-18.5, 2.0), (-8.5, 2.0), (-13.5, 11.5), (-6.0, 11.5)]
    for (sx, sy), c in zip(spots, car_cols):
        m = mat('Авто ' + c, c)
        x0, y0 = sx + 0.3, sy + 0.4
        box(g, m, x0, y0, 0.25, x0 + 1.8, y0 + 4.3, 0.85)
        prism_x(g, m, x0 + 0.1, x0 + 1.7, [(y0 + 1.0, 0.85), (y0 + 3.4, 0.85), (y0 + 3.0, 1.35), (y0 + 1.5, 1.35)])
        box(g, M_GLASS, x0 + 0.12, y0 + 1.5, 0.9, x0 + 1.68, y0 + 3.0, 1.3, False)
        for wy in (y0 + 0.8, y0 + 3.5):
            for wx in (x0 - 0.02, x0 + 1.62):
                cyl(g, mat('Шини', '#222222'), (wx, wy, 0.3), 0.3, 0.2, 'x', 10)


def build_hall():
    T = 'Обладнання'
    # 1. Острівні стелажі «Колумб» (5 × 5 секцій), довга сторона вздовж Y
    racks = [(2.6, 'drinks', 'alco'), (5.4, 'confect', 'confect'), (8.19, 'bakal', 'confect'),
             (11.0, 'bakal', 'bakal'), (13.79, 'other', 'other')]
    for i, (x0, right, left) in enumerate(racks):
        place(f'1.{i + 1} Острівний стелаж «Колумб» — {DEPTS[left][0]} / {DEPTS[right][0]}', T,
              x0, 16 - 10.4, 6.25, 1.2, '+x', island_rack, right, left)
    # 2. Пристінні стелажі: хліб (тильна стіна, 4) і алкоголь (ліва стіна, 4)
    for i in range(4):
        place(f'2.{i + 1} Пристінний стелаж — Хлібобулочні вироби', T, 0.62 + i * 1.25, 15.5, 1.25, 0.5, '-y', wall_rack, 'bread')
    for i in range(4):
        place(f'2.{i + 5} Пристінний стелаж — Алкогольні напої', T, 0, 16 - 10.75 + i * 1.25, 1.25, 0.5, '+x', wall_rack, 'alco')
    # 3. Холодильні гірки: риба 1, м'ясо 2, гастрономія 1 (тильна стіна), молочні 4 (права стіна)
    back = [(5.7, 'fish', ['fish', 'fish', 'fish', 'fish']), (8.3, 'meat', ['sausage', 'sausage', 'sausage', 'sausage']),
            (10.8, 'meat', ['sausage', 'sausage', 'sausage', 'sausage']), (13.4, 'gastro', ['cheese', 'sausage', 'cheese', 'boxes'])]
    n = 1
    for x0, dept, kinds in back:
        place(f'3.{n} Холодильна гірка — {DEPTS[dept][0]}', T, x0, 15.1, 2.5, 0.9, '-y', multideck, dept, kinds)
        n += 1
    dairy_k = [['cartons', 'cups', 'cartons', 'cups'], ['cups', 'cartons', 'cups', 'eggs'],
               ['cartons', 'cartons', 'cups', 'cartons'], ['eggs', 'cups', 'cartons', 'cups']]
    for j in range(4):
        place(f'3.{n} Холодильна гірка — {DEPTS["dairy"][0]}', T, 24.1, 16 - 1.31 - (j + 1) * 2.5, 2.5, 0.9, '-x',
              multideck, 'dairy', dairy_k[j])
        n += 1
    # 4. Холодильні вітрини-прилавки гастрономії (3)
    for i in range(3):
        place(f'4.{i + 1} Холодильна вітрина-прилавок — Гастрономія та сири', T, 15.58 + i * 2.5, 13.6, 2.5, 1.1, '-y',
              counter, 'gastro')
    # 5. Стелаж за прилавком
    place('5.1 Пристінний стелаж за прилавком (зона персоналу)', T, 16.0, 15.5, 6.0, 0.5, '-y', wall_shelf_staff)
    # 6. Холодильні шафи (ліва стіна, напої)
    for i in range(6):
        place(f'6.{i + 1} Холодильна шафа — Пиво, соки та безалкогольні напої', T, 0, 16 - 5.6 + i * 0.7, 0.7, 0.75,
              '+x', fridge_cabinet, 'drinks')
    # 7. Морозильні бонети (3)
    for i in range(3):
        place(f'7.{i + 1} Морозильна бонета — Заморожені продукти', T, 16.58, 16 - 10.4 + i * 2.0, 2.0, 0.9, '+x', freezer)
    # 8. Острівні гірки для фруктів та овочів (3)
    for i in range(3):
        place(f'8.{i + 1} Острівна гірка — Фрукти та овочі', T, 19.28, 16 - 10.4 + i * 2.0, 2.0, 1.2, '+x', fruit_island)
    # 9. Касові бокси Magellan (4) і 10. прикасові стелажі (4)
    for i, x0 in enumerate((5.0, 7.59, 10.19, 12.79)):
        place(f'9.{i + 1} Касовий бокс Magellan 2105-000 (К{i + 1})', T, x0, 0.75, 1.115, 2.248, '-y', checkout_box)
        place(f'10.{i + 1} Прикасовий стелаж', T, x0 + 0.26, 3.0, 0.6, 0.4, '+y', checkout_rack)
    # 11. Столи для пакування (2)
    for i, x0 in enumerate((0.99, 2.6)):
        place(f'11.{i + 1} Стіл для пакування покупок', T, x0, 0.0, 1.5, 0.6, '+y', pack_table)
    # 12. Камери схову (2) біля входу
    for i in range(2):
        place(f'12.{i + 1} Камера схову', T, 24.5, 0.0 + i * 1.0, 1.0, 0.5, '-x', locker)


def build_navigation():
    g = new_group('Підвісні покажчики відділів', 'Навігація')
    signs = [('fruit', 19.88, 9.0, 'y'), ('frozen', 17.04, 9.0, 'y'), ('other', 14.39, 9.0, 'y'), ('bakal', 11.6, 9.0, 'y'),
             ('confect', 6.0, 9.0, 'y'), ('drinks', 3.2, 9.0, 'y'), ('dairy', 22.9, 9.0, 'y'), ('meat', 10.8, 13.7, 'x'),
             ('fish', 6.95, 13.7, 'x'), ('gastro', 19.3, 12.6, 'x'), ('bread', 3.1, 14.6, 'x'), ('alco', 1.1, 7.8, 'y'),
             ('cash', 9.5, 4.4, 'x')]
    labels = {'fruit': 'ФРУКТИ ТА ОВОЧІ', 'frozen': 'ЗАМОРОЖЕНІ', 'other': 'СУПУТНІ ТОВАРИ', 'bakal': 'БАКАЛІЯ, КАВА, ЧАЙ',
              'confect': 'КОНДИТЕРСЬКІ', 'drinks': 'ПИВО, СОКИ, ВОДА', 'dairy': 'МОЛОЧНІ ВИРОБИ', 'meat': 'КОВБАСИ',
              'fish': 'РИБА', 'gastro': 'ГАСТРОНОМІЯ ТА СИРИ', 'bread': 'ХЛІБ', 'alco': 'АЛКОГОЛЬ', 'cash': 'КАСИ'}
    for dept, cx, cy, along in signs:
        width = 2.0
        sign(g, dept, cx, cy, width, along)
        if along == 'x':
            bm.TEXTS.append((labels[dept], cx, cy - 0.036, 2.84, 0, 0.13, 'Вивіска', 'y-'))
        else:
            bm.TEXTS.append((labels[dept], cx - 0.036, cy, 2.84, 0, 0.13, 'Вивіска', 'x-'))


def sign(g, dept, cx, cy, width, along, z=2.75):
    t = 0.03
    if along == 'x':
        box(g, dm(dept), cx - width / 2, cy - t, z, cx + width / 2, cy + t, z + 0.4)
        for xx in (cx - width / 2 + 0.1, cx + width / 2 - 0.1):
            cyl(g, M_METAL, (xx, cy, z + 0.4), 0.004, H - z - 0.4, 'z', 4, False)
    else:
        box(g, dm(dept), cx - t, cy - width / 2, z, cx + t, cy + width / 2, z + 0.4)
        for yy in (cy - width / 2 + 0.1, cy + width / 2 - 0.1):
            cyl(g, M_METAL, (cx, yy, z + 0.4), 0.004, H - z - 0.4, 'z', 4, False)


SCENES_RB = '''    scene(model, 'Загальний вигляд', [-8.0, -14.0, 20.0], [12.5, 11.0, 0.0])
    scene(model, 'Вигляд від входу', [22.5, -1.5, 1.65], [12.0, 12.0, 0.8])
    scene(model, 'План зверху', [12.5, 11.0, 45.0], [12.5, 11.01, 0.0])
    scene(model, 'Каси', [11.0, 6.5, 2.3], [6.0, 0.0, 0.6])
    scene(model, 'Острівні стелажі', [7.0, 4.0, 1.7], [7.0, 14.0, 0.9])
    scene(model, 'Гастрономія та молочний відділ', [16.0, 9.0, 1.8], [22.0, 15.0, 0.9])
    scene(model, 'Підсобні приміщення', [12.5, 4.0, 22.0], [12.5, 21.0, 0.0])
'''


def main():
    bm.GROUPS.clear()
    bm.TEXTS.clear()
    build_shell()
    build_hall()
    build_back_rooms()
    build_site()
    build_navigation()
    build_route()
    eq = [g for g in bm.GROUPS if g.tag == 'Обладнання']
    print(f'Груп: {len(bm.GROUPS)}, одиниць обладнання: {len(eq)}, полігонів: {sum(g.nfaces() for g in bm.GROUPS)}')
    dae = os.path.join(HERE, 'aero_express.dae')
    rb = os.path.join(HERE, 'aero_express.rb')
    bm.export_dae(dae)
    s = open(dae, encoding='utf-8').read()
    s = s.replace('build_model.py — ТОВ «Дитячий світ»', 'build_model.py — ТОВ «Аеро-Експрес»').replace('name="Дитячий світ"', 'name="Аеро-Експрес"')
    open(dae, 'w', encoding='utf-8').write(s)
    bm.export_rb(rb)
    s = open(rb, encoding='utf-8').read()
    a = s.index("    scene(model, 'Загальний вигляд'")
    b = s.index('    model.pages.selected_page')
    s = s[:a] + SCENES_RB + s[b:]
    s = (s.replace('DytiachyiSvit', 'AeroExpress').replace('магазину ТОВ «Дитячий світ» (курсова робота, розділ 4)',
                                                             'продовольчого магазину ТОВ «Аеро-Експрес» (курсова робота, розділ 4)')
         .replace('dytiachyi_svit.rb', 'aero_express.rb').replace('Дитячий світ', 'Аеро-Експрес'))
    s = s.replace("    when 'x+' then", "    when 'floor' then r = Geom::Transformation.translation([0, -h * M / 2.0, 0])\n    when 'x+' then")
    open(rb, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    main()
