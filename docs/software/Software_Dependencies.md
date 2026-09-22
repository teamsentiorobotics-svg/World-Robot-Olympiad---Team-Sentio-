# Software Dependencies

## Team Sentio - WRO Future Engineers 2026

This document records the software environment, external dependencies, module structure, calibration tools, and reproducibility requirements used by **Team Sentio's autonomous vehicle, Starlight** for **World Robot Olympiad 2026 - Future Engineers**.

The dependency record follows the current **Revision 27 competition architecture**.

| Item | Current Configuration |
| --- | --- |
| **Computer** | Raspberry Pi 5, 4 GB |
| **Operating System** | Raspberry Pi OS |
| **Programming Language** | Python 3 |
| **Camera Interface** | Picamera2 |
| **Computer Vision** | OpenCV + NumPy |
| **GPIO Interface** | RPi.GPIO-compatible interface |
| **I2C Interface** | SMBus2 / device-specific sensor interface |
| **Cameras** | 2 × Raspberry Pi Camera Module 3 Wide |
| **Heading Sensor** | MPU6050 |
| **Distance Sensors** | 3 × VL53L0X ToF sensors |
| **Drive Feedback** | Motor encoder |
| **Vision Architecture** | Multi-ROI HSV/LAB processing with body exclusion |
| **Competition Status** | Open, Obstacle and Parking systems physically tested |

> [!IMPORTANT]
> The source running on the physically tested robot is the authoritative competition version.
>
> GitHub, the Raspberry Pi, calibration values, wiring documentation, and engineering journal should remain synchronized whenever the competition configuration changes.

For complete Raspberry Pi installation and wiring information, also see:

- [`pi_setup_instruction.md`](pi_setup_instruction.md)
- [`wiring_guide.md`](wiring_guide.md)
- [`BOM_purchase_links.md`](BOM_purchase_links.md)
- [`testing.md`](testing.md)

---

# Competition Software

The current competition software is stored in the [`src/`](../src/) directory.

The Rev27 software architecture uses the following principal files:

```text
src/
├── Sentio_Open_2026.py
├── Final_Obstacle_Challenge.py
├── N_Vision_final.py
├── openvision.py
├── parking_final.py
├── heading.py
├── Cal_APOC.py
├── servo_test.py
├── encoder_test.py
└── TUF_test.py
```

The low-level drive interface used by the physically tested challenge programs must also be present in `src/`.

Its exact filename should match the imports in the final Raspberry Pi source.

---

## Module Responsibilities

| File | Responsibility |
| --- | --- |
| [`Sentio_Open_2026.py`](../src/Sentio_Open_2026.py) | Open Challenge wall following, direction logic and course progress |
| [`Final_Obstacle_Challenge.py`](../src/Final_Obstacle_Challenge.py) | Obstacle selection, course state and movement decisions |
| [`N_Vision_final.py`](../src/N_Vision_final.py) | Final multi-ROI vision for walls, pillars, markers and parking cues |
| [`openvision.py`](../src/openvision.py) | Primary lightweight Open Challenge vision implementation |
| [`parking_final.py`](../src/parking_final.py) | Direction-dependent parking entry and final parallel-parking behaviour |
| [`heading.py`](../src/heading.py) | MPU6050 calibration and shared relative-heading estimate |
| [`Cal_APOC.py`](../src/Cal_APOC.py) | Field calibration of LAB and HSV colour thresholds |
| [`servo_test.py`](../src/servo_test.py) | Steering centre, direction and mechanical-travel testing |
| [`encoder_test.py`](../src/encoder_test.py) | Encoder direction, response and movement testing |
| [`TUF_test.py`](../src/TUF_test.py) | VL53L0X distance-sensor communication and ranging tests |

The current architecture deliberately separates:

```text
Perception
    ↓
State / decision logic
    ↓
Movement request
    ↓
Drive / steering / encoder interface
    ↓
Changed physical state
    ↓
New sensor observation
```

This makes individual faults easier to isolate than placing every behaviour inside one large script.

---

# Software Architecture

## Open Challenge

The current Open Challenge controller is:

```text
src/Sentio_Open_2026.py
```

The primary vision module is:

```text
src/openvision.py
```

The architecture also allows the final multi-ROI vision module:

```text
src/N_Vision_final.py
```

to be used where its returned observations remain compatible with the controller.

Conceptually:

```text
Sentio_Open_2026.py
│
├── openvision.py
│   ├── OpenCV
│   ├── NumPy
│   └── Picamera2
│
├── optional N_Vision_final.py compatibility
│   ├── OpenCV
│   ├── NumPy
│   └── Picamera2
│
└── drive interface
    ├── GPIO motor control
    ├── steering control
    └── encoder-assisted movement
```

The Open Challenge performs continuous wall correction while separately tracking discrete course events.

A visible course marker may remain in the camera for several frames, so progress detection uses state and cooldown logic rather than counting every frame independently.

---

## Obstacle Challenge

The current Obstacle Challenge controller is:

```text
src/Final_Obstacle_Challenge.py
```

Its high-level architecture is:

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
├── parking_final.py
│   ├── camera information
│   ├── heading information
│   ├── ToF distance information
│   └── movement control
│
└── drive interface
    ├── DC motor
    ├── steering servo
    └── encoder
```

The controller combines:

- red / green pillar observations;
- outer-wall observations;
- inner-wall observations;
- centre-region observations;
- course direction;
- current state;
- heading feedback;
- encoder-assisted movement;
- parking cues;
- short-range distance measurements.

A detected object is therefore **not automatically a movement command**.

Its meaning depends on:

```text
Colour
+
Image region
+
Geometry
+
Course direction
+
Current state
```

---

# External Software Dependencies

The principal external software components are:

| Dependency | Purpose |
| --- | --- |
| **Python 3** | Executes competition and test software |
| **OpenCV (`cv2`)** | Colour processing, masks, morphology, contours and geometry |
| **NumPy** | Image arrays and numerical processing |
| **Picamera2** | Raspberry Pi camera interface |
| **RPi.GPIO-compatible interface** | Motor, steering and digital control |
| **SMBus2** | I2C communication used by the MPU6050 heading module |
| **VL53L0X driver used by final source** | Communication with the three ToF distance sensors |

> [!NOTE]
> The exact VL53L0X Python package must match the imports used by the physically tested `TUF_test.py` and `parking_final.py`.
>
> Do not document or install a different library merely because it supports the same sensor model.

The same rule applies to the encoder interface. The package or GPIO method documented here should match the final tested source rather than an earlier prototype.

---

# Raspberry Pi OS Packages

Install the principal Raspberry Pi OS packages with:

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
| --- | --- |
| `git` | Clone and synchronize the repository |
| `python3-picamera2` | Raspberry Pi camera interface |
| `python3-opencv` | Computer vision |
| `python3-numpy` | Numerical and image-array processing |
| `python3-smbus2` | I2C communication |
| `i2c-tools` | I2C device detection and diagnostics |

Any additional package required by the final ToF or encoder source should be installed according to the imports in that exact tested revision.

---

# Raspberry Pi 5 GPIO Compatibility

The low-level drive software uses an interface compatible with:

```python
import RPi.GPIO as GPIO
```

Test the environment with:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO import OK')"
```

On a Raspberry Pi 5 installation requiring the compatibility implementation:

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

Do not deliberately keep conflicting GPIO implementations that provide the same Python namespace.

---

# I2C Architecture

Starlight uses the Raspberry Pi I2C bus for multiple sensors.

The published baseline is:

```text
SDA: GPIO2
SCL: GPIO3
```

Enable I2C with:

```bash
sudo raspi-config
```

Then select:

```text
Interface Options
→ I2C
→ Enable
```

After rebooting:

```bash
i2cdetect -y 1
```

---

## MPU6050

The MPU6050 heading sensor is expected at:

```text
0x68
```

The shared heading helper is:

```text
src/heading.py
```

It:

1. opens communication with the MPU6050;
2. estimates stationary gyro bias;
3. reads angular rate;
4. compensates for the estimated bias;
5. integrates angular rate over time;
6. returns a relative heading.

Test with:

```bash
python3 src/heading.py
```

Keep Starlight completely stationary during initial calibration.

The heading estimate is a **local relative reference**, not a drift-free global compass.

---

# Three VL53L0X Distance Sensors

Starlight uses:

```text
3 × VL53L0X
```

The sensors share the I2C bus.

Because identical VL53L0X sensors initially use the same default I2C address, they must be enabled individually before assigning separate working addresses.

The current hardware uses three XSHUT lines:

```text
GPIO16
GPIO20
GPIO21
```

Conceptually:

```text
All ToF sensors disabled
        ↓
Enable sensor 1
        ↓
Assign unique address
        ↓
Enable sensor 2
        ↓
Assign unique address
        ↓
Enable sensor 3
        ↓
Assign unique address
        ↓
Read sensors independently
```

The low-level distance test is:

```text
src/TUF_test.py
```

Use it to verify:

- sensor communication;
- sensor identity;
- distance response;
- mounting direction;
- which physical surface each sensor observes.

A distance reading is useful only when the software knows **which sensor produced it and which physical gap it represents**.

---

# Motor Encoder

The current 600 RPM drive motor includes an encoder.

The encoder provides shaft-motion information used for:

- movement testing;
- repeatable movement requests;
- confirming motor response;
- reducing dependence on time-only movement.

The dedicated test is:

```text
src/encoder_test.py
```

Encoder calibration should establish:

```text
Count direction
Counts per shaft rotation
Motor response
Expected movement sign
```

Encoder feedback does **not** guarantee exact vehicle displacement.

Wheel slip, tire deformation and drivetrain compliance can cause body movement to differ from calculated shaft movement.

---

# Drive and Steering Interface

The final drive interface converts movement requests into:

```text
Motor direction
Motor PWM
Steering command
Encoder-assisted movement
```

Published baseline control connections include:

| Function | Interface |
| --- | --- |
| Motor direction | GPIO5 / GPIO6 |
| Motor PWM | GPIO13 |
| Motor PWM frequency | 1 kHz |
| Steering servo | GPIO22 |
| Steering PWM frequency | 50 Hz |

The exact final steering limits and speed values remain defined by the physically tested source.

Do not duplicate rapidly changing calibration constants in several documentation files.

---

# Camera Dependencies

Starlight uses:

```text
2 × Raspberry Pi Camera Module 3 Wide
```

The two cameras provide different useful views during navigation and parking.

The current camera geometry uses a viewing direction of approximately:

```text
60° from horizontal
```

This emphasizes:

- nearby track surface;
- pillar bases;
- wall geometry;
- course markers;
- parking cues.

The trade-off is reduced distant look-ahead and stronger perspective change as objects approach.

Camera pose is therefore treated as a **mechanical calibration parameter**, not merely a software setting.

---

## Camera Detection Test

List cameras:

```bash
rpicam-hello --list-cameras
```

Test camera 0:

```bash
rpicam-hello --camera 0 --timeout 3000
```

Test camera 1:

```bash
rpicam-hello --camera 1 --timeout 3000
```

Camera numbering, mounting position or orientation should not be changed immediately before competition without rerunning vision and parking tests.

---

# Current Vision Architecture

The final multi-purpose vision module is:

```text
src/N_Vision_final.py
```

The current vision configuration is based on approximately:

```text
Width:  720 px
Height: 360 px
```

The architecture uses multiple task-specific Regions of Interest rather than treating the complete camera frame as one detection region.

Conceptually:

```text
Camera frame
      ↓
Colour-space conversion
      ↓
HSV / LAB processing
      ↓
Task-specific ROIs
      ↓
Morphological filtering
      ↓
Contour extraction
      ↓
Area / shape checks
      ↓
Region-labelled observation
```

---

## Why Multiple ROIs Are Used

Different parts of the image answer different questions.

Typical roles include:

```text
Outer-wall region
Inner-wall region
Centre reference
Orange / blue course-cue region
Pillar regions
Parking-related regions
```

This reduces the chance that an unrelated object elsewhere in the frame is interpreted as the target required by the current driving state.

---

## Robot-Body Exclusion

The current camera position can include part of Starlight itself in the frame.

Dark chassis or wiring pixels could otherwise resemble track features.

The vision system therefore excludes the robot-body region from relevant detection processing.

Conceptually:

```text
Camera image
      ↓
Useful region?
   ↙       ↘
 YES        NO
 ↓           ↓
Process     Ignore
```

A vision threshold should not be expected to compensate for pixels that should never have been considered navigation information.

---

# HSV + LAB Colour Processing

The final vision system uses both:

```text
HSV
LAB
```

where useful.

HSV provides useful hue, saturation and brightness separation.

LAB provides another representation of colour and lightness that can improve distinction under changing field conditions.

The final detector also considers:

- contour area;
- contour geometry;
- confidence conditions;
- region identity;
- morphological noise removal.

A colour match alone is therefore not automatically accepted as a valid navigation object.

---

# Field Calibration

The field calibration utility is:

```text
src/Cal_APOC.py
```

It allows the team to adjust LAB and HSV ranges while viewing the actual camera image and mask.

Recommended workflow:

```text
Mount final camera
      ↓
Place robot on competition-style field
      ↓
Allow camera exposure to settle
      ↓
Show known target colour
      ↓
Adjust LAB / HSV ranges
      ↓
Check near and far observations
      ↓
Check neighbouring / competing colours
      ↓
Retain values with that camera configuration
```

Colour calibration is linked to:

- lighting;
- camera position;
- camera angle;
- exposure;
- white balance;
- physical field material.

Changing one of these conditions may require recalibration.

---

# Parking Dependencies

The final parking controller is:

```text
src/parking_final.py
```

Parking combines several different observations:

| Information | Source |
| --- | --- |
| Parking / wall geometry | Camera |
| Orientation | MPU6050 |
| Nearby physical gap | VL53L0X sensors |
| Vehicle movement | Encoder / drive interface |
| Steering state | Servo / drive interface |

No single sensor answers all of these questions.

---

## Parking Logic

The parking sequence combines:

```text
Approach
    ↓
Align
    ↓
Read distance
    ↓
Confirm
    ↓
Adjust
    ↓
Final distance condition
    ↓
Stop parallel to magenta wall
```

Distance confirmation uses repeated short-range observations rather than blindly acting on the first qualifying sample.

This helps reduce transitions caused by one transient reading.

---

## Heading and Distance Are Different

Heading answers:

```text
Which direction is the robot facing?
```

Distance answers:

```text
How large is the local gap?
```

A vehicle can have the correct heading while still being too close to a wall.

Likewise, a suitable gap does not prove the robot is parallel.

Parking therefore combines both measurements.

---

# Clockwise and Anticlockwise Parking

Clockwise and anticlockwise course completion do not place Starlight in identical positions.

The final architecture therefore uses direction-dependent entry logic.

Conceptually:

```text
CLOCKWISE
Course complete
      ↓
Clockwise entry position
      ↓
Shared parking routine
      ↓
Parallel stop
```

```text
ANTICLOCKWISE
Course complete
      ↓
Turning position / U-turn
      ↓
Wall following
      ↓
Opposite corner
      ↓
Shared parking routine
      ↓
Parallel stop
```

The final parking behaviour is shared after the robot reaches the corresponding entry condition.

---

# Calibration and Test Programs

The repository includes dedicated utilities so a subsystem can be tested before rerunning the complete challenge.

| Observed Problem | Test / Tool | Purpose |
| --- | --- | --- |
| Wrong colour mask | `Cal_APOC.py` | Verify LAB / HSV ranges against field lighting |
| Incorrect steering / binding | `servo_test.py` | Verify steering centre, direction and usable travel |
| Incorrect movement response | `encoder_test.py` | Verify count direction and encoder-controlled movement |
| Incorrect distance reading | `TUF_test.py` | Verify ToF communication and physical ranging |
| Heading drift / incorrect turn direction | `heading.py` | Verify stationary bias and controlled turning |

Recommended debugging sequence:

```text
Check power and wiring
        ↓
Run individual component test
        ↓
Verify subsystem at low speed
        ↓
Run integrated controller
        ↓
Run full challenge
        ↓
Record result
```

This prevents every robot failure from becoming a mysterious 500-line Python investigation.

---

# External Dependency Verification

Run:

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
print("Team Sentio core external dependency check: PASS")
PY
```

This verifies the principal general-purpose Python dependencies.

The ToF and encoder dependencies should also be tested using the actual competition source because their exact imports must match the physically tested implementation.

---

# Source Syntax Verification

From the repository root, the current source can be syntax-checked without executing a competition run:

```bash
python3 -m py_compile \
    src/Sentio_Open_2026.py \
    src/Final_Obstacle_Challenge.py \
    src/N_Vision_final.py \
    src/openvision.py \
    src/parking_final.py \
    src/heading.py \
    src/Cal_APOC.py \
    src/servo_test.py \
    src/encoder_test.py \
    src/TUF_test.py
```

If the low-level drive interface is stored as another Python file, include it in this check.

A syntax check does not prove that hardware communication or autonomous behaviour works.

Physical component and field testing are still required.

---

# Hardware Communication Verification

## I2C

```bash
i2cdetect -y 1
```

Check the MPU6050 and the ToF initialization procedure.

---

## Cameras

```bash
rpicam-hello --list-cameras
```

---

## Heading

```bash
python3 src/heading.py
```

---

## Steering

```bash
python3 src/servo_test.py
```

---

## Encoder

```bash
python3 src/encoder_test.py
```

---

## Distance Sensors

```bash
python3 src/TUF_test.py
```

---

## Vision Calibration

```bash
python3 src/Cal_APOC.py
```

The robot should not proceed directly from a fresh operating-system installation to a full-speed challenge run.

---

# Clean-Clone Reproducibility

A fresh clone begins with:

```bash
git clone https://github.com/teamsentiorobotics-svg/World-Robot-Olympiad---Team-Sentio-.git

cd World-Robot-Olympiad---Team-Sentio-
```

A reproducible competition repository should contain the complete source required by the robot.

At minimum, the current Rev27 software map includes:

```text
src/
├── Sentio_Open_2026.py
├── Final_Obstacle_Challenge.py
├── N_Vision_final.py
├── openvision.py
├── parking_final.py
├── heading.py
├── Cal_APOC.py
├── servo_test.py
├── encoder_test.py
├── TUF_test.py
└── [final drive interface]
```

There must not be a required helper module that exists only on the competition Raspberry Pi.

The reproducibility rule is:

```text
Physical robot configuration
        =
Raspberry Pi source
        =
GitHub source
        =
Documentation
```

---

# Repository Reproduction Workflow

A new installation should be approached in this order:

```text
1. Read README
2. Check BOM
3. Check wiring
4. Install Raspberry Pi dependencies
5. Verify GPIO and I2C
6. Verify both cameras
7. Verify steering
8. Verify encoder
9. Verify MPU6050
10. Verify all three ToF sensors
11. Calibrate vision
12. Run low-speed subsystem tests
13. Run Open Challenge
14. Run Obstacle Challenge
15. Run parking sequence
16. Record tested Git commit
```

Skipping straight from step 4 to step 13 is technically possible in the same way that jumping from a roof is technically a route to the ground.

---

# Final Configuration Principles

The software architecture reflects several retained engineering decisions.

| Earlier / Simpler Approach | Current Approach | Reason |
| --- | --- | --- |
| Broad visual detection | Multi-ROI perception | Reduce irrelevant detections |
| Threshold tuning alone | Camera geometry + calibration + ROI design | Perception depends on what the camera actually sees |
| Time-only precision movement | Encoder-assisted movement | Improve repeatability |
| Camera-only parking | Camera + heading + ToF | Add orientation and direct gap information |
| Single distance observation | Repeated confirmed observations | Reduce transient triggers |
| Fixed-time heading-sensitive turns | Gyro-assisted turn conditions | Observe orientation rather than assume it |
| Full-system debugging | Dedicated component tests | Isolate the failed subsystem |
| Earlier speed-focused drivetrain | 1:1 gearing + encoder | Prioritize torque, reliability and observable movement |

---

# Competition Calibration Policy

Do not copy tuning constants into multiple documentation files unless they are intentionally part of a frozen release.

Values such as:

```text
Steering center
Steering limits
Motor speed
Proportional gain
Colour thresholds
ROI coordinates
Marker cooldown
Distance thresholds
Encoder movement targets
Parking timing
Heading thresholds
```

can change during field calibration.

The final competition source remains authoritative for those values.

Whenever a competition calibration is changed:

1. update the Raspberry Pi source;
2. test the affected subsystem;
3. test the affected challenge;
4. commit the source;
5. push the tested revision;
6. update documentation if the architecture or interface changed.

---

# Git Revision

Record the exact revision with:

```bash
git rev-parse HEAD
```

Check for uncommitted changes:

```bash
git status
```

Before a competition repository freeze:

```text
git status
```

should not reveal an undocumented calibration or source modification that exists only on the Raspberry Pi.

---

# Evidence and Testing

Software dependency documentation establishes what is required to run the code.

It does **not** by itself prove that the robot performs correctly.

The engineering evidence should be separated into:

| Document | Purpose |
| --- | --- |
| `Software_Dependencies.md` | What software and interfaces are required |
| `testing.md` | How components and complete behaviours were tested |
| `engineering-decisions.md` | Why major design choices were made |
| `failure-log.md` | What failed, why it failed, and what changed |
| `CHANGELOG.md` | How the project changed across revisions |

Together these connect:

```text
Design choice
      ↓
Implementation
      ↓
Dependency
      ↓
Test
      ↓
Failure / observation
      ↓
Engineering change
      ↓
Retest
```

---

# Related Repository Files

For complete reproduction of Starlight, also refer to:

| Resource | Location |
| --- | --- |
| Main project overview | [`../README.md`](../README.md) |
| Development history | [`../CHANGELOG.md`](../CHANGELOG.md) |
| Raspberry Pi setup | [`pi_setup_instruction.md`](pi_setup_instruction.md) |
| Wiring guide | [`wiring_guide.md`](wiring_guide.md) |
| Bill of materials | [`BOM_purchase_links.md`](BOM_purchase_links.md) |
| Testing record | [`testing.md`](testing.md) |
| Engineering decisions | [`engineering-decisions.md`](engineering-decisions.md) |
| Failure log | [`failure-log.md`](failure-log.md) |
| Final Open Challenge | [`../src/Sentio_Open_2026.py`](../src/Sentio_Open_2026.py) |
| Final Obstacle Challenge | [`../src/Final_Obstacle_Challenge.py`](../src/Final_Obstacle_Challenge.py) |
| Final multi-ROI vision | [`../src/N_Vision_final.py`](../src/N_Vision_final.py) |
| Open Challenge vision | [`../src/openvision.py`](../src/openvision.py) |
| Parking | [`../src/parking_final.py`](../src/parking_final.py) |
| MPU6050 heading | [`../src/heading.py`](../src/heading.py) |
| Field calibration | [`../src/Cal_APOC.py`](../src/Cal_APOC.py) |
| Steering test | [`../src/servo_test.py`](../src/servo_test.py) |
| Encoder test | [`../src/encoder_test.py`](../src/encoder_test.py) |
| ToF test | [`../src/TUF_test.py`](../src/TUF_test.py) |
| Electrical schematic | [`../schemes/`](../schemes/) |
| CAD / printable components | [`../Models/`](../Models/) |
| Vehicle photographs | [`../v-photos/`](../v-photos/) |
| Team photographs | [`../t-photos/`](../t-photos/) |
| Video evidence | [`../videos/`](../videos/) |

> [!NOTE]
> If the repository still uses older filenames such as `engineering_decisions`, `models/`, or `video/`, update the links above to match the actual repository before committing this document.

---

# Final Validation Checklist

Before freezing the repository:

- [ ] Raspberry Pi boots without undervoltage warnings during normal operation
- [ ] GPIO interface imports correctly
- [ ] I2C is enabled
- [ ] MPU6050 responds correctly
- [ ] All three VL53L0X sensors initialize independently
- [ ] XSHUT sequencing works
- [ ] Encoder direction is correct
- [ ] Encoder movement test passes
- [ ] Steering centre and limits are verified
- [ ] Both cameras are detected
- [ ] Final camera mounts are secure
- [ ] Vision calibration matches field lighting
- [ ] Body exclusion matches the current camera geometry
- [ ] Open Challenge runs with the committed source
- [ ] Obstacle Challenge runs with the committed source
- [ ] Parking runs with the committed source
- [ ] No required helper file exists only on the Raspberry Pi
- [ ] `git status` shows no undocumented competition changes
- [ ] Tested Git commit hash is recorded

---

**Team Sentio 1747**  
**Starlight**  
**World Robot Olympiad - Future Engineers 2026**  
**Robofun Lab (RFL), India**
