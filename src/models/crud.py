from typing import Optional, Union, Dict, Any, List

from sqlalchemy.orm import Session
from sqlalchemy import select

from models.activities import ActivityModel
from models.auth import LoginDetailsModel
from models.athletes import AthleteModel
from models.webhooks import WebhookActivitiesModel
from schemas.activities import DetailedActivity, SummaryActivity
from schemas.auth import LoginCreate, LoginBase
from schemas.webhooks import WebhookCreate


def get_athlete_by_id(db: Session, athlete_id: int) -> Optional[AthleteModel]:
    return db.query(AthleteModel).filter(AthleteModel.id == athlete_id).first()


def create_athlete_login(db: Session, login_info: LoginCreate) -> Optional[AthleteModel]:
    db_athlete = AthleteModel(**login_info.athlete.model_dump())
    db_athlete_login = LoginDetailsModel(**login_info.model_dump(exclude={'athlete'}), athlete_id=db_athlete.id)

    db.add(db_athlete)
    db.add(db_athlete_login)
    db.commit()
    db.refresh(db_athlete)
    db.refresh(db_athlete_login)
    return db_athlete


def update_athlete_login(db: Session, login_info: LoginBase, athlete_id: int) -> Optional[LoginDetailsModel]:
    login = db.query(LoginDetailsModel).filter(
        LoginDetailsModel.athlete_id == athlete_id).first()
    login.expires_at = login_info.expires_at
    login.refresh_token = login_info.refresh_token
    login.access_token = login_info.access_token
    db.commit()
    db.refresh(login)
    return login


def get_athlete_login(db: Session, athlete_id: int) -> Optional[LoginDetailsModel]:
    return db.query(LoginDetailsModel).filter(LoginDetailsModel.athlete_id == athlete_id).first()


def create_webhook(db: Session, webhook: WebhookCreate) -> Optional[WebhookActivitiesModel]:
    webhook = WebhookActivitiesModel(**webhook.model_dump())
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook


def delete_webhook_by_id(db: Session, webhook_id: int):
    db.query(WebhookActivitiesModel).filter(WebhookActivitiesModel.id == webhook_id).delete()
    db.commit()


def get_activity_by_id(db: Session, activity_id: int):
    return db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()


def get_routes_by_athlete_id(db: Session, athlete_id: int):
    return (db.query(ActivityModel)
            .filter(ActivityModel.athlete_id == athlete_id)
            .order_by(ActivityModel.start_date_local)
            .all())


def _create_activity_model_from_schema(activity: Union[SummaryActivity, DetailedActivity]):
    return ActivityModel(
        **activity.model_dump(exclude=activity.db_exclude_list()),
        athlete_id=activity.athlete_id,
        polyline=activity.polyline,
        start_lat=activity.start_latlng[0] if len(activity.start_latlng) else None,
        start_lng=activity.start_latlng[1] if len(activity.start_latlng) else None,
        end_lat=activity.end_latlng[0] if len(activity.end_latlng) else None,
        end_lng=activity.end_latlng[1] if len(activity.end_latlng) else None,
        gear_id=activity.gear_id
    )


def create_activity(db: Session, activity: Union[SummaryActivity, DetailedActivity]) -> Optional[ActivityModel]:
    activity = _create_activity_model_from_schema(activity)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def create_activity_batch(db: Session, activities: List[Union[SummaryActivity, DetailedActivity]]):
    activities_models = [_create_activity_model_from_schema(activity) for activity in activities]
    db.bulk_save_objects(activities_models)
    db.commit()


def update_activity(db: Session, activity: Union[SummaryActivity, DetailedActivity]) -> Optional[ActivityModel]:
    new_activity_dict = activity.model_dump(exclude=activity.db_exclude_list())
    new_activity_dict.update({
        'athlete_id': activity.athlete_id,
        'polyline': activity.polyline,
        'start_lat': activity.start_latlng[0] if len(activity.start_latlng) else None,
        'start_lng': activity.start_latlng[1] if len(activity.start_latlng) else None,
        'end_lat': activity.end_latlng[0] if len(activity.end_latlng) else None,
        'end_lng': activity.end_latlng[1] if len(activity.end_latlng) else None,
        'gear_id': activity.gear_id
    })
    db.query(ActivityModel).filter(ActivityModel.id == activity.id).update(new_activity_dict)
    db.commit()
    return get_activity_by_id(db=db, activity_id=activity.id)


def update_activity_by_id(db: Session,  activity_id: int, changes: Dict[str, Any]) -> Optional[ActivityModel]:
    activity = db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()

    for key, value in changes.items():
        # For whatever reason, Strava webhooks use "title" and the rest of the api use "name" for the activity title
        # and string for boolean values
        if key == "title":
            key = "name"

        if value == "false":
            value = False
        elif value == "true":
            value = True

        setattr(activity, key, value)
    db.commit()
    return get_activity_by_id(db=db, activity_id=activity.id)


def delete_activity_by_id(db: Session, activity_id: int):
    db.query(ActivityModel).filter(ActivityModel.id == activity_id).delete()
    db.commit()
