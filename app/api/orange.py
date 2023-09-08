import requests
from bs4 import BeautifulSoup
import app.config as conf

class OrangeAPI():

    def __init__(self):
        pass


    def user_validation(self, userid, password):
        url = conf.ORANGE_API_USERVALIDATION_ENDPOINT
        headers = {'Accept':'*/*', 'Content-Type':'application/x-www-form-urlencoded', 'SOAPAction':''}
        body = """
        <Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
            <Body>        
                <isUserValid xmlns="http://srvc.hrbase.sps.com">
                    <userId>%s</userId>
                    <password>%s</password>
                </isUserValid>
            </Body>
        </Envelope>
        """ % (userid, password, )
        response = requests.post(url, data=body, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "xml")
            userValidReturns = soup.find("isUserValidReturn")
            for data in userValidReturns:
                if data.get_text() == "TRUE":
                    return True
            return False
        return False