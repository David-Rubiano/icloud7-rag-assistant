import io
from pypdf import PdfReader

class FileParser:
    SUPPORTED_EXTENSIONS = (".pdf", ".txt", ".md")

    @classmethod
    def is_supported(cls, filename: str) -> bool:
        return filename.lower().endswith(cls.SUPPORTED_EXTENSIONS)

    @staticmethod
    def extract_text(filename: str, file_bytes: bytes) -> str:
        if filename.lower().endswith(".pdf"):
            reader = PdfReader(io.BytesIO(file_bytes))
            return "\n".join([page.extract_text() or "" for page in reader.pages])
        
        # Para archivos .txt y .md
        return file_bytes.decode("utf-8", errors="ignore")