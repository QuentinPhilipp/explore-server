from typing import Dict, Optional

from models.LoginDetail import LoginDetail
from database.db import athlete_db


class Athlete:
    def __init__(
            self,
            _id: str,
            username: str,
            firstname: str,
            lastname: str,
            bio: str,
            city: str,
            state: str,
            country: str,
            sex: str,
            premium: bool,
            summit: bool,
            created_at: str,
            updated_at: str,
            badge_type_id: int,
            weight: float,
            profile_medium: str,
            login_details: Optional[LoginDetail] = None
    ):
        self._id = _id
        self._username = username
        self._firstname = firstname
        self._lastname = lastname
        self._bio = bio
        self._city = city
        self._state = state
        self._country = country
        self._sex = sex
        self._premium = premium
        self._summit = summit
        self._created_at = created_at
        self._updated_at = updated_at
        self._badge_type_id = badge_type_id
        self._weight = weight
        self._profile_medium = profile_medium
        self._login_details = login_details

    @staticmethod
    def from_strava_auth(_id, source):
        athlete = source['athlete']
        return Athlete(
            _id=str(_id),
            username=athlete["username"],
            firstname=athlete["firstname"],
            lastname=athlete["lastname"],
            bio=athlete["bio"],
            city=athlete["city"],
            state=athlete["state"],
            country=athlete["country"],
            sex=athlete["sex"],
            premium=athlete["premium"],
            summit=athlete["summit"],
            created_at=athlete["created_at"],
            updated_at=athlete["updated_at"],
            badge_type_id=athlete["badge_type_id"],
            weight=athlete["weight"],
            profile_medium=athlete["profile_medium"],
            login_details=LoginDetail.from_dict(source)
        )

    @staticmethod
    def from_db(_id, source):
        return Athlete(
            _id=str(_id),
            username=source["username"],
            firstname=source["firstname"],
            lastname=source["lastname"],
            bio=source["bio"],
            city=source["city"],
            state=source["state"],
            country=source["country"],
            sex=source["sex"],
            premium=source["premium"],
            summit=source["summit"],
            created_at=source["created_at"],
            updated_at=source["updated_at"],
            badge_type_id=source["badge_type_id"],
            weight=source["weight"],
            profile_medium=source["profile_medium"],
            login_details=LoginDetail.from_dict(source['login_details'])
        )

    @property
    def login_details(self):
        return self._login_details

    @property
    def id(self):
        return self._id

    def to_dict(self) -> Dict:
        # Remove "_" private prefix
        private_dict = self.__dict__
        public_dict = {}
        for key, value in private_dict.items():
            if key not in ("_id", "_login_details"):
                public_dict[key[1:]] = value

        public_dict["login_details"] = self._login_details.to_dict()
        return public_dict

    @staticmethod
    def get(_id=None):
        athlete = athlete_db.document(str(_id)).get()
        if athlete.exists:
            return Athlete.from_db(_id, athlete.to_dict())
        return None

    def set(self):
        athlete_db.document(self._id).set(self.to_dict())

    def __repr__(self):
        return f"Athlete(id={self._id}, username={self._username}, login:{self._login_details})"
