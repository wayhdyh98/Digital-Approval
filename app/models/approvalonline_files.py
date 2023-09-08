from app.models.base import BaseTable

class ApprovalOnlineFiles(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmds'
        self.__tablename__ = 'approvalonline_files'
        super().__init__()


    def insert_file(self, data):
        try:
            new_id, message = self.new_id()

            query = "INSERT INTO %s(approvalonlinefileid, filename, aliasfilename, size, comments, referenceid, deleteflag, createdby, createddate) VALUES(%s)" % (self.__tablename__, "?, ?, ?, ?, ?, ?, ?, ?, ?")
            self.execute(query, (new_id, data["filename"], data["aliasfilename"], data["size"], data["comments"], data["referenceid"], data["deleteflag"], data["createdby"], data["createddate"],))

            self.__connection__.commit()

            return(True, new_id, "success")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))


    def get_files(self, requestapprovalid):
        try:
            result = []
            query = "SELECT approvalonlinefileid, filename, aliasfilename, referenceid, size FROM %s WHERE referenceid = ? and deleteflag = 0" % (self.__tablename__)
            data, message = self.execute(query, (requestapprovalid,))

            for x in data:
                row = {
                    'approvalonlinefileid': x[0],
                    'filename': x[1],
                    'aliasfilename': x[2],
                    'referenceid': x[3],
                    'size': x[4]
                }
                result.append(row)
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))
        
        return (result, message)


    def readone(self, approvalonlinefileid):
        try:
            result = {}
            query = "SELECT approvalonlinefileid, filename, aliasfilename, referenceid FROM %s WHERE approvalonlinefileid = ?" % (self.__tablename__)
            data, message = self.execute(query, (approvalonlinefileid,))

            for x in data:
                result = {
                    'approvalonlinefileid': x[0],
                    'filename': x[1],
                    'aliasfilename': x[2],
                    'referenceid': x[3]
                }
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)


    def delete_file(self, data, approvalonlinefileid):
        try:
            query = "UPDATE %s SET deleteflag=?, modifby=?, modifdate=? WHERE approvalonlinefileid=?" % (self.__tablename__)
            self.execute(query, (data["deleteflag"],data["modifby"], data["modifdate"], approvalonlinefileid,))

            self.__connection__.commit()
            return(True, "success")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))
    