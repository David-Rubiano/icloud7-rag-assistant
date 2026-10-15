from app.domain.interfaces.storage_port import StoragePort
from app.domain.interfaces.text_splitter_port import TextSplitterPort
from app.domain.interfaces.vector_store_port import VectorStorePort

class IndexDocumentsUseCase:
    def __init__(self, storage: StoragePort, splitter: TextSplitterPort, vector_store: VectorStorePort):
        self.storage = storage
        self.splitter = splitter
        self.vector_store = vector_store

    def execute(self) -> dict:
        documents = self.storage.load_all_documents()
        if not documents:
            raise ValueError("No hay documentos cargados para indexar.")
        
        chunks = self.splitter.split_documents(documents)
        total_indexed = self.vector_store.save_chunks(chunks)
        return {
            "documents_processed": len(documents),
            "chunks_indexed": total_indexed,
            "status": "indexed_successfully"
        }