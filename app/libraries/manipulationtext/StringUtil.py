from app.libraries.session import security as SecurityBase
from app.models.security import Security
from app.models.monitoring import Monitoring
from app.models.requestapproval_authentication import RequestApprovalAuthentication
from bs4 import BeautifulSoup

def findandreplace(strText, findText, replaceText, position):
    find = strText.find(findText)
    # If find is not -1 we have found at least one match for the substring
    i = find != -1
    # loop util we find the word or we find no match
    while find != -1 and i != int(position):
        # find + 1 means we start searching from after the last match
        find = strText.find(findText, find + 1)
        i += 1
    # If i is equal to picsublevel we found word match so replace
    if i == int(position):
        strText = strText[:find] + replaceText + strText[find+len(findText):]
    return strText

def replacesignature(layoutdocument, piclevel, picsublevel, masterdocid):
    securitymodel = Security()
    requestapprovalauth = RequestApprovalAuthentication()
    securitybase = SecurityBase.SecurityKey()

    soup = BeautifulSoup(layoutdocument)
    if picsublevel > 1:
        for img in soup.findAll('img'):
            if img.has_attr('data-piclevel'):
                for num in range(1, picsublevel, 1):
                    if int(img['data-piclevel']) == piclevel and int(img['data-picsublevel']) == num:
                        result, message = requestapprovalauth.check_statusapprove(img['data-authid'], 1)
                        if len(result) > 0:
                            result2, message2 = securitymodel.check_loginkey(img['data-picid'])
                            hashed_seckey = securitybase.encrypt_md5(result2['secret_key'], masterdocid)

                            ttd = f'https://apps.mpm-motor.com/it/mpmqrcode/Home?d={hashed_seckey}'
                            if int(img['data-nosig']) == 1:
                                ttd = img['data-ttd'] if img['data-ttd'] != "null" else ttd
                            img['src'] = ttd
                            
        layoutdocument = str(soup)

    soup = BeautifulSoup(layoutdocument)
    for img in soup.findAll('img'):
        if img.has_attr('data-piclevel'):
            # if int(img['data-piclevel']) != piclevel:
            if int(img['data-piclevel']) == piclevel and int(img['data-picsublevel']) == picsublevel:
                result, message = securitymodel.check_loginkey(img['data-picid'])
                hashed_seckey = securitybase.encrypt_md5(result['secret_key'], masterdocid)

                ttd = f'https://apps.mpm-motor.com/it/mpmqrcode/Home?d={hashed_seckey}'
                if int(img['data-nosig']) == 1:
                    ttd = img['data-ttd'] if img['data-ttd'] != "null" else ttd
                img['src'] = ttd      
    
    layoutdocument = str(soup)
    return layoutdocument

def previewSignature(layoutdocument, requestapprovalid, masterdocid):
    securitymodel = Security()
    monitoring = Monitoring()
    requestapprovalauth = RequestApprovalAuthentication()

    result, message = monitoring.viewtracking(requestapprovalid, 2)
    resultreject = [x for x in result if x['statusapprove'] == 2]

    securitybase = SecurityBase.SecurityKey()

    soup = BeautifulSoup(layoutdocument)

    for img in soup.findAll('img'):
        if img.has_attr('data-piclevel'):
            if len(resultreject) == 0:
                resultapprove, messageapprove = requestapprovalauth.check_statusapprove(img['data-authid'], 1)
                # # testing only
                # hs = securitybase.encrypt_md5("4bb8de3fa3cc7a1f9f968dfc9ec4f41fd3a788aacfda041a069fa101ba55954b7f57c59a7cd243f75fcf3017e8f2d98ae00dcf3030488b976799be70bbae5f37f93c9ef990d5cd9111faf60c538d6ee4e1b190ca65eaef669fa37bb68fdfdfa5d138b41e4ccfe7b5d69b210bab3a35c9743f6119a74be8c5981eb9e24f4a507fa940408b0671327dde3c5133bbc8490add3dbfe6e7e9024dace005f7b3d2f9443764c000e898d24436245def56aa355546f0480665e35fe329edb3e066db7de4812338dfd3560c221f5a4f058f2071324fd2a7e47a2b9f313c0aecb720c78a4e28f1bab7f747e6f5e6005d5a79bc8520e17473e71ed16dcdffc32fd2a1e1de9d", "00E6A316-1B11-4617-B229-0E0D7CC44523")
                # hashed = securitybase.encrypt_test("4bb8de3fa3cc7a1f9f968dfc9ec4f41fd3a788aacfda041a069fa101ba55954b7f57c59a7cd243f75fcf3017e8f2d98ae00dcf3030488b976799be70bbae5f37f93c9ef990d5cd9111faf60c538d6ee4e1b190ca65eaef669fa37bb68fdfdfa5d138b41e4ccfe7b5d69b210bab3a35c9743f6119a74be8c5981eb9e24f4a507fa940408b0671327dde3c5133bbc8490add3dbfe6e7e9024dace005f7b3d2f9443764c000e898d24436245def56aa355546f0480665e35fe329edb3e066db7de4812338dfd3560c221f5a4f058f2071324fd2a7e47a2b9f313c0aecb720c78a4e28f1bab7f747e6f5e6005d5a79bc8520e17473e71ed16dcdffc32fd2a1e1de9d", "00E6A316-1B11-4617-B229-0E0D7CC44523")
                # print(hs)
                # print(hashed)
                # img['src'] = "https://apps.mpm-motor.com/it/mpmqrcode/Home?d=5609e6d15f47a8ddca9faf1659daddd3"
                #
                if len(resultapprove) > 0:
                    result2, message2 = securitymodel.check_loginkey(img['data-picid'])
                    hashed_seckey = securitybase.encrypt_md5(result2['secret_key'], masterdocid)

                    ttd = f'https://apps.mpm-motor.com/it/mpmqrcode/Home?d={hashed_seckey}'
                    if int(img['data-nosig']) == 1:
                        ttd = img['data-ttd'] if img['data-ttd'] != "null" else ttd
                    img['src'] = ttd
            else:
                for x in resultreject:
                    if int(img['data-piclevel']) == x['piclevel']:
                        img['src'] = "https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg"          
                            
    layoutdocument = str(soup)
    return layoutdocument