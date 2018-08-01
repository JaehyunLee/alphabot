import RPi.GPIO as GPIO
import time
from TRSensors import TRSensor


class AlphaBot2(object):

    def __init__(self, ain1=12, ain2=13, ena=6, bin1=20, bin2=21, enb=26):
        self.TR = TRSensor()
        self.AIN1 = ain1
        self.AIN2 = ain2
        self.BIN1 = bin1
        self.BIN2 = bin2
        self.ENA = ena
        self.ENB = enb

        self.move_speed = 30
        self.rotate_speed = 30

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

    def forward(self):
        self.__init__()
        self.PWMA.ChangeDutyCycle(self.move_speed)  # LF
        self.PWMB.ChangeDutyCycle(self.move_speed)  # RF
        GPIO.output(self.AIN2, GPIO.HIGH)
        GPIO.output(self.BIN2, GPIO.HIGH)
        time.sleep(0.05)
        while True:
            position, sensors = self.TR.readLine()
            if sensors[0] > 900 and sensors[1] > 900 and sensors[2] > 900 and sensors[3] > 900 and sensors[4] > 900:
                time.sleep(0.05)
                GPIO.output(self.AIN2, GPIO.LOW)
                GPIO.output(self.BIN2, GPIO.LOW)
                break
            else:
                proportional = position - 2000
                power_difference = proportional / 30

                if power_difference > self.move_speed:
                    power_difference = self.move_speed
                if power_difference < - self.move_speed:
                    power_difference = - self.move_speed
                if power_difference < 0:
                    self.PWMA.ChangeDutyCycle(self.move_speed + power_difference)
                    self.PWMB.ChangeDutyCycle(self.move_speed)
                else:
                    self.PWMA.ChangeDutyCycle(self.move_speed)
                    self.PWMB.ChangeDutyCycle(self.move_speed - power_difference)

    def stop(self):
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)

    def backward(self):
        self.__init__()
        self.PWMA.ChangeDutyCycle(self.move_speed)  # LB
        self.PWMB.ChangeDutyCycle(self.move_speed)  # RB
        GPIO.output(self.AIN1, GPIO.HIGH)
        GPIO.output(self.BIN1, GPIO.HIGH)

        time.sleep(0.05)
        while True:
            position, sensors = self.TR.readLine()
            if sensors[0] > 900 and sensors[1] > 900 and sensors[2] > 900 and sensors[3] > 900 and sensors[4] > 900:
                GPIO.output(self.AIN1, GPIO.LOW)
                GPIO.output(self.BIN1, GPIO.LOW)
                GPIO.output(self.AIN2, GPIO.HIGH)  # LF
                GPIO.output(self.BIN2, GPIO.HIGH)  # RF
                time.sleep(0.05)
                GPIO.output(self.AIN2, GPIO.LOW)
                GPIO.output(self.BIN2, GPIO.LOW)
                break
            else:
                proportional = position - 2000
                power_difference = proportional / 30

                if power_difference > self.move_speed:
                    power_difference = self.move_speed
                if power_difference < - self.move_speed:
                    power_difference = - self.move_speed
                if power_difference < 0:
                    self.PWMA.ChangeDutyCycle(self.move_speed + power_difference)
                    self.PWMB.ChangeDutyCycle(self.move_speed)
                else:
                    self.PWMA.ChangeDutyCycle(self.move_speed)
                    self.PWMB.ChangeDutyCycle(self.move_speed - power_difference)

    def left(self, value):
        self.__init__()
        self.PWMA.ChangeDutyCycle(self.rotate_speed)
        self.PWMB.ChangeDutyCycle(self.rotate_speed)
        GPIO.output(self.AIN2, GPIO.HIGH)  # LF
        GPIO.output(self.BIN1, GPIO.HIGH)  # RB
        time.sleep(value)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)

    def right(self, value):
        self.__init__()
        self.PWMA.ChangeDutyCycle(self.rotate_speed)
        self.PWMB.ChangeDutyCycle(self.rotate_speed)
        GPIO.output(self.AIN1, GPIO.HIGH)  # LB
        GPIO.output(self.BIN2, GPIO.HIGH)  # RF
        time.sleep(value)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)

    def calibration_left(self):
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.AIN1, GPIO.HIGH)
        GPIO.output(self.BIN2, GPIO.HIGH)

    def calibration_right(self):
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.HIGH)
        GPIO.output(self.BIN1, GPIO.HIGH)

    def calibration(self):
        print('Sensor Calibration..')
        for i in range(0, 100):
            if i < 25 or i >= 75:
                self.calibration_right()
            else:
                self.calibration_left()
            self.TR.calibrate()
        self.stop()
