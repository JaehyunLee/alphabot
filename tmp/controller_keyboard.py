from curtsies import Input
from alphabot_line import AlphaBot2
import RPi.GPIO as GPIO


if __name__ == '__main__':

    Ab = AlphaBot2()
    Ab.calibration()

    try:
        with Input(keynames='curses') as input_generator:
            for e in input_generator:
                if e is 'a':
                    print('left')
                    Ab.left(0.4)
                elif e is 'd':
                    print('right')
                    Ab.right(0.4)
                elif e is 'w':
                    print('forward')
                    Ab.forward()
                elif e is 's':
                    print('backward')
                    Ab.backward()
                elif e is 'x':
                    print('exit!')
                    GPIO.cleanup()
                    break
                else:
                    print('undefined key', e)
    except KeyboardInterrupt:
        GPIO.cleanup()
