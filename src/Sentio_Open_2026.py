# ============================================================
# F_Open_23.py
# ============================================================

import cv2
import time
from time import sleep

import F_driveEnc_23 as drive
import F_Open_Vision_23 as vision
import RPi.GPIO as GPIO


# ============================================================
# BUTTON + LED
# ============================================================

BUTTON_PIN = 18
LED_PIN = 12

GPIO.setmode(GPIO.BCM)

GPIO.setup(
    BUTTON_PIN,
    GPIO.IN
)

GPIO.setup(
    LED_PIN,
    GPIO.OUT
)

GPIO.output(
    LED_PIN,
    GPIO.LOW
)

button_state = False
last_button = 0


print()
print("========================================")
print("WAITING FOR START BUTTON")
print("GPIO 18")
print("========================================")


# ============================================================
# WAIT FOR START BUTTON
# ============================================================

while not button_state:

    button = GPIO.input(
        BUTTON_PIN
    )

    if (
        button == 1
        and
        last_button == 0
    ):

        button_state = not button_state

        print(
            "Button State:",
            button_state
        )

        if button_state:

            GPIO.output(
                LED_PIN,
                GPIO.HIGH
            )

        else:

            GPIO.output(
                LED_PIN,
                GPIO.LOW
            )

    last_button = button

    time.sleep(0.01)


# ============================================================
# SETTINGS
# ============================================================

COOLDOWN = 0.4

round_complete = False

last_orange_time = 0
last_blue_time = 0

line_count = 0
total_line = 12

rs = 70
KP = 0.013

FINAL_APPROACH_TIME = 1.5
final_approach_start = None


# ============================================================
# DRIVE SETTINGS
# ============================================================

RIGHT = drive.RIGHT
LEFT = drive.LEFT
CENTER = drive.CENTER


# ============================================================
# CAMERA SETTINGS
# ============================================================

WIDTH = vision.WIDTH
HEIGHT = vision.HEIGHT
X_MID = vision.WIDTH / 2


# ============================================================
# START CAMERA
# ============================================================

camera = vision.start_camera()


# ============================================================
# INITIAL SETTINGS
# ============================================================

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
# MAIN PROGRAM
# ============================================================

try:

    drive.forward(rs)

    while True:

        # ====================================================
        # CAMERA FRAME
        # ====================================================

        frame = camera.capture_array()

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_RGB2BGR
        )


        # ====================================================
        # OUTPUT
        # ====================================================

        if vision.SHOW_VISION_DEBUG:

            output = frame.copy()

        else:

            output = frame


        # ====================================================
        # VISION DETECTION
        # ====================================================

        (
            detections,
            color_detections,
            black_detections,
            pillar_detections,
            masks
        ) = vision.obstacle_detections(frame)


        # ====================================================
        # VISION DEBUG
        # ====================================================

        if vision.SHOW_VISION_DEBUG:

            output = vision.annotate(
                frame,
                color_detections,
                black_detections,
                pillar_detections
            )


        # ====================================================
        # LARGEST DETECTIONS
        # ====================================================

        black_blob = vision.largest_detection(
            detections["BLACK"]
        )

        blue_blob = vision.largest_detection(
            detections["BLUE"]
        )

        orange_blob = vision.largest_detection(
            detections["ORANGE"]
        )


        # ====================================================
        # BLACK BLOBS
        # ====================================================

        center_black_blob = None
        left2_black_blob = None
        right2_black_blob = None
        left1_black_blob = None
        right1_black_blob = None


        for black in detections["BLACK"]:

            roi = black.get("roi")


            if roi == "CENTER_BLACK":

                if (
                    center_black_blob is None
                    or
                    black["area"] > center_black_blob["area"]
                ):

                    center_black_blob = black


            if roi == "LEFT_2":

                if (
                    left2_black_blob is None
                    or
                    black["area"] > left2_black_blob["area"]
                ):

                    left2_black_blob = black


            if roi == "RIGHT_2":

                if (
                    right2_black_blob is None
                    or
                    black["area"] > right2_black_blob["area"]
                ):

                    right2_black_blob = black


            if roi == "LEFT_1":

                if (
                    left1_black_blob is None
                    or
                    black["area"] > left1_black_blob["area"]
                ):

                    left1_black_blob = black


            if roi == "RIGHT_1":

                if (
                    right1_black_blob is None
                    or
                    black["area"] > right1_black_blob["area"]
                ):

                    right1_black_blob = black


        # ====================================================
        # BLACK ZONES
        # ====================================================

        centerBlackZone = (
            center_black_blob is not None
        )

        leftDZone = (
            left2_black_blob is not None
        )

        rightDZone = (
            right2_black_blob is not None
        )


        # ====================================================
        # TARGETS
        # ====================================================

        left_target = None
        right_target = None

        black_w = 0

        left_y = 0
        right_y = 0


        # ====================================================
        # LEFT BLACK TARGET
        # ====================================================

        if left1_black_blob:

            x = left1_black_blob["x"]
            y = left1_black_blob["y"]
            w = left1_black_blob["w"]
            h = left1_black_blob["h"]

            left_y = y + h

            left_target = (
                x + w,
                y + h
            )

            vision.draw_target(
                output,
                left_target,
                vision.YELLOW,
                "LEFT_1"
            )


        # ====================================================
        # RIGHT BLACK TARGET
        # ====================================================

        if right1_black_blob:

            x = right1_black_blob["x"]
            y = right1_black_blob["y"]
            w = right1_black_blob["w"]
            h = right1_black_blob["h"]

            right_y = y + h

            right_target = (
                x,
                y + h
            )

            vision.draw_target(
                output,
                right_target,
                vision.YELLOW,
                "RIGHT_1"
            )


        # ====================================================
        # BLUE TARGET
        # ====================================================

        if blue_blob:

            point = (
                blue_blob["x"] + blue_blob["w"],
                blue_blob["y"] + blue_blob["h"]
            )

            vision.draw_target(
                output,
                point,
                vision.DRAW_COLORS["BLUE"],
                "BLUE"
            )


        # ====================================================
        # ORANGE TARGET
        # ====================================================

        if orange_blob:

            point = (
                orange_blob["x"] + orange_blob["w"],
                orange_blob["y"] + orange_blob["h"]
            )

            vision.draw_target(
                output,
                point,
                vision.DRAW_COLORS["ORANGE"],
                "ORANGE"
            )


        # ====================================================
        # DETERMINE DIRECTION
        # ====================================================

        if CLOCKWISE is None:

            if orange_blob:

                CLOCKWISE = True

                print("CLOCKWISE")


            if blue_blob:

                CLOCKWISE = False

                print("ANTICLOCKWISE")


        # ====================================================
        # LINE COUNT
        # ====================================================

        current_time = time.time()


        if (
            orange_blob
            and
            current_time - last_orange_time > COOLDOWN
            and
            CLOCKWISE
        ):

            line_count += 1

            last_orange_time = current_time

            print(
                "Line Count : ",
                line_count
            )


        elif (
            blue_blob
            and
            current_time - last_blue_time > COOLDOWN
            and
            not CLOCKWISE
        ):

            line_count += 1

            last_blue_time = current_time

            print(
                "Line Count : ",
                line_count
            )


        # ====================================================
        # FINAL APPROACH START
        # ====================================================

        if (
            line_count >= total_line
            and
            final_approach_start is None
        ):

            final_approach_start = (
                time.perf_counter()
            )

            print(
                "FINAL APPROACH STARTED"
            )


        # ====================================================
        # FINAL APPROACH
        # ====================================================

        if final_approach_start is not None:

            final_approach_elapsed = (
                time.perf_counter()
                -
                final_approach_start
            )


            if (
                final_approach_elapsed
                >=
                FINAL_APPROACH_TIME
            ):

                drive.steer(CENTER)

                drive.stop()

                print(
                    "FINAL APPROACH COMPLETE"
                )

                break


        # ====================================================
        # STEERING
        # ====================================================

        if rightDZone:

            angle = LEFT + 10


        elif leftDZone:

            angle = RIGHT - 10


        elif (
            centerBlackZone
            and
            left_target
            and
            right_target
            and
            CLOCKWISE is not None
        ):

            if CLOCKWISE:

                angle = RIGHT - 10

            else:

                angle = LEFT + 10


        elif left_target and right_target:

            left_x, left_y = left_target
            right_x, right_y = right_target

            left_distance = left_x

            right_distance = (
                WIDTH - right_x
            )

            error = (
                left_distance
                -
                right_distance
            )

            angle = (
                CENTER
                +
                error * 0.07
            )


        elif left_target:

            only_x, _ = left_target


            if CLOCKWISE:

                angle = RIGHT + 10

            else:

                angle = (
                    CENTER
                    +
                    (only_x - 30) * 0.07
                )


        elif right_target:

            only_x, _ = right_target


            if not CLOCKWISE:

                angle = LEFT + 10

            else:

                angle = (
                    CENTER
                    +
                    (
                        only_x
                        -
                        (WIDTH - 30)
                    ) * 0.07
                )


        else:

            if CLOCKWISE is None:

                angle = CENTER

            elif CLOCKWISE:

                angle = CENTER + 10

            else:

                angle = CENTER - 10


        # ====================================================
        # APPLY STEERING
        # ====================================================

        drive.steer(angle)


        # ====================================================
        # FPS
        # ====================================================

        fps_frames += 1

        now = time.perf_counter()


        if (
            now - fps_start
            >= 1.0
        ):

            loop_fps = (
                fps_frames
                /
                (now - fps_start)
            )

            fps_frames = 0

            fps_start = now


        # ====================================================
        # DEBUG DISPLAY
        # ====================================================

        if vision.SHOW_VISION_DEBUG:

            cv2.putText(
                output,
                f"FPS: {loop_fps:.1f}",
                (
                    10,
                    HEIGHT - 18
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                vision.WHITE,
                2
            )


            cv2.imshow(
                "WRO TEST LAP",
                output
            )


            if (
                cv2.waitKey(1) & 0xFF
            ) == ord("q"):

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

    drive.stop()

    camera.stop()

    camera.close()

    cv2.destroyAllWindows()

    GPIO.output(
        LED_PIN,
        GPIO.LOW
    )

    GPIO.cleanup()

    time.sleep(1)

    print(
        "TEST LAP STOPPED"
    )


