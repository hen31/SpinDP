import serial
import time
import threading
from Sensor import Sensor
from SensorLogger import SensorLogger


class Serial(Sensor):
    # Interval in seconds
    interval = 0.1

    sensor1 = 0
    sensor2 = 0
    voltage = 0
    voltageCounter = 0

    def __init__(self, logger, device):
        super(Serial, self).__init__(logger)
        #Logger for voltage sensor
        self.voltagelogger = SensorLogger('Voltage',logger)
        #Set serial with baudrate 9600 and a timeout of 3 seconds
        self.ser = serial.Serial(device, baudrate=9600, timeout=3.0)
        #Flushes the input. If we don't flush the input we will recieve old input.
        self.ser.flushInput()
        #Semaphores
        self.mutex1 = threading.Semaphore(1)
        self.mutex2 = threading.Semaphore(1)
        self.mutexVoltage = threading.Semaphore(1)

    def run(self):
        while self.alive:
            #Gets the sensor values
            self.getValues()
            #Sleep
            time.sleep(self.interval)

    def getValues(self):
        #Readline from serial
        response = self.ser.readline()
        #Decode response
        response = response.decode('ascii')
        #Checks if we need the response
        if len(response) > 2:
            #Remove characters that we don't need
            response = response.replace("\r\n","")
            response = response.replace("\x00","")
            response = response.replace("n'","")
            response = response.replace("'","")
            #Convert to int
            response = int(response)
            #First glove sensor
            if(response >= 2000 and response < 2500):
                sensor1 = response - 2000
                self.setSensor1(sensor1)
            #Second glove sensor
            elif(response >= 2500 and response < 3000):
                sensor2 = response - 2500
                self.setSensor2(sensor2)
            #Voltage
            else:
                voltage = float(response) / float(100)
                self.setVoltage(voltage)

    def stop(self):
        self.alive = False

    def start(self):
        self.thread.start()

    def getSensor1(self):
        self.mutex1.acquire()
        value = self.sensor1
        self.mutex1.release()
        return value

    def setSensor1(self, value):
        self.mutex1.acquire()
        self.sensor1 = value
        self.mutex1.release()

    def getSensor2(self):
        self.mutex2.acquire()
        value = self.sensor2
        self.mutex2.release()
        return value

    def setSensor2(self, value):
        self.mutex2.acquire()
        self.sensor2 = value
        self.mutex2.release()

    def getVoltage(self):
        self.mutexVoltage.acquire()
        value = self.voltage
        self.mutexVoltage.release()
        return value

    def setVoltage(self, value):
        self.mutexVoltage.acquire()
        self.voltage = value
        #Log every second
        if self.voltageCounter == 0 or self.voltageCounter == 10:
            self.voltageCounter = 0
            self.voltagelogger.log_waarde("{0:.2f}".format(self.voltage))
        self.mutexVoltage.release()