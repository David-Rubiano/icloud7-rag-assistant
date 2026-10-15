from functools import lru_cache

# Puertos
from app.domain.interfaces.storage_port import StoragePort
from app.domain.interfaces.text_splitter_port import TextSplitterPort
from app.domain.interfaces.vector_store_port import VectorStorePort
from app.domain.interfaces.llm_port import LLMPort

# Adaptadores
from app.infrastructure.storage.local_storage import LocalStorageAdapter
from app.infrastructure.storage.s3_storage import S3StorageAdapter
from app.infrastructure.rag.langchain_splitter import LangChainSplitterAdapter
from app.infrastructure.rag.chroma_vector_store import ChromaVectorStoreAdapter
from app.infrastructure.rag.langchain_llm import LangChainLLMAdapter

# Singletons en memoria con @lru_cache
@lru_cache()
def get_local_storage() -> StoragePort:
    return LocalStorageAdapter()

@lru_cache()
def get_s3_storage() -> StoragePort:
    return S3StorageAdapter()

@lru_cache()
def get_splitter() -> TextSplitterPort:
    return LangChainSplitterAdapter()

@lru_cache()
def get_vector_store() -> VectorStorePort:
    return ChromaVectorStoreAdapter()

@lru_cache()
def get_llm() -> LLMPort:
    return LangChainLLMAdapter()