import RPi.GPIO as GPIO

from time import sleep
import time

SERVO_PIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(SERVO_PIN, GPIO.OUT)

servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(0)

CENTER = 70  # 98
LEFT = 35 # 70
RIGHT = 105 # 130

def steer(angle):

    angle = max(LEFT, min(RIGHT, angle))      # Limit angle

    duty = 2.5 + (angle / 180.0) * 10.0  # Convert angle to duty cycle

    servo_pwm.ChangeDutyCycle(duty)

    sleep(0.05)

    servo_pwm.ChangeDutyCycle(0)
while True:
    steer(CENTER)
    sleep(2)
    steer(LEFT)
    sleep(2)
    steer(RIGHT)
    sleep(2)                                                 
