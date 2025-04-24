import os
from qiskit import QuantumCircuit

def find_divisor(n):
    if n % 2 == 0:
        return 2
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return i
    return n


def encode_until_one(number):
    # Add a leading 1 to the binary representation of the number
    number |= (1 << (number.bit_length()))  # This adds a 1 to the front in binary

    path = []
    step = 0
    while number > 1:
        divisor = find_divisor(number)
        path.append((number, divisor))
        number //= divisor
        step += 1
    path.append((1, None))
    return path, step


def decode_path(path):
    number = 1
    for num, divisor in reversed(path):
        if divisor:
            number *= divisor
    # Remove the leading 1 added during encoding
    number >>= 1  # Shift right to remove the leading 1
    return number


def base256_write(filename, number):
    with open(filename, 'wb') as f:
        encoded = number.to_bytes((number.bit_length() + 7) // 8 or 1, 'big')
        f.write(encoded)


def base256_read(filename):
    with open(filename, 'rb') as f:
        data = f.read()
        return int.from_bytes(data, 'big')


def simulate_quantum_register(value, label):
    X = value.bit_length()
    qubits = min(2 ** X + 1, 32)
    qc = QuantumCircuit(qubits)
    for i in range(X + 1):
        if (value >> i) & 1:
            qc.x(i)
    qc.barrier()
    for i in range(X + 1):
        qc.h(i)
    # Uncomment to visualize: print(qc.draw())


if __name__ == "__main__":
    print("Quantum Divisor Encoder\n")
    choice = input("Enter 1 to encode, 2 to decode: ")

    if choice == '1':
        in_file = input("Enter input file with number: ")
        out_J_file = input("Enter output filename for J (last divisor): ")
        out_U_file = input("Enter output filename for U (steps): ")

        if not os.path.isfile(in_file):
            print("Input file does not exist.")
        else:
            number = base256_read(in_file)
            path, total_steps = encode_until_one(number)
            last_before_one = path[-2][0] if len(path) >= 2 else 1
            last_Q = path[-2][1] if len(path) >= 2 else 1

            base256_write(out_J_file, last_Q)
            base256_write(out_U_file, total_steps)

            simulate_quantum_register(number, "Original Number")
            simulate_quantum_register(last_before_one, "Last Before One")
            simulate_quantum_register(total_steps, "Total Steps")

            print(f"Encoded. Last Q (J): {last_Q}, Steps (U): {total_steps}")

    elif choice == '2':
        file_J = input("Enter J file (last divisor): ")
        file_U = input("Enter U file (steps): ")
        output_file = input("Enter output file to save the decoded number: ")

        if not os.path.isfile(file_J) or not os.path.isfile(file_U):
            print("One or both input files do not exist.")
        else:
            J = base256_read(file_J)
            U = base256_read(file_U)

            # Reconstruct the path by repeating the last divisor
            path = [(J, J)] * (U - 1) + [(1, None)]
            decoded = decode_path(path)

            base256_write(output_file, decoded)

            print(f"Decoded Number: {decoded}")
            print(f"Saved to {output_file}")

    else:
        print("Invalid selection.")