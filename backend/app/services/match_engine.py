import math
import re
import string


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}

WORD_NORMALIZATIONS = {
    "communicate": "communication",
    "communicates": "communication",
    "communicated": "communication",
    "communicating": "communication",
}


def normalize_text(text: str) -> str:
    normalized = text.lower()
    normalized = normalized.replace("&", " and ")
    normalized = normalized.replace("\u2013", "-")
    normalized = normalized.replace("\u2014", "-")
    normalized = normalized.replace("\u2018", "'")
    normalized = normalized.replace("\u2019", "'")
    normalized = normalized.replace("\u201c", '"')
    normalized = normalized.replace("\u201d", '"')
    normalized = normalized.translate(str.maketrans("", "", string.punctuation))
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized.strip()


def get_meaningful_words(text: str) -> list[str]:
    normalized = normalize_text(text)

    if not normalized:
        return []

    words = re.findall(r"[a-z0-9]+", normalized)

    return [_normalize_word(word) for word in words if word not in STOPWORDS]


def requirement_matches_resume(requirement: str, resume_text: str) -> bool:
    normalized_requirement = normalize_text(requirement)
    normalized_resume = normalize_text(resume_text)

    if not normalized_requirement or not normalized_resume:
        return False

    if _contains_phrase(normalized_resume, normalized_requirement):
        return True

    requirement_words = get_meaningful_words(normalized_requirement)

    if not requirement_words:
        return False

    resume_words = set(get_meaningful_words(normalized_resume))
    matched_word_count = sum(1 for word in requirement_words if word in resume_words)

    if len(requirement_words) == 1:
        return matched_word_count == 1

    if len(requirement_words) == 2:
        return matched_word_count == 2

    required_match_count = math.ceil(len(requirement_words) * 0.7)

    return matched_word_count >= required_match_count


def calculate_match_score(matched_count: int, total_count: int) -> int:
    if matched_count <= 0 or total_count <= 0:
        return 0

    return round((matched_count / total_count) * 100)


def analyze_match(resume_text: str, job_requirements: list[str]) -> dict:
    if not resume_text or not job_requirements:
        return {
            "matchScore": 0,
            "matchedRequirements": [],
            "missingRequirements": [],
        }

    matched_requirements: list[str] = []
    missing_requirements: list[str] = []

    for requirement in job_requirements:
        normalized_requirement = normalize_text(requirement)

        if not normalized_requirement:
            continue

        if requirement_matches_resume(normalized_requirement, resume_text):
            matched_requirements.append(normalized_requirement)
        else:
            missing_requirements.append(normalized_requirement)

    match_score = calculate_match_score(
        len(matched_requirements),
        len(matched_requirements) + len(missing_requirements),
    )

    return {
        "matchScore": match_score,
        "matchedRequirements": matched_requirements,
        "missingRequirements": missing_requirements,
    }


def _contains_phrase(text: str, phrase: str) -> bool:
    return re.search(rf"\b{re.escape(phrase)}\b", text) is not None


def _normalize_word(word: str) -> str:
    if word in WORD_NORMALIZATIONS:
        return WORD_NORMALIZATIONS[word]

    if len(word) > 5 and word.endswith("ing"):
        stem = word[:-3]

        if len(stem) > 2 and stem[-1] == stem[-2]:
            stem = stem[:-1]

        return stem

    if len(word) > 5 and word.endswith("ated"):
        return word[:-1]

    if len(word) > 4 and word.endswith("ed"):
        stem = word[:-2]

        if len(stem) > 2 and stem[-1] == stem[-2]:
            stem = stem[:-1]

        return stem

    if len(word) > 4 and word.endswith("ies"):
        return f"{word[:-3]}y"

    if len(word) > 3 and word.endswith("s"):
        return word[:-1]

    return word
