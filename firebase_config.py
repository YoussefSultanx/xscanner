import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("x-scanner-c7127-firebase-adminsdk-is9d0-9298dc04b8.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
