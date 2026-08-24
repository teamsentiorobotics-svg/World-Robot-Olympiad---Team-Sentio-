import cv2
import time
from time import sleep
from heading import MPU6050Heading
import drive
import vision
import parking

imu = MPU6050Heading()
last_heading_time = 0

# ============================================================
# ROBOT CONTROL SETTINGS
# ============================================================
COOLDOWN = 7
total_lap = 3
lap_count = 0
round_complete = False
start_parking = False #extra added
last_purple_time = 0
end_time = 0.5
purple_gone_time = None

rs =  45 #changed from 50
KP = 0.014
RIGHT = drive.RIGHT
LEFT = drive.LEFT
CENTER = drive.CENTER

OBSTACLE_ACTION_AREA = 18000

CENTER = drive.CENTER
WIDTH = vision.WIDTH
HEIGHT = vision.HEIGHT
X_MID = vision.X_MID

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
inside_park = True
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
    
try:
    while True:

        # ----------------------------------------------------
        # CAMERA + DETECTION
        # ----------------------------------------------------

        frame = camera.capture_array()
        output = frame.copy()

        detections = vision.detect_all(frame)
        vision.draw_all(output, detections)

        # ----------------------------------------------------
        # LARGEST OBJECTS
        # ----------------------------------------------------
        
        MIN_COLOR_AREA = 2500

        red_blob = vision.largest_detection(detections["RED"])
        green_blob = vision.largest_detection(detections["GREEN"])
        black_blob = vision.largest_detection(detections["BLACK"])
        blue_blob = vision.largest_detection(detections["BLUE"])
        orange_blob = vision.largest_detection(detections["ORANGE"])
        magenta_blob = vision.largest_detection(detections["MAGENTA"])
        
        if red_blob and red_blob["area"] < MIN_COLOR_AREA:
            red_blob = None
        if green_blob and green_blob["area"] < MIN_COLOR_AREA:
            green_blob = None
        
        

        # ----------------------------------------------------
        # BLACK WALL
        # ----------------------------------------------------

        left_target = None
        right_target = None
        black_w = 0
        if black_blob:
            x = black_blob["x"]
            y = black_blob["y"]
            w = black_blob["w"]
            h = black_blob["h"]
            cx = black_blob["cx"]
            black_w = w
            black_target = (x, y + h)

            if CLOCKWISE is None:
                if cx < X_MID:
                    CLOCKWISE = True
                    print("CLOCKWISE")
                else:
                    CLOCKWISE = False
            else:
                if CLOCKWISE:
                    left_target = (x + w, y + h) if cx <= X_MID else None
                    right_target = (x, y + h) if cx > X_MID else None
                else:
                    right_target = (x, y + h) if cx >= X_MID else None
                    left_target = (x + w, y + h) if cx < X_MID else None

            vision.draw_target(output, black_target, vision.YELLOW, "BLACK")

        if round_complete:
            if CLOCKWISE:
                right_target = False
            else:
                left_target = False

        # ----------------------------------------------------
        # GREEN
        # ----------------------------------------------------

        green_target = None

        if green_blob and green_blob["area"] > OBSTACLE_ACTION_AREA:
            x = green_blob["x"]
            y = green_blob["y"]
            h = green_blob["h"]
            green_target = (x, y + h)
            print("Green Area : ",green_blob["area"])
            vision.draw_target(output, green_target, vision.DRAW_COLORS["GREEN"], "GREEN")

            if round_complete:
                if CLOCKWISE:
                    right_target = green_target
                    green_target = False
                else:
                    left_target = green_target
                    green_target = False

        # ----------------------------------------------------
        # RED
        # ----------------------------------------------------

        red_target = None

        if red_blob and red_blob["area"] > OBSTACLE_ACTION_AREA:
            x = red_blob["x"]
            y = red_blob["y"]
            w = red_blob["w"]
            h = red_blob["h"]
            red_target = (x + w, y + h)
            vision.draw_target(output, red_target, vision.DRAW_COLORS["RED"], "RED")

            if round_complete:
                if CLOCKWISE:
                    right_target = red_target
                    red_target = False
                else:
                    left_target = red_target
                    red_target = False
        
        # ----------------------------------------------------
        # DISPLAY COLORS
        # ----------------------------------------------------

        if magenta_blob and magenta_blob["area"] > 50000:
            x = magenta_blob["x"]
            y = magenta_blob["y"]
            w = magenta_blob["w"]
            h = magenta_blob["h"]

            if CLOCKWISE:
                left_target = (x+w, y+h)
            else:
                right_target = (x, y + h)

            point = (magenta_blob["x"] + magenta_blob["w"], magenta_blob["y"])
            vision.draw_target(output, point, vision.DRAW_COLORS["MAGENTA"], "MAGENTA")

        if blue_blob:
            point = (blue_blob["x"] + blue_blob["w"], blue_blob["y"] + blue_blob["h"])
            vision.draw_target(output, point, vision.DRAW_COLORS["BLUE"], "BLUE")

        if orange_blob:
            point = (orange_blob["x"] + orange_blob["w"], orange_blob["y"] + orange_blob["h"])
            vision.draw_target(output, point, vision.DRAW_COLORS["ORANGE"], "ORANGE")

        # ----------------------------------------------------
        # ROI
        # ----------------------------------------------------

        cv2.line(output, (0, vision.ROI_Y), (WIDTH - 1, vision.ROI_Y), vision.YELLOW, 2)

        # ----------------------------------------------------
        # DRIVE
        # ----------------------------------------------------

        current_time = time.time()

        if magenta_blob and current_time - last_purple_time > COOLDOWN and not inside_park:
            lap_count += 1
            last_purple_time = current_time
            #print("Line :", line_count)

        #     if orange_detected and current_time - last_orange_time > LINE_COOLDOWN:
        #             line_count += 1
        #             last_orange_time = current_time
        #             #print("Line :", line_count)
        #     
        #     if line_count == total_lines and current_time - last_orange_time > LINE_COOLDOWN:
        #         steer(CENTER)
        #         stop()
        #         sleep(2)
        #         forward(rs)
        #         final = True
        #         round_complete = True
    
                        
        if lap_count == total_lap+1 and not magenta_blob and not round_complete:    #added and changed

            if purple_gone_time is None:
                purple_gone_time = time.time()
                print("Purple wall gone - 3 second timer started")

            elif time.time() - purple_gone_time >= end_time:

                print("3 seconds complete - stopping")
                drive.steer(CENTER)
                drive.stop()
                sleep(2)
                drive.forward(rs)
                round_complete = True
                
        #         video.release()
        # break
        # print("Line", line_count)

        if inside_park:
            if CLOCKWISE:
                last_magenta_time = time.time()
                heading = imu.get_heading()

                drive.steer(LEFT)
                sleep(1)
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

                while heading > 280:
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
                drive.steer(RIGHT)
                drive.backward(rs)

                heading = imu.get_heading()

                while heading <= 358 : 
                    current_time = time.time()

                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")

            else:
                heading = imu.get_heading()

                drive.steer(RIGHT)
                sleep(1)
                drive.backward(rs)

                while heading < 35 or heading > 300: #changed from 90
                    current_time = time.time()

                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")

                drive.stop()
                drive.steer(LEFT)
                sleep(1)
                drive.forward(rs)

                while heading < 90: #changed from 90
                    current_time = time.time()

                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")

                drive.stop()
                drive.steer(CENTER)
                sleep(0.1)
                drive.forward(rs )
                sleep(1.4)
                drive.stop()
                drive.steer(LEFT)
                sleep(1)
                drive.backward(rs)

                heading = imu.get_heading()

                while heading > 3 : #changed from 2
                    current_time = time.time()

                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")
               
            drive.stop()
            drive.steer(CENTER)
            sleep(1)
            drive.backward(38)
            sleep(0.5)
            drive.stop()
            sleep(1)

            angle = CENTER
            inside_park = False

            drive.forward(rs)    

        # ====================================================
        # STEERING LOGIC
        # ====================================================

        if round_complete and black_w >= (WIDTH-100):

            if CLOCKWISE:
                drive.stop()
                drive.steer(CENTER)
                sleep(2)

                imu.reset_heading()

                # FIrst Turnnot 
                drive.steer(RIGHT)
                sleep(2)
                drive.forward(rs)

                heading = imu.get_heading()

                while heading > 270 or heading < 90: 
                    current_time = time.time()

                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")

                drive.stop()
                drive.steer(LEFT)
                sleep(2)
                drive.backward(rs)

                while heading > 180: 
                    current_time = time.time()

                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")

            else:
                drive.stop()
                drive.steer(CENTER)
                sleep(2)
                
                # FIrst Turnnot 
                drive.steer(LEFT)
                sleep(2)
                drive.forward(rs)

                heading = imu.get_heading()

                while heading > 270 or heading < 90: 
                    current_time = time.time()

                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")

                drive.stop()
                drive.steer(RIGHT)
                sleep(2)
                drive.backward(rs)

                while heading < 180: 
                    current_time = time.time()

                    if current_time-last_heading_time > 0.01:
                        heading = imu.get_heading()
                        last_heading_time = current_time
                        print(f"Heading: {heading:.5f}°")

            drive.steer(CENTER)
            drive.stop()
            sleep(2)

            if not CLOCKWISE:
                CLOCKWISE = True
                drive.forward(rs)
            else:
                break

        elif green_target:
            green_x, green_y = green_target

            if CLOCKWISE:
                if green_y > 100:
                    angle = CENTER + (green_x - (WIDTH)) * KP

                elif green_x > WIDTH / 2 and green_y < 100:
                    if left_target:
                        only_x, only_y = left_target

#                         if only_y > 200:
                        angle = CENTER + only_x * KP
#                         else:
#                             angle = CENTER + 2

                    elif right_target:
                        only_x, _ = right_target
                        angle = CENTER + (only_x - (WIDTH - 50)) * KP

                    else:
                        angle = CENTER + 20

                else:
                    angle = CENTER + (green_x - (WIDTH - 500)) * KP

            else:
                angle = CENTER + (green_x - (WIDTH - 100)) * KP

        elif red_target:
            red_x, red_y = red_target

            if CLOCKWISE:
                if red_y > 100: 
                    angle = CENTER + (red_x - 150) * KP

                elif red_x > WIDTH / 2 and red_y < 100: 
                    if left_target:
                        only_x, _ = left_target
                        angle = CENTER + only_x * KP

                    elif right_target:
                        only_x, _ = right_target
                        angle = CENTER + (only_x - (WIDTH - 50)) * KP

                    else:
                        angle = CENTER + 20

                else:
                    angle = CENTER + (red_x - WIDTH / 2) * KP

            else:
                angle = CENTER + (red_x - 100) * KP

        elif left_target and right_target:
            left_x, left_y = left_target
            right_x, right_y = right_target

    #         left_distance = left_x
    #         right_distance = WIDTH - right_x
    #         error = left_distance - right_distance
    #         angle = CENTER + error * KP

            if round_complete:
                print("TWO_Target_Following")

                if CLOCKWISE:
                    angle = CENTER - 10
                else:
                    angle = CENTER + 10

            elif CLOCKWISE:
                angle = CENTER + 15

            else:
                angle = CENTER - 15

        elif left_target:
            only_x, only_y = left_target

            if round_complete:
                print("LEFT_Target_Following")

                if CLOCKWISE:
                    angle = CENTER + (only_x - 100) * 0.006
                else:
                    angle = CENTER + 10

            else:
#                 if only_y > 200:
                angle = CENTER + (only_x - 20) * KP if CLOCKWISE else CENTER + (only_x - 20) * KP
#                 else:
#                     angle = CENTER + 2

        elif right_target:
            only_x, only_y = right_target

            if round_complete:
                if CLOCKWISE:
                    angle = CENTER - 10
                else:
                    angle = CENTER + (only_x - (WIDTH - 300)) * 0.013
                    
            else:
                angle = CENTER + (only_x - (WIDTH - 100)) * KP if CLOCKWISE else CENTER - 15
          
        else:
            if round_complete:
                print("CENTER_Target_Following")

                if CLOCKWISE:
                    angle = CENTER - 10
                else:
                    angle = CENTER + 10

            else:
                angle = CENTER + 15 if CLOCKWISE else CENTER - 15

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

        cv2.putText(
            output,
            f"FPS: {loop_fps:.1f}",
            (10, HEIGHT - 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            vision.WHITE,
            2
        )

        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

        cv2.imshow("WRO TEST LAP", output)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            drive.stop()
            drive.steer(CENTER)
            time.sleep()
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


