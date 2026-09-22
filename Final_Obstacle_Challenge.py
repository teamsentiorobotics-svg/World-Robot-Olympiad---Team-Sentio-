# N_Obstacle_Anti_22.py
import cv2
import time
from time import sleep
from heading import MPU6050Heading 
import driveEnc as drive
import N_Vision_22 as vision
import N_Parking_22 as parking
import RPi.GPIO as GPIO

BUTTON_PIN = 18
LED_PIN = 12

GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN,GPIO.LOW)

button_state = True
last_button = 0

print("Waiting For Start Button...")
print("Press the button on GPIO 18 to start...")

# Wait until button is pressed
while not button_state:
    button = GPIO.input(BUTTON_PIN)
    if button == 1 and last_button == 0:
        button_state = not button_state
        print("Button_state",button_state)
        if button_state:
            GPIO.output(LED_PIN,GPIO.HIGH)
        else:
            GPIO.output(LED_PIN,GPIO.LOW)
    last_button = button
    time.sleep(0.01)

# Small debounce delay
sleep(0.2)

imu = MPU6050Heading()
last_heading_time = 0
imu.reset_heading()
heading = 0
# ============================================================
# ROBOT CONTROL SETTINGS
# ============================================================
COOLDOWN = 3
total_lap = 3
lap_count = 0
inside_park = True
round_complete = False
last_purple_time = 0
last_orange_time = 0
purple_gone_time = None
line_count = 0
total_line = 13

rs = 35
KP = 0.028 #0.028
RIGHT = drive.RIGHT
LEFT = drive.LEFT
CENTER = drive.CENTER

OBSTACLE_ACTION_AREA = 8000 #8000
 
CENTER = drive.CENTER
WIDTH = vision.WIDTH
HEIGHT = vision.HEIGHT
X_MID = vision.WIDTH/2

# ============================================================
# CAMERA
# ============================================================

camera = vision.start_camera()

# ============================================================
# ROBOT START
# ============================================================

print("Robot Started - TEST LAP")
print("RED/GREEN = obstacle avoidance")
print("BLACK = wall following")
print("BLUE/ORANGE/MAGENTA = display only")
print("Q = stop")

CLOCKWISE = None
angle = CENTER

drive.steer(CENTER)
sleep(0.8)

# ============================================================
# FPS
# ============================================================

fps_frames = 0
fps_start = time.perf_counter()
loop_fps = 0.0

# ============================================================
# MAIN LOOP
# ============================================================
def green_turn(CLOCKWISE):
    global last_heading_time
    if CLOCKWISE:
        drive.driveencoder(200,rs)
        sleep(1)
        drive.steer(RIGHT)
        sleep(1)
        heading = imu.get_heading()
        sleep(0.5)
        drive.forward(rs)
        while heading < 90 or heading > 310:
            current_time = time.time()
            if current_time-last_heading_time > 0.01:
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: {heading:.5f}°")
        drive.stop()
        sleep(1)
        
        drive.steer(LEFT)
        sleep(1)
        heading = imu.get_heading()
        sleep(0.5)
        drive.backward(rs)
        while heading > 190:
            current_time = time.time()
            if current_time-last_heading_time > 0.01:
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: {heading:.5f}°")
        drive.stop()
    else:
        drive.steer(CENTER)
        sleep(1)
        drive.driveencoder(200,rs)
        sleep(1)
        drive.steer(RIGHT)
        sleep(1)
        heading = imu.get_heading()
        sleep(0.5)
        drive.forward(rs)
        while heading < 90 or heading > 180:
            current_time = time.time()
            if current_time-last_heading_time > 0.01:
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: {heading:.5f}°")
        drive.stop()
        sleep(1)
        drive.steer(CENTER)
        sleep(1)
        drive.driveencoder_backward(500,rs)
def red_turn(CLOCKWISE):
    global last_heading_time
    if CLOCKWISE:
        drive.steer(CENTER)
        sleep(1)
        drive.driveencoder(200,rs)
        sleep(1)
        drive.steer(LEFT)
        sleep(1)
        heading = imu.get_heading()
        sleep(0.5)
        drive.backward(rs)
        while heading < 90 or heading > 180:
            current_time = time.time()
            if current_time-last_heading_time > 0.01:
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: {heading:.5f}°")
        drive.stop()
        sleep(1)
        drive.steer(CENTER)
        sleep(1)
        drive.driveencoder_backward(500,rs)
    else:
        drive.driveencoder(200,rs)
        sleep(1)
        drive.steer(LEFT)
        sleep(1)
        heading = imu.get_heading()
        sleep(0.5)
        drive.forward(rs)
        while heading > 270 or heading < 50:
            current_time = time.time()
            if current_time-last_heading_time > 0.01:
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: {heading:.5f}°")
        drive.stop()
        sleep(1)
        
        drive.steer(RIGHT)
        sleep(1)
        heading = imu.get_heading()
        sleep(0.5)
        drive.backward(rs)
        while heading < 170:
            current_time = time.time()
            if current_time-last_heading_time > 0.01:
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: {heading:.5f}°")
        drive.stop()
def leftwall_turn(CLOCKWISE):
    global last_heading_time
    if CLOCKWISE:
        drive.driveencoder(200,rs)
        sleep(1)
        drive.steer(RIGHT)
        sleep(1)
        heading = imu.get_heading()
        sleep(0.5)
        drive.forward(rs)
        while heading < 90 or heading > 300:
            current_time = time.time()
            if current_time-last_heading_time > 0.01:
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: {heading:.5f}°")
        drive.stop()
        sleep(1)
        
        drive.steer(LEFT)
        sleep(1)
        heading = imu.get_heading()
        sleep(0.5)
        drive.backward(rs)
        while heading > 170:
            current_time = time.time()
            if current_time-last_heading_time > 0.01:
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: {heading:.5f}°")
        drive.stop()
    else:
        drive.driveencoder(400,rs)
        sleep(1)
        drive.steer(RIGHT)
        sleep(1)
        heading = imu.get_heading()
        sleep(0.5)
        drive.forward(rs)
        while heading > 190 or heading < 90:
            current_time = time.time()
            if current_time-last_heading_time > 0.01:
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: {heading:.5f}°")
        drive.stop()
        sleep(1)
        drive.steer(CENTER)
        sleep(1)
        drive.driveencoder_backward(200,rs)
        sleep(0)
def rightwall_turn(CLOCKWISE):
    global last_heading_time
    if CLOCKWISE:
        drive.driveencoder(400,rs)
        sleep(1)
        drive.steer(LEFT)
        sleep(1)
        heading = imu.get_heading()
        sleep(0.5)
        drive.forward(rs)
        while heading > 300 or heading < 170:
            current_time = time.time()
            if current_time-last_heading_time > 0.01:
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: {heading:.5f}°")
        drive.stop()
        sleep(1)
        drive.steer(CENTER)
        sleep(1)
        drive.driveencoder_backward(200,rs)
        sleep(0)
    else:
#         drive.driveencoder(rs)
        sleep(1)
        drive.steer(LEFT)
        sleep(1)
        heading = imu.get_heading()
        sleep(0.5)
        drive.forward(rs)
        while heading < 60 or heading > 300:
            current_time = time.time()
            if current_time-last_heading_time > 0.01:
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: {heading:.5f}°")
        drive.stop()
        sleep(1)
        
        drive.steer(RIGHT)
        sleep(1)
        heading = imu.get_heading()
        sleep(0.5)
        drive.backward(rs)
        while heading < 190:
            current_time = time.time()
            if current_time-last_heading_time > 0.01:
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: {heading:.5f}°")
        drive.stop()
def red_rightwall_turn(CLOCKWISE):
    global last_heading_time
    drive.driveencoder(150,rs)
    sleep(1)
    drive.steer(LEFT)
    sleep(1)
    heading = imu.get_heading()
    sleep(0.5)
    drive.forward(rs)
    while heading > 300 or heading < 180:
        current_time = time.time()
        if current_time-last_heading_time > 0.01:
            heading = imu.get_heading()
            last_heading_time = current_time
            print(f"Heading: {heading:.5f}°")
    drive.stop()
    sleep(1)

    drive.steer(CENTER)
    sleep(1)
    drive.driveencoder_backward(200,rs)
    sleep(1)
    
try:
    #drive.forward(rs)
    while True:
        frame = camera.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        output = frame.copy()
        (detections, color_detections, black_detections, pillar_detections, masks) = vision.obstacle_detections(frame)
        
        output = vision.annotate(frame, color_detections, black_detections, pillar_detections)

        red_blob = vision.largest_detection(detections["RED"])
        green_blob = vision.largest_detection(detections["GREEN"])
        black_blob = vision.largest_detection(detections["BLACK"])

        red_detected = red_blob is not None
        green_detected = green_blob is not None
        obstacle_detected = red_detected or green_detected

        # Crash zone: TRUE when a RED or GREEN obstacle overlaps
        # the crash-zone ROI.
#         crashZone = False
#         rx1, ry1, rx2, ry2 = vision.CRASH_ZONE_ROI

#         for obstacle in (red_blob, green_blob):
#             if obstacle is not None:
#                 ox1 = obstacle["x"]
#                 oy1 = obstacle["y"]
#                 ox2 = ox1 + obstacle["w"]
#                 oy2 = oy1 + obstacle["h"]
# 
#                 if (
#                     ox1 < rx2 and
#                     ox2 > rx1 and
#                     oy1 < ry2 and
#                     oy2 > ry1
#                 ):
#                     crashZone = True
#                     break

        blue_blob = vision.largest_detection(detections["BLUE"])
        orange_blob = vision.largest_detection(detections["ORANGE"])
        magenta_blob = vision.largest_detection(detections["MAGENTA"])

        center_black_blob = None
        left2_black_blob = None
        right2_black_blob = None
        left1_black_blob = None
        right1_black_blob = None

        for black in detections["BLACK"]:
            roi = black.get("roi")
            if roi == "CENTER_BLACK":
                if center_black_blob is None or black["area"] > center_black_blob["area"]:
                    center_black_blob = black
            if roi == "LEFT_2":
                if left2_black_blob is None or black["area"] > left2_black_blob["area"]:
                    left2_black_blob = black
            if roi == "RIGHT_2":
                if right2_black_blob is None or black["area"] > right2_black_blob["area"]:
                    right2_black_blob = black
            if roi == "LEFT_1":
                if left1_black_blob is None or black["area"] > left1_black_blob["area"]:
                    left1_black_blob = black
            if roi == "RIGHT_1":
                if right1_black_blob is None or black["area"] > right1_black_blob["area"]:
                    right1_black_blob = black
        
        centerBlackZone = center_black_blob is not None
        leftDZone = left2_black_blob is not None
        rightDZone = right2_black_blob is not None
        
        left_target = None
        right_target = None
        black_w = 0
        left_y = 0
        right_y = 0
#         if black_blob:
#             x = black_blob["x"]
#             y = black_blob["y"]
#             w = black_blob["w"]
#             h = black_blob["h"]
#             cx = black_blob["cx"]
#             black_w = w
#             if CLOCKWISE is None:
# 
#                 if cx < X_MID:
#                     CLOCKWISE = True
#                     print("CLOCKWISE")
# 
#                 else:
#                     CLOCKWISE = False
#                     print("ANTICLOCKWISE")
        if left1_black_blob:
            x = left1_black_blob["x"]
            y = left1_black_blob["y"]
            w = left1_black_blob["w"]
            h = left1_black_blob["h"]
            left_y = (y + h)
            left_target = (x + w, y + h)
            vision.draw_target(output,left_target,vision.YELLOW,"LEFT_1")

        if right1_black_blob:
            x = right1_black_blob["x"]
            y = right1_black_blob["y"]
            w = right1_black_blob["w"]
            h = right1_black_blob["h"]
            right_y = (y + h)
            right_target = (x, y + h)
            vision.draw_target(output,right_target,vision.YELLOW,"RIGHT_1")
# 
#         if round_complete:
#             if CLOCKWISE:
#                 right_target = None
#             else:
#                 left_target = None
        
        # ----------------------------------------------------
        # GREEN
        # ----------------------------------------------------
        if CLOCKWISE is None:

                if left1_black_blob:
                    CLOCKWISE = True
                    print("CLOCKWISE")

                else:
                    CLOCKWISE = False
                    print("ANTICLOCKWISE")
                    
        green_target = None

        if green_detected:
            x = green_blob["x"]
            y = green_blob["y"]
            h = green_blob["h"]
            green_y = green_blob["y"]+green_blob["h"]
            green_target = (x, y + h)
            vision.draw_target(output, green_target, vision.DRAW_COLORS["GREEN"], "GREEN")
#             if round_complete:
#                 if CLOCKWISE:
#                     rightDZone = green_target
#                     green_target = False
#                 else:
#                     leftDZone = green_target
#                     green_target = False
        # ----------------------------------------------------
        # RED
        # ----------------------------------------------------

        red_target = None
        red_y = 0
        green_y = 0
        if red_detected:
            x = red_blob["x"]
            y = red_blob["y"]
            w = red_blob["w"]
            h = red_blob["h"]
            red_y = red_blob["y"]+red_blob["h"]
            red_target = (x + w, y + h)
            vision.draw_target(output, red_target, vision.DRAW_COLORS["RED"], "RED")
#             if round_complete:
#                 if CLOCKWISE:
#                     right_target = red_target
#                     red_target = False
#                 else:
#                     left_target = red_target
#                     red_target = False
        if green_target and red_target:
            _,red_y = red_target
            _,green_y = green_target
            if red_y > green_y:
                green_target = False
            elif green_y > red_y:
                red_target = False
        # ----------------------------------------------------
        # DISPLAY COLORS
        # ----------------------------------------------------

        if magenta_blob: #added
            point = (magenta_blob["x"] + magenta_blob["w"], magenta_blob["y"])
            m1 = magenta_blob["x"]
            m2 = magenta_blob["x"] + magenta_blob["w"]
            if red_target:
                red_x, red_y = red_target
                if red_x > m1 and red_x < m2:
                    red_target = False
            if CLOCKWISE or round_complete:
                #print("**********************")
                left_target = (magenta_blob["x"] + magenta_blob["w"], magenta_blob["y"])
            else:
#                    print("=======================")
                right_target = (magenta_blob["x"], magenta_blob["y"])
            vision.draw_target(output, point, vision.DRAW_COLORS["MAGENTA"], "MAGENTA")

        if blue_blob:
            point = (blue_blob["x"] + blue_blob["w"], blue_blob["y"] + blue_blob["h"])
            vision.draw_target(output, point, vision.DRAW_COLORS["BLUE"], "BLUE")

        if orange_blob:
            point = (orange_blob["x"] + orange_blob["w"], orange_blob["y"] + orange_blob["h"])
            vision.draw_target(output, point, vision.DRAW_COLORS["ORANGE"], "ORANGE")

        
        # ----------------------------------------------------
        # DRIVE
        # ----------------------------------------------------
        current_time = time.time()

#         if magenta_blob and current_time - last_purple_time > COOLDOWN and not inside_park:
#             lap_count += 1
#             last_purple_time = current_time
                    #("Line :", line_count)
        if orange_blob and current_time - last_orange_time > COOLDOWN:
                line_count += 1
                last_orange_time = current_time
#                 print("Line :", line_count)
        
        if line_count >= total_line and not round_complete:#and current_time - last_orange_time > 3 and not round_complete:
            drive.steer(CENTER)
            drive.stop()
            sleep(2)
            round_complete = True
            
            if green_y > 180:
                print("Green True",green_y)
                green_turn(CLOCKWISE)
            elif red_y > 180:
                print("Red True", red_y)
                red_turn(CLOCKWISE)
            elif left_y and right_y:
                if left_y > right_y:                    
                    print("LeftWall True Inner")
                    leftwall_turn(CLOCKWISE)
                else:
                    print("RightWall True Enner")
                    rightwall_turn(CLOCKWISE)
            elif right_y:
                print("RightWall True")
                rightwall_turn(CLOCKWISE)
            elif left_y:
                print("LeftWall True")
                leftwall_turn(CLOCKWISE)
            else:
                green_turn(CLOCKWISE)
                print("ELSE")
                drive.driveencoder_backward(200,rs)
            if CLOCKWISE:
                break
            else:
                rs = 25
                drive.forward(rs)
            
        elif round_complete and orange_blob:
            drive.stop()
            drive.steer(CENTER)
            sleep(1)
            drive.steer(RIGHT)
            sleep(1)
            heading = imu.get_heading()
            sleep(0.5)
            drive.forward(rs)
            while heading > 90: 
                current_time = time.time()
                if current_time-last_heading_time > 0.01:
                    heading = imu.get_heading()
                    last_heading_time = current_time
                    print(f"Heading: {heading:.5f}°")
            drive.stop()
            sleep(0.5)
            drive.steer(LEFT)
            sleep(1)
            heading = imu.get_heading()
            sleep(0.5)
            drive.backward(rs)
            while heading > 3: 
                current_time = time.time()
                if current_time-last_heading_time > 0.01:
                    heading = imu.get_heading()
                    last_heading_time = current_time
                    print(f"Heading: {heading:.5f}°")
            drive.stop()
            sleep(0.5)
            drive.steer(CENTER)
            sleep(1)
            break
        elif inside_park:
            if CLOCKWISE:
                drive.steer(LEFT)
                sleep(1)
                heading = imu.get_heading()
                sleep(0.5)
                drive.backward(rs)
                while heading > 335 or heading < 90: 
                    current_time = time.time()
                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")
                drive.stop()
                drive.steer(RIGHT)
                sleep(1)
                drive.forward(rs)
                while heading > 290 or heading < 1: 
                    current_time = time.time()
                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")
                drive.stop()
                drive.steer(CENTER)
                sleep(1)
                drive.driveencoder(350,rs)
                drive.stop()
                drive.steer(RIGHT)
                sleep(1)
                heading = imu.get_heading()
                sleep(0.5)
                drive.backward(rs)
                while heading < 350 : 
                    current_time = time.time()
                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")
            else:
                drive.steer(RIGHT)
                sleep(1)
                heading = imu.get_heading()
                sleep(0.5)
                drive.backward(rs)
                while heading < 35 or heading > 300: 
                    current_time = time.time()
                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")
                drive.stop()
                drive.steer(LEFT)
                sleep(1)
                drive.forward(rs)
                while heading < 80 : 
                    current_time = time.time()
                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")
                drive.stop()
                drive.steer(CENTER)
                sleep(0.1)
                drive.forward(rs)
                sleep(1.5)
                drive.stop()
                drive.steer(LEFT)
                sleep(1)
                heading = imu.get_heading()
                sleep(0.5)
                drive.backward(rs)
                while heading > 10 : 
                    current_time = time.time()
                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")
            drive.stop()
            drive.steer(CENTER)
            sleep(1.5)
            drive.driveencoder_backward(30,rs)
            drive.stop()
            sleep(2)
            angle = CENTER
            inside_park = False
            drive.forward(rs)    
        # ====================================================
        # STEERING LOGIC
        # ====================================================
        elif rightDZone and not round_complete:
            print("Right D Zone") #+ 15
            if round_complete and not CLOCKWISE:
                angle = CENTER
            else:
                angle = LEFT
        elif leftDZone:
            print("Left D Zone")
            angle = RIGHT #+ 15
#         elif crashZone:
#             drive.steer(CENTER)
#             drive.stop()
#             sleep(1)
#             drive.driveencoder_backward(80,rs)
#             current_time = current_time - 2
#             drive.forward(rs)
        elif green_target and not round_complete:
#             print("greenFOllow")
            green_x, green_y = green_target
            #print("GREEN OBSTACLE DETECTED : ", green_x)
#             angle = LEFT
            if round_complete and not CLOCKWISE:
                angle = CENTER + (green_x - 10) * (KP+0.03)
            else:
                angle = CENTER + (green_x - (WIDTH - 10)) * (KP+0.03)
                #print("green Angle : ", angle)

        elif red_target and not round_complete:
#             print("red_follow")
            red_x, red_y = red_target
            #print("RED OBSTACLE DETECTED : ", red_x)
            if round_complete and CLOCKWISE:
                angle = CENTER + (red_x - (WIDTH - 10)) * (KP+0.03)
            else:
                angle = CENTER + (red_x - 10) * (KP+0.03)
                #print("red Angle : ", angle)

        elif centerBlackZone and left_target and right_target and not round_complete:
            if CLOCKWISE:
                angle = RIGHT #- 15
            else:
                angle = LEFT #+ 15
                
        elif left_target and right_target and not round_complete:
            left_x, left_y = left_target
            right_x, right_y = right_target
            left_distance = left_x
            right_distance = WIDTH - right_x
            error = left_distance - right_distance
            angle = CENTER + error * KP
#             print("LRLRLRLRLRLRLRLRLRLRLRLR")
        elif left_target: 
            only_x, _ = left_target
            if round_complete:
#                     print("LLLL - Follow ", only_x)
                angle = CENTER + (only_x - 150) * 0.4
            else:
#                 print("LLLLLLLLLLLLLLLLLLLL")
                if CLOCKWISE:
                    angle = RIGHT
                else:
                    angle = CENTER + (only_x - 10) * 0.09
        elif right_target and not round_complete:
#             print("RRRRRRRRRRRRRR")
            only_x, _ = right_target
            if CLOCKWISE:
                angle = CENTER + (only_x - (WIDTH - 10)) * 0.07
            else:
                angle = LEFT
        else:
            if round_complete:
#                 print("CENTER_Target_Following")
                angle = CENTER - 15 #- 10
            else:
                #print("CCCCCCCCCCCCCCCCCCCCCC")
                if CLOCKWISE:
                    angle = CENTER + 12 #+ 20 if CLOCKWISE else CENTER - 20
                else:
                    angle = CENTER - 12
#         print("Angle : ",angle)
        
        drive.steer(angle)
        
        # ----------------------------------------------------
        # FPS
        # ----------------------------------------------------

        fps_frames += 1
        now = time.perf_counter()

        if now - fps_start >= 1.0:
            loop_fps = fps_frames / (now - fps_start)
            fps_frames = 0
            fps_start = now

        cv2.putText(output, f"FPS: {loop_fps:.1f}", (10, HEIGHT - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, vision.WHITE, 2)

        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

        cv2.imshow("WRO TEST LAP", output)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            drive.steer(CENTER)
            drive.stop()
            sleep(2)
            break

# ============================================================
# SHUTDOWN
# ============================================================

finally:
    drive.steer(CENTER)
    sleep(2)
        
    camera.stop()
    camera.close()
    cv2.destroyAllWindows()

    time.sleep(1)
    parking.run_parking_clockwise()
    
    print("TEST LAP STOPPED")