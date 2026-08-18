# Software Requirements

## Team Sentio — WRO Future Engineers 2026

This document records the software dependencies required to reproduce and run **Team Sentio's WRO Future Engineers 2026 autonomous vehicle software**.

The repository uses Raspberry Pi OS system packages for Raspberry Pi-specific libraries. Detailed installation, configuration and verification instructions are provided in the [`docs/Raspberry_Pi_Setup.md`](docs/Raspberry_Pi_Setup.md) guide.

---

## Platform

| Component | Specification |
|---|---|
| **Computer** | Raspberry Pi 5, 4 GB |
| **Operating System** | Raspberry Pi OS |
| **Programming Language** | Python 3 |
| **Camera Interface** | Picamera2 |
| **GPIO Interface** | RPi.GPIO-compatible interface |
| **I2C Interface** | SMBus2 |

---

## Competition Programs

The competition software is located in [`src/`](src/).

| File | Purpose |
|---|---|
| [`src/Open_Challenge.py`](src/Open_Challenge.py) | Autonomous Open Challenge navigation |
| [`src/Obstacle_Challenge.py`](src/Obstacle_Challenge.py) | Obstacle Challenge navigation and parking logic |
| [`src/heading.py`](src/heading.py) | MPU6050 heading calculation used by the Obstacle Challenge |

---

## Required Software Dependencies

| Dependency | Used For |
|---|---|
| **NumPy** | Numerical operations and image-array processing |
| **OpenCV** | Image processing, colour segmentation, contour detection and navigation geometry |
| **Picamera2** | Raspberry Pi Camera Module interface |
| **RPi.GPIO-compatible interface** | Motor-driver and steering-servo GPIO/PWM control |
| **SMBus2** | I2C communication with the MPU6050 IMU |
| **Python 3** | Execution of all competition software |

---

## Raspberry Pi OS Packages

The primary Raspberry Pi OS packages required by the software are:

```bash
sudo apt update

sudo apt install -y \
    python3-picamera2 \
    python3-opencv \
    python3-numpy \
    python3-smbus2 \
    i2c-tools
```

The competition code imports the GPIO interface using:

```python
import RPi.GPIO as GPIO
```

The Raspberry Pi environment must therefore provide a compatible `RPi.GPIO` interface.

Complete GPIO setup and Raspberry Pi 5 configuration instructions are provided in:

**[`docs/Raspberry_Pi_Setup.md`](docs/Raspberry_Pi_Setup.md)**

---

## Source Dependency Map

```text
Open_Challenge.py
│
├── OpenCV
├── NumPy
├── Picamera2
└── RPi.GPIO-compatible interface


Obstacle_Challenge.py
│
├── OpenCV
├── NumPy
├── Picamera2
├── RPi.GPIO-compatible interface
└── heading.py
    │
    └── SMBus2
        │
        └── MPU6050 IMU
```

---

## Python Standard Library

The competition programs also use modules included with Python, including:

```python
import time
from time import sleep
```

These modules are part of the Python standard library and do not require separate installation.

---

## Dependency Verification

After completing the Raspberry Pi setup, the software environment can be checked using:

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

The MPU6050 heading module can then be verified independently with:

```bash
python3 src/heading.py
```

---

## Dependency and Versioning Policy

Only dependencies used by the submitted competition source are documented here.

Exact package-version pins are not stated unless they have been retained and verified from the physically tested competition environment. Unverified version numbers are not introduced solely for documentation purposes.

If the competition source changes and introduces another third-party dependency, this file and the Raspberry Pi setup documentation must be updated before the new revision is identified as the final competition release.

The **exact physically validated source revision** remains the authoritative software release.

---

## Related Reproduction Files

| Resource | Location |
|---|---|
| Project overview | [`README.md`](README.md) |
| Raspberry Pi setup | [`docs/Raspberry_Pi_Setup.md`](docs/Raspberry_Pi_Setup.md) |
| Competition software | [`src/`](src/) |
| Electrical schematic | [`schemes/`](schemes/) |
| CAD and printable models | [`models/`](models/) |
| Vehicle photographs | [`v-photos/`](v-photos/) |
| Competition video | [`video/`](video/) |

---

**Team Sentio**  
**WRO Future Engineers 2026**  
Robofun Lab (RFL), India
