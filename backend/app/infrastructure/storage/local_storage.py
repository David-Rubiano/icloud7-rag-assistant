import os
from typing import List
from app.domain.interfaces.storage_port import StoragePort
from app.domain.entities.document import RawDocument
from app.infrastructure.config.settings import settings
from app.infrastructure.parsers.file_parser import FileParser

class LocalStorageAdapter(StoragePort):
    def __init__(self):
        self.docs_dir = settings.LOCAL_DOCS_DIR
        os.makedirs(self.docs_dir, exist_ok=True)

    def save_file(self, filename: str, file_bytes: bytes) -> str:
        local_path = os.path.join(self.docs_dir, filename)
        with open(local_path, "wb") as f:
            f.write(file_bytes)
        return local_path

    def load_all_documents(self) -> List[RawDocument]:
        documents: List[RawDocument] = []
        for fname in os.listdir(self.docs_dir):
            fpath = os.path.join(self.docs_dir, fname)
            if os.path.isfile(fpath) and FileParser.is_supported(fname):
                with open(fpath, "rb") as f:
                    content = FileParser.extract_text(fname, f.read())
                documents.append(
                    RawDocument(
                        filename=fname,
                        content=content,
                        metadata={"source": fname, "storage": "local"}
                    )
                )
        return documents