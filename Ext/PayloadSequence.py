import Jetson.GPIO as GPIO
import time

PIN_A = 33
#DOOR = 32
HERTZ_TO_MICROSECONDS = 1000000.0
PIN_SERVO_IN_PWM = 2200.0 / HERTZ_TO_MICROSECONDS
PIN_SERVO_OUT_PWM = 800.0 / HERTZ_TO_MICROSECONDS
DOOR_SERVO_PWM_OPEN = 1650.0 / HERTZ_TO_MICROSECONDS
DOOR_SERVO_PWM_CLOSED = 850.0 / HERTZ_TO_MICROSECONDS

GPIO.setmode(GPIO.BOARD)

GPIO.setup(PIN_A, GPIO.OUT, initial=GPIO.HIGH)
#GPIO.setup(DOOR, GPIO.OUT)
pin_a = GPIO.PWM(PIN_A, 200)

pin_a.start(0)

print("starting")

try:
    while True:
        pin_a.stop()
        time.sleep(0.1)
        pin_a.start(100)
        time.sleep(0.1)
        pin_a.stop()
        time.sleep(0.1)
        pin_a.start(0)
        time.sleep(0.1)
finally:
    pin_a.stop()
    GPIO.cleanup()
