from app.domain.interfaces.storage_port import StoragePort

class UploadDocumentUseCase:
    def __init__(self, storage: StoragePort):
        self.storage = storage

    def execute(self, filename: str, file_bytes: bytes) -> dict:
        allowed_extensions = (".pdf", ".txt", ".md")
        if not filename.lower().endswith(allowed_extensions):
            raise ValueError(f"Formato no soportado. Use: {allowed_extensions}")
        
        path = self.storage.save_file(filename, file_bytes)
        return {"filename": filename, "storage_path": path, "status": "uploaded"}