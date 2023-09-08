import email, smtplib, ssl
from pathlib import Path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import app.config as conf

config = conf.MAIL_ACCOUNT[0]["default"]
smtp_server = config["SERVER"]
smtp_port = config["SMTP_PORT"]  # For starttls
sender_email = config["ACCOUNT"]
username = config["USERNAME"]
password = config["PASSWORD"]

# send email
def send_email(to, cc, subject, message_email, files=[]):
    context = ssl.create_default_context()
    
    # Try to log in to server and send email
    try:
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["Cc"] = cc
        message["To"] = to
        message["Subject"] = subject
        
        # Add body to email
        message.attach(MIMEText(message_email, "html"))

        # attachment
        for path in files:
            try:
                part = MIMEBase('application', "octet-stream")
                with open(path['pathname'], 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename={}'.format(path['filename']))
                message.attach(part)
            except Exception as e:
                pass
            
        text_email = message.as_string()
        
        # set list address email
        list_address_email_to = to.split(',')
        list_address_email_cc = cc.split(',')
        list_address_email = list_address_email_to + list_address_email_cc
        
        # start
        server = smtplib.SMTP(smtp_server,smtp_port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(username, password)
        
        # send email
        server.sendmail(sender_email, list_address_email, text_email)
        
        # quit
        server.quit() 
        
        return (True, 'success')
    except Exception as e:
        # Print any error messages to stdout
        print(e) 
        return (False, e)