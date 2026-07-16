"""Deterministic visual mechanisms and their auditable event contract."""

from __future__ import annotations

import math

EVENT_SPEC = {
    "S01": ("fall", "contact", "splash_or_wet_response"),
    "S05": ("surface_water_arrival", "pore_entry", "infiltration_continues"),
    "S06": ("film_transport", "adsorption"),
    "S07": ("water_arrival", "local_mycelia_wake"),
    "S09": ("visible_air_cavity", "water_surrounds", "cavity_compresses", "same_bubble_closes"),
    "S10": ("same_bubble_rises_at_1.000",),
    "S11": ("surface_contact", "film_rupture", "fine_droplets", "surface_rebound"),
    "S12": ("crack_led_darkening", "grain_edge_wetting", "restrained_film_highlight", "dry_wet_coexist"),
}


def rupture_frame_count() -> int:
    return 3


def s12_palette() -> tuple[tuple[int, int, int], ...]:
    return ((72, 61, 48), (48, 48, 42), (31, 38, 37), (123, 125, 112))


def s12_final_dry_fraction() -> float:
    return 0.34


BUBBLE_ANCHOR = (360, 1070)


def _svg(body: str, attrs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="1280" viewBox="0 0 720 1280" {attrs}>'
        '<defs><filter id="soft"><feGaussianBlur stdDeviation="5"/></filter>'
        '<filter id="glow"><feGaussianBlur stdDeviation="2"/></filter></defs>'
        f'{body}</svg>'
    )


def mechanism_a_state(index: int, total: int) -> dict[str, float | str]:
    p = max(0.0, min(1.0, index / max(1, total - 1)))
    return {
        "phase": "infiltration" if p < 0.34 else "adsorption" if p < 0.70 else "local_wake",
        "water_front": round(95 + 1060 * (p ** 0.76), 3),
        "adsorption": max(0.0, min(1.0, (p - 0.28) / 0.42)),
        "wake": max(0.0, min(1.0, (p - 0.65) / 0.30)),
    }


def mechanism_a_svg(index: int, total: int) -> str:
    state = mechanism_a_state(index, total)
    front = float(state["water_front"])
    adsorption = float(state["adsorption"])
    wake = float(state["wake"])
    bodies = []
    pores = (
        "M125 40 C110 180 165 250 132 388 S170 620 150 770 S112 1010 138 1220",
        "M350 10 C322 168 378 270 345 430 S388 650 350 805 S315 1018 352 1245",
        "M585 50 C615 205 558 315 590 465 S550 690 580 855 S620 1040 585 1230",
    )
    for n, path in enumerate(pores):
        offset = n * 42
        opacity = 0.15 + 0.14 * min(1.0, max(0.0, (front - offset) / 700))
        bodies.append(f'<path d="{path}" fill="none" stroke="#688078" stroke-width="{9-n}" opacity="{opacity:.3f}" stroke-linecap="round"/>')
        for k in range(7):
            y = 80 + k * 165 + n * 28
            if y <= front:
                x = (125, 350, 585)[n] + 18 * math.sin((index + k * 11 + n * 7) * 0.08)
                bodies.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="4" ry="7" fill="#b6c6bd" opacity="0.34"/>')
    if adsorption > 0:
        for n in range(18):
            sx = 95 + (n * 97) % 530
            sy = 410 + (n * 137) % 560
            drift = 24 * (1 - adsorption) * math.sin(index * 0.1 + n)
            radius = 4.2 - 1.6 * adsorption
            bodies.append(f'<circle cx="{sx + drift:.1f}" cy="{sy:.1f}" r="{radius:.1f}" fill="#b5a176" opacity="{0.24 + 0.35*adsorption:.3f}"/>')
            if adsorption > 0.72:
                bodies.append(f'<path d="M{sx-8} {sy+4} Q{sx} {sy-3} {sx+8} {sy+3}" fill="none" stroke="#9d9275" stroke-width="2" opacity="0.45"/>')
    if wake > 0:
        mycelia = (
            "M90 1020 C170 960 218 1010 288 930",
            "M288 930 C340 870 395 900 458 815",
            "M288 930 C350 995 435 960 548 1030",
            "M458 815 C515 770 566 790 635 720",
        )
        visible = max(1, round(len(mycelia) * wake))
        for path in mycelia[:visible]:
            bodies.append(f'<path d="{path}" fill="none" stroke="#aaa58f" stroke-width="2" opacity="{0.10 + 0.32*wake:.3f}" stroke-linecap="round"/>')
        for n in range(round(24 * wake)):
            x = 90 + (n * 83) % 540 + 2.2 * math.sin(index * 0.18 + n)
            y = 720 + (n * 59) % 390 + 1.8 * math.cos(index * 0.14 + n)
            bodies.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.8" fill="#bbb497" opacity="{0.18 + 0.26*wake:.3f}"/>')
    return _svg("".join(bodies), f'data-phase="{state["phase"]}"')


def mechanism_b_state(shot_id: str, index: int, total: int) -> dict[str, float | str]:
    p = max(0.0, min(1.0, index / max(1, total - 1)))
    if shot_id == "S09":
        close = p * p * (3 - 2 * p)
        return {
            "phase": "cavity" if p < 0.72 else "bubble_closure",
            "cx": BUBBLE_ANCHOR[0], "cy": BUBBLE_ANCHOR[1],
            "rx": round(92 - 50 * close, 3), "ry": round(150 - 88 * close, 3),
            "water": round(close, 3),
        }
    if shot_id == "S11":
        return {"phase": "rupture" if index in (2, 3, 4) else "release" if index < 28 else "rebound", "p": p}
    raise ValueError(f"unsupported mechanism B shot: {shot_id}")


def mechanism_b_svg(shot_id: str, index: int, total: int) -> str:
    state = mechanism_b_state(shot_id, index, total)
    if shot_id == "S09":
        cx, cy = int(state["cx"]), int(state["cy"])
        rx, ry = float(state["rx"]), float(state["ry"])
        water = float(state["water"])
        cavity = f"M{cx-rx:.1f} {cy} C{cx-rx*.9:.1f} {cy-ry:.1f} {cx+rx*.8:.1f} {cy-ry*.8:.1f} {cx+rx:.1f} {cy} C{cx+rx*.9:.1f} {cy+ry:.1f} {cx-rx*.75:.1f} {cy+ry*.85:.1f} {cx-rx:.1f} {cy} Z"
        body = (
            f'<path d="{cavity}" fill="#293331" opacity="{0.42 - 0.17*water:.3f}" stroke="#9baaa4" stroke-width="3"/>'
            f'<path d="M170 {1180-450*water:.1f} C260 {1140-380*water:.1f} 460 {1140-380*water:.1f} 550 {1180-450*water:.1f}" fill="none" stroke="#718b87" stroke-width="18" opacity="{0.16+0.20*water:.3f}" filter="url(#soft)"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*.62:.1f}" ry="{ry*.62:.1f}" fill="none" stroke="#d1dad4" stroke-width="4" opacity="{0.08+0.60*water:.3f}"/>'
            f'<ellipse cx="{cx-10}" cy="{cy-ry*.28:.1f}" rx="{rx*.23:.1f}" ry="{ry*.10:.1f}" fill="#d8dfda" opacity="{0.10+0.35*water:.3f}"/>'
        )
        return _svg(body, f'data-phase="{state["phase"]}"')
    rupture = index in (2, 3, 4)
    body = []
    if index < 2:
        body.append('<path d="M255 430 Q360 330 465 430" fill="none" stroke="#d3ddd8" stroke-width="8" opacity="0.74"/>')
    elif rupture:
        gap = 22 + (index - 2) * 28
        body.append(f'<path d="M245 430 Q{320-gap} 350 {345-gap} 402" fill="none" stroke="#c8d4cf" stroke-width="5" opacity="0.72"/>')
        body.append(f'<path d="M{375+gap} 402 Q{400+gap} 350 475 430" fill="none" stroke="#c8d4cf" stroke-width="5" opacity="0.72"/>')
    if 3 <= index < 28:
        q = (index - 3) / 25
        for n in range(13):
            angle = -2.6 + n * 0.42
            speed = 165 + (n % 4) * 33
            x = 360 + math.cos(angle) * speed * q
            y = 410 - abs(math.sin(angle)) * speed * q + 145 * q * q
            r = 2.2 if n % 3 else 3.2
            body.append(f'<circle data-droplet="true" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#cbd6d1" opacity="{0.60*(1-q):.3f}"/>')
    if index >= 5:
        q = min(1.0, (index - 5) / 55)
        amp = 18 * (1 - q)
        body.append(f'<path d="M70 438 Q220 {438+amp:.1f} 360 {438-amp:.1f} T650 438" fill="none" stroke="#aebcb7" stroke-width="3" opacity="{0.42*(1-0.55*q):.3f}"/>')
    attrs = f'data-phase="{state["phase"]}"' + (' data-rupture="true"' if rupture else '')
    return _svg("".join(body), attrs)


def s12_svg(index: int, total: int) -> str:
    p = max(0.0, min(1.0, index / max(1, total - 1)))
    paths = (
        "M360 0 C340 150 390 240 355 360 S310 590 370 710 S330 930 390 1280",
        "M80 180 C190 245 215 340 335 360",
        "M355 360 C500 300 560 380 710 330",
        "M120 720 C235 650 300 720 370 710",
        "M370 710 C470 770 535 720 690 830",
        "M30 1040 C170 980 280 1080 390 1010",
        "M390 1010 C500 950 610 1040 720 980",
    )
    visible = round(len(paths) * min(1.0, p * 1.25))
    body = []
    for n, path in enumerate(paths[:visible]):
        width = 16 + (n % 3) * 7
        opacity = 0.12 + 0.20 * p
        body.append(f'<path d="{path}" fill="none" stroke="#26302d" stroke-width="{width}" opacity="{opacity:.3f}" stroke-linecap="round" filter="url(#soft)"/>')
        body.append(f'<path d="{path}" fill="none" stroke="#6f716b" stroke-width="2" opacity="{0.08+0.17*p:.3f}" stroke-linecap="round"/>')
    for n in range(round(12 * p)):
        x = 55 + (n * 137) % 620
        y = 180 + (n * 173) % 980
        body.append(f'<ellipse cx="{x}" cy="{y}" rx="{34+n%4*8}" ry="{12+n%3*5}" fill="#252c2b" opacity="{0.035+0.055*p:.3f}" filter="url(#soft)"/>')
    return _svg("".join(body), f'data-dry-fraction="{s12_final_dry_fraction():.2f}"')


def _put(buf: bytearray, width: int, height: int, x: int, y: int, color: tuple[int, int, int, int]) -> None:
    if not (0 <= x < width and 0 <= y < height):
        return
    pos = (y * width + x) * 4
    src_a = color[3]
    if src_a <= buf[pos + 3]:
        return
    buf[pos:pos + 4] = bytes(color)


def _circle(buf: bytearray, width: int, height: int, cx: float, cy: float, radius: float, color: tuple[int, int, int, int]) -> None:
    radius = max(1.0, radius)
    x0, x1 = int(cx - radius), int(cx + radius) + 1
    y0, y1 = int(cy - radius), int(cy + radius) + 1
    r2 = radius * radius
    for y in range(y0, y1):
        for x in range(x0, x1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r2:
                _put(buf, width, height, x, y, color)


def _line(buf: bytearray, width: int, height: int, points: list[tuple[float, float]], thickness: float, color: tuple[int, int, int, int]) -> None:
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        distance = max(1, int(max(abs(x1 - x0), abs(y1 - y0))))
        for step in range(distance + 1):
            p = step / distance
            _circle(buf, width, height, x0 + (x1 - x0) * p, y0 + (y1 - y0) * p, thickness / 2, color)


def _scaled(points: list[tuple[float, float]], width: int, height: int) -> list[tuple[float, float]]:
    return [(x * width / 720, y * height / 1280) for x, y in points]


def render_overlay_rgba(kind: str, index: int, total: int, width: int = 720, height: int = 1280) -> bytes:
    """Rasterize sparse overlays with the Python standard library only."""
    buf = bytearray(width * height * 4)
    sx, sy = width / 720, height / 1280
    scale = min(sx, sy)
    if kind == "mechanism-a":
        state = mechanism_a_state(index, total)
        front = float(state["water_front"])
        adsorption = float(state["adsorption"])
        wake = float(state["wake"])
        paths = [
            [(125, 40), (112, 190), (145, 330), (132, 480), (162, 650), (150, 820), (138, 1020), (145, 1220)],
            [(350, 10), (330, 170), (370, 300), (345, 460), (380, 650), (350, 830), (330, 1020), (352, 1245)],
            [(585, 50), (610, 210), (565, 350), (590, 500), (555, 700), (580, 875), (610, 1040), (585, 1230)],
        ]
        for n, points in enumerate(paths):
            visible = [(x, y) for x, y in points if y <= front]
            if len(visible) >= 2:
                _line(buf, width, height, _scaled(visible, width, height), (7 - n) * scale, (104, 128, 120, 92))
            for k in range(7):
                y = 80 + k * 165 + n * 28
                if y <= front:
                    x = (125, 350, 585)[n] + 18 * math.sin((index + k * 11 + n * 7) * 0.08)
                    _circle(buf, width, height, x * sx, y * sy, 4 * scale, (182, 198, 189, 116))
        if adsorption > 0:
            for n in range(18):
                x = 95 + (n * 97) % 530 + 24 * (1 - adsorption) * math.sin(index * 0.1 + n)
                y = 410 + (n * 137) % 560
                _circle(buf, width, height, x * sx, y * sy, (4.2 - 1.6 * adsorption) * scale, (181, 161, 118, int(62 + 85 * adsorption)))
        if wake > 0:
            mycelia = [
                [(90, 1020), (170, 960), (218, 1010), (288, 930)],
                [(288, 930), (340, 870), (395, 900), (458, 815)],
                [(288, 930), (350, 995), (435, 960), (548, 1030)],
                [(458, 815), (515, 770), (566, 790), (635, 720)],
            ]
            for points in mycelia[:max(1, round(len(mycelia) * wake))]:
                _line(buf, width, height, _scaled(points, width, height), 2 * scale, (170, 165, 143, int(30 + 75 * wake)))
            for n in range(round(24 * wake)):
                x = 90 + (n * 83) % 540 + 2.2 * math.sin(index * 0.18 + n)
                y = 720 + (n * 59) % 390 + 1.8 * math.cos(index * 0.14 + n)
                _circle(buf, width, height, x * sx, y * sy, 2 * scale, (187, 180, 151, int(45 + 62 * wake)))
    elif kind == "mechanism-a-completion":
        state = mechanism_a_state(index, total)
        adsorption = float(state["adsorption"])
        wake = float(state["wake"])
        if adsorption > 0:
            for n in range(16):
                anchor_x = 95 + (n * 97) % 530
                anchor_y = 410 + (n * 137) % 500
                start_x = anchor_x + 34 * math.sin(n * 1.7)
                start_y = anchor_y - 26 - (n % 3) * 9
                ease = adsorption * adsorption * (3 - 2 * adsorption)
                x = start_x + (anchor_x - start_x) * ease
                y = start_y + (anchor_y - start_y) * ease
                _circle(buf, width, height, x * sx, y * sy, 4.8 * scale,
                        (170, 139, 82, int(105 + 105 * adsorption)))
                if adsorption > 0.78:
                    _circle(buf, width, height, anchor_x * sx, anchor_y * sy, 7.0 * scale,
                            (116, 94, 62, int(42 + 52 * adsorption)))
        if wake > 0:
            local_mycelia = [
                [(390, 1030), (435, 985), (478, 1005), (525, 955)],
                [(478, 1005), (520, 1050), (575, 1025), (630, 1072)],
                [(525, 955), (555, 905), (610, 890), (652, 845)],
            ]
            visible = max(1, round(len(local_mycelia) * wake))
            for points in local_mycelia[:visible]:
                _line(buf, width, height, _scaled(points, width, height), 3.0 * scale,
                      (185, 176, 139, int(55 + 100 * wake)))
            for n in range(round(14 * wake)):
                x = 395 + (n * 61) % 245 + 1.8 * math.sin(index * 0.17 + n)
                y = 850 + (n * 47) % 225 + 1.5 * math.cos(index * 0.13 + n)
                _circle(buf, width, height, x * sx, y * sy, 2.6 * scale,
                        (190, 176, 132, int(55 + 90 * wake)))
    elif kind == "S09":
        state = mechanism_b_state("S09", index, total)
        cx, cy = float(state["cx"]) * sx, float(state["cy"]) * sy
        rx, ry = float(state["rx"]) * sx, float(state["ry"]) * sy
        water = float(state["water"])
        ellipse = []
        for degree in range(0, 361, 4):
            a = math.radians(degree)
            ellipse.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
        _line(buf, width, height, ellipse, 4 * scale, (208, 218, 212, int(55 + 115 * water)))
        _circle(buf, width, height, cx - 10 * sx, cy - ry * .28, max(2, rx * .22), (216, 223, 218, int(28 + 75 * water)))
        y = (1180 - 450 * water) * sy
        _line(buf, width, height, [(170*sx, y), (260*sx, y-22*sy), (460*sx, y-22*sy), (550*sx, y)], 10*scale, (113, 139, 135, int(40 + 45 * water)))
    elif kind == "S11":
        if index < 2:
            dome = []
            for degree in range(200, 341, 5):
                a = math.radians(degree)
                dome.append(((360 + 115*math.cos(a))*sx, (440 + 105*math.sin(a))*sy))
            _line(buf, width, height, dome, 7*scale, (211, 221, 216, 188))
        if 2 <= index <= 4:
            gap = 22 + (index - 2) * 28
            _line(buf, width, height, _scaled([(245,430),(290-gap,370),(345-gap,402)], width, height), 5*scale, (200,212,207,184))
            _line(buf, width, height, _scaled([(375+gap,402),(430+gap,370),(475,430)], width, height), 5*scale, (200,212,207,184))
        if 3 <= index < 28:
            q = (index - 3) / 25
            for n in range(13):
                angle = -2.6 + n * 0.42
                speed = 165 + (n % 4) * 33
                x = 360 + math.cos(angle) * speed * q
                y = 410 - abs(math.sin(angle)) * speed * q + 145 * q * q
                _circle(buf, width, height, x*sx, y*sy, (2.2 if n%3 else 3.2)*scale, (203,214,209,int(150*(1-q))))
        if index >= 5:
            q = min(1.0, (index - 5) / 55)
            amp = 18 * (1 - q)
            _line(buf, width, height, _scaled([(70,438),(220,438+amp),(360,438-amp),(510,438+amp),(650,438)], width, height), 3*scale, (174,188,183,int(95*(1-.55*q))))
    elif kind == "S12":
        p = max(0.0, min(1.0, index / max(1, total - 1)))
        cracks = [
            [(360,0),(345,180),(370,360),(340,540),(370,710),(345,930),(390,1280)],
            [(80,180),(190,245),(335,360)], [(355,360),(500,300),(710,330)],
            [(120,720),(235,650),(370,710)], [(370,710),(500,770),(690,830)],
            [(30,1040),(170,980),(390,1010)], [(390,1010),(520,950),(720,980)],
        ]
        for n, points in enumerate(cracks[:round(len(cracks)*min(1,p*1.25))]):
            _line(buf, width, height, _scaled(points,width,height), (16+(n%3)*7)*scale, (38,48,45,int(38+52*p)))
            _line(buf, width, height, _scaled(points,width,height), 2*scale, (111,113,107,int(20+40*p)))
        for n in range(round(12*p)):
            x,y=55+(n*137)%620,180+(n*173)%980
            _circle(buf,width,height,x*sx,y*sy,(10+n%4*3)*scale,(37,44,43,int(14+15*p)))
    else:
        raise ValueError(f"unknown overlay kind: {kind}")
    return bytes(buf)
