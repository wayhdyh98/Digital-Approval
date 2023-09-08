from cryptography.fernet import Fernet
from app.config import SECRET_KEY
import json
import base64

def encrypt_parameter_query(data):
    key = base64.urlsafe_b64encode(SECRET_KEY.encode('utf-8').ljust(32, b'\0'))
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt((json.dumps(data)).encode())
    return (encrypted_text)


def decrypt_parameter_query(text):
    key = base64.urlsafe_b64encode(SECRET_KEY.encode('utf-8').ljust(32, b'\0'))
    cipher_suite = Fernet(key)
    # res = bytes(text, 'utf-8')
    decoded_text = cipher_suite.decrypt(text).decode('utf-8')
    return (json.loads(decoded_text))