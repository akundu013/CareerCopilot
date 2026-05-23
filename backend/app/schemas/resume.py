from enum import Enum

from pydantic import BaseModel, Field


class ResumeStatus(str, Enum):
    UPLOADED = "uploaded"
    PARSED = "parsed"
    PARSE_FAILED = "parse_failed"


class CreateResumeRequest(BaseModel):
    fileName: str = Field(min_length=1)
    fileUrl: str = Field(min_length=1)
    storagePath: str = Field(min_length=1)
    contentType: str = Field(min_length=1)
    sizeBytes: int = Field(ge=0)
    status: ResumeStatus


class UpdateResumeRequest(BaseModel):
    fileName: str | None = Field(default=None, min_length=1)
    fileUrl: str | None = Field(default=None, min_length=1)
    storagePath: str | None = Field(default=None, min_length=1)
    contentType: str | None = Field(default=None, min_length=1)
    sizeBytes: int | None = Field(default=None, ge=0)
    status: ResumeStatus | None = None
    parsedText: str | None = None


class ResumeResponse(BaseModel):
    id: str
    userId: str
    fileName: str
    fileUrl: str
    storagePath: str
    contentType: str
    sizeBytes: int
    status: ResumeStatus
    parsedText: str | None = None
    createdAt: str
    updatedAt: str
