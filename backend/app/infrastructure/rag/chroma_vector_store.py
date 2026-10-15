from typing import List
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.domain.interfaces.vector_store_port import VectorStorePort
from app.domain.entities.document import DocumentChunk, SourceReference
from app.infrastructure.config.settings import settings

class ChromaVectorStoreAdapter(VectorStorePort):
    def __init__(self):
        self.embeddings = self._initialize_embeddings()
        self.vector_store = Chroma(
            collection_name=settings.CHROMA_COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=settings.CHROMA_PERSIST_DIR
        )

    def _initialize_embeddings(self):
        # Opción 1: Embeddings Locales en CPU (Sin API Key)
        if settings.USE_LOCAL_EMBEDDINGS:
            return HuggingFaceEmbeddings(
                model_name=settings.LOCAL_EMBEDDING_MODEL
            )
        
        # Opción 2: Embeddings vía API de Google Gemini (Gratis con tu GOOGLE_API_KEY)
        if not settings.GOOGLE_API_KEY:
            raise ValueError("Falta configurar GOOGLE_API_KEY en el archivo .env para usar Gemini Embeddings.")
            
        return GoogleGenerativeAIEmbeddings(
            model=settings.GEMINI_EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY
        )

    def save_chunks(self, chunks: List[DocumentChunk]) -> int:
        if not chunks:
            return 0
        texts = [c.content for c in chunks]
        metadatas = [c.metadata for c in chunks]
        ids = [c.chunk_id for c in chunks]
        self.vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
        return len(chunks)

    def similarity_search(self, query: str, k: int = 3) -> List[SourceReference]:
        results = self.vector_store.similarity_search_with_score(query, k=k)
        sources: List[SourceReference] = []
        for doc, score in results:
            sources.append(
                SourceReference(
                    document_name=doc.metadata.get("source", "Desconocido"),
                    fragment_preview=doc.page_content,
                    score=round(float(score), 4)
                )
            )
        return sources