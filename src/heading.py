import smbus2
import time

# ============================================================
# MPU6050 SETTINGS
# ============================================================

MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B

# X-axis Gyroscope register
GYRO_XOUT_H = 0x43

# ============================================================
# MPU6050 HEADING CLASS
# ============================================================

class MPU6050Heading:

    def __init__(self):

        # I2C bus
        self.bus = smbus2.SMBus(1)

        # Wake up MPU6050
        self.bus.write_byte_data(
            MPU6050_ADDR,
            PWR_MGMT_1,
            0
        )

        time.sleep(1)

        # ----------------------------------------------------
        # Calibration
        # ----------------------------------------------------

        print()
        print("========================================")
        print("MPU6050 CALIBRATION")
        print("========================================")
        print("Keep MPU6050 completely still")
        print()

        time.sleep(2)

        samples = 1500

        self.gyro_x_offset = 0.0

        for i in range(samples):

            self.gyro_x_offset += self.read_gyro_x()

            time.sleep(0.002)

        self.gyro_x_offset /= samples

        print("Calibration complete")
        print("X Gyro Offset:", self.gyro_x_offset)
        print()

        # ----------------------------------------------------
        # Heading
        # ----------------------------------------------------

        self.heading = 0.0

        self.previous_time = time.monotonic()


    # ========================================================
    # READ 16-BIT VALUE
    # ========================================================

    def read_word(self, register):

        high = self.bus.read_byte_data(
            MPU6050_ADDR,
            register
        )

        low = self.bus.read_byte_data(
            MPU6050_ADDR,
            register + 1
        )

        value = (high << 8) | low

        if value >= 32768:
            value -= 65536

        return value


    # ========================================================
    # READ X-AXIS GYROSCOPE
    # ========================================================

    def read_gyro_x(self):

        gx = self.read_word(
            GYRO_XOUT_H
        )

        # MPU6050 ±250°/s
        gx = gx / 131.0

        return gx


    # ========================================================
    # GET HEADING
    # ========================================================

    def get_heading(self):

        # Read X-axis gyro
        gx = self.read_gyro_x()

        # Remove gyro offset
        gx -= self.gyro_x_offset

        # Current time
        current_time = time.monotonic()

        # Time difference
        dt = current_time - self.previous_time

        self.previous_time = current_time

        # Integrate angular velocity
        self.heading += gx * dt

        # Keep heading between 0° and 360°
        self.heading %= 360

        return self.heading


    # ========================================================
    # RESET HEADING TO ZERO
    # ========================================================

    def reset_heading(self):

        self.heading = 0.0

        self.previous_time = time.monotonic()


    # ========================================================
    # CLOSE MPU6050
    # ========================================================

    def close(self):

        self.bus.close()


# ============================================================
# TEST
# ============================================================
# This section runs ONLY when heading.py itself is executed.
#
# If heading.py is imported into obstacle.py,
# this section will NOT run.
# ============================================================

if __name__ == "__main__":

    imu = MPU6050Heading()

    print("Heading started")
    print("Rotate the robot to test heading")
    print("Press CTRL+C to stop")
    print()

    try:

        last_print_time = time.monotonic()

        while True:

            heading = imu.get_heading()

            current_time = time.monotonic()

            # Print every 100 ms
            if current_time - last_print_time >= 0.1:

                last_print_time = current_time

                print(
                    f"Heading: {heading:.5f}°"
                )

    except KeyboardInterrupt:

        print()
        print("Heading stopped")

    finally:

        imu.close()
