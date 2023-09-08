from app.models.base import BaseTable

class Submission(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmds'
        self.__tablename__ = ''
        super().__init__()


    def submissions(self, npk, status):
        # status approval (0 - draft, 1 - sent)
        result = []
        try:
            data, message = self.callproc("EXEC MPMDS_SUBMISSION_FILTER ?, ?", (npk, int(status), ))
            for x in data:
                row = {
                    'requestapprovalid': x[0],
                    'requestapprovalnumber': x[1],
                    'masterdocid': x[2],
                    'documentnumber': x[3],
                    'requestid': x[4],
                    'companyid': x[5],
                    'divisionid': x[6],
                    'departmentid': x[7],
                    'name': x[8],
                    'desc': x[9],
                    'createdby': x[10],
                    'createddate': x[11],
                    'statusrequest': x[12]
                }
                result.append(row)
            return (result, message)
        except Exception as e:
            print(str(e))
            return (None, str(e))