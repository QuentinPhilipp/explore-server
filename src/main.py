"""
Main application
"""
import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from models import crud, models, schemas
from database.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


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
        login_create_data = schemas.LoginCreate(**response.json())
        db_athlete = crud.get_athlete_by_id(db, login_create_data.athlete.id)
        if db_athlete is None:
            db_athlete = crud.create_athlete_login(db, login_create_data)
        else:
            crud.update_athlete_login(db, login_create_data)
        return {"athlete": db_athlete}

    elif response.status_code == 400:
        error = schemas.StravaErrors(**response.json())
        print(error)
        raise HTTPException(status_code=400, detail=f"Error registering athlete. {error}")
    else:
        raise HTTPException(status_code=400, detail=f"Unkown error. {response.json()}")


@app.post("/webhook")
def webhook(webhook_activity: schemas.WebhookCreate, db: Session = Depends(get_db)):
    """
    /webhook endpoint to get Strava webhook activities
    """
    owner = crud.get_athlete_by_id(db, athlete_id=webhook_activity.owner_id)
    if owner is not None:
        db_webhook = crud.create_webhook(db, webhook_activity)
        return {"webhook": db_webhook}
    else:
        print(f"Owner not registered in users. Skip webhook {webhook_activity}")
