# icloud7-rag-assistant

## Estructura de proyecto:

ic7-rag-assistant/
├── backend/
│   ├── app/
│   │   ├── domain/                  # Reglas de negocio puras (Sin dependencias externas)
│   │   │   ├── entities/
│   │   │   │   └── document.py      # Entidades: Document, DocumentChunk, QueryResult
│   │   │   └── interfaces/          # Puertos (Interfaces Abstractas - Principio DIP)
│   │   │       ├── storage_port.py
│   │   │       ├── vector_store_port.py
│   │   │       ├── text_splitter_port.py
│   │   │       └── llm_port.py
│   │   ├── application/             # Casos de Uso (Orquestación de negocio - Principio SRP)
│   │   │   ├── upload_document_uc.py
│   │   │   ├── index_documents_uc.py
│   │   │   └── ask_question_uc.py
│   │   ├── infrastructure/          # Adaptadores concretos (Boto3, LangChain, ChromaDB)
│   │   │   ├── config/
│   │   │   │   └── settings.py
│   │   │   ├── storage/
│   │   │   │   ├── s3_storage.py    # Sincronización Boto3 con fallback local
│   │   │   │   └── local_storage.py
│   │   │   ├── rag/
│   │   │   │   ├── langchain_splitter.py
│   │   │   │   ├── chroma_vector_store.py
│   │   │   │   └── langchain_llm.py
│   │   │   └── parsers/
│   │   │       └── file_parser.py   # Lectura de PDF, TXT y MD
│   │   └── presentation/            # API REST con FastAPI
│   │       ├── api/
│   │       │   ├── routes.py        # Endpoints: /upload, /proceso_index, /Preguntar
│   │       │   └── dependencies.py  # Inyección de dependencias
│   │       └── schemas/
│   │           └── dto.py           # Modelos Pydantic
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                        # Contenedor Streamlit
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── docs/                            # Documentos de prueba y entregables
│   ├── politicas_vacaciones.md
│   ├── manual_onboarding.txt
│   └── PRUEBAS_Y_RESULTADOS.md      # Entregable 4.4 y 4.3
├── docker-compose.yml
├── .env.example
└── README.md                        # Entregable 4.5