from abc import ABC, abstractmethod

from logger import logger


class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> str:
        """Извлекает текст из файла"""
        pass

    def safe_parse(self, file_path: str) -> str | None:
        """Обёртка с обработкой ошибок"""
        try:
            return self.parse(file_path)
        except Exception as e:
            logger.error(f"Ошибка парсинга {file_path}: {e}")
            return None
