# Raspberry Pi Setup and Run Guide

## Team Sentio — WRO Future Engineers 2026

This document describes how to prepare the Raspberry Pi, install the required software, connect and verify the sensors, confirm the competition GPIO configuration, configure the GPIO18 push-button launcher, and run the Team Sentio Open and Obstacle Challenge programs.

The purpose of this guide is reproducibility: another person should be able to prepare a compatible Raspberry Pi environment and reproduce the final physically tested Team Sentio competition software setup.

---

## 1. Competition Computing Platform

The final Team Sentio V3 robot uses:

- Raspberry Pi 5, 4 GB
- Raspberry Pi OS
- Python 3
- 2 × Raspberry Pi Camera Module 3
- OpenCV
- NumPy
- Picamera2
- RPi.GPIO-compatible GPIO interface
- MPU6050 IMU
- `smbus2` for MPU6050 I2C communication
- TB6612FNG motor driver
- DS3225 steering servo
- 3S 11.1 V 2200 mAh LiPo battery

The competition source files are:

```text
src/
├── Open_Challenge.py
├── Obstacle_Challenge.py
├── drive.py
├── openVision.py
├── vision.py
├── heading.py
├── parking.py
└── button_launcher.py
```

`drive.py`, `openVision.py`, `vision.py`, `heading.py`, and `parking.py` are required helper modules. `button_launcher.py` is the optional competition push-button launcher described later in this guide.

---

## 2. Important Safety Information

Before configuring or running the robot:

1. Switch the robot off before connecting or disconnecting cameras, GPIO wiring or I2C devices.
2. Confirm battery polarity before applying power.
3. Confirm that the Raspberry Pi receives a regulated 5 V supply.
4. Never connect the 3S LiPo voltage directly to the Raspberry Pi 5 V rail.
5. The DC motor must be controlled through the TB6612FNG motor driver and must not be connected directly to Raspberry Pi GPIO.
6. All control electronics must share the required common ground.
7. Confirm that the steering linkage moves freely before powering the servo.
8. Keep the robot raised or place it safely on the competition track before launching a program that can start the motor.
9. Keep a rapid power-disconnect method available during testing.
10. LiPo batteries must be charged using the correct charger settings and under supervision.

The earlier development system experienced Raspberry Pi undervoltage with a 5 V / 3 A supply. The final architecture therefore uses a higher-current regulated 5 V supply. The exact replacement converter model is not claimed here because it was not retained as a verified measurement record.

---

## 3. Install Raspberry Pi OS

Install a current Raspberry Pi OS image using Raspberry Pi Imager.

For this repository, Raspberry Pi OS with a graphical desktop is recommended because the current competition programs use OpenCV display windows through `cv2.imshow()`.

During Raspberry Pi Imager setup, configure:

- Username
- Password
- Wi-Fi, if required
- Keyboard layout
- Locale
- Hostname, if desired

After writing the operating system image to the storage device:

1. Insert it into the Raspberry Pi.
2. Connect display, keyboard and mouse if required.
3. Boot the Raspberry Pi.
4. Complete the initial Raspberry Pi OS configuration.

To record the exact operating environment used for a final competition release, run:

```bash
cat /etc/os-release
uname -a
python3 --version
```

The output should be retained with the final release/test record where practical.

---

## 4. Update Raspberry Pi OS

Open a terminal and run:

```bash
sudo apt update
sudo apt full-upgrade -y
```

Then reboot:

```bash
sudo reboot
```

After the Raspberry Pi restarts, open a terminal again.

---

## 5. Install Required Software Packages

Team Sentio uses Raspberry Pi OS system packages for Raspberry Pi-specific Python libraries.

Install the main dependencies:

```bash
sudo apt update
sudo apt install -y \
    git \
    python3-picamera2 \
    python3-opencv \
    python3-numpy \
    python3-smbus2 \
    i2c-tools
```

The packages provide:

| Package | Purpose |
|---|---|
| `git` | Download and update the competition repository |
| `python3-picamera2` | Raspberry Pi Camera Module interface |
| `python3-opencv` | Computer vision and image processing |
| `python3-numpy` | Numerical and image-array operations |
| `python3-smbus2` | I2C communication used by `heading.py` |
| `i2c-tools` | I2C device detection and diagnostics |

### GPIO compatibility on Raspberry Pi 5

The Team Sentio source imports GPIO using:

```python
import RPi.GPIO as GPIO
```

First test whether the installed Raspberry Pi environment already provides a working compatible interface:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO import OK')"
```

For a fresh Raspberry Pi 5 installation requiring the `RPi.GPIO` compatibility interface, `rpi-lgpio` can provide the same import namespace.

Install it using:

```bash
sudo apt install -y python3-rpi-lgpio
```

If the system reports a conflict because the classic `python3-rpi.gpio` package is installed, remove the conflicting package before installing the compatibility package:

```bash
sudo apt remove -y python3-rpi.gpio
sudo apt install -y python3-rpi-lgpio
```

Do not intentionally maintain both GPIO implementations in the same Python environment because they provide the same `RPi.GPIO` namespace.

After installation, verify again:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO interface OK')"
```

---

## 6. Enable I2C

The MPU6050 IMU communicates with the Raspberry Pi through I2C.

Open Raspberry Pi configuration:

```bash
sudo raspi-config
```

Navigate to:

```text
Interface Options
→ I2C
→ Enable
```

Finish and reboot:

```bash
sudo reboot
```

---

## 7. Verify the I2C Bus

After rebooting, confirm that I2C is available:

```bash
i2cdetect -y 1
```

The MPU6050 used by `src/heading.py` is configured at:

```text
0x68
```

Therefore, a correctly powered and connected MPU6050 should normally appear as address `68` in the I2C scan.

If `68` does not appear:

- Check MPU6050 power.
- Check SDA wiring.
- Check SCL wiring.
- Check common ground.
- Confirm I2C is enabled.
- Confirm the sensor is connected to the correct Raspberry Pi I2C bus.
- Do not start the Obstacle Challenge until the IMU connection is resolved.

---

## 8. GPIO Pin Configuration

The competition programs use BCM GPIO numbering.

| Function | BCM GPIO | Raspberry Pi physical pin |
|---|---:|---:|
| Motor driver IN1 | GPIO5 | Pin 29 |
| Motor driver IN2 | GPIO6 | Pin 31 |
| Motor PWM | GPIO13 | Pin 33 |
| Steering servo PWM | GPIO22 | Pin 15 |
| Start / mode push button | GPIO18 | Pin 12 |
| I2C SDA | GPIO2 | Pin 3 |
| I2C SCL | GPIO3 | Pin 5 |

The final wiring should also be checked against the schematic in:

```text
schemes/
```

### Motor driver

The motor is controlled through the TB6612FNG.

Competition source configuration:

```text
IN1  = GPIO5
IN2  = GPIO6
PWM  = GPIO13
```

Motor PWM frequency in the competition source:

```text
1000 Hz
```

### Steering servo

The DS3225 steering servo is controlled through:

```text
GPIO22
```

Servo PWM frequency:

```text
50 Hz
```

The Open Challenge software uses the following mechanically tested steering range:

```text
LEFT   = 70
CENTER = 95
RIGHT  = 125
```

Do not increase steering travel without physically checking the Ackermann linkage. Earlier testing showed that excessive steering commands could stress or disconnect the steering structure.

The Obstacle Challenge may use challenge-specific steering calibration. Always use the values in the exact physically validated competition source rather than assuming that Open and Obstacle centre values must be identical.

---

## 9. Camera Installation

Team Sentio V3 uses two Raspberry Pi Camera Module 3 units.

Power the Raspberry Pi off before connecting or reseating CSI camera cables.

### Front camera

Recorded final geometry:

- Located near the front edge of the vehicle
- Approximately 5 mm right of the vehicle centre
- Approximately 50° downward pitch
- Used for wall, marker, pillar and obstacle perception

### Rear camera

Recorded final geometry:

- Mounted on the rear camera structure
- Approximately 45° downward pitch
- Approximately 0° yaw
- Used for rear and parking geometry

Camera mounts should remain rigid because the image-processing thresholds and target geometry were tuned around these camera positions.

---

## 10. Verify Camera Detection

After both cameras are connected, boot the Raspberry Pi and run:

```bash
rpicam-hello --list-cameras
```

Both connected cameras should be listed.

Test camera 0:

```bash
rpicam-hello --camera 0 --timeout 3000
```

If a second camera is listed, test camera 1:

```bash
rpicam-hello --camera 1 --timeout 3000
```

Confirm:

- Image is visible.
- Image orientation is correct.
- Ribbon cable connection is stable.
- Lens is unobstructed.
- Camera mount is rigid.

### Important camera-index note

The current Open Challenge source initializes:

```python
picam2 = Picamera2()
```

without an explicit camera number.

The default camera is therefore used by that source. Before a competition run, confirm that the front navigation camera is the camera selected by the program.

If the final physically validated Obstacle/Parking program explicitly selects front and rear cameras, preserve that exact camera mapping in the submitted source and reproduction documentation.

Do not change camera numbering immediately before a validated competition run without retesting the complete program.

---

## 11. Clone the Team Sentio Repository

From the Raspberry Pi terminal:

```bash
cd ~
git clone https://github.com/teamsentiorobotics-svg/World-Robot-Olympiad---Team-Sentio-.git
cd World-Robot-Olympiad---Team-Sentio-
```

Confirm the repository contents:

```bash
ls
```

The root should contain files/folders including:

```text
README.md
requirements.md
src/
models/
schemes/
docs/
other/
t-photos/
v-photos/
video/
```

Check the competition source directory:

```bash
ls src
```

It should contain:

```text
Open_Challenge.py
Obstacle_Challenge.py
drive.py
openVision.py
vision.py
heading.py
parking.py
button_launcher.py
```

---

## 12. Record the Exact Git Revision

For reproducibility, identify the exact source revision being tested:

```bash
git rev-parse HEAD
```

Check for local modifications:

```bash
git status
```

For a final competition release, the exact commit or release tag used during physical validation should be recorded.

A physically tested file should not then be modified and presented as though the modified version were the tested executable.

---

## 13. Verify Python Imports

From the repository root, run:

```bash
python3 - <<'PY'
import cv2
import numpy
import smbus2
import RPi.GPIO as GPIO
from picamera2 import Picamera2

print("OpenCV:", cv2.__version__)
print("NumPy:", numpy.__version__)
print("Picamera2 import: OK")
print("RPi.GPIO-compatible interface: OK")
print("smbus2 import: OK")
print("Core Team Sentio imports: PASS")
PY
```

If this completes without an exception, the main external Python imports are available.

---

## 14. Test the MPU6050 Heading Module

The Team Sentio Obstacle Challenge imports:

```python
from heading import MPU6050Heading
```

The helper is located at:

```text
src/heading.py
```

Test it directly:

```bash
python3 src/heading.py
```

During startup, keep the robot and MPU6050 completely still while gyro calibration is performed.

After calibration, slowly rotate the robot.

The terminal should display changing heading values.

Stop the test with:

```text
Ctrl+C
```

If the program reports an I2C error:

1. Stop the program.
2. Run:

```bash
i2cdetect -y 1
```

3. Confirm that the MPU6050 appears at `0x68`.
4. Recheck SDA, SCL, power and common ground.

Do not proceed to IMU-assisted parking until the heading test operates correctly.

---

## 15. Verify Camera Imports from Python

Run:

```bash
python3 - <<'PY'
from picamera2 import Picamera2

cams = Picamera2.global_camera_info()

print("Detected Picamera2 cameras:", len(cams))

for index, camera in enumerate(cams):
    print(index, camera)
PY
```

Confirm that the required cameras are detected.

---

## 16. Pre-Run Mechanical Check

Before applying motor power:

- Lift the robot so the wheels can rotate safely.
- Confirm drivetrain rotates freely.
- Confirm the differential is not binding.
- Confirm steering linkage is connected.
- Confirm servo horn and linkage are secure.
- Confirm camera towers have not moved.
- Confirm no cable can enter the drivetrain.
- Confirm wheels rotate without rubbing the chassis.
- Confirm the power switch/emergency disconnect is accessible.

---

## 17. Pre-Run Electrical Check

Before every integrated run:

- Confirm battery polarity.
- Confirm battery connector is secure.
- Confirm Raspberry Pi regulated supply is connected correctly.
- Confirm common ground.
- Confirm TB6612FNG connections.
- Confirm servo connection.
- Confirm both camera cables.
- Confirm MPU6050 connection.
- Check for loose wires.
- Check for damaged insulation.
- Check that no component is unusually hot.
- Confirm there is no Raspberry Pi undervoltage warning.

If there is smoke, battery swelling, unexpected heating, repeated rebooting, drivetrain binding or uncertain polarity:

**Disconnect power and diagnose the fault before continuing.**

---

## 18. Camera Startup Behaviour

The Open Challenge program enables automatic exposure and automatic white balance during startup.

The program allows the camera to settle for approximately two seconds.

It then records:

```text
ExposureTime
AnalogueGain
```

and disables automatic exposure/white balance.

This creates more stable image conditions for the fixed LAB colour thresholds used by the competition software.

For repeatable runs:

- Place the robot in the intended starting environment before launching the program.
- Avoid covering the camera during startup.
- Avoid pointing a bright light directly into the camera during exposure setup.
- Allow the startup calibration to complete before interfering with the robot.

---

## 19. Run the Open Challenge

### IMPORTANT — MOTOR START WARNING

The current Open Challenge program is not a passive camera test.

After camera initialization, the program:

1. Centres the steering.
2. Waits approximately 1.9 seconds.
3. Commands:

```python
forward(100)
```

The robot can therefore begin moving automatically shortly after the program is launched.

Before running the program:

- Place the robot safely in the starting area, or
- Raise the drive wheels for a controlled test.
- Keep the emergency power disconnect accessible.
- Keep hands, cables and tools away from the drivetrain.

Run from the repository root:

```bash
python3 src/Open_Challenge.py
```

The program initializes the camera, locks exposure/gain, centres the steering and enters the autonomous control loop.

The current Open program uses:

```text
Frame:           1280 × 680
Format:          RGB888
KP:              0.012
LINE_COOLDOWN:   1.3 s
LEFT:            70
CENTER:          95
RIGHT:           125
Laps:            3
Count target:    12 gate events
```

The first valid marker establishes direction:

```text
Blue first   → anticlockwise
Orange first → clockwise
```

The first marker establishes direction and is not treated as a normal counted crossing.

The software stops the motor after the required count is reached.

### Manual stop

When the OpenCV display window is active, press:

```text
q
```

The program centres the steering, stops the motor and exits the main loop.

If normal software shutdown is not possible, use the physical power disconnect.

---

## 20. Run the Obstacle Challenge

Before running the Obstacle Challenge, verify all of the following:

- `src/Obstacle_Challenge.py` is present.
- `src/heading.py` is present.
- MPU6050 is detected at `0x68`.
- `python3 src/heading.py` completes calibration successfully.
- Red and green pillar detection has been checked.
- Magenta/purple parking detection has been checked.
- Steering range has been physically checked.
- Motor direction has been verified.
- The exact source being launched is the physically validated competition version.

Run:

```bash
python3 src/Obstacle_Challenge.py
```

### Release-integrity requirement

The final Obstacle/Parking executable has completed physical robot validation and is working. The GitHub version should remain synchronized with the exact tested source.

Any later development or calibration change must be physically retested before being presented as the validated competition release.

If parking speed values, camera selection, steering calls, IMU logic or other actuation behaviour are modified, the resulting file should be treated as a new revision and physically retested before being declared validated.

---


## 21. Configure GPIO18 Push-Button Challenge Launcher

Team Sentio uses a physical push button on **BCM GPIO18 (physical pin 12)** so that powering the robot does **not** immediately start a challenge program.

The launcher starts automatically after the Raspberry Pi graphical desktop loads, but the robot remains waiting until the button is deliberately pressed.

### Button behaviour

```text
Short press (< 1.5 s)  → Open Challenge
Long press (≥ 1.5 s)   → Obstacle Challenge
```

The challenge starts only **after the button is released**.

This provides one physical competition button for both programs while preventing the earlier behaviour where an autonomous program could begin immediately after power-up.

### Wiring

Connect a normally-open momentary push button as follows:

| Button connection | Raspberry Pi |
|---|---|
| Side 1 | GPIO18 — BCM18 — physical pin 12 |
| Side 2 | GND — for example physical pin 14 |

The launcher uses the Raspberry Pi's internal pull-up resistor, so no external pull-up resistor is required.

```text
GPIO18 (Pin 12)
      |
   [ BUTTON ]
      |
GND (Pin 14)
```

Normal state:

```text
GPIO18 = HIGH
```

Button pressed:

```text
GPIO18 = LOW
```

### Create the launcher

Create:

```text
src/button_launcher.py
```

with the following content:

```python
#!/usr/bin/env python3

import time
import subprocess
import sys
from pathlib import Path

import RPi.GPIO as GPIO

BUTTON_PIN = 18
LONG_PRESS_SECONDS = 1.5

SRC_DIR = Path(__file__).resolve().parent
OPEN_PROGRAM = SRC_DIR / "Open_Challenge.py"
OBSTACLE_PROGRAM = SRC_DIR / "Obstacle_Challenge.py"

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Team Sentio button launcher ready")
print("Short press: Open Challenge")
print("Long press: Obstacle Challenge")

try:
    while True:
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING, bouncetime=200)

        press_start = time.monotonic()

        while GPIO.input(BUTTON_PIN) == GPIO.LOW:
            time.sleep(0.02)

        press_duration = time.monotonic() - press_start

        if press_duration >= LONG_PRESS_SECONDS:
            program = OBSTACLE_PROGRAM
            print(f"Long press ({press_duration:.2f}s): starting Obstacle Challenge")
        else:
            program = OPEN_PROGRAM
            print(f"Short press ({press_duration:.2f}s): starting Open Challenge")

        subprocess.run(
            [sys.executable, str(program)],
            cwd=str(SRC_DIR),
            check=False
        )

        print("Challenge program ended")
        print("Waiting for next button press...")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Button launcher stopped")

finally:
    GPIO.cleanup(BUTTON_PIN)
```

Make it executable:

```bash
chmod +x src/button_launcher.py
```

### Test the button before enabling autostart

From the repository root:

```bash
python3 src/button_launcher.py
```

The terminal should show:

```text
Team Sentio button launcher ready
Short press: Open Challenge
Long press: Obstacle Challenge
```

Test with the drive wheels raised or with the robot safely positioned on the track.

1. Briefly press and release the button.
2. Confirm that `Open_Challenge.py` starts.
3. Stop the Open program normally.
4. Restart the launcher if required.
5. Hold the button for at least 1.5 seconds and release it.
6. Confirm that `Obstacle_Challenge.py` starts.

Do not enable automatic startup until both button actions have been verified.

### Automatically start the button listener after boot

Because the current competition programs use `cv2.imshow()`, the recommended launcher startup method is **graphical desktop autostart**, not a headless boot service.

Configure Raspberry Pi OS to boot into the graphical desktop with automatic login if the competition setup requires one-switch operation.

Create the desktop autostart directory:

```bash
mkdir -p ~/.config/autostart
```

From the repository root, determine the absolute repository path:

```bash
pwd
```

For example:

```text
/home/aarav_sentio/World-Robot-Olympiad---Team-Sentio-
```

Create:

```bash
nano ~/.config/autostart/sentio-button.desktop
```

Paste:

```ini
[Desktop Entry]
Type=Application
Name=Team Sentio Button Launcher
Comment=GPIO18 launcher for Open and Obstacle Challenge
Exec=python3 /home/aarav_sentio/World-Robot-Olympiad---Team-Sentio-/src/button_launcher.py
Terminal=true
X-GNOME-Autostart-enabled=true
```

If the Raspberry Pi username or repository path is different, replace the path in `Exec=` with the actual path returned by `pwd`.

Save with:

```text
Ctrl+O
Enter
Ctrl+X
```

Reboot:

```bash
sudo reboot
```

After the graphical desktop loads, the button launcher should start and remain waiting.

**The robot must not move merely because power was switched on.**

Movement begins only after:

```text
Short press → Open Challenge
Long press  → Obstacle Challenge
```

### Verify autostart

After reboot:

1. Do not touch the button.
2. Confirm that the robot remains stationary.
3. Confirm that the launcher terminal is waiting for input.
4. Short-press GPIO18 and confirm Open Challenge starts.
5. Reboot or return to the launcher.
6. Long-press GPIO18 and confirm Obstacle Challenge starts.

### Disable the launcher

To disable automatic button launching without deleting the source file:

```bash
rm ~/.config/autostart/sentio-button.desktop
```

Then reboot:

```bash
sudo reboot
```

### Important competition safety rule

The push button is a **start command**, not an emergency stop.

Always keep the main electrical power switch / rapid disconnect accessible.

Before pressing the button:

- place the robot in the correct starting position,
- confirm the track is clear,
- confirm no hands or tools are near the wheels,
- confirm steering is mechanically free,
- allow the Raspberry Pi and launcher to finish booting,
- use a deliberate short or long press for the required challenge.

---

## 22. Competition Testing Sequence


Team Sentio uses staged testing rather than immediately running an unverified full-speed program.

Recommended sequence:

```text
1. Component test
        ↓
2. Sensor / actuator subsystem test
        ↓
3. Low-speed integrated test
        ↓
4. Full challenge run
        ↓
5. Observe and classify failure
        ↓
6. Modify one relevant variable
        ↓
7. Retest
```

This reduces the risk of confusing software, electrical and mechanical failures.

---

## 23. Minimum Subsystem Verification

Before a full competition run, confirm:

### Raspberry Pi

```bash
python3 --version
```

### Cameras

```bash
rpicam-hello --list-cameras
```

### I2C / MPU6050

```bash
i2cdetect -y 1
```

### Heading helper

```bash
python3 src/heading.py
```

### Python dependencies

```bash
python3 - <<'PY'
import cv2
import numpy
import smbus2
import RPi.GPIO as GPIO
from picamera2 import Picamera2
print("Dependency check: PASS")
PY
```

### GPIO18 start button

```bash
python3 src/button_launcher.py
```

Confirm:

```text
Short press → Open Challenge
Long press  → Obstacle Challenge
```

Stop the launcher with `Ctrl+C` after the manual test.

### Git revision

```bash
git rev-parse HEAD
git status
```

Only proceed to an autonomous full run when the required checks pass.

---

## 24. Troubleshooting

### `ModuleNotFoundError: No module named 'cv2'`

Install:

```bash
sudo apt install -y python3-opencv
```

---

### `ModuleNotFoundError: No module named 'numpy'`

Install:

```bash
sudo apt install -y python3-numpy
```

---

### `ModuleNotFoundError: No module named 'picamera2'`

Install:

```bash
sudo apt install -y python3-picamera2
```

---

### `ModuleNotFoundError: No module named 'smbus2'`

Install:

```bash
sudo apt install -y python3-smbus2
```

---

### `ModuleNotFoundError: No module named 'heading'`

Confirm:

```bash
ls src
```

and verify that:

```text
src/heading.py
```

exists.

Launch the Obstacle program using:

```bash
python3 src/Obstacle_Challenge.py
```

---

### `ModuleNotFoundError` or GPIO compatibility error for `RPi.GPIO`

Check:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO import OK')"
```

On a Raspberry Pi 5 environment requiring the compatibility implementation:

```bash
sudo apt install -y python3-rpi-lgpio
```

Do not deliberately install conflicting `rpi-gpio` and `rpi-lgpio` implementations into the same Python environment.

---

### Camera not detected

Run:

```bash
rpicam-hello --list-cameras
```

If the expected camera is absent:

1. Power off the Raspberry Pi.
2. Check the CSI ribbon cable.
3. Check cable orientation.
4. Reseat the camera connector.
5. Reboot.
6. Repeat the camera-list command.

---

### MPU6050 not detected

Run:

```bash
i2cdetect -y 1
```

Check:

- GPIO2 / SDA
- GPIO3 / SCL
- Power
- Ground
- I2C enabled in `raspi-config`

The current `heading.py` expects the MPU6050 at:

```text
0x68
```

---

### Raspberry Pi undervoltage warning

Do not continue full-speed testing with repeated undervoltage warnings.

Check:

- Regulated 5 V supply
- Supply current capability
- Wiring resistance
- Connector condition
- Ground connection
- Battery state

The earlier Team Sentio 5 V / 3 A arrangement produced repeated undervoltage warnings and was replaced by a higher-current supply architecture.

---

### OpenCV window does not appear

The current competition source uses:

```python
cv2.imshow()
```

Run the program from a Raspberry Pi graphical desktop session with a working display environment.

---

### Robot drives immediately after program launch

This is expected behaviour in the current Open Challenge source.

The program eventually calls:

```python
forward(100)
```

after camera initialization and steering centring.

Always position the robot safely before launching the Open Challenge.

---


### GPIO18 button does not respond

Confirm the button wiring:

```text
GPIO18 / physical pin 12 → button → GND
```

Check the raw GPIO state:

```bash
python3 - <<'PY'
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("GPIO18 test. Press Ctrl+C to stop.")

try:
    while True:
        print(GPIO.input(18))
        time.sleep(0.2)
finally:
    GPIO.cleanup()
PY
```

Expected behaviour:

```text
Not pressed → 1
Pressed     → 0
```

If the launcher works manually but not after reboot:

1. Confirm the graphical desktop has loaded.
2. Confirm the repository path in `~/.config/autostart/sentio-button.desktop`.
3. Run the exact `Exec=` command manually in a terminal.
4. Confirm the desktop user has GPIO access.
5. Confirm `src/button_launcher.py` exists.
6. Confirm the competition source filenames exactly match the launcher.

---

## 25. Do Not Tune Multiple Variables at Once

When calibration changes are required, change one meaningful variable at a time.

Examples include:

- Camera pose
- Steering centre
- Steering limit
- KP
- Marker cooldown
- Colour threshold
- Motor speed

After a change:

```text
Change
→ Test
→ Observe
→ Record
→ Retain or reject
```

This keeps the effect of each engineering change traceable.

---

## 26. Final Competition Release Check

Before identifying a GitHub revision as the final competition release, confirm:

- [x] Correct Raspberry Pi boots without undervoltage warnings.
- [x] Required Python imports pass.
- [x] Front camera detected.
- [x] Rear camera detected where required.
- [x] Camera geometry matches the documented mounts.
- [x] I2C enabled.
- [x] MPU6050 visible at `0x68`.
- [x] `heading.py` calibration test passes.
- [x] Motor direction correct.
- [x] Steering linkage secure.
- [x] Open steering limits physically safe.
- [x] GPIO18 push button is wired and verified.
- [x] Short press launches Open Challenge.
- [x] Long press launches Obstacle Challenge.
- [x] Open Challenge program completes a physical run.
- [x] Obstacle Challenge program completes physical validation.
- [x] Parking behaviour is physically validated.
- [x] `Open_Challenge.py` is present.
- [x] `Obstacle_Challenge.py` is present.
- [x] `drive.py` is present.
- [x] `openVision.py` is present.
- [x] `vision.py` is present.
- [x] `heading.py` is present.
- [x] `parking.py` is present.
- [x] Repository dependencies are documented.
- [x] Final working project package has been pushed to GitHub.

Record the final source identity with:

```bash
git rev-parse HEAD
```

A final GitHub tag or release can then be associated with that physically validated commit.

---

## 27. Reproduction Summary

A clean Team Sentio Raspberry Pi setup follows this sequence:

```text
Install Raspberry Pi OS
        ↓
Update system
        ↓
Install Picamera2 / OpenCV / NumPy / SMBus2 / GPIO support
        ↓
Enable I2C
        ↓
Connect and verify cameras
        ↓
Verify MPU6050
        ↓
Clone repository
        ↓
Record exact Git commit
        ↓
Verify Python imports
        ↓
Test heading.py
        ↓
Check mechanical and electrical systems
        ↓
Wire and verify GPIO18 push button
        ↓
Configure button launcher autostart
        ↓
Run staged subsystem tests
        ↓
Short press → run Open Challenge
        ↓
Long press → run Obstacle Challenge
        ↓
Confirm parking
        ↓
Record final tested release
```

---

## 28. Related Repository Files

For the complete robot reconstruction, also refer to:

```text
README.md
requirements.md
src/Open_Challenge.py
src/Obstacle_Challenge.py
src/drive.py
src/openVision.py
src/vision.py
src/heading.py
src/parking.py
src/button_launcher.py
schemes/
models/
v-photos/
other/
video/
```

The Raspberry Pi software environment is only one part of reproduction. The submitted CAD, wiring, physical photographs, calibration record and exact physically tested competition source should be used together.

At the final project stage, the Open Challenge, Obstacle Challenge and Parking behaviours were physically tested and working. The complete working project package was pushed to GitHub.

---

**Team Sentio**  
**WRO Future Engineers 2026**  
**Robofun Lab (RFL), India**
