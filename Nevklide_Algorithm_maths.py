from math import log2

def find_divisor(n):
    """Finds the smallest divisor of n greater than 1."""
    if n % 2 == 0:
        return 2
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return i
    return n  # n is prime

def encode_until_one(number):
    """Encodes a number by repeatedly dividing by its smallest divisor until 1 is reached."""
    path = []
    step = 0
    print(f"\nEncoding {number} until it becomes 1...\n")

    while number > 1:
        divisor = find_divisor(number)
        path.append((number, divisor))
        number //= divisor
        step += 1
        print(f"Step {step}: P = {path[-1][0]}, Q = {divisor}, Result = {number}")

    print(f"Total steps: {step}\n")
    return path

def decode_path(path):
    """Decodes a number from its encoded path."""
    number = 1
    print("Decoding path:")
    for num, divisor in reversed(path):
        number *= divisor
        print(f"{number // divisor} * {divisor} = {number}")
    return number

def quantum_info(n):
    bit_length = n.bit_length()
    qubits = min((2 ** bit_length) + 1, 32)  # Cap for simulation
    print(f"\nOriginal Number = {n}")
    print(f"Bit length X = {bit_length}")
    print(f"Using 2^X + 1 = {2 ** bit_length + 1} qubits and X + 1 = {bit_length + 1} quantum operations")
    print(f"(Simulation uses {qubits} qubits max)\n")

if __name__ == "__main__":
    try:
        start_number = int(input("Enter a number to encode (e.g., 13751): "))
        if start_number <= 1:
            print("Please enter a number greater than 1.")
        else:
            path = encode_until_one(start_number)

            print("All (P, Q) steps:")
            for i, (p, q) in enumerate(path):
                print(f"Step {i+1}: P = {p}, Q = {q}, P ÷ Q = {p // q}")
            print()

            decoded = decode_path(path)
            print(f"\nDecoded back to: {decoded}")
            print("Success!" if decoded == start_number else "Mismatch!")

            print(f"\nLast P before reaching 1: {path[-1][0] if path else 1}")
            print(f"Total steps taken: {len(path)}")

            quantum_info(start_number)

    except ValueError:
        print("Invalid input. Please enter a valid integer.")