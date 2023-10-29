from __future__ import annotations

from pydantic import BaseModel

from schemas.athletes import Athlete


class LoginBase(BaseModel):
    expires_at: int
    refresh_token: str
    access_token: str


class LoginDetails(LoginBase):
    id: int
    athlete_id: int

    class Config:
        from_attributes = True


class LoginCreate(LoginBase):
    athlete: Athlete

    class Config:
        from_attributes = True


class RefreshedLogin(LoginBase):
    token_type: str
    expires_in: int