from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.document import DocumentChunk, SourceReference

class VectorStorePort(ABC):
    @abstractmethod
    def save_chunks(self, chunks: List[DocumentChunk]) -> int:
        """Genera embeddings y persiste los fragmentos en el vector store."""
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 3) -> List[SourceReference]:
        """Realiza una búsqueda por similitud (KNN) y retorna los fragmentos más relevantes."""
        pass