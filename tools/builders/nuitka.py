"""
Реализация инструмента сборки Nuitka.
"""

import sys
from typing import List

from .base import BaseBuilder


class NuitkaBuilder(BaseBuilder):
    """Билдер для Nuitka."""
    
    name = "nuitka"
    
    def get_version_command(self) -> List[str]:
        return [sys.executable, "-m", "nuitka", "--version"]
    
    def get_build_command(self, source_file: str) -> List[str]:
        cmd = [
            sys.executable, "-m", "nuitka",
            "--standalone",
            "--onefile",
            "--enable-plugin=tk-inter",
            "--assume-yes-for-downloads",
            "--output-dir=dist/nuitka",
            "--output-filename=app",
        ]
        
        if sys.platform == "win32":
            cmd.extend(["--windows-disable-console", "--mingw64"])
        elif sys.platform == "darwin":
            cmd.append("--macos-create-app-bundle")
        
        cmd.append(source_file)
        return cmd
    
    def get_output_path(self) -> str:
        if sys.platform == "win32":
            return "dist/nuitka/app.exe"
        return "dist/nuitka/app"
    
    def build(self, source_file: str = "app.py", timeout: int = 1200):
        """Переопределение с увеличенным таймаутом для Nuitka."""
        return super().build(source_file, timeout)
