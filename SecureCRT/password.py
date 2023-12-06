from Crypto.Cipher import Blowfish
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# 生成随机的密钥
key = get_random_bytes(16)

# 创建 Blowfish 加密器对象
cipher = Blowfish.new(key, Blowfish.MODE_ECB)

# 要加密的数据
data = b"Hello, Blowfish!"

# 加密
cipher_text = cipher.encrypt(pad(data, Blowfish.block_size))
print("Cipher text:", cipher_text)

# 解密
decipher = Blowfish.new(key, Blowfish.MODE_ECB)
plain_text = unpad(decipher.decrypt(cipher_text), Blowfish.block_size)
print("Plain text:", plain_text.decode("utf-8"))
