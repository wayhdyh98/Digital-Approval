from flask import (
    Blueprint,
    render_template, 
    g,
    request,
    session,
    redirect,
    url_for,
    flash
)
import flask_login

from app import app
from app.forms import user as user_forms
import json
from json import dumps

# database
from app.models.monitoring import Monitoring
from app.models.client import Client
from app.models.user import User

from app.libraries.session import usersession as USession

# Create a document blueprint
clientbp = Blueprint('clientbp', __name__, url_prefix='/client')


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        # find user based on userid, update information user
        user = session['user']
        g.user = user

        user = USession.User()
        # TODO: place your user / account data
        user.npk = g.user["npk"]
        user_data = User()
        person, message = user_data.profile(user.npk)

        if len(person) == 0:
            return render_template('handler/error.html', title='Error Page', message="Data user belum terdaftar di Approval Online")

        user.name = person['name']
        user.company = person['company']
        user.division = person['divisionid']
        user.department = person['departmentid']

        # save to session
        session["usersession"] = user.__dict__
        flask_login.login_user(user)



@clientbp.route('/api/1.0/clients')
@flask_login.login_required
def api_1_0_clients():
    # try to get list of client
    client = Client()
    result, message = client.list_client()
    return {
        "success": "0" if result == [] else "1",
        "message": message,
        "data": result
    }


@clientbp.route('/api/1.0/profile/<npk>')
@flask_login.login_required
def api_1_0_profile(npk):
    user = User()
    person, message = user.profile(npk)
    return {
        "success": "0" if person == None else "1",
        "message": message,
        "data": person
    }


@clientbp.route('/browse')
@flask_login.login_required
def browse():
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    return render_template('client/browse.html', title='Clients')