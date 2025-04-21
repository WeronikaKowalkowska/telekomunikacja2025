import numpy as np
import serial
import time
import serial.tools.list_ports
SOH = 0x01
EOT = 0x04
ACK = 0x06
NAK = 0x15
C = 0x43  # ASCII 'C'

BLOCK_SIZE = 128

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
def send_file(ser):
    print("Opening 'file_to_read.txt'")
    with open("file_to_read.txt", 'r') as file:
        data = file.read()

    blockNumber = 1

    # CZEKAJ aż odbiornik wyśle 'C' (oznacza żądanie transmisji z CRC)
    print("czekam na znak odbiornika: ")
    time.sleep(4)
    wait = ser.read()
    print("otrzymano: ",wait)
    if wait == bytes([0x43]):

        while data is not None:  # DOPÓKI są dane do wysłania:
            '''
            CZYTAJ 128 bajtów z pliku
            JEŚLI mniej niż 128 bajtów:
                DOPEŁNIJ bajtami 0x1A (znak EOF)
            '''
            blockFromFile = []
            blockFromFile, data, blockNumber = divide_to_blocks(data, blockNumber)
            if len(blockFromFile) < 128:
                missingLength = 128 - len(blockFromFile)
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
            crc = calculate_crc(blockFromFile)
            #block_to_send = [0x01, blockNumber, 255 - blockNumber, blockFromFile, crc]
            block_to_send = bytearray()
            block_to_send.append(0x01)
            block_to_send.append(blockNumber)
            block_to_send.append(255 - blockNumber)
            block_to_send += bytearray(blockFromFile)
            block_to_send += crc.to_bytes(2, 'big')  # CRC to int, konwertujemy na 2 bajty
            ser.write(block_to_send)
            # WYŚLIJ cały blok
            ser.write(block_to_send)
            '''
            ODBIERZ odpowiedź od odbiornika:
                JEŚLI ACK:
                    ZWIĘKSZ block_number
                JEŚLI NAK:
                    POWTÓRZ wysyłanie bloku
            '''
            response = ser.read()
            if response == 'ACK' or response == 0x06:
                blockNumber = blockNumber + 1
            elif response == 'NAK' or response == 0x015:
                ser.write(block_to_send)

            '''
            WYŚLIJ znak EOT (0x04)
            CZEKAJ na ACK od odbiornika
            ZAKOŃCZ
            '''
        ser.write(bytes([0x04]))
        print("File sent successfully")
    print("blad")

# funkcja odbiornika
def receive_file(ser):
    print("Opening 'file_to_recive.txt'")
    with open("file_to_recive.txt", 'a') as file:
        expectedBlockNumber = 1
        C_sign=bytes([0x43])
        ser.write(C_sign)
        print("wyslano ",C_sign)
        while True:
            '''
             ODBIERZ pierwszy bajt

            JEŚLI bajt to SOH (0x01):
            ODCZYTAJ numer bloku
            ODCZYTAJ dopełnienie numeru bloku
            JEŚLI numer bloku + dopełnienie != 255:
                WYŚLIJ NAK
                KONTYNUUJ'''
            header = ser.read(1)
            blockNum = 0
            if header == bytes([SOH]):
                blockNum = ser.read(1)[0]
                block_num_comp = ser.read(1)[0]
                if blockNum != 0xFF - block_num_comp:
                    print("Nieprawidłowy nagłówek bloku.")
                    ser.write(bytes([NAK]))
                    # continue
                '''
                ODCZYTAJ 128 bajtów danych
                ODCZYTAJ CRC (2 bajty)
                POLICZ CRC z danych
                JEŚLI CRC się nie zgadza:
                    WYŚLIJ NAK
                    KONTYNUUJ'''
                block = ser.read(128)
                readCrc = ser.read(2)
                calculatedCrc = calculate_crc(block)
                if readCrc != calculatedCrc:
                    print("Nieprawidłowy nagłówek bloku.")
                    ser.write(bytes([NAK]))
                '''JEŚLI numer bloku == expected_block_number:
                    ZAPISZ dane do pliku
                    ZWIĘKSZ expected_block_number

                WYŚLIJ ACK'''
                if blockNum == expectedBlockNumber:
                    print("Saving recived contant into 'file_to_recive.txt'.")
                    with open("file_to_recive.txt", 'a') as file:
                        file.write(block)
                ser.write(0x06)
            '''JEŚLI bajt to EOT (0x04):
            WYŚLIJ ACK
            PRZERWIJ'''
            if header == bytes([EOT]):
                ser.write(0x06)
                print("File received successfully")
                break
                return None
        '''ZAMKNIJ plik'''
        file.close()
    print("File received successfully")

# # metoda czytająca pojedynczy blok i zwracająca resztę
# def divide_to_blocks(data, blockNumber):
#     block_data = data[:128]
#     remaining_data = data[128:]
#     block_bytes = [ord(ch) for ch in block_data]  # zamiana znaków na bajty
#     return block_bytes, remaining_data, blockNumber + 1
def divide_to_blocks(data, blockNumber):
    block_data = data[:128]
    remaining_data = data[128:]
    block_bytes = []
    for ch in block_data:
        try:
            block_bytes.append(ord(ch))
        except TypeError:
            print(f"Błąd: {ch} nie jest znakiem.")
    return block_bytes, remaining_data, blockNumber + 1

# main:
# port = input("Port szeregowy (np. COM3 / /dev/ttyUSB0): ")
# ser = serial.Serial(port, 9600)

# znajdź wszystkie dostępne porty szeregowe
disconected = True

# konfiguracja RS-232
CONFIG = {
    'baudrate': 9600,
    'bytesize': serial.EIGHTBITS,
    'parity': serial.PARITY_NONE,
    'stopbits': serial.STOPBITS_ONE,
    'timeout': 1,
    'xonxoff': False,
    'rtscts': False,
    'dsrdtr': False
}

ports = list(serial.tools.list_ports.comports())

if not ports:
    print("Nie znaleziono żadnych portów szeregowych.")
    exit()

# wyświetl dostępne porty
print("Dostępne porty szeregowe:")
for i, port in enumerate(ports):
    print(f"{i}: {port.device}")

# wybór portu przez użytkownika
while True:
    try:
        index = int(input("Wybierz numer portu z listy: "))
        selected_port = ports[index].device
        break
    except (ValueError, IndexError):
        print("Nieprawidłowy wybór, spróbuj ponownie.")

# otwarcie portu
while disconected:
    try:
        ser = serial.Serial(selected_port, 9600)
        print(f"Połączono z {selected_port}")
        disconected = False
    except serial.SerialException as e:
        print(f"Błąd podczas otwierania portu: {e}")

mode = input("Wpisz 'send' by wysłać lub 'recv' by odebrać plik: ").strip().lower()

#filename = input("Podaj nazwę pliku: ")

if mode == "send":
    send_file(ser)
elif mode == "recv":
    receive_file(ser)
else:
    print("Nieznany tryb.")

ser.close()