from app.models.base import BaseTable

class Document(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmds'
        self.__tablename__ = 'masterdocument'
        self.__primarykey__ = "masterdocid"
        self.__fields__ = [
            "companyid",
            "divisionid",
            "departmentid",
            "name",
            "desc",
            "version",
            "status",
            "deleteflag",
            "createdby",
            "createddate",
            "modifby",
            "modifdate",
            "entryauth",
            "layout",
            "nosig",
        ]
        super().__init__()


    def list_document(self, companyid, divisionid, departmentid):
        result = []
        message = ""
        try:
            data, message = super().list_ordered()
            for x in data:
                show_data = False
                
                if companyid == "all" and divisionid == "all" and departmentid == "all":
                    show_data = True
                elif companyid == x[2] and divisionid == x[3] and departmentid == x[4]:
                    show_data = True
                
                if show_data and x[10] == 0: # delete flag
                    row = {
                        'masterdocid': x[0],
                        'documentnumber': x[1],
                        'companyid': x[2],
                        'divisionid': x[3],
                        'departmentid': x[4],
                        'isprint': x[5],
                        'name': x[6],
                        'desc': x[7],
                        'version': x[8],
                        'status': x[9],
                        'createddate': x[12],
                        'auth': x[15],
                        'layout': x[16],
                        'signature': x[17],
                        'activeversiondocument': x[18],
                    }
                    result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)

    
    def list_document_for_request(self, npk, companyid, divisionid):
        result = []
        message = ""
        try:
            data, message = self.callproc("EXEC MPMDS_TIPEDOKUMEN_REQUESTAPPROVAL ?, ?", (npk, companyid,))
            for x in data:
                if x[10] == 0: # delete flag
                    row = {
                        'masterdocid': x[0],
                        'documentnumber': x[1],
                        'companyid': x[2],
                        'divisionid': x[3],
                        'departmentid': x[4],
                        'isprint': x[5],
                        'name': x[6],
                        'desc': x[7],
                        'version': x[8],
                        'status': x[9],
                        'createddate': x[12],
                        'auth': x[15],
                        'layout': x[16],
                        'signature': x[17],
                        'activeversiondocument': x[18],
                    }
                    result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)


    def readone_document(self, key):
        result = None
        message = ""
        try:
            data, message = super().readone(key)
            if len(data) > 0:
                result = {
                    'masterdocid': data[0],
                    'documentnumber': data[1],
                    'companyid': data[2],
                    'divisionid': data[3],
                    'departmentid': data[4],
                    'isprint': data[5],
                    'name': data[6],
                    'desc': data[7],
                    'version': data[8],
                    'status': data[9],
                    'createddate': data[12],
                    'auth': data[15],
                    'layout': data[16],
                    'signature': data[17],
                    'activeversiondocument': data[18],
                }
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)


    def update_activeversion(self, data):
        try:
            query = "UPDATE %s SET activeversiondocument=?, modifby=?, modifdate=? WHERE masterdocid=?" % (self.__tablename__)
            self.execute(query, (data["activeversiondocument"],data["modifby"], data["modifdate"], data["masterdocid"],))

            self.__connection__.commit()
            return(True, "success")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))


    def delete_document(self, masterdocid):
        try:
            query = f'''select a.* from requestapproval a where a.masterdocid=?'''
            data, message = self.execute(query, (masterdocid, ))

            if len(data) == 0:
                result, message = super().delete_flag(masterdocid)
                return(True, "success")
            else:
                return(False, "You can't delete Document that is already being used!")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))