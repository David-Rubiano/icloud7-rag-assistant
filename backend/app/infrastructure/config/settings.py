from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Almacenamiento (AWS S3 / Local)
    USE_S3: bool = False
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "ic7-rag-documents-bucket"
    LOCAL_DOCS_DIR: str = "./data/docs"

    # Vector Store & Chunking
    CHROMA_PERSIST_DIR: str = "./data/chroma_db"
    CHROMA_COLLECTION_NAME: str = "ic7_internal_docs"
    CHUNK_SIZE: int = 600
    CHUNK_OVERLAP: int = 100

    # Embeddings & LLM
    USE_LOCAL_EMBEDDINGS: bool = True
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"

settings = Settings()