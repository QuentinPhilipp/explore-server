from __future__ import annotations

import uuid
from datetime import datetime
from typing import Dict


class LoginDetail:
    def __init__(
            self,
            expires_at: int,
            expires_in: int,
            refresh_token: str,
            access_token: str
    ):
        self._uuid = str(uuid.uuid4())
        self._expires_at = expires_at
        self._expires_in = expires_in
        self._refresh_token = refresh_token
        self._access_token = access_token

    @staticmethod
    def from_dict(source) -> LoginDetail:
        return LoginDetail(
            expires_at=source["expires_at"],
            expires_in=source["expires_in"],
            refresh_token=source["refresh_token"],
            access_token=source["access_token"],
        )

    def to_dict(self) -> Dict:
        return {
            "expires_at": self._expires_at,
            "expires_in": self._expires_in,
            "refresh_token": self._refresh_token,
            "access_token": self._access_token,
        }

    def is_expired(self) -> bool:
        return datetime.utcfromtimestamp(int(self._expires_at)) < datetime.utcnow()