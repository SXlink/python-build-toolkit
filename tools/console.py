"""
Утилиты вывода в консоль с цветами и форматированием.
"""

import sys
import os


# ANSI коды цветов
COLORS = {
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "CYAN": "\033[96m",
    "BOLD": "\033[1m",
    "RESET": "\033[0m",
}

# Включение ANSI цветов на Windows
if sys.platform == "win32":
    os.system("")


def colorize(text: str, color: str) -> str:
    """
    Добавляет ANSI цвет к тексту.
    
    Аргументы:
        text: Текст для окрашивания
        color: Название цвета (GREEN, RED, YELLOW, BLUE, CYAN, BOLD)
        
    Возвращает:
        Окрашенную строку текста
    """
    return f"{COLORS.get(color, '')}{text}{COLORS['RESET']}"


def print_header(text: str):
    """Вывод стилизованного заголовка с разделителями."""
    print("\n" + "=" * 80)
    print(colorize(f"  {text}", "BOLD"))
    print("=" * 80)


def print_step(text: str):
    """Вывод индикатора шага голубым цветом."""
    print(colorize(f"\n>> {text}", "CYAN"))


def print_success(text: str):
    """Вывод сообщения об успехе зелёным цветом."""
    print(colorize(f"[OK] {text}", "GREEN"))


def print_error(text: str):
    """Вывод сообщения об ошибке красным цветом."""
    print(colorize(f"[FAIL] {text}", "RED"))


def print_warning(text: str):
    """Вывод предупреждения жёлтым цветом."""
    print(colorize(f"[WARN] {text}", "YELLOW"))


def print_table(headers: list, rows: list, col_widths: list = None):
    """
    Вывод форматированной таблицы.
    
    Аргументы:
        headers: Список заголовков столбцов
        rows: Список данных строк (каждая строка — список)
        col_widths: Опциональный список ширин столбцов
    """
    if not col_widths:
        col_widths = [max(len(str(h)), max(len(str(r[i])) for r in rows))
                      for i, h in enumerate(headers)]
    
    # Заголовок
    header_line = " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
    print(header_line)
    print("-" * len(header_line))
    
    # Строки
    for row in rows:
        print(" | ".join(f"{str(c):<{w}}" for c, w in zip(row, col_widths)))
