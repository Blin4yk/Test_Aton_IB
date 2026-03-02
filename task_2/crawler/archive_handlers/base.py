from abc import ABC, abstractmethod
from typing import Generator, Tuple, BinaryIO


class BaseArchiveHandler(ABC):
    @abstractmethod
    def list_files(self, archive_path: str) -> Generator[Tuple[str, BinaryIO], None, None]:
        """Возвращает генератор пар (имя_файла, BytesIO) для всех файлов в архиве"""
        pass