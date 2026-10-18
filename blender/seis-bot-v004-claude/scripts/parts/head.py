"""head - SEIS bot head and neck (see head.NOTES.md).  Level head, built at world position; left side built and mirrored."""
import importlib
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seis_lib as L  # noqa: E402

MODS = ["head_lib", "head_skull", "head_face", "head_facets", "head_neck", "head_detail", "head_hw", "head_extra"]


def build():
    out = []
    skip = os.environ.get('HEAD_SKIP', '').split(',')
    for m in MODS:
        if m.replace('head_', '') in skip:
            continue
        try:
            mod = importlib.import_module(m)
        except ImportError:
            continue
        importlib.reload(mod)
        if hasattr(mod, "build"):
            mod.build(out)
    return out
