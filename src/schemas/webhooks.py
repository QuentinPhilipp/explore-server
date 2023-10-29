from __future__ import annotations

from typing import Dict

from pydantic import BaseModel


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
