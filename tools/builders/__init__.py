"""
Реализации инструментов сборки.
"""

from .base import BaseBuilder, BuildResult
from .pyinstaller import PyInstallerBuilder
from .cxfreeze import CxFreezeBuilder
from .nuitka import NuitkaBuilder
from .pyoxidizer import PyOxidizerBuilder

__all__ = [
    "BaseBuilder",
    "BuildResult",
    "PyInstallerBuilder",
    "CxFreezeBuilder",
    "NuitkaBuilder",
    "PyOxidizerBuilder",
]

# Реестр доступных билдеров
BUILDERS = {
    "pyinstaller": PyInstallerBuilder,
    "cxfreeze": CxFreezeBuilder,
    "nuitka": NuitkaBuilder,
    "pyoxidizer": PyOxidizerBuilder,
}


def get_builder(name: str) -> BaseBuilder:
    """
    Получить экземпляр билдера по имени.
    
    Аргументы:
        name: Имя билдера (pyinstaller, cxfreeze, nuitka, pyoxidizer)
        
    Возвращает:
        Экземпляр билдера
        
    Исключения:
        ValueError: Если имя билдера неизвестно
    """
    if name not in BUILDERS:
        raise ValueError(f"Неизвестный билдер: {name}. Доступные: {list(BUILDERS.keys())}")
    return BUILDERS[name]()
