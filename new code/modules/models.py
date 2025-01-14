from flask_login import UserMixin
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the Firebase Admin SDK
cred = credentials.Certificate("web-vulnerability-scanne-4aba6-firebase-adminsdk-gcgsj-408dae61d5.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    @staticmethod
    def get(user_id):
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return User(id=user_id, username=user_data.get('username'), email=user_data.get('email'))
        return None
