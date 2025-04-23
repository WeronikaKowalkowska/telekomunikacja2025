import serial
import time

SOH = 0x01
EOT = 0x04
ACK = 0x06
NAK = 0x15
C = 0x43

# metoda do liczenia sumy kontrolnej CRC-16 z generatorem 0x1021 (2 bajty) - jeżeli odbiornik wyśle 'C'
def calculate_crc(data: bytes) -> bytes:
    crc = 0
    for byte in data:
        crc ^= byte << 8  # bajt z najwyższych 8 bitów
        for _ in range(8):  # iteracja po bitach
            if crc & 0x8000:  # jeżeli najwyższy bit CRC to 1
                crc = (crc << 1) ^ 0x1021  # przesunięcie i XOR z generatorem
            else:
                crc <<= 1  # przesunięcie
            crc &= 0xFFFF  # utrzymanie 16-bitowego wyniku
    return crc.to_bytes(2, byteorder='big')


# metoda obliczająca algebraiczną sumę kontrolną (1 bajt) - jeżeli odbiornik wyśle 'NAK'
def calculate_checksum(data):
    return (sum(data) % 256).to_bytes(1, byteorder='big')

# funkcja nadajnika
def send_file(ser):
    global crc
    print("Opening 'file_to_read.txt'...")
    with open("file_to_read.txt", 'rb') as file:
        data = file.read()

    blockNumber = 1

    # czeka aż odbiornik wyśle 'C' (oznacza żądanie transmisji z CRC)
    print("Waiting for signal from receiver: ")
    time.sleep(4)
    wait = ser.read()
    if wait == bytes([C]):
        print("Signal received: C")
    elif wait == bytes([NAK]):
        print("Signal received: NAK")

    if wait == bytes([C]) or wait == bytes([NAK]):

        while len(data) != 0:  # dopóki są dane do wysłania
            # czyta 128 bajtów do zmiennej blockFromFile, a resztę zostawia jako data
            blockFromFile, data = divide_to_blocks(data)
            if len(blockFromFile) < 128:
                missingLength = 128 - len(blockFromFile)
                for i in range(missingLength):
                    # jeżeli blok jest któtszy, to dopełnia bajtami 0x1A (znak EOF)
                    blockFromFile = blockFromFile + bytes([0x1A])

            # składa blok do wysłania ((SOH, numer bloku, 255 - numer bloku) + dane + crc/suma)
            block_to_send = bytearray()
            block_to_send.append(SOH)
            block_to_send.append(blockNumber)
            block_to_send.append(255 - blockNumber)
            block_data = bytearray(blockFromFile)
            block_to_send += block_data
            crc = 0
            if wait == bytes([C]):
                crc = calculate_crc(blockFromFile)
            if wait == bytes([NAK]):
                crc = calculate_checksum(block_to_send)
            block_to_send += crc

            # wysyła cały blok
            ser.write(block_to_send)
            print(f"Sent block {blockNumber}")
            # czeka na odpowiedź (jeżeli ACK to wysyła kolejny blok, jeżeli NAK to powtzarza)
            time.sleep(0.5)
            response = ser.read(1)
            if response == bytes([ACK]):
                print("The block was sent successfully.")
                blockNumber += 1
            elif response == bytes([NAK]):
                print("NAK error detected, retrying resending...")
                ser.write(block_to_send)

        # jak wszysko wyśle to wysyla znak EOT (0x04)
        ser.write(bytes([EOT]))
        # czekamy na odpowiedź
        time.sleep(0.5)
        # sprawdza, czy dostał podtwierdzenie ACK
        final_ack = ser.read(1)
        if final_ack == bytes([ACK]):
            print("Final ACK received. Transmission complete.")
        else:
            print("Final ACK not received. Transmission might have failed.")



# funkcja odbiornika
def receive_file(ser):
    global sing
    print("Opening 'file_to_recive.txt'...")
    with open("file_to_recive.txt", 'wb') as file:
        expectedBlockNumber = 1
        test = True
        while test:
            checksumType = input("Type 'C' to use crc as a checksum, 'NAK' to use algebraic checksum: ")
            if checksumType == "C":
                sign = bytes([C])
                test = False
            elif checksumType == "NAK":
                sign = bytes([NAK])
                test = False
            else:
                print("Unknown checksum type.")
        ser.write(sign)
        if sign == bytes([C]):
            print("Sent C")
        elif sign == bytes([NAK]):
            print("Sent NAK")
        #dopóki nie otrzyma komunikat EOT (0x04)
        while True:
            # odbiera pierwszy bajt
            header = ser.read(1)
            # sprawdza, czy pierwszy bajt to SOH (0x01)
            if header == bytes([SOH]):
                # odbiera kolejny bajt, który jest numerem bloku i za pomocą [0] konwertuje na int
                blockNum = ser.read(1)[0]
                # odbiera kolejny bajt, który jest dopełnieniem i za pomocą [0] konwertuje na int
                block_num_comp = ser.read(1)[0]
                if blockNum != 0xFF - block_num_comp:
                    print("Invalid block header.")
                    # jeżeli nie jest spełniony warunek to wysyła komunikat o błędzie
                    ser.write(bytes([NAK]))
                # odbiera kolejne 128 bajtów danych
                block = ser.read(128)
                if sign == bytes([C]):
                    # odbiera 2 bajty crc z bloku
                    readCrc = ser.read(2)
                    # oblicza crc na podstwanie odebranych danych
                    calculatedCrc = calculate_crc(block)
                    # sprawdza, czy to crc co dostał się zgadza z oblicznym
                    if readCrc != calculatedCrc:
                        print("Incorrect crc checksum.")
                        # jeżeli nie jest spełniony warunek to wysyła komunikat o błędzie
                        ser.write(bytes([NAK]))
                if sign == bytes([NAK]):
                    # odbiera 1 bajt crc z bloku
                    readSum = ser.read(1)
                    # oblicza sumę kontrolną na podstwanie odebranych danych
                    calculatedSum = calculate_checksum(block)
                    # sprawdza, czy to crc co dostał się zgadza z oblicznym
                    if readSum != calculatedSum:
                        print("Incorrect checksum.")
                        # jeżeli nie jest spełniony warunek to wysyła komunikat o błędzie
                        ser.write(bytes([NAK]))
                # sprawdza, czy numer bloku się zgadza
                if blockNum == expectedBlockNumber:
                    print("Saving recived contant into 'file_to_recive.txt'...")
                    with open("file_to_recive.txt", 'ab') as file:
                        # usuwa znaki końca pliku
                        block = block.rstrip(bytes([0x1A]))
                        # dopisuje otrzymany blok
                        file.write(block)
                        # zwiększa numer oczekiwanego bloku
                        expectedBlockNumber += 1
                        # wysyła podwtierdzenie otrzymania bloku
                        ser.write(bytes([ACK]))
            # kiedy otrzyma EOT to konczy pętlę while
            if header == bytes([EOT]):
                # wysyła koncowe podtwierdzenie
                ser.write(bytes([ACK]))
                print("File received successfully.")
                break
        # zamyka plik
        file.close()

# metoda do podziału danych bloku; zwraca blok 128 bajtowy i resztę danych
def divide_to_blocks(data):
    block_data = data[:128]
    remaining_data = data[128:]
    return block_data, remaining_data

# start of the main

# COM1 i COM2 dla Windows i /dev/ttys001 i /dev/ttys002 dla Mac
port = input("Serial port (np. COM1 / /dev/ttys001): ")
ser = serial.Serial(port, 9600)

mode = input("Type 'send' to send or 'recv' to receive a file: ").strip().lower()

if mode == "send":
    send_file(ser)
elif mode == "recv":
    receive_file(ser)
else:
    print("Unknown method.")

ser.close()