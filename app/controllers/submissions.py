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
    abort,
    jsonify
)
import flask_login

from app import app
from app.forms import user as user_forms
import json
import ast
import hashlib
import time
import os
from json import dumps
import datetime as dt
from app.libraries.util import parameterquery

# config
import app.config as conf

# database
from app.models.document import Document
from app.models.monitoring import Monitoring
from app.models.approvalonline_files import ApprovalOnlineFiles
from app.models.user import User
from app.models.security import Security
from app.models.submission import Submission
from app.models.requestapproval import RequestApproval
from app.models.requestapproval_answer import RequestApprovalAnswer
from app.models.requestapproval_authentication import RequestApprovalAuthentication

# libraries
from app.libraries.session import security as SecurityBase
from app.libraries.email import email as Email
from app.libraries.manipulationtext import StringUtil
from app.libraries.session import usersession as USession

# Create a document blueprint
submissionbp = Blueprint('submissionbp', __name__, url_prefix='/submission')


@app.before_request
def before_request():
    g.user = None
    if 'user' in session and 'usersession' in session:
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


@submissionbp.route('/api/1.0/submissions/<status>')
@flask_login.login_required
def api_1_0_submissions(status):
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    submission = Submission()
    # result, message = submission.submissions(session["usersession"]["npk"], status)
    result, message = submission.submissions(g.user["npk"], status)
    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }


@submissionbp.route('/api/1.0/submissions/getdocumentrequest/<divisionid>', methods=['GET'])
@flask_login.login_required
def api_1_0_getdocumentrequest(divisionid):
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    # get company id 
    # usersession = session["usersession"]
    usersession = g.user
    
    # try to get list of document
    document = Document()
    result, message = document.list_document_for_request(usersession["npk"], usersession["company"], divisionid)
    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }


@submissionbp.route('/api/1.0/submissions/fillformanswer/<requestapprovalid>', methods=['GET'])
@flask_login.login_required
def api_1_0_submissions_fillformanswer(requestapprovalid):
    requestapprovalanswer = RequestApprovalAnswer()
    result1, message1 = requestapprovalanswer.get_answer(requestapprovalid)
    result2, message2 = requestapprovalanswer.get_answerbase(requestapprovalid)

    answermultirow = []
    
    for x in result2:
        if x["questiontype"] == 1:
            data = {
                'requestapprovalid': requestapprovalid,
                'designdocumentquestionid': x["designdocumentquestionid"],
                'questioncondition': x["questioncondition"],
                'questiontypecomponent': x["questiontypecomponent"]
            }
            resultanswermultirow, messageanswermultirow = requestapprovalanswer.get_answer_multirow(data)
            answermultirow.append(resultanswermultirow)

    resultsinglegroup = [x for x in result1 if x["sectiontype"] == 0]
    resultmultigroup, messagemultigroup = requestapprovalanswer.get_answer_multigroup(requestapprovalid)

    arr2 = {}
    for d in resultmultigroup:
        arr2.setdefault(d['designdocumentgroupquestionid'], []).append(d)

    arr2 = list(arr2.values())
            
    return {
        "success": "0" if result1 == None or result2 == None else "1",
        "message": message1,
        "data": result1,
        "datamultirow": answermultirow,
        "datasinglegroup": resultsinglegroup,
        "datamultigroup": resultmultigroup,
        "arr2": arr2
    }  


@submissionbp.route('/api/1.0/submissions/authrequest/<requestapprovalid>', methods=['GET'])
@flask_login.login_required
def api_1_0_submissions_authrequest(requestapprovalid):
    requestapprovalauthentication = RequestApprovalAuthentication()
    result, message = requestapprovalauthentication.get_authdata(requestapprovalid)

    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }


@submissionbp.route('/api/1.0/submissions/filerequest/<requestapprovalid>', methods=['GET'])
@flask_login.login_required
def api_1_0_submissions_filerequest(requestapprovalid):
    approvalonlinefiles = ApprovalOnlineFiles()
    result, message = approvalonlinefiles.get_files(requestapprovalid)

    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    } 


@submissionbp.route('/request_approval', methods=['GET', 'POST'])
@flask_login.login_required
def request_approval():
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    if request.method == 'POST':
        # usersession = session["usersession"]
        usersession = g.user
        data = {
            "divisionid": request.form['select-division-id'],
            "documentid": request.form['select-document-type'],
            "[desc]": request.form['textarea-notes'],
            "name": request.form['select-document-text'],
            "activeversiondocument": int(request.form['select-designdocument-version']),
            "statusrequest": 0,
            "picrequester": usersession["npk"],
            "deleteflag": 0,
            "createdby": usersession["npk"],
            "createddate": dt.datetime.now(),
            "modifby": "",
            "modifdate": "",
        }
        requestapproval = RequestApproval()
        result, message = requestapproval.insert_data(data)

        if message == "success":
            return redirect(url_for('submissionbp.submissions_fillformrequest', requestapprovalid=result))

    return render_template('submission/request.html', title='Request')


@submissionbp.route('/request_fillform', methods=['POST'])
@flask_login.login_required
def request_fillform():
    questionid = ast.literal_eval(request.form['arrayquestionid'])

    # usersession = session["usersession"]
    usersession = g.user
    requestapprovalanswer = RequestApprovalAnswer()
    arraydata = []

    arraygroupid = ast.literal_eval(request.form['arraygroupid'])
    arraygroupid = [x["uuid"] for x in arraygroupid]

    multirow = False

    for x in questionid:
        if x["sectiontype"] == 0:
            if x["questiontype"] == 0:
                data = {
                    "designdocumentquestionid": x["questionid"],
                    "requestapprovalid": request.form['requestapprovalid'],
                    "answer": request.form[str(x["questionid"])],
                    "createdby": usersession["npk"],
                    "createddate": dt.datetime.now()
                }
                arraydata.append(data)
            else:
                arraymultirow = request.form.getlist(str(x["questionid"]))
                for y in arraymultirow:
                    data = {
                        "designdocumentquestionid": x["questionid"],
                        "requestapprovalid": request.form['requestapprovalid'],
                        "answer": y,
                        "createdby": usersession["npk"],
                        "createddate": dt.datetime.now()
                    }
                    arraydata.append(data)
        else:
            multirow = True

    if multirow:
        for x in arraygroupid:
            for y in questionid:
                try:
                    inputname = f"{x}-{y['questionid']}"
                    answer = request.form[str(inputname)]
                            
                    data = {
                        "designdocumentquestionid": y["questionid"],
                        "requestapprovalid": request.form['requestapprovalid'],
                        "answer": answer,
                        "createdby": usersession["npk"],
                        "createddate": dt.datetime.now(),
                        "answergroupid": x
                    }
                        
                    arraydata.append(data)
                except Exception as e:
                    pass

    result, message = requestapprovalanswer.insert_answer(arraydata, request.form['requestapprovalid'])

    return redirect(url_for('submissionbp.submissions_authorizationrequest', requestapprovalid=request.form['requestapprovalid']))


@submissionbp.route('/request_authorization', methods=['POST'])
@flask_login.login_required
def request_authorization():
    try:
        dataarray = json.loads(request.form['arraymasterapproveid'])
        # usersession = session["usersession"]
        usersession = g.user
        requestapprovalauth = RequestApprovalAuthentication()
        resultdel, messagedel = requestapprovalauth.delete_data(request.form["requestapprovalid"])

        securitymodel = Security()

        for x in dataarray:
            resultcheck, messagecheck = requestapprovalauth.check_auth(x["masterapproveid"], request.form["requestapprovalid"])

            if len(resultcheck) == 0:
                # convert to 00000 format npk
                npk = '0' * (5 - len(x["picid"])) + x["picid"]

                # do login-key part
                base_sckey = securitymodel.createbase_secretkey(dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
                result, message = securitymodel.check_loginkey(npk)

                private_key, public_key, secret_key = result['private_key'], result['public_key'], result['secret_key']

                # generate login-key
                securitybase = SecurityBase.SecurityKey()
                basekey = securitybase.generate_basekey()
                pk_key, pb_key = securitybase.generate_loginkey(basekey)

                datakey = {
                    "modifby": npk,
                    "modifdate": dt.datetime.now()
                }

                # check if key from db none, then insert it to dict
                if private_key is None:
                    private_key = pk_key
                    datakey["private_key"] = private_key

                if public_key is None:
                    public_key = pb_key
                    datakey["public_key"] = public_key
                    
                if secret_key is None:
                    secret_key = securitybase.generate_secretkey(public_key, base_sckey)
                    datakey["secret_key"] = secret_key

                if "private_key" in datakey or "public_key" in datakey or "secret_key" in datakey:
                    result2, message2 = securitymodel.insert_loginkey(datakey, npk)

                data = {
                    "requestapprovalid": request.form["requestapprovalid"],
                    "masterapproveid": x["masterapproveid"],
                    "pictype": x["pictype"],
                    "picid": str(x["picid"]).zfill(5),
                    "piclevel": x["piclevel"],
                    "picsublevel": x["picsublevel"],
                    "picname": x["picname"],
                    "mandatory": x["mandatory"],
                    "publickey": public_key,
                    "createdby": usersession["npk"],
                    "createddate": dt.datetime.now()
                }

                result3, message3 = requestapprovalauth.insert_auth(data)
            else:
                data = {
                    "picid": str(x["picid"]).zfill(5),
                    "picname": x["picname"],
                    "modifby": usersession["npk"],
                    "modifdate": dt.datetime.now()
                }
                result2, message2 = requestapprovalauth.update_auth(data, resultcheck[0]["requestapprovalauthenticationid"])

        return redirect(url_for('submissionbp.submissions_uploadfilerequest', requestapprovalid=request.form['requestapprovalid']))
    except Exception as e:
        print(e)
        return render_template('handler/error.html', title='Error Page', message=str(e))


@submissionbp.route('/api/1.0/submissions/request_authorization/insert', methods=['POST'])
@flask_login.login_required
def api_1_0_insert_request_authorization():
    # usersession = session["usersession"]
    usersession = g.user
    params = request.json
    requestapprovalauth = RequestApprovalAuthentication()
    securitymodel = Security()

    resultcheck, messagecheck = requestapprovalauth.check_auth(params["masterapproveid"], params["requestapprovalid"])

    if len(resultcheck) == 0:
        # convert to 00000 format npk
        npk = '0' * (5 - len(params["picid"])) + params["picid"]

        # do login-key part
        base_sckey = securitymodel.createbase_secretkey(dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        result, message = securitymodel.check_loginkey(npk)

        private_key, public_key, secret_key = result['private_key'], result['public_key'], result['secret_key']

        # generate login-key
        securitybase = SecurityBase.SecurityKey()
        basekey = securitybase.generate_basekey()
        pk_key, pb_key = securitybase.generate_loginkey(basekey)

        datakey = {
            "modifby": npk,
            "modifdate": dt.datetime.now()
        }

        # check if key from db none, then insert it to dict
        if private_key is None:
            private_key = pk_key
            datakey["private_key"] = private_key

        if public_key is None:
            public_key = pb_key
            datakey["public_key"] = public_key
            
        if secret_key is None:
            secret_key = securitybase.generate_secretkey(public_key, base_sckey)
            datakey["secret_key"] = secret_key

        if "private_key" in datakey or "public_key" in datakey or "secret_key" in datakey:
            result2, message2 = securitymodel.insert_loginkey(datakey, npk)

        data = {
            "requestapprovalid": params["requestapprovalid"],
            "masterapproveid": params["masterapproveid"],
            "pictype": params["pictype"],
            "picid": params["picid"],
            "piclevel": params["piclevel"],
            "picsublevel": params["picsublevel"],
            "picname": params["picname"],
            "mandatory": params["mandatory"],
            "publickey": public_key,
            "createdby": usersession["npk"],
            "createddate": dt.datetime.now()
        }

        result3, message3 = requestapprovalauth.insert_auth(data)

        return {
            "success": "0" if result3 == None else "1",
            "message": message3,
            "data": result3
        }

    return {
        "success": "0" if resultcheck == None else "1",
        "message": messagecheck,
        "data": resultcheck
    }


# upload file blueprint
@submissionbp.route('/api/1.0/submissions/request_uploadfile/upload', methods=['POST'])
@flask_login.login_required
def upload_file():
    approvalonlinefiles = ApprovalOnlineFiles()
    # usersession = session["usersession"]
    usersession = g.user
    uploaded_file = request.files['file']
    requestapprovalid = request.form['requestapprovalid']
    
    if uploaded_file.filename != '':
        filename = uploaded_file.filename.split('.')[0]
        extension_name = uploaded_file.filename.split('.')[1]

        # encode filename
        filename_encoded = hashlib.md5((filename + str(time.time())).encode())
        alias_filename = str(filename_encoded.hexdigest()) + "." + extension_name

        # size
        uploaded_file.seek(0)
        size = len(uploaded_file.read())

        # path
        # patharray = ["..\\files\\approvalonline\\", "..\\files\\sad\\"]
        # path = [os.path.join(submissionbp.root_path, x + requestapprovalid) for x in patharray]
        patharray = ["/files/approvalonline/", "/files/emailattachment/"]

        # check all folder
        filesdir = os.path.isdir(os.path.join(app.root_path, "../files"))
        if not filesdir:
            os.mkdir(os.path.join(app.root_path, "../files"))

        approvalfilesdir = os.path.isdir(os.path.join(app.root_path, "../files/approvalonline"))
        if not approvalfilesdir:
            os.mkdir(os.path.join(app.root_path, "../files/approvalonline"))

        emailfilesdir = os.path.isdir(os.path.join(app.root_path, "../files/emailattachment"))
        if not emailfilesdir:
            os.mkdir(os.path.join(app.root_path, "../files/emailattachment"))

        # existing directory or not
        # for x in path:
        #     isdir = os.path.isdir(x)
        #     if not isdir:
        #         os.mkdir(x)

        for x in patharray:
            isdir = os.path.isdir(os.path.join(app.root_path, "../" + x + requestapprovalid))
            if not isdir:
                os.mkdir(os.path.join(app.root_path, "../" + x + requestapprovalid))
        
        # save to folder
        # pathsave = [os.path.join(submissionbp.root_path, x + requestapprovalid + "\\" + alias_filename) for x in patharray]
        pathsave = [os.path.join(app.root_path, "../" + x + requestapprovalid + "/" + alias_filename) for x in patharray]

        for x in pathsave:
            uploaded_file.stream.seek(0)
            uploaded_file.save(x)
        
        # save to database
        data = {
            "filename": uploaded_file.filename,
            "aliasfilename": alias_filename,
            "size": size,
            "comments": "",
            "referenceid": requestapprovalid,
            "deleteflag": 0,
            "createdby": usersession["npk"],
            "createddate": dt.datetime.now()
        }
        result, row, message = approvalonlinefiles.insert_file(data)

        return {
                "success": "1" if result else "0",
                "result": row,
                "message": message
        }
    else:
        return {
                "success": "0",
                "message": "Incorrect file"
        }


# delete file blueprint
@submissionbp.route('/api/1.0/submissions/request_uploadfile/delete', methods=['POST'])
@flask_login.login_required
def delete_file():
    approvalonlinefiles = ApprovalOnlineFiles()
    # usersession = session["usersession"]
    usersession = g.user
    params = request.json

    data = {
        "deleteflag": 1,
        "modifby": usersession["npk"],
        "modifdate": dt.datetime.now()
    }

    result, message = approvalonlinefiles.delete_file(data, params["approvalonlinefileid"])

    return {
        "success": "1" if result else "0",
        "message": message
    }


# download file requirement
@submissionbp.route('/api/1.0/submissions/request_uploadfile/download/<approvalonlinefileid>', methods=['GET'])
@flask_login.login_required
def download_file(approvalonlinefileid):
    try:
        approvalonlinefiles = ApprovalOnlineFiles()
        result, message = approvalonlinefiles.readone(approvalonlinefileid)
        
        # uploads = os.path.join(submissionbp.root_path, "..\\files\\approvalonline\\" + result['referenceid'] + "\\" + result['aliasfilename'])
        uploads = os.path.join(app.root_path, "../files/approvalonline/" + result['referenceid'] + "/" + result['aliasfilename'])
        return send_file(uploads, as_attachment=True, attachment_filename=result["filename"])
    except FileNotFoundError:
        abort(404)


@submissionbp.route('/api/1.0/submissions/ttd_preview', methods=['POST'])
@flask_login.login_required
def ttd_preview():
    params = request.json
    layoutdocument = StringUtil.replacesignature(params['layoutdocument'], params['piclevel'], params['picsublevel'])
    
    return {
        "success": "1",
        "result": layoutdocument
    }


@submissionbp.route('/api/1.0/submissions/requestapproval/update', methods=['POST'])
@flask_login.login_required
def request_approval_update():
    try:
        requestapproval = RequestApproval()
        # usersession = session["usersession"]
        usersession = g.user
        params = request.json

        data = {
            "layoutdocument": params['layoutdocument'],
            "statusrequest": 1,
            "modifby": usersession["npk"],
            "modifdate": dt.datetime.now()
        }

        requestapprovalauthentication = RequestApprovalAuthentication()
        monitoring = Monitoring()
        resultdocument, messagedocument = monitoring.viewtracking(params["requestapprovalid"], 0)
        resultworkflow, messageworkflow = monitoring.viewtracking(params["requestapprovalid"], 2)

        getpemohon = [x for x in resultworkflow if x["piclevel"] == 1 and x["picsublevel"] == 1]
        # test = [{'piclevel':1,'picsublevel':1},{'piclevel':2,'picsublevel':1},{'piclevel':2,'picsublevel':2}]

        # Chek file
        approvalonlinefiles = ApprovalOnlineFiles()
        resultfile, messagefile = approvalonlinefiles.get_files(params["requestapprovalid"])

        filecheck = []
        if len(resultfile) > 0:
            # filecheck = [{"pathname":os.path.join(submissionbp.root_path, "..\\files\\emailattachment\\" + x['referenceid'] + "\\" + x['aliasfilename']), "filename":x['filename']} for x in resultfile]
            filecheck = [{"pathname":os.path.join(app.root_path, "../files/emailattachment/" + x['referenceid'] + "/" + x['aliasfilename']), "filename":x['filename']} for x in resultfile]

        # Update Status Request Approval
        result, message = requestapproval.update_requestapproval(data, params["requestapprovalid"])

        tablehtml = params["workflowtable"]

        # Check if Pemohon is same with login user
        time.sleep(2)
        if params["cond"]:
            layoutdocument = StringUtil.replacesignature(params['layoutdocument'], 1, 1)
            data["layoutdocument"] = layoutdocument

            # Update Layout with User Signature
            result, message = requestapproval.update_requestapproval(data, params["requestapprovalid"])

            data.pop("layoutdocument", None)
            data["commentapprove"] = "Approved by System"
            data["statusapprove"] = data.pop("statusrequest")
            
            # Update User statusapprove
            resultapprove, messageapprove = requestapprovalauthentication.update_statusapprove(data, getpemohon[0]["requestapprovalauthenticationid"])

            # Change text and color status on table html
            tablehtml = tablehtml.replace('Pending', 'Approved', 1)
            tablehtml = tablehtml.replace('#ffc107', '#28a745', 1)

        checkpemohonsublevel = []

        # emailto = "".join((x["email"]+",") for x in resultworkflow if x["piclevel"] == 1 or x["piclevel"] == 2)
        emailto = [x for x in resultworkflow if x["piclevel"] == 1 or x["piclevel"] == 2]

        email_path = conf.EMAIL_PATH

        # http://10.10.101.217:7003/monitoring/api/1.0/page/monitoringbp.api_1_0_viewtracking_linksession/%s/%s
        # http://localhost:5000/monitoring/api/1.0/page/monitoringbp.api_1_0_viewtracking_linksession/%s/%s

        for sent in emailto:
            encryptpicid = parameterquery.encrypt_parameter_query(sent["picid"])
            emailbody = f'''<font>Salam Satu Hati,</font><br> Dokumen: {resultdocument["requestid"]} - {resultdocument["name"]}, telah terkirim!<br> 
            Keterangan: {resultdocument["desc"]}<br>Pemohon: {getpemohon[0]["picname"]} - {getpemohon[0]["divisi"]}<br>------------<br>
            <a href="{email_path}/{encryptpicid.decode('utf-8')}/{params["requestapprovalid"]}/{params["years"]}">Click here to <b>track</b> approval detail</a><br>------------<br>
            Approved By : <br> {tablehtml} </div><br>Terimakasih.'''

            # emailbody += f'''#### Buat testing alamat email asli yang dikirim:<br>
            # Email: {sent["email"]},<br>
            # Piclevel: {sent["piclevel"]},<br>
            # '''

            emailsubject = "[NO-REPLY]CONFIRMATION REQUEST APPROVAL"

            # result, message = Email.send_email(emailto, "", emailsubject, emailbody, filecheck)
            result, message = Email.send_email(sent["email"], "", emailsubject, emailbody, filecheck)
            # result, message = Email.send_email("anandagalang1@gmail.com", "", emailsubject, emailbody, filecheck)

        return {
            "success": "1" if result else "0",
            "message": message
        }
    except Exception as e:
        print(e)
        return render_template('handler/error.html', title='Error Page', message=str(e))


@submissionbp.route('/api/1.0/submissions/requestapproval/cancel', methods=['POST'])
@flask_login.login_required
def request_approval_cancel():
    # Update Status Request Approval
    requestapproval = RequestApproval()
    # usersession = session["usersession"]
    usersession = g.user
    params = request.json
    data = {
        "statusrequest": 2,
        "modifby": usersession["npk"],
        "modifdate": dt.datetime.now()
    }

    result, message = requestapproval.update_requestapproval(data, params["requestapprovalid"])

    return {
        "success": "1" if result else "0",
        "message": message
    }


@submissionbp.route('/submissions')
@flask_login.login_required
def submissions():
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    return render_template('submission/submissions.html', title='Submissions')


@submissionbp.route('/submissions/fillformrequest/<requestapprovalid>')
@flask_login.login_required
def submissions_fillformrequest(requestapprovalid):
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    requestapproval = RequestApproval()
    result, message = requestapproval.select_request(requestapprovalid)
    return render_template('submission/fillformrequest.html', title='Submissions - Fill Form Request', request=result)


@submissionbp.route('/submissions/authorizationrequest/<requestapprovalid>')
@flask_login.login_required
def submissions_authorizationrequest(requestapprovalid):
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    requestapproval = RequestApproval()
    result, message = requestapproval.select_request(requestapprovalid)
    return render_template('submission/authorizationrequest.html', title='Submissions - Authorization Request', request=result)


@submissionbp.route('/submissions/uploadfilerequest/<requestapprovalid>')
@flask_login.login_required
def submissions_uploadfilerequest(requestapprovalid):
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    requestapproval = RequestApproval()
    result, message = requestapproval.select_request(requestapprovalid)
    return render_template('submission/uploadfilerequest.html', title='Submissions - Upload File Request', request=result)


@submissionbp.route('/submissions/postingrequest/<requestapprovalid>')
@flask_login.login_required
def submissions_postingrequest(requestapprovalid):
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    monitoring = Monitoring()
    result, message = monitoring.viewtracking(requestapprovalid, 0)
    return render_template('submission/postingrequest.html', title='Submissions - Post Request', request=result, usersession=g.user)