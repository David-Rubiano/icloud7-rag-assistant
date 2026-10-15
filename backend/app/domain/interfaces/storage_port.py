from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.document import RawDocument, DocumentChunk, SourceReference

class StoragePort(ABC):
    @abstractmethod
    def save_file(self, filename: str, file_bytes: bytes) -> str:
        """Guarda un archivo en el medio de almacenamiento y retorna su ruta o URI."""
        pass

    @abstractmethod
    def load_all_documents(self) -> List[RawDocument]:
        """Carga y extrae el texto de todos los documentos almacenados."""
        pass