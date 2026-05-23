from app.services.match_engine import analyze_match, requirement_matches_resume


def test_dish_attendant_resume_matches_concrete_related_requirements() -> None:
    resume_text = (
        "Commercial cleaning\n"
        "Dishwashing & kitchen cleaning\n"
        "Hygiene & sanitation\n"
        "Teamwork\n"
        "Reliability & punctuality\n"
        "Time management"
    )
    requirements = [
        "dishwashing",
        "restaurant cleaning",
        "driver's license",
        "hygiene passport",
        "occupational safety card",
    ]

    result = analyze_match(resume_text, requirements)

    assert result["matchScore"] > 0
    assert "dishwashing" in result["matchedRequirements"]
    assert "restaurant cleaning" in result["matchedRequirements"]
    assert "driver's license" in result["missingRequirements"]
    assert "hygiene passport" in result["missingRequirements"]
    assert "occupational safety card" in result["missingRequirements"]


def test_related_cleaning_terms_match_restaurant_cleaning() -> None:
    assert requirement_matches_resume(
        "restaurant cleaning",
        "Commercial cleaning and kitchen cleaning experience.",
    )


def test_strict_requirements_do_not_match_loose_related_words() -> None:
    assert not requirement_matches_resume("project management", "Project")
    assert not requirement_matches_resume("driver's license", "Driving interest")
    assert not requirement_matches_resume(
        "occupational safety card",
        "Safety awareness",
    )


def test_matches_letter_spaced_pdf_text() -> None:
    resume_text = (
        "p r e v i o u s  r e s t a u r a n t  d i s h w a s h i n g "
        " e x p e r i e n c e . c o m m e r c i a l  c l e a n i n g"
    )

    result = analyze_match(
        resume_text,
        ["commercial cleaning", "dishwashing"],
    )

    assert result["matchScore"] == 100
    assert result["matchedRequirements"] == [
        "commercial cleaning",
        "dishwashing",
    ]


def test_matches_common_technical_aliases_and_related_devops_terms() -> None:
    resume_text = (
        "Javascript (ES6+), Typescript, Python, Angular, React, Node.js, "
        "Express.js, RESTful API Development, PostgreSQL, Docker, Kubernetes, "
        "CI/CD Practices, AWS"
    )
    requirements = [
        "JavaScript",
        "Node.js",
        "TypeScript",
        "CI/CD",
        "DevOps",
        "Python",
        "React",
        "PostgreSQL",
    ]

    result = analyze_match(resume_text, requirements)

    assert result["matchScore"] == 100
    assert result["matchedRequirements"] == requirements
    assert result["missingRequirements"] == []


def test_strict_technical_terms_do_not_overmatch() -> None:
    assert not requirement_matches_resume("Java", "JavaScript")
    assert not requirement_matches_resume("React Native", "React")
    assert not requirement_matches_resume("React", "React Native")


def test_matches_spaced_technical_aliases() -> None:
    assert requirement_matches_resume("TypeScript", "type script")
    assert requirement_matches_resume("JavaScript", "java script")
    assert requirement_matches_resume("CI/CD", "ci cd practices")


def test_matches_letter_spaced_pdf_technical_skills() -> None:
    resume_text = (
        "J a v a s c r i p t  ( E S 6 + ) ,  "
        "T y p e s c r i p t ,  P y t h o n\n"
        "A n g u l a r ,  R e a c t ,  N o d e . j s\n"
        "P o s t g r e S Q L ,  D o c k e r ,  K u b e r n e t e s ,  "
        "C I / C D  P r a c t i c e s ,  A W S"
    )
    requirements = [
        "JavaScript",
        "Node.js",
        "TypeScript",
        "CI/CD",
        "DevOps",
        "Python",
        "React",
        "PostgreSQL",
    ]

    result = analyze_match(resume_text, requirements)

    assert result["matchScore"] == 100
    assert result["matchedRequirements"] == requirements
    assert result["missingRequirements"] == []
