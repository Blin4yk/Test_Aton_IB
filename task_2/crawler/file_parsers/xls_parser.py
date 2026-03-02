import xlrd
from .base import BaseParser


class XLSParser(BaseParser):
    def parse(self, file_path: str) -> str:
        workbook = xlrd.open_workbook(file_path)
        sheets_text = []
        for sheet in workbook.sheets():
            for row in range(sheet.nrows):
                row_values = sheet.row_values(row)
                sheets_text.append(' '.join(str(v) for v in row_values))
        return '\n'.join(sheets_text)