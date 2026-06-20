from app.core.enums import Sentiment, SignalType
from app.core.scoring import clamp_score
from app.models.schemas import Event, Signal


class SignalService:
    def from_event(self, event: Event) -> Signal:
        signal_type = {
            Sentiment.POSITIVE: SignalType.POSITIVE,
            Sentiment.NEGATIVE: SignalType.NEGATIVE,
            Sentiment.NEUTRAL: SignalType.NEUTRAL,
            Sentiment.UNCERTAIN: SignalType.UNCERTAIN,
        }[event.sentiment]
        strength = clamp_score((event.importance * 0.6) + (event.confidence * 0.4))
        return Signal(
            company_id=event.company_id,
            company_name=event.company_name,
            signal_type=signal_type,
            strength=strength,
            confidence=event.confidence,
            reason=event.summary,
        )
