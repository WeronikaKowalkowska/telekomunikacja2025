
import numpy as np

def encoding(message):
    bit_list = [int(bit) for char in message for bit in format(ord(char), '08b')]  #konwertuje całą wiadomość na 8-bitowy zapis binarny

    #mnożymy macierz H przez wektor bit_list -> bity parzystości
    #result = [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]
    if len(bit_list) % 16 != 0:
        bit_list += [0] * (16 - (len(bit_list) % 16))

    result = []
    for i in range(0, len(bit_list), 16):  # podział na bloki po 16 bitów
        block = bit_list[i:i + 16]
        even_bits_list = np.dot(H_matrix, block) % 2
        result.extend(even_bits_list)
    #dodanie bity danych i parzystości w jednej tablicy wynikowej
    #result = [bit_list, even_bits_list]
        # #znajdź bity parzyste
        # if (pow(2,i))%2==0:
        #     #check_enen_bits(i)
        # else:

    return result

# def check_even_bits(position, message):
#
#     index=0
#     while index<len(message):
#         for i in range (position-1):
#             index+=1
#         for i in range (position):
#             #sprawdź parzystość
#
#
#
#     return 0

def decoding(encoded_message):
    encoded_text=0
    for i in range(encoded_message.size()):
        encoded_text+=bytes(encoded_message[i], encoding='utf-8')
    return encoded_text

# def verify_integrity(encoded_message, H_matrix):
#     for i in range(message.size()):
#         syndrome=(H_matrix*)
#     return 0

H_matrix=np.array([
    [1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0],
    [1,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0],
    [1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0],
    [0,1,0,1,0,1,1,0,0,0,0,1,0,0,0,0],
    [1,1,1,0,1,0,0,1,0,0,0,0,1,0,0,0],
    [1,0,0,1,0,1,0,1,0,0,0,0,0,1,0,0],
    [0,1,1,1,1,0,1,1,0,0,0,0,0,0,1,0],
    [1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,1]
],dtype=int) #8x16


text= input("Set text to encode: ")
print(encoding(text))
print(len(encoding(text)))
