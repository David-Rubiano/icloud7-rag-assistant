from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.domain.interfaces.llm_port import LLMPort
from app.domain.entities.document import SourceReference
from app.infrastructure.config.settings import settings

class LangChainLLMAdapter(LLMPort):
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("Falta configurar GOOGLE_API_KEY en el archivo .env")

        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.0  # Temperatura 0 para respuestas deterministas y sin alucinaciones
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Eres un asistente documental corporativo estricto. "
                "Responde a la pregunta del usuario utilizando ÚNICAMENTE la información "
                "proporcionada en el siguiente CONTEXTO.\n"
                "Reglas estrictas:\n"
                "1. Si la respuesta no se encuentra en el contexto, responde exactamente: "
                "'No cuento con información suficiente en los documentos cargados para responder esta pregunta.'\n"
                "2. Si la pregunta solo puede responderse parcialmente con el contexto, responde únicamente la parte "
                "soportada por los documentos y aclara explícitamente qué información no está disponible.\n"
                "3. Menciona siempre el documento fuente entre corchetes, por ejemplo: [Fuente: archivo.pdf].\n\n"
                "CONTEXTO:\n{context}"
            )),
            ("human", "{question}")
        ])

    def generate_answer(self, question: str, context_chunks: List[SourceReference]) -> str:
        if not context_chunks:
            return "No hay fragmentos indexados disponibles para responder la consulta."

        formatted_context = "\n\n---\n\n".join(
            [f"[Documento: {c.document_name}]\n{c.fragment_preview}" for c in context_chunks]
        )
        chain = self.prompt | self.llm
        response = chain.invoke({"context": formatted_context, "question": question})
        return response.content