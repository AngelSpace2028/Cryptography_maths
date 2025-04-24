from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram

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
    original = number
    path = []
    step = 0

    print(f"Encoding {number} with optimized steps until it becomes 1...\n")

    while number > 1:
        divisor = find_divisor(number)
        path.append((number, divisor))
        number //= divisor
        step += 1
        print(f"Step {step}: {path[-1][0]} ÷ {divisor} = {number}")

    step += 1
    path.append((1, None))
    print(f"Step {step}: Reached 1")

    return path, original, step

def decode_path(path):
    """Decodes a number from its encoded path."""
    number = 1
    print("\nDecoding path...")
    for num, divisor in reversed(path):
        if divisor:
            number *= divisor
            print(f"Decoding: {number // divisor} * {divisor} = {number}")
        else:
            print("Final step: Reached 1")
    return number

def simulate_qubits(value, label):
    """Simulates a quantum register size based on bit length of a value."""
    X = value.bit_length()
    qubits = 2 ** X + 1

    print(f"\n{label} = {value}")
    print(f"Bit length X = {X}")
    print(f"Using 2^X + 1 = {qubits} qubits and X + 1 = {X + 1} quantum operations")

    qc = QuantumCircuit(qubits)
    for i in range(min(X + 1, qubits)):
        qc.h(i)  # Hadamard gate to simulate quantum operation
    print(qc.draw())

if __name__ == "__main__":
    start_number = int(input("Enter a number to encode: "))

    if start_number <= 1:
        print("Please enter a number greater than 1 for encoding.")
    else:
        encoded_path, original, total_steps = encode_until_one(start_number)

        print("\nEncoded path:")
        for i, (num, div) in enumerate(encoded_path):
            if div:
                print(f"Step {i+1}: {num} ÷ {div} = {num // div}")
            else:
                print(f"Step {i+1}: Reached 1")

        decoded = decode_path(encoded_path)
        print(f"\nDecoded number: {decoded}")
        print("Yes" if decoded == original else "No")

        print(f"\nFinal Result:")
        if len(encoded_path) >= 2:
            last_before_one = encoded_path[-2][0]
            print(f"Last non-1 number before division: {last_before_one}")
        else:
            last_before_one = 1
            print("Last non-1 number before division: 1")

        print(f"Divided in {total_steps} steps from {original}")

        # Simulate quantum register usage
        simulate_qubits(original, "Original Number")
        simulate_qubits(last_before_one, "Last Before One")
        simulate_qubits(total_steps, "Total Steps")