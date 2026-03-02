import zipfile
import io
from .base import BaseArchiveHandler


class ZipHandler(BaseArchiveHandler):
    def list_files(self, archive_path: str):
        with zipfile.ZipFile(archive_path, 'r') as zf:
            for name in zf.namelist():
                if not name.endswith('/'):  # пропускаем директории
                    with zf.open(name) as f:
                        yield name, io.BytesIO(f.read())