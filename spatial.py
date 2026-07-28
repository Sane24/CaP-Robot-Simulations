"""
spatial.py -- deterministic parse_position for every shim.

CaP's flashcards DEMONSTRATE parse_position
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

        # a line with K points
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

        # corners and sides
        if "corner" in d:
            return env.get_corner_pos(d)
        if "side" in d or "edge" in d:
            return env.get_side_pos(d)
        if "middle" in d or "center" in d or "centre" in d:
            return np.array([cx, cy])

        # relative to a named object
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
