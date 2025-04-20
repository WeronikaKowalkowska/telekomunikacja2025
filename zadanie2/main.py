import numpy as np

def calculate_crc(data: bytes) -> int:
    crc = 0
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF  # Utrzymanie 16-bitowego wyniku
    return crc

def send_file():
    print("Opening 'file_to_read.txt'")
    with open("file_to_read.txt", 'r') as file:
        data = file.read()
    #data=divide_to_blocks(data)
    blockNumber=1

    #CZEKAJ aż odbiornik wyśle 'C' (oznacza żądanie transmisji z CRC)

    while data is not None: #DOPÓKI są dane do wysłania:
        '''
        CZYTAJ 128 bajtów z pliku
        JEŚLI mniej niż 128 bajtów:
            DOPEŁNIJ bajtami 0x1A (znak EOF)
        '''
        blockFromFile=[]
        blockFromFile,data,blockNumber=divide_to_blocks(data, blockNumber)
        if len(blockFromFile)<128:
            missingLength=128-len(blockFromFile)
            for i in range(missingLength):
                blockFromFile.append(0x1A)
        '''
        POLICZ CRC dla danych
        UTWÓRZ blok:
            SOH (0x01)
            numer bloku
            dopełnienie numeru bloku (255 - numer bloku)
            dane (128 bajtów)
            CRC (2 bajty)
        '''
        crc=calculate_crc(blockFromFile)
        block_to_send=[0x01,blockNumber,255-blockNumber,blockFromFile,crc]
        #WYŚLIJ cały blok
        '''
        ODBIERZ odpowiedź od odbiornika:
            JEŚLI ACK:
                ZWIĘKSZ block_number
            JEŚLI NAK:
                POWTÓRZ wysyłanie bloku
        '''
        '''
        WYŚLIJ znak EOT (0x04)
        CZEKAJ na ACK od odbiornika
        ZAKOŃCZ
        '''

def recive_file():
    return None

def divide_to_blocks(data,blockNumber): #musi zmniejszac data o block
    block=[]
    blockNumber=blockNumber+1
    return block,data,blockNumber


#main: