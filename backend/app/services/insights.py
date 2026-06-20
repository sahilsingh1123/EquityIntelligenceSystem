from app.models.schemas import Event, Insight


class InsightService:
    def from_event(self, event: Event) -> Insight:
        event_name = event.event_type.value.replace("_", " ").title()
        return Insight(
            title=f"{event.company_name}: {event_name}",
            what_happened=event.summary,
            why_it_matters=(
                "The event may change investor perception, near-term expectations, or sector read-throughs."
            ),
            potential_impact=(
                "Impact should be assessed through follow-up filings, management commentary, "
                "price-volume reaction, and peer movements."
            ),
            confidence=event.confidence,
            importance=event.importance,
            watch_points=[
                "Confirmation from high-trust sources",
                "Management commentary or regulatory filing",
                "Sector and peer reaction",
            ],
            evidence=event.evidence,
        )
