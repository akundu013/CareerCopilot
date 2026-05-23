from app.services.requirement_extractor import extract_requirements


def test_extracts_concrete_restaurant_requirements() -> None:
    job_description = (
        "We are looking for a dish attendant for a part-time job at Fortum "
        "Loviisa, where the working hours are 20 hours per week. The salary "
        "varies from \u20ac11.97 to \u20ac13.00 per hour depending on experience "
        "and education. Your duties include dishwashing, ensuring the "
        "restaurant is clean, and assisting with other tasks. A driver's "
        "license, hygiene passport and occupational safety card are required "
        "for the job, and we offer good employee benefits."
    )

    requirements = extract_requirements(job_description)

    assert "dishwashing" in requirements
    assert "restaurant cleaning" in requirements
    assert "driver's license" in requirements
    assert "hygiene passport" in requirements
    assert "occupational safety card" in requirements
    assert "your duties include" not in requirements
    assert "other tasks" not in requirements
    assert "working hours" not in requirements
    assert "salary" not in requirements
    assert "employee benefits" not in requirements
    assert "part-time job" not in requirements


def test_extracts_single_word_requirement_lines() -> None:
    job_description = (
        "Commercial cleaning\n"
        "Dishwashing\n"
        "Hygiene & sanitation\n"
        "Teamwork\n"
        "Reliability & punctuality\n"
        "Time management"
    )

    requirements = extract_requirements(job_description)

    assert "commercial cleaning" in requirements
    assert "dishwashing" in requirements
    assert "time management" in requirements


def test_extracts_clean_software_requirements() -> None:
    job_description = (
        "Many of our projects are built with TypeScript/JavaScript and Node.js. "
        "Python are also used. Know-how on databases (e.g. PostgreSQL)."
    )

    requirements = extract_requirements(job_description)

    assert "TypeScript" in requirements
    assert "JavaScript" in requirements
    assert "Node.js" in requirements
    assert "Python" in requirements
    assert "databases" in requirements
    assert "PostgreSQL" in requirements
    assert "many of our projects are typescript" not in requirements
    assert "python are also used" not in requirements
    assert "knowhow on databases eg" not in requirements


def test_normalizes_common_technology_aliases() -> None:
    job_description = "nodejs, postgres, ci cd, react-native"

    requirements = extract_requirements(job_description)

    assert "Node.js" in requirements
    assert "PostgreSQL" in requirements
    assert "CI/CD" in requirements
    assert "React Native" in requirements


def test_final_cleanup_removes_noisy_software_requirements() -> None:
    job_description = (
        "Many of our projects are built with TypeScript/JavaScript and Node.js. "
        "Previous at least one common server-side programming language is expected. "
        "Relevant skills to create new backend services with TypeScript. "
        "Strong knowledge of Continuous Integration CI and build CI/CD pipelines "
        "when the project requires it. Know-how on databases (e.g. PostgreSQL). "
        "React Native on mobile and common clientside language experience are helpful."
    )

    requirements = extract_requirements(job_description)

    assert "Continuous Integration" in requirements
    assert "CI/CD" in requirements
    assert "backend services" in requirements
    assert "server-side programming language" in requirements
    assert "JavaScript" in requirements
    assert "Node.js" in requirements
    assert "TypeScript" in requirements
    assert "continuous integration ci" not in requirements
    assert "build ci" not in requirements
    assert "cd pipelines when the project requires it" not in requirements
    assert "javascript and nodejs" not in requirements
    assert "react native on mobile" not in requirements
