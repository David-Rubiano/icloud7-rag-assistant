from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # ==========================================
    # 1. CONFIGURACIÓN DE ALMACENAMIENTO (Storage)
    # ==========================================
    USE_S3: bool = False
    LOCAL_DOCS_DIR: str = "./data/docs"
    
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "ic7-rag-documents-bucket"

    # ==========================================
    # 2. CONFIGURACIÓN DE CHUNKING (Text Splitter)
    # ==========================================
    CHUNK_SIZE: int = 600
    CHUNK_OVERLAP: int = 100

    # ==========================================
    # 3. CONFIGURACIÓN DE CHROMADB (Vector Store)
    # ==========================================
    CHROMA_PERSIST_DIR: str = "./data/chroma_db"
    CHROMA_COLLECTION_NAME: str = "ic7_internal_docs"

    # ==========================================
    # 4. CONFIGURACIÓN DE EMBEDDINGS
    # ==========================================
    USE_LOCAL_EMBEDDINGS: bool = False
    LOCAL_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    GEMINI_EMBEDDING_MODEL: str = "models/gemini-embedding-2"  # Modelo de embeddings de Google Gemini

    # ==========================================
    # 5. CONFIGURACIÓN DEL LLM (Google Gemini)
    # ==========================================
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"

    # ==========================================
    # CONFIGURACIÓN PARA LEER EL ARCHIVO .env
    # ==========================================
    model_config = SettingsConfigDict(
        env_file=".env",             # Busca un archivo llamado .env
        env_file_encoding="utf-8",   # Codificación del archivo
        extra="ignore"               # Ignora variables extra que estén en el .env y no en la clase
    )

settings = Settings()