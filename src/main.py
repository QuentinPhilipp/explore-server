"""
Main application
"""
import os
from typing import Annotated, Union

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Query, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from schemas.webhooks import WebhookCreate
from schemas.auth import LoginCreate
from schemas.misc import StravaErrors
from database.db import SessionLocal, engine, Base
from models import crud
from strava.api import StravaApi

Base.metadata.create_all(bind=engine)


load_dotenv()

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/ping")
def ping():
    return {"msg": "pong"}


@app.get("/login")
def login_strava():
    """
    /login endpoint to get Strava OAuth url
    """
    login_url = (f"https://www.strava.com/oauth/authorize?client_id={os.getenv('STRAVA_CLIENT_ID')}&response_type=code"
                 f"&redirect_uri={os.getenv('STRAVA_AUTH_URL')}&approval_prompt=force"
                 f"&scope={os.getenv('STRAVA_AUTH_SCOPE')}")
    return RedirectResponse(login_url)


@app.get("/exchange_token")
def exchange_token(code: str, scope: str, db: Session = Depends(get_db)):
    """
    /exchange_token endpoint to get Strava short-lived access token
    """
    if scope != "read,activity:read_all":
        raise HTTPException(status_code=400, detail="Select authorization read and activity:read_all")

    url = (f"https://www.strava.com/api/v3/oauth/token?client_id={os.getenv('STRAVA_CLIENT_ID')}&"
           f"client_secret={os.getenv('STRAVA_CLIENT_SECRET')}&code={code}&grant_type=authorization_code")

    response = requests.post(url, timeout=10)

    if response.status_code == 200:
        login_create_data = LoginCreate(**response.json())
        db_athlete = crud.get_athlete_by_id(db, login_create_data.athlete.id)
        if db_athlete is None:
            db_athlete = crud.create_athlete_login(db, login_create_data)
        else:
            crud.update_athlete_login(db, login_create_data, athlete_id=db_athlete.id)
        return {"athlete": db_athlete}

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
    else:
        print(f"Owner not registered in users. Skip webhook {webhook_activity}")
