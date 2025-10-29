import base64
from Crypto.Cipher import AES

# AES Padding
def pad(text):
    return text + (16 - len(text) % 16) * chr(16 - len(text) % 16)

# AES-256 Encryption
def encrypt_message(message, key):
    key = key.ljust(32)[:32].encode()
    cipher = AES.new(key, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(pad(message).encode())).decode()
