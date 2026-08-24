# Software Requirements

## Team Sentio — WRO Future Engineers 2026

This document records the software dependencies required to reproduce and run **Team Sentio's WRO Future Engineers 2026 autonomous vehicle, Starlight**.

The final competition software has been **physically tested on the robot and is working**. The complete working project package and its helper modules are retained in the GitHub repository.

Detailed Raspberry Pi configuration, GPIO, camera and I2C setup instructions are provided in:

**[`docs/pi_setup_instruction.md`](docs/pi_setup_instruction.md)**

---

## Platform

| Component | Specification |
|---|---|
| **Computer** | Raspberry Pi 5, 4 GB |
| **Operating System** | Raspberry Pi OS |
| **Programming Language** | Python 3 |
| **Front Camera Interface** | Picamera2 |
| **Rear Camera Interface** | Picamera2 |
| **GPIO Interface** | RPi.GPIO-compatible interface |
| **I2C Interface** | SMBus2 |
| **Vision Processing** | OpenCV + NumPy |

---

## Final Competition Software

The competition software and required helper modules are located in [`src/`](src/).

```text
src/
├── Open_Challenge.py
├── Obstacle_Challenge.py
├── drive.py
├── openVision.py
├── vision.py
├── heading.py
└── parking.py
```

| File | Purpose |
|---|---|
| [`src/Open_Challenge.py`](src/Open_Challenge.py)         | Autonomous Open Challenge controller                                    |
| [`src/Obstacle_Challenge.py`](src/Obstacle_Challenge.py) | Obstacle Challenge controller                                           |
| [`src/drive.py`](src/drive.py)                           | Motor and steering-servo control                                        |
| [`src/openVision.py`](src/openVision.py)                 | Open Challenge BLACK / BLUE / ORANGE computer vision                    |
| [`src/vision.py`](src/vision.py)                         | Obstacle Challenge RED / GREEN / BLACK / BLUE / ORANGE / MAGENTA vision |
| [`src/heading.py`](src/heading.py)                       | MPU6050 gyro calibration and heading calculation                        |
| [`src/parking.py`](src/parking.py)                       | Final dual-camera and MPU6050-assisted parking behaviour                |

All of these helper files are part of the working project package and must be present for clean-clone reproducibility.

---

## Required Software Dependencies

| Dependency | Used For |
|---|---|
| **Python 3**                      | Execution of all competition software                                   |
| **OpenCV (****`cv2`****)**        | Image processing, colour segmentation, contours and navigation geometry |
| **NumPy**                         | Image arrays, masks and numerical operations                            |
| **Picamera2**                     | Raspberry Pi Camera Module interface                                    |
| **RPi.GPIO-compatible interface** | Motor-driver PWM, motor direction and steering-servo control            |
| **SMBus2**                        | I2C communication with the MPU6050 IMU                                  |

No unnecessary software packages are listed as competition dependencies.

---

## Raspberry Pi OS Packages

The primary Raspberry Pi OS packages used by the project are:

```bash
sudo apt update

sudo apt install -y \
    python3-picamera2 \
    python3-opencv \
    python3-numpy \
    python3-smbus2 \
    i2c-tools
```

The drive module imports the GPIO interface using:

```python
import RPi.GPIO as GPIO
```

The Raspberry Pi environment must therefore provide a compatible `RPi.GPIO` interface.

Detailed Raspberry Pi installation and configuration instructions are available in:

[**`docs/pi_setup_instruction.md`**](docs/pi_setup_instruction.md)

---

# Software Dependency Map

## Open Challenge

The final Open Challenge uses:

```text
Open_Challenge.py
│
├── drive.py
│   │
│   └── RPi.GPIO-compatible interface
│
└── openVision.py
    │
    ├── OpenCV
    ├── NumPy
    └── Picamera2
```

The Open Challenge controller imports:

```python
import drive
import openVision as vision
```

`openVision.py` is intentionally separate from the Obstacle Challenge vision system.

It detects only:

```text
BLACK
BLUE
ORANGE
```

This keeps the Open Challenge vision pipeline focused on the colours actually required for wall following and direction / marker detection.

---

## Obstacle Challenge

The final Obstacle Challenge uses:

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
    └── drive.py
```

The Obstacle Challenge controller imports:

```python
from heading import MPU6050Heading
import drive
import vision
import parking
```

The Obstacle vision module detects:

```text
RED
GREEN
BLACK
BLUE
ORANGE
MAGENTA
```

The additional colour classes are required for pillar avoidance, course perception and parking-related features.

---

## Parking Dependencies

Parking is implemented separately in:

```text
src/parking.py
```

The parking system uses:

- the front Raspberry Pi camera,
- the rear Raspberry Pi camera,
- `vision.py`,
- `drive.py`,
- `heading.py`,
- MPU6050 heading information.

Both cameras use the Picamera2 interface.

The final parking behaviour has been **physically tested on Starlight and is working**.

---

## MPU6050 / Heading

The heading helper is located at:

```text
src/heading.py
```

It uses:

```python
import smbus2
import time
```

The module communicates with the MPU6050 over I2C and provides the:

```python
MPU6050Heading
```

class.

The software:

1. initializes the MPU6050,
2. calibrates the Z-axis gyro offset,
3. reads rotational velocity,
4. integrates the rotation over time,
5. maintains heading between `0°` and `360°`.

The heading system can be tested independently using:

```bash
python3 src/heading.py
```

The robot should remain completely still during the initial calibration period.

---

# Python Standard Library

The competition software also uses Python standard-library modules including:

```python
import time
from time import sleep
```

These are included with Python and do not require separate installation.

---

# Dependency Verification

After completing the Raspberry Pi setup, the main external software dependencies can be checked with:

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
print("RPi.GPIO-compatible interface: OK")
print("Team Sentio dependency check: PASS")
PY
```

The MPU6050 can then be checked separately with:

```bash
python3 src/heading.py
```

The competition modules should also be checked from the repository environment to confirm that all local imports resolve correctly.

For example:

```bash
cd src
python3 -c "import drive; import openVision; import vision; import heading; import parking; print('Team Sentio modules: PASS')"
```

---

# Clean-Clone Requirement

For another user to reproduce the final robot software, the repository must contain:

```text
src/
├── Open_Challenge.py
├── Obstacle_Challenge.py
├── drive.py
├── openVision.py
├── vision.py
├── heading.py
└── parking.py
```

A challenge program is not considered reproducible if it only works because a required helper module already exists locally on the team's Raspberry Pi.

Therefore:

- `drive.py` is required.
- `openVision.py` is required for the Open Challenge.
- `vision.py` is required for the Obstacle Challenge.
- `heading.py` is required for MPU6050 operation.
- `parking.py` is required for the final parking stage.

These files have been included with the final project package.

---

# Final Validation Status

At the final project stage:

- **Open Challenge has been physically tested and is working.**
- **Obstacle Challenge has been physically tested and is working.**
- **Parking has been physically tested and is working.**
- Required helper modules are included.
- The project package has been pushed to GitHub.
- CAD / STL, documentation and supporting evidence are retained in the repository.

The GitHub repository should remain synchronized with the software running on the physical robot.

If a last-minute competition calibration changes any threshold, gain, steering value, speed or timing parameter, the updated source should also be committed and pushed.

---

# Dependency and Versioning Policy

Only dependencies actually used by the submitted competition software are documented here.

Exact package versions are not invented when the precise versions from the physically tested Raspberry Pi environment have not been retained.

The physically validated source and its working Raspberry Pi environment remain the authoritative reference.

If future code changes introduce another third-party dependency:

1. install and test the dependency on the physical robot,
2. update this document,
3. update the Raspberry Pi setup instructions,
4. retest the affected competition program,
5. commit and push the change.

The final Git revision can be identified using:

```bash
git rev-parse HEAD
```

---

# Related Reproduction Files

| Resource | Location |
|---|---|
| Project overview         | [`README.md`](README.md)                                       |
| Software requirements    | [`requirements.md`](requirements.md)                           |
| Raspberry Pi setup       | [`docs/pi_setup_instruction.md`](docs/pi_setup_instruction.md) |
| Open Challenge           | [`src/Open_Challenge.py`](src/Open_Challenge.py)               |
| Open vision              | [`src/openVision.py`](src/openVision.py)                       |
| Obstacle Challenge       | [`src/Obstacle_Challenge.py`](src/Obstacle_Challenge.py)       |
| Obstacle vision          | [`src/vision.py`](src/vision.py)                               |
| Motor / steering control | [`src/drive.py`](src/drive.py)                                 |
| MPU6050 heading          | [`src/heading.py`](src/heading.py)                             |
| Parking controller       | [`src/parking.py`](src/parking.py)                             |
| Electrical schematic     | [`schemes/`](schemes/)                                         |
| CAD and printable models | [`models/`](models/)                                           |
| Vehicle photographs      | [`v-photos/`](v-photos/)                                       |
| Team photographs         | [`t-photos/`](t-photos/)                                       |
| Competition videos       | [`video/`](video/)                                             |
| Supporting material      | [`other/`](other/)                                             |

---

**Team Sentio**
**Starlight**
**WRO Future Engineers 2026**
**Robofun Lab (RFL), India**
