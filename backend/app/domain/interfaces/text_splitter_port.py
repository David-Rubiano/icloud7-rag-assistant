from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.document import RawDocument, DocumentChunk

class TextSplitterPort(ABC):
    @abstractmethod
    def split_documents(self, documents: List[RawDocument]) -> List[DocumentChunk]:
        """Divide una lista de documentos crudos en fragmentos (chunks) indexables."""
        pass