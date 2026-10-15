from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.document import RawDocument, DocumentChunk, SourceReference

class LLMPort(ABC):
    @abstractmethod
    def generate_answer(self, question: str, context_chunks: List[SourceReference]) -> str:
        pass