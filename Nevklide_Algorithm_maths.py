from qiskit import QuantumCircuit

def find_divisor(n):
    """Finds the smallest divisor of n greater than 1."""
    if n % 2 == 0:
        return 2
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return i
    return n  # n is prime

def encode_until_one(number):
    """Encodes by repeatedly dividing by the smallest divisor until reaching 1."""
    original = number
    path = []
    step = 0

    print(f"Encoding {number} until it becomes 1...\n")

    while number > 1:
        divisor = find_divisor(number)
        path.append((number, divisor))  # Save P and Q
        step += 1
        print(f"Step {step}: P = {number}, Q = {divisor}, Result = {number // divisor}")
        number //= divisor

    print(f"Total steps: {step}")
    return path, step

def decode_path(path):
    """Decodes number from path."""
    number = 1
    print("\nDecoding path:")
    for p, q in reversed(path):
        number *= q
        print(f"{number // q} * {q} = {number}")
    return number

def simulate_qubits(value, label):
    """Simulate qubits based on bit length."""
    X = value.bit_length()
    qubits = 2 ** X + 1

    print(f"\n{label} = {value}")
    print(f"Bit length X = {X}")
    print(f"Using 2^X + 1 = {qubits} qubits and X + 1 = {X + 1} quantum operations\n")

    qc = QuantumCircuit(qubits)
    for i in range(min(X + 1, qubits)):
        qc.h(i)
    print(qc.draw())

if __name__ == "__main__":
    start_number = int(input("Enter a number to encode (e.g., 13751): "))

    if start_number <= 1:
        print("Please enter a number greater than 1.")
    else:
        path, total_steps = encode_until_one(start_number)

        print("\nAll (P, Q) steps:")
        for i, (p, q) in enumerate(path, 1):
            print(f"Step {i}: P = {p}, Q = {q}, P ÷ Q = {p // q}")

        decoded = decode_path(path)
        print(f"\nDecoded back to: {decoded}")
        print("Success!" if decoded == start_number else "Mismatch!")

        # Last P before 1
        last_p = path[-1][0] if path else 1
        print(f"\nLast P before reaching 1: {last_p}")
        print(f"Total steps taken: {total_steps}")

        # Simulate quantum logic
        simulate_qubits(start_number, "Original Number")
        simulate_qubits(last_p, "Last P Before 1")
        simulate_qubits(total_steps, "Total Steps")