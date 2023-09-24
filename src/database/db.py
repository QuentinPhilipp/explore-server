import firebase_admin

from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("../explorev2-key.json")
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
athlete_db = db.collection("athletes")
login_db = db.collection("login_details")
