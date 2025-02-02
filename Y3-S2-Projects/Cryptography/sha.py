import hashlib
import time

# Plaintext
plaintext = b'This is a secret'

# Hash the plaintext
start_hash = time.time()
hash_object = hashlib.sha256(plaintext)
hex_dig = hash_object.hexdigest()
end_hash = time.time()
hash_time = end_hash - start_hash

print(f'SHA-256 Hash: {hex_dig}')
print(f'Hashing Time: {hash_time:.6f} seconds')
