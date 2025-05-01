import os
import math
import sympy


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

def find_primes_in_range(start, end):
    """Find all prime numbers between a given range."""
    return list(sympy.primerange(start, end))

def find_prime_factors(n):
    """Find prime factors of a number."""
    factors = []
    for i in range(2, int(math.sqrt(n)) + 1):
        while n % i == 0 and is_prime(i):
            factors.append(i)
            n //= i
    if n > 1:
        factors.append(n)
    return factors

def transform_with_pattern(data, chunk_size=4):
    """Apply XOR 0xFF transformation per chunk."""
    transformed = bytearray()
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        transformed.extend([b ^ 0xFF for b in chunk])
    return transformed

def encode_with_zlib():
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

        # Compress using zlib
        compressed_data = (bytes(transformed_data))

        # Get prime factors of the compressed data size
        size = len(compressed_data)
        factors = find_prime_factors(size)

        if not factors:
            print("Warning: Could not find suitable prime factors.")
        else:
            print(f"Info: Prime factors of size are {factors}")

        # Write the encoded (transformed and compressed) data to the output file
        with open(output_enc, 'wb') as f:
            f.write(compressed_data)

        print(f"Encoding complete. Output saved to {output_enc}")
    except Exception as e:
        print(f"An error occurred during encoding: {e}")

def decode_with_zlib():
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

        # Decompress using zlib
        decompressed_data = (compressed_data)

        # Apply XOR transformation (reverse)
        recovered_data = transform_with_pattern(decompressed_data)

        # Write the decoded data to the output file
        with open(output_file, 'wb') as f:
            f.write(recovered_data)

        print(f"Decoding complete. Output saved to {output_file}")
    except Exception as e:
        print(f"An error occurred during decoding: {e}")

def find_primes_and_factors():
    # Define the range
    lower_bound = 255
    upper_bound = 2**28 * 1024 * 1024  # 2^28 * 1024 * 1024

    # Find all primes in the range
    primes = find_primes_in_range(lower_bound, upper_bound)

    # Find primes divisible by 2 (which will only be 2)
    primes_divisible_by_2 = [p for p in primes if p % 2 == 0]

    # Find primes close to the top limit (near the upper range)
    primes_near_top = [p for p in primes if p > upper_bound - 1000]

    # Output results
    print("Prime numbers divisible by 2 (only 2 will be here):", primes_divisible_by_2)
    print("\nPrimes near the top limit (close to 2^28 * 1024 * 1024):", primes_near_top)

if __name__ == "__main__":
    print("Software")
    print("Created by Jurijus Pacalovas.")
    print("File Encoding/Decoding System")
    print("Options:")
    print("1 - Encode file")
    print("2 - Decode file")
    print("3 - Find primes and their factors")
    try:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice not in ('1', '2', '3'):
            print("Invalid choice. Exiting.")
            exit()
    except EOFError:
        print("No input detected. Defaulting to Encode (1).")
        choice = '1'

    if choice == '1':
        encode_with_zlib()
    elif choice == '2':
        decode_with_zlib()
    elif choice == '3':
        find_primes_and_factors()