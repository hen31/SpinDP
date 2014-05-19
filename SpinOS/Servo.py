__author__ = 'Rubens'


class Servo:
    def __init__(self, servoNumber, pwm):
        self.servoNumber = servoNumber
        self.pwm = pwm
        self.last_position = 0

    def set_servo(self, degree):
        # 100 = min, 600 = max, difference = 500, max = 180 degrees
        if degree > 180:
            degree = 180
        if degree <= 0:
            degree = 0
        if self.last_position != degree:
            self.last_position = degree
            self.pwm.setPWM(self.servoNumber, 0 , int(100 + (float(degree) * float(float(500)/float(180)))))

    def get_servo(self):
        return self.last_position
