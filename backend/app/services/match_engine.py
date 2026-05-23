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
    "cicd": "cicd",
    "devops": "devops",
    "javascript": "javascript",
    "nodejs": "nodejs",
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "typescript": "typescript",
}

SPACED_TECHNICAL_ALIAS_REPLACEMENTS = (
    (r"(?<![a-z0-9])j\s+a\s+v\s+a\s+s\s+c\s+r\s+i\s+p\s+t(?![a-z0-9])", "javascript"),
    (r"(?<![a-z0-9])t\s+y\s+p\s+e\s+s\s+c\s+r\s+i\s+p\s+t(?![a-z0-9])", "typescript"),
    (r"(?<![a-z0-9])n\s+o\s+d\s+e\s*\.?\s*j\s+s(?![a-z0-9])", "nodejs"),
    (r"(?<![a-z0-9])c\s+i\s*/\s*c\s+d(?![a-z0-9])", "cicd"),
    (r"(?<![a-z0-9])d\s+e\s+v\s+o\s+p\s+s(?![a-z0-9])", "devops"),
    (r"(?<![a-z0-9])p\s+o\s+s\s+t\s+g\s+r\s+e\s+s\s+q\s+l(?![a-z0-9])", "postgresql"),
    (r"(?<![a-z0-9])p\s+y\s+t\s+h\s+o\s+n(?![a-z0-9])", "python"),
    (r"(?<![a-z0-9])r\s+e\s+a\s+c\s+t\s+n\s+a\s+t\s+i\s+v\s+e(?![a-z0-9])", "react native"),
    (r"(?<![a-z0-9])r\s+e\s+a\s+c\s+t(?![a-z0-9])", "react"),
    (r"(?<![a-z0-9])d\s+o\s+c\s+k\s+e\s+r(?![a-z0-9])", "docker"),
    (r"(?<![a-z0-9])k\s+u\s+b\s+e\s+r\s+n\s+e\s+t\s+e\s+s(?![a-z0-9])", "kubernetes"),
    (r"(?<![a-z0-9])a\s+w\s+s(?![a-z0-9])", "aws"),
)

TECHNICAL_ALIAS_REPLACEMENTS = (
    (r"\bnode\s*\.?\s*js\b", "nodejs"),
    (r"\btype\s+script\b", "typescript"),
    (r"\bjava\s+script\b", "javascript"),
    (r"\bci\s*/?\s*cd\b", "cicd"),
    (r"\bdev\s+ops\b", "devops"),
    (r"\bpostgres\b", "postgresql"),
)

RELATED_TERM_GROUPS = {
    "cleaning": {
        "clean",
        "cleaning",
        "cleanliness",
        "commercial cleaning",
        "kitchen cleaning",
        "restaurant cleaning",
        "sanitation",
    },
    "customer service": {
        "client service",
        "customer service",
    },
    "communication": {
        "communicating",
        "communication",
    },
    "devops": {
        "automated deployment",
        "aws",
        "cicd",
        "ci cd",
        "ci/cd",
        "devops",
        "docker",
        "kubernetes",
    },
}


def normalize_text(text: str) -> str:
    normalized = _collapse_spaced_letters(text).lower()
    normalized = normalized.replace("&", " and ")
    normalized = normalized.replace("\u2013", "-")
    normalized = normalized.replace("\u2014", "-")
    normalized = normalized.replace("\u2018", "'")
    normalized = normalized.replace("\u2019", "'")
    normalized = normalized.replace("\u201c", '"')
    normalized = normalized.replace("\u201d", '"')

    for pattern, replacement in SPACED_TECHNICAL_ALIAS_REPLACEMENTS:
        normalized = re.sub(pattern, replacement, normalized)

    for pattern, replacement in TECHNICAL_ALIAS_REPLACEMENTS:
        normalized = re.sub(pattern, replacement, normalized)

    normalized = normalized.translate(str.maketrans("", "", string.punctuation))
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized.strip()


def _collapse_spaced_letters(text: str) -> str:
    parts = re.split(r"(\s{2,}|\n)", text)
    collapsed_parts: list[str] = []

    for part in parts:
        stripped_part = part.strip()

        if re.fullmatch(r"(?:[A-Za-z]\s+){2,}[A-Za-z]", stripped_part):
            collapsed_parts.append(stripped_part.replace(" ", ""))
        else:
            collapsed_parts.append(part)

    return "".join(collapsed_parts)


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

    if _related_requirement_matches(normalized_requirement, normalized_resume):
        return True

    if normalized_requirement == "react":
        return False

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
        requirement_label = " ".join(requirement.split())
        normalized_requirement = normalize_text(requirement)

        if not normalized_requirement:
            continue

        if requirement_matches_resume(normalized_requirement, resume_text):
            matched_requirements.append(requirement_label)
        else:
            missing_requirements.append(requirement_label)

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
    if phrase == "react":
        return re.search(r"\breact\b(?!\s+native)", text) is not None

    return re.search(rf"\b{re.escape(phrase)}\b", text) is not None


def _related_requirement_matches(requirement: str, resume_text: str) -> bool:
    requirement_words = set(get_meaningful_words(requirement))

    for group_name, related_terms in RELATED_TERM_GROUPS.items():
        group_words = set(get_meaningful_words(group_name))

        if not group_words.issubset(requirement_words):
            continue

        if any(_contains_phrase(resume_text, normalize_text(term)) for term in related_terms):
            return True

    return False


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
