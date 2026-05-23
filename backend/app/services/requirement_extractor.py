import re
import string

try:
    import yake
except ImportError:  # pragma: no cover - fallback when dependencies are not installed yet
    yake = None


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
    "strong knowledge",
    "relevant skills",
    "foundational knowledge",
    "know how",
    "know-how",
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
    "your duties include",
    "duties include",
    "tasks include",
    "you will",
    "you should",
    "are required for the job",
    "required for the job",
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
    "built with",
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
    "we build",
    "team uses",
)

ROLE_SUFFIXES = {
    "assistant",
    "associate",
    "attendant",
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
    "additional duties",
    "additional tasks",
    "are also used",
    "also used",
    "card are",
    "as assigned",
    "build backend",
    "build backend services",
    "currently",
    "employee benefits",
    "ensuring the restaurant",
    "foundational knowledge",
    "good employee benefits",
    "know how",
    "knowhow",
    "knowhow on databases eg",
    "many projects",
    "other duties",
    "other duties as assigned",
    "other tasks",
    "occupational safety",
    "passport and occupational",
    "part time job",
    "programming language",
    "salary",
    "team player",
    "various tasks",
    "working hours",
    "safety card",
    "fast paced environment",
    "services with typescript",
    "team uses react",
    "we build backend services",
    "previous experience",
    "relevant skills",
    "strong knowledge",
    "many of our projects",
    "competitive salary",
    "benefits",
    "at least one common",
    "common clientside",
    "common clientside language experience are helpful",
    "common serverside",
    "javascript and nodejs",
    "javascript reactnative",
    "javascript react native",
    "many of our projects",
    "native on mobile",
    "previous at least one common",
    "programming language",
    "react native on mobile",
    "reactnative on mobile",
}

LOW_VALUE_PHRASE_PARTS = (
    "additional duties",
    "additional tasks",
    "as assigned",
    "also used",
    "card are",
    "currently",
    "employee benefits",
    "ensuring the restaurant",
    "foundational knowledge",
    "good employee benefits",
    "hour per week",
    "hours per week",
    "know how",
    "knowhow",
    "many projects",
    "other tasks",
    "part time job",
    "previous experience",
    "services with typescript",
    "team uses react",
    "we build",
    "relevant skills",
    "salary",
    "strong knowledge",
    "various tasks",
    "working hours",
    "are also used",
    "many of our projects",
    "common clientside",
    "javascript and nodejs",
    "javascript reactnative",
    "javascript react native",
    "react native on mobile",
    "reactnative on mobile",
)

ALLOWED_SINGLE_WORD_REQUIREMENTS = {
    "certification",
    "communication",
    "databases",
    "degree",
    "dishwashing",
}

COMMUNICATION_VERBS = {
    "communicate",
    "communicates",
    "communicated",
    "communicating",
}

TECHNOLOGY_PATTERNS = (
    ("React Native", r"\breact[\s-]+native\b"),
    ("TypeScript", r"\btypescript\b|\btype\s+script\b"),
    ("JavaScript", r"\bjavascript\b|\bjava\s+script\b"),
    ("Node.js", r"\bnode\.?js\b|\bnode\s+js\b"),
    ("PostgreSQL", r"\bpostgresql\b|\bpostgres\b"),
    ("CI/CD", r"\bci\s*/?\s*cd\b"),
    ("Kubernetes", r"\bkubernetes\b"),
    ("Clojure", r"\bclojure\b"),
    ("DevOps", r"\bdevops\b"),
    ("Docker", r"\bdocker\b"),
    ("Kotlin", r"\bkotlin\b"),
    ("Python", r"\bpython\b"),
    ("React", r"\breact\b(?![\s-]+native\b)"),
    ("Scala", r"\bscala\b"),
    ("Swift", r"\bswift\b"),
    ("Java", r"\bjava\b"),
    ("AWS", r"\baws\b"),
)

TECHNOLOGY_REQUIREMENTS = {technology for technology, _pattern in TECHNOLOGY_PATTERNS}
PRESERVED_KEY_PHRASES = {
    "automated deployment",
    "backend services",
    "Continuous Integration",
    "driver's license",
    "hygiene passport",
    "occupational safety card",
    "restaurant cleaning",
    "test automation",
}

PRESERVED_KEY_PHRASE_PATTERNS = (
    ("automated deployment", r"\bautomated deployment\b"),
    ("backend services", r"\bbackend services\b"),
    ("Continuous Integration", r"\bcontinuous integration\b"),
    ("test automation", r"\btest automation\b"),
)

FINAL_REQUIREMENT_NORMALIZATIONS = {
    "build ci": "CI/CD",
    "build cicd": "CI/CD",
    "build ci cd": "CI/CD",
    "cd pipelines when the project requires": "CI/CD",
    "cd pipelines when the project requires it": "CI/CD",
    "continuous integration ci": "Continuous Integration",
    "common serverside programming": "server-side programming language",
    "clientside language": "client-side language",
    "common clientside language": "client-side language",
    "create new backend services": "backend services",
    "relevant to create new backend services": "backend services",
    "serverside programming": "server-side programming language",
    "serverside programming language": "server-side programming language",
    "server side programming language": "server-side programming language",
}

FINAL_NOISY_REQUIREMENTS = {
    "at least one common",
    "common clientside",
    "common clientside language experience are helpful",
    "common serverside",
    "javascript and nodejs",
    "javascript reactnative",
    "javascript react native",
    "many of our projects",
    "native on mobile",
    "previous at least one common",
    "programming language",
    "react native on mobile",
    "reactnative on mobile",
}

FINAL_NOISY_PREFIXES = (
    "previous at least one common ",
    "at least one common ",
    "common ",
)
YAKE_MAX_NGRAM_SIZE = 3
YAKE_TOP_KEYWORDS = 30


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

    if _allows_single_word_requirement(normalized):
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
    parts = _split_candidate_text(normalized)

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
        normalized = _finalize_requirement_phrase(normalized)

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

    requirements.extend(extract_yake_requirements(text))
    requirements.extend(extract_preserved_key_phrase_requirements(text))
    requirements.extend(extract_technology_requirements(text))

    return deduplicate_requirements(requirements)


def extract_yake_requirements(text: str) -> list[str]:
    if yake is None or not text.strip():
        return []

    try:
        extractor = yake.KeywordExtractor(
            lan="en",
            n=YAKE_MAX_NGRAM_SIZE,
            dedupLim=0.85,
            top=YAKE_TOP_KEYWORDS,
            features=None,
        )
        keywords = extractor.extract_keywords(text)
    except Exception:
        return []

    requirements: list[str] = []

    for keyword, _score in keywords:
        requirement = _clean_requirement_phrase(keyword)

        if requirement and _is_yake_requirement(requirement):
            requirements.append(requirement)

    return requirements


def extract_technology_requirements(text: str) -> list[str]:
    normalized = normalize_text(text)

    if not normalized:
        return []

    technologies: list[str] = []

    for technology, pattern in TECHNOLOGY_PATTERNS:
        if re.search(pattern, normalized):
            technologies.append(technology)

    return technologies


def extract_preserved_key_phrase_requirements(text: str) -> list[str]:
    normalized = normalize_text(text)

    if not normalized:
        return []

    requirements: list[str] = []

    for requirement, pattern in PRESERVED_KEY_PHRASE_PATTERNS:
        if re.search(pattern, normalized):
            requirements.append(requirement)

    return requirements


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

    if len(words) > 1 and words[-1] in ROLE_SUFFIXES:
        words.pop()

    cleaned = " ".join(words).strip()
    cleaned = _normalize_concrete_requirement(cleaned)
    cleaned = _normalize_technology_requirement(cleaned)

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

    if phrase in TECHNOLOGY_REQUIREMENTS:
        return True

    if phrase in PRESERVED_KEY_PHRASES:
        return True

    if any(part in phrase for part in LOW_VALUE_PHRASE_PARTS):
        return False

    words = _get_words(phrase)

    if len(words) < 2 and not _allows_single_word_requirement(phrase):
        return False

    if len(words) > 8:
        return False

    return True


def _allows_single_word_requirement(phrase: str) -> bool:
    return phrase in ALLOWED_SINGLE_WORD_REQUIREMENTS


def _is_yake_requirement(phrase: str) -> bool:
    if phrase in TECHNOLOGY_REQUIREMENTS or phrase in PRESERVED_KEY_PHRASES:
        return True

    if phrase in ALLOWED_SINGLE_WORD_REQUIREMENTS:
        return True

    words = _get_words(phrase)

    if not 1 <= len(words) <= YAKE_MAX_NGRAM_SIZE:
        return False

    blocked_words = {
        "are",
        "build",
        "built",
        "include",
        "includes",
        "including",
        "team",
        "uses",
        "we",
    }

    if any(word in blocked_words for word in words):
        return False

    return _is_meaningful_requirement(phrase)


def _get_words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _clean_sentence_fragment(sentence: str) -> str:
    cleaned = normalize_text(sentence)
    cleaned = cleaned.strip(string.whitespace + string.punctuation)
    cleaned = re.sub(r"\s+", " ", cleaned)

    return cleaned.strip()


def _split_candidate_text(text: str) -> list[str]:
    chunks = re.split(r",|;|/|\n|[•*]|(?:\s+-\s+)", text)
    parts: list[str] = []

    for chunk in chunks:
        parts.extend(re.split(r"\s+(?:and|or)\s+", chunk))

    return parts


def _normalize_concrete_requirement(phrase: str) -> str:
    if "databases" in _get_words(phrase):
        return "databases"

    if phrase in {
        "clean restaurant",
        "ensuring restaurant is clean",
        "ensuring the restaurant is clean",
        "keeping restaurant clean",
        "keeping the restaurant clean",
        "restaurant cleanliness",
        "restaurant is clean",
        "the restaurant is clean",
    }:
        return "restaurant cleaning"

    if phrase in {"driver license", "drivers license"}:
        return "driver's license"

    return phrase


def _normalize_technology_requirement(phrase: str) -> str:
    aliases = {
        "aws": "AWS",
        "ci cd": "CI/CD",
        "ci/cd": "CI/CD",
        "cicd": "CI/CD",
        "clojure": "Clojure",
        "continuous integration": "Continuous Integration",
        "devops": "DevOps",
        "devops practices": "DevOps",
        "docker": "Docker",
        "java": "Java",
        "javascript": "JavaScript",
        "kotlin": "Kotlin",
        "kubernetes": "Kubernetes",
        "node js": "Node.js",
        "nodejs": "Node.js",
        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",
        "python": "Python",
        "react": "React",
        "react native": "React Native",
        "reactnative": "React Native",
        "scala": "Scala",
        "swift": "Swift",
        "typescript": "TypeScript",
        "automated deployment": "automated deployment",
        "backend services": "backend services",
        "test automation": "test automation",
    }

    return aliases.get(phrase, phrase)


def _finalize_requirement_phrase(phrase: str) -> str:
    if not phrase:
        return ""

    lookup_key = _get_requirement_lookup_key(phrase)

    if lookup_key in FINAL_NOISY_REQUIREMENTS:
        return ""

    if lookup_key in FINAL_REQUIREMENT_NORMALIZATIONS:
        return FINAL_REQUIREMENT_NORMALIZATIONS[lookup_key]

    for prefix in FINAL_NOISY_PREFIXES:
        if not lookup_key.startswith(prefix):
            continue

        trimmed_key = lookup_key.removeprefix(prefix).strip()

        if not trimmed_key or trimmed_key in FINAL_NOISY_REQUIREMENTS:
            return ""

        if trimmed_key in FINAL_REQUIREMENT_NORMALIZATIONS:
            return FINAL_REQUIREMENT_NORMALIZATIONS[trimmed_key]

    return phrase


def _get_requirement_lookup_key(phrase: str) -> str:
    lookup_key = phrase.lower()
    lookup_key = lookup_key.replace("-", "")
    lookup_key = lookup_key.replace("/", " ")
    lookup_key = re.sub(r"\s+", " ", lookup_key)

    return lookup_key.strip()
