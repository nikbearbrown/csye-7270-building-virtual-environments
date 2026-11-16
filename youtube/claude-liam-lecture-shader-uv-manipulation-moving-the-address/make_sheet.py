#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('shader_preparation',Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16')/'prepare_films.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.build(json.loads((HERE/'film-content.json').read_text()),HERE)
