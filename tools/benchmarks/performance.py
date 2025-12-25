"""
Бенчмаркинг производительности собранных исполняемых файлов.
"""

import subprocess
import sys
import time
import statistics
from typing import Dict, List, Optional
from dataclasses import dataclass

from ..console import print_step, print_success, print_warning
from ..builders import BUILDERS


@dataclass
class BenchmarkResult:
    """Результат бенчмарка производительности."""
    mean: float
    median: float
    std: float
    min_time: float
    max_time: float
    times: List[float]
    iterations: int


class PerformanceBenchmark:
    """Бенчмаркинг производительности Python сборок."""
    
    def __init__(self, n: int = 20_000_000, iterations: int = 5):
        """
        Инициализация бенчмарка.
        
        Аргументы:
            n: Размер вычисления (верхняя граница суммы квадратов)
            iterations: Количество итераций теста
        """
        self.n = n
        self.iterations = iterations
    
    def run_all(self, tools: List[str]) -> Dict[str, BenchmarkResult]:
        """
        Запуск бенчмарков для интерпретатора Python и всех инструментов.
        
        Аргументы:
            tools: Список названий инструментов для тестирования
            
        Возвращает:
            Словарь с результатами по инструментам
        """
        results = {}
        
        # Бенчмарк интерпретируемого Python
        print_step("Бенчмарк интерпретируемого Python...")
        interp_result = self._benchmark_interpreted()
        if interp_result:
            results["interpreted"] = interp_result
            print_success(f"Среднее: {interp_result.mean:.4f}с")
        
        # Бенчмарк каждого инструмента
        for tool in tools:
            result = self.run_tool(tool)
            if result:
                results[tool] = result
        
        return results
    
    def run_tool(self, tool: str) -> Optional[BenchmarkResult]:
        """
        Запуск бенчмарка для конкретного инструмента.
        
        Аргументы:
            tool: Название инструмента
            
        Возвращает:
            BenchmarkResult или None если исполняемый файл не найден
        """
        print_step(f"Бенчмарк {tool}...")
        
        builder = BUILDERS.get(tool)
        if not builder:
            print_warning(f"Неизвестный инструмент: {tool}")
            return None
        
        exe_path = self._find_executable(builder())
        if not exe_path:
            print_warning(f"Пропускаем {tool} - исполняемый файл не найден")
            return None
        
        times = self._run_iterations(exe_path)
        if not times:
            return None
        
        result = self._calculate_stats(times)
        print_success(f"Среднее: {result.mean:.4f}с")
        return result
    
    def _benchmark_interpreted(self) -> Optional[BenchmarkResult]:
        """Бенчмарк интерпретируемого Python."""
        cmd = [sys.executable, "app.py", "--cli", "-n", str(self.n)]
        times = []
        
        for i in range(self.iterations):
            start = time.time()
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=300)
                if result.returncode == 0:
                    elapsed = time.time() - start
                    times.append(elapsed)
                    print(f"    Итерация {i+1}: {elapsed:.4f}с")
            except Exception:
                pass
        
        return self._calculate_stats(times) if times else None
    
    def _find_executable(self, builder) -> Optional[str]:
        """Поиск исполняемого файла для билдера."""
        import glob
        import os
        
        pattern = builder.get_output_path()
        
        if os.path.exists(pattern):
            return pattern
        
        matches = glob.glob(pattern)
        if matches:
            # Для директорий ищем сам исполняемый файл
            path = matches[0]
            if os.path.isdir(path):
                exe_name = "app.exe" if sys.platform == "win32" else "app"
                exe_path = f"{path}/{exe_name}"
                return exe_path if os.path.exists(exe_path) else None
            return path
        
        return None
    
    def _run_iterations(self, exe_path: str) -> List[float]:
        """Запуск итераций бенчмарка для исполняемого файла."""
        cmd = [exe_path, "--cli", "-n", str(self.n)]
        times = []
        
        for i in range(self.iterations):
            try:
                start = time.time()
                result = subprocess.run(cmd, capture_output=True, timeout=120)
                elapsed = time.time() - start
                
                if result.returncode == 0:
                    times.append(elapsed)
                    print(f"    Итерация {i+1}: {elapsed:.4f}с")
            except Exception:
                pass
        
        return times
    
    def _calculate_stats(self, times: List[float]) -> BenchmarkResult:
        """Расчёт статистики по данным времени."""
        return BenchmarkResult(
            mean=statistics.mean(times),
            median=statistics.median(times),
            std=statistics.stdev(times) if len(times) > 1 else 0.0,
            min_time=min(times),
            max_time=max(times),
            times=times,
            iterations=len(times)
        )
