"""
Реализация инструмента сборки PyInstaller.
"""

import sys
from typing import List

from .base import BaseBuilder


class PyInstallerBuilder(BaseBuilder):
    """Билдер для PyInstaller."""
    
    name = "pyinstaller"
    
    def get_version_command(self) -> List[str]:
        return [sys.executable, "-m", "PyInstaller", "--version"]
    
    def get_build_command(self, source_file: str) -> List[str]:
        return [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--distpath", "dist",
            "--workpath", "build/pyinstaller",
            "--specpath", "build/pyinstaller",
            "--noconfirm",
            source_file
        ]
    
    def get_output_path(self) -> str:
        if sys.platform == "win32":
            return "dist/app.exe"
        return "dist/app"
