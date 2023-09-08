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
from json import dumps

import datetime as dt
import json

# database
from app.models.user import User
from app.models.document import Document
from app.models.approval import Approval
from app.models.security import Security
from app.models.designdocument_groupquestion import DesignDocumentGroupQuestion
from app.models.designdocument_question import DesignDocumentQuestion
from app.models.designdocument_questioncondition import DesignDocumentQuestionCondition
from app.models.masterdocument_designdocument import MasterDocumentDesignDocument

# libraries
from app.libraries.session import usersession as USession

# forms
from app.forms import document as document_forms

# Create a document blueprint
documentbp = Blueprint('documentbp', __name__, url_prefix='/document')


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


@documentbp.route('/api/1.0/documents')
@flask_login.login_required
def api_1_0_documents():
    # get company id 
    usersession = session["usersession"]
    companyid = usersession["company"]
    divisionid = usersession["division"]
    departmentid = usersession["department"]
    
    # try to get list of document
    document = Document()
    result, message = document.list_document(companyid, divisionid, departmentid)
    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }


@documentbp.route('/api/1.0/documentssubmissions/<divisionid>')
@flask_login.login_required
def api_1_0_documentssubmissions(divisionid):
    # get company id 
    usersession = session["usersession"]
    companyid = usersession["company"]
    departmentid = usersession["department"]
    
    # try to get list of document
    document = Document()
    result, message = document.list_document(companyid, divisionid, departmentid)
    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }


@documentbp.route('/api/1.0/document/delete', methods=['POST'])
@flask_login.login_required
def api_1_0_deletedocument():
    params = request.json

    document = Document()
    result, message = document.delete_document(params["documentid"])
    return {
        "success": "1" if result else "0",
        "message": message,
        "data": result
    }


@documentbp.route('/api/1.0/approvals/<documentid>')
@flask_login.login_required
def api_1_0_approvals(documentid):    
    approval = Approval()
    result, message = approval.list_approval(documentid)
    check_pemohon = "true" if any(x['pictype'] == 0 for x in result) else "false"
    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result,
        "checkpemohon": check_pemohon
    }


@documentbp.route('/api/1.0/approval/parent/<documentid>')
@flask_login.login_required
def api_1_0_parentapproval(documentid):    
    approval = Approval()
    result, message = approval.list_approval_parent(documentid)
    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }


@documentbp.route("/api/1.0/approvals/insert", methods=["POST"])
@flask_login.login_required
def api_1_0_insertapproval():
    usersession = session["usersession"]
    approval = Approval()
    security = Security()
    params = request.json

    # check pic level, if = 0 -> do autogenerate
    piclevel = int(params["piclevel"])
    picsublevel = 1
    if piclevel == 0:
        piclevel, message = approval.get_maxlevel(params["documentid"])
        if piclevel == None:
            piclevel = 0
        piclevel = piclevel + 1
    else:
        picsublevel, message = approval.get_maxsublevel(params["documentid"], piclevel)
        picsublevel = picsublevel + 1

    # check if npk has email or not in mpmit_pic
    check, message = security.check_email_in_mpmit_pic(str(params["picid"]).zfill(5))

    if len(check) > 0:
        data = [
            {
                "masterdocid": params["documentid"],
                "pictype": int(params["pictype"]),
                "picid": str(params["picid"]).zfill(5),
                "piclevel": piclevel,
                "picsublevel": picsublevel,
                "mandatory": 1 if params["mandatory"] == "1" else 0,
                "descriptionapprovaltitle": params["description"],
                "createdby": usersession["npk"],
                "createddate": dt.datetime.now(),
                "modifby": "",
                "modifdate": "",
            }
        ]

        result, message = approval.insert(data)
    else:
        result, message = (False, f'''Data Email tidak ditemukan pada NPK {params["picid"]}!''')
    
    return {
        "success": "1" if result else "0",
        "message": message,
        "data": result
    }


@documentbp.route('/api/1.0/approvals/delete', methods=['POST'])
@flask_login.login_required
def api_1_0_deleteapproval():
    params = request.json

    approval = Approval()
    result, message = approval.delete(params["approveid"])
    return {
        "success": "1" if result else "0",
        "message": message if result else "<b>Authorization cannot be deleted because it has been</b> used <b>on Requested Approval!</b>",
        "data": result
    }


@documentbp.route('/browse')
@flask_login.login_required
def browse():
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    return render_template('document/browse.html', title='Documents')


@documentbp.route('/add', methods=['GET', 'POST'])
@flask_login.login_required
def add():
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    form = document_forms.Document(request.form)
    document = Document()

    if request.method=="POST":
        # check document is there or not with that name
        rowdoc, messagedoc = document.list_document("all", "all", "all")
        check = [x for x in rowdoc if x["name"].lower().strip().replace(" ", "") == form.documentname.data.lower().strip().replace(" ", "") and int(x["version"]) == int(form.documentversion.data)]

        if len(check) > 0:
            return render_template('document/add.html', title='Add - Documents', form=form, validation=True)

        # authorization
        authorization = ""
        if form.documentaccess_staff.data:
            authorization = authorization + "staff|"
        if form.documentaccess_supervisor.data:
            authorization = authorization + "supervisor|"
        if form.documentaccess_deputydepthead.data:
            authorization = authorization + "deputy department head|"
        if form.documentaccess_depthead.data:
            authorization = authorization + "department head|"
        if form.documentaccess_deputydivhead.data:
            authorization = authorization + "deputy division head|"
        if form.documentaccess_divhead.data:
            authorization = authorization + "division head|"
        if form.documentaccess_directur.data:
            authorization = authorization + "directur|"

        usersession = session["usersession"]
        data = [
            {
                "companyid": usersession["company"],
                "divisionid": usersession["division"],
                "departmentid": usersession["department"],
                "name": form.documentname.data,
                "isprint": form.documentisprint.data,
                "[desc]": form.documentdescription.data,
                "version": form.documentversion.data,
                "status": form.documentstatus.data,
                "deleteflag": 0,
                "createdby": usersession["npk"],
                "createddate": dt.datetime.now(),
                "layout": form.documentlayout.data,
                "nosig": form.documentsignature.data,
                "modifby": "",
                "modifdate": "",
                "entryauth": authorization
            }
        ]
        document = Document()
        result, message = document.insert(data)
        if result:
            return redirect(url_for('documentbp.browse'))    

    return render_template('document/add.html', title='Add - Documents', form=form, validation=False)


@documentbp.route('/edit/<documentid>', methods=['GET', 'POST'])
@flask_login.login_required
def edit(documentid):
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    form = document_forms.Document(request.form)
    document = Document()
    
    if request.method=="GET":
        row, message = document.readone_document(documentid)
        form.documentname.data = row["name"]
        form.documentdescription.data = row["desc"]
        form.documentversion.data = row["version"]
        form.documentisprint.data = str(row["isprint"])
        form.documentlayout.data = str(row["layout"])
        form.documentstatus.data = str(row["status"])
        form.documentsignature.data = str(row["signature"])

        # authorization
        split_auth = str(row["auth"])[:-1].split("|")
        for row in split_auth:
            if row == "staff":
                form.documentaccess_staff.data = True
            if row == "supervisor":
                form.documentaccess_supervisor.data = True
            if row == "deputy department head":
                form.documentaccess_deputydepthead.data = True
            if row == "department head":
                form.documentaccess_depthead.data = True
            if row == "deputy division head":
                form.documentaccess_deputydivhead.data = True
            if row == "division head":
                form.documentaccess_divhead.data = True
            if row == "directur":
                form.documentaccess_directur.data = True

    if request.method=="POST":
        # authorization
        authorization = ""
        if form.documentaccess_staff.data:
            authorization = authorization + "staff|"
        if form.documentaccess_supervisor.data:
            authorization = authorization + "supervisor|"
        if form.documentaccess_deputydepthead.data:
            authorization = authorization + "deputy department head|"
        if form.documentaccess_depthead.data:
            authorization = authorization + "department head|"
        if form.documentaccess_deputydivhead.data:
            authorization = authorization + "deputy division head|"
        if form.documentaccess_divhead.data:
            authorization = authorization + "division head|"
        if form.documentaccess_directur.data:
            authorization = authorization + "directur|"

        usersession = session["usersession"]

        data = [
            {
                "companyid": usersession["company"],
                "divisionid": usersession["division"],
                "departmentid": usersession["department"],
                "name": form.documentname.data,
                "isprint": form.documentisprint.data,
                "[desc]": form.documentdescription.data,
                "version": form.documentversion.data,
                "status": form.documentstatus.data,
                "layout": form.documentlayout.data,
                "nosig": form.documentsignature.data,
                "modifby": usersession["npk"],
                "modifdate": dt.datetime.now(),
                "entryauth": authorization
            }
        ]
        document = Document()
        result, message = document.update(documentid, data)
        if result:
            return redirect(url_for('documentbp.browse'))   

    return render_template('document/edit.html', 
        title='Edit - Documents', 
        form=form,
        documentid=documentid)


@documentbp.route('/authorization/<documentid>', methods=['GET', 'POST'])
@flask_login.login_required
def authorization(documentid):
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    document = Document()
    document_readone, message = document.readone_document(documentid)
    return render_template('document/authorization.html', 
        title='Authorization - Documents',
        document=document_readone)


'''
DESIGN DOCUMENTS
'''

@documentbp.route('/api/1.0/designdocument/question/condition/<documentid>/<questionconditionid>/<statuscondition>')
@flask_login.login_required
def api_1_0_designdocument_questioncondition(documentid, questionconditionid, statuscondition): 
    usersession = session["usersession"]
    companyid = usersession["company"]
    questioncondition = DesignDocumentQuestionCondition()
    result, message = questioncondition.list_selectquerycondition(questionconditionid, companyid)
    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }


@documentbp.route('/api/1.0/designdocument/groupquestions/<documentid>')
@flask_login.login_required
def api_1_0_designdocument_groupquestions(documentid):   
    designdocument_groupquestion = DesignDocumentGroupQuestion()
    result, message = designdocument_groupquestion.list_groupquestion(documentid)
    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }


@documentbp.route("/api/1.0/designdocument/groupquestion/insert", methods=["POST"])
@flask_login.login_required
def api_1_0_insertgroupquestion():
    # usersession = session["usersession"]
    usersession = g.user
    designdocument_groupquestion = DesignDocumentGroupQuestion()
    designdocument_question = DesignDocumentQuestion()
    params = request.json

    result = False
    message = ""
    if params["groupquestionid"] == "-1":
        data = [
            {
                "sectiontype": params["sectiontype"],
                "masterdocid": params["documentid"],
                "grouptitle": params["grouptitle"],
                "createdby": usersession["npk"],
                "createddate": dt.datetime.now(),
                "modifby": "",
                "modifdate": "",
            }
        ]

        if params["groupquestionidcopy"] != "-1":
            result, message = designdocument_groupquestion.insert_groupquestion_withcopy(data)

            resultquestion, messagequestion = designdocument_question.list_question(params["documentidcopy"], params["groupquestionidcopy"])

            groupquestionid = message

            for x in resultquestion:
                multichoice = []
                
                if x["questioncondition"] == 2:
                    resultmultichoice, messagemultichoice = designdocument_question.list_multichoice(x["designdocumentquestionid"])
                    multichoice = [{"code": y["code"], "value": y["[value]"]} for y in resultmultichoice]

                data = {
                    "designdocumentgroupquestionid": groupquestionid,
                    "masterdocid": params["documentid"],
                    "question": x["question"],
                    "questiontype": int(x["questiontype"]),
                    "questioncondition": int(x["questioncondition"]),
                    "mandatory": int(x["mandatory"]),
                    "questiontypecomponent": int(x["questiontypecomponent"]),
                    "note": x["note"],
                    "createdby": usersession["npk"],
                    "createddate": dt.datetime.now(),
                    "modifby": "",
                    "modifdate": "",
                    "multichoice": multichoice
                }

                result, message = designdocument_question.insert_data(data)
        else:
            result, message = designdocument_groupquestion.insert(data)
    else:
        check, messagecheck = designdocument_question.check_multirowquestion(params["groupquestionid"])
        if len(check) == 0:
            data = [
                {
                    "sectiontype": params["sectiontype"],
                    "grouptitle": params["grouptitle"],
                    "modifby": usersession["npk"],
                    "modifdate": dt.datetime.now(),
                }
            ]

            result, message = designdocument_groupquestion.update(params["groupquestionid"], data)
        else:
            return {
                "success": "0",
                "message": "You can't update if there is multirow type on your question."
            }

    return {
        "success": "1" if result else "0",
        "message": message,
        "data": result
    }


@documentbp.route('/api/1.0/designdocument/groupquestion/delete', methods=['POST'])
@flask_login.login_required
def api_1_0_deletegroupquestion():
    params = request.json
    designdocument_groupquestion = DesignDocumentGroupQuestion()
    result, message = designdocument_groupquestion.delete(params["groupquestionid"])
    return {
        "success": "1" if result else "0",
        "message": message if result else "<b>Please delete the question</b> first <b>before you delete group question!</b>" ,
        "data": result
    }


@documentbp.route('/api/1.0/designdocument/questions/<documentid>/<designdocumentgroupquestionid>')
@flask_login.login_required
def api_1_0_designdocument_questions(documentid, designdocumentgroupquestionid):    
    designdocument_question = DesignDocumentQuestion()
    result, message = designdocument_question.list_question(documentid, designdocumentgroupquestionid)
    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }


@documentbp.route('/api/1.0/designdocument/questions/multichoice/<designdocumentquestionid>')
@flask_login.login_required
def api_1_0_designdocument_questions_multichoices(designdocumentquestionid):    
    designdocument_question = DesignDocumentQuestion()
    result, message = designdocument_question.list_multichoice(designdocumentquestionid)
    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }


@documentbp.route("/api/1.0/designdocument/question/insert", methods=["POST"])
@flask_login.login_required
def api_1_0_insertquestion():
    # usersession = session["usersession"]
    usersession = g.user
    designdocument_question = DesignDocumentQuestion()
    params = request.json

    result = False
    message = ""
    if params["questionid"] == -1:
        data = {
                "designdocumentgroupquestionid": params["groupquestionid"],
                "masterdocid": params["documentid"],
                "question": params["question"],
                "questiontype": int(params["questiontype"]),
                "questioncondition": int(params["questioncondition"]),
                "mandatory": int(params["mandatory"]),
                "questiontypecomponent": int(params["questiontypecomponent"]),
                "note": params["note"],
                "createdby": usersession["npk"],
                "createddate": dt.datetime.now(),
                "modifby": "",
                "modifdate": "",
                "multichoice": params["multichoice"]
            }
        result, message = designdocument_question.insert_data(data)
    else:
        data = {
                "question": params["question"],
                "questiontype": params["questiontype"],
                "masterdocid": params["documentid"],
                "questioncondition": params["questioncondition"],
                "mandatory": params["mandatory"],
                "questiontypecomponent": params["questiontypecomponent"],
                "note": params["note"],
                "modifby": usersession["npk"],
                "modifdate": dt.datetime.now(),
                "multichoice": params["multichoice"]
            }
        
        result, message = designdocument_question.update_data(params["questionid"], data)

    return {
        "success": "1" if result else "0",
        "message": message,
        "data": result
    }


@documentbp.route('/api/1.0/designdocument/question/delete', methods=['POST'])
@flask_login.login_required
def api_1_0_deletequestion():
    params = request.json
    designdocument_question = DesignDocumentQuestion()
    result, message = designdocument_question.delete_data(params["questionid"])
    return {
        "success": "1" if result else "0",
        "message": message if result else "<b>Question cannot be deleted because it has been </b>used <b>on Requested Approval!</b>",
        "data": result
    }


@documentbp.route("/api/1.0/designdocument/<documentid>", methods=["GET"])
@flask_login.login_required
def api_1_0_designdocument(documentid):
    masterdocument_designdocument = MasterDocumentDesignDocument()
    result, message = masterdocument_designdocument.list_designdocument(documentid)

    return {
        "success": "0" if result == None else "1",
        "message": message,
        "data": result
    }


@documentbp.route("/api/1.0/designdocument/insert", methods=["POST"])
@flask_login.login_required
def api_1_0_insertdesigndocument():
    # usersession = session["usersession"]
    usersession = g.user
    masterdocument_designdocument = MasterDocumentDesignDocument()
    document = Document()
    params = request.json

    result = False
    message = ""

    resultdesign, messagedesign = masterdocument_designdocument.list_designdocument(params["documentid"])
    resultdocument, messagedocument = document.readone_document(params["documentid"])

    activeversion = ""

    if resultdocument["activeversiondocument"] == None:
        activeversion = (len(resultdesign)+1)
    else:
        if params["version"] == 0:
            activeversion = (len(resultdesign)+1) if params["activeversiondocument"] == "1" else resultdocument["activeversiondocument"]
        else:
            activeversion = int(params["version"]) if params["activeversiondocument"] == "1" else resultdocument["activeversiondocument"]

    data = {
        "activeversiondocument": activeversion,
        "masterdocid": params["documentid"],
        "modifby": usersession["npk"],
        "modifdate": dt.datetime.now()
    }
    resultupdate, messageupdate = document.update_activeversion(data)

    if params["version"] == 0:
        data = {
            "documentid": params["documentid"],
            "contentdocument": params["contentdocument"],
            "contentorigin": params["contentorigin"],
            "version": (len(resultdesign)+1),
            "createdby": usersession["npk"],
            "createddate": dt.datetime.now(),
            "modifby": "",
            "modifdate": "",
        }
        result, message = masterdocument_designdocument.insert_data(data)
    else:
        data = {
            "contentdocument": params["contentdocument"],
            "contentorigin": params["contentorigin"],
            "modifby": usersession["npk"],
            "modifdate": dt.datetime.now()
        }
        result, message = masterdocument_designdocument.update_designdocument(data, params["designdocumentid"])

    return {
        "success": "1" if result else "0",
        "message": message,
        "data": result
    }


@documentbp.route('/design/<documentid>', methods=['GET', 'POST'])
@flask_login.login_required
def design(documentid):
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    document = Document()
    document_readone, message_1 = document.readone_document(documentid)

    questioncondition = DesignDocumentQuestionCondition()
    questioncondition_data, message_2 = questioncondition.list_questioncondition()
    return render_template('document/design.html', 
        title='Design - Documents',
        document=document_readone,
        questioncondition=questioncondition_data)


@documentbp.route('/design/designquill/<documentid>', methods=['GET', 'POST'])
@flask_login.login_required
def designquill(documentid):
    if not g.user:
        return render_template('handler/error.html', title='Error Page', message="Harap lakukan login terlebih dahulu!")
    
    if g.user["npk"] != session["usersession"]["npk"]:
        return redirect('https://10.10.108.44/login')
    
    document = Document()
    document_readone, message_1 = document.readone_document(documentid)
    return render_template('document/designquill.html', 
        title='Design Quill - Documents',
        document=document_readone)


@documentbp.route('/api/1.0/submissions/fillformrequest')
@flask_login.login_required
def api_1_0_fillformrequest():    
    designdocument_groupquestion = DesignDocumentGroupQuestion()
    result, message = designdocument_groupquestion.list_groupquestion()
    return {
        "success": "1" if result == None else "0",
        "message": message,
        "data": result
    }