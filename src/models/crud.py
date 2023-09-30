from sqlalchemy.orm import Session

from models import models, schemas


def get_athlete_by_id(db: Session, athlete_id: int):
    return db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()


def create_athlete_login(db: Session, login_info: schemas.LoginCreate):
    db_athlete = models.Athlete(**login_info.athlete.model_dump())
    db_athlete_login = models.LoginDetails(**login_info.model_dump(exclude={'athlete'}), athlete_id=db_athlete.id)

    db.add(db_athlete)
    db.add(db_athlete_login)
    db.commit()
    db.refresh(db_athlete)
    db.refresh(db_athlete_login)
    return db_athlete


def update_athlete_login(db: Session, login_info: schemas.LoginCreate):
    login = db.query(models.LoginDetails).filter(models.LoginDetails.athlete_id == login_info.athlete.id).first()
    login.expires_at = login_info.expires_at
    login.refresh_token = login_info.refresh_token
    login.access_token = login_info.access_token
    db.commit()


def create_webhook(db: Session, webhook: schemas.WebhookCreate):
    webhook = models.WebhookActivities(**webhook.model_dump())
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook