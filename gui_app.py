"""Convenience wrapper for the real GUI implementation in Files/gui_app.py"""
from __future__ import annotations
import importlib.util
import sys
from pathlib import Path

FILES_DIR = Path(__file__).parent / "Files"
sys.path.insert(0, str(FILES_DIR))
_spec = importlib.util.spec_from_file_location("ads_pillar_gui_app", FILES_DIR / "gui_app.py")
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)  # type: ignore[misc]
sys.path.pop(0)

ADSPillarGUI = _module.ADSPillarGUI

if __name__ == "__main__":
    _module.main()
