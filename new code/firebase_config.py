import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("web-vulnerability-scanne-4aba6-firebase-adminsdk-gcgsj-408dae61d5.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()