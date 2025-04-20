import numpy as np

# metoda do liczenia sumy kontrolnej CRC-16 z generatorem 0x1021 (2 bajty) - jeżeli odbiornik wyśle 'C'
def calculate_crc(data: bytes) -> int:
    crc = 0
    for byte in data:
        crc ^= byte << 8  # bajt z najwyższych 8 bitów
        for _ in range(8):  # iteracja po bitach
            if crc & 0x8000:  # jeżeli najwyższy bit CRC to 1
                crc = (crc << 1) ^ 0x1021  # przesunięcie i XOR z generatorem
            else:
                crc <<= 1  # przesunięcie
            crc &= 0xFFFF  # utrzymanie 16-bitowego wyniku
    return crc

# metoda obliczająca algebraiczną sumę kontrolną (1 bajt) - jeżeli odbiornik wyśle 'NAK'
def calculate_checksum(data):
    return sum(data) % 256

# funkcja nadajnika
def send_file():
    print("Opening 'file_to_read.txt'")
    with open("file_to_read.txt", 'r') as file:
        data = file.read()
    blockFromFile = []
    blockNumber = 0 # liczymy od zera, ponieważ metoda divide_to_blocks() zwiększa licznik

    # CZEKAJ aż odbiornik wyśle 'C' (oznacza żądanie transmisji z CRC)

    while data is not None:  # DOPÓKI są dane do wysłania
        '''CZYTAJ 128 bajtów z pliku
        JEŚLI mniej niż 128 bajtów:
            DOPEŁNIJ bajtami 0x1A (znak EOF) '''
        blockFromFile, data, blockNumber = divide_to_blocks(data, blockNumber)
        if len(blockFromFile) < 128:
            missingLength = 128 - len(blockFromFile)
            for i in range(missingLength):
                blockFromFile.append(0x1A)

        '''POLICZ CRC dla danych
        UTWÓRZ blok (133 bajty):
            SOH (0x01)
            numer bloku
            dopełnienie numeru bloku (255 - numer bloku)
            dane (128 bajtów)
            CRC (2 bajty) '''
        crc = calculate_crc(blockFromFile)
        '''0x01 – SOH (Start of Header)
           [crc >> 8, crc & 0xFF] - rozdzielenie 16-bitowego CRC na dwa bajty'''
        block_to_send = [0x01, blockNumber, 255 - blockNumber] + blockFromFile + [crc >> 8, crc & 0xFF]

        # WYŚLIJ cały blok

        '''ODBIERZ odpowiedź od odbiornika:
            JEŚLI ACK:
                ZWIĘKSZ block_number
            JEŚLI NAK:
                POWTÓRZ wysyłanie bloku'''


        '''WYŚLIJ znak EOT (0x04)
        CZEKAJ na ACK od odbiornika
        ZAKOŃCZ'''


# funkcja odbiornika
def recive_file():

    # WYSYŁA 'C' lub NAK do nadajnika
    sum_method = None #wybrana metoda sumy kontrolnej

    '''Odbiera bloki danych i sprawdza:
           * Numer bloku i jego uzupełnienie
           * Sumę kontrolną lub CRC'''

    isEOT = False #czy koniec transmisji
    while isEOT:
        # Odbiera bloki i przypisuje do recived_block
        recived_block = []
        if recived_block[0] != 0x01:
            return "Błąd: Brak SOH"
        block_number = recived_block[1]
        block_complement = recived_block[2]
        if block_number + block_complement != 0xFF: #musi być równe 255
            return "Błąd: Nieprawidłowy numer bloku"
        data = recived_block[3:3 + 128]  #od 3 do 130 bajta mamy dane
        # Odpowiada ACK jeśli OK, NAK jeśli nie
        if sum_method == 'C':
            crc_received = (recived_block[131] << 8) | recived_block[132]  # CRC z bloku (2 bajty) - połączone razem
            crc_calculated = calculate_crc(data)
            if crc_received != crc_calculated:
                return "Błąd: CRC niepoprawne"
            else:
                return "OK: Blok poprawny"
        if sum_method == 'NAK':
            checksum_received = recived_block[131]
            checksum_calculated = sum(data) % 256 # od 3 do 130 bajta mamy dane
            if checksum_received != checksum_calculated:
                return "Błąd: Suma kontrolna niepoprawna"
            else:
                return "OK: Blok poprawny"

    #Po otrzymaniu EOT kończy odbiór


# metoda czytająca pojedynczy blok i zwracająca resztę
def divide_to_blocks(data, blockNumber):
    block_data = data[:128]
    remaining_data = data[128:]
    block_bytes = [ord(ch) for ch in block_data]  # zamiana znaków na bajty
    return block_bytes, remaining_data, blockNumber + 1

# main:
