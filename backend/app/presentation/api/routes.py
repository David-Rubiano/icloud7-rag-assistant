from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.application.upload_document_uc import UploadDocumentUseCase
from app.application.index_documents_uc import IndexDocumentsUseCase
from app.application.ask_question_uc import AskQuestionUseCase

# Importamos las dependencias cacheadas
from app.presentation.api.dependencies import (
    get_local_storage, get_s3_storage, 
    get_splitter, get_vector_store, get_llm
)
from app.presentation.schemas.dto import (
    UploadResponseDTO, IndexResponseDTO, QuestionRequestDTO, AnswerResponseDTO, SourceResponseDTO
)

router = APIRouter()

@router.post("/upload", response_model=UploadResponseDTO)
async def upload_document(
    use_s3: bool = False,  # <-- Recibimos la decisión desde la UI
    file: UploadFile = File(...)
):
    try:
        # Elegimos el adaptador dinámicamente según la preferencia del usuario
        storage = get_s3_storage() if use_s3 else get_local_storage()
        use_case = UploadDocumentUseCase(storage=storage)
        
        content = await file.read()
        result = use_case.execute(filename=file.filename, file_bytes=content)
        return UploadResponseDTO(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo archivo: {str(e)}")


@router.post("/proceso_index", response_model=IndexResponseDTO)
def index_documents(use_s3: bool = False): # <-- Recibimos la decisión desde la UI
    try:
        storage = get_s3_storage() if use_s3 else get_local_storage()
        use_case = IndexDocumentsUseCase(
            storage=storage,
            splitter=get_splitter(),
            vector_store=get_vector_store()
        )
        result = use_case.execute()
        return IndexResponseDTO(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en indexación: {str(e)}")


@router.post("/Preguntar", response_model=AnswerResponseDTO)
def ask_question(request: QuestionRequestDTO):
    try:
        # El endpoint preguntar no usa S3/Local, solo ChromaDB (vector_store)
        use_case = AskQuestionUseCase(
            vector_store=get_vector_store(),
            llm=get_llm()
        )
        result = use_case.execute(question=request.question, top_k=request.top_k)
        return AnswerResponseDTO(
            question=result.question,
            answer=result.answer,
            sources=[
                SourceResponseDTO(
                    document_name=s.document_name,
                    fragment_preview=s.fragment_preview,
                    similarity_score=s.score
                )
                for s in result.sources
            ]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la pregunta: {str(e)}")