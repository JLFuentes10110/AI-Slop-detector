import spacy
from collections import Counter
from typing import Tuple, List

nlp = spacy.load("en_core_web_sm")

AI_FILLER_PHRASES = [
    "it's worth noting", "it is worth noting",
    "in conclusion", "to summarize",
    "as an ai language model", "as a large language model",
    "certainly!", "absolutely!", "of course!",
    "i hope this helps", "feel free to ask",
    "delve into", "dive into", "let's explore",
    "in today's world", "in the modern era",
    "it's important to note", "it is important to note",
    "furthermore", "moreover", "in addition to",
    "needless to say", "at the end of the day",
]


def compute_type_token_ratio(text: str) -> float:
    doc = nlp(text.lower())
    tokens = [t.text for t in doc if t.is_alpha]
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def detect_repeated_ngrams(text: str, n: int = 4, threshold: int = 2) -> List[str]:
    doc = nlp(text.lower())
    words = [t.text for t in doc if t.is_alpha]
    ngrams = [" ".join(words[i:i+n]) for i in range(len(words) - n + 1)]
    counts = Counter(ngrams)
    return [phrase for phrase, count in counts.items() if count >= threshold]


def detect_filler_phrases(text: str) -> List[str]:
    text_lower = text.lower()
    return [p for p in AI_FILLER_PHRASES if p in text_lower]


def compute_sentence_length_variance(text: str) -> float:
    doc = nlp(text)
    lengths = [len(sent) for sent in doc.sents]
    if len(lengths) < 2:
        return 100.0
    mean = sum(lengths) / len(lengths)
    return sum((l - mean) ** 2 for l in lengths) / len(lengths)


def analyze_text(text: str) -> Tuple[float, List[str], List[str]]:
    issues, suggestions, penalty = [], [], 0.0

    ttr = compute_type_token_ratio(text)
    if ttr < 0.40:
        penalty += 30
        issues.append(f"Very low vocabulary diversity (TTR={ttr:.2f}).")
        suggestions.append("Use more varied synonyms and sentence structures.")
    elif ttr < 0.55:
        penalty += 15
        issues.append(f"Moderate vocabulary repetition (TTR={ttr:.2f}).")
        suggestions.append("Try varying your word choices more.")

    repeated = detect_repeated_ngrams(text)
    if len(repeated) > 3:
        penalty += 25
        issues.append(f"{len(repeated)} repeated 4-word phrases found. Likely templated content.")
        suggestions.append("Rewrite repeated passages in fresh language.")
    elif repeated:
        penalty += 10
        issues.append(f"Minor phrase repetition detected ({len(repeated)} instances).")

    fillers = detect_filler_phrases(text)
    if len(fillers) >= 3:
        penalty += 30
        issues.append(f"Many AI filler phrases found: {', '.join(fillers[:5])}")
        suggestions.append("Remove generic transitional phrases typical of AI output.")
    elif fillers:
        penalty += 10 * len(fillers)
        issues.append(f"AI filler phrase(s) detected: {', '.join(fillers)}")

    variance = compute_sentence_length_variance(text)
    if variance < 5.0:
        penalty += 15
        issues.append("Suspiciously uniform sentence lengths.")
        suggestions.append("Mix short and long sentences for a more natural rhythm.")

    return round(min(100.0, max(0.0, penalty)), 1), issues, suggestions
