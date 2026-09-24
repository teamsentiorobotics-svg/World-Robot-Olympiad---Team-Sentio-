# Software Requirements

## Team Sentio — WRO Future Engineers 2026

This document records the software environment, dependencies, hardware interfaces and verification process required to reproduce and run **Team Sentio's autonomous vehicle, Starlight**.

**Platform:** Raspberry Pi 5, 4 GB  
**Operating System:** Raspberry Pi OS  
**Programming Language:** Python 3  
**Competition:** World Robot Olympiad 2026 — Future Engineers  
**Robot:** Starlight  
**Current Documentation Baseline:** Engineering Journal Revision 29

The current Revision 29 Starlight configuration uses:

- dual Raspberry Pi Camera Module 3 Wide cameras;
- multi-ROI computer vision;
- MPU6050 heading feedback;
- a quadrature motor encoder;
- three VL53L0X time-of-flight sensors;
- Ackermann steering;
- four-wheel drive;
- modular Open, Obstacle and Parking controllers.

This document should remain synchronized with the exact software physically running on the competition robot.

For complete Raspberry Pi setup instructions, see:

[`docs/pi_setup_instruction.md`](docs/pi_setup_instruction.md)

---

# 1. Current Competition Software

The current competition software architecture is organized around:

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

The current low-level drive interface is `src/drive.py`, and the current three-sensor ToF interface is `src/TOF_22.py`.

Every local module imported by the physically tested competition controllers must be present in `src/` or otherwise clearly documented as an external dependency.

| File | Purpose |
|---|---|
| `src/N_Vision_final.py` | Final multi-ROI computer vision for walls, pillars and course colours |
| `src/Final_Obstacle_Challenge.py` | Main Obstacle Challenge controller |
| `src/Sentio_Open_2026.py` | Main Open Challenge controller |
| `src/openvision.py` | Primary Open Challenge vision module |
| `src/TOF_22.py` | Three-VL53L0X initialization, XSHUT sequencing and distance interface |
| `src/drive.py` | Motor PWM, motor direction, steering and encoder-assisted movement interface |
| `src/parking_final.py` | Direction-dependent parking entry and final parallel-parking routine |
| `src/heading.py` | MPU6050 calibration and relative heading calculation |
| `src/Cal_APOC.py` | LAB / HSV field-calibration tool |
| `src/servo_test.py` | Steering direction, center and travel testing |
| `src/encoder_test.py` | Motor-encoder and movement-control testing |
| `src/TUF_test.py` | Three-sensor VL53L0X distance-system testing |

The final repository must also contain every local module imported by these programs.

A file that exists only on the Raspberry Pi but is missing from GitHub makes the repository incomplete.

---

# 2. Software Architecture

The current architecture separates:

```text
PERCEPTION
    ↓
STATE / NAVIGATION
    ↓
MOTION REQUEST
    ↓
DRIVE + STEERING
```

Sensor information comes from:

```text
DUAL CAMERAS
→ walls, pillars, track colours and parking geometry

MPU6050
→ relative heading

MOTOR ENCODER
→ shaft rotation and movement feedback

3 × VL53L0X
→ short-range distance information
```

These observations are combined by the challenge controllers.

---

# 3. Open Challenge Architecture

The current Open Challenge controller is:

```text
src/Sentio_Open_2026.py
```

Its primary vision module is:

```text
src/openvision.py
```

The complete multi-ROI module:

```text
src/N_Vision_final.py
```

can also provide compatible visual information where used by the current controller.

Conceptual dependency structure:

```text
Sentio_Open_2026.py
│
├── openvision.py
│   ├── OpenCV
│   ├── NumPy
│   └── Picamera2
│
├── drive.py
│   ├── motor control
│   ├── steering control
│   └── encoder feedback
│
└── course-state logic
```

The Open Challenge uses vision to determine:

```text
BLACK WALL GEOMETRY
BLUE COURSE CUES
ORANGE COURSE CUES
```

The controller repeatedly observes the track and applies wall-relative steering corrections.

Course-marker logic is also used to:

- establish direction;
- track course progress;
- prevent one visible marker from being counted repeatedly;
- determine completion of the required sequence.

---

# 4. Obstacle Challenge Architecture

The current Obstacle Challenge controller is:

```text
src/Final_Obstacle_Challenge.py
```

Conceptual dependency structure:

```text
Final_Obstacle_Challenge.py
│
├── N_Vision_final.py
│   ├── OpenCV
│   ├── NumPy
│   └── Picamera2
│
├── heading.py
│   └── MPU6050
│
├── drive.py
│   ├── motor control
│   ├── encoder
│   └── steering
│
└── parking_final.py
    ├── cameras
    ├── heading.py
    ├── TOF_22.py
    └── drive.py
```

The Obstacle Challenge combines:

```text
RED PILLARS
GREEN PILLARS
BLACK WALLS
BLUE COURSE CUES
ORANGE COURSE CUES
MAGENTA PARKING FEATURES
```

with:

```text
COURSE DIRECTION
HEADING
ENCODER MOVEMENT
PARKING STATE
```

The final behaviour is based on repeated sensing and state-dependent movement rather than one fixed sequence of timed turns.

---

# 5. Core Software Dependencies

| Dependency | Purpose |
|---|---|
| **Python 3** | Executes competition software |
| **OpenCV (`cv2`)** | Image processing, masking, morphology and contour analysis |
| **NumPy** | Image-array and numerical operations |
| **Picamera2** | Raspberry Pi Camera Module interface |
| **RPi.GPIO-compatible interface** | Motor, steering and other GPIO control |
| **SMBus / SMBus2** | I2C communication where used by heading and sensors |
| **VL53L0X-compatible Python interface** | Distance-sensor communication |

The exact package used for the final VL53L0X implementation must match the imports contained in the physically tested `TOF_22.py`, `TUF_test.py` and parking source.

Dependencies should not be added merely because they were used during experimentation.

Only software required by the submitted project should be listed as a competition dependency.

---

# 6. Raspberry Pi OS Packages

Begin with:

```bash
sudo apt update
sudo apt upgrade -y
```

Install the main Raspberry Pi software dependencies:

```bash
sudo apt install -y \
    git \
    python3-picamera2 \
    python3-opencv \
    python3-numpy \
    python3-smbus2 \
    i2c-tools
```

Additional Python packages required by the final VL53L0X implementation should be installed according to the imports used by the committed sensor source.

---

# 7. GPIO Support on Raspberry Pi 5

The drive software uses the Raspberry Pi GPIO interface.

Verify that the required namespace is available:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO import OK')"
```

On Raspberry Pi 5 systems where a compatible implementation is not already available:

```bash
sudo apt install -y python3-rpi-lgpio
```

If a conflicting classic implementation is installed:

```bash
sudo apt remove -y python3-rpi.gpio
sudo apt install -y python3-rpi-lgpio
```

Verify again:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO interface OK')"
```

The exact GPIO behaviour must match the software that was physically tested on Starlight.

---

# 8. Main GPIO Architecture

The published Starlight hardware baseline uses BCM numbering.

| Function | BCM GPIO |
|---|---:|
| Motor direction IN1 | GPIO5 |
| Motor direction IN2 | GPIO6 |
| Motor PWM | GPIO13 |
| Steering servo PWM | GPIO22 |
| Encoder A | GPIO17 |
| Encoder B | GPIO27 |
| I2C SDA | GPIO2 |
| I2C SCL | GPIO3 |
| ToF 1 XSHUT | GPIO16 |
| ToF 2 XSHUT | GPIO20 |
| ToF 3 XSHUT | GPIO21 |

The final source remains authoritative for any additional pins associated with:

- start button;
- status LED;
- auxiliary control lines.

Do not copy a GPIO assignment from an earlier robot revision without checking the final source.

---

# 9. Three VL53L0X Sensors

Starlight uses:

```text
3 × VL53L0X
```

These sensors provide short-range distance information during parking and other close-range manoeuvres.

All three devices share the I2C bus.

VL53L0X sensors begin with the same default I2C address, so they cannot simply be enabled simultaneously without address management.

The current system therefore uses three XSHUT control lines:

```text
GPIO16
GPIO20
GPIO21
```

Conceptually:

```text
ALL SENSORS OFF
      ↓
ENABLE SENSOR 1
      ↓
ASSIGN WORKING ADDRESS
      ↓
ENABLE SENSOR 2
      ↓
ASSIGN WORKING ADDRESS
      ↓
ENABLE SENSOR 3
      ↓
ASSIGN WORKING ADDRESS
      ↓
NORMAL DISTANCE READING
```

The current three-sensor interface is:

```text
src/TOF_22.py
```

The low-level test program is:

```text
src/TUF_test.py
```

Before running parking logic, verify that:

```text
Sensor 1 responds
Sensor 2 responds
Sensor 3 responds
Distances are plausible
Sensor identities remain separate
```

---

# 10. Camera Architecture

Starlight uses:

```text
2 × Raspberry Pi Camera Module 3 Wide
```

The cameras provide visual information for:

- wall detection;
- pillar detection;
- course-marker detection;
- parking geometry;
- terminal positioning.

The current Starlight camera architecture uses a fixed mechanical arrangement and task-specific image regions.

Both cameras should be visible to Raspberry Pi OS.

Verify using:

```bash
rpicam-hello --list-cameras
```

Both expected cameras should appear.

A camera being detected by Linux does not prove that it has the correct:

- position;
- orientation;
- camera index;
- field of view;
- calibration;
- image exposure.

These must also be checked on the physical robot.

---

# 11. Current Vision Geometry

The current multi-ROI architecture uses a:

```text
720 × 360
```

vision coordinate system.

Different regions of the frame are assigned different purposes.

Conceptually:

```text
┌───────────────────────────────────────────┐
│ L1      L2        C        R2       R1    │
│                                           │
│            COURSE COLOUR ROI              │
│                                           │
│              BODY EXCLUSION               │
└───────────────────────────────────────────┘
```

Typical region responsibilities include:

```text
L1 / R1
→ outer-wall geometry

L2 / R2
→ inner-wall geometry

C
→ center reference

O / B
→ orange / blue course information

BODY
→ excluded robot structure
```

The robot's own body can appear as a dark object.

Pixels corresponding to visible robot structure are therefore excluded from relevant wall-processing regions.

---

# 12. Current Vision Module

The final multi-ROI perception module is:

```text
src/N_Vision_final.py
```

The processing system uses combinations of:

- HSV information;
- LAB information;
- darkness thresholds;
- image location;
- contour area;
- contour geometry;
- region identity.

Conceptual pipeline:

```text
CAMERA FRAME
      ↓
COLOUR-SPACE CONVERSION
      ↓
ROI SELECTION
      ↓
MASK / THRESHOLD
      ↓
MORPHOLOGICAL FILTERING
      ↓
CONTOUR EXTRACTION
      ↓
AREA / GEOMETRY CHECK
      ↓
REGION-AWARE TARGET
      ↓
CONTROLLER
```

Vision should never be assumed to remain calibrated after a major change in:

- lighting;
- camera position;
- camera angle;
- exposure;
- chassis geometry;
- competition field material.

---

# 13. Field Calibration

The current calibration utility is:

```text
src/Cal_APOC.py
```

It supports interactive adjustment of the colour-processing ranges used by the final vision system.

Calibration should be performed using the actual field environment whenever practical.

The calibration workflow should verify:

```text
RED
GREEN
BLACK
BLUE
ORANGE
MAGENTA
```

before a final competition run.

A threshold that worked in the workshop should not automatically be assumed correct under different lighting.

---

# 14. MPU6050 Heading

Heading support is implemented in:

```text
src/heading.py
```

The MPU6050 communicates over I2C.

Enable I2C using:

```bash
sudo raspi-config
```

Then:

```text
Interface Options
→ I2C
→ Enable
```

Verify connected I2C devices:

```bash
i2cdetect -y 1
```

The heading sensor is normally expected at:

```text
0x68
```

The heading process conceptually performs:

```text
INITIALIZE
    ↓
MEASURE STATIONARY BIAS
    ↓
READ ANGULAR VELOCITY
    ↓
REMOVE BIAS
    ↓
INTEGRATE OVER TIME
    ↓
RELATIVE HEADING
```

Keep Starlight stationary during initial gyro calibration.

The heading estimate is a local relative reference.

It is not a drift-free global compass.

---

# 15. Motor Encoder

The current drive motor includes a quadrature encoder.

The encoder provides:

```text
shaft rotation
+
direction information
```

Encoder feedback is used during:

- drivetrain testing;
- movement verification;
- selected controlled movements;
- encoder-assisted challenge manoeuvres.

The dedicated test program is:

```text
src/encoder_test.py
```

Before relying on encoder movement:

```text
1. Rotate the drivetrain.
2. Confirm that counts change.
3. Confirm the expected direction sign.
4. Verify forward movement.
5. Verify reverse movement.
6. Check for stalled or inconsistent encoder response.
```

Encoder movement does not guarantee identical physical ground travel.

Wheel slip and drivetrain play remain possible.

---

# 16. Steering Test

The dedicated steering test is:

```text
src/servo_test.py
```

It should be used to verify:

```text
LEFT
CENTER
RIGHT
```

and to confirm:

- correct steering direction;
- center calibration;
- safe steering limits;
- linkage clearance;
- absence of binding.

Excessive steering travel can damage or disconnect the steering mechanism.

The physically tested steering calibration should therefore be treated as authoritative.

---

# 17. Parking Architecture

The current parking controller is:

```text
src/parking_final.py
```

Parking combines:

```text
CAMERA GEOMETRY
+
MPU6050 HEADING
+
3 × VL53L0X
+
DRIVE CONTROL
+
ACKERMANN STEERING
```

The terminal objective is to stop with Starlight aligned parallel to the magenta parking wall.

Because Starlight uses Ackermann steering, the vehicle cannot rotate about its center.

Parking therefore uses controlled:

```text
FORWARD ARCS
+
REVERSE ARCS
```

rather than differential-drive rotation.

---

# 18. Parking Distance Logic

The current parking design uses repeated short-range measurements rather than relying exclusively on fixed timing or camera position.

Conceptually:

```text
ENTER PARKING STATE
       ↓
ALLOW SENSOR ACTIVATION
       ↓
READ DISTANCE
       ↓
QUALIFY DETECTION
       ↓
WAIT / COOLDOWN
       ↓
CONFIRM SECOND DETECTION
       ↓
CONTINUE PARKING MANOEUVRE
       ↓
RANGE-BASED STOP
```

This reduces the chance that one transient short-distance reading immediately terminates a movement.

The actual thresholds, delays and sensor identities must come from the physically tested source.

---

# 19. Clockwise and Anticlockwise Parking

The final architecture supports both course directions.

Conceptually:

```text
               COURSE COMPLETE
                      │
              DETERMINE DIRECTION
                 ┌─────┴─────┐
                 │           │
                CW          ACW
                 │           │
           CW POSITION     U-TURN
                 │           │
                 │      FOLLOW WALL
                 │           │
                 │     OPPOSITE CORNER
                 └─────┬─────┘
                      │
             SHARED FINAL PARKING
                      │
              PARALLEL FINAL STOP
```

The anticlockwise route changes how Starlight reaches the parking entry.

The final parking routine is shared once the appropriate entry condition is reached.

---

# 20. Dependency Verification

After installation, verify the main software dependencies:

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
print("GPIO: OK")
print("Picamera2: OK")
print("Team Sentio dependency check: PASS")
PY
```

The VL53L0X dependency should be verified against the imports used by the committed `TOF_22.py` and `TUF_test.py`. Do not substitute a different library merely because it supports the same sensor model.

---

# 21. Verify Local Team Sentio Modules

After the final source files are uploaded, run module-import checks from the repository root.

At minimum, confirm that the current competition modules can be imported without a missing local dependency.

The expected source set includes:

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

All local modules imported by these files must also be present and synchronized with the physically tested Raspberry Pi source.

If Python reports:

```text
ModuleNotFoundError
```

for a Team Sentio module, the repository is not yet reproducible.

---

# 22. Component-Test Sequence

Before executing a complete challenge controller, test the individual subsystems.

Recommended order:

```text
STEERING TEST
      ↓
MOTOR TEST
      ↓
ENCODER TEST
      ↓
CAMERA TEST
      ↓
VISION TEST
      ↓
MPU6050 TEST
      ↓
ToF TEST
      ↓
LOW-SPEED INTEGRATION
      ↓
OPEN / OBSTACLE TEST
      ↓
PARKING TEST
```

Relevant utilities:

```text
servo_test.py
encoder_test.py
TUF_test.py
Cal_APOC.py
heading.py
```

Testing individual components first makes faults easier to isolate.

---

# 23. Clean-Clone Reproduction

Clone the repository using:

```bash
git clone https://github.com/teamsentiorobotics-svg/World-Robot-Olympiad---Team-Sentio-.git
cd World-Robot-Olympiad---Team-Sentio-
```

Then verify the expected structure.

```text
.
├── README.md
├── CHANGELOG.md
├── requirements.md
├── .gitattributes
├── .gitignore
│
├── src/
├── docs/
├── Models/
├── schemes/
├── v-photos/
├── t-photos/
├── videos/
└── other/
```

The exact folder capitalization used by the final GitHub repository should remain consistent across documentation and links.

---

# 24. Reproduction Sequence

Recommended full software reproduction sequence:

```text
INSTALL RASPBERRY PI OS
        ↓
UPDATE SYSTEM
        ↓
INSTALL REQUIRED PACKAGES
        ↓
ENABLE I2C
        ↓
CLONE REPOSITORY
        ↓
VERIFY CAMERAS
        ↓
VERIFY MPU6050
        ↓
VERIFY 3 × VL53L0X
        ↓
VERIFY STEERING
        ↓
VERIFY MOTOR
        ↓
VERIFY ENCODER
        ↓
CALIBRATE VISION
        ↓
RUN LOW-SPEED TEST
        ↓
RUN OPEN CHALLENGE
        ↓
RUN OBSTACLE CHALLENGE
        ↓
VERIFY PARKING
```

Do not begin with a full-speed autonomous run on an unverified installation.

---

# 25. Physical Pre-Run Check

Before a complete competition run, verify:

```text
Battery secure
Battery charged
Correct polarity
Regulated Pi supply stable
Common electrical reference present
No exposed short-risk wiring
Motor mechanically free
Gears correctly engaged
Differential mechanically free
Steering linkage connected
Steering center correct
Steering limits safe
Encoder operational
Camera 1 operational
Camera 2 operational
Vision calibrated
MPU6050 operational
ToF 1 operational
ToF 2 operational
ToF 3 operational
Correct source revision loaded
```

A software test should not be used to compensate for an obvious mechanical or electrical fault.

---

# 26. Current Hardware / Software Relationship

The current Starlight architecture can be summarized as:

```text
2 × CAMERA MODULE 3 WIDE
            ↓
     MULTI-ROI VISION
            ↓
  WALL / PILLAR / COLOUR DATA
            │
            │
MPU6050 ────┤
            │
ENCODER ────┤
            │
3 × ToF ────┤
            ↓
     RASPBERRY PI 5
            ↓
     NAVIGATION STATE
            ↓
       DRIVE CONTROL
        ┌────┴────┐
        │         │
      MOTOR     SERVO
        │         │
        └────┬────┘
            ↓
     4WD + ACKERMANN
```

This architecture should remain consistent across:

```text
Engineering Journal
GitHub source
Wiring documentation
CAD
Physical robot
```

---

# 27. Requirements Versioning Policy

Dependencies and configuration values should not be invented retrospectively.

If an exact package version was not recorded from the physically tested Raspberry Pi environment, do not claim that an arbitrary version was used.

The final frozen release should ideally record:

```text
Python version
OpenCV version
NumPy version
Picamera2 version
GPIO implementation
SMBus implementation
VL53L0X library
Raspberry Pi OS version
```

using values obtained directly from the competition Raspberry Pi.

---

# 28. Record the Raspberry Pi Environment

Useful commands include:

```bash
python3 --version
```

```bash
python3 -c "import cv2; print(cv2.__version__)"
```

```bash
python3 -c "import numpy; print(numpy.__version__)"
```

```bash
uname -a
```

```bash
cat /etc/os-release
```

Package information can also be retained using:

```bash
python3 -m pip freeze
```

or:

```bash
dpkg -l
```

Do not blindly replace manually documented dependencies with the entire package list.

The final requirements should distinguish software required by Starlight from unrelated packages installed on the Raspberry Pi.

---

# 29. Record the Exact Git Revision

The exact source revision running on Starlight can be obtained using:

```bash
git rev-parse HEAD
```

Check for local modifications:

```bash
git status
```

A final competition Raspberry Pi should not contain undocumented code changes that are absent from GitHub.

The desired relationship is:

```text
PHYSICAL ROBOT
      =
RASPBERRY PI SOURCE
      =
GITHUB SOURCE
      =
DOCUMENTATION
```

---

# 30. Calibration Changes

Any change to the following may alter autonomous behaviour:

```text
steering center
steering limits
motor speed
proportional gain
camera position
camera angle
ROI position
HSV thresholds
LAB thresholds
pillar area threshold
wall target
marker logic
heading target
encoder target
ToF threshold
parking confirmation timing
```

After modifying one of these values, the robot should be physically tested again before that source revision is identified as a final competition release.

---

# 31. Reproducibility Requirement

The GitHub repository must not rely on:

```text
an undocumented Python module
an uncommitted calibration file
a hidden Raspberry Pi script
a locally edited dependency
an unrecorded CAD component
an unknown wiring change
```

that exists only on the original Starlight robot.

Everything required to reproduce the submitted configuration should be present in or clearly referenced by the repository.

---

# 32. Related Project Files

| Resource | Location |
|---|---|
| Main project overview | `README.md` |
| Development history | `CHANGELOG.md` |
| Engineering Journal | `ENGINEERING_JOURNAL.pdf` |
| Raspberry Pi setup | `docs/pi_setup_instruction.md` |
| Software dependencies | `docs/Software_Dependencies.md` |
| Bill of materials | `docs/BOM_purchase_links.md` |
| Wiring guide | `docs/wiring_guide.md` |
| Differential background | `docs/differential_drive_system.md` |
| Final multi-ROI vision | `src/N_Vision_final.py` |
| Open Challenge | `src/Sentio_Open_2026.py` |
| Open vision | `src/openvision.py` |
| Drive / steering / encoder interface | `src/drive.py` |
| Three-ToF interface | `src/TOF_22.py` |
| Obstacle Challenge | `src/Final_Obstacle_Challenge.py` |
| Parking | `src/parking_final.py` |
| Heading | `src/heading.py` |
| Colour calibration | `src/Cal_APOC.py` |
| Steering test | `src/servo_test.py` |
| Encoder test | `src/encoder_test.py` |
| ToF test | `src/TUF_test.py` |
| Electrical documentation | `schemes/` |
| CAD / printable models | `Models/` |
| Vehicle photographs | `v-photos/` |
| Team photographs | `t-photos/` |
| Autonomous video evidence | `videos/` |

---

# 33. Final Software Freeze Checklist

Before identifying the GitHub repository as the final competition release:

```text
[ ] Final Open controller uploaded
[ ] Final Obstacle controller uploaded
[ ] Final parking controller uploaded
[ ] Final drive-control module (`drive.py`) uploaded
[ ] Final three-ToF interface (`TOF_22.py`) uploaded
[ ] Final multi-ROI vision uploaded
[ ] Open vision uploaded
[ ] heading.py uploaded
[ ] Cal_APOC.py uploaded
[ ] servo_test.py uploaded
[ ] encoder_test.py uploaded
[ ] TUF_test.py uploaded

[ ] All local imports resolve

[ ] Both cameras work
[ ] MPU6050 works
[ ] Encoder works
[ ] ToF 1 works
[ ] ToF 2 works
[ ] ToF 3 works
[ ] Steering works
[ ] Drive motor works

[ ] Vision calibration verified
[ ] Open Challenge tested
[ ] Obstacle Challenge tested
[ ] Parking tested

[ ] Raspberry Pi has no undocumented local changes
[ ] GitHub matches Raspberry Pi
[ ] Documentation matches GitHub
[ ] Engineering Journal matches final configuration
```

---

# Final Software Principle

A reproducible robotics project requires more than the primary challenge program.

The final Starlight release must preserve:

```text
SOURCE CODE
     +
DEPENDENCIES
     +
CALIBRATION
     +
HARDWARE INTERFACES
     +
TEST PROGRAMS
     +
CAD
     +
WIRING
     +
DOCUMENTATION
```

The repository should therefore allow another technically competent person to understand how Starlight is built, how its software is installed, how each subsystem is verified and which exact configuration produced the documented competition behaviour.

---

**Team Sentio**  
**Starlight**  
**World Robot Olympiad — Future Engineers 2026**  
**Robofun Lab (RFL), India**
