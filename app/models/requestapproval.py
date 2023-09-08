from app.models.base import BaseTable

class RequestApproval(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmds'
        self.__tablename__ = 'requestapproval'
        super().__init__()


    def insert_data(self, data):
        try:
            new_id, message = self.new_id()

            query = "INSERT INTO %s(requestapprovalid, masterdocid, [desc], name, statusrequest, picrequester, deleteflag, createdby, createddate, modifby, modifdate, activeversiondocument) VALUES(%s)" % (self.__tablename__, "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?")
            self.execute(query, (new_id, data["documentid"], data["[desc]"], data["name"], data["statusrequest"], data["picrequester"], data["deleteflag"], data["createdby"], data["createddate"], data["modifby"], data["modifdate"], data["activeversiondocument"]))

            self.__connection__.commit()

            return(new_id, "success")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))

    
    def select_request(self, requestapprovalid):
        result = {}
        message = ""
        try:
            query = "select " \
                "CONCAT(m.documentnumber, '-', m.companyid, '-', r.requestapprovalnumber) requestapprovalnumber," \
                "r.requestapprovalid, r.masterdocid, r.name, r.[desc], r.statusrequest, r.picrequester, r.deleteflag, " \
                "r.activeversiondocument, r.layoutdocument from %s r " \
                "left join masterdocument m on r.masterdocid = m.masterdocid " \
                "where r.requestapprovalid=%s " % (self.__tablename__, "?")
            data, message = self.execute(query, (requestapprovalid,))
            for x in data:
                result = {
                    'requestapprovalnumber': x[0],
                    'requestapprovalid': x[1],
                    'masterdocid': x[2],
                    'name': x[3],
                    'desc': x[4],
                    'statusrequest': x[5],
                    'picrequester': x[6],
                    'deleteflag': x[7],
                    'activeversiondocument': x[8],
                    'layoutdocument': x[9]
                }
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)

    
    def update_requestapproval(self, data, requestapprovalid):
        try:
            field = [x+"=?" for x in data]
            field = ",".join(field)

            params = [data[x] for x in data]
            params.append(requestapprovalid)

            query = "UPDATE %s SET %s WHERE requestapprovalid=?" % (self.__tablename__, field)
            self.execute(query, tuple(params))

            self.__connection__.commit()
            return(True, "success")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))
    