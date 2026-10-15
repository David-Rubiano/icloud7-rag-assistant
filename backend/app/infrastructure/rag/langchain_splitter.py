from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.domain.interfaces.text_splitter_port import TextSplitterPort
from app.domain.entities.document import RawDocument, DocumentChunk
from app.infrastructure.config.settings import settings

class LangChainSplitterAdapter(TextSplitterPort):
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def split_documents(self, documents: List[RawDocument]) -> List[DocumentChunk]:
        chunks: List[DocumentChunk] = []
        for doc in documents:
            split_texts = self.splitter.split_text(doc.content)
            for idx, text in enumerate(split_texts):
                chunks.append(
                    DocumentChunk(
                        # Generación de ID determinista (sin UUID aleatorio)
                        chunk_id=f"{doc.filename}_chunk_{idx}",
                        document_name=doc.filename,
                        content=text,
                        metadata={
                            **doc.metadata,
                            "source": doc.filename,
                            "chunk_index": idx
                        }
                    )
                )
        return chunks