from app.core.enums import EventType, Sentiment
from app.core.scoring import clamp_score, weighted_score
from app.models.schemas import Event, Opportunity, Risk


class OpportunityService:
    positive_event_types = {
        EventType.EARNINGS_BEAT,
        EventType.GUIDANCE_UPGRADE,
        EventType.CONTRACT_WIN,
        EventType.BUYBACK,
        EventType.DIVIDEND,
        EventType.CAPEX,
    }

    def score(self, company_name: str, events: list[Event]) -> Opportunity:
        positive_events = [event for event in events if event.event_type in self.positive_event_types]
        positive_frequency = min(100, len(positive_events) * 25)
        sentiment_trend = self._sentiment_score(events, Sentiment.POSITIVE)
        institutional_activity = 50
        sector_strength = 55
        growth_signals = max([event.importance for event in positive_events], default=35)

        score = weighted_score(
            [
                (positive_frequency, 0.30),
                (sentiment_trend, 0.20),
                (institutional_activity, 0.20),
                (sector_strength, 0.15),
                (growth_signals, 0.15),
            ]
        )
        confidence = clamp_score(sum(event.confidence for event in events) / max(len(events), 1))
        return Opportunity(
            company_name=company_name,
            score=score,
            confidence=confidence,
            reason=self._reason(positive_events, "positive catalysts", "No strong positive catalyst yet"),
        )

    def _sentiment_score(self, events: list[Event], sentiment: Sentiment) -> int:
        if not events:
            return 0
        return clamp_score(sum(1 for event in events if event.sentiment == sentiment) / len(events) * 100)

    def _reason(self, events: list[Event], label: str, fallback: str) -> str:
        if not events:
            return fallback
        names = ", ".join(sorted({event.event_type.value.replace("_", " ").title() for event in events}))
        return f"Detected {label}: {names}."


class RiskService:
    risk_event_types = {
        EventType.EARNINGS_MISS,
        EventType.GUIDANCE_DOWNGRADE,
        EventType.REGULATORY_ACTION,
        EventType.LITIGATION,
        EventType.DEBT_ISSUE,
        EventType.MANAGEMENT_CHANGE,
    }

    def score(self, company_name: str, events: list[Event]) -> Risk:
        risk_events = [event for event in events if event.event_type in self.risk_event_types]
        governance_risk = 80 if any(e.event_type == EventType.MANAGEMENT_CHANGE for e in risk_events) else 35
        financial_risk = 75 if any(e.event_type == EventType.DEBT_ISSUE for e in risk_events) else 30
        sector_risk = 45
        macro_risk = 60 if any(e.event_type == EventType.MACRO_EVENT for e in events) else 35
        sentiment_risk = clamp_score(
            sum(1 for event in events if event.sentiment == Sentiment.NEGATIVE)
            / max(len(events), 1)
            * 100
        )

        score = weighted_score(
            [
                (governance_risk, 0.30),
                (financial_risk, 0.25),
                (sector_risk, 0.20),
                (macro_risk, 0.15),
                (sentiment_risk, 0.10),
            ]
        )
        confidence = clamp_score(sum(event.confidence for event in events) / max(len(events), 1))
        return Risk(
            company_name=company_name,
            score=score,
            confidence=confidence,
            reason=self._reason(risk_events),
        )

    def _reason(self, events: list[Event]) -> str:
        if not events:
            return "No major risk event detected from stored events."
        names = ", ".join(sorted({event.event_type.value.replace("_", " ").title() for event in events}))
        return f"Detected risk factors: {names}."
