import time
import random
import serial.tools.list_ports

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")                                                                                                             
            commPort = (splitPort[0])                                                                                                                  
    return commPort
    #return "COM5"                                                                                                                                     
    # return "/dev/ttyUSB1"


portName = getPort()
print(portName)

try:
    ser = serial.Serial(port=portName, baudrate=9600)
    print("Open successfully")
except:
    print("Can not open the port")

relay1_ON  = [1, 6, 0, 0, 0, 255, 200, 91]
relay1_OFF = [1, 6, 0, 0, 0, 0, 136, 27]
relay2_ON  = [2, 6, 0, 0, 0, 255, 200, 91]
relay2_OFF = [2, 6, 0, 0, 0, 0, 136, 27]
relay3_ON  = [3, 6, 0, 0, 0, 255, 200, 91]
relay3_OFF = [3, 6, 0, 0, 0, 0, 136, 27]
relay4_ON  = [4, 6, 0, 0, 0, 255, 200, 91]
relay4_OFF = [4, 6, 0, 0, 0, 0, 136, 27]
relay5_ON  = [5, 6, 0, 0, 0, 255, 200, 91]
relay5_OFF = [5, 6, 0, 0, 0, 0, 136, 27]
relay6_ON  = [6, 6, 0, 0, 0, 255, 200, 91]
relay6_OFF = [6, 6, 0, 0, 0, 0, 136, 27]
relay7_ON  = [7, 6, 0, 0, 0, 255, 200, 91]
relay7_OFF = [7, 6, 0, 0, 0, 0, 136, 27]
relay8_ON  = [8, 6, 0, 0, 0, 255, 200, 91]
relay8_OFF = [8, 6, 0, 0, 0, 0, 136, 27]
                                                                                                                                                       
                                                                                                                                                       
def setDeviceON(id):

    match id:
        case 1:
            ser.write(relay1_ON)
        case 2:
            ser.write(relay2_ON)
        case 3:
            ser.write(relay3_ON)
        case 4:
            ser.write(relay4_ON)
        case 5:
            ser.write(relay5_ON)
        case 6:
            ser.write(relay6_ON)
        case 7:
            ser.write(relay7_ON)
        case 8:
            ser.write(relay8_ON)

    time.sleep(1)
    print(serial_read_data(ser))



def setDeviceOFF(id):

    match id:
        case 1:
            ser.write(relay1_OFF)
        case 2:
            ser.write(relay2_OFF)
        case 3:
            ser.write(relay3_OFF)
        case 4:
            ser.write(relay4_OFF)
        case 5:
            ser.write(relay5_OFF)
        case 6:
            ser.write(relay6_OFF)
        case 7:
            ser.write(relay7_OFF)
        case 8:
            ser.write(relay8_OFF)

    time.sleep(1)
    print(serial_read_data(ser))

def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            value = value
            return value
        else:
            return -1
    return 0

soil_temperature = [1, 3, 0, 6, 0, 1,98,12]


def readTemperature():
    serial_read_data(ser)
    ser.write(soil_temperature)
    time.sleep(1)
    return serial_read_data(ser)


soil_moisture = [1, 3, 0, 7, 0, 1,50,200]


def readMoisture():
    serial_read_data(ser)
    ser.write(soil_moisture)
    time.sleep(1)
    return serial_read_data(ser)

# def writeData(id, state):
#     if state == "1":
#         setDeviceON(id)
#     else:
#     setDeviceOFF(id)                                                                                                                             



def readSerial(client):
    time.sleep(2)
    temperature = readTemperature() / 100
    temperature = random.randint(10,37)
    client.publish("cambien1", temperature)
    print("\nTemperature: ", temperature,"*C")
    time.sleep(1)
    humidity = readMoisture() / 100
    humidity = random.randint(10,100)
    client.publish("cambien2", humidity)
    print("Humidity: ", humidity, "%")
    time.sleep(1)

    light = random.randint(300,1000)
    client.publish("cambien3", light)
    print("Light: ", light,"lx")