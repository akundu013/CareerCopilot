from datetime import datetime, timezone
from typing import Any

from firebase_admin import auth

from app.config.demo import get_demo_user_email
from app.services.firebase_admin_service import initialize_firebase_admin
from app.services.firestore_service import get_firestore_client

SEED_MARKERS = {
    "isSeededDemoData": True,
    "createdByDemoSeed": True,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_demo_user_uid() -> str:
    initialize_firebase_admin()
    user = auth.get_user_by_email(get_demo_user_email())

    return user.uid


def seed_demo_data() -> dict[str, int]:
    demo_user_id = get_demo_user_uid()
    now = _utc_now()
    client = get_firestore_client()
    user_document = client.collection("users").document(demo_user_id)

    seed_groups = {
        "applications": _get_demo_applications(demo_user_id, now),
        "resumes": _get_demo_resumes(demo_user_id, now),
        "analyses": _get_demo_analyses(demo_user_id, now),
        "interviews": _get_demo_interviews(demo_user_id, now),
    }

    for collection_name, records in seed_groups.items():
        collection = user_document.collection(collection_name)

        for record in records:
            collection.document(record["id"]).set(record)

    return {
        collection_name: len(records)
        for collection_name, records in seed_groups.items()
    }


def _with_seed_metadata(record: dict[str, Any], now: str) -> dict[str, Any]:
    return {
        **record,
        **SEED_MARKERS,
        "createdAt": record.get("createdAt", now),
        "updatedAt": now,
    }


def _get_demo_applications(user_id: str, now: str) -> list[dict[str, Any]]:
    applications = [
        {
            "id": "demo-app-frontend-dev",
            "company": "Northstar Labs",
            "role": "Frontend Developer",
            "status": "applied",
            "location": "Helsinki, Finland",
            "jobUrl": "https://example.com/jobs/frontend-developer",
            "salaryRange": "€4,200–€5,200 / month",
            "notes": "Strong match for React and TypeScript experience.",
            "dateApplied": "2026-05-06",
        },
        {
            "id": "demo-app-fullstack-dev",
            "company": "Harbor Cloud",
            "role": "Full Stack Developer",
            "status": "interviewing",
            "location": "Remote EU",
            "jobUrl": "https://example.com/jobs/full-stack-developer",
            "salaryRange": "€5,000–€6,200 / month",
            "notes": "Technical interview scheduled. Review backend API design.",
            "dateApplied": "2026-05-09",
        },
        {
            "id": "demo-app-data-analyst",
            "company": "Signal Metrics",
            "role": "Data Analyst",
            "status": "rejected",
            "location": "Espoo, Finland",
            "jobUrl": "https://example.com/jobs/data-analyst",
            "salaryRange": "€3,800–€4,600 / month",
            "notes": "Rejected after recruiter screen. Role required deeper BI tooling.",
            "dateApplied": "2026-04-26",
        },
        {
            "id": "demo-app-backend-dev",
            "company": "Atlas Systems",
            "role": "Backend Developer",
            "status": "applied",
            "location": "Tampere, Finland",
            "jobUrl": "https://example.com/jobs/backend-developer",
            "salaryRange": "€4,700–€5,900 / month",
            "notes": "Follow up with hiring manager next week.",
            "dateApplied": "2026-05-14",
        },
        {
            "id": "demo-app-consultant",
            "company": "Blueprint Digital",
            "role": "Software Consultant",
            "status": "offer",
            "location": "Hybrid Helsinki",
            "jobUrl": "https://example.com/jobs/software-consultant",
            "salaryRange": "€5,400–€6,400 / month",
            "notes": "Offer received. Compare benefits and project fit.",
            "dateApplied": "2026-04-18",
        },
        {
            "id": "demo-app-product-engineer",
            "company": "Brightpath AI",
            "role": "Product Engineer",
            "status": "interviewing",
            "location": "Remote",
            "jobUrl": "https://example.com/jobs/product-engineer",
            "salaryRange": "€5,100–€6,100 / month",
            "notes": "Portfolio walkthrough requested.",
            "dateApplied": "2026-05-17",
        },
        {
            "id": "demo-app-platform-engineer",
            "company": "FlowStack",
            "role": "Platform Engineer",
            "status": "applied",
            "location": "Turku, Finland",
            "jobUrl": "https://example.com/jobs/platform-engineer",
            "salaryRange": "€4,900–€6,000 / month",
            "notes": "Emphasize CI/CD and cloud deployment experience.",
            "dateApplied": "2026-05-19",
        },
        {
            "id": "demo-app-mobile-dev",
            "company": "PocketWorks",
            "role": "React Native Developer",
            "status": "withdrawn",
            "location": "Remote",
            "jobUrl": "https://example.com/jobs/react-native-developer",
            "salaryRange": "€4,400–€5,400 / month",
            "notes": "Withdrawn because role shifted to native iOS focus.",
            "dateApplied": "2026-04-30",
        },
    ]

    return [
        _with_seed_metadata({**application, "userId": user_id}, now)
        for application in applications
    ]


def _get_demo_resumes(user_id: str, now: str) -> list[dict[str, Any]]:
    resumes = [
        {
            "id": "demo-resume-software-engineer",
            "fileName": "Demo_Software_Engineer_Resume.pdf",
            "fileUrl": "https://example.com/demo/software-engineer-resume.pdf",
            "storagePath": f"users/{user_id}/resumes/demo-software-engineer.pdf",
            "contentType": "application/pdf",
            "sizeBytes": 248000,
            "status": "parsed",
            "parsedText": (
                "Software engineer with experience in TypeScript, JavaScript, "
                "React, Node.js, Python, PostgreSQL, Docker, Kubernetes, AWS, "
                "REST API development, CI/CD practices, automated deployment, "
                "test automation, communication, and product collaboration."
            ),
        },
        {
            "id": "demo-resume-operations-support",
            "fileName": "Demo_Operations_Support_Resume.pdf",
            "fileUrl": "https://example.com/demo/operations-support-resume.pdf",
            "storagePath": f"users/{user_id}/resumes/demo-operations-support.pdf",
            "contentType": "application/pdf",
            "sizeBytes": 196000,
            "status": "parsed",
            "parsedText": (
                "Reliable operations support candidate with commercial cleaning, "
                "dishwashing and kitchen cleaning experience, hygiene and "
                "sanitation awareness, teamwork, time management, punctuality, "
                "and customer service strengths."
            ),
        },
    ]

    return [
        _with_seed_metadata({**resume, "userId": user_id}, now)
        for resume in resumes
    ]


def _get_demo_analyses(user_id: str, now: str) -> list[dict[str, Any]]:
    analyses = [
        {
            "id": "demo-analysis-frontend",
            "resumeId": "demo-resume-software-engineer",
            "resumeFileName": "Demo_Software_Engineer_Resume.pdf",
            "jobDescription": (
                "Frontend role requiring TypeScript, JavaScript, React, CI/CD, "
                "test automation, and strong communication."
            ),
            "matchScore": 84.0,
            "extractedRequirements": [
                "TypeScript",
                "JavaScript",
                "React",
                "CI/CD",
                "test automation",
                "communication",
            ],
            "matchedRequirements": [
                "TypeScript",
                "JavaScript",
                "React",
                "CI/CD",
                "test automation",
                "communication",
            ],
            "missingRequirements": [],
            "improvementSuggestions": [
                "Add one short project bullet that quantifies frontend impact.",
                "Mention production accessibility or performance work if relevant.",
            ],
        },
        {
            "id": "demo-analysis-backend",
            "resumeId": "demo-resume-software-engineer",
            "resumeFileName": "Demo_Software_Engineer_Resume.pdf",
            "jobDescription": (
                "Backend developer role with Node.js, Python, PostgreSQL, Docker, "
                "Kubernetes, AWS, CI/CD, and REST API ownership."
            ),
            "matchScore": 88.0,
            "extractedRequirements": [
                "Node.js",
                "Python",
                "PostgreSQL",
                "Docker",
                "Kubernetes",
                "AWS",
                "CI/CD",
                "REST API",
            ],
            "matchedRequirements": [
                "Node.js",
                "Python",
                "PostgreSQL",
                "Docker",
                "Kubernetes",
                "AWS",
                "CI/CD",
                "REST API",
            ],
            "missingRequirements": [],
            "improvementSuggestions": [
                "Add deployment ownership details to strengthen platform credibility.",
                "Include one example of API reliability or monitoring work.",
            ],
        },
        {
            "id": "demo-analysis-platform",
            "resumeId": "demo-resume-software-engineer",
            "resumeFileName": "Demo_Software_Engineer_Resume.pdf",
            "jobDescription": (
                "Platform role requiring DevOps, Kubernetes, AWS, CI/CD, automated "
                "deployment, observability, and backend services."
            ),
            "matchScore": 76.0,
            "extractedRequirements": [
                "DevOps",
                "Kubernetes",
                "AWS",
                "CI/CD",
                "automated deployment",
                "observability",
                "backend services",
            ],
            "matchedRequirements": [
                "DevOps",
                "Kubernetes",
                "AWS",
                "CI/CD",
                "automated deployment",
                "backend services",
            ],
            "missingRequirements": ["observability"],
            "improvementSuggestions": [
                "Add monitoring, alerting, or logging experience if you have it.",
                "Clarify which cloud services you used in production.",
            ],
        },
        {
            "id": "demo-analysis-dish-attendant",
            "resumeId": "demo-resume-operations-support",
            "resumeFileName": "Demo_Operations_Support_Resume.pdf",
            "jobDescription": (
                "Dish attendant role requiring dishwashing, restaurant cleaning, "
                "hygiene passport, teamwork, reliability, and time management."
            ),
            "matchScore": 67.0,
            "extractedRequirements": [
                "dishwashing",
                "restaurant cleaning",
                "hygiene passport",
                "teamwork",
                "reliability",
                "time management",
            ],
            "matchedRequirements": [
                "dishwashing",
                "restaurant cleaning",
                "teamwork",
                "reliability",
                "time management",
            ],
            "missingRequirements": ["hygiene passport"],
            "improvementSuggestions": [
                "Add hygiene passport status if the certificate is current.",
                "Mention restaurant cleaning responsibilities with concrete examples.",
            ],
        },
        {
            "id": "demo-analysis-consultant",
            "resumeId": "demo-resume-software-engineer",
            "resumeFileName": "Demo_Software_Engineer_Resume.pdf",
            "jobDescription": (
                "Consulting role requiring stakeholder communication, React, "
                "backend services, agile delivery, and client service."
            ),
            "matchScore": 72.0,
            "extractedRequirements": [
                "stakeholder communication",
                "React",
                "backend services",
                "agile delivery",
                "client service",
            ],
            "matchedRequirements": [
                "stakeholder communication",
                "React",
                "backend services",
            ],
            "missingRequirements": ["agile delivery", "client service"],
            "improvementSuggestions": [
                "Add examples of direct stakeholder or client collaboration.",
                "Show delivery cadence, prioritization, or agile team experience.",
            ],
        },
    ]

    return [
        _with_seed_metadata({**analysis, "userId": user_id}, now)
        for analysis in analyses
    ]


def _get_demo_interviews(user_id: str, now: str) -> list[dict[str, Any]]:
    interviews = [
        {
            "id": "demo-interview-frontend",
            "analysisId": "demo-analysis-frontend",
            "resumeId": "demo-resume-software-engineer",
            "resumeFileName": "Demo_Software_Engineer_Resume.pdf",
            "questions": [
                {
                    "id": "general-1",
                    "category": "general",
                    "prompt": "Walk me through your most relevant frontend project.",
                },
                {
                    "id": "technical-1",
                    "category": "technical",
                    "prompt": "How do you structure a React feature for maintainability?",
                },
                {
                    "id": "behavioral-1",
                    "category": "behavioral",
                    "prompt": "Tell me about a time you improved delivery quality.",
                },
            ],
            "answers": [
                {"questionId": "general-1", "answer": ""},
                {"questionId": "technical-1", "answer": ""},
                {"questionId": "behavioral-1", "answer": ""},
            ],
        },
        {
            "id": "demo-interview-backend",
            "analysisId": "demo-analysis-backend",
            "resumeId": "demo-resume-software-engineer",
            "resumeFileName": "Demo_Software_Engineer_Resume.pdf",
            "questions": [
                {
                    "id": "general-1",
                    "category": "general",
                    "prompt": "Which backend system are you most proud of building?",
                },
                {
                    "id": "technical-1",
                    "category": "technical",
                    "prompt": "How would you design a reliable authenticated API?",
                },
                {
                    "id": "behavioral-1",
                    "category": "behavioral",
                    "prompt": "Describe a production issue you helped resolve.",
                },
            ],
            "answers": [
                {"questionId": "general-1", "answer": ""},
                {"questionId": "technical-1", "answer": ""},
                {"questionId": "behavioral-1", "answer": ""},
            ],
        },
        {
            "id": "demo-interview-operations",
            "analysisId": "demo-analysis-dish-attendant",
            "resumeId": "demo-resume-operations-support",
            "resumeFileName": "Demo_Operations_Support_Resume.pdf",
            "questions": [
                {
                    "id": "general-1",
                    "category": "general",
                    "prompt": "What makes you reliable in a busy service environment?",
                },
                {
                    "id": "behavioral-1",
                    "category": "behavioral",
                    "prompt": "Tell me about a time you kept quality high under pressure.",
                },
                {
                    "id": "technical-1",
                    "category": "technical",
                    "prompt": "How do you keep kitchen cleaning work safe and organized?",
                },
            ],
            "answers": [
                {"questionId": "general-1", "answer": ""},
                {"questionId": "behavioral-1", "answer": ""},
                {"questionId": "technical-1", "answer": ""},
            ],
        },
    ]

    return [
        _with_seed_metadata({**interview, "userId": user_id}, now)
        for interview in interviews
    ]
