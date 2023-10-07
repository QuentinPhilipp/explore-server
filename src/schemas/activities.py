from __future__ import annotations

from datetime import datetime
from typing import List, Set, Optional

from pydantic import BaseModel

from schemas.athletes import MetaAthleteStrava
from schemas.strava_models import ActivityMap, SummaryGear


class ActivityBase(BaseModel):
    id: int
    athlete: MetaAthleteStrava
    name: str
    distance: float
    moving_time: int
    elapsed_time: int
    total_elevation_gain: float
    elev_high: float
    elev_low: float
    sport_type: str
    start_date: datetime
    start_date_local: datetime
    timezone: str
    start_latlng: List
    end_latlng: List
    map: ActivityMap
    trainer: bool
    commute: bool
    manual: bool
    private: bool
    flagged: bool
    workout_type: int
    average_speed: float
    max_speed: float
    hide_from_home: bool
    average_watts: Optional[float] = 0
    device_watts: Optional[bool] = False
    max_watts: Optional[int] = 0
    weighted_average_watts: Optional[int] = 0

    @property
    def polyline(self) -> str:
        return self.map.polyline

    @property
    def athlete_id(self) -> int:
        return self.athlete.id

    @staticmethod
    def db_exclude_list() -> Set:
        return {'athlete', 'map', 'start_latlng', 'end_latlng', 'gear_id', 'gear'}


class SummaryActivity(ActivityBase):
    gear_id: str


class DetailedActivity(ActivityBase):
    gear: SummaryGear

    @property
    def gear_id(self) -> str:
        return self.gear.id

    class Config:
        from_attributes = True
