"""
Model definition of an Athlete
"""
from __future__ import annotations
from typing import Dict, Optional

from models.login_detail import LoginDetail
from database.db import athlete_db


class Athlete:
    """
    Athlete class. Contains all utility to read and write from Strava and Firebase
    """
    def __init__(
            self,
            _id: str,
            athlete: Dict,
            login_details: Optional[LoginDetail] = None
    ):
        self._id = _id
        self._username = athlete['username']
        self._firstname = athlete['firstname']
        self._lastname = athlete['lastname']
        self._bio = athlete['bio']
        self._city = athlete['city']
        self._state = athlete['state']
        self._country = athlete['country']
        self._sex = athlete['sex']
        self._created_at = athlete['created_at']
        self._updated_at = athlete['updated_at']
        self._weight = athlete['weight']
        self._profile_medium = athlete['profile_medium']
        self._login_details = login_details

    @staticmethod
    def from_strava_auth(_id, source) -> Athlete:
        """Create an Athlete from the data returned by Strava on auth"""
        athlete = source['athlete']
        return Athlete(
            _id=str(_id),
            athlete=athlete,
            login_details=LoginDetail.from_db(source)
        )

    @staticmethod
    def from_db(_id, source) -> Athlete:
        """Create an Athlete from the data returned by Firebase"""
        return Athlete(
            _id=str(_id),
            athlete=source,
            login_details=LoginDetail.from_db(source['login_details'])
        )

    @property
    def login_details(self) -> LoginDetail:
        """Expose the LoginDetails object"""
        return self._login_details

    @property
    def id(self) -> str:
        """Expose athlete's id"""
        return self._id

    def to_dict(self) -> Dict:
        """
        Serialize the athlete into a dict
        Remove "_" private prefix
        """
        private_dict = self.__dict__
        public_dict = {}
        for key, value in private_dict.items():
            if key not in ("_id", "_login_details"):
                public_dict[key[1:]] = value

        public_dict["login_details"] = self._login_details.to_dict()
        return public_dict

    @staticmethod
    def get(_id=None) -> Optional[Athlete]:
        """
        Get the athlete if existing in db
        """
        athlete = athlete_db.document(str(_id)).get()
        if athlete.exists:
            return Athlete.from_db(_id, athlete.to_dict())
        return None

    def set(self) -> None:
        """
        Set the athlete in db. Overwrite if already existing with this id
        """
        athlete_db.document(self._id).set(self.to_dict())

    def __repr__(self) -> str:
        return f"Athlete(id={self._id}, username={self._username}, login:{self._login_details})"
