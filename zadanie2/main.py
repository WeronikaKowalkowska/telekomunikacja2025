import numpy as np
import serial

SOH = 0x01
EOT = 0x04
ACK = 0x06
NAK = 0x15
C = 0x43  # ASCII 'C'

BLOCK_SIZE = 128


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


def send_file(ser):
    print("Opening 'file_to_read.txt'")
    with open("file_to_read.txt", 'r') as file:
        data = file.read()

    blockNumber = 1

    # CZEKAJ aż odbiornik wyśle 'C' (oznacza żądanie transmisji z CRC)
    wait = ser.read()
    if wait == 'C':

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
            block_to_send = [0x01, blockNumber, 255 - blockNumber, blockFromFile, crc]
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
        ser.write(0x04)


def recive_file(ser):
    print("Opening 'file_to_recive.txt'")
    with open("file_to_recive.txt",'a') as file:
        expectedBlockNumber = 1
        ser.write(0x43)
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
            blockNum=0
            if header == bytes([SOH]):
                blockNum = ser.read(1)[0]
                block_num_comp = ser.read(1)[0]
                if blockNum != 0xFF - block_num_comp:
                    print("Nieprawidłowy nagłówek bloku.")
                    ser.write(bytes([NAK]))
                    #continue
                '''
                ODCZYTAJ 128 bajtów danych
                ODCZYTAJ CRC (2 bajty)
                POLICZ CRC z danych
                JEŚLI CRC się nie zgadza:
                    WYŚLIJ NAK
                    KONTYNUUJ'''
                block=ser.read()
                readCrc=ser.read(2)[1]
                calculatedCrc=calculate_crc(block)
                if readCrc != calculatedCrc:
                    print("Nieprawidłowy nagłówek bloku.")
                    ser.write(bytes([NAK]))
                '''JEŚLI numer bloku == expected_block_number:
                    ZAPISZ dane do pliku
                    ZWIĘKSZ expected_block_number
        
                WYŚLIJ ACK'''
                if blockNum==expectedBlockNumber:
                    print("Saving recived contant into 'file_to_recive.txt'.")
                    with open("file_to_recive.txt", 'a') as file:
                        file.write(block)
                ser.write(0x06)
            '''JEŚLI bajt to EOT (0x04):
            WYŚLIJ ACK
            PRZERWIJ'''
            if header == bytes([EOT]):
                ser.write(0x06)
                break
                #return None?
        '''ZAMKNIJ plik'''
        file.close()



def divide_to_blocks(data):  # musi zmniejszac data o block
    blockList = []
    # blockNumber = blockNumber + 1
    # return blockList, data, blockNumber
    '''//podział tekstu na bloki
        for (int i = 0; i < plainBytes.length; i += 16) {    //iteracja po blokach teksu
            byte[][] block = new byte[4][4];
            for (int row = 0; row < 4; row++) {
                for (int col = 0; col < 4; col++) {
                    block[row][col] = plainBytes[i + (col * 4) + row];
                }
            }

            blocksList.add(block);      //dodanie nowo stworzonego bloku do listy bloków
        }
    '''
    blockNumber = 0
    for i in range(0,len(data)):
        block=np.byte([][128])
        for j in range(0,128):
            block[blockNumber][j]=data[j]
        i=i+128
        blockNumber=blockNumber+1
    return blockList

# main: