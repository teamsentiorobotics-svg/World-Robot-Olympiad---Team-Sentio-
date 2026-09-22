import cv2
import time
from time import sleep
from picamera2 import Picamera2
from heading import MPU6050Heading
import driveEnc as drive 
import N_VisionP_22 as vision
import N_TOF_19 as TUF

LEFT = drive.LEFT
RIGHT = drive.RIGHT
CENTER = drive.CENTER
# ============================================================
# SETTINGS
# ============================================================

clockwise = False

# Right wall follow distance/position
BLACK_FOLLOW = 150

# Robot speed
RS = 25

# Steering gain
KP = 0.4

# TOF threshold
# 200 mm = 20 cm
TOF_STOP_DISTANCE = 200

# NEW: Time before TOF starts detecting
TOF_START_DELAY = 3.0

# TOF detection cooldown BETWEEN detection #1 and #2
TOF_COOLDOWN = 1.2

CENTER = CENTER

# Vision resolution
WIDTH = vision.WIDTH
HEIGHT = vision.HEIGHT
X_MID = WIDTH // 2

FPS = 60


# ============================================================
# PARKING
# ============================================================

def run_parking_clockwise():

    imu = MPU6050Heading()
    last_heading_time = 0

    tof_detect_count = 0
    last_tof_detection_time = 0.0

    front_cam = Picamera2(0)

    front_config = front_cam.create_video_configuration(
        main={
            "size": (WIDTH, HEIGHT),
            "format": "RGB888"
        },
        controls={
            "FrameRate": FPS
        }
    )

    front_cam.configure(front_config)
    front_cam.start()

    sleep(2)

    print("==========================================")
    print("RIGHT WALL FOLLOW PARKING")
    print("==========================================")
    print("Vision          : N_Vision_9_18")
    print("Wall            : RIGHT BLACK WALL ONLY")
    print("Right D-Zone    : TURN LEFT")
    print("TOF             : TWO DETECTIONS REQUIRED")
    print(f"TOF Start Delay : {TOF_START_DELAY} seconds")
    print(f"TOF Cooldown    : {TOF_COOLDOWN} seconds")
    print(f"TOF Distance    : {TOF_STOP_DISTANCE} mm")
    print("1st TOF         : CONTINUE")
    print("2nd TOF         : STOP")
    print("Q               : STOP")
    print("==========================================")

    drive.steer(CENTER)
    sleep(0.8)

    fps_frames = 0
    fps_start = time.perf_counter()
    loop_fps = 0.0

    try:
        
        tof_start_time = time.monotonic()

        while True:

            right_wall = None
            rightDzone = False

            front_frame = front_cam.capture_array()
            front_frame = cv2.cvtColor(front_frame, cv2.COLOR_RGB2BGR)

            output = front_frame.copy()
            (detections, color_detections, black_walls, pillar_detections, masks) = vision.obstacle_detections(front_frame)

            output = vision.annotate(front_frame,color_detections,black_walls,pillar_detections)
            
            current_time = time.monotonic()

            tof_start_elapsed = (current_time - tof_start_time)
            if tof_start_elapsed >= TOF_START_DELAY:
                tof_distance = TUF.tof1.range
                print(f"TOF: {tof_distance} mm | "f"Detection Count: {tof_detect_count}/2")
                if tof_distance < TOF_STOP_DISTANCE:
                    if (tof_detect_count == 0 or current_time - last_tof_detection_time >= TOF_COOLDOWN):
                        tof_detect_count += 1
                        last_tof_detection_time = (current_time)
                        print("------------------------------------------")
                        print(f"TOF DETECTION " f"#{tof_detect_count}")
                        print(f"Distance: " f"{tof_distance} mm")

                        if tof_detect_count == 1:
                            print("FIRST TOF DETECTION")
                            print("Robot will CONTINUE")
                            print(f"Cooldown started: " f"{TOF_COOLDOWN} seconds")

                        elif tof_detect_count >= 2:
                            print("SECOND TOF DETECTION")
                            print("2 detections confirmed")
                            print("TOF SECOND DETECTION " "-> ROBOT STOP")
                            drive.stop()
                            cv2.putText(output,f"TOF STOP "f"#{tof_detect_count} - "f"{tof_distance} mm",(10, HEIGHT - 45),cv2.FONT_HERSHEY_SIMPLEX,0.65,vision.WHITE,2)
                            cv2.putText(output,"2 TOF DETECTIONS -> STOP",(10, HEIGHT - 18),cv2.FONT_HERSHEY_SIMPLEX,0.55,vision.WHITE,2)
                            cv2.imshow("FRONT CAMERA - RIGHT WALL",output)
                            cv2.waitKey(1)
                            break
                        print("------------------------------------------")
                    else:
                        remaining = (TOF_COOLDOWN - (current_time - last_tof_detection_time))
                        print(f"TOF < " f"{TOF_STOP_DISTANCE} mm " f"but cooldown active | " f"{remaining:.2f}s remaining")
            else:
                tof_distance = None
                remaining_start_delay = (TOF_START_DELAY - tof_start_elapsed)
                print(f"TOF START DELAY | " f"{remaining_start_delay:.2f}s remaining")
                cv2.putText(output, f"TOF ENABLES IN: " f"{remaining_start_delay:.1f}s", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.55, vision.WHITE, 2)
            
            black_blob = vision.largest_detection(detections["BLACK"])
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
            drive.forward(RS)   
            if rightDZone:
                print("Right D Zone")
                angle = LEFT
            elif right_target:
                only_x, only_y = right_target
                print("Right Target", only_x)
                angle = CENTER + (only_x - (WIDTH - BLACK_FOLLOW)) * KP
            else:
                print("Else...")
                angle = CENTER + 15
            drive.steer(angle)
            print(angle)
            
            if tof_detect_count == 1:
                elapsed = (current_time - last_tof_detection_time)
                remaining = max(0,TOF_COOLDOWN - elapsed)
                cv2.putText(output,f"TOF COOLDOWN: "f"{remaining:.1f}s",(10, 120),cv2.FONT_HERSHEY_SIMPLEX,0.55,vision.WHITE,2)

            fps_frames += 1
            now = time.perf_counter()
            if now - fps_start >= 1.0:
                loop_fps = (fps_frames / (now - fps_start))
                fps_frames = 0
                fps_start = now

            cv2.putText(output,f"FPS: {loop_fps:.1f}",(10, 30),cv2.FONT_HERSHEY_SIMPLEX,0.6,vision.WHITE,2)
            cv2.imshow("FRONT CAMERA - RIGHT WALL",output)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            
    finally:

        front_cam.stop()
        front_cam.close()
        
        drive.stop()
        drive.steer(CENTER)
        sleep(1)
        
        drive.backward(RS)
        while True:
            tof1_distance = TUF.tof1.range
            print(f"TOF 2 Distance: {tof1_distance} mm")
            if tof1_distance > 200:
                drive.stop()
                print("==========================================")
                print(f"TOF 2 detected obstacle at " f"{tof1_distance} mm")
                print("ROBOT STOPPED")
                print("==========================================")
                break
            
        sleep(1)
        drive.driveencoder_backward(55,RS)
        drive.stop()
        sleep(1)

        drive.steer(RIGHT)
        sleep(2)
        heading = imu.get_heading()
        imu.reset_heading()
        sleep(0.5)
        drive.backward(RS+10)
        while heading < 80 or heading > 330:
            current_time = time.time()
            if (current_time - last_heading_time > 0.01):
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: "f"{heading:.5f}°")

        drive.stop()
        drive.steer(CENTER)
        sleep(1)
        drive.driveencoder_backward(40,RS)
        sleep(0.4)
        drive.stop()
        sleep(1)

        drive.steer(CENTER)
        sleep(0.5)
        drive.forward(RS)
        while True:
            tof2_distance = TUF.tof3.range
            print(f"TOF 2 Distance: {tof2_distance} mm")
            if tof2_distance > 240:
                drive.stop()
                print("==========================================")
                print(f"TOF 2 detected obstacle at "f"{tof2_distance} mm")
                print("ROBOT STOPPED")
                print("==========================================")
                break
 
        sleep(1)
        drive.driveencoder(10,RS)
        sleep(0.4)
        drive.stop()
        sleep(1)
        
        drive.steer(RIGHT)
        sleep(2)
        heading = imu.get_heading()
        sleep(0.5)
        drive.backward(RS+10)  # change from 33
        while heading < 160:
            current_time = time.time()
            if (current_time - last_heading_time > 0.01):
                heading = imu.get_heading()
                last_heading_time = current_time
                print(f"Heading: "f"{heading:.5f}°")
        drive.stop()

        drive.steer(CENTER)
        sleep(2)
        
        drive.driveencoder(70,RS)
        drive.stop()

        cv2.destroyAllWindows()

        print(
            "RIGHT WALL FOLLOW TEST STOPPED"
        )

if __name__ == "__main__":
    run_parking_clockwise()
