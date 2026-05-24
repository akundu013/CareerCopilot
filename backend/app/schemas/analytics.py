from pydantic import BaseModel, Field


class ApplicationsByStatusItem(BaseModel):
    status: str
    count: int = Field(ge=0)


class WeeklyApplicationActivityItem(BaseModel):
    week: str
    count: int = Field(ge=0)


class RequirementFrequencyItem(BaseModel):
    requirement: str
    count: int = Field(ge=0)


class AnalyticsSummaryResponse(BaseModel):
    totalApplications: int = Field(ge=0)
    applicationsByStatus: list[ApplicationsByStatusItem]
    responseRate: float = Field(ge=0, le=100)
    weeklyApplicationActivity: list[WeeklyApplicationActivityItem]
    totalResumes: int = Field(ge=0)
    parsedResumes: int = Field(ge=0)
    totalAnalyses: int = Field(ge=0)
    averageMatchScore: float = Field(ge=0, le=100)
    topMissingRequirements: list[RequirementFrequencyItem]
    topMatchedRequirements: list[RequirementFrequencyItem]
    totalInterviewSessions: int = Field(ge=0)
    savedInterviewAnswers: int = Field(ge=0)
