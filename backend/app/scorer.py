from typing import Optional, List

WEIGHTS = {
    "text":     0.50,
    "image":    0.25,
    "behavior": 0.25,
}


def compute_unified_score(
    text_score: Optional[float],
    image_score: Optional[float],
    behavior_score: Optional[float],
) -> float:
    components = {
        "text":     text_score,
        "image":    image_score,
        "behavior": behavior_score,
    }
    active = {k: v for k, v in components.items() if v is not None}
    if not active:
        return 0.0
    total_weight = sum(WEIGHTS[k] for k in active)
    weighted_sum = sum(WEIGHTS[k] * v for k, v in active.items())
    return round(weighted_sum / total_weight, 1)


def get_grade(score: float) -> str:
    if score < 20:  return "Clean"
    if score < 45:  return "Mild slop"
    if score < 65:  return "Suspicious"
    if score < 80:  return "High slop"
    return "AI slop"


def build_score_breakdown(
    text_score: Optional[float],
    image_score: Optional[float],
    behavior_score: Optional[float],
    all_issues: List[str],
    all_suggestions: List[str],
) -> dict:
    unified = compute_unified_score(text_score, image_score, behavior_score)
    return {
        "text_score":         text_score,
        "image_score":        image_score,
        "behavior_score":     behavior_score,
        "unified_slop_score": unified,
        "grade":              get_grade(unified),
        "issues":             all_issues,
        "suggestions":        all_suggestions,
    }
