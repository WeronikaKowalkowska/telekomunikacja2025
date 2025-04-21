import serial

print("Moduł serial pochodzi z:", serial.__file__)
ser = serial.Serial('COM3', 9600)
print("Połączenie otwarte:", ser.name)
ser.close()
