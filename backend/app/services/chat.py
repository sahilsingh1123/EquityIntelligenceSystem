from concurrent.futures import ThreadPoolExecutor
import asyncio

from app.models.schemas import ChatAnswer, Evidence, Insight
from app.core.ai.factory import create_ai_client


def run_sync(coro):
    """Safely executes an async coroutine synchronously, even inside a running event loop."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(lambda: asyncio.run(coro))
            return future.result()
    else:
        return asyncio.run(coro)


class ChatService:
    def __init__(self) -> None:
        try:
            self.ai_client = create_ai_client()
            print(f"[ChatService] Initialized AI Client with model: {self.ai_client.model_name}")
        except Exception as e:
            print(f"[ChatService] Failed to initialize AI client: {e}. Falling back to rule-based Q&A.")
            self.ai_client = None

    def answer(self, question: str, insights: list[Insight]) -> ChatAnswer:
        query_terms = {term.casefold() for term in question.split() if len(term) > 2}
        ranked = sorted(
            insights,
            key=lambda item: len(query_terms.intersection(item.title.casefold().split())),
            reverse=True,
        )
        
        # Select matched insights, or fall back to top insights if none matched query tokens
        selected = [item for item in ranked if len(query_terms.intersection(item.title.casefold().split())) > 0][:5]
        if not selected:
            selected = ranked[:3]

        if not selected:
            return ChatAnswer(
                answer="I do not have enough structured evidence to answer that yet.",
                confidence=30,
                citations=[],
            )

        citations: list[Evidence] = []
        for insight in selected:
            citations.extend(insight.evidence[:2])

        if self.ai_client:
            try:
                answer_text = run_sync(self._ai_answer(question, selected))
                avg_confidence = round(sum(insight.confidence for insight in selected) / len(selected))
                return ChatAnswer(answer=answer_text, confidence=avg_confidence, citations=citations)
            except Exception as e:
                print(f"[ChatService] AI Q&A generation failed: {e}. Falling back to rules.")

        return self._rule_answer(selected, citations)

    async def _ai_answer(self, question: str, selected_insights: list[Insight]) -> str:
        context_items = []
        for insight in selected_insights:
            context_items.append(
                f"Title: {insight.title}\n"
                f"What Happened: {insight.what_happened}\n"
                f"Why It Matters: {insight.why_it_matters}\n"
                f"Potential Impact: {insight.potential_impact}\n"
                f"Watch Points: {', '.join(insight.watch_points)}"
            )
        context = "\n---\n".join(context_items)

        prompt = (
            f"You are a helpful and professional equity intelligence assistant. Answer the user's question "
            f"based only on the structured corporate and macroeconomic insights provided as context below.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            f"If the context does not contain relevant information to answer the question, state that you do "
            f"not have enough structured evidence. Be concise, objective, and refer to the specific companies "
            f"mentioned in your answer. Limit your response to 4 sentences."
        )
        system_prompt = "You are a professional financial assistant providing evidence-backed answers."

        return await self.ai_client.generate(
            prompt=prompt,
            system_prompt=system_prompt,
        )

    def _rule_answer(self, selected: list[Insight], citations: list[Evidence]) -> ChatAnswer:
        answer = " ".join(
            [
                f"{insight.title}: {insight.what_happened} {insight.why_it_matters}"
                for insight in selected
            ]
        )
        confidence = round(sum(insight.confidence for insight in selected) / len(selected))
        return ChatAnswer(answer=answer, confidence=confidence, citations=citations)

