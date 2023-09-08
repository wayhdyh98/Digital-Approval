from flask import (
    render_template, 
    g,
    request,
    session,
    redirect,
    url_for
)
import flask_login
from app import app
from app.api import security 

from app.models.user import User

from app.models.dashboards import Dashboards
from app.libraries.session import usersession as USession

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


@app.route('/', methods = ['GET'])
@app.route("/index")
def index():
    return render_template('index.html', title="Approval Online")


@app.route('/home', methods = ['GET'])
@flask_login.login_required
def home():
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    # usersession = session["usersession"]
    dashboard = Dashboards()

    # Total Dashboards
    result, message = dashboard.total_dashboards(g.user["npk"])
    
    return render_template('home.html', title="Approval Online", request=result)