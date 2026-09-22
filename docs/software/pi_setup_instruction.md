# Raspberry Pi Setup and Run Guide

## Team Sentio — WRO Future Engineers 2026

This document describes how to prepare a Raspberry Pi 5, install the required software, configure the cameras and MPU6050, verify the motor and steering system, clone the Team Sentio repository, and run the competition software used by **Starlight**.

**Team:** Deyaan Agrawal, Darsh Zaveri, Aarav Jalan  
**Robot:** Starlight  
**Competition:** World Robot Olympiad 2026 — Future Engineers  
**Institution / Training Environment:** Robofun Lab (RFL), India

The purpose of this guide is **reproducibility**.

A technically competent user should be able to start with a compatible Raspberry Pi 5, reproduce the software environment, connect the documented hardware, verify the required subsystems and understand how the final competition software is launched.

The Open Challenge, Obstacle Challenge and Parking behaviours have been physically tested on Starlight and are working.

> [!IMPORTANT]
> The exact source running on the physically tested robot remains the authoritative competition version.
>
> Before the repository is permanently frozen, the Raspberry Pi source, GitHub source and documentation should be confirmed to be identical.

---

# 1. Competition Computing Platform

The final Starlight computing and sensing system uses:

- Raspberry Pi 5, 4 GB
- Raspberry Pi OS
- Python 3
- 2 × Raspberry Pi Camera Module 3
- OpenCV
- NumPy
- Picamera2
- RPi.GPIO-compatible GPIO interface
- MPU6050 IMU
- SMBus2
- TB6612FNG motor driver
- DS3225 steering servo
- JGB37-520 DC geared motor
- 3S 11.1 V LiPo battery
- regulated Raspberry Pi electronics supply

The current GitHub competition source directory is:

```text
src/
├── open_challenge_final_ready_to_go.py
├── Obstacle_Challenge.py
├── drive.py
├── openVision.py
├── vision.py
├── heading.py
└── parking.py
```

The supporting files have the following roles:

| File | Purpose |
|---|---|
| `open_challenge_final_ready_to_go.py` | Final Open Challenge controller |
| `Obstacle_Challenge.py` | Final Obstacle Challenge controller |
| `drive.py` | Motor and steering-servo control |
| `openVision.py` | Open Challenge BLACK / BLUE / ORANGE vision |
| `vision.py` | Obstacle Challenge multi-colour vision |
| `heading.py` | MPU6050 heading calculation |
| `parking.py` | Parking behaviour |

---

# 2. Important Safety Information

Before configuring or running Starlight:

1. Switch the robot off before connecting or disconnecting cameras, GPIO wiring or I2C devices.
2. Confirm battery polarity before applying power.
3. Never connect the 3S LiPo voltage directly to the Raspberry Pi 5 V rail.
4. Use a properly regulated power supply for the Raspberry Pi.
5. The DC motor must be controlled through the motor driver and must never be connected directly to Raspberry Pi GPIO.
6. Ensure all required electronics share the correct common ground.
7. Check the steering linkage mechanically before powering the servo.
8. Raise the drive wheels or place the robot safely on the track before running motor tests.
9. Keep hands, tools and loose wires away from the wheels and gears.
10. Keep a rapid power-disconnect method available during testing.
11. Charge the LiPo only with an appropriate balance charger and under supervision.
12. Do not change wiring while the battery is connected.
13. Do not increase steering travel without mechanically checking the Ackermann linkage.
14. Stop testing immediately if the Raspberry Pi reports repeated undervoltage warnings.

Earlier development failures led Team Sentio to place greater emphasis on:

- polarity checking,
- LiPo supervision,
- controlled power-up,
- common-ground verification,
- connector inspection,
- rapid power isolation.

These checks should be treated as part of the normal setup process.

---

# 3. Install Raspberry Pi OS

Use **Raspberry Pi Imager** to install a current Raspberry Pi OS image.

A Raspberry Pi OS installation with the **graphical desktop** is recommended because the current competition programs use OpenCV display windows through:

```python
cv2.imshow()
```

During Raspberry Pi Imager setup, configure as required:

- username,
- password,
- hostname,
- keyboard layout,
- locale,
- Wi-Fi.

After writing the image:

1. Insert the storage device into the Raspberry Pi.
2. Connect the required display, keyboard and mouse during setup.
3. Boot the Raspberry Pi.
4. Complete the Raspberry Pi OS first-run configuration.

---

# 4. Record the Operating Environment

For reproducibility, record the main operating-system and Python information:

```bash
cat /etc/os-release
```

Then:

```bash
uname -a
```

And:

```bash
python3 --version
```

These values can be retained with the final competition validation record.

Exact package versions should not be invented retrospectively if they were not recorded from the physically tested environment.

---

# 5. Update Raspberry Pi OS

Open a terminal and run:

```bash
sudo apt update
sudo apt full-upgrade -y
```

Then reboot:

```bash
sudo reboot
```

After rebooting, open a terminal again.

---

# 6. Install Required Software

Install the primary Team Sentio dependencies:

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

These packages provide:

| Package | Purpose |
|---|---|
| `git` | Clone and update the repository |
| `python3-picamera2` | Raspberry Pi camera interface |
| `python3-opencv` | Computer vision |
| `python3-numpy` | Numerical and image-array processing |
| `python3-smbus2` | MPU6050 I2C communication |
| `i2c-tools` | I2C diagnostics |

Verify Python:

```bash
python3 --version
```

---

# 7. Configure GPIO Support on Raspberry Pi 5

The Team Sentio drive software imports:

```python
import RPi.GPIO as GPIO
```

First test whether the installed system already provides a compatible GPIO interface:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO import OK')"
```

If this succeeds, continue.

If a fresh Raspberry Pi 5 installation does not provide a working compatible interface, install:

```bash
sudo apt install -y python3-rpi-lgpio
```

Then verify again:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO interface OK')"
```

If a conflicting classic `python3-rpi.gpio` package is present, it may need to be removed first:

```bash
sudo apt remove -y python3-rpi.gpio
sudo apt install -y python3-rpi-lgpio
```

Do not intentionally maintain multiple conflicting packages providing the same `RPi.GPIO` Python namespace.

---

# 8. Enable I2C

The MPU6050 IMU communicates with the Raspberry Pi through I2C.

Run:

```bash
sudo raspi-config
```

Navigate to:

```text
Interface Options
→ I2C
→ Enable
```

Exit and reboot:

```bash
sudo reboot
```

---

# 9. Verify the MPU6050

After rebooting, scan I2C bus 1:

```bash
i2cdetect -y 1
```

The current `heading.py` uses:

```text
I2C bus: 1
MPU6050 address: 0x68
```

A correctly connected MPU6050 should normally appear as:

```text
68
```

in the I2C scan.

If `68` does not appear:

- check MPU6050 power,
- check SDA,
- check SCL,
- check common ground,
- confirm I2C is enabled,
- inspect the connector,
- confirm the sensor is connected to the expected I2C bus.

Do not run IMU-dependent manoeuvres until this is resolved.

---

# 10. MPU6050 Wiring

Typical MPU6050 connections are:

| MPU6050 | Raspberry Pi |
|---|---|
| VCC | appropriate sensor supply |
| GND | GND |
| SDA | GPIO2 / physical pin 3 |
| SCL | GPIO3 / physical pin 5 |

The final wiring should always be checked against the electrical schematic in:

```text
schemes/
```

Do not rely only on this table if the final competition harness has been documented more precisely in the schematic.

---

# 11. Main GPIO Configuration

The current committed `drive.py` uses BCM GPIO numbering.

| Function | BCM GPIO | Physical Pin |
|---|---:|---:|
| Motor driver IN1 | GPIO5 | Pin 29 |
| Motor driver IN2 | GPIO6 | Pin 31 |
| Motor PWM | GPIO13 | Pin 33 |
| Steering servo PWM | GPIO22 | Pin 15 |
| I2C SDA | GPIO2 | Pin 3 |
| I2C SCL | GPIO3 | Pin 5 |

The current `drive.py` defines:

```text
PWM_PIN   = 13
IN1_PIN   = 5
IN2_PIN   = 6
SERVO_PIN = 22
```

---

# 12. Motor Driver Configuration

The motor is controlled through the TB6612FNG motor-driver system.

Current source configuration:

```text
IN1  = GPIO5
IN2  = GPIO6
PWM  = GPIO13
```

Motor PWM frequency:

```text
1000 Hz
```

The challenge code should control the drivetrain through:

```python
drive.forward(speed)
drive.backward(speed)
drive.stop()
```

rather than duplicating low-level GPIO control.

---

# 13. Steering Servo Configuration

The DS3225 steering servo is controlled through:

```text
GPIO22
```

Servo PWM frequency:

```text
50 Hz
```

The **current committed `drive.py`** defines:

```text
LEFT   = 35
CENTER = 75
RIGHT  = 105
```

The `steer()` function also clamps steering commands to the allowed range.

> [!CAUTION]
> Do not expand the steering range without inspecting the physical Ackermann mechanism.
>
> Earlier testing showed that excessive steering movement could place high stress on the linkage and could cause mechanical disconnection.

The exact physically tested source remains authoritative if a competition calibration differs from an older documentation value.

---

# 14. Camera Installation

Starlight uses two Raspberry Pi Camera Module 3 units.

Always power the Raspberry Pi off before connecting or reseating CSI cables.

## Front Camera

The front camera is used for:

- Open Challenge wall following,
- blue/orange marker detection,
- black-wall detection,
- red/green pillar detection,
- obstacle navigation,
- front parking geometry.

Recorded final geometry includes approximately:

- 5 mm right of the vehicle centre,
- approximately 50° downward pitch.

The mount should remain rigid.

Changing the camera position can alter:

- visible wall geometry,
- contour position,
- marker timing,
- obstacle apparent size,
- parking alignment.

---

## Rear Camera

The rear camera is used primarily for parking.

Recorded geometry includes approximately:

- 45° downward pitch,
- approximately 0° yaw.

The rear camera should also remain rigid because the parking logic depends on repeatable geometry.

---

# 15. Verify Both Cameras

After connecting both cameras:

```bash
rpicam-hello --list-cameras
```

Both cameras should appear.

Test camera 0:

```bash
rpicam-hello --camera 0 --timeout 3000
```

Test camera 1:

```bash
rpicam-hello --camera 1 --timeout 3000
```

Confirm for each camera:

- image is visible,
- image orientation is correct,
- CSI ribbon is secure,
- lens is unobstructed,
- mount is rigid,
- no intermittent connection occurs.

---

# 16. Current Camera Mapping

The current committed software uses the following camera mapping.

## Open Challenge

`openVision.py` initializes:

```python
Picamera2(0)
```

Therefore:

```text
Camera 0 → front navigation camera
```

---

## Obstacle Challenge

`vision.py` also initializes:

```python
Picamera2(0)
```

Therefore:

```text
Camera 0 → front navigation camera
```

---

## Parking

The current parking source initializes:

```text
Camera 0 → front camera
Camera 1 → rear camera
```

Do not exchange camera numbering immediately before competition without retesting the complete program.

---

# 17. Clone the Team Sentio Repository

From the Raspberry Pi terminal:

```bash
cd ~
```

Clone:

```bash
git clone https://github.com/teamsentiorobotics-svg/World-Robot-Olympiad---Team-Sentio-.git
```

Enter the repository:

```bash
cd World-Robot-Olympiad---Team-Sentio-
```

Check the root:

```bash
ls
```

The repository should contain items including:

```text
README.md
CHANGELOG.md
requirements.md
docs/
models/
schemes/
src/
t-photos/
v-photos/
video/
other/
```

---

# 18. Verify the Competition Source Directory

Run:

```bash
ls src
```

The current GitHub source directory should include:

```text
open_challenge_final_ready_to_go.py
Obstacle_Challenge.py
drive.py
openVision.py
vision.py
heading.py
parking.py
```

Do not assume an older filename such as:

```text
Open_Challenge.py
```

The current Open Challenge executable is:

```text
open_challenge_final_ready_to_go.py
```

---

# 19. Record the Exact Git Revision

From the repository root:

```bash
git rev-parse HEAD
```

This returns the exact commit SHA.

Also run:

```bash
git status
```

For final competition reproducibility, the preferred state is:

```text
nothing to commit, working tree clean
```

Any local modifications on the Raspberry Pi should be reviewed carefully.

A physically tested source file should not exist only as an uncommitted Raspberry Pi edit while GitHub contains a different version.

---

# 20. Verify External Python Dependencies

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
print("SMBus2: OK")
print("Picamera2: OK")
print("GPIO interface: OK")
print("Team Sentio external dependency check: PASS")
PY
```

The command should complete without an exception.

---

# 21. Verify Core Local Modules

Enter the source directory:

```bash
cd src
```

Run:

```bash
python3 - <<'PY'
import drive
import openVision
import vision
import heading

print("drive.py: OK")
print("openVision.py: OK")
print("vision.py: OK")
print("heading.py: OK")
print("Team Sentio core modules: PASS")
PY
```

Then return to the root:

```bash
cd ..
```

---

# 22. Verify `heading.py`

Place the robot on a stable surface.

The MPU6050 must remain still during calibration.

Run:

```bash
python3 src/heading.py
```

The module performs an initial Z-axis gyro calibration.

The current implementation collects approximately:

```text
1500 samples
```

with the robot stationary.

If the robot moves during calibration, the resulting gyro offset may be inaccurate.

Confirm that:

- initialization succeeds,
- no I2C exception occurs,
- calibration completes,
- heading values can be obtained.

---

# 23. Verify Motor Direction Safely

Before performing this test:

- raise the drive wheels,
- confirm the track area is clear,
- ensure the battery is secure,
- keep a power disconnect available.

From the repository root:

```bash
cd src
```

Start Python:

```bash
python3
```

Then:

```python
import drive
```

Test forward motion briefly:

```python
drive.forward(20)
```

Stop:

```python
drive.stop()
```

Test reverse briefly:

```python
drive.backward(20)
```

Stop:

```python
drive.stop()
```

Then:

```python
drive.cleanup()
```

Exit Python:

```python
exit()
```

Confirm:

- wheels move in the expected forward direction,
- reverse direction is correct,
- motor stops correctly,
- no binding is present,
- gears remain engaged.

---

# 24. Verify Steering Safely

With the robot stationary:

```bash
cd src
python3
```

Then:

```python
import drive
```

Centre:

```python
drive.steer(drive.CENTER)
```

Left:

```python
drive.steer(drive.LEFT)
```

Centre again:

```python
drive.steer(drive.CENTER)
```

Right:

```python
drive.steer(drive.RIGHT)
```

Centre:

```python
drive.steer(drive.CENTER)
```

Cleanup:

```python
drive.cleanup()
```

Exit:

```python
exit()
```

Confirm:

- the steering moves in the correct direction,
- the linkage does not bind,
- the servo does not force the mechanism past its safe mechanical limits,
- centre position is suitable for straight travel.

---

# 25. Open Challenge Vision Configuration

The current Open Challenge vision module is:

```text
src/openVision.py
```

Current primary camera configuration:

```text
Camera:        Picamera2(0)
Resolution:    1480 × 520
Pixel format:  RGB888
Requested FPS: 60
```

The Open module detects:

```text
BLACK
BLUE
ORANGE
```

The front camera should therefore be checked under competition-like lighting for:

- black walls,
- blue markers,
- orange markers.

Do not change HSV thresholds immediately before competition without retesting the complete Open Challenge.

---

# 26. Obstacle Vision Configuration

The current Obstacle Challenge vision module is:

```text
src/vision.py
```

Current primary camera configuration:

```text
Camera:        Picamera2(0)
Resolution:    1480 × 520
Pixel format:  RGB888
Requested FPS: 60
```

The module detects:

```text
RED
GREEN
BLACK
BLUE
ORANGE
MAGENTA
```

The system combines:

- HSV information,
- LAB information,
- contour geometry,
- area filtering,
- confidence filtering,
- morphological noise filtering.

Test detection under lighting conditions similar to those expected during the competition.

---

# 27. Run the Open Challenge

Return to the repository root:

```bash
cd ~/World-Robot-Olympiad---Team-Sentio-
```

The current Open executable is:

```text
src/open_challenge_final_ready_to_go.py
```

Run:

```bash
python3 src/open_challenge_final_ready_to_go.py
```

The current committed program includes settings such as:

```text
LINE_COOLDOWN     = 1.3
TOTAL_LINES       = 12
KP                = 0.013
START_SPEED       = 40
TARGET_SPEED      = 100
ACCELERATION_TIME = 2.0
```

The source itself remains the authoritative reference.

Before a full-speed run:

1. confirm camera 0 is the front camera,
2. confirm steering centre,
3. verify motor direction,
4. confirm blue/orange detection,
5. place the robot correctly,
6. ensure the track is clear.

The Open program uses:

```text
Blue   → anticlockwise direction information
Orange → clockwise direction information
Black  → wall following
```

The robot counts valid course-marker events and stops after the configured completion sequence.

---

# 28. Run the Obstacle Challenge

From the repository root:

```bash
python3 src/Obstacle_Challenge.py
```

The current source imports:

```python
from heading import MPU6050Heading
import drive
import vision
import parking
```

Important current configuration values include:

```text
total_lap            = 3
rs                   = 45
KP                   = 0.014
OBSTACLE_ACTION_AREA = 18000
```

The Obstacle Challenge combines:

- black-wall following,
- red-pillar avoidance,
- green-pillar avoidance,
- direction-aware navigation,
- MPU6050 heading,
- parking.

Before running:

1. confirm MPU6050 address `0x68`,
2. allow the IMU calibration to complete while stationary,
3. verify front-camera detection,
4. verify steering,
5. verify motor direction,
6. verify parking dependencies,
7. position the robot correctly on the track.

---

# 29. Parking Architecture

Parking is implemented through:

```text
src/parking.py
```

The parking behaviour combines:

- front camera,
- rear camera,
- black-wall geometry,
- magenta detection,
- MPU6050 heading,
- forward motion,
- reverse motion,
- Ackermann steering corrections.

Current camera mapping:

```text
Front camera → Picamera2(0)
Rear camera  → Picamera2(1)
```

Because Starlight uses Ackermann steering, the robot cannot rotate in place.

Parking therefore requires controlled forward and reverse arcs.

---

# 30. Important Repository Integrity Check Before Final Freeze

The physical robot has completed Open, Obstacle and Parking testing successfully.

However, before declaring the **GitHub clone itself** completely reproducible, compare the GitHub parking files with the exact versions on the working Raspberry Pi.

At the time of this documentation update, two items should be checked.

## A. Parking Drive Import

The current GitHub `parking.py` includes:

```python
import robot_drive as drive
```

while the visible GitHub `src/` directory contains:

```text
drive.py
```

and does not currently contain:

```text
robot_drive.py
```

If the physically tested Raspberry Pi uses a separate:

```text
robot_drive.py
```

then that exact file must be added to GitHub.

If the physically tested parking program actually uses:

```python
import drive
```

then the GitHub `parking.py` should be synchronized with that tested copy.

---

## B. Parking Function Entry Point

The current GitHub `Obstacle_Challenge.py` ends by calling:

```python
parking.run_parking_clockwise()
```

The parking file committed to GitHub must expose the exact function called by the tested Obstacle Challenge.

Therefore verify that the working Raspberry Pi copies of:

```text
Obstacle_Challenge.py
parking.py
```

match each other exactly.

Do **not** solve this by guessing immediately before competition.

Use the files from the successfully tested physical robot as the authoritative source.

After synchronizing them:

```bash
git status
```

then commit and push the validated files.

---

# 31. Clean-Clone Module Verification

After resolving the parking dependency and entry-point check, a clean clone should allow:

```bash
cd src
```

Then:

```bash
python3 -c "import drive; print('drive: OK')"
```

```bash
python3 -c "import openVision; print('openVision: OK')"
```

```bash
python3 -c "import vision; print('vision: OK')"
```

```bash
python3 -c "import heading; print('heading: OK')"
```

Finally:

```bash
python3 -c "import parking; print('parking: OK')"
```

All required local imports should complete without:

```text
ModuleNotFoundError
```

---

# 32. Recommended Testing Sequence

Do not begin with a full-speed autonomous run after a fresh setup.

Use the following sequence:

```text
Power / wiring check
        ↓
GPIO import
        ↓
I2C detection
        ↓
MPU6050 calibration
        ↓
Camera 0 test
        ↓
Camera 1 test
        ↓
Motor direction test
        ↓
Steering test
        ↓
Open vision check
        ↓
Obstacle vision check
        ↓
Low-speed Open Challenge
        ↓
Full Open Challenge
        ↓
Low-speed Obstacle Challenge
        ↓
Full Obstacle Challenge
        ↓
Parking validation
```

This allows faults to be isolated before multiple subsystems interact.

---

# 33. Minimum Pre-Run Verification

Before competition testing, confirm all of the following.

## Power

- battery connected correctly,
- battery secure,
- Raspberry Pi supply stable,
- no repeated undervoltage warnings,
- common ground present.

## Mechanical

- wheels rotate freely,
- gears engaged,
- motor mount secure,
- steering linkage intact,
- steering linkage not binding,
- camera mounts rigid.

## Raspberry Pi

```bash
python3 --version
```

```bash
python3 -c "import cv2, numpy, smbus2; print('Python dependencies OK')"
```

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO OK')"
```

## IMU

```bash
i2cdetect -y 1
```

Confirm:

```text
68
```

## Cameras

```bash
rpicam-hello --list-cameras
```

Confirm both cameras are present.

## Repository

```bash
git status
```

```bash
git rev-parse HEAD
```

Confirm the physically tested source is the source being run.

---

# 34. Troubleshooting — GPIO Import Failure

If:

```bash
python3 -c "import RPi.GPIO as GPIO"
```

fails, install the Raspberry Pi 5 compatibility package:

```bash
sudo apt install -y python3-rpi-lgpio
```

If necessary:

```bash
sudo apt remove -y python3-rpi.gpio
sudo apt install -y python3-rpi-lgpio
```

Then test again.

---

# 35. Troubleshooting — GPIO Already Allocated / In Use

If the GPIO library reports that a pin is already allocated, first confirm that another Python robot process is not still running.

Check:

```bash
ps aux | grep python
```

Stop only the known conflicting process.

For example:

```bash
kill <PID>
```

If required:

```bash
sudo kill <PID>
```

Do not indiscriminately kill unrelated system processes.

---

# 36. Troubleshooting — MPU6050 Not Detected

Run:

```bash
i2cdetect -y 1
```

If `68` is absent:

- power off,
- inspect VCC,
- inspect GND,
- inspect SDA,
- inspect SCL,
- reseat connectors,
- reboot,
- repeat the scan.

Do not begin the Obstacle Challenge while the sensor connection is unresolved.

---

# 37. Troubleshooting — Camera Not Detected

Run:

```bash
rpicam-hello --list-cameras
```

If one camera is missing:

1. power off the Raspberry Pi,
2. reseat the CSI ribbon,
3. inspect ribbon orientation,
4. inspect connector locks,
5. reboot,
6. test again.

Do not reconnect CSI cables while the Raspberry Pi is powered.

---

# 38. Troubleshooting — Wrong Camera Used

The final mapping is intended as:

```text
Camera 0 → front
Camera 1 → rear
```

If camera numbering changes:

```bash
rpicam-hello --list-cameras
```

Verify which physical camera corresponds to each index.

Do not modify the software camera numbers until you have established whether the hardware enumeration changed.

Any camera-index change must be followed by full retesting.

---

# 39. Troubleshooting — Motor Does Not Move

Check:

- battery,
- motor-driver power,
- common ground,
- GPIO5,
- GPIO6,
- GPIO13,
- TB6612FNG wiring,
- drivetrain freedom,
- motor connections.

Test at reduced speed with the wheels raised.

Do not assume that a non-moving motor is necessarily a software problem.

---

# 40. Troubleshooting — Motor Direction Reversed

If:

```python
drive.forward()
```

causes physical reverse motion, compare the Raspberry Pi wiring with the documented schematic and the physically validated robot.

Do not casually reverse source logic if the issue is caused by swapped motor connections.

The objective is to make the reproduced hardware and software match the tested robot.

---

# 41. Troubleshooting — Steering Direction Incorrect

Check:

- GPIO22,
- servo supply,
- common ground,
- linkage orientation,
- servo horn installation,
- current `drive.py`.

Do not expand the steering range as a first troubleshooting step.

---

# 42. Troubleshooting — Steering Oscillation

Possible causes include:

- proportional gain too large,
- noisy wall target,
- camera movement,
- unstable lighting,
- loose linkage,
- excessive mechanical steering travel,
- vision threshold instability.

Change one variable at a time and retest.

---

# 43. Troubleshooting — Poor Colour Detection

Before changing thresholds:

1. clean the camera lens,
2. verify camera angle,
3. verify illumination,
4. confirm the correct camera,
5. inspect the OpenCV display,
6. inspect contour size,
7. confirm object colour,
8. compare with competition-like lighting.

The Open and Obstacle vision modules use different thresholds.

Do not copy thresholds blindly between:

```text
openVision.py
```

and:

```text
vision.py
```

---

# 44. Troubleshooting — Parking Import Failure

If:

```bash
python3 -c "import parking"
```

produces:

```text
ModuleNotFoundError: No module named 'robot_drive'
```

do not invent a replacement module.

Compare the GitHub copy with the physically tested Raspberry Pi files.

Either:

- commit the exact required `robot_drive.py`, or
- synchronize `parking.py` with the tested version that uses `drive.py`.

The physically validated robot source is authoritative.

---

# 45. Troubleshooting — Parking Function Error

If the Obstacle Challenge reports an error such as:

```text
AttributeError:
module 'parking' has no attribute 'run_parking_clockwise'
```

compare:

```text
Obstacle_Challenge.py
```

and:

```text
parking.py
```

with the working physical Raspberry Pi.

The function called by `Obstacle_Challenge.py` and the function defined by `parking.py` must match.

Do not rename functions without retesting the complete Obstacle + Parking sequence.

---

# 46. Do Not Tune Multiple Variables at Once

When troubleshooting the robot, avoid changing:

- motor speed,
- steering centre,
- KP,
- colour thresholds,
- camera position,
- obstacle area threshold,

simultaneously.

Instead:

```text
Change one variable
      ↓
Test
      ↓
Record result
      ↓
Keep or revert
      ↓
Move to next variable
```

This makes cause-and-effect much easier to understand.

---

# 47. Final Competition Release Check

Before freezing the repository, verify:

- [ ] Raspberry Pi boots correctly.
- [ ] No repeated undervoltage warning.
- [ ] GPIO interface imports.
- [ ] I2C enabled.
- [ ] MPU6050 detected at `0x68`.
- [ ] `heading.py` calibration succeeds.
- [ ] Front camera detected.
- [ ] Rear camera detected.
- [ ] Camera 0 is the front camera.
- [ ] Camera 1 is the rear camera.
- [ ] Motor direction correct.
- [ ] Drivetrain mechanically free.
- [ ] Steering linkage secure.
- [ ] Current steering range mechanically safe.
- [ ] `openVision.py` works.
- [ ] `vision.py` works.
- [ ] Open Challenge source matches the physically tested file.
- [ ] Obstacle Challenge source matches the physically tested file.
- [ ] Parking source matches the physically tested file.
- [ ] Parking drive-module dependency is present.
- [ ] Parking entry-point function matches `Obstacle_Challenge.py`.
- [ ] Open Challenge completes a physical run.
- [ ] Obstacle Challenge completes a physical run.
- [ ] Parking completes physically.
- [ ] `git status` shows no accidental local source changes.
- [ ] Final Git commit SHA is recorded.
- [ ] GitHub matches the working Raspberry Pi.

---

# 48. Final Reproduction Sequence

A clean reproduction should follow this general sequence:

```text
Install Raspberry Pi OS
        ↓
Update system
        ↓
Install Python / Raspberry Pi dependencies
        ↓
Configure GPIO support
        ↓
Enable I2C
        ↓
Verify MPU6050
        ↓
Connect and verify cameras
        ↓
Clone repository
        ↓
Record Git revision
        ↓
Verify external Python imports
        ↓
Verify local modules
        ↓
Test motor
        ↓
Test steering
        ↓
Test Open vision
        ↓
Test Obstacle vision
        ↓
Run Open Challenge
        ↓
Run Obstacle Challenge
        ↓
Run / validate parking
        ↓
Confirm GitHub and Raspberry Pi are synchronized
```

---

# 49. Repository Reproduction Resources

The full project should be reproduced using all of the repository material together.

| Resource | Location |
|---|---|
| Project overview | [`../README.md`](../README.md) |
| Development history | [`../CHANGELOG.md`](../CHANGELOG.md) |
| Software requirements | [`../requirements.md`](../requirements.md) |
| Software dependencies | [`Software_Dependencies.md`](Software_Dependencies.md) |
| Open Challenge | [`../src/open_challenge_final_ready_to_go.py`](../src/open_challenge_final_ready_to_go.py) |
| Obstacle Challenge | [`../src/Obstacle_Challenge.py`](../src/Obstacle_Challenge.py) |
| Drive control | [`../src/drive.py`](../src/drive.py) |
| Open vision | [`../src/openVision.py`](../src/openVision.py) |
| Obstacle vision | [`../src/vision.py`](../src/vision.py) |
| MPU6050 heading | [`../src/heading.py`](../src/heading.py) |
| Parking | [`../src/parking.py`](../src/parking.py) |
| Electrical schematic | [`../schemes/`](../schemes/) |
| CAD / printable components | [`../models/`](../models/) |
| Vehicle photographs | [`../v-photos/`](../v-photos/) |
| Team photographs | [`../t-photos/`](../t-photos/) |
| Autonomous video evidence | [`../video/`](../video/) |
| Supporting engineering material | [`../other/`](../other/) |

---

# 50. Final Release Principle

The repository should satisfy:

```text
Physical Starlight
        =
Software on Raspberry Pi
        =
Software on GitHub
        =
Reproduction documentation
```

If any last-minute competition adjustment changes:

- steering calibration,
- motor speed,
- proportional gain,
- colour threshold,
- obstacle threshold,
- camera mapping,
- marker timing,
- parking logic,
- heading logic,

the updated version must be retested before it is treated as the final validated competition source.

The goal is not merely for the original Raspberry Pi to run successfully.

The goal is for the GitHub repository to accurately represent the robot that was physically tested.

---

**Team Sentio**  
**Starlight**  
**World Robot Olympiad — Future Engineers 2026**  
**Robofun Lab (RFL), India**
