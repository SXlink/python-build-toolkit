"""
Базовый класс билдера для всех инструментов сборки.
"""

import subprocess
import sys
import os
import time
import glob
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..console import print_step, print_success, print_error


@dataclass
class BuildResult:
    """Результат операции сборки."""
    success: bool
    elapsed_time: float
    output_path: Optional[str] = None
    size_bytes: int = 0
    error_message: str = ""


class BaseBuilder(ABC):
    """Абстрактный базовый класс для инструментов сборки."""
    
    name: str = "base"
    
    @abstractmethod
    def get_build_command(self, source_file: str) -> List[str]:
        """
        Получить команду сборки для этого инструмента.
        
        Аргументы:
            source_file: Путь к исходному Python файлу
            
        Возвращает:
            Команду в виде списка строк
        """
        pass
    
    @abstractmethod
    def get_output_path(self) -> str:
        """
        Получить ожидаемый путь вывода после сборки.
        
        Возвращает:
            Путь к исполняемому файлу или директории
        """
        pass
    
    def is_installed(self) -> bool:
        """Проверить, установлен ли инструмент сборки."""
        try:
            cmd = self.get_version_command()
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            return result.returncode == 0
        except Exception:
            return False
    
    def get_version_command(self) -> List[str]:
        """Получить команду для проверки версии инструмента."""
        return [sys.executable, "-m", self.name, "--version"]
    
    def build(self, source_file: str = "app.py", timeout: int = 600) -> BuildResult:
        """
        Собрать приложение.
        
        Аргументы:
            source_file: Путь к исходному файлу
            timeout: Таймаут сборки в секундах
            
        Возвращает:
            BuildResult со статусом и деталями
        """
        print_step(f"Сборка с помощью {self.name}...")
        
        cmd = self.get_build_command(source_file)
        print(f"  Команда: {' '.join(cmd[:5])}...")
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='replace'
            )
            
            elapsed = time.time() - start_time
            
            if result.returncode != 0:
                print_error(f"Сборка не удалась (код выхода {result.returncode})")
                if result.stderr:
                    print(f"  Ошибка: {result.stderr[:500]}")
                return BuildResult(
                    success=False,
                    elapsed_time=elapsed,
                    error_message=result.stderr[:500]
                )
            
            # Проверка вывода
            output_path = self.get_output_path()
            actual_path = self._find_output(output_path)
            
            if not actual_path:
                print_error(f"Вывод не найден: {output_path}")
                return BuildResult(
                    success=False,
                    elapsed_time=elapsed,
                    error_message=f"Вывод не найден: {output_path}"
                )
            
            size = self._get_size(actual_path)
            print_success(f"Сборка завершена за {elapsed:.1f}с - Размер: {size / 1024 / 1024:.2f} MB")
            
            return BuildResult(
                success=True,
                elapsed_time=elapsed,
                output_path=actual_path,
                size_bytes=size
            )
            
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            print_error(f"Таймаут сборки после {timeout}с")
            return BuildResult(
                success=False,
                elapsed_time=elapsed,
                error_message=f"Таймаут после {timeout}с"
            )
        except Exception as e:
            elapsed = time.time() - start_time
            print_error(f"Ошибка сборки: {e}")
            return BuildResult(
                success=False,
                elapsed_time=elapsed,
                error_message=str(e)
            )
    
    def _find_output(self, pattern: str) -> Optional[str]:
        """Найти файл/директорию вывода по шаблону."""
        if os.path.exists(pattern):
            return pattern
        
        matches = glob.glob(pattern)
        return matches[0] if matches else None
    
    def _get_size(self, path: str) -> int:
        """Получить общий размер файла или директории."""
        if os.path.isfile(path):
            return os.path.getsize(path)
        
        total = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                try:
                    total += os.path.getsize(os.path.join(dirpath, f))
                except OSError:
                    pass
        return total
