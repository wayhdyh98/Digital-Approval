from app.models.base import BaseTable

class RequestApprovalAuthentication(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmds'
        self.__tablename__ = 'requestapproval_authentication'
        super().__init__()


    def insert_auth(self, data):
        try:
            new_id, message = self.new_id()

            query = "INSERT INTO %s(requestapprovalauthenticationid, requestapprovalid, masterapproveid, pictype, picid, piclevel, picsublevel, picname, mandatory, publickey, createdby, createddate) VALUES(%s)" % (self.__tablename__, "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?")
            self.execute(query, (new_id, data["requestapprovalid"], data["masterapproveid"], data["pictype"], data["picid"], data["piclevel"], data["picsublevel"], data["picname"], data["mandatory"], data["publickey"], data["createdby"], data["createddate"],))

            self.__connection__.commit()

            return(new_id, "success")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))


    def delete_data(self, requestapprovalid):
        try:          
            # delete data
            query = "delete a from %s a " \
                    "left join masterapproval b on a.masterapproveid = b.masterapproveid " \
                    "where a.requestapprovalid = ? and b.picid = ''" % (self.__tablename__)
            self.execute(query, (requestapprovalid,))
            
            self.__connection__.commit()
            return(True, "")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))


    def check_auth(self, masterapproveid, requestapprovalid):
        try:
            result = []
            query = "SELECT requestapprovalauthenticationid, requestapprovalid, masterapproveid " \
            "FROM %s WHERE masterapproveid = ? and requestapprovalid = ?" % (self.__tablename__)
            data, message = self.execute(query, (masterapproveid, requestapprovalid,))

            for x in data:
                row = {
                    'requestapprovalauthenticationid': x[0],
                    'requestapprovalid': x[1],
                    'masterapproveid': x[2],
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)

    
    def check_statusapprove(self, requestapprovalauthenticationid, status):
        try:
            result = []
            query = "SELECT statusapprove " \
            "FROM %s WHERE requestapprovalauthenticationid = ? and statusapprove = ?" % (self.__tablename__)
            data, message = self.execute(query, (requestapprovalauthenticationid, status))

            for x in data:
                row = {
                    'statusapprove': x[0],
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)


    def update_auth(self, data, requestapprovalauthenticationid):
        try:
            query = "UPDATE %s SET picid=?, picname=?, modifby=?, modifdate=? WHERE requestapprovalauthenticationid=?" % (self.__tablename__)
            self.execute(query, (data["picid"], data["picname"], data["modifby"], data["modifdate"], requestapprovalauthenticationid,))

            self.__connection__.commit()
            return(True, "success")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))


    def get_authdata(self, requestapprovalid):
        try:
            result = []
            query = "select a.masterapproveid, a.picid, a.picname from %s a " \
                    "left join masterapproval b on a.masterapproveid = b.masterapproveid " \
                    "where a.requestapprovalid = ? and b.picid = ''" % (self.__tablename__)
            data, message = self.execute(query, (requestapprovalid,))

            for x in data:
                row = {
                    'masterapproveid': x[0],
                    'picid': x[1],
                    'picname': x[2],
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)

    
    def update_statusapprove(self, data, requestapprovalauthenticationid):
        try:
            print(data)
            query = "UPDATE %s SET statusapprove=?, commentapprove=?, modifby=?, modifdate=? WHERE requestapprovalauthenticationid=?" % (self.__tablename__)
            self.execute(query, (data["statusapprove"], data["commentapprove"], data["modifby"], data["modifdate"], requestapprovalauthenticationid,))

            self.__connection__.commit()
            return(True, "success")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))
    