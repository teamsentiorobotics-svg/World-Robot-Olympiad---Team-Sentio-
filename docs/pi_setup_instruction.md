# Raspberry Pi Setup and Run Guide

## Team Sentio — WRO Future Engineers 2026

This document describes how to prepare the Raspberry Pi, install the required software, connect and verify the sensors, confirm the competition GPIO configuration, and run the Team Sentio Open and Obstacle Challenge programs.

The purpose of this guide is reproducibility: another person should be able to prepare a compatible Raspberry Pi environment and understand the steps required before running the robot.

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
└── heading.py
```

`heading.py` provides the `MPU6050Heading` class used by the Obstacle Challenge program.

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
requirements.txt
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
heading.py
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

Only the exact Obstacle/Parking executable that has completed physical robot validation should be labelled as the final competition executable.

A development or calibration snapshot must not be presented as a physically validated release.

If parking speed values, camera selection, steering calls, IMU logic or other actuation behaviour are modified, the resulting file should be treated as a new revision and physically retested before being declared validated.

---

## 21. Competition Testing Sequence

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

## 22. Minimum Subsystem Verification

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

### Git revision

```bash
git rev-parse HEAD
git status
```

Only proceed to an autonomous full run when the required checks pass.

---

## 23. Troubleshooting

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

## 24. Do Not Tune Multiple Variables at Once

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

## 25. Final Competition Release Check

Before identifying a GitHub revision as the final competition release, confirm:

- [ ] Correct Raspberry Pi boots without undervoltage warnings.
- [ ] Required Python imports pass.
- [ ] Front camera detected.
- [ ] Rear camera detected where required.
- [ ] Camera geometry matches the documented mounts.
- [ ] I2C enabled.
- [ ] MPU6050 visible at `0x68`.
- [ ] `heading.py` calibration test passes.
- [ ] Motor direction correct.
- [ ] Steering linkage secure.
- [ ] Open steering limits physically safe.
- [ ] Open Challenge program completes a physical run.
- [ ] Obstacle Challenge program completes the required physical validation.
- [ ] Parking behaviour is validated using the exact submitted source.
- [ ] `Open_Challenge.py` is the tested file.
- [ ] `Obstacle_Challenge.py` is the tested file.
- [ ] `heading.py` is the tested dependency.
- [ ] No required source file is missing.
- [ ] Repository dependencies are documented.
- [ ] Git working tree contains no accidental local edits.
- [ ] Exact validation commit SHA is recorded.

Record the final source identity with:

```bash
git rev-parse HEAD
```

A final GitHub tag or release can then be associated with that physically validated commit.

---

## 26. Reproduction Summary

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
Run staged subsystem tests
        ↓
Run Open Challenge
        ↓
Run physically validated Obstacle Challenge
        ↓
Record final tested release
```

---

## 27. Related Repository Files

For the complete robot reconstruction, also refer to:

```text
README.md
requirements.txt
src/Open_Challenge.py
src/Obstacle_Challenge.py
src/heading.py
schemes/
models/
v-photos/
other/
video/
```

The Raspberry Pi software environment is only one part of reproduction. The submitted CAD, wiring, physical photographs, calibration record and exact physically tested competition source should be used together.

---

**Team Sentio**  
**WRO Future Engineers 2026**  
**Robofun Lab (RFL), India**
