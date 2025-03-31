import random
import numpy as np

def main():
    operation = input("Podaj operację (zakodowanie/odkodowanie): ")
    if operation == "zakodowanie":
        message = input("Wprowadź wiadomość do zakodowania: ")
        encoded_message = kodowanie(message)
        print("Zakodowana wiadomość:", encoded_message)
    elif operation == "odkodowanie":
        encoded_message = input("Wprowadź wiadomość do odkodowania: ")
        h_matrix = np.identity(8, dtype=int)  # Przykładowa macierz parzystości
        decoded_message = dekodowanie(encoded_message, h_matrix)
        print("Odkodowana wiadomość:", decoded_message)

def kodowanie(message):
    h_matrix = np.identity(8, dtype=int)  # Przykładowa macierz parzystości
    encoded_result = []
    for char in message:
        bits = format(ord(char), '08b')  # 8-bitowa reprezentacja
        data_bits = [int(bit) for bit in bits]
        parity_bits = np.dot(h_matrix, data_bits) % 2
        encoded_result.append(bits + ''.join(map(str, parity_bits)))
    return ''.join(encoded_result)

def kodujaca(encoded_message):
    modified_message = list(encoded_message)
    random_index = random.randint(0, len(modified_message) - 1)
    modified_message[random_index] = '1' if modified_message[random_index] == '0' else '0'
    return ''.join(modified_message)

def sprawdz_poprawnosc(encoded_message, h_matrix):
    corrected_message = []
    for i in range(0, len(encoded_message), 16):  # Długość pojedynczego bloku (8+8)
        word = encoded_message[i:i + 16]
        data_bits = list(map(int, word[:8]))
        parity_bits = list(map(int, word[8:]))
        syndrome = np.dot(h_matrix, data_bits) % 2
        if np.any(syndrome):
            error_index = np.where((h_matrix.T == syndrome).all(axis=1))[0]
            if error_index.size > 0:
                data_bits[error_index[0]] ^= 1
        corrected_message.append(''.join(map(str, data_bits)))
    return ''.join(corrected_message)

def dekodowanie(encoded_message, h_matrix):
    corrected_message = []
    for i in range(0, len(encoded_message), 16):  # Długość pojedynczego bloku (8+8)
        word = encoded_message[i:i + 16]
        data_bits = word[:8]
        corrected_message.append(chr(int(data_bits, 2)))
    return ''.join(corrected_message)

if __name__ == "__main__":
    main()
