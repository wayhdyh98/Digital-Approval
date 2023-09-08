from app.models.base import BaseTable

class Division(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmds'
        self.__tablename__ = 'MPMDS_ORANGE_DIVISION'
        super().__init__()


    def list_division(self, companyid):
        result = []
        message = ""
        try:
            data, message = super().list()
            for x in data:
                # if companyid == x[0]:
                row = {
                    'companyid': x[0],
                    'divisionid': x[1],
                    'divisionname': x[2]
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)