# Шпаргалки по инструментам сборки Python

## PyInstaller

**Команды сборки:**
```bash
# Базовая сборка
pyinstaller app.py

# Один файл
pyinstaller --onefile app.py

# Без консоли (GUI)
pyinstaller --windowed app.py

# С spec файлом
pyinstaller configs/pyinstaller.spec
```

**Флаги:**
| Флаг | Описание |
|------|----------|
| `--onefile` | Один исполняемый файл |
| `--windowed` / `-w` | Скрыть консоль (GUI) |
| `--console` / `-c` | Показать консоль (CLI) |
| `--name` | Имя выходного файла |
| `--icon` | Путь к иконке |
| `--hidden-import` | Добавить скрытые импорты |
| `--exclude-module` | Исключить модули |

**Типичные ошибки:**
- `ModuleNotFoundError` → добавьте `--hidden-import`
- Большой размер → `--exclude-module` для неиспользуемых библиотек

---

## cx_Freeze

**Команды сборки:**
```bash
# Через setup.py
python configs/setup_cxfreeze.py build

# Напрямую
cxfreeze app.py --target-dir dist
```

**Флаги:**
| Флаг | Описание |
|------|----------|
| `--target-dir` | Директория для сборки |
| `--include-modules` | Включить модули |
| `--exclude-modules` | Исключить модули |
| `--optimize` | Уровень оптимизации (0-2) |

---

## Nuitka

**Команды сборки:**
```bash
# Standalone один файл
python -m nuitka --standalone --onefile app.py

# С GUI плагином
python -m nuitka --standalone --onefile --enable-plugin=tk-inter app.py

# Windows без консоли
python -m nuitka --standalone --onefile --windows-disable-console app.py

# macOS bundle
python -m nuitka --macos-create-app-bundle app.py
```

**Флаги:**
| Флаг | Описание |
|------|----------|
| `--standalone` | Standalone версия |
| `--onefile` | Один файл |
| `--enable-plugin=tk-inter` | Поддержка Tkinter |
| `--windows-disable-console` | Скрыть консоль (Windows) |
| `--assume-yes-for-downloads` | Авто-скачивание |

---

## PyOxidizer

**Команды сборки:**
```bash
# Сборка
pyoxidizer build

# Release сборка
pyoxidizer build --release

# Запуск
pyoxidizer run
```

**Требования:**
- Rust toolchain (установка через rustup)
- Файл конфигурации `pyoxidizer.bzl`
