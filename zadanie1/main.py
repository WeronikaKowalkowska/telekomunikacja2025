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

    while len(bit_list) % 8 != 0:  #jeżeli liczba bitów nie wielokrotność 8 to dodajemy zera
        bit_list.append(0)

    bit_array = np.array(bit_list).reshape(-1, 8)  #przekształcamy tablicę w macierz bitów po 8

    encoded = np.dot(bit_array, G_matrix) % 2 #mnożenie wektora i macierzy

    return encoded.flatten()    #zwracenie wyniku jak jednowymiarowej tablicy

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

    return message_copy

def find_error_bit(syndrome):
    if np.array_equal(syndrome, np.zeros(8, dtype=int)):
        return None

        #sprawdzenie pojedynczego błędu
    for index, column in enumerate(H_matrix.T):
        if np.array_equal(syndrome, column):
            return [index]  #zwracamy listę z jednym indeksem

        #sprawdzenie kombinacji dwóch błędów
    for i in range(H_matrix.shape[1]):
        for j in range(i + 1, H_matrix.shape[1]):
            if np.array_equal(syndrome, (H_matrix[:, i] + H_matrix[:, j]) % 2):
                return [i, j]  #zwracamy indeksy dwóch błędnych bitów

def check_if_correct(message):
    bit_numeration_for_error = 0  #globalna zmienna dla całego teksu a nie tylko bloku

    message = np.array(message).reshape(-1, 16)  #przekształcamy tablicę w macierz bitów po 16, bo "słowo danych" ma 8 bitów, ale po zakodowaniu powstaje blok 16-bitowy

    for row in message:
        syndrome = np.dot(H_matrix, row.T) % 2  #row jest wektorem poziomym, a chcemy mieć pionowy dlatego jest transponowany

        error_bit = find_error_bit(syndrome)
        global_bit_index = []

        if error_bit is not None:
            if len(error_bit) > 1:
                for i in range(len(error_bit)):
                    global_bit_index.append(error_bit[i] + bit_numeration_for_error)
            else:
                global_bit_index.append(error_bit[0] + bit_numeration_for_error)
            print(f"Error in bit at index: {global_bit_index}")
            #naprawienie bitu
            row[error_bit] ^= 1  #XOR z 1 zmienia bit na przeciwny

        bit_numeration_for_error += 16

    return message.flatten()


def is_correct(original_message, corrected_message):
    original_message = list(original_message)
    corrected_message = list(corrected_message)
    return original_message == corrected_message


def choose_operation():
    print("Choose operation type: (default is encoding)")
    print("a) encoding: ")
    print("b) decoding: ")
    operation_choice = input("Choose operation: ")
    if operation_choice == 'b':
        choose_input()
    else:
        choose_input()



def choose_input():
    print("Choose input type: (default is direct text)")
    print("a) text file: ")
    print("b) direct text: ")
    input_choice = input("Choose input: ")
    if input_choice == 'a':
        print("Choose file: ")
        print("a) plain_file.txt")
        print("b) encoded_file.txt")

        test=True
        while test:
            choice = input("Your choice: ")
            if(choice == 'a'):



    else:
        text=input("Your text:")


text = "hello"
encoded_text = encoding(text)
print("Encoded text:")
print(encoded_text)
print("\n")
destroyed_text = destroy_bits(encoded_text)
print("Destroyed text:")
print(destroyed_text)
print("\n")
corrected_text = check_if_correct(destroyed_text)
print("Corrected text:")
print(corrected_text)
print("Is correct:", is_correct(encoded_text, corrected_text))