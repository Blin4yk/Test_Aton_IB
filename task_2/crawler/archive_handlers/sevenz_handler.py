import py7zr
from .base import BaseArchiveHandler


class SevenZHandler(BaseArchiveHandler):
    def list_files(self, archive_path: str):
        with py7zr.SevenZipFile(archive_path, mode='r') as sz:
            for name, bio in sz.readall().items():
                # bio - это BytesIO объекта
                yield name, bio