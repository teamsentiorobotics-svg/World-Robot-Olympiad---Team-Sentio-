import RPi.GPIO as GPIO
from gpiozero import RotaryEncoder
from time import sleep, monotonic

# ============================================================
# ROBOT SETTINGS
# ============================================================

# ---------------- MOTOR ----------------

PWM_PIN = 13
IN1_PIN = 5
IN2_PIN = 6

# ---------------- SERVO ----------------

SERVO_PIN = 22

CENTER = 75
LEFT = 40
RIGHT = 110

# ---------------- ENCODER ----------------

ENCODER_A_PIN = 17
ENCODER_B_PIN = 27


# ============================================================
# DRIVE SETTINGS
# ============================================================

DEFAULT_SPEED = 40

# Encoder polling
ENCODER_POLL_INTERVAL = 0.002

# Encoder print interval
ENCODER_PRINT_INTERVAL = 0.05

# Safety timeout
DEFAULT_TIMEOUT = 15.0

# Slow down near target
SLOWDOWN_STEPS = 5

# Speed near target
SLOW_SPEED = 22


# ============================================================
# GPIO SETUP
# ============================================================

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(IN1_PIN, GPIO.OUT)
GPIO.setup(IN2_PIN, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)


# ============================================================
# MOTOR PWM
# ============================================================

motor_pwm = GPIO.PWM(PWM_PIN, 1000)
motor_pwm.start(0)


# ============================================================
# SERVO PWM
# ============================================================

servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(0)


# ============================================================
# ENCODER
# ============================================================

encoder = RotaryEncoder(
    ENCODER_A_PIN,
    ENCODER_B_PIN,
    max_steps=0
)


# ============================================================
# SERVO
# ============================================================

def steer(angle):

    # Limit angle
    angle = max(
        LEFT,
        min(RIGHT, angle)
    )

    duty = 2.5 + (angle / 180.0) * 10.0

    servo_pwm.ChangeDutyCycle(duty)

    sleep(0.05)

    # Turn PWM signal off after movement
    servo_pwm.ChangeDutyCycle(0)


# ============================================================
# NORMAL MOTOR FORWARD
# ============================================================

def forward(speed):

    speed = max(
        0,
        min(100, speed)
    )

    GPIO.output(
        IN1_PIN,
        GPIO.LOW
    )

    GPIO.output(
        IN2_PIN,
        GPIO.HIGH
    )

    motor_pwm.ChangeDutyCycle(speed)


# ============================================================
# NORMAL MOTOR BACKWARD
# ============================================================

def backward(speed):

    speed = max(
        0,
        min(100, speed)
    )

    GPIO.output(
        IN1_PIN,
        GPIO.HIGH
    )

    GPIO.output(
        IN2_PIN,
        GPIO.LOW
    )

    motor_pwm.ChangeDutyCycle(speed)


# ============================================================
# MOTOR STOP
# ============================================================

def stop():

    motor_pwm.ChangeDutyCycle(0)


# ============================================================
# ENCODER POSITION
# ============================================================

def encoder_position():

    return int(encoder.steps)


# ============================================================
# RESET ENCODER
# ============================================================

def reset_encoder():

    encoder.steps = 0

    return encoder_position()


# ============================================================
# ENCODER BASED FORWARD
# ============================================================

def driveencoder(
    motion_steps,
    speed=DEFAULT_SPEED,
    timeout=DEFAULT_TIMEOUT
):

    """
    Move FORWARD by encoder steps.

    Example:

        driveencoder(65)

    Move forward 65 encoder steps.

    Example:

        driveencoder(100, 50)

    Move forward 100 encoder steps at speed 50.
    """

    motion_steps = int(motion_steps)
    speed = float(speed)

    if motion_steps < 0:

        raise ValueError(
            "motion_steps must be 0 or greater."
        )

    if speed <= 0 or speed > 100:

        raise ValueError(
            "speed must be between 1 and 100."
        )

    if motion_steps == 0:

        stop()

        return 0


    # --------------------------------------------------------
    # RESET ENCODER
    # --------------------------------------------------------

    reset_encoder()

    starting_position = encoder_position()

    started_at = monotonic()

    last_print_time = started_at

    current_speed = speed


    print()
    print("======================================")
    print("ENCODER FORWARD START")
    print("======================================")
    print("Target steps:", motion_steps)
    print("Motor speed:", speed)
    print("Starting encoder:", starting_position)
    print("======================================")
    print()


    try:

        # ----------------------------------------------------
        # START MOTOR
        # ----------------------------------------------------

        forward(speed)


        while True:

            current_position = encoder_position()

            progress = abs(
                current_position
                - starting_position
            )

            remaining = max(
                0,
                motion_steps - progress
            )


            # ------------------------------------------------
            # PRINT ENCODER
            # ------------------------------------------------

            current_time = monotonic()

            if (
                current_time - last_print_time
                >= ENCODER_PRINT_INTERVAL
            ):

                print(
                    "Encoder:",
                    current_position,
                    "| Progress:",
                    progress,
                    "/",
                    motion_steps,
                    "| Remaining:",
                    remaining
                )

                last_print_time = current_time


            # ------------------------------------------------
            # TARGET REACHED
            # ------------------------------------------------

            if progress >= motion_steps:

                stop()

                print()
                print("======================================")
                print("FORWARD TARGET REACHED")
                print("======================================")
                print(
                    "Final encoder:",
                    current_position
                )
                print(
                    "Requested:",
                    motion_steps
                )
                print(
                    "Actual movement:",
                    progress
                )
                print("======================================")
                print()

                return progress


            # ------------------------------------------------
            # SLOWDOWN
            # ------------------------------------------------

            wanted_speed = speed

            if remaining <= SLOWDOWN_STEPS:

                wanted_speed = min(
                    speed,
                    SLOW_SPEED
                )


            if wanted_speed != current_speed:

                motor_pwm.ChangeDutyCycle(
                    wanted_speed
                )

                current_speed = wanted_speed


            # ------------------------------------------------
            # TIMEOUT
            # ------------------------------------------------

            if (
                timeout is not None
                and
                monotonic() - started_at >= timeout
            ):

                raise TimeoutError(
                    "Encoder target not reached. "
                    f"Requested: {motion_steps}, "
                    f"Measured: {progress}"
                )


            sleep(
                ENCODER_POLL_INTERVAL
            )


    finally:

        stop()


# ============================================================
# ENCODER BASED BACKWARD
# ============================================================

def driveencoder_backward(
    motion_steps,
    speed=DEFAULT_SPEED,
    timeout=DEFAULT_TIMEOUT
):

    """
    Move BACKWARD by encoder steps.

    Example:

        driveencoder_backward(65)

    Move backward 65 encoder steps.

    Example:

        driveencoder_backward(100, 50)

    Move backward 100 encoder steps at speed 50.
    """

    motion_steps = int(motion_steps)
    speed = float(speed)

    if motion_steps < 0:

        raise ValueError(
            "motion_steps must be 0 or greater."
        )

    if speed <= 0 or speed > 100:

        raise ValueError(
            "speed must be between 1 and 100."
        )

    if motion_steps == 0:

        stop()

        return 0


    # --------------------------------------------------------
    # RESET ENCODER
    # --------------------------------------------------------

    reset_encoder()

    starting_position = encoder_position()

    started_at = monotonic()

    last_print_time = started_at

    current_speed = speed


    print()
    print("======================================")
    print("ENCODER BACKWARD START")
    print("======================================")
    print("Target steps:", motion_steps)
    print("Motor speed:", speed)
    print("Starting encoder:", starting_position)
    print("======================================")
    print()


    try:

        # ----------------------------------------------------
        # START MOTOR
        # ----------------------------------------------------

        backward(speed)


        while True:

            current_position = encoder_position()

            progress = abs(
                current_position
                - starting_position
            )

            remaining = max(
                0,
                motion_steps - progress
            )


            # ------------------------------------------------
            # PRINT ENCODER
            # ------------------------------------------------

            current_time = monotonic()

            if (
                current_time - last_print_time
                >= ENCODER_PRINT_INTERVAL
            ):

                print(
                    "Encoder:",
                    current_position,
                    "| Progress:",
                    progress,
                    "/",
                    motion_steps,
                    "| Remaining:",
                    remaining
                )

                last_print_time = current_time


            # ------------------------------------------------
            # TARGET REACHED
            # ------------------------------------------------

            if progress >= motion_steps:

                stop()

                print()
                print("======================================")
                print("BACKWARD TARGET REACHED")
                print("======================================")
                print(
                    "Final encoder:",
                    current_position
                )
                print(
                    "Requested:",
                    motion_steps
                )
                print(
                    "Actual movement:",
                    progress
                )
                print("======================================")
                print()

                return progress


            # ------------------------------------------------
            # SLOWDOWN
            # ------------------------------------------------

            wanted_speed = speed

            if remaining <= SLOWDOWN_STEPS:

                wanted_speed = min(
                    speed,
                    SLOW_SPEED
                )


            if wanted_speed != current_speed:

                motor_pwm.ChangeDutyCycle(
                    wanted_speed
                )

                current_speed = wanted_speed


            # ------------------------------------------------
            # TIMEOUT
            # ------------------------------------------------

            if (
                timeout is not None
                and
                monotonic() - started_at >= timeout
            ):

                raise TimeoutError(
                    "Encoder target not reached. "
                    f"Requested: {motion_steps}, "
                    f"Measured: {progress}"
                )


            sleep(
                ENCODER_POLL_INTERVAL
            )


    finally:

        stop()


# ============================================================
# CLEANUP
# ============================================================

def cleanup():

    stop()

    steer(CENTER)

    encoder.close()

    servo_pwm.stop()

    motor_pwm.stop()

    GPIO.cleanup()

# 
# forward(100)
# sleep(10)
# stop()
