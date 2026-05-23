from pydantic import BaseModel, Field


class CreateAnalysisRequest(BaseModel):
    resumeId: str = Field(min_length=1)
    jobDescription: str = Field(min_length=1)


class AnalysisResponse(BaseModel):
    id: str
    userId: str
    resumeId: str
    resumeFileName: str
    jobDescription: str
    matchScore: float = Field(ge=0, le=100)
    extractedRequirements: list[str]
    matchedRequirements: list[str]
    missingRequirements: list[str]
    improvementSuggestions: list[str]
    createdAt: str
    updatedAt: str


class AnalysisSummaryResponse(BaseModel):
    id: str
    resumeId: str
    resumeFileName: str
    matchScore: float = Field(ge=0, le=100)
    matchedRequirements: list[str]
    missingRequirements: list[str]
    createdAt: str
    updatedAt: str
