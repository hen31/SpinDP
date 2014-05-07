import threading
import time
import smbus
import math
from Sensor import Sensor
from SensorLogger import SensorLogger
from Logger import Logger

__author__ = 'Ruben'

class MPU6050(Sensor):
    # Power management registers
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c

    # MPU6050 scales
    gyro_scale = 131.0
    acceleration_scale = 16384.0

    # This is the address value read via the i2cdetect command
    address = 0x68

    # Interval in seconds
    interval = 1

    # Values
    last_value = [0, 0, 0]
    current_value = [0, 0, 0]

    def __init__(self, logger):
        super(MPU6050, self).__init__(logger)
        self.thread = threading.Thread(target=self.run)
        self.bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for Revision 1 boards
        try:
            self.bus.write_byte_data(self.address, self.power_mgmt_1, 0) # Wake up
        except IOError:
            self.sensorlogger("Unable to access parallel port on bus %d, addresss 0x%02x" % (self.bus, self.address))

    def run(self):
        while self.alive:
            (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, acceleration_scaled_x, acceleration_scaled_y, acceleration_scaled_z) = self.read_all()

            last_x = self.get_x_rotation(acceleration_scaled_x, acceleration_scaled_y, acceleration_scaled_z)
            last_y = self.get_y_rotation(acceleration_scaled_x, acceleration_scaled_y, acceleration_scaled_z)

            gyro_offset_x = gyro_scaled_x
            gyro_offset_y = gyro_scaled_y

            gyro_total_x = last_x - gyro_offset_x
            gyro_total_y = last_y - gyro_offset_y

            self.last_value = self.current_value
            self.current_value = [gyro_scaled_x, gyro_scaled_y, gyro_scaled_z]
            
            #print "{0:.2f} {1:.2f} {2:.2f} {3:.2f}".format(gyro_total_x, last_x, gyro_total_y, last_y)
            self.sensorlogger.log_waarde("x:{0:.2f} y:{1:.2f} z:{2:.2f}".format(gyro_scaled_x,gyro_scaled_y,gyro_scaled_z))

            time.sleep(self.interval)

    def stop(self):
        self.alive = False
        self.sensorlogger.log_waarde('Sensor MPU6050 stopped')

    def start(self):
        self.thread.start()
        self.sensorlogger.log_waarde('Sensor MPU6050 started')

    def read_all(self):
        try:
            raw_gyro_data = self.bus.read_i2c_block_data(self.address, 0x43, 6)
            raw_acceleration_data = self.bus.read_i2c_block_data(self.address, 0x3b, 6)
        except IOError:
            self.sensorlogger("Unable to access parallel port on bus %d, addresss 0x%02x" % (self.bus, self.address))
            return (0, 0, 0, 0, 0, 0)

        gyro_scaled_x = self.twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / self.gyro_scale
        gyro_scaled_y = self.twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / self.gyro_scale
        gyro_scaled_z = self.twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / self.gyro_scale

        acceleration_scaled_x = self.twos_compliment((raw_acceleration_data[0] << 8) + raw_acceleration_data[1]) / self.acceleration_scale
        acceleration_scaled_y = self.twos_compliment((raw_acceleration_data[2] << 8) + raw_acceleration_data[3]) / self.acceleration_scale
        acceleration_scaled_z = self.twos_compliment((raw_acceleration_data[4] << 8) + raw_acceleration_data[5]) / self.acceleration_scale

        return (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, acceleration_scaled_x, acceleration_scaled_y, acceleration_scaled_z)

    def getValue(self):
        return self.current_value

    @staticmethod
    def twos_compliment(val):
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    @staticmethod
    def dist(a, b):
        return math.sqrt((a * a) + (b * b))

    def get_y_rotation(self,x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(self,x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)
