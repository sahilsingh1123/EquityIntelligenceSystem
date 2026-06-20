def clamp_score(value: float) -> int:
    return max(0, min(100, round(value)))


def weighted_score(parts: list[tuple[float, float]]) -> int:
    """Return a 0-100 score from value, weight pairs."""
    total_weight = sum(weight for _, weight in parts)
    if total_weight <= 0:
        return 0
    return clamp_score(sum(value * weight for value, weight in parts) / total_weight)
