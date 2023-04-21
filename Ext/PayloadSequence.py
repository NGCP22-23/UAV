import Jetson.GPIO as GPIO
import time

PIN_A = 38
#DOOR = 32
HERTZ_TO_MICROSECONDS = 1000000.0
PIN_SERVO_IN_PWM = 2200.0 / HERTZ_TO_MICROSECONDS
PIN_SERVO_OUT_PWM = 800.0 / HERTZ_TO_MICROSECONDS
DOOR_SERVO_PWM_OPEN = 1650.0 / HERTZ_TO_MICROSECONDS
DOOR_SERVO_PWM_CLOSED = 850.0 / HERTZ_TO_MICROSECONDS

GPIO.setmode(GPIO.BOARD)

GPIO.setup(PIN_A, GPIO.OUT)
#GPIO.setup(DOOR, GPIO.OUT)

print("starting")
while True:
    GPIO.PWM(PIN_A, PIN_SERVO_IN_PWM)
    time.sleep(1)
    GPIO.PWM(PIN_A, PIN_SERVO_OUT_PWM)
    time.sleep(1)
