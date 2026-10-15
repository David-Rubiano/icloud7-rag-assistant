from app.domain.interfaces.vector_store_port import VectorStorePort
from app.domain.interfaces.llm_port import LLMPort
from app.domain.entities.document import RAGResponse

class AskQuestionUseCase:
    def __init__(self, vector_store: VectorStorePort, llm: LLMPort):
        self.vector_store = vector_store
        self.llm = llm

    def execute(self, question: str, top_k: int = 3) -> RAGResponse:
        sources = self.vector_store.similarity_search(query=question, k=top_k)
        answer = self.llm.generate_answer(question=question, context_chunks=sources)
        return RAGResponse(
            question=question,
            answer=answer,
            sources=sources
        )