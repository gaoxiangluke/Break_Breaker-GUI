from ArduinoUnoClass import Arduino
AR1 = Arduino()
while True:
    Array = AR1.readData(0,False,True,True,False)
    print(Array[0]+1);
