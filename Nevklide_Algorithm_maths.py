import os
import math
import paq

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

def find_p_and_q(n):
    original_n = n
    p = n
    
    # Divide by 2 until we get an odd number
    while p % 2 == 0:
        p = p // 2
    
    # If the result isn't prime, find smallest prime factor
    if not is_prime(p):
        for i in range(3, int(math.isqrt(p)) + 1, 2):
            if p % i == 0 and is_prime(i):
                p = i
                break
    
    q = original_n // p
    return p, q

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

def fake_quantum_encode(number):
    return number ^ 0xAAAAAAAA

def fake_quantum_decode(encoded_number):
    return encoded_number ^ 0xAAAAAAAA

def compress_with_paq(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        data = f_in.read()
    compressed_data = paq.compress(data)
    with open(output_file, 'wb') as f_out:
        f_out.write(compressed_data)

def decompress_with_paq(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        compressed_data = f_in.read()
    decompressed_data = paq.decompress(compressed_data)
    with open(output_file, 'wb') as f_out:
        f_out.write(decompressed_data)

def encode():
    print("\nSimple Encoder")
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
    size = len(transformed_data)
    p, q = find_p_and_q(size)

    temp_file = output_base + "_temp"
    with open(temp_file, 'wb') as f:
        # Store p and q as 4-byte integers
        write_4byte_int(f, p)
        write_4byte_int(f, q)
        
        # Store transformed data
        f.write(transformed_data)

    compress_with_paq(temp_file, output_paq)
    os.remove(temp_file)

    print(f"Encoding complete. Output saved to {output_paq}")
    print(f"Size factors: p={p}, q={q}")

def decode():
    print("\nSimple Decoder")
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
        # Read p and q (4-byte integers)
        p = read_4byte_int(f)
        q = read_4byte_int(f)
        
        # Read transformed data
        transformed_data = f.read()

    # Verify the size matches p*q
    if len(transformed_data) != p * q:
        print("Warning: File size doesn't match p*q factors!")

    recovered_data = transform_with_pattern(transformed_data)

    with open(output_file, 'wb') as f:
        f.write(recovered_data)

    os.remove(temp_file)
    print(f"Decoding complete. Output saved to {output_file}")

if __name__ == "__main__":
    print("File Encoding/Decoding System")
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