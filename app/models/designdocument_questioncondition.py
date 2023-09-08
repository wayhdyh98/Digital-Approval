from app.models.base import BaseTable

class DesignDocumentQuestionCondition(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmds'
        self.__tablename__ = 'designdocument_questioncondition'
        self.__primarykey__ = "designdocumentquestionconditionid"
        super().__init__()


    def list_questioncondition(self):
        result = []
        message = ""
        try:
            data, message = self.list()
            for x in data:
                row = {
                    'designdocumentquestionconditionid': x[0],
                    'questionconditionname': x[1],
                    'questionconditionquery': x[2],
                    'statuscondition': x[3],
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)


    def list_selectquerycondition(self, questionconditionid, companyid):
        result = []
        message = ""
        try:
            query = "select questionconditionquery from %s where %s=%s" % (self.__tablename__, self.__primarykey__, "?")
            data, message = self.readone(questionconditionid)
            
            # select the query
            query = "SELECT A.CODE, A.VALUE FROM (%s) A WHERE COMPANYID=%s ORDER BY A.VALUE" % (data[2], "?")
            data_select, message = self.execute(query, (companyid, ))
            for y in data_select:
                row = {
                    "code": y[0],
                    "value": f'''{str(y[0]).zfill(5)} - {y[1]}''',
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)