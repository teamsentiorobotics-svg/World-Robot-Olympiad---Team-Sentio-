import time
import sys
import select

# ============================================================
# IMPORT DRIVE FUNCTIONS
# ============================================================

from drive import (
    steer,
    forward,
    stop,
    cleanup
)

# ============================================================
# IMPORT TOF FUNCTIONS
# ============================================================

from tof import (
    tof_init,
    read_tofs,
    tof_cleanup
)


# ============================================================
# SETTINGS
# ============================================================

SPEED = 25

# Steering center from your drive.py
CENTER = 75

# Maximum steering correction
MAX_CORRECTION = 25

# Wall-following gains
KP_DISTANCE = 3.0
KP_ANGLE = 1.2


# ============================================================
# CHECK FOR "q"
# ============================================================

def check_for_q():

    if select.select([sys.stdin], [], [], 0)[0]:

        key = sys.stdin.readline().strip().lower()

        if key == "q":
            return True

    return False


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # ASK FOR DESIRED WALL DISTANCE
    # --------------------------------------------------------

    target_distance = float(
        input("Enter desired distance from right wall (cm): ")
    )

    print()
    print("==========================================")
    print("         RIGHT WALL FOLLOWING")
    print("==========================================")
    print(f"Target distance: {target_distance:.1f} cm")
    print(f"Speed: {SPEED}%")
    print("------------------------------------------")
    print("Press 'q' + ENTER to stop.")
    print("==========================================")
    print()


    # --------------------------------------------------------
    # INITIALIZE TOF SENSORS
    # --------------------------------------------------------

    tof_init()


    # --------------------------------------------------------
    # CENTER STEERING
    # --------------------------------------------------------

    steer(CENTER)

    time.sleep(0.1)


    # --------------------------------------------------------
    # START MOVING
    # --------------------------------------------------------

    forward(SPEED)


    try:

        while True:

            # =================================================
            # CHECK FOR Q
            # =================================================

            if check_for_q():

                print("\n'q' pressed.")
                break


            # =================================================
            # READ TOF SENSORS
            # =================================================

            tof1, status1, tof2, status2 = read_tofs()


            # =================================================
            # CHECK SENSOR STATUS
            # =================================================
# 
#             if status1 != 0 or status2 != 0:
# 
#                 print(
#                     f"Invalid reading | "
#                     f"TOF1: {tof1} mm ({status1}) | "
#                     f"TOF2: {tof2} mm ({status2})"
#                 )

#                 # Keep moving straight.
#                 steer(CENTER)
# 
#                 time.sleep(0.05)
# 
#                 continue


            # =================================================
            # CONVERT MM TO CM
            # =================================================

            front_distance = tof1 / 10.0
            rear_distance = tof2 / 10.0


            # =================================================
            # AVERAGE DISTANCE FROM WALL
            # =================================================

            average_distance = (
                front_distance + rear_distance
            ) / 2.0


            # =================================================
            # DISTANCE ERROR
            # =================================================

            distance_error = (
                average_distance - target_distance
            )


            # =================================================
            # ANGLE ERROR
            # =================================================

            angle_error = (
                front_distance - rear_distance
            )


            # =================================================
            # CALCULATE STEERING CORRECTION
            # =================================================

            correction = (
                KP_DISTANCE * distance_error
                -
                KP_ANGLE * angle_error
            )


            # =================================================
            # LIMIT CORRECTION
            # =================================================

            correction = max(
                -MAX_CORRECTION,
                min(MAX_CORRECTION, correction)
            )


            # =================================================
            # CALCULATE SERVO ANGLE
            # =================================================

            steering_angle = CENTER - correction


            # Keep inside your drive.py servo limits
            steering_angle = max(
                40,
                min(110, steering_angle)
            )


            # =================================================
            # STEER
            # =================================================

            steer(steering_angle)


            # =================================================
            # DISPLAY
            # =================================================

            print(
                f"TOF1: {front_distance:5.1f} cm | "
                f"TOF2: {rear_distance:5.1f} cm | "
                f"Avg: {average_distance:5.1f} cm | "
                f"Error: {distance_error:6.2f} | "
                f"Steer: {steering_angle:5.1f}"
            )


            # =================================================
            # LOOP SPEED
            # =================================================

            time.sleep(0.03)


    except KeyboardInterrupt:

        print("\nKeyboard interrupt.")


    finally:

        # Stop only when program is exited
        stop()

        cleanup()
        tof_cleanup()

        print("Robot stopped.")
        print("Done.")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
