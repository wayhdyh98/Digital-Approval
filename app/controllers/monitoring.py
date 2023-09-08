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
import datetime as dt
import os

# config
import app.config as conf

from app.libraries.email import email as Email
from app.libraries.manipulationtext import StringUtil
from app.libraries.util import parameterquery
from app.libraries.session import usersession as USession

# database
from app.models.user import User
from app.models.requestapproval import RequestApproval
from app.models.monitoring import Monitoring
from app.models.approvalonline_files import ApprovalOnlineFiles
from app.models.requestapproval_authentication import RequestApprovalAuthentication
from app.models.masterdocument_designdocument import MasterDocumentDesignDocument

# Create a document blueprint
monitoringbp = Blueprint('monitoringbp', __name__, url_prefix='/monitoring')


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


@monitoringbp.route('/api/1.0/documents/<period>/<status>')
@flask_login.login_required
def api_1_0_documents(period, status):
    # try to get list of document
    monitoring = Monitoring()
    # result, message = monitoring.document(session["usersession"]["npk"], period, status)
    result, message = monitoring.document(g.user["npk"], period, status)
    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }


@monitoringbp.route('/api/1.0/trackingworkflow/<period>/<status>')
@flask_login.login_required
def api_1_0_trackingworkflow(period, status):
    monitoring = Monitoring()
    # result, message = monitoring.trackingworkflow(session["usersession"]["npk"], period, status)
    # resultheader, messageheader = monitoring.trackingworkflow_header(session["usersession"]["npk"], period, status)
    result, message = monitoring.trackingworkflow(g.user["npk"], period, status)
    resultheader, messageheader = monitoring.trackingworkflow_header(g.user["npk"], period, status)
    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result,
        "dataheader": resultheader
    }


@monitoringbp.route('/api/1.0/viewtracking/designdocument', methods=['POST'])
@flask_login.login_required
def api_1_0_viewtracking_designdocument():
    params = request.json
    masterdocument_designdocument = MasterDocumentDesignDocument()
    result, message = masterdocument_designdocument.list_designdocument(params["documentid"])
    try:
        result = [x for x in result if x["version"] == int(params["activeversion"])]
    except Exception as e:
        pass

    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }


@monitoringbp.route('/api/1.0/viewtracking/bodypart/<requestapprovalid>', methods=['GET'])
@flask_login.login_required
def api_1_0_viewtracking_bodypart(requestapprovalid):
    sidedata = {
        # "npkuser": session["usersession"]["npk"],
        "npkuser": g.user["npk"],
        "piclevel": session["pictracking"]["piclevel"] if "pictracking" in session else "",
        "picsublevel": session["pictracking"]["picsublevel"] if "pictracking" in session else "",
        "requestapprovalauthenticationid": session["pictracking"]["requestapprovalauthenticationid"] if "pictracking" in session else ""
    }
    buttonkey = False
    pic = ""

    monitoring = Monitoring()
    result, message = monitoring.viewtracking(requestapprovalid, 1)
    result2, message2 = monitoring.viewtracking(requestapprovalid, 2)

    if "pictracking" in session:
        # Is There This User in This Auth RequestApproval
        levelcheck = [x for x in result2 if x["piclevel"] <= sidedata["piclevel"] and any(d['picid'] == sidedata["npkuser"] for d in result2)]
        if len(levelcheck) > 0:
            # Check if There is no 'Rejected' Status
            if not any(d['statusapprove'] == 2 for d in levelcheck):
                # Check if Pemohon is not Approved because need security
                levelonecheck = [x for x in levelcheck if x["piclevel"] == 1 and x["statusapprove"] == 0 and x["picid"] == sidedata["npkuser"]]
                if len(levelonecheck) > 0:
                    buttonkey = True
                else:
                    # Check if Before this User, is There Level below This User Level
                    downlevelcheck = [x for x in levelcheck if x["piclevel"] == (sidedata["piclevel"]-1)]
                    if len(downlevelcheck) > 0:
                        # Check if Before this User, is There 'Approved' Action
                        if any(d['statusapprove'] == 1 for d in downlevelcheck):
                            samelevelcheck = [x for x in levelcheck if x["piclevel"] == sidedata["piclevel"]]
                            # Check if There is Multi Level
                            if len(samelevelcheck) > 0:
                                # # Check if There is no 'Approved' Status between Same Level
                                if not any(d['statusapprove'] == 1 for d in samelevelcheck):
                                    buttonkey = True
                                    pic = [x for x in samelevelcheck if x['picid'] == sidedata["npkuser"]]
                            else:
                                buttonkey = True


    return {
        "success": "0" if result == None or result2 == None else "1",
        "message": message,
        "message2": message2,
        "data": result,
        "data2": result2,
        "datapic": pic,
        "key": buttonkey,
        "sidedata": sidedata
    }

@monitoringbp.route('/api/2.0/viewtracking/bodypart/<npk>/<requestapprovalid>', methods=['GET'])
def email_viewtracking_bodypart(npk, requestapprovalid):
    sidedata = {
        "npkuser": npk,
        "piclevel": session["pictracking"]["piclevel"] if "pictracking" in session else "",
        "picsublevel": session["pictracking"]["picsublevel"] if "pictracking" in session else "",
        "requestapprovalauthenticationid": session["pictracking"]["requestapprovalauthenticationid"] if "pictracking" in session else ""
    }
    buttonkey = False
    pic = ""

    monitoring = Monitoring()
    result, message = monitoring.viewtracking(requestapprovalid, 1)
    result2, message2 = monitoring.viewtracking(requestapprovalid, 2)

    if "pictracking" in session:
        # Is There This User in This Auth RequestApproval
        levelcheck = [x for x in result2 if x["piclevel"] <= sidedata["piclevel"] and any(d['picid'] == sidedata["npkuser"] for d in result2)]
        if len(levelcheck) > 0:
            # Check if There is no 'Rejected' Status
            if not any(d['statusapprove'] == 2 for d in levelcheck):
                # Check if Pemohon is not Approved because need security
                levelonecheck = [x for x in levelcheck if x["piclevel"] == 1 and x["statusapprove"] == 0 and x["picid"] == sidedata["npkuser"]]
                if len(levelonecheck) > 0:
                    buttonkey = True
                else:
                    # Check if Before this User, is There Level below This User Level
                    downlevelcheck = [x for x in levelcheck if x["piclevel"] == (sidedata["piclevel"]-1)]
                    if len(downlevelcheck) > 0:
                        # Check if Before this User, is There 'Approved' Action
                        if any(d['statusapprove'] == 1 for d in downlevelcheck):
                            samelevelcheck = [x for x in levelcheck if x["piclevel"] == sidedata["piclevel"]]
                            # Check if There is Multi Level
                            if len(samelevelcheck) > 0:
                                # # Check if There is no 'Approved' Status between Same Level
                                if not any(d['statusapprove'] == 1 for d in samelevelcheck):
                                    buttonkey = True
                                    pic = [x for x in samelevelcheck if x['picid'] == sidedata["npkuser"]]
                            else:
                                buttonkey = True


    return {
        "success": "0" if result == None or result2 == None else "1",
        "message": message,
        "message2": message2,
        "data": result,
        "data2": result2,
        "datapic": pic,
        "key": buttonkey,
        "sidedata": sidedata
    }


# For checking if the replacement is success or not, popol
@monitoringbp.route('/api/1.0/viewtracking/ttd_preview', methods=['POST'])
@flask_login.login_required
def ttd_preview():
    params = request.json
    layoutdocument = StringUtil.previewSignature(params['layoutdocument'], params['requestapprovalid'], params['masterdocid'])
    
    return {
        "success": "1",
        "result": layoutdocument
    }


@monitoringbp.route('/api/1.0/viewtracking/approveaction', methods=['POST'])
@flask_login.login_required
def api_1_0_viewtracking_approveaction():
    requestapprovalauthentication = RequestApprovalAuthentication()
    # usersession = session["usersession"]
    usersession = g.user
    params = request.json
    data = {
        "statusapprove": params["statusapprove"],
        "commentapprove": params["commentapprove"],
        "modifby": usersession["npk"],
        "modifdate": dt.datetime.now()
    }

    # Chek file
    approvalonlinefiles = ApprovalOnlineFiles()
    resultfile, messagefile = approvalonlinefiles.get_files(params["requestapprovalid"])

    filecheck = []
    if len(resultfile) > 0:
        filecheck = [{"pathname":os.path.join(monitoringbp.root_path, "..\\files\\emailattachment\\" + x['referenceid'] + "\\" + x['aliasfilename']), "filename":x['filename']} for x in resultfile]
        # filecheck = [{"pathname":os.path.join(app.root_path, "../files/emailattachment/" + x['referenceid'] + "/" + x['aliasfilename']), "filename":x['filename']} for x in resultfile]

    # Update Status Approve
    resultapprove, messageapprove = requestapprovalauthentication.update_statusapprove(data, params["requestapprovalauthenticationid"])

    # Set Period & Status
    period = session["pictracking"]["period"]

    # Get data for Email Part
    monitoring = Monitoring()
    resultdocument, messagedocument = monitoring.viewtracking(params["requestapprovalid"], 0)
    resultworkflow, messageworkflow = monitoring.viewtracking(params["requestapprovalid"], 2)

    getpemohon = [x for x in resultworkflow if x["piclevel"] == 1 and x["picsublevel"] == 1]
    getcurrentapprover = [x for x in resultworkflow if x["picid"] == usersession["npk"]]

    getmaxlevel = max(resultworkflow, key=lambda x:x['piclevel'])
    getlastperson = [x for x in resultworkflow if x["piclevel"] == getmaxlevel["piclevel"]]

    # Get email for sending To:
    # emailto = "".join((x["email"]+",") for x in resultworkflow if x["piclevel"] > int(params["piclevel"]))
    # emailto = "".join((x["email"]+",") for x in resultworkflow if x["piclevel"] == (int(params["piclevel"]) + 1))
    emailto = [x for x in resultworkflow if x["piclevel"] == (int(params["piclevel"]) + 1)]

    # Replace Approver Status on Table Html
    tablehtml = StringUtil.findandreplace(params["workflowtable"], 'Pending', params["textstatus"], params["picsublevel"])
    tablehtml = StringUtil.findandreplace(tablehtml, '#ffc107', params["colorstatus"], params["picsublevel"])

    if params["statusapprove"] == 1:
        # Replace the signature
        layoutdocument = StringUtil.replacesignature(params['layoutdocument'], session['pictracking']['piclevel'], session['pictracking']['picsublevel'], params["masterdocid"])

        data.pop("statusapprove", None)
        data.pop("commentapprove", None)
        data["layoutdocument"] = layoutdocument

        # Update Layout on RequestApproval
        requestapproval = RequestApproval()
        resultupdatelayout, messageupdatelayout = requestapproval.update_requestapproval(data, params["requestapprovalid"])

        # toDo perlu ditanyakan lagi
        # Chek if user is last person or not
        iflastperson = [x for x in getlastperson if x["picid"] == usersession["npk"]]

        if len(iflastperson) > 0:
            # emailto = "".join((x["email"]+",") for x in resultworkflow)
            emailto = [x for x in resultworkflow]
    else:
        # emailto = f'{getpemohon[0]["email"]},{getcurrentapprover[0]["email"]}'
        emailto = [{"email": getpemohon[0]["email"], "picid": getpemohon[0]["picid"]}, {"email": getcurrentapprover[0]["email"], "picid": getcurrentapprover[0]["picid"]}]
    
    email_path = conf.EMAIL_PATH

    for sent in emailto:
        emailbody = f'''<font>Salam Satu Hati,</font><br> Dokumen: {resultdocument["requestid"]} - {resultdocument["name"]}, telah terkirim!<br> 
        Keterangan: {resultdocument["desc"]}<br>Pemohon: {getpemohon[0]["picname"]} - {getpemohon[0]["divisi"]}<br>------------<br>
        <a href="{email_path}/{sent["picid"]}/{params["requestapprovalid"]}/{period}">Click here to <b>track</b> approval detail</a><br>------------<br>
        Approved By : <br> {tablehtml} </div><br>Terimakasih.'''

        emailsubject = "[NO-REPLY]CONFIRMATION REQUEST APPROVAL"

        result, message = True, "Success"
        if emailto != "":
            # result, message = Email.send_email("wahyuhidayah.4haha@gmail.com", "", emailsubject, emailbody, filecheck)
            result, message = Email.send_email(sent["email"], "", emailsubject, emailbody, filecheck)

            return {
                "success": "1" if result else "0",
                "message": message
            }
    return {
        "success": "1" if resultapprove else "0",
        "message": messageapprove
    }


@monitoringbp.route('/api/2.0/viewtracking/approveaction', methods=['POST'])
def email_viewtracking_approveaction():
    requestapprovalauthentication = RequestApprovalAuthentication()
    params = request.json
    data = {
        "statusapprove": params["statusapprove"],
        "commentapprove": params["commentapprove"],
        "modifby": params["picid"],
        "modifdate": dt.datetime.now()
    }

    # Chek file
    approvalonlinefiles = ApprovalOnlineFiles()
    resultfile, messagefile = approvalonlinefiles.get_files(params["requestapprovalid"])

    filecheck = []
    if len(resultfile) > 0:
        filecheck = [{"pathname":os.path.join(monitoringbp.root_path, "..\\files\\emailattachment\\" + x['referenceid'] + "\\" + x['aliasfilename']), "filename":x['filename']} for x in resultfile]
        # filecheck = [{"pathname":os.path.join(app.root_path, "../files/emailattachment/" + x['referenceid'] + "/" + x['aliasfilename']), "filename":x['filename']} for x in resultfile]

    # Update Status Approve
    # resultapprove, messageapprove = requestapprovalauthentication.update_statusapprove(data, params["requestapprovalauthenticationid"])
    resultapprove, messageapprove = (True, "Done")

    # Set Period & Status
    period = session["pictracking"]["period"]

    # Get data for Email Part
    monitoring = Monitoring()
    resultdocument, messagedocument = monitoring.viewtracking(params["requestapprovalid"], 0)
    resultworkflow, messageworkflow = monitoring.viewtracking(params["requestapprovalid"], 2)

    getpemohon = [x for x in resultworkflow if x["piclevel"] == 1 and x["picsublevel"] == 1]
    getcurrentapprover = [x for x in resultworkflow if x["picid"] == params["picid"]]

    getmaxlevel = max(resultworkflow, key=lambda x:x['piclevel'])
    getlastperson = [x for x in resultworkflow if x["piclevel"] == getmaxlevel["piclevel"]]

    # Get email for sending To:
    # emailto = "".join((x["email"]+",") for x in resultworkflow if x["piclevel"] > int(params["piclevel"]))
    # emailto = "".join((x["email"]+",") for x in resultworkflow if x["piclevel"] == (int(params["piclevel"]) + 1))
    emailto = [x for x in resultworkflow if x["piclevel"] == (int(params["piclevel"]) + 1)]

    # Replace Approver Status on Table Html
    tablehtml = StringUtil.findandreplace(params["workflowtable"], 'Pending', params["textstatus"], params["picsublevel"])
    tablehtml = StringUtil.findandreplace(tablehtml, '#ffc107', params["colorstatus"], params["picsublevel"])

    if params["statusapprove"] == 1:
        # Replace the signature
        layoutdocument = StringUtil.replacesignature(params['layoutdocument'], session['pictracking']['piclevel'], session['pictracking']['picsublevel'], params["masterdocid"])

        data.pop("statusapprove", None)
        data.pop("commentapprove", None)
        data["layoutdocument"] = layoutdocument

        # Update Layout on RequestApproval
        requestapproval = RequestApproval()
        # resultupdatelayout, messageupdatelayout = requestapproval.update_requestapproval(data, params["requestapprovalid"])

        # toDo perlu ditanyakan lagi
        # Chek if user is last person or not
        iflastperson = [x for x in getlastperson if x["picid"] == params["picid"]]

        if len(iflastperson) > 0:
            # emailto = "".join((x["email"]+",") for x in resultworkflow)
            emailto = [x for x in resultworkflow]
    else:
        # emailto = f'{getpemohon[0]["email"]},{getcurrentapprover[0]["email"]}'
        emailto = [{"email": getpemohon[0]["email"], "picid": getpemohon[0]["picid"]}, {"email": getcurrentapprover[0]["email"], "picid": getcurrentapprover[0]["picid"]}]
    
    email_path = conf.EMAIL_PATH

    for sent in emailto:
        encryptpicid = parameterquery.encrypt_parameter_query(sent["picid"])
        emailbody = f'''<font>Salam Satu Hati,</font><br> Dokumen: {resultdocument["requestid"]} - {resultdocument["name"]}, telah terkirim!<br> 
        Keterangan: {resultdocument["desc"]}<br>Pemohon: {getpemohon[0]["picname"]} - {getpemohon[0]["divisi"]}<br>------------<br>
        <a href="{email_path}/{encryptpicid.decode('utf-8')}/{params["requestapprovalid"]}/{period}">Click here to <b>track</b> approval detail</a><br>------------<br>
        Approved By : <br> {tablehtml} </div><br>Terimakasih.'''

        emailsubject = "[NO-REPLY]CONFIRMATION REQUEST APPROVAL"

        result, message = True, "Success"
        if emailto != "":
            # result, message = Email.send_email("wahyuhidayah.4haha@gmail.com", "", emailsubject, emailbody, filecheck)
            result, message = Email.send_email(sent["email"], "", emailsubject, emailbody, filecheck)

            return {
                "success": "1" if result else "0",
                "message": message
            }
    return {
        "success": "1" if resultapprove else "0",
        "message": messageapprove
    }


@monitoringbp.route('/api/1.0/viewtracking/levelsession', methods=['POST'])
@flask_login.login_required
def api_1_0_viewtracking_levelsession():
    params = request.json
    session['pictracking'] = {
        "piclevel": params['piclevel'],
        "picsublevel": params['picsublevel'],
        "requestapprovalauthenticationid": params['requestapprovalauthenticationid'],
        "period": params['period']
    }
    return {
        "success": "1",
        "message": "Done",
    }


# @monitoringbp.route('/api/1.0/page/<url>/<requestapprovalid>/<period>', methods=['GET'])
# def api_1_0_page(url, requestapprovalid, period):
#     session['urlpage'] = {
#         "url": url,
#         "requestapprovalid": requestapprovalid,
#         "period": period
#     }
#     return redirect(url_for(url, requestapprovalid=requestapprovalid, period=period))
#     # return redirect(f'''https://go.mpm-motor.com/approvalonline/monitoring/viewtracking/linksession/{requestapprovalid}/{period}''', code=302)


# @monitoringbp.route('/viewtracking/linksession/<requestapprovalid>/<period>', methods=['GET'])
# @flask_login.login_required
# def linksess(requestapprovalid, period):
#     try:
#         session['urlpage'] = None

#         monitoring = Monitoring()

#         # If Pemohon is not approved
#         resultfilter, messagefilter = monitoring.trackingworkflow_header(session["usersession"]["npk"], period, 2)
#         getrequestapproval = [x for x in resultfilter if x["requestapprovalid"] == requestapprovalid and x["statusapprove"] == 0]

#         if len(getrequestapproval) == 0:
#             # Check without header
#             resultfilter, messagefilter = monitoring.trackingworkflow(session["usersession"]["npk"], period, 2)
#             getrequestapproval = [x for x in resultfilter if x["requestapprovalid"] == requestapprovalid and x["statusapprove"] == 0]

#         if len(getrequestapproval) > 0:
#             resultworkflow, messageworkflow = monitoring.viewtracking(requestapprovalid, 2)
#             istherenpk = [x for x in resultworkflow if x["picid"] == session["usersession"]["npk"]]

#             if len(istherenpk) > 0:
#                 sorted_getrequestapproval = sorted(getrequestapproval, key=lambda d: d['piclevel'])

#                 session['pictracking'] = {
#                     "piclevel": sorted_getrequestapproval[0]['piclevel'],
#                     "picsublevel": sorted_getrequestapproval[0]['picsublevel'],
#                     "requestapprovalauthenticationid": sorted_getrequestapproval[0]['requestapprovalauthenticationid'],
#                     "period": period
#                 }

#                 if sorted_getrequestapproval[0]['statusapprove'] == 1 or sorted_getrequestapproval[0]['statusapprove'] == 2:
#                     # return redirect(f'''https://go.mpm-motor.com/approvalonline/monitoring/pageapproved/''', code=302)
#                     return redirect(url_for('monitoringbp.pageapproved'))
#                 else:
#                     # return redirect(f'''https://go.mpm-motor.com/approvalonline/monitoring/trackingworkflow/view/{requestapprovalid}''', code=302)
#                     return redirect(url_for('monitoringbp.viewtracking', requestapprovalid=requestapprovalid))
#             else:
#                 raise ValueError("Access denied!")
#         else:
#             raise ValueError("Request Approval tidak ditemukan!")
        
#     except Exception as e:
#         return render_template('handler/error.html', title='Error Page', message=str(e))


# @monitoringbp.route('/api/2.0/page/<url>/<npk>/<requestapprovalid>/<period>', methods=['GET'])
# def api_1_0_page(url, npk, requestapprovalid, period):
#     session['urlpage'] = {
#         "url": url,
#         "npk": str(npk).zfill(5),
#         "requestapprovalid": requestapprovalid,
#         "period": period
#     }
#     return redirect(url_for(url, npk=str(npk).zfill(5), requestapprovalid=requestapprovalid, period=period))


@monitoringbp.route('/viewtracking/validation/<npk>/<requestapprovalid>/<period>', methods=['GET'])
def validation_url_email(npk, requestapprovalid, period):
    try:
        decryptnpk = parameterquery.decrypt_parameter_query(npk.encode('utf-8'))
        npk = str(decryptnpk).zfill(5)
        # npk = str(npk).zfill(5)
        monitoring = Monitoring()

        # If Pemohon is not approved
        resultfilter, messagefilter = monitoring.trackingworkflow_header(npk, period, 2)
        getrequestapproval = [x for x in resultfilter if x["requestapprovalid"] == requestapprovalid and x["statusapprove"] == 0]

        if len(getrequestapproval) == 0:
            # Check without header
            resultfilter, messagefilter = monitoring.trackingworkflow(npk, period, 2)
            getrequestapproval = [x for x in resultfilter if x["requestapprovalid"] == requestapprovalid and x["statusapprove"] == 0]

        if len(getrequestapproval) > 0:
            resultworkflow, messageworkflow = monitoring.viewtracking(requestapprovalid, 2)
            istherenpk = [x for x in resultworkflow if x["picid"] == npk]

            if len(istherenpk) > 0:
                sorted_getrequestapproval = sorted(getrequestapproval, key=lambda d: d['piclevel'])

                session['pictracking'] = {
                    "piclevel": sorted_getrequestapproval[0]['piclevel'],
                    "picsublevel": sorted_getrequestapproval[0]['picsublevel'],
                    "requestapprovalauthenticationid": sorted_getrequestapproval[0]['requestapprovalauthenticationid'],
                    "period": period
                }

                if sorted_getrequestapproval[0]['statusapprove'] == 1 or sorted_getrequestapproval[0]['statusapprove'] == 2:
                    # return redirect(f'''https://go.mpm-motor.com/approvalonline/monitoring/pageapproved/''', code=302)
                    return redirect(url_for('monitoringbp.pageapproved'))
                else:
                    # return redirect(f'''https://go.mpm-motor.com/approvalonline/monitoring/trackingworkflow/view/{requestapprovalid}''', code=302)
                    return redirect(url_for('monitoringbp.emaildecision', npk=npk, requestapprovalid=requestapprovalid))
            else:
                raise ValueError("Access denied!")
        else:
            raise ValueError("Request Approval tidak ditemukan!")
        
    except Exception as e:
        return render_template('handler/error.html', title='Error Page', message=str(e))


@monitoringbp.route('/document')
@flask_login.login_required
def document():
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    return render_template('monitoring/document.html', title='Documents')


@monitoringbp.route('/trackingworkflow')
@flask_login.login_required
def trackingworkflow():
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    return render_template('monitoring/trackingworkflow.html', title='Tracking Workflow')


@monitoringbp.route('/trackingworkflow/view/<requestapprovalid>')
@flask_login.login_required
def viewtracking(requestapprovalid):
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if 'pictracking' not in session:
        # find user based on userid, update information user
        return redirect(url_for('monitoringbp.trackingworkflow'))
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    monitoring = Monitoring()
    result, message = monitoring.viewtracking(requestapprovalid, 0)
    return render_template('monitoring/viewtracking.html', title='View Tracking', request=result)


@monitoringbp.route('/pageapproved')
def pageapproved():
    return render_template('monitoring/pageapproved.html')


@monitoringbp.route('/emaildecision/<npk>/<requestapprovalid>')
def emaildecision(npk, requestapprovalid):
    monitoring = Monitoring()
    result, message = monitoring.viewtracking(requestapprovalid, 0)
    return render_template('monitoring/emailpage.html', title="Request Decision", request=result, picid=npk)