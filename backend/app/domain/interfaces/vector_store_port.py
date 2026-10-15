from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.document import RawDocument, DocumentChunk, SourceReference

class VectorStorePort(ABC):
    @abstractmethod
    def save_chunks(self, chunks: List[DocumentChunk]) -> int:
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 3) -> List[SourceReference]:
        pass