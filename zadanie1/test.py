# import random
#
import numpy as np

from zadanie1.nowy import correct_errors

#
# H_matrix=np.array([
#     [1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0],
#     [1,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0],
#     [1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0],
#     [0,1,0,1,0,1,1,0,0,0,0,1,0,0,0,0],
#     [1,1,1,0,1,0,0,1,0,0,0,0,1,0,0,0],
#     [1,0,0,1,0,1,0,1,0,0,0,0,0,1,0,0],
#     [0,1,1,1,1,0,1,1,0,0,0,0,0,0,1,0],
#     [1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,1]
# ],dtype=int) #8x16
#
# def encoding(message):
#     even_bits_in_message = []
#     all_signs=[]
#     for i in range(len(message)):
#         sign=format(ord(message[i]), '08b')
#         all_signs.append(sign)
#         even_bits_in_message.append(check_even_bits(sign))
#         '''print(sign)
#         print(check_even_bits(sign))
#         print(even_bits_in_message)
#         print("\n")'''
#     return all_signs,even_bits_in_message
#
# def check_even_bits(sign):
#     result=0
#     for i in range(len(sign)):
#         result=result^int(sign[i])
#     return result;  #result=1-> w znaku jest nieparzysta liczba 1 , result=0-> w znaku jest parzysta liczba 1
#
#
# def destroy_bits(message):  # message to ciąg bitów
#     howMuch = int(input("How much bits do you want to destroy? "))
#
#     if howMuch > len(message):
#         print("Too many bits selected!")
#         return message
#
#     option = input("Choose '1' for randomised indexing and '2' for static indexing (random is default): ")
#     index = []
#
#     if option == '2':
#         for i in range(howMuch):
#             test = True
#             while test:
#                 input_index = int(input("Choose which bit you want to destroy: "))
#                 if input_index in index:
#                     print("You've already destroyed this bit. Choose another one.")
#                 elif 0 <= input_index < len(message):  # Sprawdzenie zakresu indeksu
#                     test = False
#                 else:
#                     print("Index out of range! Try again.")
#             index.append(input_index)
#     else:
#         while len(index) < howMuch:
#             random_index = random.randrange(0, len(message))
#             if random_index not in index:
#                 index.append(random_index)
#
#     # Zamień wybrane bity na przeciwne
#     for i in index:
#         #int(message[i] = int(message[i])^int(message[i])  # XOR z 1 zmienia bit na przeciwny
#         #message[i]=message[i]^message[i]
#         if(message[i] == 1):
#             message[i] = 0
#         else:
#             message[i] = 1
#     return message
#
# '''def contains(message,sign):
#     for i in range(len(message)):
#         if(sign==message[i]):
#             return True
#
#     return False'''
#
# def verify_integrity(message):
#     all_signs=[]
#     for i in range(len(message)):
#         sign=format(ord(message[i]), '08b')
#         syndrome=multiply(sign)%2
#         h_transposition=np.transpose(H_matrix)
#         index=None;
#         #multiply(sign)
#         print("Syndrome:",syndrome)
#         if syndrome!=0:
#             #zidentyfikuj błędny bit (porównaj z kolumnami h)
#             #test = True
#             for i in range(16):
#                 test=True
#                 for j in range(8):
#                     if h_transposition[i][j] != syndrome[j]:
#                         test=False
#                 if test==True:
#                     index=i
#             if(index!=None):
#                 #znaleziono ktory bit jest bledny -> napraw bit (zmien bit )
#                 sign[index]^=1
#         all_signs.append(sign)
#     return all_signs
#
# def multiply(sign):
#     result=[[0] * 16 for _ in range(8)]
#     for col in range(16):
#         for row in range(8):
#             result[row][col] = H_matrix[row][col] * sign[row]
#     return result
#
# all_signs=[]
# even_bits_in_message=[]
# all_signs,even_bits_in_message=encoding("hejka")
# print(all_signs)
# print("\n")
# bit_list = [int(bit) for char in "hejka" for bit in format(ord(char), '08b')]
# verify_integrity("hejka")

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

    bit_array = np.array(bit_list).reshape(-1, 8)  #przekształcamy tablicę w macierz bitów po 8

    encoded = np.dot(bit_array, G_matrix) % 2 #mnożenie wektora i macierzy

    return encoded.flatten()    #zwracenie wyniku jak jednowymiarowej tablicy

#bity parzystości to ostatnie 8 bitów w zakodowanym ciągu
def remove_parity_bits(corrected_bits):
    return corrected_bits[:8]

def corrected_to_text(encoded_bits):
    encoded_array = np.array(encoded_bits).reshape(-1, 16)
    decoded_message = []

    for row in encoded_array:
        print(len(row))
        #usunięcie bitów parzystości z segmentu
        data_bits = remove_parity_bits(row)
        print(len(data_bits))
        #zamiana segmentu na znak ASCII
        byte_str = ''.join(map(str, data_bits))
        decoded_message.append(chr(int(byte_str, 2)))

    return ''.join(decoded_message)

bit_list = [int(bit) for char in "hello" for bit in format(ord(char), '08b')]
print("Oryginał:", bit_list)
print(len(bit_list))
text_byte = encoding("hello")
print("Oryginał po zakodowaniu:", text_byte)

print("Tekst po dekodowaniu:", corrected_to_text(text_byte))


# def corrected_to_text(corrected_message):
#     text = ""
#     byte_list_no_parity = []
#     byte_list = np.array(corrected_message).reshape(-1, 16)  #dzielę po 8 bitów, każdy znak
#     for row in byte_list:
#         row = remove_parity_bits(row)
#         byte_list_no_parity.append(row)
#     byte_list_no_parity = np.array(byte_list_no_parity).reshape(-1, 8)
#     for row in byte_list_no_parity:
#         byte_str = ''.join(map(str, row))  #zamiana bitów na ciąg tekstowy np. '10101010'
#         byte_int = int(byte_str, 2)     #zamiana ciągu binarnego na liczbę dziesiętną np. '10101010' -> 170
#         text += chr(byte_int)          #zamiana liczby dziesiętnej na znak np. 170 -> 'a'
#     return text