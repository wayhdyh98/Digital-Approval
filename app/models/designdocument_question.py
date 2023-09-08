import pyodbc
from datetime import timedelta
from app.models.base import BaseTable

class DesignDocumentQuestion(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmds'
        self.__tablename__ = 'designdocument_question'
        self.__primarykey__ = "designdocumentquestionid"
        super().__init__()


    def list_question(self, documentid, groupquestionid):
        result = []
        message = ""
        try:
            query = f'''select a.designdocumentquestionid, a.designdocumentgroupquestionid, a.masterdocid,
                a.question, a.questiontype, a.questioncondition, a.mandatory, a.questiontypecomponent, 
                b.questionconditionname, a.note
                from {self.__tablename__} a
                left join designdocument_questioncondition b on a.questioncondition = b.designdocumentquestionconditionid
                where a.masterdocid=? and a.designdocumentgroupquestionid=?
                order by createddate asc'''
            data, message = self.execute(query, (documentid, groupquestionid, ))
            for x in data:
                row = {
                    'designdocumentquestionid': x[0],
                    'designdocumentgroupquestionid': x[1],
                    'masterdocid': x[2],
                    'question': x[3],
                    'questiontype': x[4],
                    'questioncondition': x[5],
                    'mandatory': x[6],
                    'questiontypecomponent': x[7],
                    'questionconditionname': x[8],
                    'note': x[9],
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)


    def list_multichoice(self, designdocumentquestionid):
        result = []
        message = ""
        try:
            query = "select " \
                "a.designdocumentmultichoiceid, a.designdocumentquestionid, a.masterdocid, " \
                "a.code, a.[value] " \
                "from designdocument_multichoice a " \
                "where a.designdocumentquestionid=%s order by a.createddate" % ("?")
            data, message = self.execute(query, (designdocumentquestionid, ))
            for x in data:
                row = {
                    'designdocumentmultichoiceid': x[0],
                    'designdocumentquestionid': x[1],
                    'masterdocid': x[2],
                    'code': x[3],
                    '[value]': x[4],
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)

    def check_multirowquestion(self, designdocumentgroupquestionid):
        result = []
        message = ""
        try:
            query = f'''select a.designdocumentquestionid from {self.__tablename__} a
                where a.designdocumentgroupquestionid=? and a.questiontype=1 '''
            data, message = self.execute(query, (designdocumentgroupquestionid, ))
            for x in data:
                row = {
                    'designdocumentquestionid': x[0],
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)

    def insert_data(self, data):
        try:
            multichoice =  data.pop('multichoice')

            new_id, message = self.new_id()
            field = [x for x in data]
            field.append("designdocumentquestionid")
            field = ",".join(field)

            fieldvalues = ["?" for x in data]
            fieldvalues.append("?")
            fieldvalues = ",".join(fieldvalues)

            params = [data[x] for x in data]
            params.append(new_id)

            # insert the question
            query = "INSERT INTO %s(%s) VALUES (%s)" % (self.__tablename__, field, fieldvalues)
            self.execute(query, tuple(params))

            # iterate multichoice
            if len(multichoice) > 0:
                temptime = data["createddate"] + timedelta(seconds=5)
                for x in multichoice:
                    query = "INSERT INTO designdocument_multichoice(designdocumentquestionid, masterdocid, code, [value], createdby, createddate) VALUES(%s)" % ("?, ?, ?, ?, ?, ?")
                    self.execute(query, (new_id, data["masterdocid"], x["code"], x["value"], data["createdby"], temptime,))
                    temptime = temptime + timedelta(seconds=5)
            
            self.__connection__.commit()
            return(True, "")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))


    def delete_data(self, designdocumentquestionid):
        try:
            cursor = self.__connection__.cursor()
            # delete all multi choice
            query = "DELETE FROM designdocument_multichoice WHERE designdocumentquestionid=? "
            cursor.execute(query, (designdocumentquestionid,))

            # delete question
            query2 = "DELETE FROM designdocument_question WHERE designdocumentquestionid=?"
            cursor.execute(query2, (designdocumentquestionid,))
            
            self.__connection__.commit()
            return(True, "")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))
            

    
    def update_data(self, designdocumentquestionid, data):
        try:
            multichoice =  data.pop('multichoice')

            field = [x+"=?" for x in data]
            field = ",".join(field)

            params = [data[x] for x in data]
            params.append(designdocumentquestionid)

            query = "UPDATE %s SET %s WHERE designdocumentquestionid=?" % (self.__tablename__, field)
            self.execute(query, tuple(params))
            
            # delete all multi choice
            query = "DELETE FROM designdocument_multichoice WHERE designdocumentquestionid=?"
            self.execute(query, (designdocumentquestionid))

            # iterate multichoice
            if len(multichoice) > 0:
                temptime = data["modifdate"] + timedelta(seconds=5)
                for x in multichoice:
                    query = "INSERT INTO designdocument_multichoice(designdocumentquestionid, masterdocid, code, [value], createdby, createddate) VALUES(%s)" % ("?, ?, ?, ?, ?, ?")
                    self.execute(query, (designdocumentquestionid, data["masterdocid"], x["code"], x["value"], data["modifby"], temptime,))
                    temptime = temptime + timedelta(seconds=5)
            
            self.__connection__.commit()
            return(True, "")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))