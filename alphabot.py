import RPi.GPIO as GPIO
import time


class AlphaBot2(object):
    def __init__(self, ain1=12, ain2=13, ena=6, bin1=20, bin2=21, enb=26):
        self.AIN1 = ain1
        self.AIN2 = ain2
        self.BIN1 = bin1
        self.BIN2 = bin2
        self.ENA = ena
        self.ENB = enb

        self.move_speed = 20
        self.rotate_speed = 20

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.AIN1, GPIO.OUT)
        GPIO.setup(self.AIN2, GPIO.OUT)
        GPIO.setup(self.BIN1, GPIO.OUT)
        GPIO.setup(self.BIN2, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA, 500)
        self.PWMB = GPIO.PWM(self.ENB, 500)
        self.PWMA.start(self.move_speed)
        self.PWMB.start(self.move_speed)
        self.stop()

    def forward(self, value):
        self.__init__()
        self.PWMA.ChangeDutyCycle(self.move_speed - 1)  # LF
        self.PWMB.ChangeDutyCycle(self.move_speed)  # RF
        GPIO.output(self.AIN2, GPIO.HIGH)
        GPIO.output(self.BIN2, GPIO.HIGH)
        time.sleep(value)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)

    def stop(self):
        self.__init__()
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)

    def backward(self, value):
        self.__init__()
        self.PWMA.ChangeDutyCycle(self.move_speed + 1)  # LB
        self.PWMB.ChangeDutyCycle(self.move_speed)  # RB
        GPIO.output(self.AIN1, GPIO.HIGH)
        GPIO.output(self.BIN1, GPIO.HIGH)
        time.sleep(value)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)

    def left(self, value):
        self.__init__()
        self.PWMA.ChangeDutyCycle(self.rotate_speed - 3)  # LF
        self.PWMB.ChangeDutyCycle(self.rotate_speed - 3)  # RB
        GPIO.output(self.AIN2, GPIO.HIGH)
        GPIO.output(self.BIN1, GPIO.HIGH)
        time.sleep(value)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)

    def right(self, value):
        self.__init__()
        self.PWMA.ChangeDutyCycle(self.rotate_speed)  # LB
        self.PWMB.ChangeDutyCycle(self.rotate_speed)  # RF
        GPIO.output(self.AIN1, GPIO.HIGH)
        GPIO.output(self.BIN2, GPIO.HIGH)
        time.sleep(value)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)

    def change_speed(self, value):
        self.move_speed = value
        self.rotate_speed = value
