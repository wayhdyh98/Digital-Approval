from flask import (
    Blueprint,
    render_template, 
    g,
    request,
    session,
    redirect,
    url_for,
    flash,
    send_file,
    send_from_directory,
    abort
)
import flask_login

from app import app
from app.forms import user as user_forms
import json
from json import dumps
import datetime as dt
import os
from xml.sax.saxutils import escape

from app.libraries.session import usersession as USession
from app.libraries.session import security as SecurityBase
from app.api import orange as Orange 

# database
from app.models.user import User
from app.models.security import Security

# Create a user blueprint
userbp = Blueprint('userbp', __name__, url_prefix='/user')


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


@userbp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = user_forms.SignUp(request.form)

    # form submit
    if request.method == 'POST' and form.validate():
        return redirect(url_for('index'))

    return render_template('user/signup.html', form=form, title='Sign Up')


@userbp.route('/signin', methods=['GET', 'POST'])
def signin():
    # if already login, redirect to home
    if 'usersession' in session and session["usersession"] is not None:
        return redirect(url_for('home'))

    form = user_forms.SignIn(request.form)

    # initialize sample input
    if request.method=="GET":
        form.userid.data = "05660"

    # form submit
    if request.method=="POST" and form.validate():
        apiOrange = Orange.OrangeAPI()
        password = escape(form.password.data)
        isValid = apiOrange.user_validation(form.userid.data, password)
        
        ## pass without API for development
        # process the login manager session
        user = USession.User()
        # TODO: place your user / account data
        user.npk = str(form.userid.data).zfill(5)
        user_data = User()
        person, message = user_data.profile(user.npk)

        if len(person) == 0:
            flash('Account is not found.', 'negative')
            return redirect(url_for('userbp.signin'))

        user.name = person['name']
        user.company = person['company']
        user.division = person['divisionid']
        user.department = person['departmentid']

        # save to session
        session["usersession"] = user.__dict__
        flask_login.login_user(user)
        if 'urlpage' in session and session['urlpage'] is not None:
            url = session['urlpage']["url"]
            return redirect(url_for(url, requestapprovalid=session['urlpage']["requestapprovalid"], period=session['urlpage']["period"]))
            # return redirect(f'''https://go.mpm-motor.com/approvalonline/monitoring/viewtracking/linksession/{session['urlpage']["requestapprovalid"]}/{session['urlpage']["period"]}''', code=302)
        else:
            return redirect(url_for('home'))

        # if isValid:
        #     # check login-key
        #     securitymodel = Security()
        #     base_sckey = securitymodel.createbase_secretkey(dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        #     result, message = securitymodel.check_loginkey(form.userid.data)

        #     # set private, public, & secret key
        #     private_key, public_key, secret_key = result['private_key'], result['public_key'], result['secret_key']

        #     # generate login-key
        #     securitybase = SecurityBase.SecurityKey()
        #     basekey = securitybase.generate_basekey()
        #     pk_key, pb_key = securitybase.generate_loginkey(basekey)

        #     # set data
        #     data = {
        #         "modifby": form.userid.data,
        #         "modifdate": dt.datetime.now()
        #     }

        #     # check if key from db none, then insert it to dict
        #     if private_key is None:
        #         private_key = pk_key
        #         data["private_key"] = private_key

        #     if public_key is None:
        #         public_key = pb_key
        #         data["public_key"] = public_key
                
        #     if secret_key is None:
        #         secret_key = securitybase.generate_secretkey(public_key, base_sckey)
        #         data["secret_key"] = secret_key

        #     # insert login-key to db
        #     if "private_key" in data or "public_key" in data or "secret_key" in data:
        #         result2, message2 = securitymodel.insert_loginkey(data, form.userid.data)

        #     # process the login manager session
        #     user = USession.User()
        #     # TODO: place your user / account data
        #     user.npk = form.userid.data
        #     user_data = User()
        #     person, message = user_data.profile(user.npk)
            
        #     if len(person) == 0:
        #         flash('Account is not found.', 'negative')
        #         return redirect(url_for('userbp.signin'))

        #     user.name = person['name']
        #     user.company = person['company']
        #     user.division = person['divisionid']
        #     user.department = person['departmentid']

        #     # save to session
        #     session["usersession"] = user.__dict__
        #     flask_login.login_user(user)
        #     if 'urlpage' in session and session['urlpage'] is not None:
        #         url = session['urlpage']["url"]
        #         # return redirect(url_for(url, requestapprovalid=session['urlpage']["requestapprovalid"], period=session['urlpage']["period"]))
        #         return redirect(f'''https://go.mpm-motor.com/approvalonline/monitoring/viewtracking/linksession/{session['urlpage']["requestapprovalid"]}/{session['urlpage']["period"]}''', code=302)
        #     else:
        #         return redirect(url_for('home'))
        # else:
        #     flash('Invalid account.', 'negative')
        #     return redirect(url_for('userbp.signin'))

    return render_template('user/signin.html', form=form, title='Sign In')


@userbp.route('/api/1.0/profile/upload', methods=['POST'])
@flask_login.login_required
def insert_ttd():
    user_data = User()
    params = request.json
    
    data = {
        "ttd": params['file'],
        # "modifby": session["usersession"]["npk"],
        "modifby": g.user["npk"],
        "modifdate": dt.datetime.now()
    }
    # result, message = user_data.insert_ttd(data, session["usersession"]["npk"])
    result, message = user_data.insert_ttd(data, g.user["npk"])

    return {
        "success": "1" if result else "0",
        "result": result,
        "message": message
    }


# @userbp.route('/signout')
# @flask_login.login_required
# def signout():
#     flask_login.logout_user()
#     session["usersession"] = None
#     flash('Succesfully signed out.', 'positive')
#     return redirect(url_for('index'))


@userbp.route('/signout')
def signout():
    if "user" in session:
        session.pop("user")
    g.user = None
    flash('Succesfully signed out.', 'positive')
    return redirect('https://10.10.108.44/login')


@userbp.route('/profile')
@flask_login.login_required
def profile():
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    # usersession = session["usersession"]
    usersession = g.user

    user = User()
    person, message = user.profile(usersession["npk"])

    # check login-key
    securitymodel = Security()
    securitybase = SecurityBase.SecurityKey()

    result, message = securitymodel.check_loginkey(usersession["npk"])
    
    base_sckey = securitymodel.createbase_secretkey(dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    # set private, public, & secret key
    private_key, public_key, secret_key = result['private_key'], result['public_key'], result['secret_key']

    # generate login-key
    securitybase = SecurityBase.SecurityKey()
    basekey = securitybase.generate_basekey()
    pk_key, pb_key = securitybase.generate_loginkey(basekey)

    # set data
    data = {
        "modifby": usersession["npk"],
        "modifdate": dt.datetime.now()
    }

    # check if key from db none, then insert it to dict
    if private_key is None:
        private_key = pk_key
        data["private_key"] = private_key

    if public_key is None:
        public_key = pb_key
        data["public_key"] = public_key
        
    if secret_key is None:
        secret_key = securitybase.generate_secretkey(public_key, base_sckey)
        data["secret_key"] = secret_key

    # insert login-key to db
    if "private_key" in data or "public_key" in data or "secret_key" in data:
        result2, message2 = securitymodel.insert_loginkey(data, usersession["npk"])

    hashed_seckey = securitybase.encrypt_md5_profile(secret_key)

    return render_template('user/profile.html', 
        title='Profile',
        person=person,
        key=hashed_seckey)


@userbp.route('/manual')
@flask_login.login_required
def manual():
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    # usersession = session["usersession"]
    return render_template('user/manual.html', 
        title='User Manual')


# download file manual
@userbp.route('/api/1.0/profile/manual/download/<path:params>', methods=['GET'])
@flask_login.login_required
def api_documentfile(params):
    try:
        uploads = os.path.join('./files/help/')
        return send_from_directory(directory=uploads, path=params, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@userbp.route('/browse')
@flask_login.login_required
def browse():
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    return render_template('user/browse.html', title='Users')