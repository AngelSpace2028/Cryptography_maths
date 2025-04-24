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
    """Encodes a number by repeatedly dividing by its smallest divisor until 1 is reached."""
    original = number
    path = []
    step = 0

    print(f"Encoding {number} until it becomes 1...\n")

    while number > 1:
        divisor = find_divisor(number)
        path.append((number, divisor))
        number //= divisor
        step += 1
        print(f"Step {step}: P = {path[-1][0]}, Q = {divisor}, Result = {number}")

    step += 1
    path.append((1, None))
    print(f"Step {step}: Reached P = 1")

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
            print("Final step: Reached P = 1")
    return number


def simulate_quantum_register(value, label):
    """Simulates a quantum register for encoding with Qiskit."""
    X = value.bit_length()
    qubits = min(2 ** X + 1, 32)  # Cap the qubits for practical simulation
    #print(f"\nSimulating quantum register for {label} ({value}):")
    #print(f"Bit length X = {X}, Using 2^X + 1 = {qubits} qubits and X + 1 = {X + 1} quantum operations.\n")

    qc = QuantumCircuit(qubits)

    # Apply X gate to simulate encoding the number
    for i in range(X + 1):
        if (value >> i) & 1:
            qc.x(i)

    qc.barrier()

    # Add example operations (e.g., Hadamard for demonstration)
    for i in range(X + 1):
        qc.h(i)

    #print(qc.draw())


if __name__ == "__main__":
    start_number = int(input("Enter a number to encode (e.g., 11234567): "))

    if start_number <= 1:
        print("Please enter a number greater than 1 for encoding.")
    else:
        encoded_path, original, total_steps = encode_until_one(start_number)

        print("\nAll (P, Q) steps:")
        for i, (num, div) in enumerate(encoded_path):
            if div:
                print(f"Step {i + 1}: P = {num}, Q = {div}, P ÷ Q = {num // div}")
            else:
                print(f"Step {i + 1}: P = {num}, Reached P = 1")

        decoded = decode_path(encoded_path)
        print(f"\nDecoded back to: {decoded}")
        print("Success!" if decoded == original else "Failure!")

        print(f"\nFinal Result:")
        if len(encoded_path) >= 2:
            last_before_one = encoded_path[-2][0]
            last_Q = encoded_path[-2][1]
            print(f"Last P before reaching 1: {last_before_one}")
            print(f"Last Q when P = 1: J = {last_Q}")
        else:
            print("Last P before reaching 1: 1")
            print("No Q value, as we reached P = 1 immediately.")

        print(f"Total steps (U): {total_steps}")
        print(f"Original Number = {original}")

        simulate_quantum_register(original, "Original Number")
        simulate_quantum_register(last_before_one, "Last Before One")
        simulate_quantum_register(total_steps, "Total Steps")