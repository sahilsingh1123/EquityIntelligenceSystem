from app.models.schemas import Insight


class Retriever:
    def retrieve(self, query: str, insights: list[Insight]) -> list[Insight]:
        terms = {term.casefold() for term in query.split() if len(term) > 2}
        return [
            insight
            for insight in insights
            if terms.intersection(f"{insight.title} {insight.what_happened}".casefold().split())
        ]
