# Import necessary libraries
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import psutil
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Function to get system metrics
def get_system_metrics():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    return cpu_usage, memory_info.percent

# Function to measure AES performance
def measure_aes_performance(key_size, plaintext):
    key = os.urandom(key_size // 8)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext, AES.block_size)

    initial_cpu, initial_memory = get_system_metrics()
    
    start_encrypt = time.time()
    ciphertext = cipher.encrypt(padded_plaintext)
    end_encrypt = time.time()
    encrypt_time = end_encrypt - start_encrypt

    cipher_decrypt = AES.new(key, AES.MODE_ECB)
    start_decrypt = time.time()
    decrypted_padded_plaintext = cipher_decrypt.decrypt(ciphertext)
    decrypted_plaintext = unpad(decrypted_padded_plaintext, AES.block_size)
    end_decrypt = time.time()
    decrypt_time = end_decrypt - start_decrypt

    final_cpu, final_memory = get_system_metrics()

    return (encrypt_time, decrypt_time, decrypted_plaintext,
            initial_cpu, final_cpu, initial_memory, final_memory)

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

# Function to record performance metrics
def record_performance():
    key_sizes = [128, 192, 256]
    data_sizes = [16, 256, 1024, 4096, 16384]
    file_types = ['binary', 'text', 'json', 'csv']
    
    results = []

    for key_size in key_sizes:
        for data_size in data_sizes:
            for file_type in file_types:
                plaintext = generate_test_data(data_size, file_type)
                encrypt_time, decrypt_time, _, initial_cpu, final_cpu, initial_memory, final_memory = measure_aes_performance(key_size, plaintext)

                results.append((key_size, data_size, file_type, encrypt_time, decrypt_time, initial_cpu, final_cpu, initial_memory, final_memory))

                print(f"Key Size: {key_size} bits, Data Size: {data_size} bytes, File Type: {file_type}")
                print(f"  AES Encryption Time: {encrypt_time:.6f} seconds")
                print(f"  AES Decryption Time: {decrypt_time:.6f} seconds")
                print(f"  Initial CPU Usage: {initial_cpu}%, Final CPU Usage: {final_cpu}%")
                print(f"  Initial Memory Usage: {initial_memory}%, Final Memory Usage: {final_memory}%")
                print('-' * 60)

    return results

# Function to plot performance results
def plot_results(results):
    key_sizes = sorted(set(k for k, _, _, _, _, _, _, _, _ in results))
    data_sizes = sorted(set(d for _, d, _, _, _, _, _, _, _ in results))
    file_types = sorted(set(f for _, _, f, _, _, _, _, _, _ in results))

    # Example for encryption times:
    enc_times = np.zeros((len(key_sizes), len(data_sizes), len(file_types)))
    
    for key_size, data_size, file_type, encrypt_time, _, _, _, _, _ in results:
        enc_times[key_sizes.index(key_size), data_sizes.index(data_size), file_types.index(file_type)] = encrypt_time

    plt.figure(figsize=(15, 5))
    for i, file_type in enumerate(file_types):
        plt.subplot(1, len(file_types), i + 1)
        plt.imshow(enc_times[:, :, i], interpolation='nearest', cmap='hot')
        plt.title(f'Encryption Times ({file_type})')
        plt.colorbar()
        plt.xticks(np.arange(len(data_sizes)), data_sizes)
        plt.yticks(np.arange(len(key_sizes)), key_sizes)
        plt.xlabel('Data Size (bytes)')
        plt.ylabel('Key Size (bits)')

    plt.tight_layout()
    plt.savefig('aes_performance_results.png', dpi=300)
    plt.close()
    print("Plots saved as 'aes_performance_results.png'")

# Run performance tests and plot results
results = record_performance()
plot_results(results)
