import dencoder
from time import sleep

try:
    print("Testing encoder drive...")

    dencoder.driveencoder(100, 40)

    print("Test complete.")

    sleep(1)

except KeyboardInterrupt:
    print("Stopped by user.")

except Exception as e:
    print("ERROR:", e)

finally:
    dencoder.cleanup()
