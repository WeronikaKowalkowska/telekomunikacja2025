import random

import numpy as np

H_matrix = np.array([
        [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    ], dtype=int)  # 8x16

def encoding(message):

    I_8 = np.eye(8, dtype=int)  #macierz jednostkowa 8x8
    P = H_matrix[:, :8].T  #pierwsze 8 kolumn H, transponowane

    G_matrix = np.hstack((I_8, P))  #połączenie macierzy I_8 i P -> wynik to macierz do kodowania

    bit_list = [int(bit) for char in message for bit in format(ord(char), '08b')] #znak w wiadomości jest zamieniany na jego 8-bitowy zapis binarny

    encoded = np.dot(bit_list, G_matrix) % 2 #mnożenie wektora i macierzy

    return encoded    #zwracenie wyniku jak jednowymiarowej tablicy

def destroy_bits(message):  #message to ciąg bitów
    howMuch = int(input("How much bits do you want to destroy? "))
    message_copy = message.copy()

    if howMuch > len(message):
        print("Too many bits selected!")
        return message

    option = input("Choose '1' for randomised indexing and '2' for static indexing (random is default): ")
    index = []

    if option == '2':
        for i in range(howMuch):
            test = True
            while test:
                input_index = int(input("Choose which bit you want to destroy: "))
                if input_index in index:
                    print("You've already destroyed this bit. Choose another one.")
                elif 0 <= input_index < len(message):  #sprawdzenie zakresu indeksu
                    test = False
                else:
                    print("Index out of range! Try again.")
            index.append(input_index)
    else:
        while len(index) < howMuch:
            random_index = random.randrange(0, len(message))
            if random_index not in index:
                index.append(random_index)

    #zamień wybrane bity na przeciwne
    for i in index:
        message_copy[i] ^= 1 #XOR z 1 zmienia bit na przeciwny

    return message_copy,howMuch

def find_error_bit(syndrome, H_matrix):
    if np.array_equal(syndrome, np.zeros(H_matrix.shape[0], dtype=int)):
        return None

        # Sprawdzenie pojedynczego błędu
    for index, column in enumerate(H_matrix.T):
        if np.array_equal(syndrome, column):
            return [index]  # Zwracamy listę z jednym indeksem

        # Sprawdzenie kombinacji dwóch błędów
    for i in range(H_matrix.shape[1]):
        for j in range(i + 1, H_matrix.shape[1]):
            if np.array_equal(syndrome, (H_matrix[:, i] + H_matrix[:, j]) % 2):
                return [i, j]  # Zwracamy indeksy dwóch błędnych bitów

def check_if_correct(message,howMuch):

    for i in range(howMuch):
        message=check_again(message)


    return message

def check_again(message):
    syndrome = (np.dot(H_matrix, message.T) % 2).flatten()

    print(f"Syndrom: {syndrome}")

    error_bit = find_error_bit(syndrome, H_matrix)

    if error_bit is not None:
        print(f"Błąd w bicie o indeksie: {error_bit}")
        # naprawienie bitu
        message[error_bit] ^= 1  # XOR z 1 zmienia bit na przeciwny
    else:
        print("Brak błędu lub nierozpoznany syndrom.")
    return message


def is_correct(original_message, corrected_message):
    original_message = list(original_message)
    corrected_message = list(corrected_message)
    for i in range(len(original_message)):
        if original_message[i] != corrected_message[i]:
            return False
    return True

text = "j"
encoded_text = encoding(text)
print("Encoded text:")
print(encoded_text)
print("\n")
destroyed_text,howMuch = destroy_bits(encoded_text)
print("Destroyed text:")
print(destroyed_text)
print("\n")
corrected_text = check_if_correct(destroyed_text,howMuch)
print("Corrected text:")
print(corrected_text)
print("Is correct:")
print(is_correct(encoded_text, corrected_text))