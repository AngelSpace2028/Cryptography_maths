import os
import math

def is_prime(n):
    """Primality test (can be improved for larger numbers)."""
    if n < 2:
        return False, b'\x00'
    if n == 2:
        return True, b'\x01'
    if n % 2 == 0:
        return False, b'\x02'
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False, b'\x03'
    return True, b'\xFF'

def find_p_and_q(n):
    """Finds factors p and q.  Improved error handling."""
    original_n = n
    p = n
    while p % 2 == 0:
        p //= 2
    if p == 1:  # Handle the case where n is a power of 2
        return 2, n // 2

    prime, _ = is_prime(p)
    if prime:
        q = original_n // p
        return p, q
    else:
        # Attempt to find a prime factor (this is still a basic approach)
        for i in range(3, int(math.sqrt(p)) + 1, 2): # Use math.sqrt for better precision.
            if p % i == 0:
                prime_check, _ = is_prime(i)
                if prime_check:
                    p = i
                    q = original_n // p
                    return p, q
        return None, None  # Indicate failure to find factors

def write_4byte_int(f, value):
    f.write(value.to_bytes(4, 'big'))

def read_4byte_int(f):
    return int.from_bytes(f.read(4), 'big')

def transform_with_pattern(data, chunk_size=4):
    transformed = bytearray()
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        transformed.extend([b ^ 0xFF for b in chunk])
    return transformed

def encode_no_compression():
    print("\nSimple Encoder (No Compression)")
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

        transformed_data = transform_with_pattern(original_data)
        size = len(transformed_data)
        p, q = find_p_and_q(size)

        if p is None or q is None:
            print("Error: Could not find suitable factors p and q.")
            return

        with open(output_enc, 'wb') as f:
            write_4byte_int(f, p)
            write_4byte_int(f, q)
            f.write(transformed_data)

        print(f"Encoding complete. Output saved to {output_enc}")
        print(f"Size factors: p={p}, q={q}")

    except Exception as e:
        print(f"An error occurred during encoding: {e}")


def decode_no_compression():
    print("\nSimple Decoder (No Compression)")
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
            p = read_4byte_int(f)
            q = read_4byte_int(f)
            transformed_data = f.read()

        if len(transformed_data) != p * q:
            print("Warning: File size doesn't match p*q factors!")

        recovered_data = transform_with_pattern(transformed_data)

        with open(output_file, 'wb') as f:
            f.write(recovered_data)

        print(f"Decoding complete. Output saved to {output_file}")

    except Exception as e:
        print(f"An error occurred during decoding: {e}")


if __name__ == "__main__":
    print("Quantum Software (No Compression)")
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
