import subprocess
from .base import BaseParser


class DocParser(BaseParser):
    def parse(self, file_path: str) -> str:
        # Попытка использовать antiword
        try:
            result = subprocess.run(['antiword', file_path], capture_output=True, text=True, check=True)
            return result.stdout
        except (subprocess.SubprocessError, FileNotFoundError):
            # fallback: читаем как текст
            with open(file_path, 'r', encoding='cp1251', errors='ignore') as f:
                return f.read()