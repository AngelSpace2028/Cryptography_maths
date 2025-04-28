import os
import math

try:
    import paq  # Ensure you have a paq library, or replace this with zlib if needed
except ImportError:
    import paq  # fallback to zlib if paq not available

# Check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

# Find divisors, dividing by 2 and 3 as long as possible, and count primes
def find_divisor_and_primes(n):
    primes_found = 0
    divisors = []
    
    # Divide by 2 as long as possible
    while n % 2 == 0:
        divisors.append(2)
        n //= 2
        primes_found += 1
    
    # Divide by 3 as long as possible
    while n % 3 == 0:
        divisors.append(3)
        n //= 3
        primes_found += 1

    # Check for other prime factors
    for i in range(5, int(math.isqrt(n)) + 1, 2):
        while n % i == 0:
            divisors.append(i)
            n //= i
            if is_prime(i):
                primes_found += 1

    if n > 2 and is_prime(n):
        divisors.append(n)
        primes_found += 1

    return divisors, primes_found

# Write and read 4-byte integer
def write_4byte_int(f, value):
    f.write(value.to_bytes(4, 'big'))

def read_4byte_int(f):
    return int.from_bytes(f.read(4), 'big')

# Simple pattern transformation (bit-flipping)
def transform_with_pattern(data, chunk_size=4):
    transformed = bytearray()
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        transformed.extend([b ^ 0xFF for b in chunk])
    return transformed

# Fake quantum encoding
def fake_quantum_encode(number):
    return number ^ 0xAAAAAAAA

def fake_quantum_decode(encoded_number):
    return encoded_number ^ 0xAAAAAAAA

# Compress using PAQ (or zlib fallback)
def compress_with_paq(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        data = f_in.read()
    compressed_data = paq.compress(data)
    with open(output_file, 'wb') as f_out:
        f_out.write(compressed_data)

# Decompress using PAQ (or zlib fallback)
def decompress_with_paq(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        compressed_data = f_in.read()
    decompressed_data = paq.decompress(compressed_data)
    with open(output_file, 'wb') as f_out:
        f_out.write(decompressed_data)

# Encoding function
def encode():
    print("\nSimple Encoder (no Qiskit)")
    try:
        input_file = input("Enter input file: ").strip()
        output_base = input("Enter output base name (without .paq): ").strip()
    except EOFError:
        print("No input detected. Exiting encode mode.")
        return

    output_paq = output_base + ".paq"
    
    if not os.path.isfile(input_file):
        print("File does not exist.")
        return

    with open(input_file, 'rb') as f:
        original_data = f.read()

    transformed_data = transform_with_pattern(original_data)

    temp_file = output_base + "_temp"
    with open(temp_file, 'wb') as f:
        size = len(transformed_data)
        divisors, prime_count = find_divisor_and_primes(size)

        if prime_count == 2:
            f.write(bytes([0x01]))
        elif prime_count == 0:
            f.write(bytes([0x02]))
        elif prime_count == 1:
            f.write(bytes([0x03]))
        else:
            f.write(bytes([0x00]))

        write_4byte_int(f, len(divisors))
        write_4byte_int(f, prime_count)

        encoded_size = fake_quantum_encode(size)
        write_4byte_int(f, encoded_size)

        f.write(transformed_data)

    compress_with_paq(temp_file, output_paq)
    os.remove(temp_file)

    print(f"Encoding complete. Output saved to {output_paq}")

# Decoding function
def decode():
    print("\nSimple Decoder (no Qiskit)")
    try:
        input_paq = input("Enter compressed file (.paq): ").strip()
        output_file = input("Enter output file: ").strip()
    except EOFError:
        print("No input detected. Exiting decode mode.")
        return

    if not os.path.isfile(input_paq):
        print("Compressed file does not exist.")
        return

    temp_file = input_paq.replace('.paq', '_temp')
    decompress_with_paq(input_paq, temp_file)

    with open(temp_file, 'rb') as f:
        prepend_byte = f.read(1)

        if prepend_byte not in (b'\x00', b'\x01', b'\x02', b'\x03'):
            print("Unexpected prepend byte. Extraction failed.")
            os.remove(temp_file)
            return

        divisors_count = read_4byte_int(f)
        prime_count = read_4byte_int(f)
        encoded_size = read_4byte_int(f)
        size = fake_quantum_decode(encoded_size)

        transformed_data = f.read()

    recovered_data = transform_with_pattern(transformed_data)

    with open(output_file, 'wb') as f:
        f.write(recovered_data)

    os.remove(temp_file)
    print(f"Decoding complete. Output saved to {output_file}")

# Main CLI
if __name__ == "__main__":
    print("Created by Jurijus Pacalovas.")
    print("Options:")
    print("1 - Encode file")
    print("2 - Decode file")
    try:
        choice = input("Enter 1 or 2: ").strip()
    except EOFError:
        print("No input detected. Defaulting to Encode (1).")
        choice = '1'

    if choice == '1':
        encode()
    elif choice == '2':
        decode()
    else:
        print("Invalid choice. Exiting.")
