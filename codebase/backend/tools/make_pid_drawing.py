"""Generate the Boiler Feed Water P&ID (PID-BFW-04) demo drawing.

Reproducible generator for the Prahari demo corpus. Produces a vector PDF and a
200 dpi PNG render of a readable, ISA-style P&ID covering the BFW pump system.

Run:
    C:/Projects/ET1/codebase/backend/.venv/Scripts/python.exe \
        C:/Projects/ET1/codebase/backend/tools/make_pid_drawing.py
"""

from __future__ import annotations

import math
import os

import fitz  # PyMuPDF

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "corpus", "drawings",
)
PDF_PATH = os.path.join(OUT_DIR, "PID-BFW-04_P-101B.pdf")
PNG_PATH = os.path.join(OUT_DIR, "PID-BFW-04_P-101B.png")

PAGE_W, PAGE_H = 1190.0, 842.0

BLACK = (0, 0, 0)
GREY = (0.45, 0.45, 0.45)
WHITE = (1, 1, 1)

FONT = "helv"
FONT_B = "hebo"

LW = 1.1          # process line width
LW_THIN = 0.7     # symbol / secondary line width


# --------------------------------------------------------------------------- #
# primitives
# --------------------------------------------------------------------------- #
def text(page, x, y, s, size=9, bold=False, color=BLACK, anchor="left"):
    """Insert text; anchor is left | center | right (horizontal only)."""
    font = FONT_B if bold else FONT
    w = fitz.get_text_length(s, fontname=font, fontsize=size)
    if anchor == "center":
        x -= w / 2.0
    elif anchor == "right":
        x -= w
    page.insert_text((x, y), s, fontname=font, fontsize=size, color=color)
    return w


def line(page, p0, p1, width=LW, color=BLACK, dashes=None):
    page.draw_line(fitz.Point(*p0), fitz.Point(*p1),
                   color=color, width=width, dashes=dashes)


def polyline(page, pts, width=LW, color=BLACK, dashes=None):
    for a, b in zip(pts, pts[1:]):
        line(page, a, b, width=width, color=color, dashes=dashes)


def arrow(page, at, direction, size=9, color=BLACK):
    """Filled arrowhead with its tip at `at`, pointing along `direction`."""
    dx, dy = direction
    n = math.hypot(dx, dy) or 1.0
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    tip = fitz.Point(*at)
    base = fitz.Point(at[0] - ux * size, at[1] - uy * size)
    half = size * 0.42
    a = fitz.Point(base.x + px * half, base.y + py * half)
    b = fitz.Point(base.x - px * half, base.y - py * half)
    shape = page.new_shape()
    shape.draw_polyline([tip, a, b, tip])
    shape.finish(color=color, fill=color, width=0.5)
    shape.commit()


def bubble(page, cx, cy, tag, r=21, leader_from=None):
    """ISA instrument bubble: circle with two lines of tag text inside."""
    if leader_from is not None:
        line(page, leader_from, (cx, cy), width=LW_THIN, dashes="[2 2] 0")
    page.draw_circle(fitz.Point(cx, cy), r, color=BLACK, fill=WHITE, width=1.0)
    if "-" in tag:
        top, bot = tag.split("-", 1)
    else:
        top, bot = tag, ""
    text(page, cx, cy - 1, top, size=9, bold=True, anchor="center")
    text(page, cx, cy + 10, bot, size=9, bold=True, anchor="center")


def gate_valve(page, cx, cy, size=9, vertical=False):
    """Two opposed triangles (bowtie) = valve body."""
    s = page.new_shape()
    if not vertical:
        pts_l = [fitz.Point(cx - size, cy - size * 0.72),
                 fitz.Point(cx - size, cy + size * 0.72),
                 fitz.Point(cx, cy)]
        pts_r = [fitz.Point(cx + size, cy - size * 0.72),
                 fitz.Point(cx + size, cy + size * 0.72),
                 fitz.Point(cx, cy)]
    else:
        pts_l = [fitz.Point(cx - size * 0.72, cy - size),
                 fitz.Point(cx + size * 0.72, cy - size),
                 fitz.Point(cx, cy)]
        pts_r = [fitz.Point(cx - size * 0.72, cy + size),
                 fitz.Point(cx + size * 0.72, cy + size),
                 fitz.Point(cx, cy)]
    for p in (pts_l, pts_r):
        s.draw_polyline(p + [p[0]])
    s.finish(color=BLACK, fill=WHITE, width=1.0)
    s.commit()


def motor_operator(page, cx, cy, valve_size=9):
    """'M' actuator on a stem above a valve."""
    line(page, (cx, cy - valve_size), (cx, cy - valve_size - 12), width=LW_THIN)
    page.draw_circle(fitz.Point(cx, cy - valve_size - 20), 9,
                     color=BLACK, fill=WHITE, width=1.0)
    text(page, cx, cy - valve_size - 16.5, "M", size=9, bold=True, anchor="center")


def pump(page, cx, cy, r=22):
    """Centrifugal pump: circle on a baseplate with a discharge nozzle wedge."""
    page.draw_circle(fitz.Point(cx, cy), r, color=BLACK, fill=WHITE, width=1.2)
    s = page.new_shape()
    s.draw_polyline([fitz.Point(cx, cy - r), fitz.Point(cx + r + 10, cy - r),
                     fitz.Point(cx + r, cy), fitz.Point(cx, cy)])
    s.finish(color=BLACK, fill=WHITE, width=1.0)
    s.commit()
    # baseplate
    line(page, (cx - r - 6, cy + r + 6), (cx + r + 12, cy + r + 6), width=1.4)


def strainer(page, cx, cy, w=34, h=26):
    """Y-type strainer symbol: body box with hatched screen leg."""
    page.draw_rect(fitz.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
                   color=BLACK, fill=WHITE, width=1.1)
    for i in range(5):
        x = cx - w / 2 + 5 + i * 6
        line(page, (x, cy - h / 2 + 3), (x - 5, cy + h / 2 - 3), width=LW_THIN)


def vessel(page, x0, y0, x1, y1):
    """Vertical vessel: rectangle with rounded (elliptical) heads."""
    page.draw_rect(fitz.Rect(x0, y0, x1, y1), color=BLACK, fill=WHITE, width=1.3)
    for yc in (y0, y1):
        page.draw_curve(fitz.Point(x0, yc),
                        fitz.Point((x0 + x1) / 2, yc + (14 if yc == y1 else -14)),
                        fitz.Point(x1, yc), color=BLACK, fill=WHITE, width=1.3)


# --------------------------------------------------------------------------- #
# drawing
# --------------------------------------------------------------------------- #
def build() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    doc = fitz.open()
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    # ---- border + drawing frame -----------------------------------------
    page.draw_rect(fitz.Rect(18, 18, PAGE_W - 18, PAGE_H - 18),
                   color=BLACK, width=1.8)
    page.draw_rect(fitz.Rect(26, 26, PAGE_W - 26, PAGE_H - 26),
                   color=BLACK, width=0.7)

    # ---- deaerator DA-100 ------------------------------------------------
    da = (62, 150, 158, 330)
    vessel(page, *da)
    text(page, 110, 200, "DA-100", size=13, bold=True, anchor="center")
    text(page, 110, 216, "DEAERATOR", size=8.5, anchor="center")
    text(page, 110, 232, "& STORAGE", size=8.5, anchor="center")

    Y_SUCT = 300.0

    # ---- suction run: DA-100 -> S-14 -> pump header ----------------------
    line(page, (158, Y_SUCT), (243, Y_SUCT))
    strainer(page, 262, Y_SUCT)
    line(page, (281, Y_SUCT), (372, Y_SUCT))
    arrow(page, (372, Y_SUCT), (1, 0))
    text(page, 200, Y_SUCT - 10, '8"-BFW-1041', size=9.5, bold=True, anchor="center")
    text(page, 262, Y_SUCT + 32, "S-14", size=12, bold=True, anchor="center")
    text(page, 262, Y_SUCT + 45, "SUCTION STRAINER", size=8, anchor="center")

    # PDI across the strainer
    bubble(page, 262, 196, "PDI-S14", r=23)
    polyline(page, [(240, Y_SUCT - 13), (240, 232), (262, 219)],
             width=LW_THIN, dashes="[2 2] 0")
    polyline(page, [(284, Y_SUCT - 13), (284, 232), (262, 219)],
             width=LW_THIN, dashes="[2 2] 0")

    # ---- suction header split -------------------------------------------
    Y_A, Y_B = 210.0, 400.0
    X_SUCT_HDR = 372.0
    line(page, (X_SUCT_HDR, Y_A), (X_SUCT_HDR, Y_B))
    for y in (Y_A, Y_B):
        line(page, (X_SUCT_HDR, y), (418, y))
        arrow(page, (418, y), (1, 0))

    # ---- pumps -----------------------------------------------------------
    X_PA, X_PB = 452.0, 452.0
    pump(page, X_PA, Y_A)
    pump(page, X_PB, Y_B)
    line(page, (418, Y_A), (430, Y_A))
    line(page, (418, Y_B), (430, Y_B))

    text(page, X_PA, Y_A + 68, "P-101A", size=13, bold=True, anchor="center")
    text(page, X_PA, Y_A + 82, "BOILER FEED PUMP A", size=8, anchor="center")
    text(page, X_PB, Y_B + 68, "P-101B", size=13, bold=True, anchor="center")
    text(page, X_PB, Y_B + 82, "BOILER FEED PUMP B", size=8, anchor="center")

    # pump discharge risers up to the common discharge header
    Y_DISCH = 120.0
    X_DA, X_DB = 512.0, 560.0
    polyline(page, [(X_PA + 22, Y_A - 22), (X_DA, Y_A - 22), (X_DA, Y_DISCH)])
    arrow(page, (X_DA, Y_DISCH + 2), (0, -1))
    polyline(page, [(X_PB + 22, Y_B - 22), (X_DB, Y_B - 22), (X_DB, Y_DISCH)])
    arrow(page, (X_DB, Y_DISCH + 2), (0, -1))

    # ---- P-101B local instruments ---------------------------------------
    bubble(page, 372, 480, "TE-101B", r=23,
           leader_from=(X_PB - 16, Y_B + 16))
    text(page, 372, 512, "BEARING HSG", size=7.5, anchor="center")
    bubble(page, 452, 545, "VE-101B", r=23,
           leader_from=(X_PB, Y_B + 28))

    text(page, 545, 470, "P-101B NOTES:", size=9, bold=True)
    text(page, 545, 486, "SEAL PLAN: API 682 PLAN 23", size=9.5, bold=True)
    text(page, 545, 502, "MIN CONT FLOW 72 m³/h", size=9.5, bold=True)

    # ---- discharge header to boiler --------------------------------------
    X_BOIL = 1050.0
    line(page, (X_DA, Y_DISCH), (X_BOIL, Y_DISCH))
    arrow(page, (X_BOIL, Y_DISCH), (1, 0))
    text(page, 700, Y_DISCH - 12, '6"-BFW-1042', size=9.5, bold=True, anchor="center")
    text(page, X_BOIL + 6, Y_DISCH - 6, "TO BOILER", size=10, bold=True)
    text(page, X_BOIL + 6, Y_DISCH + 8, "B-01 DRUM", size=8.5)
    text(page, 700, Y_DISCH + 22, "DESIGN 150 bar / 180 °C", size=9.5, bold=True,
         anchor="center")

    # header instruments
    bubble(page, 660, 62, "PT-101", r=22, leader_from=(660, Y_DISCH))
    bubble(page, 790, 62, "FT-101", r=22, leader_from=(790, Y_DISCH))
    text(page, 790, 30, "TO MIN-FLOW CONTROL", size=7.5, anchor="center")

    # ---- minimum flow recirculation --------------------------------------
    X_TAP = 880.0
    Y_REC = 660.0
    line(page, (X_TAP, Y_DISCH), (X_TAP, Y_REC))
    arrow(page, (X_TAP, Y_REC - 40), (0, 1))
    text(page, X_TAP + 8, 300, "MIN FLOW RECIRC", size=9, bold=True)
    text(page, X_TAP + 8, 314, '3"-BFW-1043', size=9.5, bold=True)

    # horizontal recirc run back toward DA-100
    line(page, (X_TAP, Y_REC), (150, Y_REC))
    arrow(page, (300, Y_REC), (-1, 0))

    # MOV-118
    gate_valve(page, 700, Y_REC, size=11)
    motor_operator(page, 700, Y_REC, valve_size=11)
    text(page, 700, Y_REC + 28, "MOV-118", size=11, bold=True, anchor="center")
    text(page, 700, Y_REC + 41, "MIN-FLOW CONTROL VALVE", size=8, anchor="center")

    # RO-119 restriction orifice: two short bars across the line
    line(page, (560, Y_REC - 13), (560, Y_REC + 13), width=1.4)
    line(page, (566, Y_REC - 13), (566, Y_REC + 13), width=1.4)
    text(page, 563, Y_REC + 28, "RO-119", size=11, bold=True, anchor="center")
    text(page, 563, Y_REC + 41, "RESTRICTION ORIFICE", size=8, anchor="center")

    # return riser into DA-100
    polyline(page, [(150, Y_REC), (150, 352)])
    arrow(page, (150, 344), (0, -1))
    line(page, (150, 344), (150, 330))
    text(page, 158, 470, "RECIRC RETURN", size=8.5)
    text(page, 158, 484, "TO DA-100", size=8.5)

    # ---- V-201 knockout drum --------------------------------------------
    vessel(page, 300, 700, 470, 790)
    text(page, 385, 735, "V-201", size=13, bold=True, anchor="center")
    text(page, 385, 750, "KNOCKOUT DRUM", size=8.5, anchor="center")
    text(page, 385, 764, "DESIGN 25 bar", size=9.5, bold=True, anchor="center")
    # vent tie-in from the DA-100 area (dashed = off-plot / vent service)
    polyline(page, [(300, 745), (250, 745), (250, 700)],
             width=LW_THIN, dashes="[3 3] 0")
    text(page, 196, 692, "VENT HDR", size=8)

    # ---- legend ----------------------------------------------------------
    lx, ly = 935, 400
    page.draw_rect(fitz.Rect(lx, ly, lx + 215, ly + 100), color=BLACK, width=0.9)
    text(page, lx + 10, ly + 18, "LEGEND", size=10, bold=True)
    line(page, (lx + 12, ly + 34), (lx + 46, ly + 34), width=LW)
    text(page, lx + 54, ly + 37, "PROCESS LINE", size=8.5)
    line(page, (lx + 12, ly + 52), (lx + 46, ly + 52),
         width=LW_THIN, dashes="[2 2] 0")
    text(page, lx + 54, ly + 55, "INSTRUMENT SIGNAL", size=8.5)
    page.draw_circle(fitz.Point(lx + 29, ly + 70), 8, color=BLACK,
                     fill=WHITE, width=0.9)
    text(page, lx + 54, ly + 73, "FIELD INSTRUMENT (ISA)", size=8.5)
    line(page, (lx + 12, ly + 88), (lx + 40, ly + 88), width=LW)
    arrow(page, (lx + 46, ly + 88), (1, 0))
    text(page, lx + 54, ly + 91, "FLOW DIRECTION", size=8.5)

    # ---- title block -----------------------------------------------------
    tb = fitz.Rect(790, 690, PAGE_W - 30, PAGE_H - 30)
    page.draw_rect(tb, color=BLACK, width=1.6)
    rows = [tb.y0 + 34, tb.y0 + 56, tb.y0 + 78, tb.y0 + 100]
    for y in rows:
        line(page, (tb.x0, y), (tb.x1, y), width=0.8)
    line(page, ((tb.x0 + tb.x1) / 2, rows[0]), ((tb.x0 + tb.x1) / 2, rows[2]),
         width=0.8)

    # NB: base-14 Helvetica is latin-1; an em dash would drop out, so use "-".
    text(page, tb.x0 + 10, tb.y0 + 22, "BOILER FEED WATER SYSTEM - P&ID",
         size=12, bold=True)
    text(page, tb.x0 + 10, rows[0] + 15, "DRAWING NO.", size=7.5, color=GREY)
    text(page, tb.x0 + 100, rows[0] + 16, "PID-BFW-04", size=11, bold=True)
    text(page, (tb.x0 + tb.x1) / 2 + 10, rows[0] + 15, "REV", size=7.5, color=GREY)
    text(page, (tb.x0 + tb.x1) / 2 + 50, rows[0] + 16, "3", size=11, bold=True)

    text(page, tb.x0 + 10, rows[1] + 15, "DATE", size=7.5, color=GREY)
    text(page, tb.x0 + 100, rows[1] + 16, "2026-04-08", size=11, bold=True)
    text(page, (tb.x0 + tb.x1) / 2 + 10, rows[1] + 15, "SHEET", size=7.5, color=GREY)
    text(page, (tb.x0 + tb.x1) / 2 + 50, rows[1] + 16, "1 OF 1", size=10, bold=True)

    text(page, tb.x0 + 10, rows[2] + 15, "PLANT", size=7.5, color=GREY)
    text(page, tb.x0 + 100, rows[2] + 16, "Unit 1 - Boiler House", size=11, bold=True)

    text(page, tb.x0 + 10, rows[3] + 16, "ISSUED FOR CONSTRUCTION", size=9, bold=True)

    doc.save(PDF_PATH)
    pix = page.get_pixmap(dpi=200)
    pix.save(PNG_PATH)
    doc.close()
    print(f"PDF: {PDF_PATH}")
    print(f"PNG: {PNG_PATH} ({pix.width}x{pix.height})")


if __name__ == "__main__":
    build()
