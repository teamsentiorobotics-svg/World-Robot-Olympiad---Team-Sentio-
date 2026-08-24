# 🧩 Software Dependencies

## Team Sentio — WRO Future Engineers 2026

This document records the software environment and Python dependencies used by **Team Sentio's autonomous vehicle, Starlight**, developed for the **World Robot Olympiad 2026 — Future Engineers** category.

| Item | Configuration |
|---|---|
| **Computer** | Raspberry Pi 5, 4 GB |
| **Operating System** | Raspberry Pi OS |
| **Programming Language** | Python 3 |
| **Camera Interface** | Picamera2 |
| **Computer Vision** | OpenCV + NumPy |
| **GPIO Interface** | RPi.GPIO-compatible interface |
| **I2C Interface** | SMBus2 |
| **Competition Status** | Final Open, Obstacle and Parking behaviour physically tested and working |

> [!NOTE]
> The exact source running on the physically tested robot remains the authoritative competition version. GitHub and the Raspberry Pi should remain synchronized whenever a competition calibration is changed.

For complete Raspberry Pi installation, wiring checks and configuration instructions, see:

**[`pi_setup_instruction.md`](pi_setup_instruction.md)**

---

# 🚗 Competition Software

The current competition software is stored in the [`src/`](../src/) directory.

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
| [`open_challenge_final_ready_to_go.py`](../src/open_challenge_final_ready_to_go.py) | Final Open Challenge autonomous controller |
| [`Obstacle_Challenge.py`](../src/Obstacle_Challenge.py) | Final Obstacle Challenge controller |
| [`drive.py`](../src/drive.py) | DC motor and steering-servo control |
| [`openVision.py`](../src/openVision.py) | Open Challenge BLACK / BLUE / ORANGE vision |
| [`vision.py`](../src/vision.py) | Obstacle Challenge RED / GREEN / BLACK / BLUE / ORANGE / MAGENTA vision |
| [`heading.py`](../src/heading.py) | MPU6050 gyro calibration and relative heading calculation |
| [`parking.py`](../src/parking.py) | Dual-camera and IMU-assisted parking behaviour |

The challenge controllers depend on these helper modules. A clean clone should not depend on undocumented Python files that exist only on the original Raspberry Pi.

---

# 📦 External Software Dependencies

The competition system uses the following main external software components:

| Dependency | Purpose |
|---|---|
| **Python 3** | Executes all competition software |
| **OpenCV (`cv2`)** | Image processing, masks, morphology, contours and navigation geometry |
| **NumPy** | Numerical and image-array processing |
| **Picamera2** | Raspberry Pi Camera Module interface |
| **RPi.GPIO-compatible interface** | Motor-driver and steering-servo GPIO/PWM control |
| **SMBus2** | I2C communication with the MPU6050 IMU |

Only dependencies used by the competition software are documented here.

---

# 🍓 Raspberry Pi OS Packages

Raspberry Pi-specific libraries are installed primarily through the Raspberry Pi OS package manager.

Install the main packages using:

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
| `git` | Clone and update the Team Sentio repository |
| `python3-picamera2` | Raspberry Pi camera interface |
| `python3-opencv` | Computer vision and image processing |
| `python3-numpy` | Numerical and image-array operations |
| `python3-smbus2` | MPU6050 I2C communication |
| `i2c-tools` | I2C device detection and diagnostics |

---

# 🔌 Raspberry Pi 5 GPIO Compatibility

The low-level drive software imports:

```python
import RPi.GPIO as GPIO
```

The Raspberry Pi environment must therefore provide an interface compatible with the `RPi.GPIO` namespace.

Test the current environment with:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO import OK')"
```

On a Raspberry Pi 5 installation requiring a compatibility implementation:

```bash
sudo apt install -y python3-rpi-lgpio
```

If the classic `python3-rpi.gpio` package conflicts with the Raspberry Pi 5 compatibility package:

```bash
sudo apt remove -y python3-rpi.gpio
sudo apt install -y python3-rpi-lgpio
```

Do not deliberately maintain conflicting GPIO implementations providing the same Python namespace.

Verify again with:

```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO interface OK')"
```

---

# 🔗 Dependency Architecture

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

The Open Challenge uses a separate lightweight vision system because it requires only:

```text
BLACK
BLUE
ORANGE
```

Black provides wall geometry.

Blue and orange provide course-marker and direction information.

Keeping `openVision.py` separate from the complete Obstacle Challenge vision module reduces unnecessary processing and allows the Open Challenge thresholds to be tuned independently.

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

Its main dependency structure is:

```text
Obstacle_Challenge.py
│
├── drive.py
│   └── GPIO / motor / steering control
│
├── vision.py
│   ├── OpenCV
│   ├── NumPy
│   └── Picamera2
│
├── heading.py
│   └── SMBus2
│       └── MPU6050
│
└── parking.py
    ├── Picamera2
    ├── vision.py
    ├── heading.py
    └── drive-control dependency
```

The full Obstacle Challenge vision system detects:

```text
RED
GREEN
BLACK
BLUE
ORANGE
MAGENTA
```

Red and green are used for pillar navigation.

Black provides wall geometry.

Blue, orange and magenta support course and parking-related perception.

---

# 👁️ Open Challenge Vision

The Open Challenge vision module is:

```text
src/openVision.py
```

Its main imports are:

```python
import cv2
import numpy as np
import time
from picamera2 import Picamera2
```

The current camera configuration uses:

```text
Width:          1480 px
Height:         520 px
Format:         RGB888
Requested FPS:  60
```

The module detects:

```text
BLACK
BLUE
ORANGE
```

Its perception pipeline includes:

```text
Camera frame
      ↓
HSV conversion
      ↓
Colour mask
      ↓
Morphological filtering
      ↓
Contour extraction
      ↓
Area / geometry filtering
      ↓
Target information
```

---

# 🚧 Obstacle Challenge Vision

The complete obstacle-vision module is:

```text
src/vision.py
```

Its main imports are:

```python
import cv2
import numpy as np
import time
from picamera2 import Picamera2
```

The current front-camera configuration uses:

```text
Width:          1480 px
Height:         520 px
Format:         RGB888
Requested FPS:  60
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

Its detection system combines:

- HSV colour information,
- LAB colour information,
- contour geometry,
- contour area,
- confidence filtering,
- morphological noise removal.

This reduces the chance that isolated colour noise is immediately treated as a valid navigation object.

---

# 🧭 MPU6050 Heading Dependency

The heading helper is:

```text
src/heading.py
```

It provides:

```python
MPU6050Heading
```

and uses:

```python
import smbus2
import time
```

The MPU6050 communicates with the Raspberry Pi over I2C.

Enable I2C using:

```bash
sudo raspi-config
```

Then select:

```text
Interface Options
→ I2C
→ Enable
```

After rebooting, verify the sensor with:

```bash
i2cdetect -y 1
```

The MPU6050 used by Starlight is expected at:

```text
0x68
```

Test the heading module directly using:

```bash
python3 src/heading.py
```

Keep the robot completely stationary while the initial gyro calibration is performed.

---

# 🅿️ Parking Dependencies

Parking is implemented in:

```text
src/parking.py
```

The parking architecture uses:

- front Raspberry Pi camera,
- rear Raspberry Pi camera,
- OpenCV,
- Picamera2,
- `vision.py`,
- `heading.py`,
- MPU6050 heading feedback,
- motor and steering control.

The rear camera provides parking geometry that becomes important when Starlight is reversing and the front camera can no longer observe the complete parking area.

Because Starlight uses Ackermann steering, parking requires controlled forward and reverse arcs rather than an in-place rotation.

The final parking behaviour has been physically tested on Starlight and is working.

---

## ⚠️ Parking Drive-Module Reproducibility Check

The current repository copy of `parking.py` should remain identical to the version used during physical validation.

Before the final repository freeze, confirm the drive-module import used by the physically tested Raspberry Pi copy.

If the tested source uses:

```python
import robot_drive as drive
```

then the corresponding:

```text
robot_drive.py
```

must also be committed to `src/`.

If the physically tested parking program instead uses:

```python
import drive
```

then the GitHub copy of `parking.py` should use that same tested dependency.

The repository must not require a helper module that exists only on the original Raspberry Pi.

---

# 📷 Camera Dependencies

Starlight uses **two Raspberry Pi Camera Module 3 units**.

## Front Camera

Used for:

- black-wall perception,
- blue/orange marker detection,
- red/green pillar detection,
- obstacle navigation,
- front parking geometry.

## Rear Camera

Used primarily for:

- parking reference detection,
- reverse positioning,
- rear geometry during final manoeuvres.

Both cameras can be checked with:

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

Camera numbering should not be changed immediately before competition without retesting the complete physically validated program.

---

# ⚙️ Python Standard Library

The source also uses modules included with Python itself.

Examples include:

```python
import time
from time import sleep
```

These modules are part of the Python standard library and do not require separate installation.

---

# ✅ External Dependency Verification

After the Raspberry Pi setup is complete, run:

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

If this command completes without an exception, the principal third-party Python dependencies are available.

---

# ✅ Local Module Verification

From the repository root:

```bash
cd src
```

Verify the core helper modules:

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

Then check parking separately:

```bash
python3 -c "import parking; print('parking.py: OK')"
```

If the parking import produces:

```text
ModuleNotFoundError: No module named 'robot_drive'
```

the GitHub repository is missing the drive-control dependency used by that copy of `parking.py`.

Resolve the dependency against the **exact physically tested Raspberry Pi source** before permanently freezing the repository.

---

# 🏁 Current Competition Configuration

## Open Challenge

Current executable:

```text
src/open_challenge_final_ready_to_go.py
```

Important current settings include:

```text
LINE_COOLDOWN     = 1.3 s
TOTAL_LINES       = 12
KP                = 0.013
START_SPEED       = 40
TARGET_SPEED      = 100
ACCELERATION_TIME = 2.0 s
```

The source itself remains authoritative for all final competition calibration values.

---

## Obstacle Challenge

Current executable:

```text
src/Obstacle_Challenge.py
```

Important current settings include:

```text
total_lap            = 3
rs                   = 45
KP                   = 0.014
OBSTACLE_ACTION_AREA = 18000
```

Again, the exact physically validated source remains authoritative.

---

# 🔄 Clean-Clone Reproducibility

A fresh clone should begin with:

```bash
git clone https://github.com/teamsentiorobotics-svg/World-Robot-Olympiad---Team-Sentio-.git

cd World-Robot-Olympiad---Team-Sentio-
```

The current main competition source set is:

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

If the physically tested version of `parking.py` requires another drive-control module, that module must also be included.

The guiding reproducibility rule is:

```text
Physical robot source
        =
Raspberry Pi source
        =
GitHub source
        =
Documentation
```

---

# ✅ Final Validation Status

At the final competition stage:

- **Open Challenge has been physically tested and is working.**
- **Obstacle Challenge has been physically tested and is working.**
- **Parking has been physically tested and is working.**
- `drive.py` is included.
- `openVision.py` is included.
- `vision.py` is included.
- `heading.py` is included.
- `parking.py` is included.
- Raspberry Pi setup documentation is included.
- Software dependency documentation is included.
- Electrical documentation is included.
- CAD and printable-model material is included.
- Final robot photographs are included.
- Team photographs are included.
- Autonomous video evidence is included.
- Supporting engineering and testing material is included.

The remaining parking drive-module import should be checked against the exact working Raspberry Pi copy before the repository is permanently frozen.

---

# 📝 Dependency and Versioning Policy

Only dependencies actually required by the competition source are documented here.

Exact package-version numbers are not invented when the precise versions from the physically tested Raspberry Pi environment were not retained.

If a later software change introduces a new external dependency:

1. install the dependency on the Raspberry Pi,
2. physically test the affected challenge,
3. update this document,
4. update `pi_setup_instruction.md`,
5. commit the changed source,
6. push the synchronized revision to GitHub.

Changes to any of the following should also be physically retested:

- steering values,
- motor speed,
- proportional gain,
- image thresholds,
- marker cooldown,
- camera mapping,
- parking timing,
- IMU logic.

---

# 🔖 Git Revision

The exact Git revision can be recorded using:

```bash
git rev-parse HEAD
```

Check for uncommitted Raspberry Pi changes using:

```bash
git status
```

A final competition setup should not contain undocumented source modifications that exist on the Raspberry Pi but are absent from GitHub.

---

# 📁 Related Repository Files

For complete reproduction of Starlight, also refer to:

| Resource | Location |
|---|---|
| Main project overview | [`../README.md`](../README.md) |
| Development history | [`../CHANGELOG.md`](../CHANGELOG.md) |
| Software requirements | [`../requirements.md`](../requirements.md) |
| Raspberry Pi setup | [`pi_setup_instruction.md`](pi_setup_instruction.md) |
| Final Open Challenge | [`../src/open_challenge_final_ready_to_go.py`](../src/open_challenge_final_ready_to_go.py) |
| Obstacle Challenge | [`../src/Obstacle_Challenge.py`](../src/Obstacle_Challenge.py) |
| Drive control | [`../src/drive.py`](../src/drive.py) |
| Open vision | [`../src/openVision.py`](../src/openVision.py) |
| Obstacle vision | [`../src/vision.py`](../src/vision.py) |
| MPU6050 heading | [`../src/heading.py`](../src/heading.py) |
| Parking | [`../src/parking.py`](../src/parking.py) |
| Electrical schematic | [`../schemes/`](../schemes/) |
| CAD and printable components | [`../models/`](../models/) |
| Vehicle photographs | [`../v-photos/`](../v-photos/) |
| Team photographs | [`../t-photos/`](../t-photos/) |
| Autonomous video evidence | [`../video/`](../video/) |
| Supporting engineering evidence | [`../other/`](../other/) |

---

**Team Sentio**  
**Starlight**  
**World Robot Olympiad — Future Engineers 2026**  
**Robofun Lab (RFL), India**
