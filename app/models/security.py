from app.models.base import BaseTable

class Security(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmit'
        self.__tablename__ = 'mpmit_pic'
        super().__init__()


    def insert_loginkey(self, data, npk):
        try:
            field = [x+"=?" for x in data]
            field = ",".join(field)

            params = [data[x] for x in data]
            params.append(npk)

            query = "UPDATE %s SET %s WHERE npk=?" % (self.__tablename__, field)
            self.execute(query, tuple(params))

            self.__connection__.commit()
            return(True, "success")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))
    
    
    def check_loginkey(self, npk):
        result = {}
        message = ""
        try:
            query = "select " \
                "a.private_key, a.public_key, a.secret_key " \
                "from %s a " \
                "where a.npk=%s " % (self.__tablename__, "?")
            data, message = self.execute(query, (npk, ))
            for x in data:
                result = {
                    'private_key': x[0],
                    'public_key': x[1],
                    'secret_key': x[2]
                }
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)
    

    def check_email_in_mpmit_pic(self, npk):
        result = []
        message = ""
        try:
            query = "select mp.email " \
            "from %s mp " \
            "where mp.npk=%s" % (self.__tablename__, "?")
            data, message = self.execute(query, (npk, ))
            for x in data:
                row = {
                    'email': x[0],
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)


    def createbase_secretkey(self, timespan):
        new_id, message = self.new_id()
        base_secretkey = ''.join((new_id, timespan))
        return base_secretkey

        