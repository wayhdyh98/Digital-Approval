from app.models.base import BaseTable

class Client(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmit'
        self.__tablename__ = 'MPMIT_PIC'
        super().__init__()

    
    def list_client(self):
        result = []
        message = ""
        try:
            data, message = super().list()
            for x in data:
                row = {
                    'npk': x[0],
                    'name': x[1],
                    'email': x[2],
                    'companyid': x[3],
                    'divisionid': x[4],
                    'statuspic': x[5],
                    'alias': x[6],
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)