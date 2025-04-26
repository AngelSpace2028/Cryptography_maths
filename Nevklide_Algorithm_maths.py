import os
import math
import zstandard as zstd
from qiskit import QuantumCircuit

# Function to find the divisor of a number
def find_divisor(n):
    if n % 2 == 0:
        return 2
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0:
            return i
    return n

# Function to encode a number until it reaches 1
def encode_until_one(number):
    path = []
    step = 0
    while number > 1:
        divisor = find_divisor(number)
        path.append((number, divisor))
        number //= divisor
        step += 1
    path.append((1, None))
    return path, step

# Decode function
def decode_path(path):
    number = 1
    for num, divisor in reversed(path):
        if divisor:
            number *= divisor
    return number

# Read/write number in base256 format
def base256_write(filename, number):
    with open(filename, 'wb') as f:
        encoded = number.to_bytes((number.bit_length() + 7) // 8 or 1, 'big')
        f.write(encoded)

def base256_read(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return int.from_bytes(data, 'big')

# Zstandard compression
def compress_with_zstd(input_file, output_file):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        cctx = zstd.ZstdCompressor()
        cctx.copy_stream(f_in, f_out)

def decompress_with_zstd(input_file, output_file):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        dctx = zstd.ZstdDecompressor()
        dctx.copy_stream(f_in, f_out)

# Apply pattern transformation: "4,4,4,4,4" chunk-based transformation
def transform_with_pattern(data, chunk_size=4):
    transformed_data = bytearray()
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        if len(chunk) < chunk_size:
            chunk = chunk.ljust(chunk_size, b'\x00')  # Pad last chunk if needed
        # A simple transformation example (you can customize this part)
        transformed_chunk = bytearray([x ^ 0xFF for x in chunk])  # Bit-flipping for example
        transformed_data.extend(transformed_chunk)
    return transformed_data

# Quantum encoding with Qiskit (without execution)
def quantum_encode(number, qubits=3):
    # Create a quantum circuit with 'qubits' number of qubits
    circuit = QuantumCircuit(qubits, qubits)
    
    # Apply Hadamard gate to put the qubits in superposition
    for qubit in range(qubits):
        circuit.h(qubit)
    
    # Encode the number by applying a series of CNOT gates based on the number's bits
    bin_number = bin(number)[2:].zfill(qubits)
    for i, bit in enumerate(bin_number):
        if bit == '1':
            circuit.x(i)  # Apply X gate for '1' bit

    # Instead of execution, we will just visualize the circuit here
    # This is where we stop execution, and we're not measuring or running on a simulator
    print(f"Quantum Encoding Circuit for {number} (with {qubits} qubits):")
    print(circuit)
    
    # We will not actually simulate it, but return the quantum circuit for review
    return circuit

# Write 4-byte long to file
def write_4byte_int(f, value):
    f.write(value.to_bytes(4, 'big'))

# Read 4-byte long from file
def read_4byte_int(f):
    return int.from_bytes(f.read(4), 'big')

# Main encode function
def encode():
    print("Transformation Encoder\n")
    in_file = input("Enter input file with number: ").strip()
    out_path_file = input("Enter output filename for path (without .zst): ").strip()
    compressed_path_file = out_path_file + ".zst"
    
    if not os.path.isfile(in_file):
        print("Input file does not exist.")
        return
    
    original_data = bytearray()
    with open(in_file, 'rb') as f:
        original_data = f.read()

    # Apply pattern-based transformation to data
    transformed_data = transform_with_pattern(original_data)
    
    # Write transformed data to a temporary file, including 4-byte long values (p, q, a, b)
    temp_file = out_path_file + "_transformed"
    with open(temp_file, 'wb') as f:
        # Example: Write p, q, a, b as 4-byte integers
        p = find_divisor(len(transformed_data))  # Dummy value for demonstration
        q = len(transformed_data) // p
        a = p + 1  # Just an example value
        b = q + 1  # Just an example value
        
        # Write p, q, a, b as 4-byte values
        write_4byte_int(f, p)
        write_4byte_int(f, q)
        write_4byte_int(f, a)
        write_4byte_int(f, b)
        
        # Quantum encoding of the transformed data length
        encoded_length_circuit = quantum_encode(len(transformed_data), qubits=3)  # Without execution
        write_4byte_int(f, len(transformed_data))  # Use the actual length of data instead of quantum result
        
        # Write the transformed data
        f.write(transformed_data)
    
    # Compress using Zstandard
    compress_with_zstd(temp_file, compressed_path_file)
    os.remove(temp_file)  # Delete the uncompressed file after compressing
    print(f"Encoded and saved to: {compressed_path_file}")

# Decode function
def decode():
    print("Transformation Decoder\n")
    file_path = input("Enter path file (.zst): ").strip()
    output_file = input("Enter output file to save the decoded number: ").strip()
    decompressed_path = file_path.replace('.zst', '')
    
    if not os.path.isfile(file_path):
        print("Input .zst file does not exist.")
        return
    
    # Decompress using Zstandard
    decompress_with_zstd(file_path, decompressed_path)
    
    with open(decompressed_path, 'rb') as f:
        # Read p, q, a, b (4-byte integers each)
        p = read_4byte_int(f)
        q = read_4byte_int(f)
        a = read_4byte_int(f)
        b = read_4byte_int(f)
        
        # Read quantum-encoded length
        encoded_length = read_4byte_int(f)
        print(f"Quantum-encoded length: {encoded_length}")
        
        # Read transformed data
        transformed_data = f.read()

    # Reverse the pattern-based transformation
    original_data = transform_with_pattern(transformed_data)  # Apply same transformation logic
    
    # Write the original data to output file
    with open(output_file, 'wb') as f:
        f.write(original_data)
    
    os.remove(decompressed_path)  # Delete the decompressed temp file
    print(f"Decoded and saved to: {output_file}")

# CLI handler
if __name__ == "__main__":
    print("Options:")
    print("1 - Encode a number")
    print("2 - Decode a number")
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == '1':
        encode()
    elif choice == '2':
        decode()
    else:
        print("Invalid selection.")