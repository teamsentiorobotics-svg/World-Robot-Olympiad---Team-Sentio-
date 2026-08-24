# Software Requirements

## Team Sentio — WRO Future Engineers 2026

This document records the software environment and dependencies required to reproduce and run **Team Sentio's WRO Future Engineers 2026 autonomous vehicle, Starlight**.

**Platform:** Raspberry Pi 5, 4 GB  
**Operating System:** Raspberry Pi OS  
**Programming Language:** Python 3  
**Competition:** World Robot Olympiad 2026 — Future Engineers

The Open Challenge, Obstacle Challenge and Parking behaviours have been physically tested on Starlight and are working.

This file documents the software required by the final GitHub project and identifies the source modules on which the competition programs depend.

For complete Raspberry Pi installation and configuration instructions, see:

[`docs/pi_setup_instruction.md`](docs/pi_setup_instruction.md)

---

# 1. Current Competition Software

The current competition source is stored in:

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

| File | Purpose |
|---|---|
| [`src/open_challenge_final_ready_to_go.py`](src/open_challenge_final_ready_to_go.py) | Final Open Challenge autonomous controller |
| [`src/Obstacle_Challenge.py`](src/Obstacle_Challenge.py) | Final Obstacle Challenge controller |
| [`src/drive.py`](src/drive.py) | Motor and steering-servo GPIO/PWM control |
| [`src/openVision.py`](src/openVision.py) | Open Challenge BLACK / BLUE / ORANGE computer vision |
| [`src/vision.py`](src/vision.py) | Obstacle Challenge RED / GREEN / BLACK / BLUE / ORANGE / MAGENTA vision |
| [`src/heading.py`](src/heading.py) | MPU6050 gyro calibration and relative heading calculation |
| [`src/parking.py`](src/parking.py) | Dual-camera and MPU6050-assisted parking behaviour |

The helper modules are part of the competition software architecture and are required for reproducibility.

---

# 2. Software Architecture

## Open Challenge

The final Open Challenge executable is:

```text
src/open_challenge_final_ready_to_go.py
```

It imports:

```python
import drive
import openVision as vision
```

Dependency structure:

```text
open_challenge_final_ready_to_go.py
│
├── drive.py
│   └── RPi.GPIO-compatible interface
│
└── openVision.py
    ├── OpenCV
    ├── NumPy
    └── Picamera2
```

`openVision.py` is intentionally separate from the complete Obstacle Challenge vision system.

The Open Challenge requires detection of:

```text
BLACK
BLUE
ORANGE
```

This keeps the Open Challenge perception pipeline focused on the visual information required for wall following, direction detection and course-marker counting.

---

## Obstacle Challenge

The final Obstacle Challenge executable is:

```text
src/Obstacle_Challenge.py
```

It imports:

```python
from heading import MPU6050Heading
import drive
import vision
import parking
```

Dependency structure:

```text
Obstacle_Challenge.py
│
├── drive.py
│   └── RPi.GPIO-compatible interface
│
├── vision.py
│   ├── OpenCV
│   ├── NumPy
│   └── Picamera2
│
├── heading.py
│   └── SMBus2
│       └── MPU6050 IMU
│
└── parking.py
    ├── Picamera2
    ├── vision.py
    ├── heading.py
    └── drive-control module
```

The full Obstacle Challenge vision module detects:

```text
RED
GREEN
BLACK
BLUE
ORANGE
MAGENTA
```

Red and green are used for pillar navigation, black provides wall geometry, and the remaining colour information supports course and parking behaviour.

---

# 3. Core External Dependencies

| Dependency | Purpose |
|---|---|
| **Python 3** | Executes all competition software |
| **OpenCV (`cv2`)** | Image processing, masks, morphology, contour detection and navigation geometry |
| **NumPy** | Image-array and numerical operations |
| **Picamera2** | Raspberry Pi Camera Module interface |
| **RPi.GPIO-compatible interface** | Motor-driver and steering-servo GPIO/PWM control |
| **SMBus2** | I2C communication with the MPU6050 IMU |

The project deliberately avoids listing packages that are not used by the competition source.

---

# 4. Raspberry Pi OS Packages

The primary Raspberry Pi OS packages required by Starlight are:

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

These packages provide the Raspberry Pi-specific camera and I2C interfaces as well as the main computer-vision dependencies.

---

# 5. GPIO Support on Raspberry Pi 5

The drive code imports GPIO using:

```python
import RPi.GPIO as GPIO
```

The Raspberry Pi environment must therefore provide a compatible `RPi.GPIO` namespace.

First test:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO import OK')"
```

On Raspberry Pi 5 systems where a compatible implementation is not already installed, use:

```bash
sudo apt install -y python3-rpi-lgpio
```

If the classic `python3-rpi.gpio` package conflicts with the Raspberry Pi 5 compatibility implementation:

```bash
sudo apt remove -y python3-rpi.gpio
sudo apt install -y python3-rpi-lgpio
```

Do not intentionally maintain two conflicting implementations providing the same `RPi.GPIO` namespace.

Verify again:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO interface OK')"
```

---

# 6. GPIO Architecture

The current competition hardware uses BCM numbering.

| Function | BCM GPIO |
|---|---:|
| Motor driver IN1 | GPIO5 |
| Motor driver IN2 | GPIO6 |
| Motor PWM | GPIO13 |
| Steering servo PWM | GPIO22 |
| I2C SDA | GPIO2 |
| I2C SCL | GPIO3 |

The motor PWM frequency implemented in `drive.py` is:

```text
1000 Hz
```

The steering servo PWM frequency is:

```text
50 Hz
```

The source file:

```text
src/drive.py
```

is the authoritative reference for the steering calibration actually used by the current software.

---

# 7. Camera Dependencies

Starlight uses two Raspberry Pi Camera Module 3 units.

## Front Camera

The front camera is used for:

- black wall perception,
- blue/orange marker detection,
- red/green pillar detection,
- obstacle navigation,
- front parking geometry.

The Open Challenge vision module initializes the front camera through:

```python
from picamera2 import Picamera2
```

The current Open vision configuration uses:

```text
Resolution: 1480 × 520
Format:     RGB888
Requested FPS: 60
```

---

## Rear Camera

The rear camera is used during parking.

The parking system uses a second Picamera2 camera and combines rear-camera information with MPU6050 heading feedback.

Both connected cameras should be verified using:

```bash
rpicam-hello --list-cameras
```

---

# 8. Computer Vision Dependencies

## Open Challenge

The Open Challenge uses:

```text
src/openVision.py
```

Main Python dependencies:

```python
import cv2
import numpy as np
import time
from picamera2 import Picamera2
```

The module detects:

```text
BLACK
BLUE
ORANGE
```

---

## Obstacle Challenge

The Obstacle Challenge uses:

```text
src/vision.py
```

Main Python dependencies:

```python
import cv2
import numpy as np
import time
from picamera2 import Picamera2
```

The full vision module detects:

```text
RED
GREEN
BLACK
BLUE
ORANGE
MAGENTA
```

The final obstacle-vision architecture combines colour and geometric information rather than using colour alone.

---

# 9. MPU6050 / Heading Dependency

The heading helper is:

```text
src/heading.py
```

It provides the:

```python
MPU6050Heading
```

class.

The main external dependency is:

```python
import smbus2
```

The MPU6050 communicates through Raspberry Pi I2C.

Enable I2C using:

```bash
sudo raspi-config
```

Then navigate to:

```text
Interface Options
→ I2C
→ Enable
```

After rebooting, verify the bus:

```bash
i2cdetect -y 1
```

The MPU6050 used by the project is expected at:

```text
0x68
```

The heading module can be tested using:

```bash
python3 src/heading.py
```

Keep the robot completely stationary during initial gyro calibration.

---

# 10. Parking Dependencies

Parking is implemented in:

```text
src/parking.py
```

The parking architecture uses:

- front camera,
- rear camera,
- OpenCV,
- NumPy,
- Picamera2,
- `vision.py`,
- `heading.py`,
- MPU6050,
- drive control.

The final parking behaviour has been physically tested on Starlight and is working.

---

## Important Clean-Clone Dependency Check

The current GitHub version of:

```text
src/parking.py
```

must be checked against the physically tested Raspberry Pi copy before the repository is permanently frozen.

If the tested parking source imports:

```python
import robot_drive as drive
```

then the corresponding:

```text
robot_drive.py
```

must also be included in `src/`.

If the physically tested version instead uses the existing:

```text
src/drive.py
```

then the parking import and the repository must remain synchronized with that tested version.

A GitHub repository is not considered completely reproducible if a helper module exists only on the team's Raspberry Pi and is absent from the repository.

The **physically tested Raspberry Pi source should be treated as authoritative** when resolving this dependency.

---

# 11. Python Standard Library

The competition software also uses standard Python modules such as:

```python
import time
from time import sleep
```

These are included with Python 3 and do not require separate installation.

Other standard-library imports may include modules used for normal Python program control.

They are not listed as external dependencies.

---

# 12. Dependency Verification

After completing the Raspberry Pi setup, verify the main third-party dependencies with:

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

---

# 13. Verify Local Team Sentio Modules

From the repository root:

```bash
cd src
```

Verify the main helper modules:

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

Parking should then be checked separately because its drive-control import must match the exact physically tested source:

```bash
python3 -c "import parking; print('parking.py: OK')"
```

If this command produces:

```text
ModuleNotFoundError: No module named 'robot_drive'
```

the repository and physically tested Raspberry Pi dependency set are not yet synchronized.

Resolve that mismatch before the final GitHub freeze.

---

# 14. Current Open Challenge Configuration

The current committed Open Challenge executable is:

```text
src/open_challenge_final_ready_to_go.py
```

Key current software settings include:

```text
LINE_COOLDOWN     = 1.3 s
TOTAL_LINES       = 12
KP                = 0.013
START_SPEED       = 40
TARGET_SPEED      = 100
ACCELERATION_TIME = 2.0 s
```

The current Open Challenge code imports:

```python
import drive
import openVision as vision
```

The first valid course information is used to establish driving direction rather than permanently hard-coding one direction at startup.

The actual source file remains authoritative for competition calibration.

---

# 15. Current Obstacle Challenge Configuration

The current committed Obstacle Challenge executable is:

```text
src/Obstacle_Challenge.py
```

It imports:

```python
from heading import MPU6050Heading
import drive
import vision
import parking
```

Current main settings include:

```text
total_lap            = 3
rs                   = 45
KP                   = 0.014
OBSTACLE_ACTION_AREA = 18000
```

The actual physically tested source remains authoritative for all final field-calibration values.

---

# 16. Clean-Clone Reproduction Requirement

A clean reproduction should begin with:

```bash
git clone https://github.com/teamsentiorobotics-svg/World-Robot-Olympiad---Team-Sentio-.git
cd World-Robot-Olympiad---Team-Sentio-
```

The expected competition source should include:

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

If an additional drive-control file is required by the physically tested parking code, that file must also be present.

The repository should never depend on an undocumented Python file that exists only on the original Raspberry Pi.

---

# 17. Reproduction Sequence

Recommended software reproduction sequence:

```text
Install Raspberry Pi OS
        ↓
Update system packages
        ↓
Install OpenCV / NumPy / Picamera2 / SMBus2
        ↓
Install compatible GPIO support
        ↓
Enable I2C
        ↓
Verify MPU6050
        ↓
Verify front and rear cameras
        ↓
Clone repository
        ↓
Verify external Python dependencies
        ↓
Verify local source modules
        ↓
Test drive system safely
        ↓
Test vision modules
        ↓
Test heading module
        ↓
Run Open Challenge
        ↓
Run Obstacle Challenge
        ↓
Validate parking
```

---

# 18. Versioning Policy

Only dependencies actually used by the submitted competition software are documented here.

Exact package versions are not invented when they have not been retained and verified from the physically tested Raspberry Pi environment.

The following should remain synchronized:

```text
Physical robot
      =
Raspberry Pi source
      =
GitHub source
      =
Documentation
```

If a field-calibration change modifies:

- steering,
- speed,
- KP,
- image thresholds,
- marker cooldown,
- parking timing,
- camera mapping,
- IMU logic,

the changed source should be physically tested again before it is identified as the final competition release.

---

# 19. Record the Exact Git Revision

The current Git revision can be obtained using:

```bash
git rev-parse HEAD
```

Check for local Raspberry Pi modifications using:

```bash
git status
```

A clean final competition setup should not contain undocumented local source changes that are absent from GitHub.

---

# 20. Related Reproduction Files

| Resource | Location |
|---|---|
| Main project overview | [`README.md`](README.md) |
| Development history | [`CHANGELOG.md`](CHANGELOG.md) |
| Raspberry Pi setup | [`docs/pi_setup_instruction.md`](docs/pi_setup_instruction.md) |
| Detailed software dependencies | [`docs/Software_Dependencies.md`](docs/Software_Dependencies.md) |
| Final Open Challenge | [`src/open_challenge_final_ready_to_go.py`](src/open_challenge_final_ready_to_go.py) |
| Obstacle Challenge | [`src/Obstacle_Challenge.py`](src/Obstacle_Challenge.py) |
| Drive control | [`src/drive.py`](src/drive.py) |
| Open vision | [`src/openVision.py`](src/openVision.py) |
| Obstacle vision | [`src/vision.py`](src/vision.py) |
| MPU6050 heading | [`src/heading.py`](src/heading.py) |
| Parking | [`src/parking.py`](src/parking.py) |
| Electrical schematic | [`schemes/`](schemes/) |
| CAD / printable models | [`models/`](models/) |
| Vehicle photographs | [`v-photos/`](v-photos/) |
| Team photographs | [`t-photos/`](t-photos/) |
| Autonomous video evidence | [`video/`](video/) |
| Supporting engineering evidence | [`other/`](other/) |

---

# Final Software Status

At the final project stage:

- Open Challenge has been physically tested and is working.
- Obstacle Challenge has been physically tested and is working.
- Parking has been physically tested and is working.
- Separate Open and Obstacle computer-vision modules are retained.
- MPU6050 heading support is included.
- Raspberry Pi setup documentation is included.
- CAD, electrical documentation, photographs and testing evidence are included.
- The repository is intended to reproduce the complete Starlight system rather than only provide the main challenge files.

Before permanently freezing the GitHub repository, the remaining parking drive-module import should be checked against the exact working Raspberry Pi copy so that the GitHub dependency set is identical to the physically validated robot.

---

**Team Sentio**  
**Starlight**  
**World Robot Olympiad — Future Engineers 2026**  
**Robofun Lab (RFL), India**
