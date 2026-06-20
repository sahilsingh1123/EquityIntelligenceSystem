from app.models.schemas import ChatAnswer, Evidence, Insight


class ChatService:
    def answer(self, question: str, insights: list[Insight]) -> ChatAnswer:
        query_terms = {term.casefold() for term in question.split() if len(term) > 2}
        ranked = sorted(
            insights,
            key=lambda item: len(query_terms.intersection(item.title.casefold().split())),
            reverse=True,
        )
        selected = ranked[:3]
        citations: list[Evidence] = []
        for insight in selected:
            citations.extend(insight.evidence[:2])

        if not selected:
            return ChatAnswer(
                answer="I do not have enough structured evidence to answer that yet.",
                confidence=30,
                citations=[],
            )

        answer = " ".join(
            [
                f"{insight.title}: {insight.what_happened} {insight.why_it_matters}"
                for insight in selected
            ]
        )
        confidence = round(sum(insight.confidence for insight in selected) / len(selected))
        return ChatAnswer(answer=answer, confidence=confidence, citations=citations)
