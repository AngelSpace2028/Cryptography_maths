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

# Qiskit demonstration of 2**X = value using X+1 qubits
def demonstrate_qubits(value):
    if value <= 0:
        print("Value must be positive for Qiskit demo.")
        return
    x = value.bit_length() - 1
    num_qubits = x + 1
    print(f"Qiskit Demo: Representing 2^{x} = {value} using {num_qubits} qubits")
    circuit = QuantumCircuit(num_qubits, name="Qubits for 2^X")
    circuit.x(x)  # Flip the highest qubit
    print(circuit.draw())

# Main encode function
def encode():
    print("Quantum Divisor Encoder\n")
    in_file = input("Enter input file with number: ").strip()
    out_path_file = input("Enter output filename for path (without .zst): ").strip()
    compressed_path_file = out_path_file + ".zst"
    
    if not os.path.isfile(in_file):
        print("Input file does not exist.")
        return
    
    original_number = base256_read(in_file)
    demonstrate_qubits(original_number)
    
    path, total_steps = encode_until_one(original_number)
    
    # Saving file size and p:q values
    file_size = os.path.getsize(in_file)
    p = find_divisor(original_number)
    q = original_number // p
    
    with open(out_path_file, 'w') as f:
        f.write(f"{file_size}\n")
        f.write(f"{p}:{q}\n")
        for num, divisor in path:
            if divisor is not None:
                f.write(f"{num}:{divisor}\n")
            else:
                f.write(f"{num}:None\n")
    
    compress_with_zstd(out_path_file, compressed_path_file)
    os.remove(out_path_file)  # Delete the uncompressed file after compressing
    print(f"Encoded and saved to: {compressed_path_file}")
    print(f"File Size: {file_size} bytes, Divisors: p = {p}, q = {q}")

# Decode function
def decode():
    print("Quantum Divisor Decoder\n")
    file_path = input("Enter path file (.zst): ").strip()
    output_file = input("Enter output file to save the decoded number: ").strip()
    decompressed_path = file_path.replace('.zst', '')
    
    if not os.path.isfile(file_path):
        print("Input .zst file does not exist.")
        return
    
    decompress_with_zstd(file_path, decompressed_path)
    
    with open(decompressed_path, 'r') as f:
        lines = f.readlines()
    
    # Skip first two lines (file size and p:q info)
    path = []
    for line in lines[2:]:
        num_str, div_str = line.strip().split(':')
        num = int(num_str)
        if div_str == 'None':
            divisor = None
        else:
            divisor = int(div_str)
        path.append((num, divisor))
    
    decoded = decode_path(path)
    base256_write(output_file, decoded)
    os.remove(decompressed_path)  # Delete the decompressed temp file
    print(f"Decoded Number: {decoded}")
    print(f"Saved to {output_file}")

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