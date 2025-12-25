"""
Реализация инструмента сборки PyOxidizer.
"""

import sys
from typing import List

from .base import BaseBuilder


class PyOxidizerBuilder(BaseBuilder):
    """Билдер для PyOxidizer."""
    
    name = "pyoxidizer"
    
    def get_version_command(self) -> List[str]:
        return ["pyoxidizer", "--version"]
    
    def get_build_command(self, source_file: str) -> List[str]:
        # pyoxidizer.bzl должен находиться в корне проекта
        # build/ создаётся рядом с конфигом
        return ["pyoxidizer", "build", "--release"]
    
    def get_output_path(self) -> str:
        return "build/*/release/install"
    
    def build(self, source_file: str = "app.py", timeout: int = 1200):
        """Переопределение с увеличенным таймаутом для PyOxidizer."""
        return super().build(source_file, timeout)
