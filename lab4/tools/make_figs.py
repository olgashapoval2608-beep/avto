"""Генерує HTML-рисунки (SQL-код + реальний результат запиту з MySQL/MariaDB)."""
import html, json, re, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "html"
OUT.mkdir(exist_ok=True)

KW = r"\b(CREATE|TABLE|SCHEMA|DEFAULT|CHARACTER|SET|COLLATE|INT|UNSIGNED|NOT|NULL|AUTO_INCREMENT|VARCHAR|SMALLINT|DECIMAL|PRIMARY|KEY|FOREIGN|REFERENCES|INSERT|INTO|VALUES|SELECT|FROM|WHERE|AND|OR|IN|ORDER|BY|ASC|DESC|AS|CONCAT|USE)\b"

def hl(sql):
    out = []
    for line in sql.split("\n"):
        parts = re.split(r"('(?:[^']*)')", line)
        seg = []
        for p in parts:
            if p.startswith("'") and p.endswith("'") and len(p) >= 2:
                seg.append(f'<span class="s">{html.escape(p)}</span>')
            else:
                e = html.escape(p)
                e = re.sub(r"\b(\d+(?:\.\d+)?)\b", r'<span class="n">\1</span>', e)
                e = re.sub(KW, r'<span class="k">\1</span>', e)
                seg.append(e)
        out.append("".join(seg))
    return out

def run(sql):
    r = subprocess.run(["mariadb", "--default-character-set=utf8mb4", "--batch", "library4"],
                       input=sql, capture_output=True, text=True, check=True)
    lines = [l for l in r.stdout.split("\n") if l]
    if not lines:
        return None
    return [l.split("\t") for l in lines]

CSS = """
body{margin:0;background:#fff;font-family:'DejaVu Sans',sans-serif;}
.win{width:WIDTHpx;border:1px solid #9aa4b1;}
.bar{background:#e9edf2;border-bottom:1px solid #c5ccd5;font-size:12px;padding:4px 8px;color:#333}
.code{display:flex;font-family:'DejaVu Sans Mono',monospace;font-size:13px;line-height:19px;background:#fff;padding:6px 0}
.ln{color:#8b96a3;text-align:right;padding:0 8px 0 6px;border-right:1px solid #e1e5ea;user-select:none;white-space:pre}
.src{padding-left:10px;white-space:pre;color:#1d1d1d}
.k{color:#1f5fbf;font-weight:bold}.s{color:#2e8b3e}.n{color:#c46a00}
.out{border-top:1px solid #c5ccd5}
table{border-collapse:collapse;font-size:12.5px;margin:0}
th{background:#eef1f5;border:1px solid #c9d0d8;padding:3px 10px;text-align:left;font-weight:normal;color:#222}
td{border:1px solid #dde2e8;padding:3px 10px;white-space:nowrap}
tr:nth-child(even) td{background:#f6f8fb}
.msg{font-size:12px;padding:4px 8px;color:#2b6b2b;background:#f3f8f3;border-top:1px solid #c5ccd5}
"""

def page(name, title, sql, result=None, msg=None, width=900):
    lines = hl(sql.strip())
    ln = "\n".join(str(i+1) for i in range(len(lines)))
    body = f'<div class="win"><div class="bar">{html.escape(title)}</div>'
    body += f'<div class="code"><div class="ln">{ln}</div><div class="src">' + "\n".join(lines) + '</div></div>'
    if result:
        head, rows = result[0], result[1:]
        t = "<table><tr>" + "".join(f"<th>{html.escape(h)}</th>" for h in head) + "</tr>"
        for r in rows:
            t += "<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>"
        t += "</table>"
        body += f'<div class="bar">Result Grid</div><div class="out">{t}</div>'
        body += f'<div class="msg">{len(rows)} row(s) returned</div>'
    elif msg:
        body += f'<div class="msg">{html.escape(msg)}</div>'
    body += "</div>"
    doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS.replace("WIDTH", str(width))}</style></head><body>{body}</body></html>'
    (OUT / f"{name}.html").write_text(doc, encoding="utf-8")

def sec(text, start, end=None):
    """Повертає фрагмент SQL-файлу між маркерами."""
    i = text.index(start)
    j = text.index(end, i + len(start)) if end else len(text)
    return text[i:j].strip()

ddl = (ROOT / "library_lab4.sql").read_text(encoding="utf-8")
q = (ROOT / "queries_lab4.sql").read_text(encoding="utf-8")

def strip_comments(s):
    return "\n".join(l for l in s.split("\n") if not l.strip().startswith("--")).strip()

figs = []
def add(name, title, sql, query=None, msg=None, width=900):
    res = run(query) if query else None
    page(name, title, sql, res, msg, width)
    figs.append(name)

add("f01_schema", "SQL File 1 — створення схеми",
    "CREATE SCHEMA `library4` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
    msg="CREATE SCHEMA `library4` ... — 1 row(s) affected", width=820)
for n, (a, b) in enumerate([("CREATE TABLE author (", "-- 3."), ("CREATE TABLE publisher (", "-- 4."),
                            ("CREATE TABLE bookstore (", "-- 5."), ("CREATE TABLE book (", "-- 6.")], 2):
    s = sec(ddl, a, b)
    tname = a.split()[-2]
    add(f"f0{n}_{tname}", f"SQL File {n} — таблиця {tname}", s, msg=f"CREATE TABLE {tname} ... — 0 row(s) affected", width=600)
for n, t in enumerate(["author", "publisher", "bookstore", "book"], 6):
    s = sec(ddl, f"INSERT INTO `library4`.`{t}`", ");") + ");"
    add(f"f{n:02d}_ins_{t}", f"Заповнення таблиці {t} та перегляд (Select Rows)", s,
        query=f"SELECT * FROM {t};", width=900)

qs = [("q2", "-- Q2.", "-- Q3."), ("q3", "-- Q3.", "-- Q4."), ("q4", "-- Q4.", "-- Q5."),
      ("q5", "-- Q5.", "-- Q6."), ("q6", "-- Q6.", "-- Q7."), ("q7", "-- Q7.", "-- Q8."),
      ("q8", "-- Q8.", "-- Q9."), ("q9", "-- Q9.", "-- Самостійно 1."),
      ("s1", "-- Самостійно 1.", "-- Самостійно 2."), ("s2", "-- Самостійно 2.", "-- Підсумковий"),
      ("fin", "-- Підсумковий", None)]
for name, a, b in qs:
    s = strip_comments(sec(q, a, b))
    add(name, "Query", s, query=s, width=1100 if name in ("q3", "q4", "fin") else 900)

json.dump(figs, open(OUT / "list.json", "w"))
print(figs)
