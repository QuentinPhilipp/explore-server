import os
from datetime import datetime
from typing import Dict, Optional, List

import requests

from sqlalchemy.orm import Session

from models import crud
from schemas.activities import DetailedActivity, SummaryActivity
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

    def get_strava(self, endpoint: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict] = None):
        headers_with_auth = self._headers(headers=headers)
        response = requests.get(endpoint, headers=headers_with_auth, params=params)
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
            crud.create_activity(db=self._db, activity=activity)
        else:
            crud.update_activity(db=self._db, activity=activity)

    def _list_activity_recursive(self, page: Optional[int] = 1) -> List[Dict]:
        url = f"https://www.strava.com/api/v3/athlete/activities"
        per_page_max = 200
        params = {
            'per_page': per_page_max,
            'page': page
        }
        data = self.get_strava(endpoint=url, params=params).json()
        if len(data) == per_page_max:
            data.extend(self._list_activity_recursive(page=page+1))
        return data

    @staticmethod
    def _parse_activities(raw_activities: List[Dict]) -> List[SummaryActivity]:
        return [SummaryActivity(**raw_activity) for raw_activity in raw_activities]

    def list_activity_for_athlete_id(self):
        data = self._list_activity_recursive()
        activities = self._parse_activities(data)
        return activities
