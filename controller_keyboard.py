from curtsies import Input
from alphabot import AlphaBot2
import RPi.GPIO as GPIO


if __name__ == '__main__':

    Ab = AlphaBot2()

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
                    Ab.forward(1.6)
                elif e is 's':
                    print('backward')
                    Ab.backward(1.6)
                elif e is 'q':
                    if (Ab.move_speed + 10) <= 90:
                        Ab.change_speed(Ab.move_speed + 10)
                        print('speed up to', Ab.move_speed)
                    else:
                        print('max speed')
                elif e is 'e':
                    if 10 <= (Ab.move_speed - 10):
                        Ab.change_speed(Ab.move_speed - 10)
                        print('speed down to', Ab.move_speed)
                    else:
                        print('min speed')
                elif e is 'x':
                    print('exit!')
                    GPIO.cleanup()
                    break
                else:
                    print('undefined key', e)
    except KeyboardInterrupt:
        GPIO.cleanup()
