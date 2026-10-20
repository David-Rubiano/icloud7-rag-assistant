### Diagrama de la Arquitectura

```mermaid
graph TD
    %% Contenedor Frontend
    subgraph Frontend["Frontend Container (Docker)"]
        UI[Streamlit UI]
    end

    %% Contenedor Backend
    subgraph Backend["Backend Container (Docker) - Microservicio"]
        direction TB
        
        %% Capa 4: Presentation
        subgraph Presentation["4. Presentation Layer"]
            API[FastAPI Endpoints & DTOs]
        end

        %% Capa 3: Infrastructure (Adapters)
        subgraph Infrastructure["3. Infrastructure Layer (Adapters)"]
            S3[Storage: S3 / Local]
            Chroma[VectorStore: ChromaDB]
            Gemini[LLM: Google Gemini]
        end

        %% Capa 2: Application (Use Cases)
        subgraph Application["2. Application Layer"]
            UC[Casos de Uso: Orquestación]
        end

        %% Capa 1: Domain (Core)
        subgraph Domain["1. Domain Layer (Core)"]
            Ports[Puertos: Interfaces Abstractas]
            Entities[Entidades de Negocio]
        end

        %% Relaciones de Clean Architecture
        API -- "Llama a" --> UC
        UC -- "Usa" --> Ports
        UC -- "Usa" --> Entities
        Infrastructure -. "Implementa" .-> Ports
    end

    %% Comunicación entre microservicios
    UI -- "HTTP REST (JSON)" --> API

    classDef core fill:#d4edda,stroke:#28a745,stroke-width:2px,color:black;
    classDef app fill:#cce5ff,stroke:#007bff,stroke-width:2px,color:black;
    classDef infra fill:#f8d7da,stroke:#dc3545,stroke-width:2px,color:black;
    classDef pres fill:#fff3cd,stroke:#ffc107,stroke-width:2px,color:black;
    classDef front fill:#e2e3e5,stroke:#6c757d,stroke-width:2px,color:black;

    class Domain core;
    class Application app;
    class Infrastructure infra;
    class Presentation pres;
    class Frontend front;