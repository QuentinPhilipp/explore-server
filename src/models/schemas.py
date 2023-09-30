from __future__ import annotations

import datetime
from typing import List, Dict

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


class StravaErrors(BaseModel):
    message: str
    errors: List[Dict[str, str]]


class WebhookCreate(BaseModel):
    object_type: str
    object_id: int
    aspect_type: str
    updates: Dict
    owner_id: int
    subscription_id: int
    event_time: int


class Webhook(WebhookCreate):
    id: int
