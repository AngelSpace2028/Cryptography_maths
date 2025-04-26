import os
import math
import paq
from qiskit import QuantumCircuit

# Find a divisor
def find_divisor(n):
    if n % 2 == 0:
        return 2
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return i
    return n

# Write and read 4-byte integer
def write_4byte_int(f, value):
    f.write(value.to_bytes(4, 'big'))

def read_4byte_int(f):
    return int.from_bytes(f.read(4), 'big')

# Simple pattern transformation (bit-flipping example)
def transform_with_pattern(data, chunk_size=4):
    transformed = bytearray()
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        if len(chunk) < chunk_size:
            chunk = chunk.ljust(chunk_size, b'\x00')
        transformed.extend([b ^ 0xFF for b in chunk])
    return transformed

# Quantum encoding simulation (without Aer, purely by building circuit)
def quantum_encode(number, qubits):
    circuit = QuantumCircuit(qubits)
    bin_number = bin(number)[2:].zfill(qubits)
    for i, bit in enumerate(reversed(bin_number)):
        if bit == '1':
            circuit.x(i)
    return int(bin_number, 2)

# Compress using zlib
def compress_with_zlib(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        data = f_in.read()
    compressed_data = paq.compress(data)
    with open(output_file, 'wb') as f_out:
        f_out.write(compressed_data)

# Decompress using zlib
def decompress_with_zlib(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        compressed_data = f_in.read()
    decompressed_data = paq.decompress(compressed_data)
    with open(output_file, 'wb') as f_out:
        f_out.write(decompressed_data)

# Main encoding function
def encode():
    print("Quantum Encoder (X+1 qubits)")
    input_file = input("Enter input file: ").strip()
    output_base = input("Enter output base name (without .zlib): ").strip()
    output_zlib = output_base + ".zlib"

    if not os.path.isfile(input_file):
        print("File does not exist.")
        return

    with open(input_file, 'rb') as f:
        original_data = f.read()

    transformed_data = transform_with_pattern(original_data)

    temp_file = output_base + "_temp"
    with open(temp_file, 'wb') as f:
        size = len(transformed_data)
        p = find_divisor(size)
        q = size // p
        a = p + 1
        b = q + 1

        # Write P, Q, A, B
        write_4byte_int(f, p)
        write_4byte_int(f, q)
        write_4byte_int(f, a)
        write_4byte_int(f, b)

        # Calculate number of qubits needed
        x = (size - 1).bit_length()
        qubits = x + 1
        
        # Quantum encode the size
        encoded_size = quantum_encode(size, qubits)
        write_4byte_int(f, encoded_size)

        # Write transformed data
        f.write(transformed_data)

    compress_with_zlib(temp_file, output_zlib)
    os.remove(temp_file)

    print(f"Encoding complete. Output saved to {output_zlib}")

# Main decoding function
def decode():
    print("Quantum Decoder (X+1 qubits)")
    input_zlib = input("Enter compressed file (.zlib): ").strip()
    output_file = input("Enter output file: ").strip()

    if not os.path.isfile(input_zlib):
        print("Compressed file does not exist.")
        return

    temp_file = input_zlib.replace('.zlib', '_temp')
    decompress_with_zlib(input_zlib, temp_file)

    with open(temp_file, 'rb') as f:
        p = read_4byte_int(f)
        q = read_4byte_int(f)
        a = read_4byte_int(f)
        b = read_4byte_int(f)
        encoded_size = read_4byte_int(f)
        transformed_data = f.read()

    recovered_data = transform_with_pattern(transformed_data)

    with open(output_file, 'wb') as f:
        f.write(recovered_data)

    os.remove(temp_file)
    print(f"Decoding complete. Output saved to {output_file}")

# CLI
if __name__ == "__main__":
    print("Created by Jurijus Pacalovas.")
    print("Options:")
    print("1 - Encode file")
    print("2 - Decode file")
    choice = input("Enter 1 or 2: ").strip()
    if choice == '1':
        encode()
    elif choice == '2':
        decode()
    else:
        print("Invalid choice.")
