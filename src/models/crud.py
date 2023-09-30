from typing import Optional

from sqlalchemy.orm import Session

from models.auth import LoginDetailsModel
from models.athletes import AthleteModel
from models.webhooks import WebhookActivitiesModel
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