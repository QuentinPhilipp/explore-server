from __future__ import annotations

from typing import List, Dict

from pydantic import BaseModel


class StravaErrors(BaseModel):
    message: str
    errors: List[Dict[str, str]]
