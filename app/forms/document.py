from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField, BooleanField
import wtforms.validators as validators


class Document(Form):
    documentname = StringField('Document Name', validators=[
        validators.input_required(), validators.length(max=100)])
    documentdescription = TextAreaField('Document Description', validators=[
        validators.input_required(), validators.length(max=255)])
    documentversion = StringField('Document Version', validators=[
        validators.input_required(), validators.length(max=5)])
    documenttype = StringField('Document Type', validators=[
        validators.input_required()])
    documentstatus = SelectField('Document Status', choices=[('0', 'Inactive'), ('1', 'Active')], validators=[
        validators.input_required()])
    documentlayout = SelectField('Document Layout', choices=[('0', 'Portrait'), ('1', 'Landscape')], validators=[
        validators.input_required()])
    documentsignature = SelectField('Document Signature', choices=[('1', 'Yes'), ('0', 'No')], validators=[
        validators.input_required()])
    documentisprint = SelectField('Document Print?', choices=[('1', 'Yes'), ('0', 'No')], validators=[
        validators.input_required()])

    documentaccess_staff = BooleanField("Staff")
    documentaccess_supervisor = BooleanField("Supervisor")
    documentaccess_deputydepthead = BooleanField("Deputy Department Head")
    documentaccess_depthead = BooleanField("Department Head")
    documentaccess_deputydivhead = BooleanField("Deputy Division Head")
    documentaccess_divhead = BooleanField("Division Head")
    documentaccess_directur = BooleanField("Directur")
