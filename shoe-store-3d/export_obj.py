#!/usr/bin/env python3
"""Експорт моделі «Взуття» у OBJ + MTL (метри, вісь Z угору) — відкривається в будь-якій версії SketchUp, Blender, 3D Viewer."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
import importlib.util
_spec = importlib.util.spec_from_file_location('shoe_model', os.path.join(HERE, 'build_model.py'))
shoe = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(shoe)
shoe.main()
bm = shoe.bm

out_dir = sys.argv[1] if len(sys.argv) > 1 else HERE
base = sys.argv[2] if len(sys.argv) > 2 else 'vzuttia'
obj_p, mtl_p = os.path.join(out_dir, base + '.obj'), os.path.join(out_dir, base + '.mtl')
with open(mtl_p, 'w', encoding='utf8') as f:
    for name, (col, a) in bm.MATERIALS.items():
        r, g, b = bm.hx(col)
        f.write(f'newmtl {bm.mat_id(name)}\nKd {r:.4f} {g:.4f} {b:.4f}\nKa 0 0 0\nd {a:.3f}\nillum 1\n\n')
vi = 0
with open(obj_p, 'w', encoding='utf8') as f:
    f.write(f'# Vzuttia shoe store model, units: metres\nmtllib {base}.mtl\n')
    for gi, g in enumerate(bm.GROUPS):
        gname = ''.join(c if c.isascii() and (c.isalnum() or c in '_-') else '_' for c in getattr(g, 'name', '') or '')
        f.write(f'g grp{gi:04d}_{gname}\n')
        for (m, _s), polys in g.parts.items():
            f.write(f'usemtl {bm.mat_id(m)}\n')
            for pts, _n in polys:
                for p in pts:
                    f.write(f'v {p[0]:.4f} {p[1]:.4f} {p[2]:.4f}\n')
                f.write('f ' + ' '.join(str(vi + 1 + k) for k in range(len(pts))) + '\n')
                vi += len(pts)
print(obj_p, vi, 'вершин')
