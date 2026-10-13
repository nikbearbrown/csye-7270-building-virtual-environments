#!/usr/bin/env python3
"""make_sheet.py: four-line shim. The builder is shared: ../_godot-shaders-series/make_sheet_shared.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import make_sheet_shared
make_sheet_shared.main(Path(__file__).resolve().parent)
