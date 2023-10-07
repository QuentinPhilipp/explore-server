from __future__ import annotations

from pydantic import BaseModel


class AuthCode(BaseModel):
    code: str
    scope: str