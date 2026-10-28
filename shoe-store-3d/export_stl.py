#!/usr/bin/env python3
"""Експорт моделі «Взуття» у бінарний STL (міліметри) — для імпорту в безкоштовну онлайн-версію SketchUp."""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
import importlib.util                          # noqa: E402
_spec = importlib.util.spec_from_file_location('shoe_model', os.path.join(HERE, 'build_model.py'))
shoe = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(shoe)

shoe.main()                                    # будує модель (і заодно оновлює .rb/.dae — результат той самий)
bm = shoe.bm
tris = []
for g in bm.GROUPS:
    for (_m, _s), polys in g.parts.items():
        for pts, _n in polys:
            for i in range(1, len(pts) - 1):
                tris.append((pts[0], pts[i], pts[i + 1]))


def normal(a, b, c):
    ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    l = (nx * nx + ny * ny + nz * nz) ** 0.5 or 1.0
    return nx / l, ny / l, nz / l


out = os.path.join(HERE, 'vzuttia.stl')
with open(out, 'wb') as f:
    f.write(b'Vzuttia shoe store model, units: millimetres'.ljust(80, b' '))
    f.write(struct.pack('<I', len(tris)))
    for a, b, c in tris:
        f.write(struct.pack('<3f', *normal(a, b, c)))
        for p in (a, b, c):
            f.write(struct.pack('<3f', p[0] * 1000, p[1] * 1000, p[2] * 1000))
        f.write(b'\0\0')
print(out, len(tris), 'трикутників')
