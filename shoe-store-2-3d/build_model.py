#!/usr/bin/env python3
"""Генератор 3D-моделі торговельної зали магазину взуття ТОВ «Взуття» (курсова, варіант із залою 20 × 14 м).

За курсовою роботою: прямокутна зала 20,0 × 14,0 м, висота 3,0 м, дверний проріз 2,0 м посередині фасаду;
зони — жіночий відділ 104 м² (ліворуч), чоловічий 97 м² (праворуч), дитячий 55 м² (у центрі біля задньої
стіни), вхідна і касова зона 24 м²; обладнання — табл. 2.2–2.3 (108 од.), розміщення — рис. 2.2.

Координати: X — уздовж фасаду (0 — ліва стіна), Y — углиб (0 — фасадна стіна), Z — вгору, метри.
Взуття, примітиви й експорт беруться з ../shoe-store-3d/build_model.py та ../toy-store-3d/build_model.py.
"""
import importlib.util
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('shoe_model', os.path.join(HERE, '..', 'shoe-store-3d', 'build_model.py'))
sh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sh)
bm = sh.bm
box, cyl, prism_x, mat, new_group = bm.box, bm.cyl, bm.prism_x, bm.mat, bm.new_group

random.seed(2014)
L, D, H = 20.0, 14.0, 3.0
WALL = 0.2
DOOR = (9.25, 11.25)                    # дверний проріз 2,0 м
SERVICE_DOOR = (12.86, 13.58)           # службові двері до складу в задній стіні
bm.H = H

# зони підлоги (рис. 2.2)
ZONES = {
    'women': ('Жіночий відділ', (0.0, 0.0, 7.43, D), '#F6E1E8'),
    'kids': ('Дитячий відділ', (7.43, 4.24, 13.07, D), '#FBF0D4'),
    'entry': ('Вхідна і касова зона', (7.43, 0.0, 13.07, 4.24), '#ECECEC'),
    'men': ('Чоловічий відділ', (13.07, 0.0, L, D), '#E1E9F4'),
}
DEPT = {'women': 'Жіночий відділ', 'men': 'Чоловічий відділ', 'kids': 'Дитячий відділ', 'cash': 'Вхідна і касова зона'}
DCOL = {'women': '#D9779A', 'men': '#5B87C2', 'kids': '#E3B437', 'cash': '#B04545'}
for k, c in DCOL.items():
    mat('Відділ — ' + DEPT[k], c)

M_RACK = mat('Каркас стелажа (графіт)', '#4A4F57')
M_SHELF = mat('Полиці стелажа', '#F4F4F2')
M_BACK = mat('Задня панель стелажа', '#E9E7E2')
M_SEAT = mat('Оббивка банкеток', '#6E9C55')
M_MDF = mat('Основа банкеток (МДФ)', '#C9B28F')
M_LDSP = mat('Касовий прилавок (ЛДСП)', '#B04545')
M_TOP = mat('Стільниця', '#EDEBE6')
M_WALL = mat('Стіни', '#F2EFEA')
M_WALL_OUT = mat('Фасад', '#B9AE9E')
M_GLASS = mat('Скло', '#A8D8EA', 0.3)
M_FRAME = mat('Алюмінієвий профіль', '#5F6A72')
M_DOOR = mat('Службові двері', '#9AA4AD')
M_PAVE = mat('Тротуарна плитка', '#BDB8AE')
M_SCREEN, M_DARK, M_SHOEBOX = sh.M_SCREEN, sh.M_DARK, sh.M_SHOEBOX
for k, (n, _r, c) in ZONES.items():
    mat('Підлога — ' + n, c)
    mat('Підлога — ' + n + ' (темніша)', bm.shade(c, 0.94))


def dm(dept):
    return 'Відділ — ' + DEPT[dept]


# ---------------------------------------------------------------- обладнання (табл. 2.2)
def wall_rack(g, dept):
    """Пристінний стелаж 1,00 × 0,40 × 1,93 м з регульованими похилими полицями (фронт — y=0)."""
    w, d, h = 1.0, 0.4, 1.93
    box(g, M_RACK, 0.0, 0.03, 0, w, d, 0.1)
    box(g, M_BACK, 0.02, d - 0.025, 0.1, w - 0.02, d, h)
    for xx in (0.0, w - 0.025):
        box(g, M_RACK, xx, d - 0.05, 0, xx + 0.025, d, h)
    levels = [0.1, 0.45, 0.8, 1.15, 1.5]
    for i, z0 in enumerate(levels):
        y0 = 0.04 + 0.03 * i
        if i:
            box(g, M_SHELF, 0.025, y0, z0 - 0.02, w - 0.025, d - 0.025, z0)
            box(g, dm(dept), 0.025, y0 - 0.01, z0 - 0.045, w - 0.025, y0, z0, False)    # цінникова планка
        if i == 4:
            xx = 0.04
            while xx < w - 0.3:
                box(g, M_SHOEBOX, xx, y0 + 0.02, z0, xx + 0.29, y0 + 0.2, z0 + 0.12)
                box(g, M_SHOEBOX, xx, y0 + 0.02, z0 + 0.12, xx + 0.29, y0 + 0.2, z0 + 0.24)
                xx += 0.32
        else:
            sh.shoes_row(g, dept, 0.02, w - 0.02, y0 + 0.02, z0, d - y0 - 0.05)
    box(g, M_RACK, 0, 0.03, h - 0.02, w, d, h)
    box(g, dm(dept), 0, d - 0.1, h + 0.05, w, d - 0.03, h + 0.3)                     # навігаційний фриз


def island_rack(g, dept):
    """Острівний двосторонній стелаж: секція 1,00 м уздовж ряду, глибина 1,25 м, висота 1,47 м (фронти — y=0 і y=d)."""
    w, d, h = 1.0, 1.25, 1.47
    box(g, M_RACK, 0.0, 0.08, 0, w, d - 0.08, 0.1)
    box(g, M_BACK, 0.0, d / 2 - 0.02, 0.1, w, d / 2 + 0.02, h)
    for xx in (0.0, w - 0.025):
        box(g, M_RACK, xx, d / 2 - 0.04, 0, xx + 0.025, d / 2 + 0.04, h)
    for side in (0, 1):
        old = g.xf
        g.xf = (bm.Xf(w, d, 0, 180) if side else bm.Xf()).then(old)
        for i, (y0, z0) in enumerate(((0.06, 0.1), (0.17, 0.48), (0.28, 0.86))):
            if i:
                box(g, M_SHELF, 0.0, y0, z0 - 0.02, w, d / 2 - 0.02, z0)
            box(g, dm(dept), 0.0, y0 - 0.008, z0 - 0.04, w, y0, z0, False)
            sh.shoes_row(g, dept, 0.0, w, y0 + 0.02, z0, d / 2 - y0 - 0.05)
        g.xf = old
    box(g, M_SHELF, 0.0, d / 2 - 0.16, h - 0.02, w, d / 2 + 0.16, h)
    sh.shoes_row(g, dept, 0.05, w - 0.05, d / 2 - 0.14, h, 0.27, pairs=False)


def banquette(g, dept):
    """Банкетка для примірювання 1,00 × 0,35 × 0,45 м: м'яке сидіння на основі з МДФ."""
    w, d = 1.0, 0.35
    box(g, M_MDF, 0.03, 0.03, 0, w - 0.03, d - 0.03, 0.3)
    box(g, M_SEAT, 0, 0, 0.3, w, d, 0.45)
    box(g, sh.mat('Ріжок для взуття', '#B03A2E'), 0.06, 0.12, 0.45, 0.09, 0.26, 0.46)


def cash_counter(g, n):
    """Модульний касовий прилавок 1,00 × 0,60 × 0,90 м, ЛДСП (покупець — y=0)."""
    w, d, h = 1.0, 0.6, 0.9
    box(g, M_LDSP, 0, 0, 0, w, 0.04, h - 0.03)
    for xx in (0, w - 0.03):
        box(g, M_LDSP, xx, 0.04, 0, xx + 0.03, d, h - 0.03)
    box(g, M_TOP, -0.02, -0.02, h - 0.03, w + 0.02, d + 0.02, h)
    box(g, M_TOP, 0.03, 0.1, 0.65, w - 0.03, d - 0.02, 0.68)                           # полиця касира
    box(g, M_DARK, 0.4, 0.38, h, 0.48, 0.46, h + 0.18)                                  # монітор
    box(g, M_DARK, 0.2, 0.42, h + 0.18, 0.68, 0.45, h + 0.48)
    box(g, M_SCREEN, 0.22, 0.415, h + 0.2, 0.66, 0.42, h + 0.46, False)
    box(g, M_DARK, 0.75, 0.12, h, 0.84, 0.22, h + 0.05)                                 # POS-термінал
    box(g, M_DARK, 0.2, 0.3, 0.68, 0.6, 0.55, 0.78)                                     # грошова скринька
    box(g, mat('Пакети', '#F5F5F5'), 0.03, 0.1, 0.68, 0.18, 0.5, 0.85)
    for k in range(3):                                                                  # шкарпетки біля каси
        box(g, sh.cm(random.choice(['#222222', '#E6C3A5', '#7B1E3A', '#1F3A5F'])), 0.05 + k * 0.1, 0.0, h, 0.13 + k * 0.1, 0.08, h + 0.12)


# ---------------------------------------------------------------- компоненти
DEF_TITLES = {
    'wall_rack': 'Пристінний стелаж 1000×400×1930', 'island_rack': 'Острівний двосторонній стелаж 1250×1000×1470',
    'banquette': 'Банкетка для примірювання 1000×350×450', 'cash_counter': 'Касовий прилавок 1000×600×900',
}
DEFS, INSTANCES = {}, []


def place(name, tag, x0, y0, w, d, facing, builder, *args):
    rot = {'-y': 0, '+x': 90, '+y': 180, '-x': 270}[facing]
    key = (builder.__name__,) + args
    if key not in DEFS:
        title = DEF_TITLES[builder.__name__] + (f' — {DEPT[args[0]]}' if args and args[0] in DEPT else '')
        local = bm.Group(title, tag)
        builder(local, *args)
        DEFS[key] = local
    r = bm.Xf(0, 0, 0, rot)
    cs = [r((0, 0, 0)), r((w, 0, 0)), r((0, d, 0)), r((w, d, 0))]
    tx, ty = x0 - min(c[0] for c in cs), y0 - min(c[1] for c in cs)
    xf = bm.Xf(0, 0, 0, rot).then(bm.Xf(tx, ty, 0))
    g = new_group(name, tag)
    for k, polys in DEFS[key].parts.items():
        g.parts[k] = [([xf(p) for p in pts], [r(n) for n in ns] if ns else None) for pts, ns in polys]
    g.instance = True
    INSTANCES.append((key, name, tag, tx, ty, rot))
    return g


# ---------------------------------------------------------------- будівля
def build_shell():
    for k, (name, (x0, y0, x1, y1), _c) in ZONES.items():
        g = new_group('Підлога — ' + name, 'Підлога')
        import math
        for i in range(int(math.floor(x0)), int(math.ceil(x1))):
            for j in range(int(math.floor(y0)), int(math.ceil(y1))):
                a, b, c, e = max(x0, i), min(x1, i + 1), max(y0, j), min(y1, j + 1)
                if b - a > 1e-6 and e - c > 1e-6:
                    m = 'Підлога — ' + name + (' (темніша)' if (i + j) % 2 else '')
                    g.poly(m, [(a, c, 0), (b, c, 0), (b, e, 0), (a, e, 0)])
        # межа зони — тонка смуга
        line = mat('Межа відділів', '#9A9A9A')
        for (a, b, c, e) in ((x0, y0, x1, y0 + 0.02), (x0, y1 - 0.02, x1, y1), (x0, y0, x0 + 0.02, y1), (x1 - 0.02, y0, x1, y1)):
            box(g, line, a, b, 0.0005, c, e, 0.002, False)
    g = new_group('Плита основи', 'Підлога')
    box(g, mat('Плита перекриття', '#8C8478'), -WALL, -WALL, -0.25, L + WALL, D + WALL, -0.01)
    box(g, mat('Килимок', '#3D3D3D'), DOOR[0] + 0.1, 0.05, 0, DOOR[1] - 0.1, 1.4, 0.012, False)
    g = new_group('Стіни', 'Стіни')
    box(g, M_WALL, -WALL, 0, 0, 0, D + WALL, H)
    box(g, M_WALL, L, 0, 0, L + WALL, D + WALL, H)
    box(g, M_WALL, 0, D, 0, SERVICE_DOOR[0], D + WALL, H)
    box(g, M_WALL, SERVICE_DOOR[1], D, 0, L, D + WALL, H)
    box(g, M_WALL, SERVICE_DOOR[0], D, 2.1, SERVICE_DOOR[1], D + WALL, H)
    box(g, M_DOOR, SERVICE_DOOR[0] + 0.03, D + 0.06, 0, SERVICE_DOOR[1] - 0.03, D + 0.1, 2.08)
    box(g, M_DARK, SERVICE_DOOR[0] + 0.08, D + 0.03, 1.0, SERVICE_DOOR[0] + 0.12, D + 0.06, 1.1)
    bm.TEXTS.append(('СКЛАД', (SERVICE_DOOR[0] + SERVICE_DOOR[1]) / 2, D - 0.005, 2.15, 0, 0.12, 'Вивіска', 'y-'))
    g = new_group('Фасадна стіна з дверним прорізом 2,0 м і вітринами', 'Стіни')
    for a, b in ((-WALL, 0.4), (DOOR[1], DOOR[1] + 0.4), (DOOR[0] - 0.4, DOOR[0]), (L - 0.4, L + WALL)):
        box(g, M_WALL_OUT, a, -WALL, 0, b, 0, H)
    for a, b in ((0.4, DOOR[0] - 0.4), (DOOR[1] + 0.4, L - 0.4)):
        box(g, M_WALL_OUT, a, -WALL, 0, b, 0, 0.5)
        box(g, M_WALL_OUT, a, -WALL, 2.6, b, 0, H)
        n = max(1, round((b - a) / 1.7))
        for i in range(n + 1):
            xx = a + (b - a) * i / n
            box(g, M_FRAME, xx - 0.04, -WALL, 0.5, xx + 0.04, -0.05, 2.6)
        for i in range(n):
            box(g, M_GLASS, a + (b - a) * i / n + 0.04, -0.13, 0.5, a + (b - a) * (i + 1) / n - 0.04, -0.11, 2.6)
    box(g, M_WALL_OUT, DOOR[0], -WALL, 2.4, DOOR[1], 0, H)
    box(g, M_FRAME, DOOR[0], -WALL, 2.33, DOOR[1], 0, 2.4)
    box(g, M_GLASS, DOOR[0] + 0.05, -0.17, 0.02, DOOR[0] + 0.5, -0.15, 2.33)
    box(g, M_GLASS, DOOR[1] - 0.5, -0.17, 0.02, DOOR[1] - 0.05, -0.15, 2.33)
    g = new_group('Вивіска «Взуття»', 'Навігація')
    box(g, mat('Вивіска фон', '#7B1E3A'), 6.0, -WALL - 0.12, 2.62, 14.5, -WALL, 2.95)
    mat('Вивіска', '#FFFFFF')
    bm.TEXTS.append(('ВЗУТТЯ', 10.25, -WALL - 0.125, 2.68, 0, 0.22, 'Вивіска', 'facade'))
    g = new_group('Тротуар', 'Благоустрій')
    box(g, M_PAVE, -1.0, -4.0, -0.25, L + 1.0, -WALL, -0.03)


def build_equipment():
    TAG = {'women': 'Жіночий відділ', 'men': 'Чоловічий відділ', 'kids': 'Дитячий відділ', 'cash': 'Вхідна і касова зона'}
    n = [0]

    def wall(x0, y0, facing, dept):
        n[0] += 1
        place(f'1.{n[0]} Пристінний стелаж — {DEPT[dept]}', TAG[dept], x0, y0, 1.0, 0.4, facing, wall_rack, dept)

    for i in range(7):
        wall(0.405 + i * 1.0, D - 0.4, '-y', 'women')               # задня стіна, жіночий
    for j in range(12):
        wall(0.0, 1.0 + j * 1.0, '+x', 'women')                      # ліва стіна
    for i in range(5):
        wall(7.83 + i * 1.0, D - 0.4, '-y', 'kids')                   # задня стіна, дитячий
    for j in range(5):
        wall(7.43, 7.6 + j * 1.0, '+x', 'kids')                       # перегородка дитячого відділу
    for i in range(6):
        wall(13.6 + i * 1.0, D - 0.4, '-y', 'men')                    # задня стіна, чоловічий
    for j in range(12):
        wall(L - 0.4, 1.0 + j * 1.0, '-x', 'men')                     # права стіна
    k = [0]

    def island(x0, y0, dept):
        k[0] += 1
        place(f'2.{k[0]} Острівний двосторонній стелаж — {DEPT[dept]}', TAG[dept], x0, y0, 1.0, 1.25, '+x', island_rack, dept)

    for x0 in (1.81, 4.46):
        for y0 in (7.09, 8.09, 9.09, 10.09, 1.49, 2.49, 3.49, 4.49):
            island(x0, y0, 'women')
    for y0 in (7.09, 8.09, 9.09, 10.09, 1.49, 2.49, 3.49, 4.49):
        island(14.3, y0, 'men')
    for y0 in (7.09, 8.09, 9.09, 1.49, 2.49, 3.49, 4.49):
        island(16.95, y0, 'men')
    for x0 in (8.96, 10.21):
        for y0 in (5.4, 6.4, 7.4, 8.4):
            island(x0, y0, 'kids')
    b = [0]

    def bench(x0, y0, along, dept):
        b[0] += 1
        place(f'3.{b[0]} Банкетка для примірювання — {DEPT[dept]}', TAG[dept], x0, y0, 1.0, 0.35,
              '-y' if along == 'x' else '+x', banquette, dept)

    for x0 in (1.71, 2.90, 4.36, 5.55):
        bench(x0, 12.29, 'x', 'women')
    for y0 in (10.0, 8.0, 4.2, 2.2):
        bench(6.55, y0, 'y', 'women')
    bench(8.6, 12.39, 'x', 'kids')
    for x0 in (8.6, 9.8, 11.0):
        bench(x0, 11.6, 'x', 'kids')
    for x0 in (14.2, 15.4, 16.85, 18.05):
        bench(x0, 12.29, 'x', 'men')
    for y0 in (8.0, 4.2, 2.2):
        bench(13.25, y0, 'y', 'men')
    for i, y0 in enumerate((3.09, 2.0, 0.9)):
        place(f'4.{i + 1} Касовий прилавок {i + 1}', TAG['cash'], 11.9, y0, 1.0, 0.6, '+y', cash_counter, 1)


def build_navigation():
    g = new_group('Підвісні покажчики відділів', 'Навігація')
    for dept, cx, cy, txt in (('women', 3.7, 6.3, 'ЖІНОЧЕ ВЗУТТЯ'), ('men', 16.5, 6.3, 'ЧОЛОВІЧЕ ВЗУТТЯ'),
                              ('kids', 10.25, 10.6, 'ДИТЯЧЕ ВЗУТТЯ'), ('cash', 12.4, 4.0, 'КАСИ')):
        width = 2.4 if dept != 'cash' else 1.4
        box(g, dm(dept), cx - width / 2, cy - 0.03, 2.35, cx + width / 2, cy + 0.03, 2.7)
        for xx in (cx - width / 2 + 0.1, cx + width / 2 - 0.1):
            cyl(g, sh.M_METAL, (xx, cy, 2.7), 0.004, H - 2.7, 'z', 4, False)
        bm.TEXTS.append((txt, cx, cy - 0.035, 2.43, 0, 0.14, 'Вивіска', 'y-'))


SCENES_RB = '''    scene(model, 'Загальний вигляд', [-5.0, -11.0, 15.0], [10.0, 7.5, 0.0])
    scene(model, 'Вигляд від входу', [10.25, 0.4, 1.65], [10.25, 12.0, 0.9])
    scene(model, 'План зверху', [10.0, 7.0, 30.0], [10.0, 7.0, 0.0], false, 15.5)
    scene(model, 'Жіночий відділ', [6.9, 6.3, 1.8], [0.5, 12.5, 0.8])
    scene(model, 'Чоловічий відділ', [13.3, 6.3, 1.8], [19.5, 12.5, 0.8])
    scene(model, 'Дитячий відділ', [10.25, 3.0, 2.2], [10.25, 13.0, 0.6])
'''

SHEET = dict(sh.SHEET)
SHEET.update({
    'SHEET_TITLE': 'ПРОЄКТ ТОРГОВЕЛЬНОЇ ЗАЛИ МАГАЗИНУ ВЗУТТЯ ТА АКСЕСУАРІВ ТОВ «ВЗУТТЯ»',
    'SHEET_SUBTITLE': 'Тривимірна модель торговельної зали у SketchUp (п. 2.3, рис. 2.3, Б.1). Зала 20,0 × 14,0 м, площа 280 м², висота 3,0 м',
    'SHEET_VIEWS': [
        ['План зверху', 30, 34, 245, 205, 'План торговельної зали з розміщенням обладнання, М 1:100', 0.01],
        ['Загальний вигляд', 290, 34, 300, 205, 'Загальний вигляд моделі (рис. 2.3)', None],
        ['Вигляд від входу', 605, 34, 221, 205, 'Вигляд торговельної зали від входу (рис. Б.1)', None],
        ['Жіночий відділ', 30, 255, 260, 180, 'Жіночий відділ', None],
        ['Чоловічий відділ', 300, 255, 260, 180, 'Чоловічий відділ', None],
        ['Дитячий відділ', 570, 255, 256, 180, 'Дитячий відділ і касова зона', None],
    ],
    'SHEET_EQUIP': [[1, 'Пристінний стелаж (Modern Expo)', '1000×400×1930', 47], [2, 'Острівний двосторонній стелаж (Modern Expo)', '1250×1000×1470', 39],
                    [3, 'Банкетка для примірювання', '1000×350×450', 19], [4, 'Касовий прилавок модульний', '1000×600×900', 3],
                    ['', 'Разом', '', 108]],
    'SHEET_LEGEND': [['Жіночий відділ, 104 м²', '#F6E1E8'], ['Чоловічий відділ, 97 м²', '#E1E9F4'],
                     ['Дитячий відділ, 55 м²', '#FBF0D4'], ['Вхідна і касова зона, 24 м²', '#ECECEC']],
    'SHEET_STAMP': [['Курсова робота з дисципліни «Проєктування торговельних об’єктів»', 9, False],
                    ['Магазин взуття та аксесуарів ТОВ «Взуття». Тривимірна модель зали', 9, True],
                    ['Розробив(ла): ______________________   Перевірив(ла): ______________________', 9, False],
                    ['ДТЕУ, кафедра торговельного підприємництва та логістики', 9, False],
                    ['Аркуш А1 (841 × 594)        Масштаб плану 1:100        Київ 2026', 9, False]],
})


def main():
    bm.GROUPS.clear()
    bm.TEXTS.clear()
    DEFS.clear()
    INSTANCES.clear()
    build_shell()
    build_equipment()
    build_navigation()
    eq = [g for g in bm.GROUPS if getattr(g, 'instance', False)]
    print(f'Груп: {len(bm.GROUPS)}, одиниць обладнання: {len(eq)}, визначень компонентів: {len(DEFS)}, '
          f'полігонів: {sum(g.nfaces() for g in bm.GROUPS)}')
    dae = os.path.join(HERE, 'vzuttia_zal.dae')
    rb = os.path.join(HERE, 'vzuttia_zal.rb')
    bm.export_dae(dae)
    s = open(dae, encoding='utf-8').read()
    s = s.replace('build_model.py — ТОВ «Дитячий світ»', 'build_model.py — ТОВ «Взуття»').replace('name="Дитячий світ"', 'name="Взуття"')
    open(dae, 'w', encoding='utf-8').write(s)
    all_groups = list(bm.GROUPS)
    bm.GROUPS[:] = [g for g in all_groups if not getattr(g, 'instance', False)] + list(DEFS.values())
    bm.export_rb(rb)
    bm.GROUPS[:] = all_groups
    s = open(rb, encoding='utf-8').read()
    for g in DEFS.values():
        a = s.index(f"    grp(model, {bm.rb_str(g.name)}, ")
        b = s.index('    ])\n', a) + len('    ])\n')
        s = s[:a] + s[b:]
    comps = ['    # обладнання: визначення компонентів і їхні копії\n', '    defs = {}\n']
    keys = list(DEFS)
    for i, (key, g) in enumerate(DEFS.items()):
        comps.append(f'    defs[{i}] = defn(model, {bm.rb_str(g.name)}, [\n{sh.rb_parts(g)}    ])\n')
    for key, name, tag, tx, ty, rot in INSTANCES:
        comps.append(f'    inst(model, defs[{keys.index(key)}], {bm.rb_str(name)}, {bm.rb_str(tag)}, {tx:.4f}, {ty:.4f}, {rot})\n')
    a = s.index("    scene(model, 'Загальний вигляд'")
    b = s.index('    model.pages.selected_page')
    s = s[:a] + ''.join(comps) + SCENES_RB + s[b:]
    consts = ''.join(f'  {k} = {sh.rb_val(v)}.freeze\n' for k, v in SHEET.items())
    s = s.replace('  def self.build\n', consts + sh.RB_HELPERS + '\n  def self.build\n', 1)
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
                  """      model.options['UnitsOptions']['LengthUnit'] = 2       # міліметри
      model.options['UnitsOptions']['LengthPrecision'] = 0""")
    s = s.replace("""    model.commit_operation
""", """    model.commit_operation
    dir = File.dirname(__FILE__)
    skp = File.join(dir, 'vzuttia_zal.skp')
    model.save(skp)
    puts "Збережено: #{skp}"
    begin
      make_layout(skp, File.join(dir, 'vzuttia_zal_A1.layout'), File.join(dir, 'vzuttia_zal_A1.pdf'))
    rescue StandardError, LoadError => e
      puts "Аркуш LayOut не створено: #{e.message}"
    end
""", 1)
    s = (s.replace('DytiachyiSvit', 'VzuttiaZal').replace('магазину ТОВ «Дитячий світ» (курсова робота, розділ 4)',
                                                          'торговельної зали магазину взуття ТОВ «Взуття» 20 × 14 м (курсова робота, п. 2.3)')
         .replace('dytiachyi_svit.rb', 'vzuttia_zal.rb').replace('Дитячий світ', 'Взуття'))
    s = s.replace("# Згенеровано build_model.py; одиниці — метри.",
                  "# Згенеровано build_model.py. Після побудови скрипт зберігає поруч vzuttia_zal.skp,\n"
                  "# створює аркуш А1 vzuttia_zal_A1.layout у LayOut і експортує його у vzuttia_zal_A1.pdf.")
    open(rb, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    main()
