from docx import Document
from .base import BaseParser


class DocxParser(BaseParser):
    def parse(self, file_path: str) -> str:
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])