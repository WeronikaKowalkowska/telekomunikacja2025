import numpy as np
import random

def generate_h_matrix():
    return np.array([
        [1, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 1],
        [0, 1, 1, 1, 0, 0, 0]
    ])

def encode_character(char, H):
    data_bits = [int(b) for b in format(ord(char), '07b')]
    parity_bits = (H @ data_bits) % 2
    return np.append(data_bits, parity_bits)

def encode_text(text):
    H = generate_h_matrix()
    encoded_bits = np.concatenate([encode_character(char, H) for char in text])
    return encoded_bits.astype(int)

def introduce_error(encoded_bits):
    index = random.randint(0, len(encoded_bits) - 1)
    encoded_bits[index] = 1 - encoded_bits[index]
    return encoded_bits

def correct_errors(encoded_bits):
    H = generate_h_matrix()
    corrected_bits = encoded_bits.copy()
    for i in range(0, len(corrected_bits), 10):
        word = corrected_bits[i:i+10]
        syndrome = (H @ word[:7] % 2)
        if np.any(syndrome):
            error_pos = np.where((H.T == syndrome).all(axis=1))[0]
            if error_pos.size > 0:
                corrected_bits[i + error_pos[0]] ^= 1
    return corrected_bits

def decode_text(encoded_bits):
    decoded_chars = []
    for i in range(0, len(encoded_bits), 10):
        data_bits = encoded_bits[i:i+7]
        char_code = int(''.join(map(str, data_bits)), 2)
        decoded_chars.append(chr(char_code))
    return ''.join(decoded_chars)

def main():
    choice = input("Wybierz operację: (1) Kodowanie, (2) Dekodowanie: ")
    if choice == '1':
        text = input("Podaj tekst do zakodowania: ")
        encoded_bits = encode_text(text)
        print("Zakodowane dane:", ''.join(map(str, encoded_bits)))
    elif choice == '2':
        encoded_input = input("Podaj zakodowane dane: ")
        encoded_bits = np.array([int(b) for b in encoded_input])
        corrected_bits = correct_errors(encoded_bits)
        decoded_text = decode_text(corrected_bits)
        print("Odkodowany tekst:", decoded_text)
    else:
        print("Nieprawidłowy wybór.")

if __name__ == "__main__":
    main()
