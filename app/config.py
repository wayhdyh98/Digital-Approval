import logging

TIMEZONE = 'Asia/Jakarta'

# DEBUG can only be set to True in a development environment for security reasons
DEBUG = True

# user session dummy
DEV_MODE = False
USER_DUMMY = {
    "userid": "123456789",
    "username": "rocket",
    "uniqueid": "R0ck3t",
    "name": "Rocket System",
    "email": "rocket.system@gmail.com",
    "secretkey": "123456789",
    "isadmin": 0,
    "isactive": 1,
    "isapprove": 1
}

# secret key for generating tokens
SECRET_KEY = "go-rocket-2021"

# Admin credentials
ADMIN_CREDENTIALS = ('admin', 'Pa$$word')

# Configuration of a Email account for sending and receiving mails
MAIL_ACCOUNT = [
    {
        "default": {
            "ACCOUNT": "rocket@mpm-motor.com",
            "SERVER": "mail.mpm-motor.com",
            "IMAP_PORT": 993,
            "SMTP_PORT": 587,
            "USE_TLS": False,
            "USE_SSL": True,
            "USERNAME": "rocket@mpm-motor.com",
            "PASSWORD": "E<3qs=4V"
        }
        # "default": {
        #     "ACCOUNT": "mpm.system@mpm-motor.com",
        #     "SERVER": "mail.mpm-motor.com",
        #     "IMAP_PORT": 993,
        #     "SMTP_PORT": 587,
        #     "USE_TLS": False,
        #     "USE_SSL": True,
        #     "USERNAME": "autoreply",
        #     "PASSWORD": "JLBFxUX5"
        # }
    }
]

# Configuration of a Database account
DATABASE_ACCOUNT = {
        "mpmds": {
            "DRIVER": "{ODBC Driver 18 for SQL Server}",
            # "SERVER": "mml-lsn-dbaxex.mpm-motor.com",
            "SERVER": "10.10.108.49",
            "PORT": 1443,
            "user": "appreader",
            "password": "Simpang4244",
            "database": "MPMDS",
        },
        "mpmit": {
            "DRIVER": "{ODBC Driver 18 for SQL Server}",
            # "SERVER": "mml-lsn-dbaxex.mpm-motor.com",
            "SERVER": "10.10.108.49",
            "PORT": 1443,
            "user": "appreader",
            "password": "Simpang4244",
            "database": "MPMIT",
        },
    }

# Number of times a password is hashed
BCRYPT_LOG_ROUNDS = 12

LOG_LEVEL = logging.DEBUG
LOG_FILENAME = 'activity.log'
LOG_MAXBYTES = 1024
LOG_BACKUPS = 2

# API ENDPOINT
ORANGE_API_USERVALIDATION_ENDPOINT = "https://hr.mpm-motor.com:8080/MPM/services/UserValidationSrvcs?wsdl"
QRCODE_API_ENDPOINT = "https://apps.mpm-motor.com/it/mpmqrcode/Home?d="

# EMAIL URL ENDPOINT
# EMAIL_PATH = "https://go.mpm-motor.com/approvalonline/monitoring/api/1.0/page/monitoringbp.linksess"
# EMAIL_PATH = "http://10.10.101.30:7005/monitoring/api/1.0/page/monitoringbp.linksess"
EMAIL_PATH = "http://10.10.101.30:7005/monitoring/viewtracking/validation"