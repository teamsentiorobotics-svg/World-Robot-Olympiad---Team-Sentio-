# 🧩 Software Dependencies

## Team Sentio — WRO Future Engineers 2026

This document records the software environment and Python dependencies used by **Team Sentio's Raspberry Pi 5 autonomous vehicle, Starlight**.

| Item | Configuration |
|---|---|
| **Platform** | Raspberry Pi 5 (4 GB) |
| **Operating System** | Raspberry Pi OS |
| **Language** | Python 3 |
| **Competition Status** | Final software physically tested and working |

> [!NOTE]
> The **Open Challenge**, **Obstacle Challenge**, and **Parking** software have all been tested on the physical robot. All required helper modules are included in the final GitHub project package.

---

## 🚗 Competition Software

The final competition software is located in the [`src/`](../src/) directory:

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
| [`Open_Challenge.py`](../src/Open_Challenge.py)         | Autonomous navigation for the Open Challenge                    |
| [`Obstacle_Challenge.py`](../src/Obstacle_Challenge.py) | Main Obstacle Challenge controller                              |
| [`drive.py`](../src/drive.py)                           | Motor and steering-servo control                                |
| [`openVision.py`](../src/openVision.py)                 | Open Challenge vision for BLACK, BLUE and ORANGE                |
| [`vision.py`](../src/vision.py)                         | Obstacle vision for RED, GREEN, BLACK, BLUE, ORANGE and MAGENTA |
| [`heading.py`](../src/heading.py)                       | MPU6050 heading calculation                                     |
| [`parking.py`](../src/parking.py)                       | Final dual-camera and IMU-assisted parking control              |

All required helper modules must remain in the repository for clean-clone reproducibility.

---

## 📦 Dependency Overview

The competition system uses the following software components:

| Dependency | Purpose |
|---|---|
| **NumPy**                         | Numerical operations and image-array processing                     |
| **OpenCV**                        | Computer vision, colour detection, contours and geometry processing |
| **Picamera2**                     | Raspberry Pi Camera Module interface                                |
| **RPi.GPIO-compatible interface** | Motor and steering GPIO/PWM control                                 |
| **SMBus2**                        | I2C communication with the MPU6050 IMU                              |
| **Python 3**                      | Main programming environment                                        |

The robot uses two Raspberry Pi cameras during the complete Obstacle/Parking sequence, while the Open Challenge uses the front camera.

---

## 🍓 Raspberry Pi-Specific Packages

Raspberry Pi-specific Python libraries are installed using the **Raspberry Pi OS package manager (`apt`)** rather than being treated as ordinary pip-only dependencies.

The primary packages used by the system are:

```bash
sudo apt update

sudo apt install -y \
    python3-picamera2 \
    python3-opencv \
    python3-numpy \
    python3-smbus2 \
    i2c-tools
```

GPIO support must provide compatibility with:

```python
import RPi.GPIO as GPIO
```

For the complete Raspberry Pi installation, configuration and verification procedure, see:

[**Raspberry Pi Setup and Run Guide**](Raspberry_Pi_Setup.md)

---

## 🔗 Dependency Map

### Open Challenge

```text
Open_Challenge.py
│
├── drive.py
│   └── RPi.GPIO-compatible interface
│
└── openVision.py
    ├── OpenCV
    ├── NumPy
    └── Picamera2
```

The Open Challenge imports:

```python
import drive
import openVision as vision
```

`openVision.py` is intentionally separate from the full Obstacle Challenge vision system.

It processes only the colours required for the Open Challenge:

```text
BLACK
BLUE
ORANGE
```

This allows the Open Challenge vision system to remain simpler and independently tunable.

---

### Obstacle Challenge

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
│       └── MPU6050 over I2C
│
└── parking.py
    ├── Picamera2
    ├── vision.py
    ├── heading.py
    └── drive.py
```

The Obstacle Challenge imports:

```python
from heading import MPU6050Heading
import drive
import vision
import parking
```

The full `vision.py` module detects:

```text
RED
GREEN
BLACK
BLUE
ORANGE
MAGENTA
```

Red and green are used for pillar navigation, black for wall geometry, and magenta is used during course/parking logic.

---

## 🅿️ Parking Dependencies

Parking is contained in:

```text
src/parking.py
```

The parking system uses:

- front Raspberry Pi camera,
- rear Raspberry Pi camera,
- `vision.py`,
- `drive.py`,
- `heading.py`,
- MPU6050 heading feedback.

The parking sequence combines computer vision with controlled forward/reverse Ackermann steering manoeuvres.

The final parking software has been **physically tested on Starlight and is working**.

---

## 🧭 MPU6050 Heading Module

The MPU6050 helper is contained in:

```text
src/heading.py
```

It uses:

```python
import smbus2
import time
```

The `MPU6050Heading` class:

1. initializes the MPU6050,
2. calibrates the Z-axis gyro offset,
3. reads angular velocity,
4. integrates rotational movement over time,
5. maintains a heading between `0°` and `360°`.

The IMU is used where orientation feedback is more useful than camera position alone, particularly during parking and controlled turning manoeuvres.

The heading module can be tested independently using:

```bash
python3 src/heading.py
```

The robot should remain stationary during initial gyro calibration.

---

## ⚙️ Python Standard-Library Modules

Modules included with Python itself do **not** require separate installation.

Examples used by the competition software include:

```python
import time
from time import sleep
```

These are part of the Python standard library and are therefore not listed as external dependencies.

---

## ✅ Dependency Verification

After completing the Raspberry Pi setup, the core software environment can be checked with:

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

The MPU6050 heading module can then be tested using:

```bash
python3 src/heading.py
```

The local Team Sentio modules can also be checked from inside `src/`:

```bash
cd src

python3 -c "import drive; import openVision; import vision; import heading; import parking; print('Team Sentio modules: PASS')"
```

---

## ✅ Final Validation

At the final competition project stage:

- **Open Challenge has been physically tested and is working.**
- **Obstacle Challenge has been physically tested and is working.**
- **Parking has been physically tested and is working.**
- `drive.py` is included.
- `openVision.py` is included.
- `vision.py` is included.
- `heading.py` is included.
- `parking.py` is included.
- CAD and STL material is included.
- Electrical documentation is included.
- Final robot photographs and supporting evidence are included.
- The complete working project package has been pushed to GitHub.

The repository should remain synchronized with the exact software running on Starlight.

If a final competition calibration changes a threshold, speed, steering value, gain or timing parameter, the corresponding change should also be committed and pushed.

---

## 🔄 Clean-Clone Reproducibility Requirements

A clean clone must contain at least:

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

A competition program is not fully reproducible if it works only because a required helper file already exists locally on the Raspberry Pi.

For this reason:

- `drive.py` is required for motor and steering control.
- `openVision.py` is required by the Open Challenge.
- `vision.py` is required by the Obstacle Challenge and parking.
- `heading.py` is required for MPU6050 heading feedback.
- `parking.py` is required for the final parking sequence.

All of these files are part of the final working project package.

---

## 📁 Related Documentation

For full reproduction of the robot, also refer to:

- [`README.md`](../README.md) — project overview and engineering summary
- [`Raspberry_Pi_Setup.md`](Raspberry_Pi_Setup.md) — Raspberry Pi installation and run procedure
- [`src/`](../src/) — complete competition source code
- [`schemes/`](../schemes/) — electrical wiring documentation
- [`models/`](../models/) — CAD and printable components
- [`v-photos/`](../v-photos/) — final vehicle photographs
- [`t-photos/`](../t-photos/) — team photographs
- [`video/`](../video/) — autonomous challenge videos
- [`other/`](../other/) — supporting testing and engineering evidence

---

## 📝 Dependency Policy

The repository separates **software dependencies** from **installation instructions**:

- This document records **what software the robot requires**.
- The Raspberry Pi Setup and Run Guide explains **how to install and configure it**.
- The exact competition source in `src/` determines the final dependency set.
- The physically tested robot software remains the authoritative competition version.

Exact package-version numbers are not invented when they have not been independently retained from the physically tested Raspberry Pi environment.

If a future competition-software revision introduces another third-party dependency:

1. install it on the Raspberry Pi,
2. physically test the affected software,
3. update this document,
4. update the Raspberry Pi Setup guide,
5. commit and push the change.

The current Git revision can be identified using:

```bash
git rev-parse HEAD
```

The GitHub repository and the software running on the physical robot should remain synchronized.

---

**Team Sentio**  
**Starlight**  
*WRO Future Engineers 2026*  
**Robofun Lab (RFL), India**
