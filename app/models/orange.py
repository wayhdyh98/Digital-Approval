from app.models.base import BaseTable

class OrangeData(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmds'
        self.__tablename__ = 'MPMDS_ORANGE_DATA'
        super().__init__()


    def list_pic(self, companyid, divisionid):
        result = []
        message = ""
        try:
            data, message = super().list()
            for x in data:
                # if companyid == x[0] and divisionid == x[6]:
                if divisionid == x[6]:
                    row = {
                        'companyid': x[0],
                        'employeeid': x[1],
                        'displayname': f'''{str(x[1]).zfill(5)} - {x[2]}''',
                        'gradeid': x[3],
                        'internaltitle': x[4],
                        'companyoffice': x[5],
                        'divisionid': x[6],
                        'divisionname': x[7],
                        'departmentid': x[8],
                        'departmentname': x[9],
                    }
                    result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)
    

    # def list_pic(self, companyid, divisionid):
    #     result = []
    #     message = ""
    #     try:
    #         query = "select a.* from %s a " \
    #         "left join mpmit_pic b on RIGHT('00000'+CAST(ISNULL(a.CODE ,0) AS VARCHAR(5)),5) = b.NPK " \
    #         "where b.email is not null" % (self.__tablename__)
    #         data, message = self.execute(query, ())
    #         for x in data:
    #             # if companyid == x[0] and divisionid == x[6]:
    #             if divisionid == x[6]:
    #                 row = {
    #                     'companyid': x[0],
    #                     'employeeid': x[1],
    #                     'displayname': x[2],
    #                     'gradeid': x[3],
    #                     'internaltitle': x[4],
    #                     'companyoffice': x[5],
    #                     'divisionid': x[6],
    #                     'divisionname': x[7],
    #                     'departmentid': x[8],
    #                     'departmentname': x[9],
    #                 }
    #                 result.append(row)
    #     except Exception as e:
    #         print(str(e))
    #         result = None
    #         message = str(e)

    #     return (result, message)