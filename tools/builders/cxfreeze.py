"""
Реализация инструмента сборки cx_Freeze.
"""

import sys
from typing import List

from .base import BaseBuilder


class CxFreezeBuilder(BaseBuilder):
    """Билдер для cx_Freeze."""
    
    name = "cxfreeze"
    
    def get_version_command(self) -> List[str]:
        return [sys.executable, "-c", "import cx_Freeze; print(cx_Freeze.__version__)"]
    
    def get_build_command(self, source_file: str) -> List[str]:
        return [sys.executable, "configs/setup_cxfreeze.py", "build"]
    
    def get_output_path(self) -> str:
        if sys.platform == "win32":
            return "build/exe.win-amd64-3.*"
        elif sys.platform == "darwin":
            return "build/exe.macosx-*"
        return "build/exe.linux-*"
