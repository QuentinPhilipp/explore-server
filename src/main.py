"""
Main application
"""
import os
from typing import Annotated, Union

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Query, BackgroundTasks, Request
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from schemas.strava_models.auth_code import AuthCode
from schemas.webhooks import WebhookCreate
from schemas.auth import LoginCreate
from schemas.misc import StravaErrors
from database.db import SessionLocal, engine, Base
from models import crud
from strava.api import StravaApi

Base.metadata.create_all(bind=engine)


load_dotenv()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
]

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv('SESSION_KEY'),
    max_age=3600,
    https_only=False,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def check_user_session(request: Request):
    athlete_id = request.session.get('athlete_id')
    if athlete_id is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    return athlete_id


@app.get("/ping")
def ping():
    return {"msg": "pong"}


@app.post("/exchange_token")
def exchange_token(request: Request, auth_code: AuthCode, db: Session = Depends(get_db)):
    """
    /exchange_token endpoint to get Strava short-lived access token
    """
    if auth_code.scope != "read,activity:read_all":
        raise HTTPException(status_code=400, detail="Select authorization read and activity:read_all")

    url = (f"https://www.strava.com/api/v3/oauth/token?client_id={os.getenv('STRAVA_CLIENT_ID')}&"
           f"client_secret={os.getenv('STRAVA_CLIENT_SECRET')}&code={auth_code.code}&grant_type=authorization_code")

    response = requests.post(url, timeout=10)

    if response.status_code == 200:
        login_create_data = LoginCreate(**response.json())
        db_athlete = crud.get_athlete_by_id(db, login_create_data.athlete.id)
        if db_athlete is None:
            db_athlete = crud.create_athlete_login(db, login_create_data)
        else:
            crud.update_athlete_login(db, login_create_data, athlete_id=db_athlete.id)

        request.session['athlete_id'] = db_athlete.id
        return "OK"

    elif response.status_code == 400:
        error = StravaErrors(**response.json())
        print(error)
        raise HTTPException(status_code=400, detail=f"Error registering athlete. {error}")
    else:
        raise HTTPException(status_code=400, detail=f"Unknown error. {response.json()}")


@app.post("/webhook", status_code=200)
def webhook(webhook_activity: WebhookCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    /webhook endpoint to get Strava webhook activities
    """
    background_tasks.add_task(register_webhook, webhook_activity, db)


@app.get("/webhook")
def webhook_validation(verify_token: Annotated[Union[str, None], Query(alias="hub.verify_token")] = None,
                       challenge: Annotated[Union[str, None], Query(alias="hub.challenge")] = None,
                       mode: Annotated[Union[str, None], Query(alias="hub.mode")] = None,
                       ):
    """
    Strava needs to validate the endpoint for the webhook. This allows their server to validate the endpoint.
    """
    if verify_token != "StravaWebhookRideout" or mode != "subscribe":
        raise HTTPException(status_code=400, detail="Wrong token or mode, webhook not registered")
    return {'hub.challenge': challenge}


def register_webhook(webhook_activity: WebhookCreate, db: Session):
    """
    async registration of the webhook in DB
    """
    strava_api = StravaApi(db=db, athlete_id=webhook_activity.owner_id)
    athlete = crud.get_athlete_by_id(db, athlete_id=webhook_activity.owner_id)
    if athlete is not None and webhook_activity.object_type == "activity":
        webhook_db = crud.create_webhook(db, webhook_activity)

        if webhook_activity.aspect_type == "create":
            strava_api.get_activity_from_id(webhook_db.object_id)
        elif webhook_activity.aspect_type == "update":
            crud.update_activity_by_id(
                db=db,
                activity_id=webhook_activity.object_id,
                changes=webhook_activity.updates
            )
        elif webhook_activity.aspect_type == "delete":
            crud.delete_activity_by_id(
                db=db,
                activity_id=webhook_activity.object_id
            )
        crud.delete_webhook_by_id(db, webhook_db.id)
    else:
        print(f"Owner not registered in users. Skip webhook {webhook_activity}")


@app.get("/activity/{activity_id}")
def get_activity(activity_id: int,
                 db: Session = Depends(get_db),
                 athlete_id=Depends(check_user_session)):
    activity = crud.get_activity_by_id(db=db, activity_id=activity_id)
    if activity.athlete_id != athlete_id:
        raise HTTPException(status_code=403, detail="You cannot access another user's activity")
    return activity


@app.post("/backpopulate", status_code=200)
def back_populate_post(athlete_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(back_populate, db, athlete_id)


def back_populate(db: Session, athlete_id: int):
    api = StravaApi(db=db, athlete_id=athlete_id)
    activities = api.list_activity_for_athlete_id()
    crud.create_activity_batch(db=db, activities=activities)
    return activities