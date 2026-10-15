from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class RawDocument:
    filename: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DocumentChunk:
    chunk_id: str
    document_name: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SourceReference:
    document_name: str
    fragment_preview: str
    score: float

@dataclass
class RAGResponse:
    question: str
    answer: str
    sources: List[SourceReference]