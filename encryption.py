import base64, os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def generateKeyFromPassword(password_provided):
    password = password_provided.encode()
    salt = b'sampyisgoodthing'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt(content, key):
    message = content.encode()
    f = Fernet(key)
    encrypted = f.encrypt(message)
    return encrypted

def decrypt(content, key):
    message = content

    f = Fernet(key)
    decrypted = f.decrypt(message)
    return decrypted

