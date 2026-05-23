from pydantic import BaseModel, Field


class CreateAnalysisRequest(BaseModel):
    resumeId: str = Field(min_length=1)
    jobDescription: str = Field(min_length=1)


class AnalysisResponse(BaseModel):
    id: str
    userId: str
    resumeId: str
    jobDescription: str
    matchScore: float = Field(ge=0, le=100)
    matchedSkills: list[str]
    missingSkills: list[str]
    improvementSuggestions: list[str]
    createdAt: str
    updatedAt: str


class AnalysisSummaryResponse(BaseModel):
    id: str
    resumeId: str
    matchScore: float = Field(ge=0, le=100)
    matchedSkills: list[str]
    missingSkills: list[str]
    createdAt: str
    updatedAt: str
