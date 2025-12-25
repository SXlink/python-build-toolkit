#!/usr/bin/env python3
"""
Единый скрипт сборки и тестирования Python Build Toolkit.

Использование:
    python build_all.py              # Сборка + бенчмарки
    python build_all.py --build-only # Только сборка
    python build_all.py --test-only  # Только бенчмарки
    python build_all.py --tools pyinstaller nuitka
"""

import sys
import os
import json
import argparse
from datetime import datetime
from dataclasses import asdict

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools import print_header, print_success, print_warning
from tools.builders import BUILDERS, get_builder
from tools.benchmarks import PerformanceBenchmark, SizeBenchmark


TOOL_NAMES = list(BUILDERS.keys())


def build_all(tools: list, source_file: str = "app.py") -> dict:
    """
    Сборка всеми указанными инструментами.
    
    Аргументы:
        tools: Список названий инструментов
        source_file: Путь к исходному файлу
        
    Возвращает:
        Словарь с результатами сборки
    """
    results = {}
    
    for tool_name in tools:
        builder = get_builder(tool_name)
        
        if not builder.is_installed():
            print_warning(f"{tool_name} не установлен - пропускаем")
            continue
        
        result = builder.build(source_file)
        results[tool_name] = {
            "success": result.success,
            "time": result.elapsed_time,
            "size_mb": result.size_bytes / 1024 / 1024 if result.size_bytes else 0,
            "path": result.output_path,
            "error": result.error_message,
        }
    
    return results


def run_benchmarks(tools: list, n: int, iterations: int) -> tuple:
    """
    Запуск бенчмарков производительности и размера.
    
    Аргументы:
        tools: Список названий инструментов
        n: Размер вычисления
        iterations: Количество итераций
        
    Возвращает:
        Кортеж (результаты_производительности, результаты_размера)
    """
    print_header("Запуск бенчмарков производительности")
    perf_bench = PerformanceBenchmark(n=n, iterations=iterations)
    perf_results = perf_bench.run_all(tools)
    
    print_header("Измерение размеров сборок")
    size_bench = SizeBenchmark()
    size_results = size_bench.run_all(tools)
    
    return perf_results, size_results


def save_results(perf_results: dict, size_results: dict, build_results: dict):
    """Сохранение всех результатов в JSON файл."""
    os.makedirs("benchmarks", exist_ok=True)
    
    # Конвертация dataclass в словари
    perf_dict = {
        k: asdict(v) if hasattr(v, '__dataclass_fields__') else v 
        for k, v in perf_results.items()
    }
    size_dict = {
        k: asdict(v) if hasattr(v, '__dataclass_fields__') else v 
        for k, v in size_results.items()
    }
    
    combined = {
        "timestamp": datetime.now().isoformat(),
        "platform": sys.platform,
        "python_version": sys.version,
        "performance": perf_dict,
        "sizes": size_dict,
        "build_times": build_results,
    }
    
    output_path = "benchmarks/full_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, default=str)
    
    print_success(f"Результаты сохранены в {output_path}")


def print_summary(perf_results: dict, size_results: dict, build_results: dict):
    """Вывод итоговых таблиц."""
    from tools.console import colorize
    
    print_header("ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
    
    # Таблица производительности
    print("\n" + colorize("Производительность (меньше = лучше):", "BOLD"))
    print("-" * 70)
    print(f"{'Инструмент':<15} {'Среднее (с)':<12} {'Медиана (с)':<12} {'Std Dev':<12}")
    print("-" * 70)
    
    sorted_perf = sorted(
        perf_results.items(), 
        key=lambda x: x[1].mean if hasattr(x[1], 'mean') else 999
    )
    for tool, data in sorted_perf:
        if hasattr(data, 'mean'):
            print(f"{tool:<15} {data.mean:<12.4f} {data.median:<12.4f} {data.std:<12.4f}")
    
    # Таблица размеров
    print("\n" + colorize("Размеры сборок (меньше = лучше):", "BOLD"))
    print("-" * 70)
    print(f"{'Инструмент':<15} {'Исполняемый':<15} {'Общий размер':<15}")
    print("-" * 70)
    
    sorted_size = sorted(
        size_results.items(),
        key=lambda x: x[1].total_mb if hasattr(x[1], 'total_mb') else 999
    )
    for tool, data in sorted_size:
        if hasattr(data, 'total_mb'):
            print(f"{tool:<15} {data.executable_mb:>10.2f} MB   {data.total_mb:>10.2f} MB")
    
    # Таблица времени сборки
    if build_results:
        print("\n" + colorize("Время сборки:", "BOLD"))
        print("-" * 70)
        print(f"{'Инструмент':<15} {'Время (с)':<15} {'Статус':<15}")
        print("-" * 70)
        
        for tool, data in build_results.items():
            time_s = data.get('time', 0)
            status = colorize("[OK]", "GREEN") if data.get('success') else colorize("[FAIL]", "RED")
            print(f"{tool:<15} {time_s:<15.1f} {status}")
    
    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Сборка и бенчмарки Python приложений",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python build_all.py                    # Сборка + бенчмарки
  python build_all.py --build-only       # Только сборка
  python build_all.py --test-only        # Только бенчмарки
  python build_all.py --tools pyinstaller nuitka
        """
    )
    
    parser.add_argument("--build-only", action="store_true", 
                       help="Только сборка, без бенчмарков")
    parser.add_argument("--test-only", action="store_true", 
                       help="Только бенчмарки")
    parser.add_argument("--tools", nargs="+", choices=TOOL_NAMES, 
                       default=TOOL_NAMES, help="Инструменты для сборки/теста")
    parser.add_argument("-n", type=int, default=20_000_000, 
                       help="Размер вычисления для бенчмарка")
    parser.add_argument("-k", "--iterations", type=int, default=5, 
                       help="Количество итераций бенчмарка")
    
    args = parser.parse_args()
    
    print_header("Python Build Toolkit - Сборка и тестирование")
    print(f"  Платформа: {sys.platform}")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  Инструменты: {', '.join(args.tools)}")
    print(f"  Размер N: {args.n:,}")
    print(f"  Итераций: {args.iterations}")
    
    build_results = {}
    
    # Фаза сборки
    if not args.test_only:
        print_header("Сборка приложений")
        build_results = build_all(args.tools)
    
    # Фаза бенчмарков
    if not args.build_only:
        perf_results, size_results = run_benchmarks(
            args.tools, args.n, args.iterations
        )
        save_results(perf_results, size_results, build_results)
        print_summary(perf_results, size_results, build_results)
    
    print_header("Завершено!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
