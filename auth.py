import hashlib
import os

def hash_password(password):

    salt = os.urandom(32)

    passwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return passwd_hash.hex(), salt.hex()

def verify_password(stored_password_hex, stored_salt_hex, provided_password):
    salt = bytes.fromhex(stored_salt_hex)
    passwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return passwd_hash.hex() == stored_password_hex