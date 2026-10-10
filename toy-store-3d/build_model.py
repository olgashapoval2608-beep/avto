#!/usr/bin/env python3
"""Генератор детальної 3D-моделі магазину ТОВ «Дитячий світ» для SketchUp.

Модель будується за курсовою роботою: зал 25,0 × 16,0 м, висота 3,3 м,
обладнання та габарити — таблиця 3.4, розміщення відділів — таблиця 3.3,
координати — планограма (додаток Б, рис. Б.1).

Система координат: X — уздовж фасаду (0 — ліва стіна, вихід; 25 — права стіна,
вхід), Y — углиб залу (0 — фасад, 16 — дальня стіна), Z — вгору. Одиниці — метри.

Результат:
  dytiachyi_svit.dae — COLLADA для «Файл → Імпорт» у SketchUp;
  dytiachyi_svit.rb  — Ruby-скрипт, що будує модель безпосередньо в SketchUp
                       (групи, матеріали, теги, 3D-написи, сцени).
"""
import math
import random
import os

random.seed(2026)
HERE = os.path.dirname(os.path.abspath(__file__))

L, W, H = 25.0, 16.0, 3.3          # зал
WALL = 0.25                        # товщина стін

# ---------------------------------------------------------------- матеріали
MATERIALS = {}


def mat(name, hexcol, alpha=1.0):
    MATERIALS[name] = (hexcol, alpha)
    return name


def hx(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))


def shade(hexcol, k):
    r, g, b = hx(hexcol)
    if k >= 1:
        r, g, b = (x + (1 - x) * (k - 1) for x in (r, g, b))
    else:
        r, g, b = (x * k for x in (r, g, b))
    return '#%02X%02X%02X' % tuple(int(max(0, min(1, x)) * 255) for x in (r, g, b))


M_FLOOR_A = mat('Підлога керамограніт світлий', '#EDEAE2')
M_FLOOR_B = mat('Підлога керамограніт сірий', '#DCD8CE')
M_WALL = mat('Стіни фарба', '#F4F1EA')
M_WALL_OUT = mat('Фасад', '#C9BBA5')
M_PLINTH = mat('Плінтус', '#8C8478')
M_GLASS = mat('Скло', '#A8D8EA', 0.35)
M_FRAME = mat('Алюмінієвий профіль', '#6E7378')
M_MAT = mat('Килимок входу', '#4A4A4A')
M_PAVE = mat('Бруківка', '#B9B4AA')
M_SHELF = mat('Обладнання білий ЛДСП', '#F7F7F5')
M_SHELF_EDGE = mat('Обладнання кромка', '#D9D6CF')
M_METAL = mat('Метал хром', '#B8BCC2')
M_DARK = mat('Метал чорний', '#2E3134')
M_WOOD = mat('Дерево', '#C8A27A')
M_PODIUM = mat('Подіум', '#FAFAFA')
M_SCREEN = mat('Екран', '#1C2833')
M_CURTAIN = mat('Штора примірочної', '#7E57C2')
M_MIRROR = mat('Дзеркало', '#D6E4EA')
M_TYRE = mat('Шини', '#222222')
M_SIGN = mat('Вивіска', '#FFFFFF')
M_SKIN = mat('Ляльки обличчя', '#F2C9A8')
M_STROLLER_PARK = mat('Стійка для візків', '#5D6D7E')

TOY = ['#E53935', '#FB8C00', '#FDD835', '#43A047', '#1E88E5', '#8E24AA',
       '#00ACC1', '#F06292', '#7CB342', '#FF7043', '#5C6BC0', '#26A69A']
for c in TOY:
    mat('Товар ' + c, c)


def toy_mat(base=None, p_base=0.45):
    if base and random.random() < p_base:
        c = shade(base, random.choice([0.8, 0.9, 1.0, 1.15, 1.3]))
        return mat('Товар ' + c, c)
    return 'Товар ' + random.choice(TOY)


# Відділи (табл. 3.3), кольори навігації — як у рис. 4.2
DEPTS = {
    'konstr':  ('Конструктори', 'A', '#E2572B'),
    'games':   ('Розвиваючі дедуктивні ігри', 'A', '#F0A01E'),
    'cars':    ('Електромобілі, педальні машини', 'A', '#D7263D'),
    'play':    ('Обладнання для ігрових майданчиків', 'A', '#43A047'),
    'girls':   ('Одяг для дівчат', 'A', '#E98FB0'),
    'boys':    ('Одяг для хлопчиків', 'A', '#5BA3E0'),
    'access':  ('Аксесуари', 'A', '#AE7CC8'),
    'station': ('Канцтовари', 'A', '#26AFC0'),
    'sport':   ('Іграшки для спорту', 'B', '#7CB342'),
    'balls':   ("М'ячі", 'B', '#FFD54F'),
    'dolls':   ('Ляльки', 'B', '#F48FB1'),
    'rooms':   ('Дитячі кімнати для ляльок', 'B', '#FFB74D'),
    'dollwear': ('Одяг для ляльок', 'C', '#CE93D8'),
    'transport': ('Транспорт', 'C', '#4FC3F7'),
    'military': ('Моделі іграшкової воєнної техніки', 'C', '#6B8E23'),
    'books':   ('Художня література для дітей', 'C', '#8D6E63'),
    'service': ('Касова зона, примірочні, камера схову', '-', '#9E9E9E'),
}
for k, (n, g, c) in DEPTS.items():
    mat('Відділ — ' + n, c)
    mat('Відділ — ' + n + ' (світлий)', shade(c, 1.35))


def dmat(dept, light=False):
    return 'Відділ — ' + DEPTS[dept][0] + (' (світлий)' if light else '')


# ---------------------------------------------------------------- геометрія
class Xf:
    """Поворот навколо Z (кратний 90°) + перенесення."""

    def __init__(self, ox=0, oy=0, oz=0, rot=0):
        self.o = (ox, oy, oz)
        self.rot = rot % 360

    def __call__(self, p):
        x, y, z = p
        if self.rot == 90:
            x, y = -y, x
        elif self.rot == 180:
            x, y = -x, -y
        elif self.rot == 270:
            x, y = y, -x
        return (x + self.o[0], y + self.o[1], z + self.o[2])

    def then(self, outer):
        """Композиція: спершу self, потім outer."""
        s = self
        return _Comp(s, outer)


class _Comp:
    def __init__(self, a, b):
        self.a, self.b = a, b

    def __call__(self, p):
        return self.b(self.a(p))

    def then(self, outer):
        return _Comp(self, outer)


class Group:
    def __init__(self, name, tag):
        self.name = name
        self.tag = tag
        self.parts = {}            # (material, smooth) -> list of (pts, normals|None)
        self.xf = Xf()

    def poly(self, m, pts, normals=None, smooth=False):
        pts = [self.xf(p) for p in pts]
        if normals is not None:
            normals = [self.xf_dir(n) for n in normals]
        self.parts.setdefault((m, smooth), []).append((pts, normals))

    def xf_dir(self, n):
        a = self.xf((0, 0, 0))
        b = self.xf(n)
        return (b[0] - a[0], b[1] - a[1], b[2] - a[2])

    def nfaces(self):
        return sum(len(v) for v in self.parts.values())


def box(g, m, x0, y0, z0, x1, y1, z1, bottom=True):
    if x1 < x0: x0, x1 = x1, x0
    if y1 < y0: y0, y1 = y1, y0
    if z1 < z0: z0, z1 = z1, z0
    P = lambda x, y, z: (x, y, z)
    g.poly(m, [P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)])        # top
    if bottom:
        g.poly(m, [P(x0, y0, z0), P(x0, y1, z0), P(x1, y1, z0), P(x1, y0, z0)])    # bottom
    g.poly(m, [P(x0, y0, z0), P(x1, y0, z0), P(x1, y0, z1), P(x0, y0, z1)])        # -y
    g.poly(m, [P(x1, y1, z0), P(x0, y1, z0), P(x0, y1, z1), P(x1, y1, z1)])        # +y
    g.poly(m, [P(x0, y1, z0), P(x0, y0, z0), P(x0, y0, z1), P(x0, y1, z1)])        # -x
    g.poly(m, [P(x1, y0, z0), P(x1, y1, z0), P(x1, y1, z1), P(x1, y0, z1)])        # +x


def cyl(g, m, c, r, length, axis='z', n=12, caps=True, r2=None):
    """Циліндр (або зрізаний конус, якщо задано r2) з центром основи c."""
    r2 = r if r2 is None else r2
    cx, cy, cz = c

    def pt(a, rr, t):
        u, v = rr * math.cos(a), rr * math.sin(a)
        if axis == 'z':
            return (cx + u, cy + v, cz + t)
        if axis == 'x':
            return (cx + t, cy + u, cz + v)
        return (cx + v, cy + t, cz + u)        # axis y

    def nrm(a):
        u, v = math.cos(a), math.sin(a)
        if axis == 'z':
            return (u, v, 0)
        if axis == 'x':
            return (0, u, v)
        return (v, 0, u)

    angs = [2 * math.pi * i / n for i in range(n)]
    for i in range(n):
        a0, a1 = angs[i], angs[(i + 1) % n]
        g.poly(m, [pt(a0, r, 0), pt(a1, r, 0), pt(a1, r2, length), pt(a0, r2, length)],
               [nrm(a0), nrm(a1), nrm(a1), nrm(a0)], smooth=True)
    if caps:
        g.poly(m, [pt(a, r2, length) for a in angs])
        g.poly(m, [pt(a, r, 0) for a in reversed(angs)])


def sphere(g, m, c, r, nu=10, nv=6, zscale=1.0):
    cx, cy, cz = c

    def P(i, j):
        th = 2 * math.pi * i / nu
        ph = math.pi * j / nv - math.pi / 2
        n = (math.cos(ph) * math.cos(th), math.cos(ph) * math.sin(th), math.sin(ph))
        return (cx + r * n[0], cy + r * n[1], cz + r * zscale * n[2]), n

    for j in range(nv):
        for i in range(nu):
            quad = [P(i, j), P(i + 1, j), P(i + 1, j + 1), P(i, j + 1)]
            pts, ns = [q[0] for q in quad], [q[1] for q in quad]
            if j == 0:
                pts, ns = [pts[0], pts[2], pts[3]], [ns[0], ns[2], ns[3]]
            elif j == nv - 1:
                pts, ns = pts[:3], ns[:3]
            g.poly(m, pts, ns, smooth=True)


def prism_x(g, m, x0, x1, prof):
    """Призма: профіль prof [(y,z),...] (проти год. стрілки, якщо дивитись з +x),
    витягнутий уздовж X від x0 до x1."""
    n = len(prof)
    g.poly(m, [(x1, y, z) for y, z in prof])
    g.poly(m, [(x0, y, z) for y, z in reversed(prof)])
    for i in range(n):
        (ya, za), (yb, zb) = prof[i], prof[(i + 1) % n]
        g.poly(m, [(x0, ya, za), (x0, yb, zb), (x1, yb, zb), (x1, ya, za)])


def prism_y(g, m, y0, y1, prof):
    """Профіль [(x,z),...] проти год. стрілки, якщо дивитись з -y; уздовж Y."""
    n = len(prof)
    g.poly(m, [(x, y0, z) for x, z in prof])
    g.poly(m, [(x, y1, z) for x, z in reversed(prof)])
    for i in range(n):
        (xa, za), (xb, zb) = prof[i], prof[(i + 1) % n]
        g.poly(m, [(xa, y1, za), (xb, y1, zb), (xb, y0, zb), (xa, y0, za)])


def plate(g, m, pts):
    """Двостороння тонка площина (для таблички/штори)."""
    g.poly(m, pts)
    g.poly(m, list(reversed(pts)))


# ---------------------------------------------------------------- товари
def products(g, kind, dept, x0, x1, y0, y1, z, hmax):
    """Заповнює ділянку полиці [x0,x1]×[y0,y1] на висоті z товарами."""
    base = DEPTS[dept][2]
    d = y1 - y0
    x = x0 + 0.02
    if kind == 'balls':
        while True:
            r = random.uniform(0.07, min(0.11, hmax / 2 - 0.01))
            if x + 2 * r > x1:
                break
            for yy in (y0 + d * 0.3, y0 + d * 0.72):
                sphere(g, toy_mat(base, 0.3), (x + r, yy, z + r), r, 8, 5)
            x += 2 * r + 0.01
        return
    if kind == 'books':
        while x < x1 - 0.03:
            t = random.uniform(0.018, 0.04)
            h = random.uniform(0.18, min(0.3, hmax - 0.02))
            box(g, toy_mat(base, 0.25), x, y0 + 0.04, z, x + t, y0 + random.uniform(0.17, 0.22), z + h, False)
            x += t + 0.004
            if random.random() < 0.08:
                x += 0.08
        return
    if kind in ('transport', 'military'):
        while True:
            w = random.uniform(0.2, 0.3)
            if x + w > x1:
                break
            for yy in (y0 + 0.05, y0 + d * 0.5):
                vehicle(g, x, yy, z, w, min(0.2, d * 0.42), kind == 'military', base)
            x += w + 0.04
        return
    if kind == 'games':                        # стоси плоских коробок
        while True:
            w = random.uniform(0.28, 0.4)
            if x + w > x1:
                break
            zz = z
            for _ in range(random.randint(2, 5)):
                t = random.uniform(0.05, 0.08)
                if zz + t > z + hmax - 0.03:
                    break
                box(g, toy_mat(base), x, y0 + 0.04, zz, x + w, y1 - 0.04, zz + t, False)
                zz += t
            x += w + 0.03
        return
    if kind == 'dolls':
        while True:
            w = random.uniform(0.16, 0.22)
            if x + w > x1:
                break
            h = min(hmax - 0.03, random.uniform(0.28, 0.34))
            m = toy_mat(base, 0.7)
            box(g, m, x, y0 + 0.06, z, x + w, y0 + 0.16, z + h, False)
            box(g, M_GLASS, x + 0.03, y0 + 0.055, z + 0.05, x + w - 0.03, y0 + 0.06, z + h - 0.06, False)
            sphere(g, M_SKIN, (x + w / 2, y0 + 0.1, z + h - 0.11), 0.035, 8, 5)
            box(g, toy_mat(base, 0.6), x + w / 2 - 0.035, y0 + 0.08, z + 0.05, x + w / 2 + 0.035, y0 + 0.12, z + h - 0.15, False)
            x += w + 0.02
        return
    if kind == 'rooms':                        # будиночки для ляльок
        while True:
            w = random.uniform(0.35, 0.45)
            if x + w > x1:
                break
            h = min(hmax - 0.14, 0.2)
            m = toy_mat(base, 0.6)
            box(g, m, x, y0 + 0.08, z, x + w, y1 - 0.05, z + h, False)
            prism_x(g, toy_mat(None), x - 0.01, x + w + 0.01,
                    [(y0 + 0.06, z + h), (y1 - 0.03, z + h), ((y0 + y1) / 2, z + h + 0.12)])
            box(g, M_GLASS, x + 0.06, y0 + 0.075, z + 0.06, x + 0.14, y0 + 0.08, z + 0.14, False)
            box(g, M_WOOD, x + w - 0.13, y0 + 0.075, z, x + w - 0.06, y0 + 0.08, z + 0.13, False)
            x += w + 0.04
        return
    # boxes: конструктори, спорт, аксесуари, канцтовари, одяг для ляльок
    while True:
        w = random.uniform(0.14, 0.36) if kind != 'konstr' else random.uniform(0.25, 0.45)
        if x + w > x1:
            break
        h = random.uniform(0.35, 0.95) * (hmax - 0.03)
        dd = random.uniform(0.5, 0.9) * d
        m = toy_mat(base, 0.4)
        box(g, m, x, y0 + 0.03, z, x + w, y0 + 0.03 + dd, z + h, False)
        if kind == 'sport' and random.random() < 0.3 and h > 0.2:
            sphere(g, toy_mat(None), (x + w / 2, y0 + 0.03 + dd / 2, z + h + 0.06), 0.06, 8, 5)
        x += w + random.uniform(0.01, 0.04)


def vehicle(g, x, y, z, w, d, military, base):
    m = 'Товар ' + ('#556B2F' if military else random.choice(TOY))
    if military:
        m = mat('Товар хакі', shade('#6B8E23', random.choice([0.7, 0.85, 1.0])))
    wr = 0.035
    box(g, m, x, y, z + wr, x + w, y + d, z + wr + 0.06, False)
    if military and random.random() < 0.5:     # танк
        box(g, m, x + w * 0.3, y + d * 0.2, z + wr + 0.06, x + w * 0.75, y + d * 0.8, z + wr + 0.11, False)
        cyl(g, m, (x + w * 0.75, y + d / 2, z + wr + 0.085), 0.012, w * 0.4, 'x', 6, False)
        box(g, M_TYRE, x, y - 0.005, z, x + w, y + 0.03, z + wr + 0.02, False)
        box(g, M_TYRE, x, y + d - 0.03, z, x + w, y + d + 0.005, z + wr + 0.02, False)
        return
    box(g, M_GLASS if not military else m, x + w * 0.25, y + 0.01, z + wr + 0.06, x + w * 0.7, y + d - 0.01, z + wr + 0.11, False)
    for xx in (x + w * 0.2, x + w * 0.8):
        for yy, sgn in ((y, -1), (y + d, 1)):
            cyl(g, M_TYRE, (xx, yy - (0.012 if sgn < 0 else 0), z + wr), wr, 0.012, 'y', 8)


# ---------------------------------------------------------------- обладнання
def gorka(g, dept, kind, h=2.2, levels=None, frieze=True):
    """Пристінний стелаж-гірка 1,25×0,60×h (фронт — y=0)."""
    w, d = 1.25, 0.6
    box(g, M_SHELF_EDGE, 0.03, 0.04, 0, w - 0.03, d, 0.1)                      # цоколь
    box(g, M_SHELF, 0, 0, 0, 0.03, d, h)                                        # боковини
    box(g, M_SHELF, w - 0.03, 0, 0, w, d, h)
    box(g, dmat(dept, True), 0.03, d - 0.03, 0.1, w - 0.03, d, h)               # задня панель у кольорі відділу
    levels = levels or ([0.1, 0.5, 0.9, 1.3, 1.7] if h > 2 else [0.1, 0.55, 1.0])
    tops = levels[1:] + [h - 0.04]
    for z0, z1 in zip(levels, tops):
        if z0 > 0.1:
            box(g, M_SHELF, 0.03, 0.02, z0 - 0.025, w - 0.03, d - 0.03, z0)      # полиця
            box(g, dmat(dept), 0.03, 0.0, z0 - 0.055, w - 0.03, 0.02, z0)       # цінникова планка
        products(g, kind, dept, 0.05, w - 0.05, 0.03, d - 0.05, z0, z1 - z0 - 0.04)
    box(g, M_SHELF, 0, 0, h - 0.03, w, d, h)                                    # кришка
    if frieze:                                                                  # кольоровий фриз
        box(g, dmat(dept), 0, d - 0.12, h + 0.12, w, d - 0.02, h + 0.42)


def clothes_wall(g, dept):
    """Пристінна система для одягу 1,25×0,60×2,2."""
    w, d, h = 1.25, 0.6, 2.2
    box(g, dmat(dept, True), 0, d - 0.04, 0, w, d, h)                           # економпанель
    for xx in (0.0, w - 0.03):
        box(g, M_METAL, xx, d - 0.07, 0, xx + 0.03, d - 0.04, h)
    box(g, M_SHELF, 0.02, 0.15, 1.92, w - 0.02, d - 0.04, 1.95)                 # верхня полиця
    xx = 0.08
    while xx < w - 0.18:                                                        # складений одяг
        hh = random.uniform(0.08, 0.16)
        box(g, toy_mat(DEPTS[dept][2], 0.75), xx, 0.25, 1.95, xx + 0.26, d - 0.08, 1.95 + hh, False)
        xx += 0.3
    for zr, hang in ((1.75, 0.7), (1.05, 0.62)):                                # штанги з одягом
        cyl(g, M_METAL, (0.02, 0.3, zr), 0.012, w - 0.04, 'x', 6, False)
        xx = 0.07
        while xx < w - 0.05:
            garment(g, xx, 0.3, zr, hang, DEPTS[dept][2])
            xx += random.uniform(0.07, 0.1)
    box(g, M_SHELF, 0.02, 0.05, 0.0, w - 0.02, d - 0.04, 0.3)                   # нижній бокс
    xx = 0.06
    while xx < w - 0.25:                                                        # взуття / коробки
        box(g, toy_mat(DEPTS[dept][2], 0.5), xx, 0.12, 0.3, xx + 0.22, 0.42, 0.3 + 0.12, False)
        xx += 0.27
    box(g, dmat(dept), 0, d - 0.12, h + 0.12, w, d - 0.02, h + 0.42)


def garment(g, x, y, zr, hang, base, along='x'):
    m = toy_mat(base, 0.65)
    t = 0.025
    if along == 'x':          # одяг, повішений «боком» (плечики перпендикулярні штанзі)
        box(g, m, x - t / 2, y - 0.2, zr - 0.05 - hang, x + t / 2, y + 0.2, zr - 0.05, False)
        box(g, M_DARK, x - 0.004, y - 0.002, zr - 0.05, x + 0.004, y + 0.002, zr + 0.01, False)


def low_shelf(g):
    gorka(g, 'station', 'boxes', h=1.4, levels=[0.1, 0.55, 1.0], frieze=False)


def gondola(g, dept, kind, end_left=False, end_right=False):
    """Острівна двостороння гондола 1,25×1,20×1,60."""
    w, d, h = 1.25, 1.2, 1.6
    box(g, M_SHELF_EDGE, 0, 0.05, 0, w, d - 0.05, 0.1)
    box(g, dmat(dept, True), 0.0, d / 2 - 0.03, 0.1, w, d / 2 + 0.03, h)       # центральна панель
    box(g, M_METAL, 0.0, d / 2 - 0.04, 0.1, 0.03, d / 2 + 0.04, h)
    box(g, M_METAL, w - 0.03, d / 2 - 0.04, 0.1, w, d / 2 + 0.04, h)
    box(g, M_SHELF, 0, d / 2 - 0.05, h - 0.03, w, d / 2 + 0.05, h)
    levels = [0.1, 0.5, 0.9, 1.3]
    for side in (0, 1):
        sx = Xf(w, d, 0, 180) if side else Xf()
        old = g.xf
        g.xf = sx.then(old)
        for i, z0 in enumerate(levels):
            depth = 0.55 - 0.05 * i
            y0 = d / 2 - 0.03 - depth
            if z0 > 0.1:
                box(g, M_SHELF, 0.03, y0, z0 - 0.025, w - 0.03, d / 2 - 0.03, z0)
                box(g, dmat(dept), 0.03, y0 - 0.02, z0 - 0.055, w - 0.03, y0, z0)
            else:
                box(g, M_SHELF, 0.0, 0.05, 0.08, w, d / 2 - 0.03, 0.1)
            top = levels[i + 1] if i + 1 < len(levels) else h - 0.02
            products(g, kind, dept, 0.05, w - 0.05, y0 + 0.01, d / 2 - 0.05, z0, top - z0 - 0.04)
        g.xf = old
    for end, xx in ((end_left, -0.02), (end_right, w)):
        if end:                                                                 # торцева панель
            box(g, dmat(dept), xx, 0.05, 0.1, xx + 0.02, d - 0.05, h + 0.05)


def podium(g, dept, content):
    w, d, h = 3.0, 2.0, 0.3
    box(g, M_PODIUM, 0, 0, 0, w, d, h)
    box(g, dmat(dept), -0.005, -0.005, 0.02, w + 0.005, d + 0.005, 0.08, False)
    old = g.xf
    g.xf = Xf(0, 0, h).then(old)
    if content == 'cars1':
        kid_car(g, 0.25, 0.35, '#D7263D', 'jeep')
        kid_car(g, 1.65, 0.45, '#1E88E5', 'sport')
    elif content == 'cars2':
        kid_car(g, 0.2, 0.4, '#FDD835', 'sport')
        pedal_car(g, 1.6, 0.6, '#43A047')
        kid_car(g, 2.05, 1.25, '#E53935', 'quad')
    elif content == 'slide':
        slide(g, 0.3, 0.5)
        sandbox(g, 2.0, 0.6)
    elif content == 'house':
        playhouse(g, 0.25, 0.4)
        swing(g, 1.75, 0.35)
    g.xf = old


def kid_car(g, x, y, col, style):
    m = mat('Корпус ' + col, col)
    if style == 'quad':
        box(g, m, x, y, 0.18, x + 0.75, y + 0.45, 0.32)
        box(g, M_DARK, x + 0.25, y + 0.12, 0.32, x + 0.5, y + 0.33, 0.4)
        cyl(g, M_DARK, (x + 0.6, y + 0.225, 0.32), 0.015, 0.25, 'z', 6, False)
        box(g, M_DARK, x + 0.62, y + 0.05, 0.55, x + 0.65, y + 0.4, 0.58)
        for xx in (x + 0.12, x + 0.63):
            for yy in (y - 0.08, y + 0.45):
                cyl(g, M_TYRE, (xx, yy, 0.13), 0.13, 0.08, 'y', 12)
        return
    L_, W_ = 1.15, 0.68
    if style == 'jeep':
        prism_y(g, m, y, y + W_, [(x, 0.12), (x + L_, 0.12), (x + L_, 0.42), (x + 0.95, 0.46), (x + 0.15, 0.46), (x, 0.4)])
        box(g, M_GLASS, x + 0.72, y + 0.06, 0.46, x + 0.75, y + W_ - 0.06, 0.7)
        box(g, m, x + 0.05, y + 0.02, 0.46, x + 0.25, y + W_ - 0.02, 0.5)
        box(g, M_DARK, x + 0.3, y + 0.12, 0.46, x + 0.65, y + W_ - 0.12, 0.62)     # сидіння
        box(g, M_DARK, x + 0.3, y + 0.12, 0.62, x + 0.36, y + W_ - 0.12, 0.8)
        box(g, M_METAL, x + L_ - 0.01, y + 0.1, 0.25, x + L_ + 0.03, y + W_ - 0.1, 0.33)
    else:
        prism_y(g, m, y, y + W_, [(x, 0.12), (x + L_, 0.12), (x + L_, 0.3), (x + 0.85, 0.36), (x + 0.35, 0.36), (x + 0.05, 0.42)])
        box(g, M_GLASS, x + 0.7, y + 0.08, 0.36, x + 0.73, y + W_ - 0.08, 0.52)
        box(g, M_DARK, x + 0.3, y + 0.14, 0.36, x + 0.6, y + W_ - 0.14, 0.44)
        box(g, M_DARK, x + 0.3, y + 0.14, 0.44, x + 0.35, y + W_ - 0.14, 0.62)
        box(g, m, x + 0.0, y + 0.05, 0.42, x + 0.06, y + W_ - 0.05, 0.47)        # спойлер
    cyl(g, M_DARK, (x + 0.62, y + W_ / 2, 0.45), 0.012, 0.18, 'z', 6, False)        # кермо
    cyl(g, M_DARK, (x + 0.62, y + W_ / 2, 0.63), 0.09, 0.02, 'x', 12)
    for xx in (x + 0.22, x + L_ - 0.22):
        for yy in (y - 0.09, y + W_):
            cyl(g, M_TYRE, (xx, yy, 0.13), 0.13, 0.09, 'y', 14)
            cyl(g, M_METAL, (xx, yy + (-0.005 if yy < y else 0.09), 0.13), 0.06, 0.005, 'y', 10)
    box(g, mat('Фари', '#FFF8C4'), x + L_, y + 0.06, 0.28, x + L_ + 0.01, y + 0.16, 0.34, False)
    box(g, mat('Фари', '#FFF8C4'), x + L_, y + W_ - 0.16, 0.28, x + L_ + 0.01, y + W_ - 0.06, 0.34, False)


def pedal_car(g, x, y, col):
    m = mat('Корпус ' + col, col)
    prism_y(g, m, y, y + 0.45, [(x, 0.1), (x + 0.85, 0.1), (x + 0.85, 0.25), (x + 0.6, 0.3), (x + 0.1, 0.32)])
    box(g, M_DARK, x + 0.15, y + 0.08, 0.32, x + 0.4, y + 0.37, 0.38)
    box(g, M_DARK, x + 0.15, y + 0.08, 0.38, x + 0.19, y + 0.37, 0.52)
    cyl(g, M_DARK, (x + 0.55, y + 0.225, 0.3), 0.01, 0.15, 'z', 6, False)
    cyl(g, M_DARK, (x + 0.55, y + 0.225, 0.45), 0.07, 0.015, 'x', 10)
    for xx in (x + 0.15, x + 0.7):
        for yy in (y - 0.06, y + 0.45):
            cyl(g, M_TYRE, (xx, yy, 0.1), 0.1, 0.06, 'y', 12)


def slide(g, x, y):
    """Дитяча гірка: майданчик, сходи, скат."""
    red = mat('Пластик червоний', '#E53935')
    yel = mat('Пластик жовтий', '#FDD835')
    blu = mat('Пластик синій', '#1E88E5')
    p = 0.9                                   # висота майданчика
    for xx in (x, x + 0.7):
        for yy in (y, y + 0.7):
            box(g, blu, xx, yy, 0, xx + 0.07, yy + 0.07, p + 0.55)
    box(g, yel, x, y, p - 0.05, x + 0.77, y + 0.77, p)
    box(g, red, x, y, p + 0.45, x + 0.77, y + 0.77, p + 0.52)                    # дах-рамка
    prism_x(g, red, x - 0.05, x + 0.82, [(y - 0.05, p + 0.52), (y + 0.82, p + 0.52), (y + 0.385, p + 0.85)])
    box(g, yel, x, y + 0.7, p, x + 0.77, y + 0.77, p + 0.35)                     # бортик
    for i in range(5):                                                          # сходинки
        zz = p * (i + 1) / 6
        box(g, yel, x - 0.45 + 0.07 * i, y + 0.1, zz - 0.03, x - 0.3 + 0.07 * i, y + 0.67, zz)
    box(g, blu, x - 0.47, y + 0.07, 0, x - 0.42, y + 0.1, p - 0.1)
    box(g, blu, x - 0.47, y + 0.67, 0, x - 0.42, y + 0.7, p - 0.1)
    # скат уздовж +X від майданчика до підлоги
    x0, x1 = x + 0.77, x + 2.15
    z0, z1 = p - 0.02, 0.06
    t = 0.04
    prism_y(g, red, y + 0.12, y + 0.65, [(x0, z0 - t), (x1, z1 - t + 0.02), (x1, z1 + 0.02), (x0, z0)])
    for yy in (y + 0.08, y + 0.65):
        prism_y(g, yel, yy, yy + 0.04, [(x0, z0 - t), (x1, z1 - t + 0.02), (x1, z1 + 0.14), (x0, z0 + 0.12)])


def sandbox(g, x, y):
    wd = mat('Дерево світле', '#E0BE8C')
    s = 0.85
    for (a, b, c, d) in ((0, 0, s, 0.06), (0, s - 0.06, s, s), (0, 0, 0.06, s), (s - 0.06, 0, s, s)):
        box(g, wd, x + a, y + b, 0, x + c, y + d, 0.22)
    box(g, mat('Пісок (кінетичний)', '#F3D9A4'), x + 0.06, y + 0.06, 0, x + s - 0.06, y + s - 0.06, 0.15)
    box(g, mat('Пластик червоний', '#E53935'), x + 0.2, y + 0.25, 0.15, x + 0.32, y + 0.37, 0.27)
    box(g, mat('Пластик синій', '#1E88E5'), x + 0.5, y + 0.5, 0.15, x + 0.68, y + 0.58, 0.2)


def playhouse(g, x, y):
    wallc = mat('Будиночок стіни', '#FFF3C4')
    roof = mat('Будиночок дах', '#43A047')
    w, d, h = 1.2, 1.1, 1.0
    box(g, wallc, x, y, 0, x + 0.06, y + d, h)
    box(g, wallc, x + w - 0.06, y, 0, x + w, y + d, h)
    box(g, wallc, x, y + d - 0.06, 0, x + w, y + d, h)
    box(g, wallc, x, y, 0, x + 0.3, y + 0.06, h)                                  # фронт з дверима
    box(g, wallc, x + 0.75, y, 0, x + w, y + 0.06, h)
    box(g, wallc, x + 0.3, y, 0.8, x + 0.75, y + 0.06, h)
    box(g, M_GLASS, x + 0.85, y - 0.005, 0.45, x + 1.1, y + 0.065, 0.7)
    prism_y(g, roof, y - 0.1, y + d + 0.1, [(x - 0.1, h), (x + w + 0.1, h), (x + w / 2, h + 0.55)])
    box(g, mat('Пластик червоний', '#E53935'), x + 0.32, y - 0.02, 0, x + 0.73, y + 0.0, 0.78)


def swing(g, x, y):
    fr = mat('Пластик синій', '#1E88E5')
    hgt = 1.3
    for yy in (y, y + 1.2):
        prism_y(g, fr, yy, yy + 0.05, [(x - 0.05, 0), (x + 0.05, 0), (x + 0.5, hgt), (x + 0.4, hgt)])
        prism_y(g, fr, yy, yy + 0.05, [(x + 0.85, 0), (x + 0.95, 0), (x + 0.5, hgt), (x + 0.4, hgt)])
    cyl(g, fr, (x + 0.45, y, hgt - 0.03), 0.04, 1.25, 'y', 10)
    for yy in (y + 0.35, y + 0.85):
        cyl(g, M_DARK, (x + 0.45, yy, 0.4), 0.008, hgt - 0.43, 'z', 5, False)
    box(g, mat('Пластик червоний', '#E53935'), x + 0.3, y + 0.3, 0.37, x + 0.6, y + 0.9, 0.42)


def rack(g, dept):
    """Острівна стійка-вішало 1,50×0,80×1,50."""
    w, d, h = 1.5, 0.8, 1.5
    for xx in (0.05, w - 0.05):
        box(g, M_METAL, xx - 0.03, 0.0, 0.0, xx + 0.03, d, 0.04)                   # опори
        cyl(g, M_METAL, (xx, d / 2, 0.04), 0.02, h - 0.04, 'z', 8, False)
        for yy in (0.03, d - 0.03):
            cyl(g, M_DARK, (xx, yy, 0.0), 0.025, 0.03, 'z', 8)                   # коліщата
    cyl(g, M_METAL, (0.03, d / 2, h), 0.02, w - 0.06, 'x', 8)
    xx = 0.12
    while xx < w - 0.1:
        box(g, toy_mat(DEPTS[dept][2], 0.7), xx - 0.012, d / 2 - 0.2, h - 0.05 - random.uniform(0.55, 0.75),
            xx + 0.012, d / 2 + 0.2, h - 0.05, False)
        box(g, M_DARK, xx - 0.004, d / 2 - 0.002, h - 0.05, xx + 0.004, d / 2 + 0.002, h + 0.02, False)
        xx += random.uniform(0.06, 0.085)
    # табличка відділу
    box(g, dmat(dept), w / 2 - 0.25, d / 2 - 0.01, h + 0.05, w / 2 + 0.25, d / 2 + 0.01, h + 0.25)
    cyl(g, M_METAL, (w / 2, d / 2, h), 0.008, 0.05, 'z', 5, False)


def basket(g):
    """Сітчастий кошик-контейнер 1,0×1,0×1,0 з м'ячами."""
    s, h = 1.0, 1.0
    for xx in (0, s - 0.03):
        for yy in (0, s - 0.03):
            box(g, M_METAL, xx, yy, 0, xx + 0.03, yy + 0.03, h)
    for zz in (0.08, h - 0.03):
        box(g, M_METAL, 0, 0, zz, s, 0.02, zz + 0.03, False)
        box(g, M_METAL, 0, s - 0.02, zz, s, s, zz + 0.03, False)
        box(g, M_METAL, 0, 0, zz, 0.02, s, zz + 0.03, False)
        box(g, M_METAL, s - 0.02, 0, zz, s, s, zz + 0.03, False)
    for i in range(1, 8):                                                       # сітка
        t = i * s / 8
        box(g, M_METAL, t - 0.004, 0, 0.08, t + 0.004, 0.006, h, False)
        box(g, M_METAL, t - 0.004, s - 0.006, 0.08, t + 0.004, s, h, False)
        box(g, M_METAL, 0, t - 0.004, 0.08, 0.006, t + 0.004, h, False)
        box(g, M_METAL, s - 0.006, t - 0.004, 0.08, s, t + 0.004, h, False)
    for i in range(1, 6):
        zz = 0.08 + i * (h - 0.08) / 6
        for (a, b, c, d) in ((0, 0, s, 0.006), (0, s - 0.006, s, s), (0, 0, 0.006, s), (s - 0.006, 0, s, s)):
            box(g, M_METAL, a, b, zz - 0.004, c, d, zz + 0.004, False)
    box(g, M_METAL, 0.02, 0.02, 0.08, s - 0.02, s - 0.02, 0.1)
    # м'ячі — гірка, що виступає над краєм
    for layer in range(5):
        n = 4 if layer < 4 else 3
        r = 0.115
        for i in range(n):
            for j in range(n):
                off = (s - n * 2 * r) / 2
                cx = off + r + i * 2 * r + random.uniform(-0.01, 0.01)
                cy = off + r + j * 2 * r + random.uniform(-0.01, 0.01)
                cz = 0.1 + r + layer * 1.7 * r
                if layer == 4 and (i, j) == (1, 1):
                    cz += 0.08
                if cz + r > h + 0.12:
                    continue
                sphere(g, toy_mat('#FFD54F', 0.25), (cx, cy, cz), r, 10, 6)


def table(g, dept):
    """Демонстраційний стіл 1,6×0,8×0,8 (діти тестують товар)."""
    w, d, h = 1.6, 0.8, 0.8
    box(g, M_WOOD, 0, 0, h - 0.04, w, d, h)
    box(g, dmat(dept), -0.005, -0.005, h - 0.05, w + 0.005, d + 0.005, h - 0.03, False)
    for xx in (0.05, w - 0.1):
        for yy in (0.05, d - 0.1):
            box(g, M_SHELF, xx, yy, 0, xx + 0.05, yy + 0.05, h - 0.04)
    if dept == 'konstr':                                                        # «конструктор» з цеглинок
        for _ in range(26):
            bx = random.uniform(0.1, w - 0.3)
            by = random.uniform(0.1, d - 0.2)
            bz = h + random.choice([0, 0, 0, 0.05, 0.1])
            box(g, 'Товар ' + random.choice(TOY), bx, by, bz, bx + random.choice([0.08, 0.16]), by + 0.08, bz + 0.05)
        for i in range(4):                                                      # башта
            box(g, 'Товар ' + random.choice(TOY), 1.1, 0.3, h + i * 0.05, 1.26, 0.38, h + (i + 1) * 0.05)
    else:                                                                       # настільна гра
        box(g, mat('Ігрове поле', '#FFF59D'), 0.3, 0.15, h, 0.9, 0.65, h + 0.01)
        for i in range(6):
            cyl(g, 'Товар ' + TOY[i], (0.4 + i * 0.08, 0.3 + (i % 2) * 0.2, h + 0.01), 0.02, 0.05, 'z', 8)
        box(g, toy_mat(DEPTS[dept][2]), 1.05, 0.2, h, 1.45, 0.6, h + 0.07)
    # дитячі табурети
    for xx in (0.3, 0.8, 1.3):
        for yy in (-0.35, d + 0.1):
            cyl(g, 'Товар ' + random.choice(TOY), (xx, yy + 0.12, 0), 0.12, 0.35, 'z', 12)


def checkout(g):
    """Касовий бокс 1,80×0,90×1,00 (фронт до покупця — y=0)."""
    w, d, h = 1.8, 0.9, 1.0
    blk = mat('Касовий бокс корпус', '#ECEFF1')
    box(g, blk, 0, 0, 0.05, w, d, h - 0.04)
    box(g, M_DARK, 0.02, 0.02, 0, w - 0.02, d - 0.02, 0.05)
    box(g, M_WOOD, -0.02, -0.02, h - 0.04, w + 0.02, d + 0.02, h)
    box(g, dmat('service'), 0, -0.005, 0.6, w, 0.0, 0.75, False)
    box(g, mat('Логотип кольоровий', '#F0A01E'), 0, -0.006, 0.45, w, -0.001, 0.52, False)
    # монітор і термінал
    box(g, M_DARK, 1.2, 0.55, h, 1.3, 0.65, h + 0.25)
    box(g, M_DARK, 1.0, 0.5, h + 0.25, 1.5, 0.55, h + 0.55)
    box(g, M_SCREEN, 1.02, 0.6, h + 0.27, 1.48, 0.605, h + 0.53, False)
    box(g, M_DARK, 0.3, 0.15, h, 0.42, 0.33, h + 0.05)
    box(g, M_SCREEN, 0.32, 0.18, h + 0.05, 0.4, 0.28, h + 0.051, False)
    box(g, M_DARK, 0.9, 0.55, h, 1.6, 0.85, h + 0.03)                            # клавіатура/сканер
    # місце касира
    cyl(g, M_DARK, (0.9, d + 0.45, 0), 0.25, 0.04, 'z', 12)
    cyl(g, M_METAL, (0.9, d + 0.45, 0.04), 0.03, 0.5, 'z', 8)
    cyl(g, mat('Сидіння', '#455A64'), (0.9, d + 0.45, 0.54), 0.2, 0.08, 'z', 14)


def showcase(g):
    """Прикасова вітрина-прилавок 1,50×0,60×1,10."""
    w, d, h = 1.5, 0.6, 1.1
    box(g, M_SHELF, 0, 0, 0, w, d, 0.55)
    box(g, dmat('access'), 0, -0.005, 0.1, w, 0, 0.5, False)
    for xx in (0, w - 0.03):
        box(g, M_FRAME, xx, 0, 0.55, xx + 0.03, d, h)
    box(g, M_GLASS, 0.03, 0.0, 0.55, w - 0.03, 0.01, h - 0.02)
    box(g, M_GLASS, 0.03, d - 0.01, 0.55, w - 0.03, d, h - 0.02)
    box(g, M_GLASS, 0, 0, h - 0.02, w, d, h)
    box(g, M_SHELF, 0.03, 0.05, 0.8, w - 0.03, d - 0.05, 0.82)
    for zz in (0.55, 0.82):
        xx = 0.08
        while xx < w - 0.15:
            ww = random.uniform(0.06, 0.12)
            box(g, toy_mat('#AE7CC8', 0.5), xx, 0.15, zz, xx + ww, 0.15 + random.uniform(0.06, 0.25), zz + random.uniform(0.04, 0.15), False)
            xx += ww + 0.05


def fitting_room(g):
    """Примірочна кабіна 1,20×1,20×2,20 (вхід зі шторою — y=0)."""
    w, d, h = 1.2, 1.2, 2.2
    pan = mat('Примірочна панелі', '#FFFFFF')
    box(g, pan, 0, 0, 0, 0.04, d, h)
    box(g, pan, w - 0.04, 0, 0, w, d, h)
    box(g, pan, 0, d - 0.04, 0, w, d, h)
    box(g, dmat('service'), 0, -0.01, h - 0.15, w, 0.03, h)
    box(g, M_MIRROR, 0.25, d - 0.045, 0.3, 0.95, d - 0.04, 2.0, False)
    box(g, M_WOOD, 0.1, 0.4, 0.0, 0.45, 0.75, 0.45)                              # пуф
    cyl(g, M_METAL, (0.04, 0.06, h - 0.2), 0.01, w - 0.08, 'x', 6, False)
    # штора напіввідсунута (хвиляста)
    n = 10
    for i in range(n):
        xa = 0.05 + i * 0.07
        xb = xa + 0.07
        ya = 0.04 + (0.03 if i % 2 else -0.0)
        yb = 0.04 + (0.0 if i % 2 else 0.03)
        plate(g, M_CURTAIN, [(xa, ya, 0.05), (xb, yb, 0.05), (xb, yb, h - 0.2), (xa, ya, h - 0.2)])


def locker(g):
    """Шафа камери схову 1,25×0,60×1,90 (12 комірок)."""
    w, d, h = 1.25, 0.6, 1.9
    body = mat('Шафа камери схову', '#90A4AE')
    box(g, body, 0, 0.01, 0, w, d, h)
    for i in range(3):
        for j in range(4):
            x0 = 0.02 + i * (w - 0.04) / 3
            z0 = 0.05 + j * (h - 0.07) / 4
            box(g, mat('Дверцята комірки', '#B0BEC5'), x0 + 0.01, 0, z0 + 0.01,
                x0 + (w - 0.04) / 3 - 0.01, 0.01, z0 + (h - 0.07) / 4 - 0.01, False)
            box(g, M_DARK, x0 + 0.27, -0.015, z0 + 0.2, x0 + 0.3, 0.0, z0 + 0.3, False)
            box(g, mat('Номерок', '#F0A01E'), x0 + 0.05, -0.002, z0 + 0.32, x0 + 0.1, 0.0, z0 + 0.37, False)


def hanging_sign(g, dept, cx, cy, width, along='x', z=2.55):
    """Підвісна навігаційна табличка над зоною."""
    t = 0.03
    if along == 'x':
        box(g, dmat(dept), cx - width / 2, cy - t, z, cx + width / 2, cy + t, z + 0.4)
        box(g, M_SIGN, cx - width / 2 + 0.05, cy - t - 0.003, z + 0.05, cx + width / 2 - 0.05, cy - t, z + 0.35, False)
        box(g, M_SIGN, cx - width / 2 + 0.05, cy + t, z + 0.05, cx + width / 2 - 0.05, cy + t + 0.003, z + 0.35, False)
        for xx in (cx - width / 2 + 0.1, cx + width / 2 - 0.1):
            cyl(g, M_METAL, (xx, cy, z + 0.4), 0.004, H - z - 0.4, 'z', 4, False)
    else:
        box(g, dmat(dept), cx - t, cy - width / 2, z, cx + t, cy + width / 2, z + 0.4)
        for yy in (cy - width / 2 + 0.1, cy + width / 2 - 0.1):
            cyl(g, M_METAL, (cx, yy, z + 0.4), 0.004, H - z - 0.4, 'z', 4, False)


# ---------------------------------------------------------------- сцена
GROUPS = []
TEXTS = []          # (text, центр x, центр y, низ z, rot_deg, height, material, facing) — лише для Ruby


def new_group(name, tag):
    g = Group(name, tag)
    GROUPS.append(g)
    return g


def place(name, tag, x0, y0, w, d, facing, builder, *args, **kw):
    """Розміщує обладнання (локальний габарит w×d, фронт до -y) у прямокутнику плану
    з мінімальним кутом (x0, y0). facing — куди дивиться фронт: '-y', '+x', '+y', '-x'."""
    rot = {'-y': 0, '+x': 90, '+y': 180, '-x': 270}[facing]
    g = new_group(name, tag)
    r = Xf(0, 0, 0, rot)
    cs = [r((0, 0, 0)), r((w, 0, 0)), r((0, d, 0)), r((w, d, 0))]
    mx, my = min(c[0] for c in cs), min(c[1] for c in cs)
    g.xf = Xf(0, 0, 0, rot).then(Xf(x0 - mx, y0 - my, 0))
    builder(g, *args, **kw)
    return g


def build_shell():
    g = new_group('Підлога', 'Будівля')
    for i in range(int(L)):
        for j in range(int(W)):
            box_top = [(i, j, 0), (i + 1, j, 0), (i + 1, j + 1, 0), (i, j + 1, 0)]
            g.poly(M_FLOOR_A if (i + j) % 2 == 0 else M_FLOOR_B, box_top)
    # стяжка під підлогою (щоб було видно товщину)
    box(g, M_PLINTH, -WALL, -WALL, -0.25, L + WALL, W + WALL, -0.03, True)
    # килимок у зоні декомпресії
    box(g, M_MAT, 20.6, 0.05, 0, 22.9, 1.6, 0.012, False)
    box(g, M_MAT, 1.6, 0.05, 0, 3.9, 1.3, 0.012, False)

    g = new_group('Стіни', 'Будівля')
    box(g, M_WALL, -WALL, 0, 0, 0, W + WALL, H)                         # ліва
    box(g, M_WALL, L, 0, 0, L + WALL, W + WALL, H)                      # права
    box(g, M_WALL, 0, W, 0, L, W + WALL, H)                             # дальня
    # плінтуси
    box(g, M_PLINTH, 0, W - 0.02, 0, L, W, 0.08, False)
    box(g, M_PLINTH, 0, 0, 0, 0.02, W, 0.08, False)
    box(g, M_PLINTH, L - 0.02, 0, 0, L, W, 0.08, False)

    # фасад: вхід 20,5–23,0, вихід 1,5–4,0; між ними — вітрини
    g = new_group('Фасад з вітринами', 'Будівля')
    door_h = 2.5
    openings = [(1.5, 4.0), (20.5, 23.0)]
    solid = [(-WALL, 1.5), (4.0, 4.6), (20.0, 20.5), (23.0, L + WALL)]
    for a, b in solid:
        box(g, M_WALL_OUT, a, -WALL, 0, b, 0, H)
    for a, b in openings:
        box(g, M_WALL_OUT, a, -WALL, door_h, b, 0, H)                    # надпроріжжя
        box(g, M_FRAME, a, -WALL, door_h - 0.08, b, 0, door_h)
        for xx in (a, b - 0.06):
            box(g, M_FRAME, xx, -WALL, 0, xx + 0.06, 0, door_h)
        # розсувні стулки, відсунуті до країв
        box(g, M_GLASS, a + 0.06, -0.16, 0.02, a + 0.7, -0.14, door_h - 0.08)
        box(g, M_GLASS, b - 0.7, -0.16, 0.02, b - 0.06, -0.14, door_h - 0.08)
    # вітрини 4,6–20,0
    a, b = 4.6, 20.0
    box(g, M_WALL_OUT, a, -WALL, 0, b, 0, 0.45)                          # цоколь
    box(g, M_WALL_OUT, a, -WALL, 2.85, b, 0, H)                          # перемичка
    nseg = 10
    for i in range(nseg + 1):
        xx = a + (b - a) * i / nseg
        box(g, M_FRAME, xx - 0.04, -WALL, 0.45, xx + 0.04, -0.05, 2.85)
    box(g, M_FRAME, a, -WALL, 0.45, b, -0.05, 0.5)
    box(g, M_FRAME, a, -WALL, 2.8, b, -0.05, 2.85)
    for i in range(nseg):
        x0 = a + (b - a) * i / nseg + 0.04
        x1 = a + (b - a) * (i + 1) / nseg - 0.04
        box(g, M_GLASS, x0, -0.14, 0.5, x1, -0.12, 2.8)

    # вивіска на фасаді
    g = new_group('Вивіска «Дитячий світ»', 'Навігація')
    box(g, mat('Вивіска фон', '#F0A01E'), 8.5, -WALL - 0.12, 2.9, 16.5, -WALL, 3.25)
    TEXTS.append(('ДИТЯЧИЙ СВІТ', 12.5, -WALL - 0.125, 2.95, 0, 0.26, 'Вивіска', 'facade'))
    for xx, txt in ((1.6, 'ВИХІД'), (20.6, 'ВХІД')):
        box(g, mat('Табло вхід/вихід', '#2E7D32'), xx, -WALL - 0.06, 2.6, xx + 1.0, -WALL, 2.82)
        TEXTS.append((txt, xx + 0.5, -WALL - 0.065, 2.64, 0, 0.14, 'Вивіска', 'facade'))

    # благоустрій перед входом: тротуар, пандус, стоянка візків/велосипедів
    g = new_group('Майданчик перед входом', 'Благоустрій')
    box(g, M_PAVE, -1.0, -4.0, -0.2, L + 1.0, -WALL, -0.02)
    ramp = mat('Пандус', '#A9A39A')
    prism_x(g, ramp, 19.8, 23.7, [(-WALL - 1.6, -0.02), (-WALL, -0.02), (-WALL, 0.0)])
    for i in range(5):                                                   # велосипедні дуги
        xx = 5.0 + i * 0.7
        for yy in (-2.6, -1.9):
            cyl(g, M_STROLLER_PARK, (xx, yy, -0.02), 0.025, 0.75, 'z', 6, False)
        cyl(g, M_STROLLER_PARK, (xx, -2.6, 0.73), 0.025, 0.7, 'y', 6, False)
    for xx in (11.0, 14.0, 17.0):                                        # вазони
        cyl(g, mat('Вазон', '#78909C'), (xx, -2.0, -0.02), 0.35, 0.5, 'z', 14)
        sphere(g, mat('Рослини', '#558B2F'), (xx, -2.0, 0.6), 0.38, 10, 6)


def build_equipment():
    T = 'Обладнання'
    # 1. Пристінні стелажі-гірки: дальня стіна (20 шт.) — зліва направо
    back = (['access'] * 3 + ['books'] * 3 + ['military'] * 3 + ['transport'] * 3 +
            ['balls'] * 3 + ['sport'] * 5)
    kinds = {'access': 'boxes', 'books': 'books', 'military': 'military',
             'transport': 'transport', 'balls': 'balls', 'sport': 'boxes',
             'dollwear': 'boxes', 'rooms': 'rooms', 'dolls': 'dolls'}
    n = 1
    for i, dep in enumerate(back):
        place(f'1.{n} Стелаж-гірка — {DEPTS[dep][0]}', T, i * 1.25, W - 0.6, 1.25, 0.6, '-y',
              gorka, dep, kinds[dep])
        n += 1
    # права стіна (9 шт.) від дальньої стіни до входу
    right = ['dollwear'] * 2 + ['rooms'] * 3 + ['dolls'] * 4
    for j, dep in enumerate(right):
        y1 = W - 0.6 - j * 1.25
        place(f'1.{n} Стелаж-гірка — {DEPTS[dep][0]}', T, L - 0.6, y1 - 1.25, 1.25, 0.6, '-x',
              gorka, dep, kinds[dep])
        n += 1
    # 2. Пристінна система для одягу — ліва стіна (9 шт.): дівчата 5 (дальня частина), хлопчики 4
    left = ['girls'] * 5 + ['boys'] * 4
    for j, dep in enumerate(left):
        y1 = W - 0.6 - j * 1.25
        place(f'2.{j + 1} Пристінна система для одягу — {DEPTS[dep][0]}', T, 0, y1 - 1.25, 1.25, 0.6,
              '+x', clothes_wall, dep)
    # 3. Пристінні низькі стелажі — фасадна стіна, канцтовари (6 шт.)
    for i in range(6):
        place(f'3.{i + 1} Низький стелаж — Канцтовари', T, 9.5 + i * 1.25, 0, 1.25, 0.6, '+y', low_shelf)
    # 4. Острівні гондоли: дальній ряд — конструктори, ближній — розвиваючі ігри
    for row, (dep, kind, y0) in enumerate((('konstr', 'konstr', W - 4.42), ('games', 'games', W - 7.2))):
        for i in range(8):
            place(f'4.{row * 8 + i + 1} Острівна гондола — {DEPTS[dep][0]}', T, 8.0 + i * 1.25, y0,
                  1.25, 1.2, '-y', gondola, dep, kind, end_left=(i == 0), end_right=(i == 7))
    # 5. Демонстраційні подіуми 3×2 (передня «холодна» зона)
    pods = [(5.75, 'play', 'slide'), (9.25, 'play', 'house'), (12.75, 'cars', 'cars1'), (16.25, 'cars', 'cars2')]
    for i, (x0, dep, cont) in enumerate(pods):
        place(f'5.{i + 1} Подіум — {DEPTS[dep][0]}', T, x0, W - 11.12, 3.0, 2.0, '-y', podium, dep, cont)
    # 6. Острівні стійки-вішала (одяг)
    racks = [(2.4, W - 3.62, 'girls'), (5.0, W - 3.62, 'girls'), (5.0, W - 6.02, 'girls'),
             (2.4, W - 6.02, 'boys'), (2.4, W - 8.63, 'boys'), (5.0, W - 8.63, 'boys')]
    for i, (x0, y0, dep) in enumerate(racks):
        place(f'6.{i + 1} Стійка-вішало — {DEPTS[dep][0]}', T, x0, y0, 1.5, 0.8, '-y', rack, dep)
    # 7. Сітчасті кошики з м'ячами
    for i, y0 in enumerate((W - 5.01, W - 9.03)):
        place(f"7.{i + 1} Кошик-контейнер — М'ячі", T, 20.98, y0, 1.0, 1.0, '-y', basket)
    # 8. Демонстраційні столи на торцях рядів гондол
    for i, (y0, dep) in enumerate(((W - 4.23, 'konstr'), (W - 7.02, 'games'))):
        place(f'8.{i + 1} Демонстраційний стіл — {DEPTS[dep][0]}', T, 18.6, y0, 1.6, 0.8, '-y', table, dep)
    # 9. Касові бокси та 10. прикасові вітрини
    for i, x0 in enumerate((5.0, 7.8)):     # праворуч від виходу (1,5–4,0 м), щоб не перекривати його
        place(f'9.{i + 1} Касовий бокс', T, x0, 1.98, 1.8, 0.9, '+y', checkout)
        place(f'10.{i + 1} Прикасова вітрина — Аксесуари', T, x0 + 0.15, 3.08, 1.5, 0.6, '+y', showcase)
    # 11. Примірочні кабіни
    for i, x0 in enumerate((0.0, 1.2)):
        place(f'11.{i + 1} Примірочна кабіна', T, x0, 2.8, 1.2, 1.2, '-y', fitting_room)
    # 12. Шафа камери схову біля входу
    place('12.1 Шафа камери схову', T, L - 0.6, 1.0, 1.25, 0.6, '-x', locker)


def build_navigation():
    g = new_group('Підвісні навігаційні таблички', 'Навігація')
    hanging_sign(g, 'konstr', 13.0, W - 3.8, 2.4)
    hanging_sign(g, 'games', 13.0, W - 6.6, 2.4)
    hanging_sign(g, 'play', 9.0, W - 10.1, 2.4)
    hanging_sign(g, 'cars', 16.0, W - 10.1, 2.4)
    hanging_sign(g, 'girls', 4.0, W - 4.5, 2.0)
    hanging_sign(g, 'boys', 4.0, W - 7.4, 2.0)
    hanging_sign(g, 'service', 7.3, 2.4, 2.0, z=2.6)
    # написи на підвісних табличках і фризах (тільки в Ruby-версії)
    TEXTS.append(('КОНСТРУКТОРИ', 13.0, W - 3.8 - 0.035, 2.66, 0, 0.17, 'Відділ — Конструктори', 'y-'))
    TEXTS.append(('РОЗВИВАЮЧІ ІГРИ', 13.0, W - 6.6 - 0.035, 2.66, 0, 0.15, 'Відділ — Розвиваючі дедуктивні ігри', 'y-'))
    TEXTS.append(('ІГРОВІ МАЙДАНЧИКИ', 9.0, W - 10.1 - 0.035, 2.67, 0, 0.13, 'Відділ — Обладнання для ігрових майданчиків', 'y-'))
    TEXTS.append(('ЕЛЕКТРОМОБІЛІ', 16.0, W - 10.1 - 0.035, 2.67, 0, 0.15, 'Відділ — Електромобілі, педальні машини', 'y-'))
    TEXTS.append(('ОДЯГ ДЛЯ ДІВЧАТ', 4.0, W - 4.5 - 0.035, 2.67, 0, 0.13, 'Відділ — Одяг для дівчат', 'y-'))
    TEXTS.append(('ОДЯГ ДЛЯ ХЛОПЧИКІВ', 4.0, W - 7.4 - 0.035, 2.67, 0, 0.12, 'Відділ — Одяг для хлопчиків', 'y-'))
    TEXTS.append(('КАСИ', 7.3, 2.4 - 0.035, 2.72, 0, 0.18, 'Відділ — Касова зона, примірочні, камера схову', 'y-'))
    # фризи над дальньою стіною (на висоті 2,32–2,62 м)
    spans = [('АКСЕСУАРИ', 0, 3), ('КНИГИ', 3, 6), ('ВОЄННА ТЕХНІКА', 6, 9),
             ('ТРАНСПОРТ', 9, 12), ("М'ЯЧІ", 12, 15), ('СПОРТ', 15, 20)]
    for txt, a, b in spans:
        cx = (a + b) * 1.25 / 2
        TEXTS.append((txt, cx, W - 0.125, 2.39, 0, 0.16, 'Вивіска', 'y-'))
    for txt, j0, j1 in (('ОДЯГ ДЛЯ ЛЯЛЬОК', 0, 2), ('КІМНАТИ ДЛЯ ЛЯЛЬОК', 2, 5), ('ЛЯЛЬКИ', 5, 9)):
        cy = W - 0.6 - (j0 + j1) * 1.25 / 2
        TEXTS.append((txt, L - 0.125, cy, 2.39, 0, 0.14, 'Вивіска', 'x-'))
    for txt, j0, j1 in (('ОДЯГ ДЛЯ ДІВЧАТ', 0, 5), ('ОДЯГ ДЛЯ ХЛОПЧИКІВ', 5, 9)):
        cy = W - 0.6 - (j0 + j1) * 1.25 / 2
        TEXTS.append((txt, 0.125, cy, 2.39, 0, 0.14, 'Вивіска', 'x+'))


# ---------------------------------------------------------------- експорт
def tri(pts):
    return [(pts[0], pts[i], pts[i + 1]) for i in range(1, len(pts) - 1)]


def fnormal(pts):
    nx = ny = nz = 0.0
    n = len(pts)
    for i in range(n):
        x1, y1, z1 = pts[i]
        x2, y2, z2 = pts[(i + 1) % n]
        nx += (y1 - y2) * (z1 + z2)
        ny += (z1 - z2) * (x1 + x2)
        nz += (x1 - x2) * (y1 + y2)
    l = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
    return (nx / l, ny / l, nz / l)


def mat_id(name):
    return 'mat%03d' % list(MATERIALS).index(name)


def export_dae(path):
    out = []
    w = out.append
    w('<?xml version="1.0" encoding="utf-8"?>\n')
    w('<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">\n')
    w('<asset><contributor><authoring_tool>build_model.py — ТОВ «Дитячий світ»</authoring_tool></contributor>'
      '<unit name="meter" meter="1"/><up_axis>Z_UP</up_axis></asset>\n')
    used = sorted({m for g in GROUPS for (m, _s) in g.parts}, key=lambda m: list(MATERIALS).index(m))
    w('<library_effects>\n')
    for m in used:
        c, a = MATERIALS[m]
        r, gg, b = hx(c)
        tr = ''
        if a < 1:
            tr = f'<transparent opaque="A_ONE"><color>1 1 1 {a:.3f}</color></transparent><transparency><float>1</float></transparency>'
        w(f'<effect id="{mat_id(m)}-fx"><profile_COMMON><technique sid="common"><lambert>'
          f'<diffuse><color>{r:.4f} {gg:.4f} {b:.4f} 1</color></diffuse>{tr}</lambert></technique></profile_COMMON></effect>\n')
    w('</library_effects>\n<library_materials>\n')
    for m in used:
        nm = m.replace('&', 'and').replace('"', "'").replace('<', '').replace('>', '')
        w(f'<material id="{mat_id(m)}" name="{nm}"><instance_effect url="#{mat_id(m)}-fx"/></material>\n')
    w('</library_materials>\n<library_geometries>\n')
    for gi, g in enumerate(GROUPS):
        pos, nor, prims = [], [], []
        for (m, smooth), polys in g.parts.items():
            idx = []
            for pts, ns in polys:
                fn = fnormal(pts)
                base = len(pos)
                pos.extend(pts)
                if ns is None:
                    nor.extend([fn] * len(pts))
                else:
                    nor.extend(ns)
                for i in range(1, len(pts) - 1):
                    idx.extend((base, base + i, base + i + 1))
            prims.append((m, idx))
        gid = f'geom{gi}'
        w(f'<geometry id="{gid}"><mesh>\n')
        w(f'<source id="{gid}-p"><float_array id="{gid}-pa" count="{len(pos) * 3}">')
        w(' '.join('%.4f %.4f %.4f' % p for p in pos))
        w(f'</float_array><technique_common><accessor source="#{gid}-pa" count="{len(pos)}" stride="3">'
          '<param name="X" type="float"/><param name="Y" type="float"/><param name="Z" type="float"/></accessor></technique_common></source>\n')
        w(f'<source id="{gid}-n"><float_array id="{gid}-na" count="{len(nor) * 3}">')
        w(' '.join('%.3f %.3f %.3f' % n for n in nor))
        w(f'</float_array><technique_common><accessor source="#{gid}-na" count="{len(nor)}" stride="3">'
          '<param name="X" type="float"/><param name="Y" type="float"/><param name="Z" type="float"/></accessor></technique_common></source>\n')
        w(f'<vertices id="{gid}-v"><input semantic="POSITION" source="#{gid}-p"/></vertices>\n')
        for m, idx in prims:
            w(f'<triangles material="{mat_id(m)}" count="{len(idx) // 3}">'
              f'<input semantic="VERTEX" source="#{gid}-v" offset="0"/>'
              f'<input semantic="NORMAL" source="#{gid}-n" offset="1"/><p>')
            w(' '.join(f'{i} {i}' for i in idx))
            w('</p></triangles>\n')
        w('</mesh></geometry>\n')
    w('</library_geometries>\n<library_visual_scenes><visual_scene id="scene" name="Дитячий світ">\n')
    tags = []
    for g in GROUPS:
        if g.tag not in tags:
            tags.append(g.tag)
    for ti, tag in enumerate(tags):
        w(f'<node id="tag{ti}" name="{tag}">\n')
        for gi, g in enumerate(GROUPS):
            if g.tag != tag:
                continue
            nm = g.name.replace('&', 'and').replace('"', "'")
            w(f'<node id="node{gi}" name="{nm}"><instance_geometry url="#geom{gi}"><bind_material><technique_common>')
            for (m, _s) in g.parts:
                w(f'<instance_material symbol="{mat_id(m)}" target="#{mat_id(m)}"/>')
            w('</technique_common></bind_material></instance_geometry></node>\n')
        w('</node>\n')
    w('</visual_scene></library_visual_scenes>\n<scene><instance_visual_scene url="#scene"/></scene>\n</COLLADA>\n')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(''.join(out))


def rb_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


def export_rb(path):
    o = []
    w = o.append
    w('# encoding: UTF-8\n')
    w('# 3D-модель магазину ТОВ «Дитячий світ» (курсова робота, розділ 4).\n')
    w('# Запуск у SketchUp: Вікно → Консоль Ruby →  load "шлях/до/dytiachyi_svit.rb"\n')
    w('# або Розширення → (Extension Manager не потрібен) — просто load у консолі.\n')
    w('# Згенеровано build_model.py; одиниці — метри.\n\n')
    w('module DytiachyiSvit\n  M = 39.37007874015748\n')
    w('  MATS = {\n')
    used = sorted({m for g in GROUPS for (m, _s) in g.parts} | {t[6] for t in TEXTS},
                  key=lambda m: list(MATERIALS).index(m))
    for m in used:
        c, a = MATERIALS[m]
        w(f'    {rb_str(m)} => [{rb_str(c)}, {a}],\n')
    w('  }\n\n')
    w('''  def self.mats(model)
    @m = {}
    MATS.each do |name, (col, a)|
      mt = model.materials[name] || model.materials.add(name)
      mt.color = Sketchup::Color.new(col)
      mt.alpha = a if a < 1.0
      @m[name] = mt
    end
  end

  def self.tag(model, name)
    model.layers[name] || model.layers.add(name)
  end

  # parts: [[material, smooth, [[x,y,z, x,y,z, ...], ...]], ...]
  def self.grp(model, name, tagname, parts)
    g = model.active_entities.add_group
    g.name = name
    g.layer = tag(model, tagname)
    parts.each do |mname, smooth, polys|
      mesh = Geom::PolygonMesh.new
      polys.each do |flat|
        pts = []
        (0...flat.length).step(3) { |i| pts << Geom::Point3d.new(flat[i] * M, flat[i + 1] * M, flat[i + 2] * M) }
        mesh.add_polygon(pts) rescue nil
      end
      flags = smooth ? 12 : 0
      g.entities.fill_from_mesh(mesh, true, flags, @m[mname], @m[mname])
    end
    g
  end

  def self.text(model, str, x, y, z, h, mname, facing)
    g = model.active_entities.add_group
    g.name = 'Напис: ' + str
    g.layer = tag(model, 'Навігація')
    g.entities.add_3d_text(str, TextAlignLeft, 'Arial', true, false, h * M, 0.0, 0.0, true, 0.01 * M)
    g.entities.grep(Sketchup::Face).each { |f| f.material = @m[mname]; f.back_material = @m[mname] }
    bw = g.entities.to_a.inject(Geom::BoundingBox.new) { |b, e| b.add(e.bounds) }.width
    g.entities.transform_entities(Geom::Transformation.translation([-bw / 2.0, 0, 0]), g.entities.to_a)
    rx = Geom::Transformation.rotation(ORIGIN, X_AXIS, 90.degrees)
    case facing
    when 'facade', 'y-' then r = rx
    when 'x-' then r = Geom::Transformation.rotation(ORIGIN, Z_AXIS, -90.degrees) * rx
    when 'x+' then r = Geom::Transformation.rotation(ORIGIN, Z_AXIS, 90.degrees) * rx
    end
    g.transform!(Geom::Transformation.translation([x * M, y * M, z * M]) * r)
  end

  def self.scene(model, name, eye, target)
    cam = Sketchup::Camera.new(eye.map { |v| v * M }, target.map { |v| v * M }, Z_AXIS)
    cam.fov = 50
    model.active_view.camera = cam
    pg = model.pages.add(name)
    pg.update
  end

  def self.build
    model = Sketchup.active_model
    model.start_operation('Дитячий світ — 3D-модель', true)
    begin
      model.options['UnitsOptions']['LengthUnit'] = 4  # метри
    rescue StandardError
    end
    mats(model)
''')
    for g in GROUPS:
        w(f'    grp(model, {rb_str(g.name)}, {rb_str(g.tag)}, [\n')
        for (m, smooth), polys in g.parts.items():
            w(f'      [{rb_str(m)}, {"true" if smooth else "false"}, [\n')
            for pts, _n in polys:
                w('        [' + ','.join('%.4f,%.4f,%.4f' % p for p in pts) + '],\n')
            w('      ]],\n')
        w('    ])\n')
    for (t, x, y, z, _r, h, m, facing) in TEXTS:
        w(f'    text(model, {rb_str(t)}, {x:.3f}, {y:.3f}, {z:.3f}, {h}, {rb_str(m)}, {rb_str(facing)})\n')
    w('''    scene(model, 'Загальний вигляд', [-6.0, -12.0, 17.0], [12.5, 8.5, 0.0])
    scene(model, 'Вигляд від входу', [21.8, 0.6, 1.65], [12.0, 12.0, 0.6])
    scene(model, 'План зверху', [12.5, 8.0, 38.0], [12.5, 8.0, 0.0])
    scene(model, 'Відділ одягу та каси', [9.5, 2.5, 2.2], [1.5, 10.0, 0.6])
    scene(model, 'Дальня стіна', [16.0, 7.6, 1.7], [8.0, 16.0, 1.0])
    scene(model, 'Фасад', [12.5, -14.0, 3.0], [12.5, 4.0, 1.2])
    model.pages.selected_page = model.pages[0]
    model.commit_operation
    model.active_view.zoom_extents if model.pages.empty?
    puts 'Дитячий світ: модель побудовано.'
  rescue StandardError => e
    model.abort_operation
    raise e
  end
end

DytiachyiSvit.build
''')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(''.join(o))


def main():
    build_shell()
    build_equipment()
    build_navigation()
    nf = sum(g.nfaces() for g in GROUPS)
    eq = [g for g in GROUPS if g.tag == 'Обладнання']
    print(f'Груп: {len(GROUPS)}, одиниць обладнання: {len(eq)}, полігонів: {nf}')
    export_dae(os.path.join(HERE, 'dytiachyi_svit.dae'))
    export_rb(os.path.join(HERE, 'dytiachyi_svit.rb'))


if __name__ == '__main__':
    main()
