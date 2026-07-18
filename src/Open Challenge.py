# ============================================================
# WRO Future Engineers Open Challenge
# Raspberry Pi 5
# Pi Camera Module 3
# Black Wall Detection
# ============================================================

from turtle
import cv2
import numpy as np
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from time import sleep

# ============================================================
# GPIO PINS
# ============================================================

DIR_PIN = 17          # DIR2
PWM_PIN = 27          # PWM2
SERVO_PIN = 25        # Servo

# ============================================================
# CAMERA SETTINGS
# ============================================================

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

IMAGE_CENTER_X = FRAME_WIDTH // 2      # 320
IMAGE_CENTER_Y = FRAME_HEIGHT // 2     # 240

# ============================================================
# GPIO SETUP
# ============================================================

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)

motor_pwm = GPIO.PWM(PWM_PIN, 1000)
motor_pwm.start(0)

servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(7.5)

# ============================================================
# CAMERA
# ============================================================

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={
        "size": (FRAME_WIDTH, FRAME_HEIGHT),
        "format": "RGB888"
    }
)

picam2.configure(config)
picam2.start()

sleep(2)

# ============================================================
# BLACK LAB THRESHOLD
# Tune for your lighting
# ============================================================

black_lower = np.array([0, 0, 0])
black_upper = np.array([70, 130, 130])

kernel = np.ones((5, 5), np.uint8)

# ============================================================
# SERVO POSITIONS
# Adjust after testing
# ============================================================

CENTER = 98
LEFT = 55
RIGHT = 145 

# ============================================================
# FUNCTIONS
# ============================================================

def steer(angle):
    """
    Move servo to the specified angle (0° to 180°).
    """
    angle = max(0, min(180, angle))      # Limit angle

    duty = 2.5 + (angle / 180.0) * 10.0  # Convert angle to duty cycle

    servo_pwm.ChangeDutyCycle(duty)

    sleep(0.2)

    servo_pwm.ChangeDutyCycle(0)         # Stop sending PWM to reduce jitter


def forward(speed=60):
    # If your motor moves backwards,
    # change HIGH to LOW
    GPIO.output(DIR_PIN, GPIO.HIGH)
    motor_pwm.ChangeDutyCycle(speed)


def stop():
    motor_pwm.ChangeDutyCycle(0)

# ============================================================
# START
# ============================================================

steer(CENTER)
forward(60)

print("Robot Started")

# ============================================================
# MAIN LOOP
# ============================================================


left_x = 0
right_x = 0

while True:

    frame = picam2.capture_array()

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    mask = cv2.inRange(
        lab,
        black_lower,
        black_upper
    )

    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    black_wall_detected = False

    if contours:

        largest = max(contours, key=cv2.contourArea)

        area = cv2.contourArea(largest)

        if area > 3000:

            black_wall_detected = True

            x, y, w, h = cv2.boundingRect(largest)

            # Center of detected wall
            center_x = x + (w // 2)

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Draw detected center
            cv2.circle(
                frame,
                (center_x, y + h // 2),
                5,
                (0, 0, 255),
                -1
            )

            # Draw image center
            cv2.circle(
                frame,
                (IMAGE_CENTER_X, IMAGE_CENTER_Y),
                5,
                (255, 0, 0),
                -1
            )
            # =================================================
            # WALL FOLLOWING LOGIC
            # =================================================

            # Reset flags every frame
            left_target = False
            right_target = False

            # Determine wall position
            if x < IMAGE_CENTER_X:

                left_x = x
                left_target = True

            elif x > IMAGE_CENTER_X:

                right_x = x
                right_target = True

            # Steering using Boolean flags
            if left_target :
                servo_pwm.ChangeDutyCycle(left_x + CENTER)
                print("LEFT")
                print("left_target =", left_target)
                print("left_x =", left_x)

            elif right_target:
                servo_pwm.ChangeDutyCycle(CENTER - (640 - right_x))
                print("RIGHT")
                print("right_tsarget =", right_target)
                print("right_x =", right_x)

            else:

                servo_pwm.ChangeDutyCycle(CENTER)
                print("STRAIGHT")

    if not black_wall_detected:

        steer(CENTER)

    # Keep driving forward
    forward(60)

    # Draw center line
    cv2.line(
        frame,
        (IMAGE_CENTER_X, 0),
        (IMAGE_CENTER_X, FRAME_HEIGHT),
        (255, 0, 0),
        2
    )

    cv2.imshow("Camera", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ============================================================
# CLEANUP
# ============================================================

stop()

servo_pwm.stop()
motor_pwm.stop()

GPIO.cleanup()

picam2.stop()   

cv2.destroyAllWindows()