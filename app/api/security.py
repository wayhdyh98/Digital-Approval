import app.config as conf
import datetime as dt
import json

# import requests
# from bs4 import BeautifulSoup
# from flask import jsonify

from flask import (
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
from app.api import orange as Orange
from app.libraries.session import usersession as USession
from app.libraries.session import security as SecurityBase
from app.libraries.util import parameterquery
from app.models.security import Security

from app.models.user import User

# from PIL import Image
# from io import BytesIO

@app.route('/api/security/generate_qrcode/<userid>/<password>', methods=['GET'])
def generate_qrcode(userid, password):
    apiOrange = Orange.OrangeAPI()
    isValid = apiOrange.user_validation(userid, password)

    if isValid:
        # check login-key
        securitymodel = Security()
        base_sckey = securitymodel.createbase_secretkey(dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        result, message = securitymodel.check_loginkey(userid)

        # set private, public, & secret key
        private_key, public_key, secret_key = result['private_key'], result['public_key'], result['secret_key']

        # generate login-key
        securitybase = SecurityBase.SecurityKey()
        basekey = securitybase.generate_basekey()
        pk_key, pb_key = securitybase.generate_loginkey(basekey)

        # set data
        data = {
            "modifby": userid,
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
            result2, message2 = securitymodel.insert_loginkey(data, userid)

        hashed_seckey = securitybase.encrypt_md5(secret_key)
        url = conf.QRCODE_API_ENDPOINT + hashed_seckey

        # response = requests.get(url)
        # soup = BeautifulSoup(response.content, "xml")
        # sad = ''
        # for img in soup.findAll('img'):
        #     sad = img
        # img = Image.open(response)
        # img = Image.open(BytesIO(response.content))

        return {
            "success": "1",
            "result": url,
            "message": "success"
        }
        # return send_file(img, mimetype='image/jpeg')

    return {
        "success": "0",
        "result": isValid,
        "message": "failed"
    }

@app.route('/api/security/validation_hashcode', methods=['POST'])
def validation_hashcode():
    securitymodel = Security()
    securitybase = SecurityBase.SecurityKey()
    params = request.json

    result, message = securitymodel.check_loginkey(params["userid"])
    hashed_seckey = securitybase.encrypt_md5(result["secret_key"])

    if params["code"] == hashed_seckey:
        return {
            "success": "1",
            "result": True,
            "message": "success"
        }

    return {
        "success": "0",
        "result": False,
        "message": "failed"
    }


@app.route('/dashboard')
def dashboard():
    return redirect(url_for('home'))


@app.route('/api/directlogin', methods=['POST'])
def do_login():
    try:
        # if already login, redirect to home
        if 'usersession' in session and session["usersession"] is not None:
            return redirect(url_for('home'))
        
        jsonparams = request.json

        params = parameterquery.decrypt_parameter_query(jsonparams['q'])

        # check login-key
        securitymodel = Security()
        base_sckey = securitymodel.createbase_secretkey(dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        result, message = securitymodel.check_loginkey(params)

        # set private, public, & secret key
        private_key, public_key, secret_key = result['private_key'], result['public_key'], result['secret_key']

        # generate login-key
        securitybase = SecurityBase.SecurityKey()
        basekey = securitybase.generate_basekey()
        pk_key, pb_key = securitybase.generate_loginkey(basekey)

        # set data
        data = {
            "modifby": params,
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
            result2, message2 = securitymodel.insert_loginkey(data, params)

        # process the login manager session
        user = USession.User()
        # TODO: place your user / account data
        user.npk = params
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
            # return redirect(url_for(url, requestapprovalid=session['urlpage']["requestapprovalid"], period=session['urlpage']["period"]))
            return redirect(f'''https://go.mpm-motor.com/approvalonline/monitoring/viewtracking/linksession/{session['urlpage']["requestapprovalid"]}/{session['urlpage']["period"]}''', code=302)
        else:
            return redirect(url_for('home'), code=302)

    except Exception as e:
        return render_template('handler/error.html', title='Error Page', message=str(e))
            