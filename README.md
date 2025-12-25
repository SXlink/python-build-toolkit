# Python Build Toolkit

Сравнение инструментов сборки Python-приложений: PyInstaller, cx_Freeze, Nuitka, PyOxidizer. Код частично написан Opus 4.5, рефакторинг был произведен также им.

## Быстрый старт

```bash
# Установка зависимостей
pip install -r requirements.txt

# Сборка и тестирование всех инструментов
python build_all.py

# Только сборка
python build_all.py --build-only

# Только бенчмарки
python build_all.py --test-only

# Конкретные инструменты
python build_all.py --tools pyinstaller nuitka
```

## Структура проекта

```
python-build-toolkit/
├── app.py                  # Точка входа приложения (для сборки)
├── compute.py              # Вычислительная функция
├── build_all.py            # Главный скрипт сборки и тестов
│
├── src/                    # Исходный код приложения
│   ├── __init__.py
│   ├── app.py              # GUI/CLI приложение
│   └── compute.py          # CPU-интенсивная функция
│
├── tools/                  # Инструменты сборки и бенчмарки
│   ├── __init__.py
│   ├── console.py          # Утилиты вывода в консоль
│   ├── builders/           # Модули сборки
│   │   ├── __init__.py
│   │   ├── base.py         # Базовый класс
│   │   ├── pyinstaller.py
│   │   ├── cxfreeze.py
│   │   ├── nuitka.py
│   │   └── pyoxidizer.py
│   └── benchmarks/         # Модули бенчмарков
│       ├── __init__.py
│       ├── performance.py
│       └── size.py
│
├── configs/                # Конфигурационные файлы
│   ├── pyinstaller.spec
│   ├── setup_cxfreeze.py
│   └── pyoxidizer.bzl
│
├── docs/                   # Документация
│   ├── CHEATSHEETS.md
│   └── FINAL_COMPARISON.md
│
├── benchmarks/             # Результаты бенчмарков
│   └── full_results.json
│
├── dist/                   # Собранные приложения
└── build/                  # Временные файлы сборки
```

## Инструменты сборки

### PyInstaller
```bash
pip install pyinstaller
pyinstaller --onefile --windowed app.py
```

### cx_Freeze
```bash
pip install cx-freeze
python configs/setup_cxfreeze.py build
```

### Nuitka
```bash
pip install nuitka
python -m nuitka --standalone --onefile --enable-plugin=tk-inter app.py
```

### PyOxidizer
```bash
pip install pyoxidizer
pyoxidizer build --release
```

## Результаты сравнения

| Инструмент | Размер | Производительность | Простота |
|------------|--------|-------------------|----------|
| **Nuitka** | ~8 MB | Средняя | ⭐⭐⭐ |
| PyInstaller | ~10 MB | Средняя | ⭐⭐⭐⭐⭐ |
| cx_Freeze | ~27 MB | Хорошая | ⭐⭐⭐⭐ |
| PyOxidizer | ~66 MB | Самая лучшая | ⭐ |

**Рекомендация:** Nuitka для минимального размера, PyInstaller для простоты.

## Демо-приложение

```bash
# GUI режим
python app.py

# CLI режим
python app.py --cli -n 1000000
```

## API инструментов

```python
from tools.builders import get_builder, BUILDERS

# Сборка с PyInstaller
builder = get_builder("pyinstaller")
result = builder.build("app.py")

# Бенчмарк
from tools.benchmarks import PerformanceBenchmark
bench = PerformanceBenchmark(n=10_000_000, iterations=3)
results = bench.run_all(["pyinstaller", "nuitka"])
```

## Документация

- [Cheatsheets](docs/CHEATSHEETS.md) — краткие справочники
- [Сравнение](docs/FINAL_COMPARISON.md) — детальное сравнение

## Лицензия

MIT License
