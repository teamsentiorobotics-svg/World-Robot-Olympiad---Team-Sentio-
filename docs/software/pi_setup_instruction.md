# Raspberry Pi Setup and Run Guide

## Team Sentio — WRO Future Engineers 2026

This document describes how to prepare a Raspberry Pi 5, install the required software, configure the cameras, MPU6050, encoder and three VL53L0X sensors, verify the motor and steering system, clone the Team Sentio repository, and run the competition software used by **Starlight**.

**Team:** Deyaan Agrawal, Darsh Zaveri, Aarav Jalan  
**Mentors:** Sunil Solanki, Shyam Satasiya  
**Robot:** Starlight  
**Competition:** World Robot Olympiad 2026 — Future Engineers  
**Institution / Training Environment:** Robofun Lab (RFL), India  
**Documentation Revision:** Revision 29, September 2026

The purpose of this guide is **reproducibility**.

A technically competent user should be able to start with a compatible Raspberry Pi 5, reproduce the software environment, connect the documented hardware, verify the required subsystems and understand how the current competition software is launched.

> [!IMPORTANT]
> The exact source running on the physically tested robot remains the authoritative competition version.
>
> The Raspberry Pi source, GitHub source, calibration values, wiring documentation and engineering journal should remain synchronized whenever the competition configuration changes.

---

# 1. Competition Computing Platform

The current Starlight computing and sensing system uses:

- Raspberry Pi 5, 4 GB
- Raspberry Pi OS
- Python 3
- 2 × Raspberry Pi Camera Module 3 Wide
- OpenCV
- NumPy
- Picamera2
- RPi.GPIO-compatible GPIO interface
- SMBus2 / I2C
- MPU6050 heading sensor
- 3 × VL53L0X time-of-flight sensors
- motor quadrature encoder
- TB6612FNG motor driver
- DS3225 steering servo
- 12 V geared DC encoder motor
- 3S 11.1 V LiPo battery
- regulated Raspberry Pi electronics supply

The current GitHub competition source directory is:

```text
src/
├── Cal_APOC.py
├── Final_Obstacle_Challenge.py
├── N_Vision_final.py
├── Sentio_Open_2026.py
├── openvision.py
├── TOF_22.py
├── TUF_test.py
├── drive.py
├── encoder_test.py
├── heading.py
├── parking_final.py
└── servo_test.py
```

The principal files have the following roles:

| File | Purpose |
|---|---|
| `Cal_APOC.py` | Interactive HSV / LAB field calibration |
| `Final_Obstacle_Challenge.py` | Main Obstacle Challenge controller |
| `N_Vision_final.py` | Multi-ROI obstacle, wall and course-colour vision |
| `Sentio_Open_2026.py` | Main Open Challenge controller |
| `openvision.py` | Open Challenge vision module |
| `TOF_22.py` | Three-VL53L0X initialization and distance interface |
| `TUF_test.py` | ToF communication and distance test |
| `drive.py` | Motor, steering and encoder interface |
| `encoder_test.py` | Encoder and movement test |
| `heading.py` | MPU6050 relative-heading calculation |
| `parking_final.py` | Parking controller |
| `servo_test.py` | Steering centre, direction and travel test |

---

# 2. Important Safety Information

Before configuring or running Starlight:

1. Switch the robot off before connecting or disconnecting cameras, GPIO wiring or I2C devices.
2. Confirm battery polarity before applying power.
3. Never connect the 3S LiPo voltage directly to the Raspberry Pi 5 V rail.
4. Use a properly regulated power supply for the Raspberry Pi.
5. The DC motor must be controlled through the motor driver and must never be connected directly to Raspberry Pi GPIO.
6. Ensure connected control electronics share the correct common electrical reference.
7. Check the steering linkage mechanically before powering the servo.
8. Raise the drive wheels or place the robot safely on the track before running motor tests.
9. Keep hands, tools and loose wires away from wheels, gears and the steering mechanism.
10. Keep a rapid power-disconnect method available during testing.
11. Charge the LiPo only with an appropriate balance charger and under supervision.
12. Do not change wiring while the battery is connected.
13. Do not increase steering travel without mechanically checking the Ackermann linkage.
14. Stop testing immediately if the Raspberry Pi reports repeated undervoltage warnings.

These checks are part of the normal setup process, not optional extras added after something starts smoking.

---

# 3. Install Raspberry Pi OS

Use **Raspberry Pi Imager** to install a current Raspberry Pi OS image compatible with the Raspberry Pi 5.

A Raspberry Pi OS installation with the graphical desktop is useful during development because the vision programs may use OpenCV display windows such as:

```python
cv2.imshow()
```

During Raspberry Pi Imager setup, configure as required:

- username;
- password;
- hostname;
- keyboard layout;
- locale;
- Wi-Fi.

After writing the image:

1. insert the storage device into the Raspberry Pi;
2. connect the required display, keyboard and mouse during setup;
3. boot the Raspberry Pi;
4. complete Raspberry Pi OS first-run configuration.

---

# 4. Record the Operating Environment

For reproducibility, record the operating-system and Python information:

```bash
cat /etc/os-release
```

```bash
uname -a
```

```bash
python3 --version
```

Optional package-state records:

```bash
python3 -m pip list
```

```bash
dpkg -l | grep -E "picamera2|opencv|numpy|smbus|gpio"
```

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

Install the principal Raspberry Pi OS packages:

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
| `git` | Clone and synchronize the repository |
| `python3-picamera2` | Raspberry Pi camera interface |
| `python3-opencv` | Computer vision |
| `python3-numpy` | Numerical and image-array processing |
| `python3-smbus2` | I2C communication |
| `i2c-tools` | I2C diagnostics |

Any additional package required by the exact final ToF or encoder source should be installed according to the imports in that tested source.

Verify Python:

```bash
python3 --version
```

---

# 7. Configure GPIO Support on Raspberry Pi 5

The Team Sentio drive software uses an interface compatible with:

```python
import RPi.GPIO as GPIO
```

First test the current environment:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO import OK')"
```

If this succeeds, continue.

If a Raspberry Pi 5 installation does not provide a working compatible interface, install:

```bash
sudo apt install -y python3-rpi-lgpio
```

Then verify again:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO interface OK')"
```

If a conflicting classic package is present:

```bash
sudo apt remove -y python3-rpi.gpio
sudo apt install -y python3-rpi-lgpio
```

Do not intentionally maintain conflicting packages that provide the same `RPi.GPIO` namespace.

---

# 8. Enable I2C

The MPU6050 and VL53L0X sensors use I2C.

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

After reboot:

```bash
i2cdetect -y 1
```

---

# 9. Verify the MPU6050

The shared heading helper is:

```text
src/heading.py
```

The MPU6050 is expected on I2C bus 1 at:

```text
0x68
```

Scan:

```bash
i2cdetect -y 1
```

A correctly connected MPU6050 should normally appear as:

```text
68
```

If `68` does not appear:

- check MPU6050 power;
- check SDA;
- check SCL;
- check common ground;
- confirm I2C is enabled;
- inspect the connector;
- confirm the sensor is connected to the expected bus.

Do not run IMU-dependent manoeuvres until the connection is resolved.

---

# 10. MPU6050 Wiring

Typical connections are:

| MPU6050 | Raspberry Pi |
|---|---|
| VCC | appropriate sensor supply |
| GND | GND |
| SDA | GPIO2 / physical pin 3 |
| SCL | GPIO3 / physical pin 5 |

The final wiring should also be checked against:

```text
schemes/
docs/wiring_guide.md
```

The schematic takes precedence over a generic table if the final harness is documented more precisely there.

---

# 11. Main GPIO Configuration

The current documented control assignments are:

| Function | BCM GPIO | Physical Pin |
|---|---:|---:|
| Motor driver IN1 | GPIO5 | Pin 29 |
| Motor driver IN2 | GPIO6 | Pin 31 |
| Motor PWM | GPIO13 | Pin 33 |
| Steering servo | GPIO22 | Pin 15 |
| Encoder A | GPIO17 | Pin 11 |
| Encoder B | GPIO27 | Pin 13 |
| I2C SDA | GPIO2 | Pin 3 |
| I2C SCL | GPIO3 | Pin 5 |
| ToF 1 XSHUT | GPIO16 | Pin 36 |
| ToF 2 XSHUT | GPIO20 | Pin 38 |
| ToF 3 XSHUT | GPIO21 | Pin 40 |

The competition source remains authoritative if a late tested revision changes any assignment.

---

# 12. Motor Driver Configuration

The drive motor is controlled through the TB6612FNG motor-driver system.

The documented motor-control pins are:

```text
IN1  = GPIO5
IN2  = GPIO6
PWM  = GPIO13
```

The motor PWM baseline is:

```text
1000 Hz
```

Challenge controllers should request movement through the shared drive interface:

```python
drive.forward(speed)
drive.backward(speed)
drive.stop()
```

rather than reimplementing low-level GPIO control inside each challenge script.

---

# 13. Steering Servo Configuration

The DS3225 steering servo is controlled through:

```text
GPIO22
```

with a baseline PWM frequency of:

```text
50 Hz
```

The exact competition steering centre and travel limits are defined by the tested `src/drive.py`.

Do not copy an older centre, left limit or right limit into a new installation without checking the current source and the physical mechanism.

> [!CAUTION]
> Do not expand the steering range without inspecting the physical Ackermann linkage.
>
> Excessive steering travel can load the linkage, bind the mechanism or disconnect steering components.

Use the dedicated test:

```bash
python3 src/servo_test.py
```

before a full challenge run.

---

# 14. Encoder Configuration

The current drive motor includes a quadrature encoder.

Documented encoder pins are:

```text
Encoder A → GPIO17
Encoder B → GPIO27
```

The encoder is used for:

- movement feedback;
- checking direction;
- repeatable encoder-targeted movement;
- motor-response testing.

The encoder measures shaft motion, not exact ground displacement.

Wheel slip, tyre deformation and drivetrain play can make physical travel differ from shaft-based movement.

Use:

```bash
python3 src/encoder_test.py
```

to verify the current implementation.

---

# 15. Three VL53L0X Sensors

Starlight uses:

```text
3 × VL53L0X
```

The sensors share the I2C bus.

Because identical VL53L0X sensors begin with the same default address, their XSHUT lines are used to enable them sequentially and assign separate working addresses.

The documented XSHUT connections are:

```text
ToF 1 XSHUT → GPIO16
ToF 2 XSHUT → GPIO20
ToF 3 XSHUT → GPIO21
```

The current sensor interface is:

```text
src/TOF_22.py
```

The dedicated test program is:

```text
src/TUF_test.py
```

Run:

```bash
python3 src/TUF_test.py
```

Verify:

- all three sensors initialize;
- each sensor responds independently;
- distances change sensibly when an object is moved;
- physical sensor orientation matches the software meaning assigned to that sensor.

---

# 16. Camera Installation

Starlight uses:

```text
2 × Raspberry Pi Camera Module 3 Wide
```

Always power the Raspberry Pi off before connecting or reseating CSI cables.

The camera mounts should remain rigid.

Changing camera position can alter:

- visible wall geometry;
- contour position;
- marker timing;
- pillar apparent size;
- parking alignment;
- ROI validity.

The current engineering documentation describes a relatively downward-facing camera geometry, approximately:

```text
60° from horizontal
```

Treat camera pose as a mechanical calibration parameter, not merely a cosmetic mounting choice.

---

# 17. Verify Both Cameras

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

- image is visible;
- image orientation is correct;
- CSI ribbon is secure;
- lens is unobstructed;
- mount is rigid;
- no intermittent connection occurs.

Camera numbering must be verified on the physical Raspberry Pi before changing software indices.

---

# 18. Clone the Team Sentio Repository

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
.gitattributes
.gitignore
Models/
docs/
schemes/
src/
t-photos/
v-photos/
videos/
other/
```

---

# 19. Verify the Competition Source Directory

Run:

```bash
ls src
```

The current documented source directory should contain:

```text
Cal_APOC.py
Final_Obstacle_Challenge.py
N_Vision_final.py
Sentio_Open_2026.py
openvision.py
TOF_22.py
TUF_test.py
drive.py
encoder_test.py
heading.py
parking_final.py
servo_test.py
```

Do not substitute older development filenames such as:

```text
open_challenge_final_ready_to_go.py
Obstacle_Challenge.py
openVision.py
vision.py
parking.py
```

unless the physically tested competition Raspberry Pi actually uses those files and the repository has deliberately been reverted to that architecture.

For Revision 29 documentation, the filenames listed above are the current documented names.

---

# 20. Record the Exact Git Revision

From the repository root:

```bash
git rev-parse HEAD
```

This returns the exact commit SHA.

Also run:

```bash
git status
```

For a frozen competition configuration, the preferred state is:

```text
nothing to commit, working tree clean
```

A physically tested source file should not exist only as an uncommitted Raspberry Pi edit while GitHub contains a different version.

---

# 21. Verify External Python Dependencies

From the repository root:

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

The ToF and encoder dependencies should also be tested through the actual competition source because their exact supporting packages must match the tested implementation.

---

# 22. Syntax-Check the Current Source

From the repository root:

```bash
python3 -m py_compile \
    src/Cal_APOC.py \
    src/Final_Obstacle_Challenge.py \
    src/N_Vision_final.py \
    src/Sentio_Open_2026.py \
    src/openvision.py \
    src/TOF_22.py \
    src/TUF_test.py \
    src/drive.py \
    src/encoder_test.py \
    src/heading.py \
    src/parking_final.py \
    src/servo_test.py
```

A syntax check proves only that Python can parse the files.

It does not prove:

- camera access;
- I2C communication;
- GPIO operation;
- correct steering;
- correct motor direction;
- correct vision thresholds;
- successful autonomous behaviour.

Physical testing remains required.

---

# 23. Verify Core Local Modules

Enter the source directory:

```bash
cd src
```

Check modules that can safely be imported in the current environment:

```bash
python3 - <<'PY'
import drive
import heading
import openvision
import N_Vision_final

print("drive.py: OK")
print("heading.py: OK")
print("openvision.py: OK")
print("N_Vision_final.py: OK")
print("Core source imports: PASS")
PY
```

Return to the repository root:

```bash
cd ..
```

> [!NOTE]
> Some hardware modules may initialize GPIO, cameras or I2C devices at import time.
>
> If a module intentionally performs hardware setup during import, test it only with the robot safely connected and powered.

---

# 24. Verify `heading.py`

Place the robot on a stable surface.

The MPU6050 must remain still during calibration.

Run:

```bash
python3 src/heading.py
```

Confirm:

- initialization succeeds;
- no I2C exception occurs;
- stationary calibration completes;
- heading values can be obtained;
- the documented left/right heading convention matches physical movement.

The result is a **relative heading estimate**, not a drift-free global compass.

---

# 25. Verify Motor Direction Safely

Before this test:

- raise the drive wheels;
- confirm the area is clear;
- secure the battery;
- keep a power disconnect available.

From the repository root:

```bash
cd src
python3
```

Then:

```python
import drive
```

Test low-speed forward motion using the current function signature defined by `drive.py`.

For example, if the current source accepts a speed argument:

```python
drive.forward(20)
```

Stop:

```python
drive.stop()
```

Test reverse:

```python
drive.backward(20)
```

Stop:

```python
drive.stop()
```

If `drive.py` exposes a cleanup function:

```python
drive.cleanup()
```

Exit:

```python
exit()
```

Confirm:

- forward direction is physically correct;
- reverse direction is correct;
- the motor stops correctly;
- no mechanical binding occurs;
- gears remain engaged.

---

# 26. Verify Steering Safely

The preferred steering test is:

```bash
python3 src/servo_test.py
```

Alternatively, if testing interactively:

```bash
cd src
python3
```

Then:

```python
import drive
drive.steer(drive.CENTER)
drive.steer(drive.LEFT)
drive.steer(drive.CENTER)
drive.steer(drive.RIGHT)
drive.steer(drive.CENTER)
```

If available:

```python
drive.cleanup()
```

Exit:

```python
exit()
```

Confirm:

- steering direction is correct;
- centre is suitable for straight travel;
- linkage does not bind;
- servo does not force the mechanism past safe travel;
- steering commands remain inside the calibrated mechanical range.

---

# 27. Open Challenge Vision

The current Open Challenge vision module is:

```text
src/openvision.py
```

The current Open Challenge controller is:

```text
src/Sentio_Open_2026.py
```

The Open vision system is responsible for the visual information required by the Open Challenge, including wall and course-marker observations used by the controller.

The physically tested source remains authoritative for:

- resolution;
- FPS;
- ROI coordinates;
- colour thresholds;
- contour filters;
- proportional gain;
- line cooldown;
- speed and acceleration settings.

Do not copy tuning constants from an older version simply because the filename looks similar.

---

# 28. Obstacle Vision

The current multi-ROI vision module is:

```text
src/N_Vision_final.py
```

It supports observations involving:

```text
RED
GREEN
BLACK
BLUE
ORANGE
MAGENTA
```

as required by the current challenge architecture.

The system may combine:

- HSV information;
- LAB information;
- contour geometry;
- contour area;
- ROI identity;
- morphological filtering;
- body-exclusion regions.

The current documentation uses a multi-ROI image architecture approximately based on:

```text
720 × 360
```

The exact active camera configuration and threshold values should be read from the current tested source.

---

# 29. Field Colour Calibration

The current calibration utility is:

```text
src/Cal_APOC.py
```

Run:

```bash
python3 src/Cal_APOC.py
```

Calibration should be performed with:

- final camera mount;
- competition-like field lighting;
- final exposure behaviour;
- representative target colours;
- robot placed at useful near and far distances.

Check:

- black;
- blue;
- orange;
- red;
- green;
- magenta;
- any LAB / HSV ranges used by the final vision source.

After calibration, synchronize the resulting values with the competition vision files if required by the current workflow.

Do not recalibrate one file while accidentally leaving the challenge controller dependent on another stale vision file.

---

# 30. Run the Open Challenge

From the repository root:

```bash
cd ~/World-Robot-Olympiad---Team-Sentio-
```

Run:

```bash
python3 src/Sentio_Open_2026.py
```

Before a complete run:

1. verify camera mapping;
2. verify steering centre;
3. verify motor direction;
4. verify black-wall detection;
5. verify blue/orange course-marker detection;
6. confirm the correct calibration;
7. place the robot correctly;
8. clear the track;
9. confirm the exact Git revision being tested.

The final source itself remains authoritative for:

- acceleration;
- speed;
- steering gain;
- course-event count;
- cooldown;
- final stopping behaviour.

---

# 31. Run the Obstacle Challenge

From the repository root:

```bash
python3 src/Final_Obstacle_Challenge.py
```

The current architecture uses supporting modules including:

```text
N_Vision_final.py
heading.py
drive.py
parking_final.py
TOF_22.py
```

depending on the exact final integration.

The Obstacle Challenge combines:

- black-wall observations;
- red-pillar observations;
- green-pillar observations;
- direction-aware navigation;
- course-event counting;
- MPU6050 relative heading;
- encoder-assisted movement;
- parking transition logic.

Before running:

1. confirm MPU6050 communication;
2. allow IMU calibration to complete while stationary;
3. verify camera detection;
4. verify steering;
5. verify motor direction;
6. verify the encoder;
7. verify ToF sensors required by the parking stage;
8. verify parking dependencies;
9. position the robot correctly on the track.

---

# 32. Parking Architecture

The current parking controller is:

```text
src/parking_final.py
```

The parking architecture combines:

- camera geometry;
- wall observations;
- magenta parking references;
- MPU6050 heading;
- three VL53L0X sensors;
- encoder / drive control;
- forward and reverse Ackermann arcs.

Because Starlight uses Ackermann steering, it cannot rotate about its centre like a differential-drive robot.

Parking therefore requires controlled forward and reverse movement.

The final tested parking source is authoritative for:

- camera indices;
- ToF mapping;
- distance thresholds;
- heading thresholds;
- encoder movement;
- parking entry sequence;
- final stop logic.

---

# 33. Clockwise and Anticlockwise Parking

Clockwise and anticlockwise course completion do not place the robot in identical positions.

The parking architecture therefore contains direction-dependent positioning before final alignment.

Conceptually:

```text
CLOCKWISE
Course complete
      ↓
Direction-specific entry
      ↓
Parking positioning
      ↓
Final parallel alignment
      ↓
STOP
```

```text
ANTICLOCKWISE
Course complete
      ↓
Required reposition / turn
      ↓
Wall-relative approach
      ↓
Parking positioning
      ↓
Final parallel alignment
      ↓
STOP
```

The exact final sequence must match the physically tested `parking_final.py` and Obstacle Challenge integration.

---

# 34. Verify ToF Behaviour Before Parking

Run:

```bash
python3 src/TUF_test.py
```

Confirm all three sensors.

Then check the ToF module:

```text
src/TOF_22.py
```

against the physical sensor arrangement.

For each sensor, document:

- XSHUT GPIO;
- working I2C address;
- physical position;
- viewing direction;
- software variable name;
- parking condition that uses it.

A correct number from the wrong physical sensor is still wrong.

---

# 35. Component-Test Programs

The repository includes dedicated tests:

| Subsystem | File |
|---|---|
| Steering | `src/servo_test.py` |
| Encoder / drive movement | `src/encoder_test.py` |
| ToF sensors | `src/TUF_test.py` |
| Heading | `src/heading.py` |
| Vision calibration | `src/Cal_APOC.py` |

Recommended order:

```text
Power / wiring
      ↓
Individual component
      ↓
Subsystem
      ↓
Low-speed integration
      ↓
Full challenge
```

Do not begin debugging a complete autonomous run when the actual fault can be reproduced with a small component test.

---

# 36. Recommended Testing Sequence

Use:

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
Steering test
        ↓
Motor direction test
        ↓
Encoder test
        ↓
Three-ToF test
        ↓
Field colour calibration
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

This allows faults to be isolated before several subsystems interact.

---

# 37. Minimum Pre-Run Verification

## Power

- battery connected correctly;
- battery secure;
- Raspberry Pi supply stable;
- no repeated undervoltage warning;
- common electrical reference present.

## Mechanical

- wheels rotate freely;
- gears remain engaged;
- motor mount secure;
- steering linkage intact;
- steering does not bind;
- camera mounts rigid;
- ToF mounts rigid.

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

Confirm the MPU6050 appears at:

```text
0x68
```

## Cameras

```bash
rpicam-hello --list-cameras
```

Confirm both cameras are present.

## Source

```bash
git status
```

```bash
git rev-parse HEAD
```

Confirm the physically tested source is the source being run.

---

# 38. Repository Integrity Check

The GitHub repository should contain every module required by the competition controllers.

At minimum, verify:

```text
src/Cal_APOC.py
src/Final_Obstacle_Challenge.py
src/N_Vision_final.py
src/Sentio_Open_2026.py
src/openvision.py
src/TOF_22.py
src/TUF_test.py
src/drive.py
src/encoder_test.py
src/heading.py
src/parking_final.py
src/servo_test.py
```

There should not be a required module that exists only on the working Raspberry Pi.

The intended relationship is:

```text
Physical robot configuration
        =
Raspberry Pi source
        =
GitHub source
        =
Documentation
```

If a final competition source imports a differently named helper, add that exact tested helper or synchronize the source before freezing the repository.

Do not "fix" an import by guessing which historical file it was probably supposed to use.

---

# 39. Clean-Clone Verification

After cloning the repository on a clean Raspberry Pi environment:

```bash
git status
```

should show a clean working tree before local calibration changes are made.

Syntax-check the source:

```bash
python3 -m py_compile \
    src/Cal_APOC.py \
    src/Final_Obstacle_Challenge.py \
    src/N_Vision_final.py \
    src/Sentio_Open_2026.py \
    src/openvision.py \
    src/TOF_22.py \
    src/TUF_test.py \
    src/drive.py \
    src/encoder_test.py \
    src/heading.py \
    src/parking_final.py \
    src/servo_test.py
```

Then perform hardware tests in the order documented above.

A clean clone is not considered validated merely because all files compile.

---

# 40. Troubleshooting — GPIO Import Failure

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

# 41. Troubleshooting — PWM Object Already Exists

If execution reports something similar to:

```text
RuntimeError: A PWM object already exists for this GPIO channel
```

check whether two different drive modules are being imported in the same Python process.

For example, avoid an architecture in which one stage initializes:

```python
import drive
```

and a later stage imports another module that creates a second PWM object on the same motor or servo GPIO.

Also check whether another robot process is still running:

```bash
ps aux | grep python
```

Stop only the known conflicting process:

```bash
kill <PID>
```

If required:

```bash
sudo kill <PID>
```

The preferred competition architecture should have one clear owner for each GPIO PWM resource.

Do not attempt to solve a duplicate-PWM error by adding arbitrary sleeps. Time is many things, but it is not garbage collection.

---

# 42. Troubleshooting — MPU6050 Not Detected

Run:

```bash
i2cdetect -y 1
```

If `68` is absent:

- power off;
- inspect VCC;
- inspect GND;
- inspect SDA;
- inspect SCL;
- reseat connectors;
- reboot;
- repeat the scan.

Do not begin the Obstacle Challenge while the sensor connection is unresolved.

---

# 43. Troubleshooting — ToF Sensor Failure

If one or more VL53L0X sensors fail to initialize:

1. power-cycle the robot;
2. inspect all three XSHUT connections;
3. inspect SDA and SCL;
4. confirm common ground;
5. verify the correct XSHUT GPIO numbers;
6. run `src/TUF_test.py`;
7. verify sensors are enabled sequentially;
8. check that unique working addresses are assigned;
9. confirm a sensor is not physically disconnected or swapped.

Because identical VL53L0X sensors begin at the same default address, attempting to communicate with all of them before address assignment can create an I2C conflict.

---

# 44. Troubleshooting — Camera Not Detected

Run:

```bash
rpicam-hello --list-cameras
```

If one camera is missing:

1. power off the Raspberry Pi;
2. reseat the CSI ribbon;
3. inspect ribbon orientation;
4. inspect connector locks;
5. reboot;
6. test again.

Do not reconnect CSI cables while the Raspberry Pi is powered.

---

# 45. Troubleshooting — Wrong Camera Used

If a controller displays the wrong physical camera:

```bash
rpicam-hello --list-cameras
```

Verify which physical camera corresponds to each index.

Do not modify software camera indices until the actual hardware enumeration is known.

Any camera-index change should be followed by complete vision and parking retesting.

---

# 46. Troubleshooting — Motor Does Not Move

Check:

- battery;
- motor-driver power;
- common ground;
- GPIO5;
- GPIO6;
- GPIO13;
- TB6612FNG wiring;
- drivetrain freedom;
- motor connections.

Test at reduced speed with the wheels raised.

A non-moving motor is not automatically a software failure.

---

# 47. Troubleshooting — Motor Direction Reversed

If the software's forward command causes physical reverse motion:

1. compare wiring with the schematic;
2. compare the installed `drive.py` with the tested competition version;
3. confirm IN1 / IN2 connections;
4. confirm motor polarity;
5. determine whether the difference is hardware or software before changing either.

The goal is to reproduce the physically validated robot, not create a new convention five minutes before a run.

---

# 48. Troubleshooting — Steering Direction Incorrect

Check:

- GPIO22;
- servo supply;
- common ground;
- linkage orientation;
- servo horn installation;
- current `drive.py`;
- current `servo_test.py`.

Do not expand steering range as a first troubleshooting step.

---

# 49. Troubleshooting — Steering Oscillation

Possible causes include:

- proportional gain too large;
- noisy wall target;
- camera movement;
- unstable lighting;
- loose linkage;
- excessive mechanical steering travel;
- vision-threshold instability.

Change one variable at a time and retest.

---

# 50. Troubleshooting — Poor Colour Detection

Before changing thresholds:

1. clean the camera lens;
2. verify camera angle;
3. verify illumination;
4. confirm the correct camera;
5. inspect the debug image if enabled;
6. inspect contour size;
7. confirm target colour;
8. compare with competition-like lighting;
9. run `Cal_APOC.py`.

Do not assume Open Challenge and Obstacle Challenge thresholds are interchangeable.

The relevant current modules are:

```text
openvision.py
N_Vision_final.py
```

Each should retain the values validated for its actual use.

---

# 51. Troubleshooting — Encoder Does Not Count

Run:

```bash
python3 src/encoder_test.py
```

Check:

- GPIO17;
- GPIO27;
- encoder power;
- encoder ground;
- signal wiring;
- motor movement;
- count direction;
- mechanical encoder connection.

If the motor moves but the count does not change, stop encoder-targeted movements until the feedback path is repaired.

---

# 52. Troubleshooting — Import Failure

If a competition controller reports:

```text
ModuleNotFoundError
```

do not immediately create a dummy replacement module.

Check:

```bash
grep -R "^import\|^from" src/*.py
```

Then compare the imports against:

```bash
ls src
```

Every required local module should either:

- exist in the repository; or
- be a documented external dependency.

Synchronize from the physically tested Raspberry Pi if GitHub is missing a required helper.

---

# 53. Troubleshooting — Parking Function Error

If the Obstacle Challenge reports an error such as:

```text
AttributeError:
module 'parking_final' has no attribute '...'
```

compare:

```text
Final_Obstacle_Challenge.py
parking_final.py
```

with the working Raspberry Pi versions.

The function called by the controller and the function defined by the parking module must match.

Do not rename functions without rerunning the complete Obstacle + Parking sequence.

---

# 54. Do Not Tune Multiple Variables at Once

Avoid simultaneously changing:

- motor speed;
- steering centre;
- steering limits;
- proportional gain;
- colour thresholds;
- ROI coordinates;
- camera position;
- obstacle area threshold;
- orange / blue marker cooldown;
- ToF distance threshold;
- encoder target;
- heading threshold;
- parking timing.

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

This makes cause-and-effect much easier to identify.

---

# 55. Competition Calibration Policy

Values such as:

```text
Steering center
Steering limits
Motor speed
Proportional gain
Colour thresholds
ROI coordinates
Course-marker cooldown
Distance thresholds
Encoder movement targets
Parking timing
Heading thresholds
```

can change during field calibration.

The final physically tested source is authoritative.

Whenever competition calibration changes:

1. update the Raspberry Pi source;
2. test the affected subsystem;
3. test the affected challenge;
4. commit the tested source;
5. push the tested revision;
6. update documentation if architecture or interfaces changed.

---

# 56. Final Competition Release Check

Before freezing the repository:

- [ ] Raspberry Pi boots correctly.
- [ ] No repeated undervoltage warning.
- [ ] GPIO interface imports.
- [ ] I2C is enabled.
- [ ] MPU6050 detected at `0x68`.
- [ ] `heading.py` calibration succeeds.
- [ ] Front / primary navigation camera detected.
- [ ] Second camera detected.
- [ ] Camera indices match the tested source.
- [ ] Camera mounts secure.
- [ ] Motor direction correct.
- [ ] Drivetrain mechanically free.
- [ ] Encoder responds correctly.
- [ ] `encoder_test.py` passes.
- [ ] Steering linkage secure.
- [ ] Steering range mechanically safe.
- [ ] `servo_test.py` passes.
- [ ] All three VL53L0X sensors initialize.
- [ ] XSHUT sequencing works.
- [ ] `TOF_22.py` matches the tested sensor arrangement.
- [ ] `TUF_test.py` passes.
- [ ] `Cal_APOC.py` calibration matches competition lighting.
- [ ] `openvision.py` works.
- [ ] `N_Vision_final.py` works.
- [ ] Open Challenge source matches the physically tested file.
- [ ] Obstacle Challenge source matches the physically tested file.
- [ ] Parking source matches the physically tested file.
- [ ] Open Challenge completes a physical run.
- [ ] Obstacle Challenge completes a physical run.
- [ ] Parking completes physically.
- [ ] No required helper exists only on the Raspberry Pi.
- [ ] `git status` shows no accidental local source changes.
- [ ] Final Git commit SHA is recorded.
- [ ] GitHub matches the working Raspberry Pi.

---

# 57. Final Reproduction Sequence

A clean reproduction should follow:

```text
Install Raspberry Pi OS
        ↓
Update system
        ↓
Install dependencies
        ↓
Configure GPIO support
        ↓
Enable I2C
        ↓
Verify MPU6050
        ↓
Connect and verify both cameras
        ↓
Clone repository
        ↓
Record Git revision
        ↓
Syntax-check source
        ↓
Verify external Python imports
        ↓
Verify drive + steering
        ↓
Verify encoder
        ↓
Verify all three ToF sensors
        ↓
Calibrate vision
        ↓
Test Open vision
        ↓
Test Obstacle vision
        ↓
Run Open Challenge
        ↓
Run Obstacle Challenge
        ↓
Validate parking
        ↓
Confirm GitHub and Raspberry Pi are synchronized
```

---

# 58. Repository Reproduction Resources

Use the repository material together.

| Resource | Location |
|---|---|
| Project overview | [`../README.md`](../README.md) |
| Development history | [`../CHANGELOG.md`](../CHANGELOG.md) |
| Software requirements | [`../requirements.md`](../requirements.md) |
| Software dependencies | [`Software_Dependencies.md`](Software_Dependencies.md) |
| Bill of materials | [`BOM_purchase_links.md`](BOM_purchase_links.md) |
| Wiring guide | [`wiring_guide.md`](wiring_guide.md) |
| Open Challenge | [`../src/Sentio_Open_2026.py`](../src/Sentio_Open_2026.py) |
| Open Challenge vision | [`../src/openvision.py`](../src/openvision.py) |
| Obstacle Challenge | [`../src/Final_Obstacle_Challenge.py`](../src/Final_Obstacle_Challenge.py) |
| Multi-ROI vision | [`../src/N_Vision_final.py`](../src/N_Vision_final.py) |
| Drive control | [`../src/drive.py`](../src/drive.py) |
| Encoder test | [`../src/encoder_test.py`](../src/encoder_test.py) |
| MPU6050 heading | [`../src/heading.py`](../src/heading.py) |
| Parking | [`../src/parking_final.py`](../src/parking_final.py) |
| Three-ToF interface | [`../src/TOF_22.py`](../src/TOF_22.py) |
| ToF test | [`../src/TUF_test.py`](../src/TUF_test.py) |
| Field calibration | [`../src/Cal_APOC.py`](../src/Cal_APOC.py) |
| Steering test | [`../src/servo_test.py`](../src/servo_test.py) |
| Electrical schematic | [`../schemes/`](../schemes/) |
| CAD / printable components | [`../Models/`](../Models/) |
| Vehicle photographs | [`../v-photos/`](../v-photos/) |
| Team photographs | [`../t-photos/`](../t-photos/) |
| Autonomous video evidence | [`../videos/`](../videos/) |
| Supporting engineering material | [`../other/`](../other/) |

---

# 59. Final Release Principle

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

If a final competition adjustment changes:

- steering calibration;
- motor speed;
- proportional gain;
- colour threshold;
- ROI geometry;
- obstacle threshold;
- camera mapping;
- marker timing;
- ToF logic;
- encoder movement;
- parking logic;
- heading logic;

the updated version must be retested before it is treated as the final validated competition source.

The goal is not merely for one Raspberry Pi to run successfully.

The goal is for the repository to accurately represent the robot that was physically tested.

---

**Team Sentio 1747**  
**Starlight**  
**World Robot Olympiad — Future Engineers 2026**  
**Robofun Lab (RFL), India**
