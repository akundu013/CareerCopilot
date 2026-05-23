import re
import string


REQUIREMENT_SIGNALS = (
    "required",
    "requirements",
    "preferred",
    "qualifications",
    "skills",
    "experience",
    "experience with",
    "experience in",
    "experience handling",
    "responsible for",
    "must have",
    "nice to have",
    "ability to",
    "familiar with",
    "knowledge of",
    "proficiency in",
    "certification",
    "license",
    "degree",
)

FILLER_PHRASES = (
    "we are looking for",
    "the ideal candidate",
    "ideal candidate",
    "candidate should",
    "you will",
    "you should",
    "responsible for",
    "responsibilities include",
    "must have",
    "nice to have",
    "required",
    "requirements",
    "preferred",
    "qualifications",
    "skills",
    "experience with",
    "experience in",
    "experience handling",
    "experience managing",
    "ability to",
    "knowledge of",
    "familiar with",
    "proficiency in",
    "proficient in",
    "strong",
    "excellent",
    "solid",
)

ROLE_SUFFIXES = {
    "assistant",
    "associate",
    "coordinator",
    "manager",
    "representative",
    "specialist",
}

LEADING_FILLER_WORDS = {
    "a",
    "an",
    "and",
    "as",
    "for",
    "in",
    "of",
    "or",
    "the",
    "to",
    "with",
}

LOW_VALUE_REQUIREMENTS = {
    "other duties",
    "other duties as assigned",
    "team player",
    "fast paced environment",
    "competitive salary",
    "benefits",
}

ALLOWED_SINGLE_WORD_REQUIREMENTS = {
    "certification",
    "communication",
    "degree",
    "license",
}

COMMUNICATION_VERBS = {
    "communicate",
    "communicates",
    "communicated",
    "communicating",
}


def normalize_text(text: str) -> str:
    normalized = text.lower()
    normalized = normalized.replace("&", " and ")
    normalized = normalized.replace("\u2022", "\n- ")
    normalized = normalized.replace("\u2013", "-")
    normalized = normalized.replace("\u2014", "-")
    normalized = normalized.replace("\u2018", "'")
    normalized = normalized.replace("\u2019", "'")
    normalized = normalized.replace("\u201c", '"')
    normalized = normalized.replace("\u201d", '"')
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n\s+", "\n", normalized)
    normalized = re.sub(r"\n{2,}", "\n", normalized)

    return normalized.strip()


def split_into_sentences(text: str) -> list[str]:
    normalized = normalize_text(text)

    if not normalized:
        return []

    fragments: list[str] = []

    for line in normalized.splitlines():
        cleaned_line = re.sub(r"^\s*[-*•\d.)]+\s*", "", line).strip()

        if not cleaned_line:
            continue

        sentence_parts = re.split(r"(?<=[.!?])\s+|[|]", cleaned_line)

        for part in sentence_parts:
            sentence = _clean_sentence_fragment(part)

            if sentence:
                fragments.append(sentence)

    return fragments


def is_requirement_sentence(sentence: str) -> bool:
    normalized = normalize_text(sentence)

    if not normalized:
        return False

    if any(signal in normalized for signal in REQUIREMENT_SIGNALS):
        return True

    words = _get_words(normalized)

    if len(words) < 2:
        return False

    if normalized in LOW_VALUE_REQUIREMENTS:
        return False

    return len(words) <= 18


def extract_candidate_phrases(sentence: str) -> list[str]:
    normalized = normalize_text(sentence)

    if not normalized:
        return []

    normalized = _remove_filler_phrases(normalized)
    parts = re.split(
        r",|;|/|\n|(?:\s+-\s+)|(?:\s+ and \s+)|(?:\s+ or \s+)",
        normalized,
    )

    candidates: list[str] = []

    for part in parts:
        phrase = _clean_requirement_phrase(part)

        if not phrase:
            continue

        candidates.extend(_expand_candidate_phrase(phrase))

    return deduplicate_requirements(candidates)


def deduplicate_requirements(requirements: list[str]) -> list[str]:
    unique_requirements: list[str] = []
    seen: set[str] = set()

    for requirement in requirements:
        normalized = _clean_requirement_phrase(requirement)

        if not normalized or normalized in seen:
            continue

        seen.add(normalized)
        unique_requirements.append(normalized)

    return unique_requirements


def extract_requirements(text: str) -> list[str]:
    requirements: list[str] = []

    for sentence in split_into_sentences(text):
        if not is_requirement_sentence(sentence):
            continue

        requirements.extend(extract_candidate_phrases(sentence))

    return deduplicate_requirements(requirements)


def _remove_filler_phrases(text: str) -> str:
    cleaned = text

    for phrase in FILLER_PHRASES:
        cleaned = re.sub(rf"\b{re.escape(phrase)}\b", " ", cleaned)

    return re.sub(r"\s+", " ", cleaned).strip()


def _clean_requirement_phrase(phrase: str) -> str:
    cleaned = normalize_text(phrase)
    cleaned = _remove_filler_phrases(cleaned)
    cleaned = cleaned.translate(str.maketrans("", "", string.punctuation))
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    words = cleaned.split()

    while words and words[0] in LEADING_FILLER_WORDS:
        words.pop(0)

    if len(words) > 2 and words[-1] in ROLE_SUFFIXES:
        words.pop()

    cleaned = " ".join(words).strip()

    if not _is_meaningful_requirement(cleaned):
        return ""

    return cleaned


def _expand_candidate_phrase(phrase: str) -> list[str]:
    words = _get_words(phrase)

    if not words:
        return []

    candidates: list[str] = []

    if " with " in phrase:
        before_with, after_with = phrase.split(" with ", maxsplit=1)

        if _is_meaningful_requirement(before_with):
            candidates.append(before_with)

        if _is_meaningful_requirement(after_with):
            candidates.append(after_with)
    else:
        candidates.append(phrase)

    if any(word in COMMUNICATION_VERBS for word in words):
        candidates.append("communication")

    if len(words) >= 3 and words[0].endswith("ing"):
        noun_phrase = " ".join(words[1:])

        if _is_meaningful_requirement(noun_phrase):
            if phrase in candidates:
                candidates.remove(phrase)

            candidates.append(noun_phrase)

    return candidates


def _is_meaningful_requirement(phrase: str) -> bool:
    if not phrase or phrase in LOW_VALUE_REQUIREMENTS:
        return False

    words = _get_words(phrase)

    if len(words) < 2 and not _allows_single_word_requirement(phrase):
        return False

    if len(words) > 8:
        return False

    return True


def _allows_single_word_requirement(phrase: str) -> bool:
    return phrase in ALLOWED_SINGLE_WORD_REQUIREMENTS


def _get_words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _clean_sentence_fragment(sentence: str) -> str:
    cleaned = normalize_text(sentence)
    cleaned = cleaned.strip(string.whitespace + string.punctuation)
    cleaned = re.sub(r"\s+", " ", cleaned)

    return cleaned.strip()
