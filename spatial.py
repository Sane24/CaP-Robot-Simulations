"""
spatial.py -- deterministic parse_position for every shim.

WHY THIS EXISTS: CaP's flashcards DEMONSTRATE parse_position
(their own demo solves "put the blocks in a horizontal line near the top" with
it), so generated policies call it in every condition, including baseline. An
environment that executes CaP policies must therefore provide it; without it,
a policy that correctly uses the demonstrated vocabulary crashes mid-run, the
trailing say() still fires, and the scorer records a FALSE CONFIRMATION that
is an artifact of the environment, not the model. That contaminates the
headline metric, which is why this module exists.

WHY DETERMINISTIC: in CaP, parse_position is itself an LLM sub-prompt. We
reimplement it as a deterministic parser so execution is reproducible, offline,
and identical across all 1350+ grid cells -- an LLM-in-the-loop here would add
a second stochastic model INSIDE the thing being measured.

Coordinate convention (matches the shims + parse_question):
    top = +x (far from the robot), bottom = -x, left = -y, right = +y.
"Horizontal line" = spread across y at a fixed x (left-to-right from above).

Supported phrases (everything the CaP tabletop flashcards use, plus obvious
variants): "a <N>cm horizontal/vertical line near the top/bottom/... with K
points", "the top right corner", "the bottom side", "the middle/center",
"<N>cm above/below/left/right of the <object>". Unknown text falls back to the
workspace center and records env.last_parse_fallback for diagnostics.
"""
import re
import numpy as np


def make_parse_position(env):

    def parse_position(desc):
        d = str(desc).lower()
        x_min, x_max, y_min, y_max = env.get_workspace_bounds()
        cx, cy = (x_min + x_max) / 2.0, (y_min + y_max) / 2.0

        # ---- a line with K points ----
        if "line" in d:
            m = re.search(r"(\d+)\s*(?:points|blocks|pts)", d)
            k = int(m.group(1)) if m else 4
            vertical = "vertical" in d
            x = (x_max - 0.03 if "top" in d else
                 x_min + 0.03 if "bottom" in d else cx)
            y = (y_min + 0.03 if "left" in d else
                 y_max - 0.03 if "right" in d else cy)
            if vertical:            # spread along x at fixed y
                xs = np.linspace(x_min + 0.04, x_max - 0.04, k)
                return [np.array([xx, y]) for xx in xs]
            ys = np.linspace(y_min + 0.04, y_max - 0.04, k)   # horizontal
            return [np.array([x, yy]) for yy in ys]

        # ---- a square (CaP Blocks #5: "a square with size 10cm around the
        #      middle with 4 points"). Must return a LIST; falling through to
        #      the 'middle' branch returned ONE point and broke every L9 run.
        if "square" in d:
            m = re.search(r"(\d+(?:\.\d+)?)\s*cm", d)
            side = float(m.group(1)) / 100.0 if m else 0.14
            h = side / 2.0
            cx0, cy0 = cx, cy
            if "top" in d and "corner" not in d:    cx0 = x_max - h - 0.02
            if "bottom" in d and "corner" not in d: cx0 = x_min + h + 0.02
            # clockwise from top-right, matching the corners convention
            return [np.array([cx0 + h, cy0 + h]), np.array([cx0 + h, cy0 - h]),
                    np.array([cx0 - h, cy0 - h]), np.array([cx0 - h, cy0 + h])]

        # ---- corners and sides ----
        # PLURAL first: "the corners clockwise starting at the top right" must
        # return a LIST of positions. Returning a single [x, y] here silently
        # broke L5 -- the policy's zip(blocks, corners) iterated over the two
        # COORDINATES instead of four corners, so one block was placed with a
        # scalar target and the rest raised. All 25 L5 runs failed this way.
        if "corners" in d or ("corner" in d and ("clockwise" in d or "each" in d)):
            names = ["top right corner", "bottom right corner",
                     "bottom left corner", "top left corner"]        # clockwise
            start = next((i for i, n in enumerate(names)
                          if n.replace(" corner", "") in d), 0)
            ordered = names[start:] + names[:start]
            if "counter" in d or "anticlock" in d:
                ordered = [ordered[0]] + ordered[1:][::-1]
            m = re.search(r"(\d+)\s*(?:corners|points|blocks)", d)
            k = int(m.group(1)) if m else 4
            return [env.get_corner_pos(n) for n in ordered[:k]]
        if "corner" in d:
            return env.get_corner_pos(d)
        if "sides" in d or "edges" in d:
            names = ["top side", "right side", "bottom side", "left side"]
            start = next((i for i, n in enumerate(names)
                          if n.replace(" side", "") in d), 0)
            ordered = names[start:] + names[:start]
            if "counter" in d or "anticlock" in d:
                ordered = [ordered[0]] + ordered[1:][::-1]
            return [env.get_side_pos(n) for n in ordered]
        if "side" in d or "edge" in d:
            return env.get_side_pos(d)
        if "middle" in d or "center" in d or "centre" in d:
            return np.array([cx, cy])

        # ---- relative to a named object ----
        for name in env.get_obj_names():
            if name in d:
                p = np.array(env.get_obj_pos(name)[:2], dtype=float)
                m = re.search(r"(\d+(?:\.\d+)?)\s*cm", d)
                off = float(m.group(1)) / 100.0 if m else 0.10
                if "left" in d:  p[1] -= off
                if "right" in d: p[1] += off
                if "above" in d or "behind" in d or "top" in d:    p[0] += off
                if "below" in d or "front" in d or "bottom" in d:  p[0] -= off
                return p

        env.last_parse_fallback = desc          # visible to diagnostics
        return np.array([cx, cy])

    return parse_position


def transform_shape_pts(desc, shape_pts):
    """Deterministic version of CaP's transform_shape_pts LMP (their flashcards
    demonstrate it for "make the square bigger": scale it by 1.5x). Supports
    scale by <f>x, rotate by <d> degrees, and directional shifts by <n>cm --
    all about/relative to the shape's centroid. Same rationale as
    parse_position: this is DEMONSTRATED CaP vocabulary, so an environment
    without it crashes correct policies and manufactures artifact failures."""
    pts = [np.asarray(p, dtype=float).ravel()[:2] for p in shape_pts]
    if not pts:
        return pts
    d = str(desc).lower()
    c = np.mean(pts, axis=0)

    m = re.search(r"(?:scale|bigger|larger|enlarge|grow)\D*?(\d+(?:\.\d+)?)\s*x?", d)
    if "scale" in d or "bigger" in d or "larger" in d or "enlarge" in d:
        f = float(m.group(1)) if m else 1.5
        return [c + (p - c) * f for p in pts]
    if "smaller" in d or "shrink" in d:
        f = float(m.group(1)) if m else 0.75
        f = min(f, 1.0) if f <= 1.0 else 1.0 / f
        return [c + (p - c) * f for p in pts]

    m = re.search(r"(\d+(?:\.\d+)?)\s*degrees?", d)
    if "rotate" in d and m:
        a = np.deg2rad(float(m.group(1)))
        R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
        return [c + R @ (p - c) for p in pts]

    m = re.search(r"(\d+(?:\.\d+)?)\s*cm", d)
    off = float(m.group(1)) / 100.0 if m else 0.05
    v = np.zeros(2)
    if "left" in d:  v[1] -= off
    if "right" in d: v[1] += off
    if "up" in d or "top" in d or "behind" in d:      v[0] += off
    if "down" in d or "bottom" in d or "front" in d:  v[0] -= off
    return [p + v for p in pts]