from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.api.routes import router

app = FastAPI(
    title="I Cloud Seven - Asistente Documental RAG",
    description="Backend REST API con Clean Architecture, FastAPI, LangChain, ChromaDB y Boto3",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "ic7-rag-backend"}