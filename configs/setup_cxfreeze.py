"""
Конфигурационный файл cx_Freeze.
Запуск из корня проекта: python configs/setup_cxfreeze.py build
"""

import sys
import os

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cx_Freeze import setup, Executable

# Определение базы для исполняемого файла
if sys.platform == "win32":
    base = "Win32GUI"  # Использовать "Console" для CLI режима
else:
    base = None

build_exe_options = {
    "packages": ["tkinter"],
    "excludes": ["matplotlib", "numpy", "pandas", "scipy"],
    "optimize": 2,
    "include_files": [],
}

executables = [
    Executable(
        "app.py",
        base=base,
        target_name="app",
        icon=None,
    )
]

setup(
    name="Python Build Toolkit Demo",
    version="1.0",
    description="Демо-приложение для сравнения инструментов сборки Python",
    options={"build_exe": build_exe_options},
    executables=executables,
)
