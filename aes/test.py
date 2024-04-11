# key = b'Secloud@DeviceSn'
# plain_text = b'sn12345678abc'


from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

def encrypt(plain_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plain_text = pad(plain_text.encode('utf-8'), AES.block_size)
    cipher_text = cipher.encrypt(padded_plain_text)
    return base64.b64encode(cipher_text)

key = b'Sexxxxx@xxxxxxxx'
plain_text = 'Hello, world!'
cipher_text = encrypt(plain_text, key)
print("Cipher text:", cipher_text.decode('utf-8'))
