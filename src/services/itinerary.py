from models import crud
from sqlalchemy.orm import Session


def get_routes_by_date(athlete_id: int, db: Session):
    activities = crud.get_routes_by_athlete_id(db=db, athlete_id=athlete_id)

    activities_routes = [{'polyline': activity.polyline, 'date': activity.start_date_local} for activity in activities]
    return activities_routes