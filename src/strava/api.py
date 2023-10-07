import os
from datetime import datetime
from typing import Dict, Optional

import requests

from sqlalchemy.orm import Session

from models import crud
from schemas.activities import DetailedActivity
from schemas.auth import RefreshedLogin


class StravaApi:
    def __init__(self, db: Session, athlete_id: int):
        self._db = db
        self._athlete_id = athlete_id

    def _headers(self, headers: Optional[Dict[str, str]] = None):
        token = self.get_token()
        base_headers = {"Authorization": f"Bearer {token}"}
        if headers is not None:
            return base_headers.update(headers)
        return base_headers

    def get_strava(self, endpoint: str, headers: Optional[Dict[str, str]] = None):
        headers_with_auth = self._headers(headers=headers)
        response = requests.get(endpoint, headers=headers_with_auth)
        if response.status_code == 200:
            return response
        else:
            print(f"Error while requesting GET {endpoint}")

    def get_token(self) -> str:
        login = crud.get_athlete_login(self._db, self._athlete_id)

        if datetime.utcfromtimestamp(login.expires_at) < datetime.utcnow():
            params = {
                'client_id': os.getenv('STRAVA_CLIENT_ID'),
                'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
                'grant_type': 'refresh_token',
                'refresh_token': login.refresh_token
            }
            response = requests.post("https://www.strava.com/api/v3/oauth/token", params=params)
            if response.status_code == 200:
                refreshed_login_data = RefreshedLogin(**response.json())
                crud.update_athlete_login(self._db, refreshed_login_data, athlete_id=self._athlete_id)
                return refreshed_login_data.access_token
            else:
                print("ERROR while refreshing token")
        else:
            return login.access_token

    def get_activity_from_id(self, activity_id: int):
        url = f"https://www.strava.com/api/v3/activities/{activity_id}?"
        response = self.get_strava(url)
        activity = DetailedActivity(**response.json())
        if crud.get_activity_by_id(db=self._db, activity_id=activity.id) is None:
            db_activity = crud.create_activity(db=self._db, activity=activity)
        else:
            db_activity = crud.update_activity(db=self._db, activity=activity)

        print(db_activity)