import os
import zstandard as zstd
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram

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
    # Remove the leading 1 added during encoding
    number >>= 1
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

# Function to add a leading 1 bit to a number before encoding
def add_leading_one_bit(number):
    binary = bin(number)[2:]  # Remove '0b'
    modified = '1' + binary
    return int(modified, 2)

# Function to remove the leading 1 bit during decoding
def remove_leading_one_bit(number):
    binary = bin(number)[2:]
    if binary[0] != '1':
        raise ValueError("No leading 1 found in binary")
    return int(binary[1:], 2)

# Quantum Addition Function using Qiskit
def quantum_addition(number1, number2):
    qubits = max(number1.bit_length(), number2.bit_length()) + 1
    qc = QuantumCircuit(qubits)

    # Encode the numbers into quantum registers
    for i in range(qubits):
        if (number1 >> i) & 1:
            qc.x(i)
        if (number2 >> i) & 1:
            qc.x(i + qubits // 2)  # Divide the qubits into two parts for addition

    # Apply some quantum gates for addition (simulated for illustration)
    for i in range(qubits - 1):
        qc.cx(i, i + 1)

    # Visualize the circuit
    print("Quantum addition circuit:")
    print(qc.draw())

    return qc

# Main encoding function
def encode():
    print("Quantum Divisor Encoder\n")
    in_file = input("Enter input file with number: ")
    out_J_file = input("Enter output filename for J (last divisor): ")
    out_U_file = input("Enter output filename for U (steps): ")
    compressed_J_file = out_J_file + ".zst"
    compressed_U_file = out_U_file + ".zst"
    
    if not os.path.isfile(in_file):
        print("Input file does not exist.")
    else:
        original_number = base256_read(in_file)
        number = add_leading_one_bit(original_number)  # Add the leading 1 before encoding
        path, total_steps = encode_until_one(number)
        last_before_one = path[-2][0] if len(path) >= 2 else 1
        last_Q = path[-2][1] if len(path) >= 2 else 1
        
        base256_write(out_J_file, last_Q)
        base256_write(out_U_file, total_steps)
        
        # Compress the J and U files using Zstandard
        compress_with_zstd(out_J_file, compressed_J_file)
        compress_with_zstd(out_U_file, compressed_U_file)
        
        print(f"Encoded. Last Q (J): {last_Q}, Steps (U): {total_steps}")
        print(f"Compressed files: {compressed_J_file} and {compressed_U_file}")

        # Quantum operation for addition (just as an illustration)
        quantum_addition(original_number, last_Q)

# Main decoding function
def decode():
    file_J = input("Enter J file (last divisor .zst): ")
    file_U = input("Enter U file (steps .zst): ")
    output_file = input("Enter output file to save the decoded number: ")
    
    # Decompressed file paths (remove .zst extension)
    decompressed_J = file_J.replace('.zst', '')
    decompressed_U = file_U.replace('.zst', '')
    
    # Check if the .zst files exist
    if not os.path.isfile(file_J) or not os.path.isfile(file_U):
        print("One or both input .zst files do not exist.")
        return
    
    # Decompress the .zst files into original files
    decompress_with_zstd(file_J, decompressed_J)
    decompress_with_zstd(file_U, decompressed_U)
    
    # Read the decompressed files
    J = base256_read(decompressed_J)
    U = base256_read(decompressed_U)
    
    # Reconstruct the path by repeating the last divisor
    path = [(J, J)] * (U - 1) + [(1, None)]
    
    # Decode the number from the path
    decoded = decode_path(path)
    
    # Remove the leading 1 bit before saving the original number
    decoded = remove_leading_one_bit(decoded)
    
    # Save the decoded number to a file
    base256_write(output_file, decoded)
    
    print(f"Decoded Number: {decoded}")
    print(f"Saved to {output_file}")

    # Quantum operation for addition (just as an illustration)
    quantum_addition(decoded, J)

# Main program to handle encoding and decoding
if __name__ == "__main__":
    choice = input("Enter 1 to encode, 2 to decode: ")

    if choice == '1':
        encode()
    elif choice == '2':
        decode()
    else:
        print("Invalid selection.")