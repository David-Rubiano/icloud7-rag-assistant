from functools import lru_cache

# 1. Puertos del Dominio (Interfaces Abstractas)
from app.domain.interfaces.storage_port import StoragePort
from app.domain.interfaces.text_splitter_port import TextSplitterPort
from app.domain.interfaces.vector_store_port import VectorStorePort
from app.domain.interfaces.llm_port import LLMPort

# 2. Configuración e Infraestructura (Adaptadores Concretos)
from app.infrastructure.config.settings import settings
from app.infrastructure.storage.local_storage import LocalStorageAdapter
from app.infrastructure.storage.s3_storage import S3StorageAdapter
from app.infrastructure.rag.langchain_splitter import LangChainSplitterAdapter
from app.infrastructure.rag.chroma_vector_store import ChromaVectorStoreAdapter
from app.infrastructure.rag.langchain_llm import LangChainLLMAdapter

# 3. Casos de Uso (Capa de Aplicación)
from app.application.upload_document_uc import UploadDocumentUseCase
from app.application.index_documents_uc import IndexDocumentsUseCase
from app.application.ask_question_uc import AskQuestionUseCase


# --- PROVEEDORES DE INFRAESTRUCTURA (Singletons en memoria con @lru_cache) ---

@lru_cache()
def get_storage() -> StoragePort:
    """Retorna el adaptador de S3 o Local según la variable USE_S3 del .env"""
    if settings.USE_S3:
        return S3StorageAdapter()
    return LocalStorageAdapter()

@lru_cache()
def get_splitter() -> TextSplitterPort:
    """Retorna el adaptador de fragmentación con RecursiveCharacterTextSplitter"""
    return LangChainSplitterAdapter()

@lru_cache()
def get_vector_store() -> VectorStorePort:
    """Retorna el adaptador de ChromaDB (con Embeddings de Gemini o HuggingFace)"""
    return ChromaVectorStoreAdapter()

@lru_cache()
def get_llm() -> LLMPort:
    """Retorna el adaptador del modelo generativo (Google Gemini)"""
    return LangChainLLMAdapter()


# --- PROVEEDORES DE CASOS DE USO (Para inyectar con Depends() en FastAPI) ---

def get_upload_uc() -> UploadDocumentUseCase:
    return UploadDocumentUseCase(storage=get_storage())

def get_index_uc() -> IndexDocumentsUseCase:
    return IndexDocumentsUseCase(
        storage=get_storage(),
        splitter=get_splitter(),
        vector_store=get_vector_store()
    )

def get_ask_uc() -> AskQuestionUseCase:
    return AskQuestionUseCase(
        vector_store=get_vector_store(),
        llm=get_llm()
    )