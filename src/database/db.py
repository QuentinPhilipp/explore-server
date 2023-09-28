"""
Access to Firebase database
"""

import os
from base64 import b64decode

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from dotenv import load_dotenv

load_dotenv()

cred_dict = {
  "type": os.getenv("FIREBASE_TYPE"),
  "project_id": os.getenv("FIREBASE_PROJECT_ID"),
  "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
  "private_key": b64decode(os.getenv("FIREBASE_PRIVATE_KEY")),
  "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
  "client_id": os.getenv("FIREBASE_CLIENT_ID"),
  "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
  "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
  "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
  "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
  "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN")
}

cred = credentials.Certificate(cred_dict)
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
athlete_db = db.collection("athletes")
login_db = db.collection("login_details")
