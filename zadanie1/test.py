import random

import numpy as np

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

def encoding(message):
    even_bits_in_message = []
    all_signs=[]
    for i in range(len(message)):
        sign=format(ord(message[i]), '08b')
        all_signs.append(sign)
        even_bits_in_message.append(check_even_bits(sign))
        '''print(sign)
        print(check_even_bits(sign))
        print(even_bits_in_message)
        print("\n")'''
    return all_signs,even_bits_in_message

def check_even_bits(sign):
    result=0
    for i in range(len(sign)):
        result=result^int(sign[i])
    return result;  #result=1-> w znaku jest nieparzysta liczba 1 , result=0-> w znaku jest parzysta liczba 1


def destroy_bits(message):  # message to ciąg bitów
    howMuch = int(input("How much bits do you want to destroy? "))

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
                elif 0 <= input_index < len(message):  # Sprawdzenie zakresu indeksu
                    test = False
                else:
                    print("Index out of range! Try again.")
            index.append(input_index)
    else:
        while len(index) < howMuch:
            random_index = random.randrange(0, len(message))
            if random_index not in index:
                index.append(random_index)

    # Zamień wybrane bity na przeciwne
    for i in index:
        #int(message[i] = int(message[i])^int(message[i])  # XOR z 1 zmienia bit na przeciwny
        #message[i]=message[i]^message[i]
        if(message[i] == 1):
            message[i] = 0
        else:
            message[i] = 1
    return message

'''def contains(message,sign):
    for i in range(len(message)):
        if(sign==message[i]):
            return True

    return False'''

def verify_integrity(message):
    all_signs=[]
    for i in range(len(message)):
        sign=format(ord(message[i]), '08b')
        syndrome=multiply(sign)%2
        h_transposition=np.transpose(H_matrix)
        index=None;
        #multiply(sign)
        print("Syndrome:",syndrome)
        if syndrome!=0:
            #zidentyfikuj błędny bit (porównaj z kolumnami h)
            #test = True
            for i in range(16):
                test=True
                for j in range(8):
                    if h_transposition[i][j] != syndrome[j]:
                        test=False
                if test==True:
                    index=i
            if(index!=None):
                #znaleziono ktory bit jest bledny -> napraw bit (zmien bit )
                sign[index]^=1
        all_signs.append(sign)
    return all_signs





def multiply(sign):
    '''print(sign)
    sign=np.transpose(sign)  #chyba nie ma zadnego efektu na wektor
    print(sign)
    print("\n")'''
    result=[[0] * 16 for _ in range(8)]
    for col in range(16):
        for row in range(8):
            result[row][col] = H_matrix[row][col] * sign[row]
    #result = np.dot(H_matrix, sign)
    return result

all_signs=[]
even_bits_in_message=[]
all_signs,even_bits_in_message=encoding("hejka")
print(all_signs)
print("\n")
bit_list = [int(bit) for char in "hejka" for bit in format(ord(char), '08b')]
#print(destroy_bits(bit_list))
verify_integrity("hejka")

