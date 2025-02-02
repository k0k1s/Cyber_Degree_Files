# Import necessary libraries
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import psutil
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Function to get system metrics
def get_system_metrics():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    return cpu_usage, memory_info.percent

# Function to encrypt large messages in chunks using RSA
def encrypt_message(cipher, message):
    """Encrypt the message using the given cipher, handling large messages."""
    key_size = cipher._key.size_in_bytes()
    hash_size = 32  # SHA-256 hash size is 32 bytes
    chunk_size = key_size - 2 * hash_size - 2  # Maximum chunk size for RSA OAEP
    
    encrypted_chunks = []
    
    for i in range(0, len(message), chunk_size):
        chunk = message[i:i + chunk_size]
        encrypted_chunks.append(cipher.encrypt(chunk))
    
    return b''.join(encrypted_chunks)

# Function to measure RSA performance (encryption and decryption)
def measure_rsa_performance(key_size, plaintext):
    key = RSA.generate(key_size)
    public_key = key.publickey()
    private_key = key

    # Encrypt the message
    start_encrypt = time.time()
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted = encrypt_message(cipher_rsa, plaintext)
    end_encrypt = time.time()
    encrypt_time = end_encrypt - start_encrypt

    # Decrypt the message
    start_decrypt = time.time()
    cipher_rsa_decrypt = PKCS1_OAEP.new(private_key)
    decrypted = b''
    
    for i in range(0, len(encrypted), key_size // 8):
        chunk = encrypted[i:i + (key_size // 8)]
        decrypted += cipher_rsa_decrypt.decrypt(chunk)
    
    end_decrypt = time.time()
    decrypt_time = end_decrypt - start_decrypt

    return encrypt_time, decrypt_time, decrypted

# Function to generate test data
def generate_test_data(data_size, file_type='binary'):
    if file_type == 'binary':
        return os.urandom(data_size)
    elif file_type == 'text':
        return b'This is a test string. ' * (data_size // 25)
    elif file_type == 'json':
        return bytes('{"key": "value"}' * (data_size // 15), 'utf-8')
    elif file_type == 'csv':
        return bytes('field1,field2\n' + ','.join(['value1,value2'] * (data_size // 20)), 'utf-8')

# Function to record RSA performance
def record_performance():
    key_sizes = [1024, 2048, 4096]  # Common RSA key sizes
    data_sizes = [16, 256, 1024, 4096, 16384]  # in bytes
    file_types = ['binary', 'text', 'json', 'csv']
    
    results = []

    for key_size in key_sizes:
        for data_size in data_sizes:
            for file_type in file_types:
                plaintext = generate_test_data(data_size, file_type)
                encrypt_time, decrypt_time, decrypted = measure_rsa_performance(key_size, plaintext)

                results.append((key_size, data_size, file_type, encrypt_time, decrypt_time))

                print(f"Key Size: {key_size} bits, Data Size: {data_size} bytes, File Type: {file_type}")
                print(f"  RSA Encryption Time: {encrypt_time:.6f} seconds")
                print(f"  RSA Decryption Time: {decrypt_time:.6f} seconds")
                print('-' * 60)

    return results

# Function to plot RSA performance results
def plot_results(results):
    key_sizes = sorted(set(k for k, _, _, _, _ in results))
    data_sizes = sorted(set(d for _, d, _, _, _ in results))
    file_types = sorted(set(f for _, _, f, _, _ in results))

    enc_times = np.zeros((len(key_sizes), len(data_sizes), len(file_types)))
    dec_times = np.zeros((len(key_sizes), len(data_sizes), len(file_types)))

    for key_size, data_size, file_type, encrypt_time, decrypt_time in results:
        enc_times[key_sizes.index(key_size), data_sizes.index(data_size), file_types.index(file_type)] = encrypt_time
        dec_times[key_sizes.index(key_size), data_sizes.index(data_size), file_types.index(file_type)] = decrypt_time

    plt.figure(figsize=(15, 5))

    # Encryption Times Plot
    for i, file_type in enumerate(file_types):
        plt.subplot(1, len(file_types), i + 1)
        plt.imshow(enc_times[:, :, i], interpolation='nearest', cmap='hot')
        plt.title(f'RSA Encryption Times ({file_type})')
        plt.colorbar()
        plt.xticks(np.arange(len(data_sizes)), data_sizes)
        plt.yticks(np.arange(len(key_sizes)), key_sizes)
        plt.xlabel('Data Size (bytes)')
        plt.ylabel('Key Size (bits)')

    plt.tight_layout()
    plt.savefig('rsa_performance_results.png', dpi=300)
    plt.close()
    print("Plots saved as 'rsa_performance_results.png'")

# Run performance tests and plot results
results = record_performance()
plot_results(results)
