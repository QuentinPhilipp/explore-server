from pydantic import BaseModel


class ActivityMap(BaseModel):
    id: str


class DetailedActivityMap(ActivityMap):
    polyline: str


class SummaryActivityMap(ActivityMap):
    summary_polyline: str

    @property
    def polyline(self):
        return self.summary_polyline