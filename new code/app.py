import sys
import os
import threading
import datetime
import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth
from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import RegistrationForm
import requests
import logging

# Adjust paths for module imports
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.join(current_dir, 'modules')
sys.path.insert(0, modules_path)

from modules.port_scanning import start_scan
from modules.xss_scanning import start_xss_scan
from modules.sql_injection_scanning import crawl_and_scan
from modules.rce_scanning import start_rce_scan

# Initialize Firebase Admin SDK
cred = credentials.Certificate("web-vulnerability-scanne-4aba6-firebase-adminsdk-gcgsj-408dae61d5.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_form'

class User(UserMixin):
    def __init__(self, id, username, email, admin_status):
        self.id = id
        self.username = username
        self.email = email
        self.admin_status = admin_status

    @staticmethod
    def get(user_id):
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return User(id=user_id, username=user_data.get('username'), email=user_data.get('email'), admin_status=user_data.get('admin_status'))
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('Email and password are required', 'danger')
        return redirect(url_for('login_form'))

    try:
        # Firebase REST API to verify email and password
        api_key = 'AIzaSyDfjcl7cWfEBVh6wSJSSb5BuY3nWd4_O50'  # Replace with your Firebase Web API key
        payload = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }
        response = requests.post(f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}', json=payload)
        data = response.json()

        if 'error' in data:
            flash(data['error']['message'], 'danger')
            return redirect(url_for('login_form'))

        user_id = data['localId']
        id_token = data['idToken']

        # Check if user exists in Firestore
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            user_obj = User(id=user_id, username=user_data.get('username'), email=user_data.get('email'), admin_status=user_data.get('admin_status'))
            login_user(user_obj)
            session['user_id'] = user_id
            session['id_token'] = id_token
            session['admin_status'] = user_data.get('admin_status')  # Store admin_status in session
            return redirect(url_for('home'))
        else:
            flash('User not found in Firestore', 'danger')
            return redirect(url_for('login_form'))
    except requests.exceptions.RequestException as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('login_form'))



@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        try:
            user = firebase_auth.create_user(
                email=email,
                password=password
            )
            user_data = {
                'uid': user.uid,
                'username': username,
                'email': email,
                'admin_status': 0
            }
            db.collection('users').document(user.uid).set(user_data)
            flash('Account created for {}!'.format(email), 'success')
            return redirect(url_for('login_form'))
        except firebase_admin._auth_utils.EmailAlreadyExistsError:
            flash('Email is already registered. Please use a different email.', 'danger')
        except Exception as e:
            flash(f'An unexpected error occurred: {e}', 'danger')
    return render_template('register.html', form=form)

@app.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/start_scanning')
@login_required
def start_scanning():
    return render_template('start_scanning.html', user=current_user)

@app.route('/view_scan_history')
@login_required
def view_scan_history():
    user_id = current_user.id
    scans_ref = db.collection('scans').where('user_id', '==', user_id).order_by('timestamp', direction=firestore.Query.DESCENDING)
    scans = [scan.to_dict() for scan in scans_ref.stream()]
    
    for scan in scans:
        if isinstance(scan['timestamp'], datetime.datetime):
            scan['timestamp'] = scan['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        else:
            scan['timestamp'] = str(scan['timestamp'])

    return render_template('view_scan_history.html', scans=scans)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    session.pop('id_token', None)
    session.pop('admin_status', None)
    return redirect(url_for('index'))

from firebase_admin import auth as firebase_auth, _auth_utils

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    data = request.form
    new_username = data.get('new_username')
    new_email = data.get('new_email')
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    user_id = current_user.id

    try:
        # Reauthenticate user
        user = firebase_auth.get_user(user_id)
        # In the Admin SDK, reauthentication isn't necessary as the Admin SDK has elevated privileges

        # Update user fields in Firestore
        update_data = {}
        if new_username:
            update_data['username'] = new_username
        if new_email:
            update_data['email'] = new_email
            firebase_auth.update_user(user_id, email=new_email)
        if new_password:
            firebase_auth.update_user(user_id, password=new_password)

        if update_data:
            db.collection('users').document(user_id).update(update_data)

        if new_username:
            firebase_auth.update_user(user_id, display_name=new_username)

        return redirect(url_for('profile'))
    except Exception as e:
        return jsonify({'error': str(e)}), 400


from firebase_admin import auth as firebase_auth

from firebase_admin import auth as firebase_auth

@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    user_id = current_user.id

    try:
        # Delete user from Firebase Authentication
        firebase_auth.delete_user(user_id)

        # Delete user document from Firestore
        db.collection('users').document(user_id).delete()

        logout_user()
        session.pop('user_id', None)

        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({'error': str(e)}), 400



@app.route('/admin')
@login_required
def admin():
    if current_user.admin_status != 1:  # Check as integer
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))
    
    # Fetch users from Firestore
    users_ref = db.collection('users').stream()
    users = []
    for user in users_ref:
        user_dict = user.to_dict()
        user_dict['id'] = user.id
        users.append(user_dict)
    
    return render_template('admin.html', users=users)



@app.route('/admin/toggle_admin', methods=['POST'])
@login_required
def toggle_admin():
    if current_user.admin_status != 1:  # Ensure admin check
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    user_id = data.get('user_id')
    current_status = data.get('current_status')

    try:
        user_ref = db.collection('users').document(user_id)
        new_status = 0 if current_status == 1 else 1
        user_ref.update({'admin_status': new_status})

        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400



@app.route('/admin/delete_user', methods=['POST'])
@login_required
def admin_delete_user():
    if current_user.admin_status != 1:  # Ensure admin check
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    user_id = data.get('user_id')

    try:
        user_ref = db.collection('users').document(user_id)
        user_ref.delete()

        firebase_auth.delete_user(user_id)

        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/admin/update_user', methods=['POST'])
@login_required
def admin_update_user():
    if current_user.admin_status != 1:  # Ensure admin check
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.form
    user_id = data.get('user_id')
    new_username = data.get('username')
    new_email = data.get('email')
    new_password = data.get('new_password')

    try:
        user_ref = db.collection('users').document(user_id)

        update_data = {}
        if new_username:
            update_data['username'] = new_username
        if new_email:
            update_data['email'] = new_email
        if new_password:
            firebase_auth.update_user(user_id, password=new_password)

        user_ref.update(update_data)

        return redirect(url_for('admin'))
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/admin/view_scan_history')
@login_required
def admin_view_scan_history():
    if current_user.admin_status != 1:  # Ensure admin check
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))

    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user ID'}), 400

    scans_ref = db.collection('scans').where('user_id', '==', user_id).order_by('timestamp', direction=firestore.Query.DESCENDING)
    scans = [scan.to_dict() for scan in scans_ref.stream()]
    
    for scan in scans:
        if isinstance(scan['timestamp'], datetime.datetime):
            scan['timestamp'] = scan['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        else:
            scan['timestamp'] = str(scan['timestamp'])

    user_ref = db.collection('users').document(user_id).get()
    user = user_ref.to_dict() if user_ref.exists else {}

    return render_template('admin_view_scan_history.html', scans=scans, user=user)


@app.route('/admin/delete_scan', methods=['POST'])
@login_required
def admin_delete_scan():
    scan_id = request.form.get('scan_id')
    user_id = request.form.get('user_id')

    try:
        db.collection('scans').document(scan_id).delete()
        return redirect(url_for('admin_view_scan_history', user_id=user_id))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/scan', methods=['POST'])
@login_required
def scan():
    url = request.form.get('url')
    port_scan = 'port' in request.form
    sql_scan = 'sql' in request.form
    xss_scan = 'xss' in request.form
    rce_scan = 'rce' in request.form

    if not url:
        flash('URL is required!', 'danger')
        return redirect(url_for('start_scanning'))

    def run_scan(host, user_id):
        port_scan_results = []
        sql_scan_results = []
        xss_scan_results = []
        rce_scan_results = []

        if port_scan:
            ports = None  # Define default ports or get from user input
            port_scan_results = start_scan(host, ports)

        if xss_scan:
            xss_scan_results = start_xss_scan(host).splitlines()
        
        if sql_scan:
            sql_scan_results = crawl_and_scan(url)
        
        if rce_scan:
            rce_scan_results = start_rce_scan(url)

        scan_data = {
            "user_id": user_id,
            "host": host,
            "port_scan_results": port_scan_results,
            "sql_scan_results": sql_scan_results,
            "xss_scan_results": xss_scan_results,
            "rce_scan_results": rce_scan_results,
            "timestamp": datetime.datetime.now(datetime.timezone.utc)
        }
        db.collection("scans").add(scan_data)

    scan_thread = threading.Thread(target=run_scan, args=(url, current_user.id))
    scan_thread.start()

    flash('Scanning started!', 'success')
    return redirect(url_for('start_scanning'))

@app.route('/debug')
@login_required
def debug():
    return jsonify(dict(session))

if __name__ == '__main__':
    app.run(debug=True)
