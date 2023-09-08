from app.libraries.session.usersession import User
from flask import Flask ## import Flask dari package flask
from flask import session, redirect, url_for
import flask_login

app = Flask(__name__)

# Setup the app with config.py file
app.config.from_object('app.config')

# Setup the logger
from app.logger_setup import logger

# Set secret key
app.secret_key = app.config['SECRET_KEY']

# Import the controllers
from app.controllers import *

# TODO: add your blueprint page in here
app.register_blueprint(user.userbp)
app.register_blueprint(document.documentbp)
app.register_blueprint(submissions.submissionbp)
app.register_blueprint(client.clientbp)
app.register_blueprint(monitoring.monitoringbp)
app.register_blueprint(division.divisionbp)
app.register_blueprint(orange.orangebp)

# login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# TODO: authenticate the user session
@login_manager.user_loader
def user_loader(id):
    if 'usersession' in session:
        usersession = session['usersession']
    
    # authenticate the roles
    # redirect to unathorized if not passed

    return User(id)

@login_manager.request_loader
def request_loader(request):
    pass

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('userbp.signin'))
    # return redirect(f'''https://go.mpm-motor.com/approvalonline/user/signin''', code=302)