from app.models.base import BaseTable

class Approval(BaseTable):

    def __init__(self):
        self.__database__ = 'mpmds'
        self.__tablename__ = 'masterapproval'
        self.__primarykey__ = "masterapproveid"
        super().__init__()


    def list_approval(self, documentid):
        result = []
        message = ""
        try:
            query = '''
                select
                    ma.masterapproveid,
                    ma.masterdocid,
                    ma.pictype,
                    ma.picid,
                    ma.piclevel,
                    ma.picsublevel,
                    ma.mandatory,
                    ma.descriptionapprovaltitle,
                    o.VALUE picname
                from
                    %s ma
                left join MPMDS_ORANGE_EMPLOYEE o ON
                    RIGHT('00000'+CAST(ISNULL(ma.picid ,0) AS VARCHAR(5)),5) = RIGHT('00000'+CAST(ISNULL(o.CODE ,0) AS VARCHAR(5)),5)
                where
                    masterdocid = %s
                order by
                    piclevel,
                    picsublevel
            ''' % (self.__tablename__, "?")
            
            
            #"select ma.masterapproveid, ma.masterdocid, ma.pictype, " \
            #    "ma.picid, ma.piclevel, ma.picsublevel, ma.mandatory, ma.descriptionapprovaltitle, " \
            #    "o.VALUE picname " \
            #    "from %s ma " \
            #    "left join MPMDS_ORANGE_EMPLOYEE o ON o.CODE = ma.picid " \
            #    "where masterdocid=%s " \
            #    "order by piclevel, picsublevel" % (self.__tablename__, "?")
            data, message = self.execute(query, (documentid, ))
            for x in data:
                row = {
                    'masterapproveid': x[0],
                    'masterdocid': x[1],
                    'pictype': x[2], # 0 - pemohon, 1 - mengetahui, 2 - menyetujui
                    'pictypetext': "Pemohon" if x[2] == 0 else "Mengetahui" if x[2] == 1 else "Menyetujui",
                    'picid': x[3],
                    'piclevel': x[4],
                    'picsublevel': x[5],
                    'mandatory': x[6], # 0 - not mandatory, 1 - mandatory
                    'mandatorytext': "Not Mandatory" if x[6] == 0 else "Mandatory",
                    'description': x[7],
                    'picname': x[8]
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)


    def list_approval_parent(self, documentid):
        result = []
        message = ""
        try:
            query = "select ma.pictype, ma.picid, ma.piclevel, o.VALUE picname " \
            "from %s ma left join MPMDS_ORANGE_EMPLOYEE o ON RIGHT('00000'+CAST(ISNULL(ma.picid ,0) AS VARCHAR(5)),5) = RIGHT('00000'+CAST(ISNULL(o.CODE ,0) AS VARCHAR(5)),5) " \
            "where masterdocid=%s order by ma.pictype, ma.piclevel, ma.picsublevel, o.VALUE" % (self.__tablename__, "?")
            data, message = self.execute(query, (documentid, ))
            for x in data:
                row = {
                    'pictype': x[0],
                    'picid': x[1],
                    'piclevel': x[2],
                    'picname': x[3]
                }
                result.append(row)
        except Exception as e:
            print(str(e))
            result = None
            message = str(e)

        return (result, message)
    

    def get_maxlevel(self, documentid):
        result = 0
        message = ""
        try:
            query = "select max(piclevel) from %s where masterdocid=%s" % (self.__tablename__, "?")
            data, message = self.execute(query, (documentid, ))
            if data == None:
                result = 0
            else:
                for x in data:
                    result = x[0]
        except Exception as e:
            print(str(e))
            result = 0
            message = str(e)

        return (result, message)


    def get_maxsublevel(self, documentid, piclevel):
        result = 0
        message = ""
        try:
            query = "select max(picsublevel) from %s where masterdocid=%s and piclevel=%s" % (self.__tablename__, "?", "?")
            data, message = self.execute(query, (documentid, piclevel, ))
            if data == None:
                result = 0
            else:
                for x in data:
                    result = x[0]
        except Exception as e:
            print(str(e))
            result = 0
            message = str(e)
            
        return (result, message)