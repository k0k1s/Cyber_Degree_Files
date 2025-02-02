from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time

# Generate RSA keys
key = RSA.generate(2048)
public_key = key.publickey()
private_key = key

# Message
message = b'The coldest story ever told Somewhere far along this road He lost his soul to a woman so heartless'

# Encrypt
start_encrypt = time.time()
cipher_rsa = PKCS1_OAEP.new(public_key)
encrypted = cipher_rsa.encrypt(message)
end_encrypt = time.time()
encrypt_time = end_encrypt - start_encrypt

print(f'Encrypted Message (RSA): {encrypted}')
print(f'Encryption Time: {encrypt_time:.6f} seconds')

# Decrypt
start_decrypt = time.time()
cipher_rsa_decrypt = PKCS1_OAEP.new(private_key)
decrypted = cipher_rsa_decrypt.decrypt(encrypted)
end_decrypt = time.time()
decrypt_time = end_decrypt - start_decrypt

print(f'Decrypted Message (RSA): {decrypted.decode("utf-8")}')
print(f'Decryption Time: {decrypt_time:.6f} seconds')
