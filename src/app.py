"""
Главное приложение с поддержкой GUI и CLI.
"""

import sys
import time
import argparse

from .compute import compute


def run_cli(n: int = 1000000) -> float:
    """
    Запуск вычисления в режиме CLI.
    
    Аргументы:
        n: Верхняя граница вычисления
        
    Возвращает:
        Время выполнения в секундах
    """
    print(f"Вычисление суммы квадратов от 1 до {n}...")
    start_time = time.time()
    result = compute(n)
    elapsed_time = time.time() - start_time
    print(f"Результат: {result}")
    print(f"Время выполнения: {elapsed_time:.4f} секунд")
    return elapsed_time


def run_gui():
    """Запуск вычисления в GUI режиме с Tkinter."""
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
    except ImportError:
        print("Tkinter недоступен. Установите его или используйте CLI режим.")
        sys.exit(1)
    
    def on_compute():
        """Обработка нажатия кнопки вычисления."""
        try:
            n = int(entry_n.get())
            if n <= 0:
                messagebox.showerror("Ошибка", "Введите положительное число")
                return
            
            # Отключение кнопок во время вычисления
            btn_compute.config(state=tk.DISABLED)
            btn_exit.config(state=tk.DISABLED)
            result_label.config(text="Вычисление...")
            time_label.config(text="")
            root.update()
            
            # Выполнение вычисления
            start_time = time.time()
            result = compute(n)
            elapsed_time = time.time() - start_time
            
            # Обновление интерфейса
            result_label.config(text=f"Результат: {result:,}")
            time_label.config(text=f"Время: {elapsed_time:.4f} секунд")
            
            # Включение кнопок
            btn_compute.config(state=tk.NORMAL)
            btn_exit.config(state=tk.NORMAL)
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число")
            btn_compute.config(state=tk.NORMAL)
            btn_exit.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            btn_compute.config(state=tk.NORMAL)
            btn_exit.config(state=tk.NORMAL)
    
    def on_exit():
        """Обработка нажатия кнопки выхода."""
        root.quit()
        root.destroy()
    
    # Создание главного окна
    root = tk.Tk()
    root.title("Python Build Toolkit - Демо вычислений")
    root.geometry("500x300")
    root.resizable(False, False)
    
    # Главный фрейм
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Заголовок
    title_label = ttk.Label(
        main_frame, 
        text="Калькулятор суммы квадратов",
        font=("Arial", 16, "bold")
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
    # Поле ввода
    ttk.Label(main_frame, text="Введите n (верхняя граница):").grid(
        row=1, column=0, sticky=tk.W, pady=5
    )
    entry_n = ttk.Entry(main_frame, width=20)
    entry_n.insert(0, "1000000")
    entry_n.grid(row=1, column=1, pady=5, padx=(10, 0))
    
    # Кнопки
    btn_frame = ttk.Frame(main_frame)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
    
    btn_compute = ttk.Button(btn_frame, text="Вычислить", command=on_compute, width=15)
    btn_compute.pack(side=tk.LEFT, padx=5)
    
    btn_exit = ttk.Button(btn_frame, text="Выход", command=on_exit, width=15)
    btn_exit.pack(side=tk.LEFT, padx=5)
    
    # Отображение результата
    result_label = ttk.Label(main_frame, text="Результат: -", font=("Arial", 12))
    result_label.grid(row=3, column=0, columnspan=2, pady=10)
    
    time_label = ttk.Label(main_frame, text="", font=("Arial", 10))
    time_label.grid(row=4, column=0, columnspan=2, pady=5)
    
    # Запуск GUI
    root.mainloop()


def main():
    """Главная точка входа."""
    parser = argparse.ArgumentParser(description="Демо Python Build Toolkit")
    parser.add_argument("--cli", action="store_true", help="Запуск в режиме CLI")
    parser.add_argument(
        "-n", type=int, default=1000000, 
        help="Верхняя граница вычисления (режим CLI)"
    )
    
    args = parser.parse_args()
    
    if args.cli:
        run_cli(args.n)
    else:
        run_gui()


if __name__ == "__main__":
    main()
