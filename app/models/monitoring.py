from app.models.base import BaseQuery

class Monitoring(BaseQuery):

    def __init__(self):
        self.__database__ = 'mpmds'
        super().__init__()


    def document(self, npk, period, status):
        # status approval (1 - approved, 0 - rejected)
        result = []
        try:
            data, message = self.callproc("EXEC MPMDS_FILTER_APPROVEMONITORING_ALL ?, ?, ?", (npk, int(period), int(status), ))
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
                    'descreption': x[9],
                    'createdby': x[10],
                    'createddate': x[11],
                    'statusrequest': x[12],
                    'picid': x[13],
                    'piclevel': x[14],
                    'picsublevel': x[15],
                    'picname': x[16],
                    'statusapprove': x[17],
                    'modifdate': x[18],
                    'lastapproval': x[19],
                    'division': x[20],
                }
                result.append(row)
            return (result, message)
        except Exception as e:
            print(str(e))
            return (None, str(e))


    def trackingworkflow(self, npk, period, status):
        # status approval (0 - pembuat, 1 - pemilik, 2 - pengapprove)
        result = []
        try:
            data, message = self.callproc("EXEC MPMDS_FILTER_TRACKINGWORKFLOW ?, ?, ?", (npk, int(period), int(status), ))
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
                    'descreption': x[9],
                    'createdby': x[10],
                    'createddate': x[11],
                    'statusrequest': x[12],
                    'picid': x[13],
                    'piclevel': x[14],
                    'picsublevel': x[15],
                    'picname': x[16],
                    'statusapprove': x[17],
                    'modifdate': x[18],
                    'requestapprovalauthenticationid': x[19],
                    'lastapproval': x[20],
                    'division': x[21],
                }
                result.append(row)
            return (result, message)
        except Exception as e:
            print(str(e))
            return (None, str(e))


    def trackingworkflow_header(self, npk, period, status):
        # status approval (0 - pembuat, 1 - pemilik, 2 - pengapprove)
        result = []
        try:
            data, message = self.callproc("EXEC MPMDS_FILTER_TRACKINGWORKFLOW_HEADER ?, ?, ?", (npk, int(period), int(status), ))
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
                    'descreption': x[9],
                    'createdby': x[10],
                    'createddate': x[11],
                    'statusrequest': x[12],
                    'picid': x[13],
                    'piclevel': x[14],
                    'picsublevel': x[15],
                    'picname': x[16],
                    'statusapprove': x[17],
                    'modifdate': x[18],
                    'requestapprovalauthenticationid': x[19],
                    'lastapproval': x[20],
                    'division': x[21],
                }
                result.append(row)
            return (result, message)
        except Exception as e:
            print(str(e))
            return (None, str(e))



    def viewtracking(self, requestapprovalid, status):
        # status approval (0 - document part, 1 - question part, 2 - workflow part)
        result = []
        try:
            data, message = self.callproc("EXEC MPMDS_DETAIL_TRACKINGDOC ?, ?", (requestapprovalid, int(status), ))
            for x in data:
                if status == 0:
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
                        'statusrequest': x[12],
                        'nosig': x[13],
                        'picrequester': x[14],
                        'activeversiondocument': x[15],
                        'contentorigin': x[16],
                        'layoutdocument': x[17],
                        'years': x[18],
                        'picid': x[19],
                        'picname': x[20],
                        'divisi': x[21],
                        'divisiid': x[22],
                        'layout': x[23],
                    }
                    result = row
                elif status == 1:
                    row = {
                        'requestapprovalanswerid': x[0],
                        'requestapprovalid': x[1],
                        'designdocumentquestionid': x[2],
                        'answer': x[3],
                        'grouptitle': x[4],
                        'questiontype': x[5],
                        'question': x[6],
                        'questioncondition': x[7],
                        'questiontypecomponent': x[8],
                        'mandatory': x[9],
                        'designdocumentgroupquestionid': x[10],
                        'sectiontype': x[11],
                        'answergroupid': x[12],
                        'codevalue': x[13],
                    }
                    result.append(row)
                else:
                    row = {
                        'requestapprovalauthenticationid': x[0],
                        'requestapprovalid': x[1],
                        'masterapproveid': x[2],
                        'picid': x[3],
                        'piclevel': x[4],
                        'picsublevel': x[5],
                        'picname': x[6],
                        'mandatory': x[7],
                        'createdby': x[8],
                        'createddate': x[9],
                        'modifdate': x[10],
                        'commentapprove': x[11],
                        'modifby': x[12],
                        'pictype': x[13],
                        'statusapprove': x[14],
                        'divisi': x[15],
                        'nama': x[16],
                        'email': x[17],
                        'ttd': x[18],
                        'publickey': x[19],
                        'descriptionapprovaltitle': x[20],
                        'statusapprovetext': x[21],
                    }
                    result.append(row)
            return (result, message)
        except Exception as e:
            print(str(e))
            return (None, str(e))