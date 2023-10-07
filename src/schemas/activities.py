from __future__ import annotations

from datetime import datetime
from typing import List, Set, Optional

from pydantic import BaseModel

from schemas.athletes import MetaAthleteStrava
from schemas.strava_models import SummaryGear, DetailedActivityMap, SummaryActivityMap


class ActivityBase(BaseModel):
    id: int
    athlete: MetaAthleteStrava
    name: str
    distance: float
    moving_time: int
    elapsed_time: int
    total_elevation_gain: float
    elev_high: Optional[float] = 0
    elev_low: Optional[float] = 0
    sport_type: str
    start_date: datetime
    start_date_local: datetime
    timezone: str
    start_latlng: List
    end_latlng: List
    trainer: bool
    commute: bool
    manual: bool
    private: bool
    visibility: str
    flagged: bool
    workout_type: Optional[int] = None
    average_speed: float
    max_speed: float
    hide_from_home: Optional[bool] = False
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
    gear_id: Optional[str] = ""
    map: SummaryActivityMap


class DetailedActivity(ActivityBase):
    gear: Optional[SummaryGear] = None
    map: DetailedActivityMap

    @property
    def gear_id(self) -> str:
        if self.gear is not None:
            return self.gear.id
        return ""

    class Config:
        from_attributes = True
