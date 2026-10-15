from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.document import RawDocument, DocumentChunk, SourceReference

class TextSplitterPort(ABC):
    @abstractmethod
    def split_documents(self, documents: List[RawDocument]) -> List[DocumentChunk]:
        pass