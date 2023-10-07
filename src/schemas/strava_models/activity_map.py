from pydantic import BaseModel


class ActivityMap(BaseModel):
    id: str
    polyline: str