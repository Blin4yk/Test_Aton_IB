import csv
import os
import shutil
import tempfile

from crawler.archive_handlers import ZipHandler, RarHandler, SevenZHandler
from crawler.file_parsers import (
    DocParser, DocxParser, XLSParser, XLSXParser, PDFParser
)
from logger import logger


class Crawler:
    SUPPORTED_EXTENSIONS = {
        '.doc': DocParser(),
        '.docx': DocxParser(),
        '.xls': XLSParser(),
        '.xlsx': XLSXParser(),
        '.pdf': PDFParser(),
    }
    ARCHIVE_HANDLERS = {
        '.zip': ZipHandler(),
        '.rar': RarHandler(),
        '.7z': SevenZHandler(),
    }

    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.temp_dir = tempfile.mkdtemp(prefix="crawler_")

    def __del__(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def crawl(self) -> list[dict[str, any]]:
        results = []
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                self._process_file(file_path, results, base_path=self.root_dir)
        return results

    def _process_file(self, file_path: str, results: list[dict], base_path: str, archive_context: str | None = None):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in self.ARCHIVE_HANDLERS:
            self._process_archive(file_path, results, base_path, archive_context)
        elif ext in self.SUPPORTED_EXTENSIONS:
            self._process_document(file_path, results, base_path, archive_context)
        else:
            logger.debug(f"Неподдерживаемый тип файла: {file_path}")

    def _process_document(self, file_path: str, results: list[dict], base_path: str,
                          archive_context: str | None = None):
        parser = self.SUPPORTED_EXTENSIONS.get(os.path.splitext(file_path)[1].lower())
        if not parser:
            return

        logger.info(f"Парсинг документа: {file_path}")
        content = parser.safe_parse(file_path)
        if content is None:
            return

        # Формируем относительный путь
        if archive_context:
            display_path = f"{archive_context}/{os.path.basename(file_path)}"
        else:
            display_path = os.path.relpath(file_path, base_path)

        results.append({
            'file_path': display_path,
            'file_name': os.path.basename(file_path),
            'file_type': os.path.splitext(file_path)[1],
            'content': content
        })

    def _process_archive(self, archive_path: str, results: list[dict], base_path: str,
                         parent_context: str | None = None):
        handler = self.ARCHIVE_HANDLERS.get(os.path.splitext(archive_path)[1].lower())
        if not handler:
            return

        logger.info(f"Процесс арзивации: {archive_path}")
        try:
            for file_name, file_bytes in handler.list_files(archive_path):
                # Создаём временный файл для обработки
                temp_file = os.path.join(self.temp_dir, file_name)
                os.makedirs(os.path.dirname(temp_file), exist_ok=True)
                with open(temp_file, 'wb') as f:
                    f.write(file_bytes.read())

                # Формируем контекст для отображения пути внутри архива
                if parent_context:
                    new_context = f"{parent_context}/{os.path.basename(archive_path)}"
                else:
                    new_context = os.path.relpath(archive_path, base_path)

                self._process_file(temp_file, results, base_path, archive_context=new_context)
        except Exception as e:
            logger.error(f"Ошибка архивации {archive_path}: {e}")

    @staticmethod
    def save_to_csv(data: list[dict[str, any]], csv_path: str):
        if not data:
            logger.warning("Нет данных для сохранения")
            return
        keys = data[0].keys()
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
