import numpy as np

def encoding(message):
    wynik = np.array()
    for i in range(message.size()):
        wynik[i] = bytes(message[i], encoding='utf-8') #zamiana tektu na tablice bajtów

    return wynik
def decoding(encoded_message):
    encoded_text=0
    for i in range(encoded_message.size()):
        encoded_text+=bytes(encoded_message[i], encoding='utf-8')
    return encoded_text
def verify_integrity():
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

