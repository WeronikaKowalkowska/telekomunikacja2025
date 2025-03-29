from email import message

import numpy as np

def encoding(message):
    wynik = np.array()
    for i in range(message.size()):
        wynik[i] = bytes(message[i], encoding='utf-8') #zamiana tektu na tablice bajtów
        #znajdź bity parzyste
        if (pow(2,i))%2==0:
            #check_enen_bits(i)
        else:


    return wynik

'''def check_enen_bits(position, message):

    index=0
    while index<len(message):
        for i in range (position-1):
            index+=1
        for i in range (position):
            #sprawdź parzystość



    return 0'''

def decoding(encoded_message):
    encoded_text=0
    for i in range(encoded_message.size()):
        encoded_text+=bytes(encoded_message[i], encoding='utf-8')
    return encoded_text

def verify_integrity(encoded_message, H_matrix):
    for i in range(message.size()):
        syndrome=(H_matrix*)
    return 0

H_matrix=np.array([
    [1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0],
    [1,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0],
    [1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0],
    [0,1,0,1,0,1,1,0,0,0,0,1,0,0,0,0],
    [1,1,1,0,1,0,0,1,0,0,0,0,1,0,0,0],
    [1,0,0,1,0,1,0,1,0,0,0,0,0,1,0,0],
    [0,1,1,1,1,0,1,1,0,0,0,0,0,0,1,0],
    [1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,1]
],dtype=int)


text= input("Set text to encode: ")

