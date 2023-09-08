from app.models.base import BaseTable

class DesignDocumentGroupQuestion(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmds'
        self.__tablename__ = 'designdocument_groupquestion'
        self.__primarykey__ = "designdocumentgroupquestionid"
        super().__init__()


    def list_groupquestion(self, documentid):
        result = []
        message = ""
        try:
            query = "select gq.designdocumentgroupquestionid, gq.grouptitle, gq.sectiontype " \
                "from %s gq " \
                "where gq.masterdocid=%s " \
                "order by createddate asc" % (self.__tablename__, "?")
            data, message = self.execute(query, (documentid, ))
            for x in data:
                row = {
                    'designdocumentgroupquestionid': x[0],
                    'grouptitle': x[1],
                    'sectiontype': x[2]
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)

    def insert_groupquestion_withcopy(self, data):
        try:
            for x in data:
                new_id, message = self.new_id()
                field = [y for y in x]
                field.append("designdocumentgroupquestionid")
                field = ",".join(field)

                fieldvalues = ["?" for y in x]
                fieldvalues.append("?")
                fieldvalues = ",".join(fieldvalues)

                params = [x[y] for y in x]
                params.append(new_id)

                query = "INSERT INTO %s(%s) VALUES (%s)" % (self.__tablename__, field, fieldvalues)
                self.execute(query, tuple(params))
            
            self.__connection__.commit()
            return(True, new_id)
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))