from __future__ import annotations

from pydantic import BaseModel


class SummaryGear(BaseModel):
    id: str
    primary: bool
    name: str
    distance: int