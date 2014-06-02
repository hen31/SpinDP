import threading
import time
import math
from SensorLogger import SensorLogger

from Sensor import Sensor
from PyComms.mpu6050base import MPU6050BASE

__author__ = 'Ruben'

class MPU6050(Sensor):
    # Interval in seconds
    interval = 1

    # Default value
    current_value = {'yaw': 0, 'pitch': 0, 'roll': 0}

    def __init__(self, logger):
        #initialize
        super(MPU6050, self).__init__(logger)
        self.sensorlogger = SensorLogger('MPU6050',logger)
        self.mutex = threading.Semaphore(1)
        self.mpu = MPU6050BASE()
        self.mpu.dmpInitialize()
        self.mpu.setDMPEnabled(True)

        # get expected DMP packet size for later comparison
        self.packetSize = self.mpu.dmpGetFIFOPacketSize()

    #get Values
    def run(self):
        while self.alive:
            self.getValues()
            time.sleep(self.interval)

    def getValues(self):
        # Get INT_STATUS byte
        mpuIntStatus = self.mpu.getIntStatus()
        if mpuIntStatus >= 2: # check for DMP data ready interrupt (this should happen frequently)
            # get current FIFO count
            fifoCount = self.mpu.getFIFOCount()

            # check for overflow (this should never happen unless our code is too inefficient)
            if fifoCount == 1024:
                # reset so we can continue cleanly
                self.mpu.resetFIFO()
                # print('FIFO overflow!')


            # wait for correct available data length, should be a VERY short wait
            fifoCount = self.mpu.getFIFOCount()
            while fifoCount < self.packetSize:
                fifoCount = self.mpu.getFIFOCount()

            result = self.mpu.getFIFOBytes(self.packetSize)
            q = self.mpu.dmpGetQuaternion(result)
            g = self.mpu.dmpGetGravity(q)
            ypr = self.mpu.dmpGetYawPitchRoll(q, g)

            #save sensordata
            sensorData = {'yaw': ypr['yaw'] * 180 / math.pi, 'pitch': ypr['pitch'] * 180 / math.pi, 'roll': ypr['roll'] * 180 / math.pi}
            self.setValue(sensorData)
            fifoCount -= self.packetSize

            #log sensor
            self.sensorlogger.log_waarde("y:{0:.3f}, p:{1:.3f}, r:{2:.3f}".format(sensorData['yaw'], sensorData['pitch'], sensorData['roll']))
    #stop thread
    def stop(self):
        self.alive = False

    #start thread
    def start(self):
        self.thread.start()

    #get yaw, pith, roll
    def getValue(self):
        self.mutex.acquire()
        value = self.current_value
        self.mutex.release()
        return value

    #set sensorData
    def setValue(self, value):
        self.mutex.acquire()
        self.current_value = value
        self.mutex.release()