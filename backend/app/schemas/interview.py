from enum import Enum

from pydantic import BaseModel, Field


class InterviewQuestionCategory(str, Enum):
    GENERAL = "general"
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"


class InterviewQuestion(BaseModel):
    id: str = Field(min_length=1)
    category: InterviewQuestionCategory
    prompt: str = Field(min_length=1)


class InterviewAnswer(BaseModel):
    questionId: str = Field(min_length=1)
    answer: str = ""


class CreateInterviewSessionRequest(BaseModel):
    analysisId: str = Field(min_length=1)


class UpdateInterviewAnswersRequest(BaseModel):
    answers: list[InterviewAnswer]


class InterviewSessionResponse(BaseModel):
    id: str
    userId: str
    analysisId: str
    resumeId: str
    resumeFileName: str
    questions: list[InterviewQuestion]
    answers: list[InterviewAnswer]
    createdAt: str
    updatedAt: str
