from app.models.base import BaseTable

class MasterDocumentDesignDocument(BaseTable):
    def __init__(self):
        self.__database__ = 'mpmds'
        self.__tablename__ = 'masterdocument_designdocument'
        self.__primarykey__ = "designdocumentid"
        super().__init__()


    def insert_data(self, data):
        try:
            new_id, message = self.new_id()

            query = "INSERT INTO %s VALUES(%s)" % (self.__tablename__, "?, ?, ?, ?, ?, ?, ?, ?, ?")
            self.execute(query, (new_id, data["documentid"], data["contentdocument"], data["contentorigin"], data["version"], data["createdby"], data["createddate"], data["modifby"], data["modifdate"],))
            
            self.__connection__.commit()
            return(True, "success")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))


    def list_designdocument(self, documentid):
        result = []
        message = ""
        try:
            query = "select d.designdocumentid, d.documentid, d.contentdocument, " \
                "d.contentorigin, d.version, m.activeversiondocument from %s d " \
                "left join masterdocument m on d.documentid = m.masterdocid " \
                "where d.documentid=%s order by d.version" % (self.__tablename__, "?")
            data, message = self.execute(query, (documentid,))

            for x in data:
                row = {
                    'designdocumentid': x[0],
                    'documentid': x[1],
                    'contentdocument': x[2],
                    'contentorigin': x[3],
                    'version': x[4],
                    'activeversiondocument': x[5],
                }
                result.append(row)

        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)


    def update_designdocument(self, data, designdocumentid):
        try:
            query = "UPDATE %s SET contentdocument=?, contentorigin=?, modifby=?, modifdate=? WHERE designdocumentid=?" % (self.__tablename__)
            self.execute(query, (data["contentdocument"], data["contentorigin"], data["modifby"], data["modifdate"], designdocumentid,))

            self.__connection__.commit()
            return(True, "success")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))