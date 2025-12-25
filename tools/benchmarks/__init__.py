"""
Утилиты бенчмаркинга для сравнения производительности и размера.
"""

from .performance import PerformanceBenchmark
from .size import SizeBenchmark

__all__ = ["PerformanceBenchmark", "SizeBenchmark"]
