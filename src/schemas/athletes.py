from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class MetaAthleteStrava(BaseModel):
    id: int


class Athlete(MetaAthleteStrava):
    id: int
    username: str
    firstname: str
    lastname: str
    bio: str
    city: str
    state: str
    country: str
    sex: str
    created_at: datetime
    updated_at: datetime
    profile_medium: str
    weight: float

    class Config:
        from_attributes = True
