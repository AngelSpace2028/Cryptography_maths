import os
import zstandard as zstd
import pickle
from qiskit import QuantumCircuit


# Function to find the divisor of a number
def find_divisor(n):
    if n % 2 == 0:
        return 2
    for i in range(3, int(n**0.5) + 1, 2):
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

# Function to decode the encoded path back to the original number
def decode_path(path):
    number = 1
    for num, divisor in reversed(path):
        if divisor:
            number *= divisor
    return number

# Function to write a number to a file in base 256 encoding
def base256_write(filename, number):
    with open(filename, 'wb') as f:
        encoded = number.to_bytes((number.bit_length() + 7) // 8 or 1, 'big')
        f.write(encoded)

# Function to read a number from a file in base 256 encoding
def base256_read(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return int.from_bytes(data, 'big')

# Function to compress a file using Zstandard (zstd)
def compress_with_zstd(input_file, output_file):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        cctx = zstd.ZstdCompressor()
        cctx.copy_stream(f_in, f_out)

# Function to decompress a file using Zstandard (zstd)
def decompress_with_zstd(input_file, output_file):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        dctx = zstd.ZstdDecompressor()
        dctx.copy_stream(f_in, f_out)

def encode_quantum(x):
    """Prepares a quantum circuit representing 2^x using x+1 qubits (no simulation)."""
    if x < 0:
        print("Error: x must be a non-negative integer.")
        return None

    num_qubits = x + 1
    qc = QuantumCircuit(num_qubits, num_qubits)  # Create a quantum circuit

    # Prepare the state |2^x⟩ (simplified representation)
    qc.x(x)  # Set the x-th qubit to 1

    return qc  # Return the quantum circuit


# Main encoding function (modified to include quantum part)
def encode():
    print("Quantum Divisor Encoder\n")
    in_file = input("Enter input file with number: ")
    out_path_file = input("Enter output filename for path: ")
    compressed_path_file = out_path_file + ".zst"

    if not os.path.isfile(in_file):
        print("Input file does not exist.")
        return

    try:
        original_number = base256_read(in_file)
        path, total_steps = encode_until_one(original_number)

        # Quantum part (no simulation):
        x = (original_number).bit_length() -1
        quantum_circuit = encode_quantum(x)
        if quantum_circuit:
            print(f"Quantum circuit representing 2^{x} created successfully.")
            print(quantum_circuit)

        # Classical serialization and compression
        with open(out_path_file, 'wb') as f:
            pickle.dump(path, f)

        compress_with_zstd(out_path_file, compressed_path_file)
        print(f"Encoded. Path saved to: {compressed_path_file}")
    except Exception as e:
        print(f"An error occurred during encoding: {e}")


# Main decoding function
def decode():
    file_path = input("Enter path file (.zst): ")
    output_file = input("Enter output file to save the decoded number: ")

    decompressed_path = file_path.replace('.zst', '')

    if not os.path.isfile(file_path):
        print("Input .zst file does not exist.")
        return

    try:
        decompress_with_zstd(file_path, decompressed_path)
        with open(decompressed_path, 'rb') as f:
            path = pickle.load(f)
        decoded = decode_path(path)
        base256_write(output_file, decoded)
        print(f"Decoded Number: {decoded}")
        print(f"Saved to {output_file}")
    except Exception as e:
        print(f"An error occurred during decoding: {e}")



# Main program to handle encoding and decoding
if __name__ == "__main__":
    choice = input("Enter 1 to encode, 2 to decode: ")

    if choice == '1':
        encode()
    elif choice == '2':
        decode()
    else:
        print("Invalid selection.")

