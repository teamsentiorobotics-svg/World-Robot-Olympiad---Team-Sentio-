# 🧩 Software Dependencies

## Team Sentio — WRO Future Engineers 2026

This document records the software environment and Python dependencies used by **Team Sentio's Raspberry Pi 5 autonomous vehicle**.

> **Platform:** Raspberry Pi 5 (4 GB)  
> **Operating System:** Raspberry Pi OS  
> **Language:** Python 3

---

## 🚗 Competition Programs

The main competition software is located in the [`src/`](../src/) directory:

| File | Purpose |
|---|---|
| [`Open_Challenge.py`](../src/Open_Challenge.py) | Autonomous navigation for the Open Challenge |
| [`Obstacle_Challenge.py`](../src/Obstacle_Challenge.py) | Obstacle navigation and parking control |
| [`heading.py`](../src/heading.py) | MPU6050 heading calculation used by the Obstacle Challenge |

---

## 📦 Software Stack

The competition system uses the following software components:

| Dependency | Purpose |
|---|---|
| **NumPy** | Numerical operations and image-array processing |
| **OpenCV** | Computer vision, colour detection, contours and geometry processing |
| **Picamera2** | Raspberry Pi Camera Module interface |
| **RPi.GPIO-compatible interface** | Motor and steering GPIO/PWM control |
| **SMBus2** | I2C communication with the MPU6050 IMU |
| **Python 3** | Main programming environment |

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

**[Raspberry Pi Setup and Run Guide](Raspberry_Pi_Setup.md)**

---

## 🔗 Dependency Mapping

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
           └── MPU6050 over I2C
```

---

## ⚙️ Standard-Library Modules

Modules included with Python itself do **not** require separate installation.

Examples used by the competition software include:

```python
import time
from time import sleep
```

These are therefore not listed as external dependencies.

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

The MPU6050 heading module can then be tested independently using:

```bash
python3 src/heading.py
```

---

## 📁 Related Documentation

For full reproduction of the robot, also refer to:

- [`README.md`](../README.md) — project overview and engineering summary
- [`Raspberry_Pi_Setup.md`](Raspberry_Pi_Setup.md) — Raspberry Pi installation and run procedure
- [`src/`](../src/) — competition source code
- [`schemes/`](../schemes/) — electrical wiring documentation
- [`models/`](../models/) — CAD and printable components
- [`v-photos/`](../v-photos/) — final vehicle photographs

---

## 📝 Dependency Policy

The repository separates **software dependencies** from **installation instructions**:

- This document records **what software the robot requires**.
- The Raspberry Pi Setup and Run Guide explains **how to install and configure it**.
- The exact competition source in `src/` determines the final dependency set.

If a future competition-software revision introduces another third-party dependency, this document and the setup guide should be updated together.

---

**Team Sentio**  
*WRO Future Engineers 2026*  
**Robofun Lab (RFL), India**
