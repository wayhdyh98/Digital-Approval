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

from app.libraries.session import usersession as USession

# database
from app.models.orange import OrangeData
from app.models.user import User

# Create a document blueprint
orangebp = Blueprint('orangebp', __name__, url_prefix='/orange')

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


@orangebp.route('/api/1.0/picapprovals/<divisionid>')
@flask_login.login_required
def api_1_0_picapprovals(divisionid):
    usersession = session["usersession"]
    companyid = usersession["company"]

    orange = OrangeData()
    result, message = orange.list_pic(companyid, divisionid)
    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }