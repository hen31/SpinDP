__author__ = 'Rubens'

from Adafruit_PWM_Servo_Driver import PWM
from Leg import Leg
import time

pwm = PWM(0x40, debug=True)
pwm.setPWMFreq(50)

def setServo(servo, degree):
    # 100 = min, 600 = max, difference = 500, max = 180 degrees
    pwm.setPWM(servo, 0 , int(100 + (float(degree) * float(float(500)/float(180)))))

while(True):
    for x in xrange(0, 16):
        setServo(x,90)
    print(120)
    time.sleep(2)
    for x in xrange(0, 16):
        setServo(x,90)
    print(60)
    time.sleep(2)

#leg = Leg(0,pwm)
#leg.walk()
