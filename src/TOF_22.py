import time
import board
import busio
import digitalio
import adafruit_vl6180x

# ============================================================
# SETTINGS
# ============================================================

TOF1_XSHUT_PIN = board.D16
TOF2_XSHUT_PIN = board.D20
TOF3_XSHUT_PIN = board.D21

TOF1_ADDRESS = 0x30
TOF2_ADDRESS = 0x31
TOF3_ADDRESS = 0x32

DEFAULT_ADDRESS = 0x29


# ============================================================
# I2C
# ============================================================

i2c = busio.I2C(board.SCL, board.SDA)


# ============================================================
# XSHUT PINS
# ============================================================

xshut1 = digitalio.DigitalInOut(TOF1_XSHUT_PIN)
xshut1.switch_to_output(value=False)

xshut2 = digitalio.DigitalInOut(TOF2_XSHUT_PIN)
xshut2.switch_to_output(value=False)

xshut3 = digitalio.DigitalInOut(TOF3_XSHUT_PIN)
xshut3.switch_to_output(value=False)


# All sensors OFF
time.sleep(0.5)


# ============================================================
# FUNCTION TO CHANGE VL6180X I2C ADDRESS
# ============================================================

def change_address(old_address, new_address):

    # VL6180X I2C slave address register = 0x0212
    register = bytes([0x02, 0x12])

    # New address must be 7-bit
    data = register + bytes([new_address & 0x7F])

    while not i2c.try_lock():
        pass

    try:
        i2c.writeto(old_address, data)
    finally:
        i2c.unlock()

    time.sleep(0.05)


# ============================================================
# START TOF 1
# ============================================================

print("Starting TOF 1...")

xshut1.value = True
time.sleep(0.5)

# Detect sensor at default address 0x29
tof1_temp = adafruit_vl6180x.VL6180X(
    i2c,
    address=DEFAULT_ADDRESS
)

print("TOF 1 detected at 0x29")

# Change TOF 1 address
change_address(
    DEFAULT_ADDRESS,
    TOF1_ADDRESS
)

print("TOF 1 address changed to 0x30")

# Reconnect using new address
tof1 = adafruit_vl6180x.VL6180X(
    i2c,
    address=TOF1_ADDRESS
)

print("TOF 1 ready")


# ============================================================
# START TOF 2
# ============================================================

print("\nStarting TOF 2...")

xshut2.value = True
time.sleep(0.5)

# Detect second sensor at default address 0x29
tof2_temp = adafruit_vl6180x.VL6180X(
    i2c,
    address=DEFAULT_ADDRESS
)

print("TOF 2 detected at 0x29")

# Change TOF 2 address
change_address(
    DEFAULT_ADDRESS,
    TOF2_ADDRESS
)

print("TOF 2 address changed to 0x31")

# Reconnect using new address
tof2 = adafruit_vl6180x.VL6180X(
    i2c,
    address=TOF2_ADDRESS
)

print("TOF 2 ready")


# ============================================================
# START TOF 3
# ============================================================

print("\nStarting TOF 3...")

xshut3.value = True
time.sleep(0.5)

# Detect third sensor at default address 0x29
tof3_temp = adafruit_vl6180x.VL6180X(
    i2c,
    address=DEFAULT_ADDRESS
)

print("TOF 3 detected at 0x29")

# Change TOF 3 address
change_address(
    DEFAULT_ADDRESS,
    TOF3_ADDRESS
)

print("TOF 3 address changed to 0x32")

# Reconnect using new address
tof3 = adafruit_vl6180x.VL6180X(
    i2c,
    address=TOF3_ADDRESS
)

print("TOF 3 ready")


# ============================================================
# TEST MODE
# ============================================================

if __name__ == "__main__":

    print("\n============================================")
    print("       THREE TOF SENSOR TEST")
    print("============================================")
    print("TOF 1 = GPIO 16 | Address 0x30 | RIGHT")
    print("TOF 2 = GPIO 20 | Address 0x31 | RIGHT")
    print("TOF 3 = GPIO 21 | Address 0x32 | LEFT")
    print("Press Ctrl+C to stop.")
    print("============================================\n")

    try:

        while True:

            # --------------------------------------------
            # READ TOF 1
            # --------------------------------------------

            distance1 = tof1.range
            status1 = tof1.range_status

            # --------------------------------------------
            # READ TOF 2
            # --------------------------------------------

            distance2 = tof2.range
            status2 = tof2.range_status

            # --------------------------------------------
            # READ TOF 3
            # --------------------------------------------

            distance3 = tof3.range
            status3 = tof3.range_status

            # --------------------------------------------
            # PRINT VALUES
            # --------------------------------------------

            print(
                f"TOF 1 (RIGHT): {distance1:3} mm | "
                f"Status: {status1}    "
                f"TOF 2 (RIGHT): {distance2:3} mm | "
                f"Status: {status2}    "
                f"TOF 3 (LEFT): {distance3:3} mm | "
                f"Status: {status3}"
            )

            time.sleep(0.05)

    except KeyboardInterrupt:

        print("\nStopping ToF sensors...")

    finally:

        xshut1.value = False
        xshut2.value = False
        xshut3.value = False

        xshut1.deinit()
        xshut2.deinit()
        xshut3.deinit()

        print("Done.")