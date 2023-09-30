from __future__ import annotations

import datetime

from pydantic import BaseModel


class Athlete(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    bio: str
    city: str
    state: str
    country: str
    sex: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    profile_medium: str
    weight: float

    class Config:
        from_attributes = True
