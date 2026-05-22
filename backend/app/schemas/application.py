from enum import Enum

from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class CreateApplicationRequest(BaseModel):
    company: str = Field(min_length=1)
    role: str = Field(min_length=1)
    status: ApplicationStatus
    location: str | None = None
    jobUrl: str | None = None
    salaryRange: str | None = None
    notes: str | None = None
    dateApplied: str | None = None


class UpdateApplicationRequest(BaseModel):
    company: str | None = Field(default=None, min_length=1)
    role: str | None = Field(default=None, min_length=1)
    status: ApplicationStatus | None = None
    location: str | None = None
    jobUrl: str | None = None
    salaryRange: str | None = None
    notes: str | None = None
    dateApplied: str | None = None


class ApplicationResponse(BaseModel):
    id: str
    userId: str
    company: str
    role: str
    status: ApplicationStatus
    location: str | None = None
    jobUrl: str | None = None
    salaryRange: str | None = None
    notes: str | None = None
    dateApplied: str | None = None
    createdAt: str
    updatedAt: str
