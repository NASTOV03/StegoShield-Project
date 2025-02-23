import base64
from Crypto.Cipher import AES

# AES Unpadding
def unpad(text):
    return text[:-ord(text[-1])]

# AES-256 Decryption
def decrypt_message(encrypted_message, key):
    try:
        key = key.ljust(32)[:32].encode()
        cipher = AES.new(key, AES.MODE_ECB)
        return unpad(cipher.decrypt(base64.b64decode(encrypted_message)).decode())
    except Exception:
        return "Invalid key or corrupted file!"
