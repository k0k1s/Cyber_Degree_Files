import os
import time
import hashlib
import psutil
import matplotlib.pyplot as plt
import numpy as np

# Function to get system metrics
def get_system_metrics():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    return cpu_usage, memory_info.percent

# Function to measure hashing performance and collect system metrics
def measure_hash_performance(plaintext):
    initial_cpu, initial_memory = get_system_metrics()  # Record initial CPU and memory usage
    
    # Hash the plaintext
    start_hash = time.time()
    hash_object = hashlib.sha256(plaintext)
    hex_dig = hash_object.hexdigest()
    end_hash = time.time()
    hash_time = end_hash - start_hash
    
    final_cpu, final_memory = get_system_metrics()  # Record final CPU and memory usage
    
    return hash_time, hex_dig, initial_cpu, final_cpu, initial_memory, final_memory

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

# Function to conduct comprehensive testing with varying conditions
def record_hash_performance():
    data_sizes = [16, 256, 1024, 4096, 16384]  # Different input data sizes (in bytes)
    file_types = ['binary', 'text', 'json', 'csv']  # Different file types for testing
    
    results = []

    for data_size in data_sizes:
        for file_type in file_types:
            plaintext = generate_test_data(data_size, file_type)
            hash_time, hex_dig, initial_cpu, final_cpu, initial_memory, final_memory = measure_hash_performance(plaintext)
            
            # Store the performance results
            results.append((data_size, file_type, hash_time, initial_cpu, final_cpu, initial_memory, final_memory))
            
            print(f"Data Size: {data_size} bytes, File Type: {file_type}")
            print(f"  SHA-256 Hash: {hex_dig}")
            print(f"  Hashing Time: {hash_time:.6f} seconds")
            print(f"  Initial CPU Usage: {initial_cpu}%, Final CPU Usage: {final_cpu}%")
            print(f"  Initial Memory Usage: {initial_memory}%, Final Memory Usage: {final_memory}%")
            print('-' * 60)
    
    return results

# Function to plot the performance results
def plot_performance(results):
    data_sizes = sorted(set(d for d, _, _, _, _, _, _ in results))
    file_types = sorted(set(f for _, f, _, _, _, _, _ in results))
    
    # Prepare data for plotting
    hash_times = np.zeros((len(data_sizes), len(file_types)))
    cpu_usages = np.zeros((len(data_sizes), len(file_types)))
    memory_usages = np.zeros((len(data_sizes), len(file_types)))

    for i, (data_size, file_type, hash_time, initial_cpu, final_cpu, initial_memory, final_memory) in enumerate(results):
        row_idx = data_sizes.index(data_size)
        col_idx = file_types.index(file_type)
        
        hash_times[row_idx, col_idx] = hash_time
        cpu_usages[row_idx, col_idx] = final_cpu - initial_cpu
        memory_usages[row_idx, col_idx] = final_memory - initial_memory

    # Create plots
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    # Plot for Hashing Time
    for j, file_type in enumerate(file_types):
        axs[0].plot(data_sizes, hash_times[:, j], label=file_type)
    axs[0].set_title("Hashing Time by Data Size")
    axs[0].set_xlabel("Data Size (bytes)")
    axs[0].set_ylabel("Hashing Time (seconds)")
    axs[0].legend(title="File Type")

    # Plot for CPU Usage
    for j, file_type in enumerate(file_types):
        axs[1].plot(data_sizes, cpu_usages[:, j], label=file_type)
    axs[1].set_title("CPU Usage by Data Size")
    axs[1].set_xlabel("Data Size (bytes)")
    axs[1].set_ylabel("CPU Usage Change (%)")
    axs[1].legend(title="File Type")

    # Plot for Memory Usage
    for j, file_type in enumerate(file_types):
        axs[2].plot(data_sizes, memory_usages[:, j], label=file_type)
    axs[2].set_title("Memory Usage by Data Size")
    axs[2].set_xlabel("Data Size (bytes)")
    axs[2].set_ylabel("Memory Usage Change (%)")
    axs[2].legend(title="File Type")

    # Save and show the plot
    plt.tight_layout()
    plt.savefig('hash_performance_results.png', dpi=300)
    plt.show()
    print("Plot saved as 'hash_performance_results.png'")

# Conduct the performance tests
results = record_hash_performance()

# Plot the results
plot_performance(results)
