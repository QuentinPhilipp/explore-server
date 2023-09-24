import os
from typing import Dict

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from models.Athlete import Athlete

load_dotenv()


app = FastAPI()


@app.get("/ping")
def ping():
    return {"msg": "pong"}


@app.get("/login")
def login_strava():
    login_url = (f"https://www.strava.com/oauth/authorize?client_id={os.getenv('STRAVA_CLIENT_ID')}&response_type=code"
                 f"&redirect_uri={os.getenv('STRAVA_AUTH_URL')}&approval_prompt=force"
                 f"&scope={os.getenv('STRAVA_AUTH_SCOPE')}")
    return RedirectResponse(login_url)


@app.get("/exchange_token")
def exchange_token(code: str, scope: str):
    if scope != "read,activity:read_all":
        raise HTTPException(status_code=400, detail="Select authorization read and activity:read_all")

    try:
        url = (f"https://www.strava.com/api/v3/oauth/token?client_id={os.getenv('STRAVA_CLIENT_ID')}&"
               f"client_secret={os.getenv('STRAVA_CLIENT_SECRET')}&code={code}&grant_type=authorization_code")
        response = requests.post(url)
        athlete = register_athlete(response.json())

        if athlete is not None:
            return {"athleteId": athlete.id}
        raise HTTPException(status_code=400, detail=f"Error registering athlete.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error registering athlete. {str(e)}")


def register_athlete(auth_data: Dict) -> Athlete:
    athlete = Athlete.from_strava_auth(_id=auth_data['athlete']['id'], source=auth_data)
    athlete.set()
    return athlete
