import serial
class serialRW():

    def __init__(self):
      print("Serial connection start\n")
      self.ser = serial.Serial('/dev/ttyACM0', 9600)
      print("Serial connection Complete\n")
    #this data package should have 4 data any given time,
    #3 data inidicate 3 different sensor data, and 1 indicate which data
    #is valid
    def read_data(self):
        #clear input buffer
        self.ser.flushImput()
        s = ""
        if self.ser.inWaiting()>0:
            read_serial=self.ser.readline()
            s = read_serial.split()
            print(s+"\n")



