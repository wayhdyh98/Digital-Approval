import xdrlib
from app.models.base import BaseQuery

class User(BaseQuery):

    def __init__(self):
        self.__database__ = 'mpmds'
        super().__init__()


    def profile(self, npk):
        result = []
        try:
            result, message = self.callproc("EXEC MPMIT_DATAUSER ?", (npk, ))
            person = {}
            for x in result:
                person = {
                    'npk': x[0],
                    'name':x[1],
                    'division':x[2],
                    'company':x[3],
                    'department':x[4],
                    'divisionid': x[5],
                    'departmentid': x[6],
                    'email':x[7],
                    'position':x[9],
                    'ttd': x[10],
                    'publickey':x[11]
                }
            return (person, message)
        except Exception as e:
            print(str(e))
            return (None, str(e))


    def insert_ttd(self, data, npk):
        try:
            query = "UPDATE mpmit.dbo.MPMIT_PIC SET ttd=?, modifby=?, modifdate=? WHERE npk=?"
            self.execute(query, (data["ttd"], data["modifby"], data["modifdate"], npk,))

            self.__connection__.commit()
            return(True, "success")
        except Exception as e:
            self.__connection__.rollback()
            print(str(e))
            return (False, str(e))