"""
Измерение размера собранных артефактов.
"""

import os
import sys
import glob
from typing import Dict, Optional
from dataclasses import dataclass

from ..console import print_step, print_success, print_warning
from ..builders import BUILDERS


@dataclass
class SizeResult:
    """Результат измерения размера."""
    executable_bytes: int
    executable_mb: float
    total_bytes: int
    total_mb: float
    path: str


class SizeBenchmark:
    """Измерение размера Python сборок."""
    
    def run_all(self, tools: list) -> Dict[str, SizeResult]:
        """
        Измерение размеров для всех собранных инструментов.
        
        Аргументы:
            tools: Список названий инструментов
            
        Возвращает:
            Словарь с результатами размеров по инструментам
        """
        results = {}
        
        for tool in tools:
            result = self.measure_tool(tool)
            if result:
                results[tool] = result
        
        return results
    
    def measure_tool(self, tool: str) -> Optional[SizeResult]:
        """
        Измерение размера для конкретного инструмента.
        
        Аргументы:
            tool: Название инструмента
            
        Возвращает:
            SizeResult или None если сборка не найдена
        """
        print_step(f"Измерение {tool}...")
        
        builder_class = BUILDERS.get(tool)
        if not builder_class:
            print_warning(f"Неизвестный инструмент: {tool}")
            return None
        
        builder = builder_class()
        pattern = builder.get_output_path()
        
        # Поиск фактического пути
        path = self._find_path(pattern)
        if not path:
            print_warning(f"Пропускаем {tool} - сборка не найдена")
            return None
        
        # Расчёт размеров
        if os.path.isfile(path):
            exe_size = os.path.getsize(path)
            total_size = exe_size
        else:
            exe_name = "app.exe" if sys.platform == "win32" else "app"
            exe_path = os.path.join(path, exe_name)
            exe_size = os.path.getsize(exe_path) if os.path.exists(exe_path) else 0
            total_size = self._get_dir_size(path)
        
        result = SizeResult(
            executable_bytes=exe_size,
            executable_mb=exe_size / 1024 / 1024,
            total_bytes=total_size,
            total_mb=total_size / 1024 / 1024,
            path=path
        )
        
        print_success(
            f"Исполняемый: {result.executable_mb:.2f} MB, "
            f"Всего: {result.total_mb:.2f} MB"
        )
        
        return result
    
    def _find_path(self, pattern: str) -> Optional[str]:
        """Поиск фактического пути по шаблону."""
        if os.path.exists(pattern):
            return pattern
        
        matches = glob.glob(pattern)
        return matches[0] if matches else None
    
    def _get_dir_size(self, path: str) -> int:
        """Получение общего размера директории."""
        total = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                try:
                    total += os.path.getsize(os.path.join(dirpath, f))
                except OSError:
                    pass
        return total
