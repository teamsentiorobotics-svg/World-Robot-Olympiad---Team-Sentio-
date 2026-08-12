import cv2
import numpy as np
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from time import sleep
import time
from heading import MPU6050Heading

imu = MPU6050Heading()
last_heading_time = 0

ps = 0#50
rs = 0#55

inside_park = False
CLOCKWISE = None
LINE_COOLDOWN = 1.2
blue_detected = False
orange_detected = False
line_count = 0
total_lines = 12
last_orange_time = 0.0
last_blue_time = 0.0

KP = 0.02
PWM_PIN = 13
IN1_PIN = 5
IN2_PIN = 6         # PWM2
SERVO_PIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(IN1_PIN, GPIO.OUT)
GPIO.setup(IN2_PIN, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)

motor_pwm = GPIO.PWM(PWM_PIN, 1000)
motor_pwm.start(0)

servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(0)

CENTER = 98 # 98
LEFT = 70 # 70
RIGHT = 125 # 130

last_angle = -1

current_angle = CENTER
last_servo_time = 0

def steer(angle):

    angle = max(LEFT, min(RIGHT, angle))      # Limit angle

    duty = 2.5 + (angle / 180.0) * 10.0  # Convert angle to duty cycle

    servo_pwm.ChangeDutyCycle(duty)

    sleep(0.05)

    servo_pwm.ChangeDutyCycle(0)    
def forward(speed):
    GPIO.output(IN1_PIN, GPIO.HIGH)
    GPIO.output(IN2_PIN, GPIO.LOW)
    motor_pwm.ChangeDutyCycle(speed)
def backward(speed):
    GPIO.output(IN1_PIN, GPIO.LOW)
    GPIO.output(IN2_PIN, GPIO.HIGH)
    motor_pwm.ChangeDutyCycle(speed)

def stop():
    motor_pwm.ChangeDutyCycle(0)
    GPIO.output(IN1_PIN, GPIO.LOW)
    GPIO.output(IN2_PIN, GPIO.LOW)
# ============================================================
# START
# ============================================================

# ==========================================================
# CAMERA SETTINGS
# ==========================================================
WIDTH = 1280
HEIGHT = 680
X_MID = WIDTH // 2

BLACK_LOWER = np.array([0,118,118])
BLACK_UPPER = np.array([75,138,138])

BLUE_LOWER = np.array([70, 150, 145])
BLUE_UPPER = np.array([170, 185, 175])

RED_LOWER = np.array([60, 150, 145]) #[70, 150, 145]
RED_UPPER = np.array([125, 185, 170]) #[170, 185, 175]

ORANGE_LOWER = np.array([140, 120, 145])
ORANGE_UPPER = np.array([210, 155, 210])

PURPLE_LOWER = np.array([80, 120, 100])
PURPLE_UPPER = np.array([190, 180, 170])

GREEN_LOWER = np.array([80, 80, 140])
GREEN_UPPER = np.array([150, 110, 175])

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"size": (WIDTH, HEIGHT), "format": "RGB888"}
)

picam2.configure(config)

picam2.start()

print("Auto adjusting camera...")
picam2.set_controls({
    "AeEnable": True,
    "AwbEnable": True
})

time.sleep(2)

meta = picam2.capture_metadata()

exp = meta["ExposureTime"]
gain = meta["AnalogueGain"]

picam2.set_controls({
    "AeEnable": False,
    "AwbEnable": False,
    "ExposureTime": exp,
    "AnalogueGain": gain
})

print("Camera locked")
print("Exposure:", exp)
print("Gain:", gain)

clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
kernel = np.ones((5,5), np.uint8)

fps_time = time.time()
# 60s = 0.02kp
print("Robot Started")
#video = cv2.VideoWriter(f"output{timestamp}.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 20, (WIDTH, HEIGHT))
while True:
# Turn PWM off after 30 ms
    if time.time() - last_servo_time > 0.03:
        servo_pwm.ChangeDutyCycle(0)

    frame = picam2.capture_array()
    frame = cv2.GaussianBlur(frame, (5,5), 0)

    lab = cv2.cvtColor(frame, cv2.COLOR_RGB2LAB)

    l,a,b = cv2.split(lab)
    l = clahe.apply(l)
    lab = cv2.merge((l,a,b))

    black_mask = cv2.inRange(lab, BLACK_LOWER, BLACK_UPPER)
    black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, kernel)
    black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_CLOSE, kernel)
    black_mask = cv2.dilate(black_mask, kernel, iterations=1) 
    black_contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    output = frame.copy()
    
    left_target = None
    right_target = None

    left_bottom = -1
    right_bottom = -1

    for cnt in black_contours:
        area = cv2.contourArea(cnt)
        if area < 3000:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(output, (x, y), (x+w, y+h), (255,255,0), 2)
        cx = x + w//2
        bottom = y + h
            
        if cx < X_MID:
            if CLOCKWISE is None:
                print("CLOCKWISE")
                CLOCKWISE = True
            if bottom > left_bottom:
                left_bottom = bottom
                left_target = (x+w, bottom)
                cv2.circle(output, left_target, 8, (255,0,0), -1)
        else:
            if CLOCKWISE is None:
                CLOCKWISE = False
                print("AntiCLOCKWISE")
            if bottom > right_bottom:
                right_bottom = bottom
                right_target = (x, bottom)
                cv2.circle(output, right_target, 8, (0,0,255), -1)
    green_detected = False
    green_target = None
    green_mask = cv2.inRange(lab, GREEN_LOWER, GREEN_UPPER)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
    green_mask = cv2.dilate(green_mask, kernel, iterations=1)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if green_contours:
        largest = max(green_contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        print("Green Area", area)
        if area > 800:        
            x, y, w, h = cv2.boundingRect(largest)
            green_detected = True
            green_target = (x, y+h)
            cv2.rectangle(output, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.circle(output, (x, y+h), 8, (0, 0, 255), -1)
            
    red_detected = False
    red_target = None
    red_mask = cv2.inRange(lab, RED_LOWER, RED_UPPER)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
    red_mask = cv2.dilate(red_mask, kernel, iterations=1)
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if red_contours:
        largest = max(red_contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        if area > 800:        
            x, y, w, h = cv2.boundingRect(largest)            
            red_detected = True
            red_target = (x+w, y+h)
            cv2.rectangle(output, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.circle(output, (x+w, y+h), 8, (0,255,0), -1)
            
    purple_mask = cv2.inRange(lab,PURPLE_LOWER,PURPLE_UPPER)
    purple_mask = cv2.morphologyEx(purple_mask,cv2.MORPH_OPEN,kernel)
    purple_mask = cv2.morphologyEx(purple_mask,cv2.MORPH_CLOSE,kernel)
    purple_mask = cv2.dilate(purple_mask,kernel,iterations=1)

    purple_contours, _ = cv2.findContours(purple_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    purple_detected = False
    purple_target = None

    if purple_contours:
        largest = max(purple_contours,key=cv2.contourArea)
        area = cv2.contourArea(largest)
        # Minimum area
        if area > 100:
            x, y, w, h = cv2.boundingRect(largest)
            purple_detected = True
            purple_target = (x + w // 2,y)
            cv2.rectangle(output,(x, y),(x + w, y + h),(255, 0, 255),2)
            cv2.circle(output,purple_target,6,(255, 0, 255),-1)
            cv2.putText(output,"PURPLE",(x, max(y - 8, 20)),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255, 0, 255),2)
            cv2.putText(output,f"Area: {int(area)}",(10, 25),cv2.FONT_HERSHEY_SIMPLEX,0.55,(255, 0, 255),2)
            cv2.putText(output,f"X: {purple_target[0]}  Y: {purple_target[1]}",(10, 50),cv2.FONT_HERSHEY_SIMPLEX,0.55,(255, 0, 255),2)
            print(f"Purple detected | "f"Area: {int(area)} | "f"Target: {purple_target}")
            cv2.putText(output,"PURPLE DETECTED",(10, HEIGHT - 15),cv2.FONT_HERSHEY_SIMPLEX,0.65,(255, 0, 255),2)
        else:
            cv2.putText(output,"NO PURPLE",(10, HEIGHT - 15),cv2.FONT_HERSHEY_SIMPLEX,0.65,(255, 255, 255),2)
        
    blue_detected = False                    
    blue_mask = cv2.inRange(lab, BLUE_LOWER, BLUE_UPPER)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)
    blue_mask = cv2.dilate(blue_mask, kernel, iterations=1)
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if blue_contours:
        largest = max(blue_contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        if area > 800:        
            x, y, w, h = cv2.boundingRect(largest)
            if (x+w) > 300:
                blue_detected = True
            cv2.rectangle(output, (x, y), (x+w, y+h), (255,0,0), 2)
        
    orange_detected = False
    orange_mask = cv2.inRange(lab, ORANGE_LOWER, ORANGE_UPPER)
    orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_OPEN, kernel)
    orange_mask = cv2.morphologyEx(
        orange_mask,
        cv2.MORPH_CLOSE,
        np.ones((21,21), np.uint8)
    )
    orange_mask = cv2.dilate(
        orange_mask,
        np.ones((15,15), np.uint8),
        iterations=2
    )
    orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    all_points = []

    for cnt in orange_contours:
        if cv2.contourArea(cnt) > 50:
            all_points.append(cnt)

    if all_points:
        merged = np.vstack(all_points)
        x, y, w, h = cv2.boundingRect(merged)
        cv2.rectangle(output, (x, y), (x+w, y+h), (0,165,255), 2)
    
    current_time = time.time()

    if CLOCKWISE:
        if blue_detected and current_time - last_blue_time > LINE_COOLDOWN:
            line_count += 1
            last_blue_time = current_time
            #print("Line :", line_count)
    else:
        if orange_detected and current_time - last_orange_time > LINE_COOLDOWN:
            line_count += 1
            last_orange_time = current_time
            #print("Line :", line_count)
    if line_count >= total_lines:
        steer(CENTER)
        stop()
        break
    print("Line", line_count)
    if inside_park:
        if CLOCKWISE:
            steer(RIGHT)
            sleep(1)
            forward(ps)
            heading = imu.get_heading()
            while heading > 300 or heading < 1: 
                current_time = time.time()
                if current_time-last_heading_time > 0.01:
                    heading = imu.get_heading()
                    last_heading_time = current_time
                    print(f"Heading: {heading:.5f}°")
            stop()
            steer(CENTER)
            sleep(0.1)
            forward(ps)
            sleep(1)
            steer(RIGHT)
            backward(ps)
            heading = imu.get_heading()
            while heading < 350 : 
                current_time = time.time()
                if current_time-last_heading_time > 0.01:
                    heading = imu.get_heading()
                    last_heading_time = current_time
                    print(f"Heading: {heading:.5f}°")
            stop()
            angle = CENTER
            forward(rs)
        inside_park = False
    
    elif green_target:
        green_x, green_y = green_target
        if CLOCKWISE:
            angle = CENTER + ((green_x - (WIDTH - 10)) * KP)
        else:
            if green_y > 500:
                angle = CENTER + ((green_x - (WIDTH - 10)) * KP)
            else:
                angle = CENTER + ((green_x - (WIDTH - 200)) * KP)
            
    elif red_target:
        red_x, red_y = red_target
        if CLOCKWISE:
            if red_y > 500:
                angle = CENTER + ((red_x - 10) * KP)
            else:
                angle = CENTER + ((red_x - 200) * KP)   
        
        else:
            angle = CENTER + ((red_x - 10) * KP)
            
    elif left_target and right_target:
        left_x, left_y = left_target
        right_x, right_y = right_target
        left_distance = left_x
        right_distance = WIDTH - right_x
        error = left_distance - right_distance
        angle = CENTER + error * KP

    elif left_target:
        only_x, _ = left_target
        if CLOCKWISE:
            angle = CENTER + ((only_x) * KP)
        else:
            angle = CENTER + ((only_x - 10) * KP)

    elif right_target:
        only_x, _ = right_target
        if CLOCKWISE:
            angle = CENTER + ((only_x - (WIDTH - 10)) * KP)
        else:
            angle = CENTER + ((only_x - (WIDTH)) * KP)
    else:
        if CLOCKWISE:
            angle = CENTER + 15
        else:
            angle = CENTER - 15
#     steer(angle)
        
    cv2.imshow("Original", output)
    #cv2.imshow("Mask", mask)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        steer(CENTER)
        stop()
        #video.release()
        break

cv2.destroyAllWindows()
picam2.stop()