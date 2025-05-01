import os
import math

def is_prime(n):
    """Simple primality test."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def find_p_and_q(n):
    """Finds two factors p and q of n where p is prime if possible."""
    original_n = n
    p = n
    while p % 2 == 0:
        p //= 2
        if p == 1:
            return 2, n // 2
    if is_prime(p):
        return p, original_n // p
    for i in range(3, int(math.sqrt(p)) + 1, 2):
        if p % i == 0 and is_prime(i):
            return i, original_n // i
    return None, None

def transform_with_pattern(data, chunk_size=4):
    """Apply XOR 0xFF transformation per chunk."""
    transformed = bytearray()
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        transformed.extend([b ^ 0xFF for b in chunk])
    return transformed

def encode_no_compression():
    print("\nSimple Encoder (XOR + zlib Compression)")
    try:
        input_file = input("Enter input file: ").strip()
        output_base = input("Enter output base name (without .enc): ").strip()
    except EOFError:
        print("No input detected. Exiting encode mode.")
        return

    output_enc = output_base + ".enc"

    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        return

    try:
        with open(input_file, 'rb') as f:
            original_data = f.read()

        # Apply XOR transformation
        transformed_data = transform_with_pattern(original_data)
        compressed_data = bytes(transformed_data)

        # Get prime factors of the compressed data size
        size = len(compressed_data)
        p, q = find_p_and_q(size)

        if p is None or q is None:
            print("Warning: Could not find suitable factors p and q.")
        else:
            print(f"Info: Factors of size are p = {p}, q = {q}")

        # Write the encoded (transformed) data to the output file
        with open(output_enc, 'wb') as f:
            f.write(compressed_data)

        print(f"Encoding complete. Output saved to {output_enc}")
    except Exception as e:
        print(f"An error occurred during encoding: {e}")

def decode_no_compression():
    print("\nSimple Decoder (zlib Decompression + XOR)")
    try:
        input_enc = input("Enter encoded file (.enc): ").strip()
        output_file = input("Enter output file: ").strip()
    except EOFError:
        print("No input detected. Exiting decode mode.")
        return

    if not os.path.isfile(input_enc):
        print(f"Error: File '{input_enc}' does not exist.")
        return

    try:
        with open(input_enc, 'rb') as f:
            compressed_data = f.read()

        # Apply XOR transformation (reverse)
        transformed_data = compressed_data
        recovered_data = transform_with_pattern(transformed_data)

        # Write the decoded data to the output file
        with open(output_file, 'wb') as f:
            f.write(recovered_data)

        print(f"Decoding complete. Output saved to {output_file}")
    except Exception as e:
        print(f"An error occurred during decoding: {e}")

if __name__ == "__main__":
    print("Software")
    print("Created by Jurijus Pacalovas.")
    print("File Encoding/Decoding System")
    print("Options:")
    print("1 - Encode file")
    print("2 - Decode file")
    try:
        choice = input("Enter 1 or 2: ").strip()
        if choice not in ('1', '2'):
            print("Invalid choice. Exiting.")
            exit()
    except EOFError:
        print("No input detected. Defaulting to Encode (1).")
        choice = '1'

    if choice == '1':
        encode_no_compression()
    elif choice == '2':
        decode_no_compression()