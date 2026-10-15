from pydantic import BaseModel, Field
from typing import List


# --- DTOs para /upload ---
class UploadResponseDTO(BaseModel):
    filename: str = Field(..., description="Nombre del archivo subido (PDF, TXT o MD)")
    storage_path: str = Field(..., description="Ruta local o URI de Amazon S3 donde se guardó")
    status: str = Field(..., example="uploaded")


# --- DTOs para /proceso_index ---
class IndexResponseDTO(BaseModel):
    documents_processed: int = Field(..., description="Total de documentos leídos")
    chunks_indexed: int = Field(..., description="Total de fragmentos guardados en ChromaDB")
    status: str = Field(..., example="indexed_successfully")


# --- DTOs para /Preguntar ---
class QuestionRequestDTO(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="Pregunta del usuario sobre el contenido de los documentos",
        examples=["¿Cuántos días de vacaciones remuneradas tiene un empleado por año?"]
    )
    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Cantidad de fragmentos relevantes a recuperar por similitud (KNN)"
    )


class SourceResponseDTO(BaseModel):
    document_name: str = Field(..., description="Nombre del documento fuente original")
    fragment_preview: str = Field(..., description="Texto del fragmento recuperado de ChromaDB")
    similarity_score: float = Field(..., description="Puntaje de distancia/similitud KNN")


class AnswerResponseDTO(BaseModel):
    question: str = Field(..., description="Pregunta original realizada")
    answer: str = Field(..., description="Respuesta generada por el LLM basada en el contexto")
    sources: List[SourceResponseDTO] = Field(
        default_factory=list,
        description="Lista de fragmentos y documentos usados como referencia"
    )