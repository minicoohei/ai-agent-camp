"""Repo-local fallback for the external ``pysrt`` package."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


_MODULE_PATH = Path(__file__).resolve().parent / "skills" / "youtube-clipper" / "scripts" / "pysrt.py"
_SPEC = importlib.util.spec_from_file_location("_repo_pysrt", _MODULE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Unable to load fallback pysrt module from {_MODULE_PATH}")
_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)

SubRipTime = _MODULE.SubRipTime
SubRipItem = _MODULE.SubRipItem
SubRipFile = _MODULE.SubRipFile
open = _MODULE.open
