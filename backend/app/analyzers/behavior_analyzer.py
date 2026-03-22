from typing import Tuple, List


def analyze_behavior(
    typing_time: float,
    posts_per_day: int,
) -> Tuple[float, List[str], List[str]]:
    issues, suggestions, penalty = [], [], 0.0

    # Typing time checks — very fast = likely pasted AI output
    if typing_time < 1.0:
        penalty += 40
        issues.append(f"Extremely fast typing time ({typing_time}s). Content likely pasted.")
        suggestions.append("Write content manually rather than copy-pasting AI output.")
    elif typing_time < 3.0:
        penalty += 20
        issues.append(f"Low typing time ({typing_time}s). Possible AI-assisted input.")
        suggestions.append("Take more time composing your content.")

    # Posts per day checks
    if posts_per_day >= 50:
        penalty += 40
        issues.append(f"Extremely high post volume ({posts_per_day}/day). Strong AI usage signal.")
        suggestions.append("Review and meaningfully edit content before posting.")
    elif posts_per_day >= 20:
        penalty += 20
        issues.append(f"High post volume ({posts_per_day}/day). Possible AI-assisted bulk posting.")
        suggestions.append("Slow down and focus on quality over quantity.")

    if suggestions:
        suggestions.append("Add personal insights and original thinking to your content.")

    return round(min(100.0, max(0.0, penalty)), 1), issues, suggestions
