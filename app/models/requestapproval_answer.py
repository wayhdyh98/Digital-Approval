from app.models.base import BaseTable

class RequestApprovalAnswer(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmds'
        self.__tablename__ = 'requestapproval_answer'
        super().__init__()


    def get_answer(self, requestapprovalid):
        try:
            result = []
            query = "SELECT a.requestapprovalanswerid, a.requestapprovalid, a.designdocumentquestionid," \
            "a.answer, b.questiontypecomponent, b.questioncondition, b.questiontype, b.designdocumentgroupquestionid, c.sectiontype FROM %s a " \
            "LEFT JOIN designdocument_question b ON a.designdocumentquestionid = b.designdocumentquestionid " \
            "LEFT JOIN designdocument_groupquestion c on b.designdocumentgroupquestionid = c.designdocumentgroupquestionid " \
            "WHERE a.requestapprovalid = ? and b.questiontype = 0" % (self.__tablename__)
            data, message = self.execute(query, (requestapprovalid,))

            for x in data:
                row = {
                    'requestapprovalanswerid': x[0],
                    'requestapprovalid': x[1],
                    'designdocumentquestionid': x[2],
                    'answer': x[3],
                    'questiontypecomponent': x[4],
                    'questioncondition': x[5],
                    'questiontype': x[6],
                    'designdocumentgroupquestionid': x[7],
                    'sectiontype': x[8],
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)

    
    def get_answerbase(self, requestapprovalid):
        try:
            result = []
            query = "SELECT a.designdocumentquestionid," \
            "b.questiontypecomponent, b.questioncondition, b.questiontype FROM %s a " \
            "LEFT JOIN designdocument_question b ON a.designdocumentquestionid = b.designdocumentquestionid " \
            "WHERE a.requestapprovalid = ? " \
            "group by a.designdocumentquestionid, b.questiontypecomponent, b.questioncondition, b.questiontype" % (self.__tablename__)
            data, message = self.execute(query, (requestapprovalid,))

            for x in data:
                row = {
                    'designdocumentquestionid': x[0],
                    'questiontypecomponent': x[1],
                    'questioncondition': x[2],
                    'questiontype': x[3]
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)


    def get_answer_multirow(self, data):
        try:
            result = []
            query = "SELECT a.requestapprovalanswerid, a.requestapprovalid, a.designdocumentquestionid," \
            "a.answer, b.questiontypecomponent, b.questioncondition, b.questiontype, b.designdocumentgroupquestionid, c.sectiontype " \
            "FROM %s a " \
            "LEFT JOIN designdocument_question b ON a.designdocumentquestionid = b.designdocumentquestionid " \
            "LEFT JOIN designdocument_groupquestion c on b.designdocumentgroupquestionid = c.designdocumentgroupquestionid " \
            "WHERE a.requestapprovalid = ? and a.designdocumentquestionid = ? and b.questiontype = 1 and b.questiontypecomponent = ? and b.questioncondition = ?" % (self.__tablename__)
            data, message = self.execute(query, (data['requestapprovalid'], data['designdocumentquestionid'], data['questiontypecomponent'], data['questioncondition'],))

            for x in data:
                row = {
                    'requestapprovalanswerid': x[0],
                    'requestapprovalid': x[1],
                    'designdocumentquestionid': x[2],
                    'answer': x[3],
                    'questiontypecomponent': x[4],
                    'questioncondition': x[5],
                    'questiontype': x[6],
                    'designdocumentgroupquestionid': x[7],
                    'sectiontype': x[8],
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)

    
    def get_answer_multigroup(self, requestapprovalid):
        try:
            result = []
            query = "SELECT a.requestapprovalanswerid, a.requestapprovalid, a.designdocumentquestionid, " \
            "a.answer, b.questiontypecomponent, b.questioncondition, b.questiontype, " \
            "b.designdocumentgroupquestionid, a.answergroupid " \
            "FROM %s a " \
            "LEFT JOIN designdocument_question b ON a.designdocumentquestionid = b.designdocumentquestionid " \
            "LEFT JOIN designdocument_groupquestion c on b.designdocumentgroupquestionid = c.designdocumentgroupquestionid " \
            "WHERE a.requestapprovalid = ? and c.sectiontype = 1 ORDER BY a.answerorder, a.answergroupid" % (self.__tablename__)
            data, message = self.execute(query, (requestapprovalid,))

            for x in data:
                row = {
                    'requestapprovalanswerid': x[0],
                    'requestapprovalid': x[1],
                    'designdocumentquestionid': x[2],
                    'answer': x[3],
                    'questiontypecomponent': x[4],
                    'questioncondition': x[5],
                    'questiontype': x[6],
                    'designdocumentgroupquestionid': x[7],
                    'answergroupid': x[8],
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)


    def insert_answer(self, data, requestapprovalid):
        try:
            query2 = "DELETE FROM %s WHERE requestapprovalid=?" % (self.__tablename__)
            self.execute(query2, (requestapprovalid,))
            
            for x in data:
                new_id, message = self.new_id()
                field = [y for y in x]
                field.append("requestapprovalanswerid")
                field = ",".join(field)

                fieldvalues = ["?" for y in x]
                fieldvalues.append("?")
                fieldvalues = ",".join(fieldvalues)

                params = [x[y] for y in x]
                params.append(new_id)

                query = "INSERT INTO %s(%s) VALUES (%s)" % (self.__tablename__, field, fieldvalues)
                self.execute(query, tuple(params))

            self.__connection__.commit()

            return(True, "success")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))
    