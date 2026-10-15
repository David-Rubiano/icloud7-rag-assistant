# ☁️ Asistente Documental RAG - I Cloud Seven (Prueba Técnica)

Este proyecto es un asistente documental basado en Inteligencia Artificial (RAG) diseñado para el rol de **AI Developer Engineer Junior** en I Cloud Seven. Permite a los usuarios cargar documentos (PDF, TXT, MD), indexarlos en una base de datos vectorial local, y realizar preguntas sobre su contenido obteniendo respuestas precisas y estrictamente limitadas a la información proporcionada.

## 1. Descripción de la Solución

La solución consta de una arquitectura de microservicios con dos contenedores principales:
1. **Frontend (Streamlit):** Interfaz gráfica intuitiva que permite seleccionar entre almacenamiento local o AWS S3, cargar documentos, ejecutar el proceso de indexación y chatear con los documentos.
2. **Backend (FastAPI):** Servidor REST API *stateless* construido bajo los principios de **Clean Architecture** y **SOLID**. Orquesta el motor RAG utilizando LangChain, ChromaDB y Google Gemini (API Gratuita).

## 2. Arquitectura del Proyecto (Clean Architecture & Principios SOLID)

A continuación se presenta el diagrama arquitectónico de la solución. Aunque para facilitar esta evaluación técnica el proyecto se entrega contenerizado para su ejecución local (Docker Compose), el diseño del sistema es **100% Cloud-Ready**. 

[Diagrama de Arquitectura](./docs/Arquitectura_Asistente_Cloud_Seven_drawio.png)

Como se ilustra en el diagrama, los componentes están completamente desacoplados, lo que permite una transición directa hacia un entorno de producción en AWS:
* **Despliegue de Contenedores:** El Frontend (Streamlit) y Backend (FastAPI) pueden ser migrados directamente a servicios gestionados como **Amazon ECS (Fargate)**, **EKS** o **App Runner**.
* **Almacenamiento Híbrido:** Gracias a la inyección de dependencias implementada en la capa de infraestructura, el sistema ya es capaz de alternar entre el disco duro local y **Amazon S3** con solo cambiar un parámetro, sin tocar la lógica de negocio.
* **Modularidad del Motor RAG:** La separación en capas (*Domain, Application, Infrastructure, Presentation*) asegura que el LLM (Gemini) o la base de datos vectorial (ChromaDB) puedan ser reemplazados por alternativas empresariales (como AWS Bedrock, Azure Foundry o Pinecone, etc) de forma transparente.

El backend está diseñado para ser modular y escalable, dividiendo responsabilidades en capas claras para facilitar el mantenimiento y la inyección de dependencias (DIP):
* **Domain:** Entidades puras y Puertos (Interfaces abstractas para Storage, LLM, VectorStore y TextSplitter).
* **Application:** Casos de Uso aislados (UploadDocument, IndexDocuments, AskQuestion) que no dependen de ningún framework externo.
* **Infrastructure:** Adaptadores concretos (`Boto3` para S3, `ChromaDB`, `HuggingFaceEmbeddings` / `GoogleGenerativeAIEmbeddings`, `ChatGoogleGenerativeAI`).
* **Presentation:** Endpoints de FastAPI y validación de esquemas con Pydantic (DTOs).

## 3. Requisitos Previos
* Docker y Docker Compose instalados.
* *Opcional:* Python 3.11 si se desea ejecutar sin Docker.

## 4. Configuración y Variables de Entorno

Para facilitar la ejecución inmediata por parte del equipo evaluador sin requerir tarjetas de crédito ni descargas pesadas, el proyecto está preconfigurado para usar **Google Gemini 3.5 Flash Lite** (gratuito) y almacenamiento local por defecto.

1. Copia el archivo de ejemplo a `.env` en la carpeta `backend/`:
   ```bash
   cp backend/.env.example backend/.env

## 5. Pasos de Instalación y Ejecución
La forma recomendada de probar la solución es a través de Docker Compose, el cual construirá y levantará ambos servicios y los comunicará en una red interna privada.


```
# 1. Clonar el repositorio
git clone https://github.com/David-Rubiano/icloud7-rag-assistant
cd ic7-rag-assistant

# 2. Construir y levantar los contenedores
docker compose up --build
```

Una vez que los contenedores estén corriendo, accede a:

- 🖥️ Interfaz de Usuario (Streamlit): http://localhost:8501

- ⚙️ Documentación API (Swagger): http://localhost:8000/docs

## 6. Guía de Uso Rápido

1. Selección de Almacenamiento: En la barra lateral de Streamlit, elige entre "Local" o "AWS S3".

2. Cargar Documentos: Arrastra archivos PDF, TXT o MD (se recomiendan los ubicados en la carpeta docs/ de este repositorio) y presiona "Subir Documentos".

3. Indexación: Presiona el botón amarillo "Ejecutar /proceso_index" para extraer el texto, aplicar el chunking determinista y guardar los vectores en ChromaDB.

4. Hacer Preguntas: En el panel central de chat, escribe tu consulta. El sistema responderá y mostrará un desplegable con los fragmentos exactos consultados y su puntaje de similitud (KNN).

## 7. Matriz de Pruebas Realizadas (Requisito 4.4)

Para cumplir con el diseño modular y las buenas prácticas de QA, las 3 pruebas obligatorias (pregunta respondible, parcialmente respondible y no respondible) junto con sus resultados y observaciones técnicas han sido documentadas en un archivo independiente.

Ver resultados detallados de las pruebas en: [Ir al archivo de destino](./docs/PRUEBAS_Y_RESULTADOS.md)

## 8. Uso de Herramientas AI-Assisted Development (Requisito 4.3)

- Como parte de un flujo de desarrollo moderno, se utilizaron asistentes de IA de forma responsable para acelerar tareas repetitivas y estructurar la arquitectura:

- Herramientas utilizadas: Google Gemini y Claude Code (integrado en Visual Studio Code).

- Propósito: Generación del boilerplate de la estructura de directorios bajo Clean Architecture, definición inicial de DTOs en Pydantic y maquetación de los componentes de Streamlit.

- Revisión y ajustes manuales críticos:

   1. Control estricto de Alucinaciones: Se ajustó manualmente el System Prompt de LangChain. Se añadió un StrOutputParser para mitigar errores de parseo cuando la API de Gemini devuelve bloques anómalos.

   2. Resolución de Duplicidad en Vector Store: Se modificó manualmente el generador de IDs en RecursiveCharacterTextSplitter para usar IDs deterministas en lugar de UUIDs aleatorios, logrando que ChromaDB haga un upsert en lugar de duplicar fragmentos al re-indexar los mismos documentos.

   3. Inyección de Dependencias Dinámica: Se implementó lógica manual en los endpoints de FastAPI para que el adaptador de Storage (S3 o Local) se inyecte en los Casos de Uso evaluando la selección del usuario por query params, garantizando un backend 100% stateless.

- Aprendizajes principales: Se consolidó el conocimiento sobre cómo aislar completamente un motor RAG detrás de "Puertos" e "Interfaces". Este desacoplamiento comprobó su valor al permitir cambiar los embeddings de OpenAI a Google Gemini (al no contar con una API-KEY activa) en un solo archivo sin tener que reescribir la lógica principal del chatbot

## 9. Limitaciones Conocidas y Mejoras Futuras

- Limitaciones Actuales:

   - PDFs Escaneados: La extracción actual se realiza mediante pypdf, la cual lee el texto nativo del documento. Si el PDF cargado es una imagen pura (escaneada), la extracción de texto será nula y no generará fragmentos para indexar.

   - Concurrencia de ChromaDB: La versión embebida de ChromaDB se basa en SQLite local. Es excelente para este prototipo o para uso departamental, pero no soportaría miles de lecturas/escrituras concurrentes en producción masiva.

- Roadmap y Mejoras Futuras:

   - Búsqueda Híbrida y Reranking: Integrar BM25 junto con la búsqueda vectorial, y añadir un paso final de Reranking (ej. Cohere Rerank o Cross-Encoder) para mejorar dramáticamente la recuperación en manuales muy técnicos con vocabulario denso.

   - Soporte OCR (Reconocimiento Óptico de Caracteres) Integrado: Conectar AWS Textract, Google Document AI o Tesseract para soportar documentos escaneados.

   - Testing Automatizado: Implementar un suite de pruebas unitarias y de integración con pytest, aprovechando que la Clean Architecture permite hacer mock de los adaptadores de infraestructura fácilmente.

## 10. Estructura de proyecto:


```text
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
│   │   │   │   ├── langchain_splitter.py # Adaptador langchain_splitter
│   │   │   │   ├── chroma_vector_store.py # Adaptador chroma_vector_store
│   │   │   │   └── langchain_llm.py # langchain_llm
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
```