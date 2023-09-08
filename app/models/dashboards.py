from app.models.base import BaseQuery

class Dashboards(BaseQuery):

    def __init__(self):
        self.__database__ = 'mpmds'
        super().__init__()


    def total_dashboards(self, npk):
        result = []
        try:
            data, message = self.callproc("EXEC MPMDS_DASHBOARD_TOTALDOC ?", (npk, ))
            for x in data:
                row = {
                    'totalapprove': x[0],
                    'totalpending': x[1]
                }
                result = row
            return (result, message)
        except Exception as e:
            print(str(e))
            return (None, str(e))