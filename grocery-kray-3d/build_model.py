#!/usr/bin/env python3
"""Генератор 3D-моделі торговельної зали продовольчого магазину ТОВ «Край» для SketchUp.

За курсовою роботою: зала 28,0 × 20,0 м (560 м²), висота 3,2 м; вхід праворуч і вихід через касовий вузол
у фасадній стіні; 13 відділів і вхідна зона з різним кольором підлоги (табл. 2.1, рис. 2.2);
обладнання — табл. 2.2–2.3 (160 од.). Координати обладнання розпізнано з рис. 2.2 (layout_fig2_2.json).

Координати: X — уздовж фасаду (0 — ліва стіна), Y — углиб (0 — фасадна стіна), Z — вгору, метри.
Товари й примітиви — з ../food-store-3d/build_model.py та ../toy-store-3d/build_model.py.
"""
import importlib.util
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, '..', rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fm = _load('food_model', 'food-store-3d/build_model.py')
sh = _load('shoe_model', 'shoe-store-3d/build_model.py')
bm = fm.bm
box, cyl, sphere, prism_x, prism_y, mat, new_group = bm.box, bm.cyl, bm.sphere, bm.prism_x, bm.prism_y, bm.mat, bm.new_group
food = fm.food

random.seed(560)
L, D, H = 28.0, 20.0, 3.2
WALL = 0.2
ENTRY, EXIT = (23.1, 25.3), (16.5, 18.5)
SERVICE_DOORS = [(7.1, 8.05), (16.6, 17.55), (24.25, 25.15)]
bm.H = H

ZONES = {   # № : назва, прямокутник (x0, y0, x1, y1), колір підлоги (рис. 2.2)
    1: ('Овочі та фрукти', (25.2, 2.52, 28, 5.71), '#E2ECE9'),
    2: ('Хлібний', (25.2, 5.71, 28, 13.21), '#FFF1E6'),
    3: ('Кондитерський', (25.2, 13.21, 28, 20), '#DFE7FD'),
    4: ('Рибний', (21.72, 13.38, 25.2, 20), '#FBF8CC'),
    5: ('Заморожені продукти', (21.72, 11.66, 25.2, 13.38), '#CFE1F2'),
    6: ('М’ясо-ковбасний', (7.93, 11.66, 21.72, 20), '#E9F5DB'),
    7: ('Молочно-жировий', (3.02, 11.66, 7.93, 20), '#F0EFEB'),
    8: ('Алкогольні та безалкогольні напої', (0, 2.52, 3.02, 20), '#FDE2E4'),
    9: ('Бакалійний', (18.4, 2.52, 25.2, 11.66), '#ECE4DB'),
    10: ('Зоотовари', (15.25, 2.52, 18.4, 11.66), '#D8E2DC'),
    11: ('Господарські товари', (9.8, 2.52, 15.25, 11.66), '#FAE1DD'),
    12: ('Гігієна та догляд', (4.99, 2.52, 9.8, 11.66), '#E8E8E4'),
    13: ('Канцтовари та подарунки', (3.02, 2.52, 4.99, 11.66), '#F1E3F3'),
    14: ('Вхідна і касова зона', (0, 0, 28, 2.52), '#EEEEEE'),
}
ACCENT = {1: '#5E9E4A', 2: '#B9874A', 3: '#7E8FD8', 4: '#C9B83A', 5: '#5B9BD5', 6: '#C0392B', 7: '#8E8E7A',
          8: '#C2185B', 9: '#9C7A54', 10: '#5F8A72', 11: '#D9776A', 12: '#7A7A72', 13: '#9C6FB0', 14: '#9AA3AD'}
for z, (n, _r, c) in ZONES.items():
    mat('Підлога — ' + n, c)
    mat('Підлога — ' + n + ' (темніша)', bm.shade(c, 0.95))
    mat('Відділ — ' + n, ACCENT[z])

M_RACK = mat('Каркас стелажа Modern Expo (RAL 7035)', '#D7DADC')
M_UP = mat('Стійки стелажа (графіт)', '#4A4F57')
M_SHELF = mat('Полиці стелажа', '#F4F4F2')
M_COLD = mat('Холодильне обладнання (корпус)', '#ECEFF1')
M_WALL = mat('Стіни', '#F2EFEA')
M_WALL_OUT = mat('Фасад', '#B9AE9E')
M_GLASS, M_FRAME, M_METAL, M_DARK, M_LIGHT = fm.M_GLASS, fm.M_FRAME, fm.M_METAL, fm.M_DARK, fm.M_LIGHT
M_WOOD, M_CRATE, M_SCREEN, M_BELT, M_WHITE = fm.M_WOOD, fm.M_CRATE, fm.M_SCREEN, fm.M_BELT, fm.M_WHITE
M_CASH = mat('Касовий бокс Modern Expo', '#B04848')
M_DOOR = mat('Службові двері', '#9AA4AD')


def zone_of(x, y):
    for z, (_n, (a, b, c, d), _c) in ZONES.items():
        if a <= x < c and b <= y < d:
            return z
    return 14


def dm(z):
    return 'Відділ — ' + ZONES[z][0]


KINDS = {   # види товарів на рівнях полиць (з генератора «Аеро-Експрес»)
    2: ['bread'], 3: ['boxes'], 8: ['wine', 'vodka', 'beer', 'cartons_juice'], 9: ['bags', 'jars', 'boxes'],
    10: ['bags', 'jars', 'boxes'], 11: ['boxes', 'jars'], 12: ['jars', 'boxes'], 13: ['boxes'],
}


def goods(g, z, level, x0, x1, y0, y1, zz, hmax):
    kinds = KINDS.get(z, ['boxes'])
    k = kinds[level % len(kinds)]
    if k == 'cartons_juice':
        return food(g, 'cartons', x0, x1, y0, y1, zz, hmax, 'juice')
    return food(g, k, x0, x1, y0, y1, zz, hmax, ACCENT[z])


# ---------------------------------------------------------------- обладнання (табл. 2.2)
def wall_rack(g, z):
    """Пристінний стелаж 1,00 × 0,50 × 2,00 м (фронт — y=0)."""
    w, d, h = 1.0, 0.5, 2.0
    box(g, M_RACK, 0, 0.05, 0, w, d, 0.1)
    box(g, M_RACK, 0.02, d - 0.03, 0.1, w - 0.02, d, h)
    for xx in (0, w - 0.03):
        box(g, M_UP, xx, d - 0.05, 0, xx + 0.03, d, h)
    levels = [0.1, 0.45, 0.8, 1.15, 1.5, 1.82]
    for i, z0 in enumerate(levels):
        if i:
            box(g, M_SHELF, 0.02, 0.02, z0 - 0.02, w - 0.02, d - 0.03, z0)
            box(g, dm(z), 0.02, 0.0, z0 - 0.045, w - 0.02, 0.02, z0, False)
        top = levels[i + 1] if i + 1 < len(levels) else h + 0.12
        goods(g, z, i, 0.04, w - 0.04, 0.02, d - 0.05, z0, top - z0 - 0.03)
    box(g, dm(z), 0, d - 0.12, h + 0.05, w, d - 0.04, h + 0.28)


def bread_rack(g, z):
    """Стелаж для хліба 1,00 × 0,50 × 1,90 м з похилими полицями і кошиками."""
    w, d, h = 1.0, 0.5, 1.9
    box(g, M_WOOD, 0, 0.05, 0, w, d, 0.15)
    box(g, M_WOOD, 0.02, d - 0.03, 0.15, w - 0.02, d, h)
    for xx in (0, w - 0.03):
        box(g, M_WOOD, xx, 0.0, 0, xx + 0.03, d, h)
    for i, z0 in enumerate([0.15, 0.55, 0.95, 1.35]):
        prism_x(g, M_SHELF, 0.03, w - 0.03, [(0.02, z0), (d - 0.03, z0 + 0.08), (d - 0.03, z0 + 0.1), (0.02, z0 + 0.02)])
        box(g, dm(z), 0.03, 0.0, z0 - 0.02, w - 0.03, 0.02, z0 + 0.06, False)
        food(g, 'bread', 0.05, w - 0.05, 0.04, d - 0.05, z0 + 0.04, 0.3, ACCENT[z])
    box(g, dm(z), 0, d - 0.12, h + 0.05, w, d - 0.04, h + 0.28)


def island_rack(g, z):
    """Острівний двосторонній стелаж: секція 1,00 м, глибина 0,90 м, висота 1,60 м (фронти — y=0 і y=d)."""
    w, d, h = 1.0, 0.9, 1.6
    box(g, M_RACK, 0, 0.06, 0, w, d - 0.06, 0.1)
    box(g, M_RACK, 0, d / 2 - 0.02, 0.1, w, d / 2 + 0.02, h)
    for xx in (0, w - 0.03):
        box(g, M_UP, xx, d / 2 - 0.04, 0, xx + 0.03, d / 2 + 0.04, h)
    levels = [0.1, 0.48, 0.86, 1.24]
    for side in (0, 1):
        old = g.xf
        g.xf = (bm.Xf(w, d, 0, 180) if side else bm.Xf()).then(old)
        for i, z0 in enumerate(levels):
            if i:
                box(g, M_SHELF, 0.0, 0.03, z0 - 0.02, w, d / 2 - 0.02, z0)
                box(g, dm(z), 0.0, 0.01, z0 - 0.045, w, 0.03, z0, False)
            top = levels[i + 1] if i + 1 < len(levels) else h + 0.15
            if z == 2:
                food(g, 'bread', 0.04, w - 0.04, 0.04, d / 2 - 0.04, z0, top - z0 - 0.03, ACCENT[z])
            else:
                goods(g, z, i, 0.04, w - 0.04, 0.04, d / 2 - 0.04, z0, top - z0 - 0.03)
        g.xf = old
    box(g, M_SHELF, 0, d / 2 - 0.1, h - 0.02, w, d / 2 + 0.1, h)


def vitrine(g, z):
    """Холодильна вітрина обслуговування 1,88 × 1,10 × 1,25 м (покупець — y=0, продавець — y=d)."""
    w, d = 1.88, 1.1
    box(g, M_COLD, 0, 0.1, 0, w, d, 0.85)
    box(g, dm(z), 0, 0.095, 0.15, w, 0.1, 0.6, False)
    box(g, M_WOOD, 0, 0.0, 0.85, w, 0.12, 0.9)
    box(g, M_METAL, 0.03, 0.15, 0.85, w - 0.03, d - 0.25, 0.88)
    box(g, M_WHITE, 0, d - 0.25, 0.85, w, d, 0.95)
    for xx in (0, w - 0.03):
        prism_y(g, M_COLD, 0.1, d - 0.25, [(xx, 0.85), (xx + 0.03, 0.85), (xx + 0.03, 1.25), (xx, 1.25)])
    prism_x(g, M_GLASS, 0.03, w - 0.03, [(0.12, 0.86), (0.16, 0.86), (0.48, 1.25), (0.44, 1.25)])
    box(g, M_GLASS, 0.03, 0.44, 1.23, w - 0.03, d - 0.25, 1.25)
    box(g, M_LIGHT, 0.05, 0.6, 1.21, w - 0.05, d - 0.3, 1.23, False)
    kinds = {7: ['cheese', 'cheese'], 4: ['fish', 'fish']}.get(z, ['sausage', 'sausage'])
    for i, k in enumerate(kinds):
        food(g, k, 0.08 + i * 0.9, 0.08 + i * 0.9 + 0.85, 0.18, d - 0.3, 0.88, 0.3, ACCENT[z])
    box(g, M_WHITE, 0.7, d - 0.2, 0.95, 1.0, d - 0.05, 1.0)                    # ваги
    box(g, M_DARK, 0.8, d - 0.12, 1.0, 0.9, d - 0.1, 1.15)


def multideck(g, z):
    """Холодильна пристінна гірка 1,88 × 0,85 × 2,00 м (фронт — y=0)."""
    w, d, h = 1.88, 0.85, 2.0
    box(g, M_COLD, 0, 0.12, 0, w, d, 0.42)
    box(g, dm(z), 0, 0.115, 0.05, w, 0.12, 0.38, False)
    box(g, M_COLD, 0, d - 0.12, 0.42, w, d, h)
    box(g, M_COLD, 0, 0.25, h - 0.18, w, d, h)
    box(g, M_LIGHT, 0.05, 0.25, h - 0.19, w - 0.05, d - 0.15, h - 0.18, False)
    box(g, dm(z), 0, 0.24, h - 0.16, w, 0.25, h - 0.02, False)
    for xx in (0, w - 0.03):
        box(g, M_COLD, xx, 0.12, 0.42, xx + 0.03, d, 0.5)
        box(g, M_GLASS, xx, 0.15, 0.5, xx + 0.03, d - 0.12, h - 0.18)
    box(g, M_METAL, 0.03, 0.05, 0.42, w - 0.03, 0.12, 0.47)
    kinds = {7: ['cartons', 'cups', 'eggs', 'cheese'], 4: ['fish', 'fish', 'fish', 'jars']}.get(z, ['sausage', 'sausage', 'sausage', 'cheese'])
    levels = [0.47, 0.82, 1.14, 1.46]
    for li, z0 in enumerate(levels):
        depth = 0.62 - li * 0.06
        y0 = d - 0.12 - depth
        if li:
            box(g, M_METAL, 0.03, y0, z0 - 0.02, w - 0.03, d - 0.12, z0)
            box(g, dm(z), 0.03, y0 - 0.02, z0 - 0.045, w - 0.03, y0, z0, False)
        top = levels[li + 1] if li + 1 < len(levels) else h - 0.2
        food(g, kinds[li], 0.06, w - 0.06, y0 + 0.01, d - 0.14, z0, top - z0 - 0.03, ACCENT[z])


def freezer(g, z):
    """Морозильний лар (бонета) 1,50 × 0,80 × 0,90 м, доступ з обох довгих боків."""
    w, d, h = 1.5, 0.8, 0.9
    box(g, M_COLD, 0, 0, 0.05, w, d, 0.4)
    box(g, M_DARK, 0.04, 0.04, 0, w - 0.04, d - 0.04, 0.05)
    for yy in (0, d):
        box(g, dm(z), 0, yy - 0.002, 0.1, w, yy + 0.002, 0.5, False)
    for (a, b, c, e) in ((0, 0, w, 0.04), (0, d - 0.04, w, d), (0, 0, 0.04, d), (w - 0.04, 0, w, d)):
        box(g, M_COLD, a, b, 0.4, c, e, h)
    box(g, M_GLASS, 0.04, 0.04, h - 0.02, w / 2, d - 0.04, h)
    box(g, M_GLASS, w / 2, 0.04, h - 0.04, w - 0.04, d - 0.04, h - 0.02)
    x = 0.06
    while x + 0.12 < w - 0.06:
        ww = random.uniform(0.12, 0.2)
        for k in range(random.randint(3, 5)):
            box(g, fm.rnd(['#1565C0', '#C62828', '#2E7D32', '#F9A825', '#6A1B9A', '#EF6C00']), x, 0.06, 0.42 + k * 0.06,
                x + ww, d - 0.06, 0.42 + k * 0.06 + 0.055)
        x += ww + 0.01


def fridge(g, z):
    """Холодильна шафа 0,60 × 0,65 × 2,00 м зі скляними дверима (фронт — y=0)."""
    w, d, h = 0.6, 0.65, 2.0
    box(g, M_COLD, 0, 0.05, 0, w, d, h)
    box(g, dm(z), 0, 0.045, h - 0.28, w, 0.05, h - 0.03, False)
    for xx in (0.02, w - 0.06):
        box(g, M_FRAME, xx, 0.0, 0.1, xx + 0.04, 0.05, h - 0.29)
    box(g, M_FRAME, 0.02, 0.0, 0.1, w - 0.02, 0.05, 0.14)
    box(g, M_FRAME, 0.02, 0.0, h - 0.33, w - 0.02, 0.05, h - 0.29)
    box(g, M_GLASS, 0.06, 0.015, 0.14, w - 0.06, 0.025, h - 0.33)
    box(g, M_DARK, w - 0.1, -0.03, 0.8, w - 0.08, 0.0, 1.4)
    for li, z0 in enumerate([0.15, 0.5, 0.85, 1.2]):
        box(g, M_METAL, 0.06, 0.06, z0 - 0.015, w - 0.06, d - 0.06, z0)
        if z == 5:
            food(g, 'frozen', 0.07, w - 0.07, 0.07, d - 0.08, z0, 0.3)
        else:
            food(g, ['beer', 'cartons', 'beer', 'cartons'][li], 0.07, w - 0.07, 0.07, d - 0.08, z0, 0.32, 'juice')


def veg_hill(g, z):
    """Гірка для овочів і фруктів 1,25 × 1,00 × 1,00 м (ящики з двох боків)."""
    w, d = 1.25, 1.0
    box(g, M_WOOD, 0, 0.08, 0, w, d - 0.08, 0.42)
    prism_x(g, M_WOOD, 0, w, [(0.08, 0.42), (d - 0.08, 0.42), (d / 2, 0.85)])
    box(g, dm(z), 0, d / 2 - 0.02, 0.82, w, d / 2 + 0.02, 1.0)
    for side in (0, 1):
        old = g.xf
        g.xf = (bm.Xf(w, d, 0, 180) if side else bm.Xf()).then(old)
        for (y0, z0) in ((0.0, 0.42), (0.25, 0.66)):
            for i in range(3):
                x0 = 0.02 + i * 0.41
                box(g, M_CRATE, x0, y0, z0 - 0.12, x0 + 0.39, y0 + 0.25, z0, True)
                col, r = random.choice(fm.FRUITS)
                fmat = mat('Фрукти ' + col, col)
                for a in range(int(0.34 / (2 * r))):
                    for b in range(int(0.21 / (2 * r))):
                        sphere(g, fmat, (x0 + 0.03 + r + a * 2 * r, y0 + 0.02 + r + b * 2 * r, z0 + r * 0.6), r, 6, 4)
        g.xf = old


def checkout(g, z):
    """Касовий бокс 1,90 × 0,90 × 0,90 м (уздовж Y; покупці рухаються від y=d до y=0)."""
    w, d, h = 0.9, 1.9, 0.9
    box(g, M_CASH, 0.35, 0.0, 0.0, w, d, h - 0.05)
    box(g, M_METAL, 0.35, 0.0, h - 0.05, w, d, h)
    box(g, M_BELT, 0.4, 0.95, h, w - 0.05, d - 0.05, h + 0.01, False)
    box(g, M_METAL, 0.38, 0.92, h, w - 0.02, 0.95, h + 0.06)
    box(g, M_DARK, 0.5, 0.65, h, 0.8, 0.9, h + 0.03)
    box(g, M_METAL, 0.35, 0.0, h - 0.2, w, 0.6, h - 0.15)
    box(g, M_CASH, 0.0, 0.6, 0.0, 0.35, 1.3, 0.75)
    box(g, M_METAL, 0.0, 0.6, 0.75, 0.35, 1.3, 0.78)
    box(g, M_DARK, 0.04, 0.8, 0.78, 0.28, 1.15, 0.88)
    box(g, M_DARK, 0.06, 0.9, 1.08, 0.3, 1.1, 1.1)
    box(g, M_DARK, 0.06, 0.92, 1.1, 0.3, 0.94, 1.3)
    box(g, M_SCREEN, 0.07, 0.915, 1.11, 0.29, 0.92, 1.29, False)
    cyl(g, M_DARK, (0.17, 1.0, 0.78), 0.02, 0.3, 'z', 6, False)
    box(g, M_DARK, 0.68, 0.4, h, 0.78, 0.5, h + 0.12)
    cyl(g, M_DARK, (-0.28, 0.95, 0), 0.22, 0.04, 'z', 10)
    cyl(g, M_METAL, (-0.28, 0.95, 0.04), 0.03, 0.45, 'z', 6)
    cyl(g, mat('Сидіння', '#37474F'), (-0.28, 0.95, 0.49), 0.18, 0.07, 'z', 12)
    cyl(g, M_METAL, (0.62, 1.4, h), 0.012, 0.9, 'z', 5, False)
    box(g, M_CASH, 0.52, 1.38, h + 0.9, 0.72, 1.42, h + 1.1)
    for k in range(3):                                                               # прикасова викладка
        box(g, fm.rnd(), 0.37 + k * 0.17, d - 0.02, 0.2, 0.5 + k * 0.17, d + 0.1, 0.75)


# ---------------------------------------------------------------- компоненти
TITLES = {'wall_rack': 'Пристінний стелаж 1000×500×2000', 'bread_rack': 'Стелаж для хліба 1000×500×1900',
          'island_rack': 'Острівний двосторонній стелаж 1000×900×1600', 'vitrine': 'Холодильна вітрина 1880×1100×1250',
          'multideck': 'Холодильна пристінна гірка 1880×850×2000', 'freezer': 'Морозильний лар 1500×800×900',
          'fridge': 'Холодильна шафа 600×650×2000', 'veg_hill': 'Гірка для овочів і фруктів 1250×1000×1000',
          'checkout': 'Касовий бокс 1900×900×900'}
DEFS, INSTANCES = {}, []
NUM = {}


def place(builder, z, x0, y0, w, d, facing):
    rot = {'-y': 0, '+x': 90, '+y': 180, '-x': 270}[facing]
    key = (builder.__name__, z)
    if key not in DEFS:
        local = bm.Group(TITLES[builder.__name__] + ' — ' + ZONES[z][0], ZONES[z][0])
        builder(local, z)
        DEFS[key] = local
    r = bm.Xf(0, 0, 0, rot)
    cs = [r((0, 0, 0)), r((w, 0, 0)), r((0, d, 0)), r((w, d, 0))]
    tx, ty = x0 - min(c[0] for c in cs), y0 - min(c[1] for c in cs)
    xf = bm.Xf(0, 0, 0, rot).then(bm.Xf(tx, ty, 0))
    NUM[builder.__name__] = NUM.get(builder.__name__, 0) + 1
    name = f'{TITLES[builder.__name__].split(" 1")[0].split(" 6")[0]} {NUM[builder.__name__]} — {ZONES[z][0]}'
    g = new_group(name, ZONES[z][0])
    for k, polys in DEFS[key].parts.items():
        g.parts[k] = [([xf(p) for p in pts], [r(n) for n in ns] if ns else None) for pts, ns in polys]
    g.instance = True
    INSTANCES.append((key, name, ZONES[z][0], tx, ty, rot))


def build_equipment():
    lay = json.load(open(os.path.join(HERE, 'layout_fig2_2.json')))
    snap = lambda v: round(v * 20) / 20                                   # прив'язка до 5 см
    for t, rects in lay.items():
        for (x0, y0, x1, y1) in rects:
            x0, y0, x1, y1 = snap(x0), snap(y0), snap(x1), snap(y1)
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            z = zone_of(cx, cy)
            vert = (y1 - y0) > (x1 - x0)
            if t == 'W':                      # пристінний 1,0 × 0,5: біля стін і спиною до острівних рядів
                if cx < 1:
                    place(wall_rack, z, x0, y0, 1.0, 0.5, '+x')
                elif cx > 27:
                    place(wall_rack, z, L - 0.5, y0, 1.0, 0.5, '-x')
                else:
                    place(wall_rack, z, x1 - 0.5, y0, 1.0, 0.5, '-x')
            elif t == 'H':
                place(bread_rack, z, L - 0.5, y0, 1.0, 0.5, '-x')
            elif t == 'I':
                place(island_rack, z, x1 - 0.9, y0, 1.0, 0.9, '+x')
            elif t == 'V':
                if vert:
                    place(vitrine, z, x0, y0, 1.88, 1.1, '-x')
                else:
                    place(vitrine, z, x0, y1 - 1.1, 1.88, 1.1, '-y')
            elif t == 'G':
                if not vert:
                    place(multideck, z, x0, D - 0.85, 1.88, 0.85, '-y')
                else:
                    place(multideck, z, x0, y0, 1.88, 0.85, '-x' if cx < 6.16 else '+x')
            elif t == 'L':
                place(freezer, z, x0, y0, 1.5, 0.8, '-y')
            elif t == 'S':
                if cx < 1:
                    place(fridge, z, 0.0, y0, 0.6, 0.65, '+x')
                else:
                    place(fridge, z, x0, y0, 0.6, 0.65, '-y')
            elif t == 'O':
                place(veg_hill, z, x0, y0, 1.25, 1.0, '+x')
            elif t == 'K':
                place(checkout, z, x0, y0, 0.9, 1.9, '-y')


# ---------------------------------------------------------------- будівля
def build_shell():
    for z, (name, (x0, y0, x1, y1), _c) in ZONES.items():
        g = new_group('Підлога — ' + name, 'Підлога')
        for i in range(int(math.floor(x0)), int(math.ceil(x1))):
            for j in range(int(math.floor(y0)), int(math.ceil(y1))):
                a, b, c, e = max(x0, i), min(x1, i + 1), max(y0, j), min(y1, j + 1)
                if b - a > 1e-6 and e - c > 1e-6:
                    g.poly('Підлога — ' + name + (' (темніша)' if (i + j) % 2 else ''), [(a, c, 0), (b, c, 0), (b, e, 0), (a, e, 0)])
        line = mat('Межі відділів', '#9A9A9A')
        for (a, b, c, e) in ((x0, y0, x1, y0 + 0.02), (x0, y1 - 0.02, x1, y1), (x0, y0, x0 + 0.02, y1), (x1 - 0.02, y0, x1, y1)):
            box(g, line, a, b, 0.0005, c, e, 0.002, False)
        bm.TEXTS.append((f'{z}. {name}', (x0 + x1) / 2, y0 + 0.35 if z != 14 else 2.25, 0.01, 0, 0.18, 'Відділ — ' + name, 'floor'))
    g = new_group('Плита основи', 'Підлога')
    box(g, mat('Плита перекриття', '#8C8478'), -WALL, -WALL, -0.25, L + WALL, D + WALL, -0.01)
    box(g, mat('Килимок', '#3D3D3D'), ENTRY[0] + 0.1, 0.05, 0, ENTRY[1] - 0.1, 1.4, 0.012, False)
    g = new_group('Стіни', 'Стіни')
    box(g, M_WALL, -WALL, 0, 0, 0, D + WALL, H)
    box(g, M_WALL, L, 0, 0, L + WALL, D + WALL, H)
    xs = [0.0] + [v for a, b in SERVICE_DOORS for v in (a, b)] + [L]
    for i in range(0, len(xs), 2):
        box(g, M_WALL, xs[i], D, 0, xs[i + 1], D + WALL, H)
    for a, b in SERVICE_DOORS:
        box(g, M_WALL, a, D, 2.1, b, D + WALL, H)
        box(g, M_DOOR, a + 0.03, D + 0.06, 0, b - 0.03, D + 0.1, 2.08)
        box(g, M_DARK, a + 0.08, D + 0.03, 1.0, a + 0.12, D + 0.06, 1.1)
    g = new_group('Фасад із вітринами, входом і виходом', 'Стіни')
    solids = [(-WALL, 0.4), (EXIT[0] - 0.4, EXIT[0]), (EXIT[1], EXIT[1] + 0.4), (ENTRY[0] - 0.4, ENTRY[0]), (ENTRY[1], L + WALL)]
    glass = [(0.4, EXIT[0] - 0.4), (EXIT[1] + 0.4, ENTRY[0] - 0.4)]
    for a, b in solids:
        box(g, M_WALL_OUT, a, -WALL, 0, b, 0, H)
    for a, b in glass:
        box(g, M_WALL_OUT, a, -WALL, 0, b, 0, 0.5)
        box(g, M_WALL_OUT, a, -WALL, 2.7, b, 0, H)
        n = max(1, round((b - a) / 1.8))
        for i in range(n + 1):
            xx = a + (b - a) * i / n
            box(g, M_FRAME, xx - 0.04, -WALL, 0.5, xx + 0.04, -0.05, 2.7)
        for i in range(n):
            box(g, M_GLASS, a + (b - a) * i / n + 0.04, -0.13, 0.5, a + (b - a) * (i + 1) / n - 0.04, -0.11, 2.7)
    for a, b in (EXIT, ENTRY):
        box(g, M_WALL_OUT, a, -WALL, 2.5, b, 0, H)
        box(g, M_FRAME, a, -WALL, 2.42, b, 0, 2.5)
        box(g, M_GLASS, a + 0.05, -0.17, 0.02, a + 0.55, -0.15, 2.42)
        box(g, M_GLASS, b - 0.55, -0.17, 0.02, b - 0.05, -0.15, 2.42)
    g = new_group('Вивіска «Край»', 'Навігація')
    box(g, mat('Вивіска фон', '#2E7D32'), 4.0, -WALL - 0.12, 2.78, 14.0, -WALL, 3.15)
    mat('Вивіска', '#FFFFFF')
    bm.TEXTS += [('КРАЙ · ПРОДУКТИ', 9.0, -WALL - 0.125, 2.84, 0, 0.24, 'Вивіска', 'facade'),
                 ('ВХІД', (ENTRY[0] + ENTRY[1]) / 2, -WALL - 0.03, 2.55, 0, 0.14, 'Вивіска', 'facade'),
                 ('ВИХІД', (EXIT[0] + EXIT[1]) / 2, -WALL - 0.03, 2.55, 0, 0.14, 'Вивіска', 'facade')]
    g = new_group('Тротуар', 'Благоустрій')
    box(g, mat('Тротуарна плитка', '#BDB8AE'), -1.0, -5.0, -0.25, L + 1.0, -WALL, -0.03)


def build_navigation():
    g = new_group('Підвісні покажчики відділів', 'Навігація')
    signs = {1: (26.6, 4.9), 2: (26.6, 9.6), 3: (26.6, 16.0), 4: (23.4, 17.0), 5: (23.4, 13.6), 6: (14.5, 14.6),
             7: (4.6, 17.5), 8: (1.5, 12.3), 9: (21.8, 10.9), 10: (16.8, 10.9), 11: (12.5, 10.9), 12: (7.4, 10.9),
             13: (4.0, 10.9), 14: (9.0, 2.6)}
    for z, (cx, cy) in signs.items():
        name = ZONES[z][0] if z != 14 else 'Каси'
        width = min(2.6, max(1.2, 0.11 * len(name)))
        box(g, dm(z), cx - width / 2, cy - 0.03, 2.55, cx + width / 2, cy + 0.03, 2.9)
        for xx in (cx - width / 2 + 0.1, cx + width / 2 - 0.1):
            cyl(g, M_METAL, (xx, cy, 2.9), 0.004, H - 2.9, 'z', 4, False)
        bm.TEXTS.append((name.upper() if len(name) < 22 else name, cx, cy - 0.035, 2.63, 0, 0.12, 'Вивіска', 'y-'))


SCENES_RB = '''    scene(model, 'Загальний вигляд', [-6.0, -14.0, 20.0], [14.0, 10.5, 0.0])
    scene(model, 'Вигляд від входу', [24.2, 0.4, 1.65], [14.0, 14.0, 0.9])
    scene(model, 'План зверху', [14.0, 10.0, 40.0], [14.0, 10.0, 0.0], false, 22.0)
    scene(model, 'М’ясо-ковбасний і молочний відділи', [12.0, 11.2, 2.0], [12.0, 19.0, 0.9])
    scene(model, 'Ряди стелажів', [12.4, 2.8, 1.7], [12.4, 11.0, 0.9])
    scene(model, 'Касовий вузол', [16.0, 4.0, 2.3], [6.0, 0.5, 0.6])
'''

SHEET = dict(sh.SHEET)
SHEET.update({
    'SHEET_TITLE': 'ПРОЄКТ ТОРГОВЕЛЬНОЇ ЗАЛИ ПРОДОВОЛЬЧОГО МАГАЗИНУ ТОВ «КРАЙ»',
    'SHEET_SUBTITLE': 'Тривимірна модель торговельної зали у SketchUp (п. 2.4, рис. 2.3, Б.1). Зала 28,0 × 20,0 м, площа 560 м², висота 3,2 м',
    'SHEET_VIEWS': [
        ['План зверху', 30, 34, 300, 215, 'План торговельної зали з розміщенням обладнання, М 1:100', 0.01],
        ['Загальний вигляд', 345, 34, 481, 215, 'Загальний вигляд моделі (рис. 2.3)', None],
        ['Вигляд від входу', 30, 270, 260, 165, 'Вигляд торговельної зали від входу (рис. Б.1)', None],
        ['М’ясо-ковбасний і молочний відділи', 300, 270, 260, 165, 'Холодильне обладнання біля задньої стіни', None],
        ['Касовий вузол', 570, 270, 256, 165, 'Касовий вузол', None],
    ],
    'SHEET_EQUIP': [[1, 'Пристінний стелаж', '1000×500×2000', 59], [2, 'Острівний двосторонній стелаж', '1000×900×1600', 53],
                    [3, 'Стелаж для хліба', '1000×500×1900', 6], [4, 'Холодильна вітрина (прилавок)', '1880×1100×1250', 14],
                    [5, 'Холодильна пристінна гірка', '1880×850×2000', 11], [6, 'Морозильний лар (бонета)', '1500×800×900', 4],
                    [7, 'Холодильна шафа', '600×650×2000', 5], [8, 'Гірка для овочів і фруктів', '1250×1000×1000', 2],
                    [9, 'Касовий бокс', '1900×900×900', 6], ['', 'Разом', '', 160]],
    'SHEET_LEGEND': [[f'{z}. {ZONES[z][0]}', ZONES[z][2]] for z in ZONES][:7],
    'SHEET_STAMP': [['Курсова робота з дисципліни «Проєктування торговельних об’єктів»', 9, False],
                    ['Продовольчий магазин ТОВ «Край». Тривимірна модель торговельної зали', 9, True],
                    ['Розробив(ла): ______________________   Перевірив(ла): ______________________', 9, False],
                    ['ДТЕУ, кафедра торговельного підприємництва та логістики', 9, False],
                    ['Аркуш А1 (841 × 594)        Масштаб плану 1:100        Київ 2026', 9, False]],
})


def main():
    bm.GROUPS.clear(); bm.TEXTS.clear(); DEFS.clear(); INSTANCES.clear(); NUM.clear()
    build_shell()
    build_equipment()
    build_navigation()
    eq = [g for g in bm.GROUPS if getattr(g, 'instance', False)]
    from collections import Counter
    print(f'Груп: {len(bm.GROUPS)}, одиниць обладнання: {len(eq)}, визначень компонентів: {len(DEFS)}, '
          f'полігонів: {sum(g.nfaces() for g in bm.GROUPS)}')
    print(dict(Counter(k[0] for k, *_ in INSTANCES)))
    dae = os.path.join(HERE, 'kray.dae')
    rb = os.path.join(HERE, 'kray.rb')
    bm.export_dae(dae)
    s = open(dae, encoding='utf-8').read()
    s = s.replace('build_model.py — ТОВ «Дитячий світ»', 'build_model.py — ТОВ «Край»').replace('name="Дитячий світ"', 'name="Край"')
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
    keys = list(DEFS)
    comps = ['    # обладнання: визначення компонентів і їхні копії\n', '    defs = {}\n']
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
    s = s.replace("""    when 'x+' then""", """    when 'floor' then r = Geom::Transformation.translation([0, -h * M / 2.0, 0])
    when 'x+' then""", 1)
    s = s.replace("""      model.options['UnitsOptions']['LengthUnit'] = 4  # метри""",
                  """      model.options['UnitsOptions']['LengthUnit'] = 2       # міліметри
      model.options['UnitsOptions']['LengthPrecision'] = 0""")
    s = s.replace("""    model.commit_operation
""", """    model.commit_operation
    dir = File.dirname(__FILE__)
    skp = File.join(dir, 'kray.skp')
    model.save(skp)
    puts "Збережено: #{skp}"
    begin
      make_layout(skp, File.join(dir, 'kray_A1.layout'), File.join(dir, 'kray_A1.pdf'))
    rescue StandardError, LoadError => e
      puts "Аркуш LayOut не створено: #{e.message}"
    end
""", 1)
    s = (s.replace('DytiachyiSvit', 'Kray').replace('магазину ТОВ «Дитячий світ» (курсова робота, розділ 4)',
                                                   'торговельної зали продовольчого магазину ТОВ «Край» (курсова робота, п. 2.4)')
         .replace('dytiachyi_svit.rb', 'kray.rb').replace('Дитячий світ', 'Край'))
    s = s.replace("# Згенеровано build_model.py; одиниці — метри.",
                  "# Згенеровано build_model.py. Після побудови скрипт зберігає поруч kray.skp,\n"
                  "# створює аркуш А1 kray_A1.layout у LayOut і експортує його у kray_A1.pdf.")
    open(rb, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    main()
