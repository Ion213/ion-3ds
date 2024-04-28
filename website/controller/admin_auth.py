#libraries needed
from flask import (
    Blueprint, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash
)
from flask_login import (
                        LoginManager,
                         login_user,
                         logout_user,
                         login_required,
                         current_user
                         )
import pyrebase

#your firebase config
config = {
    "apiKey": "AIzaSyBTpIhaojpQ9eakMj-nJ_jfKYYJaTV9MTg",
    "authDomain": "ds-web-fca30.firebaseapp.com",
    "databaseURL": "",  # Not needed for Pyrebase
    "projectId": "ds-web-fca30",
    "storageBucket": "ds-web-fca30.appspot.com",
    "messagingSenderId": "201056273751",
    "appId": "1:201056273751:web:0ff380f1324bb3649b6a12",
    "measurementId": "G-P7HPKTMH24"
}
#initialize the config
firebase = pyrebase.initialize_app(config)
#create a variable to the initialized config
auth = firebase.auth()

#create blueprint/routes
admin_auth = Blueprint('admin_auth', __name__)

@admin_auth.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user= auth.sign_in_with_email_and_password(email, password)
            session_id = user['localId']
            from website.sessions.session_storage import User
            login_user(User(session_id))
            flash('Log in successfully!', category='login_success')
            return redirect(url_for('admin_views.add_games'))
        except Exception as e:
            flash('Invalid Admin Credential please contact the admin or developer to get access', category='login_error')
            
    return render_template('admin_login.html')

#admin logout route
@admin_auth.route('/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_auth.admin_login'))