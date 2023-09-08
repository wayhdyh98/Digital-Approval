from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from hashlib import md5, sha256
import binascii

class SecurityKey():
    def generate_basekey(self):
        new_key = RSA.generate(2048)
        return new_key   
    
    def generate_loginkey(self, key):
        private_key = key.exportKey("PEM")
        public_key = key.publickey().exportKey("PEM")
        return (private_key, public_key)

    def generate_secretkey(self, pb_key, text):
        key = RSA.import_key(pb_key)
        cipher = PKCS1_OAEP.new(key)
        ciphertext = cipher.encrypt(text.encode('utf-8'))
        hexlify_ciphertext = binascii.hexlify(ciphertext)
        return hexlify_ciphertext.decode('utf-8')

    def encrypt_md5(self, data, docid):
        data = f'{data}:{docid}'
        data = md5(data.encode('utf-8')).hexdigest()
        return data
    
    def encrypt_md5_profile(self, data):
        data = md5(data.encode('utf-8')).hexdigest()
        return data
    
    def encrypt_test(self, data, docid):
        data = f'{data}:{docid}'
        data = sha256(data.encode('utf-8')).hexdigest()
        return data

    def unlock_secretkey(self, pk_key, data):
        unhexlify_ciphertext = binascii.unhexlify(data.encode('utf-8'))
        key = RSA.import_key(pk_key)
        cipher = PKCS1_OAEP.new(key)
        plaintext = cipher.decrypt(unhexlify_ciphertext)
        return plaintext.decode('utf-8')