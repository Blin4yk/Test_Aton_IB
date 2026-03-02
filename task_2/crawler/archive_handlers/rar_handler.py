import rarfile
import io
from .base import BaseArchiveHandler


class RarHandler(BaseArchiveHandler):
    def list_files(self, archive_path: str):
        with rarfile.RarFile(archive_path) as rf:
            for name in rf.namelist():
                if not name.endswith('/'):
                    with rf.open(name) as f:
                        yield name, io.BytesIO(f.read())