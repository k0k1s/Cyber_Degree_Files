from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time

key = b'This is a key!!!'  # 16 bytes for AES-128
cipher = AES.new(key, AES.MODE_ECB)

# Plaintext
plaintext = b'This is a secret'  # Must be padded to a multiple of 16 bytes
padded_plaintext = pad(plaintext, AES.block_size)

# Encrypt
start_encrypt = time.time()
ciphertext = cipher.encrypt(padded_plaintext)
end_encrypt = time.time()
encrypt_time = end_encrypt - start_encrypt

print(f'Ciphertext (AES): {ciphertext}')
print(f'Encryption Time: {encrypt_time:.6f} seconds')

# Decrypt
cipher_decrypt = AES.new(key, AES.MODE_ECB)

start_decrypt = time.time()
decrypted_padded_plaintext = cipher_decrypt.decrypt(ciphertext)
decrypted_plaintext = unpad(decrypted_padded_plaintext, AES.block_size)
end_decrypt = time.time()
decrypt_time = end_decrypt - start_decrypt

print(f'Decrypted Plaintext (AES): {decrypted_plaintext.decode("utf-8")}')
print(f'Decryption Time: {decrypt_time:.6f} seconds')
