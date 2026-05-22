from pydantic import BaseModel


class AuthenticatedUserResponse(BaseModel):
    uid: str
    email: str | None = None
    email_verified: bool | None = None
