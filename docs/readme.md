# Starlight Technical Documentation

**Team Sentio 6010**  
**WRO Future Engineers 2026**  
**Robot:** Starlight  
**Organisation:** Robofun Lab (RFL), India

---

## Documentation Overview

This directory contains the technical documentation for **Starlight**, Team Sentio's autonomous vehicle developed for the **World Robot Olympiad 2026 Future Engineers** category.

**Current documentation baseline:** Engineering Journal Revision 29.

The documentation is organized around the complete engineering process:

```text
Requirement
    ↓
Design
    ↓
Prototype
    ↓
Test
    ↓
Observe
    ↓
Identify limitation
    ↓
Modify
    ↓
Retest
    ↓
Retain / Reject
```

The aim is not only to describe the final robot, but also to make the development process traceable:

- what was built;
- why major decisions were made;
- what failed;
- what changed;
- how changes were tested;
- which configuration is current;
- how the system can be reproduced.

---

# Quick Navigation

## Engineering Process

| Document | Purpose |
| --- | --- |
| [Engineering Decisions](engineering-decisions.md) | Major design decisions, alternatives considered, trade-offs and reasons for the retained architecture |
| [Failure Log](failure-log.md) | Observed failures, diagnoses, engineering responses and retest outcomes |
| [Testing](testing.md) | Structured component, subsystem and integrated testing records |

These three documents form the main engineering traceability chain:

```text
Why was it chosen?
        ↓
engineering-decisions.md

What went wrong?
        ↓
failure-log.md

How was it verified?
        ↓
testing.md
```

---

# Hardware Documentation

| Document | Purpose |
| --- | --- |
| [Bill of Materials](hardware/bom.md) | Current components, specifications and sourcing references |
| [Drivetrain](hardware/drivetrain.md) | 4WD architecture, 1:1 gearing, motor, encoder, differential and Ackermann steering |
| [Wiring Guide](hardware/wiring-guide.md) | GPIO assignments, power connections, motor control, I2C and sensor wiring |

---

## Current Hardware Architecture

The current **Revision 29** Starlight configuration includes:

- Raspberry Pi 5, 4 GB;
- 2 × Raspberry Pi Camera Module 3 Wide;
- 3 × VL53L0X Time-of-Flight sensors;
- MPU6050 heading sensor;
- 12 V, 600 RPM geared DC motor;
- integrated quadrature encoder;
- TB6612FNG motor driver;
- DS3225 steering servo;
- four-wheel drive;
- mechanical differential;
- front Ackermann steering;
- 1:1 external drivetrain gearing.

The current configuration combines visual, heading, shaft-motion and distance observations rather than relying on a single sensing method.

```text
CAMERAS
   ↓
Appearance + geometry

MPU6050
   ↓
Relative heading

ENCODER
   ↓
Shaft movement

3 × ToF
   ↓
Local physical distance

        ↓
AUTONOMOUS CONTROL
```

---

# Software Documentation

| Document | Purpose |
| --- | --- |
| [Software Dependencies](software/Software_Dependencies.md) | Python environment, external packages, module relationships and reproducibility checks |
| [Raspberry Pi Setup](software/pi_setup_instruction.md) | Raspberry Pi installation, interface setup and system preparation |

The current principal source files are located in:

```text
../src/
```

and include:

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

The Revision 29 source map explicitly includes:

- `drive.py` as the shared motor, steering and encoder interface;
- `TOF_22.py` as the three-VL53L0X sensor interface;
- `TUF_test.py`, `encoder_test.py` and `servo_test.py` as dedicated subsystem tests.

Every local module required by the physically tested competition controllers should also be present in GitHub.

---

# Development History

| Document | Purpose |
| --- | --- |
| [APOC Hardware Update](development/apoc-hardware-update.md) | Post-Nationals chassis, camera, drivetrain and sensor redesign for the Asia Pacific Open Championship |

The current robot is the result of several major development stages:

```text
Early LEGO platform
        ↓
Hybrid LEGO + printed construction
        ↓
Nationals configuration
        ↓
Post-Nationals redesign
        ↓
Current APOC-oriented architecture
```

The post-Nationals redesign revised the:

- chassis;
- camera locations;
- camera mounts;
- vision geometry;
- drivetrain operating point;
- encoder integration;
- distance sensing;
- parking architecture.

---

# Current Design Identity

Starlight combines several mechanical and sensing decisions into one vehicle architecture.

| Design Feature | Engineering Purpose |
| --- | --- |
| **4WD** | Distribute propulsion across four driven wheels |
| **Ackermann steering** | Produce car-like forward and reverse turning geometry |
| **Mechanical differential** | Allow driven wheels to rotate at different speeds during a turn |
| **600 RPM encoder motor** | Provide propulsion with shaft-motion feedback |
| **1:1 gearing** | Prioritize available torque and controllability over maximum theoretical speed |
| **Dual cameras** | Provide task-specific visual geometry |
| **Multi-ROI vision** | Assign different image regions to different navigation tasks |
| **MPU6050** | Provide relative-heading feedback |
| **3 × VL53L0X** | Measure local physical gaps during close-range manoeuvres |
| **Rigid sensor mounts** | Preserve calibration geometry |

---

# Engineering Traceability

The documentation is designed so that a major design change can be traced across several files.

For example:

```text
Observed drivetrain stall
        ↓
failure-log.md
        ↓
Motor / gearing reconsidered
        ↓
engineering-decisions.md
        ↓
600 RPM motor + 1:1 gearing
        ↓
hardware/drivetrain.md
        ↓
encoder / drivetrain testing
        ↓
testing.md
```

Another example:

```text
Parking inconsistency
        ↓
failure-log.md
        ↓
Need direct gap information
        ↓
engineering-decisions.md
        ↓
3 × VL53L0X added
        ↓
development/apoc-hardware-update.md
        ↓
parking / ToF trials
        ↓
testing.md
```

This prevents the repository from presenting the final robot as if every design choice mysteriously appeared fully formed.

---

# Documentation Structure

Recommended `docs/` structure:

```text
docs/
├── README.md
├── engineering-decisions.md
├── failure-log.md
├── testing.md
│
├── hardware/
│   ├── bom.md
│   ├── drivetrain.md
│   └── wiring-guide.md
│
├── software/
│   ├── Software_Dependencies.md
│   └── pi_setup_instruction.md
│
└── development/
    └── apoc-hardware-update.md
```

---

# Repository Structure

The complete project extends beyond this documentation directory.

```text
World-Robot-Olympiad---Team-Sentio-/
│
├── README.md
├── CHANGELOG.md
│
├── src/
│   ├── Cal_APOC.py
│   ├── Final_Obstacle_Challenge.py
│   ├── N_Vision_final.py
│   ├── Sentio_Open_2026.py
│   ├── openvision.py
│   ├── TOF_22.py
│   ├── TUF_test.py
│   ├── drive.py
│   ├── encoder_test.py
│   ├── heading.py
│   ├── parking_final.py
│   └── servo_test.py
│
├── docs/
│   ├── engineering documentation
│   ├── testing
│   ├── hardware
│   ├── software
│   └── development history
│
├── Models/
│   ├── CAD
│   └── printable parts
│
├── schemes/
│   └── electrical documentation
│
├── v-photos/
│   └── vehicle and development photographs
│
├── t-photos/
│   └── team photographs
│
└── videos/
    └── autonomous demonstration evidence
```

---

# Suggested Judge Route

For a rapid technical review, the most useful path through the repository is:

### 1. Understand the final robot

Start with:

- [`../README.md`](../README.md)
- [`hardware/drivetrain.md`](hardware/drivetrain.md)
- [`hardware/bom.md`](hardware/bom.md)

---

### 2. Understand why the design looks this way

Read:

- [`engineering-decisions.md`](engineering-decisions.md)
- [`development/apoc-hardware-update.md`](development/apoc-hardware-update.md)

---

### 3. See the engineering iteration

Read:

- [`failure-log.md`](failure-log.md)

This records the progression from:

```text
Failure
   ↓
Diagnosis
   ↓
Engineering change
   ↓
Retest
```

---

### 4. Check the evidence

Read:

- [`testing.md`](testing.md)

This contains the component and integrated testing records supporting the retained architecture.

---

### 5. Inspect the implementation

Continue to:

```text
../src/
```

for the current competition code.

---

# Hardware → Software Relationship

Starlight is documented as one connected system.

A physical change can affect the software directly.

```text
Camera position changes
        ↓
Image geometry changes
        ↓
ROI coordinates change
        ↓
Detection changes
        ↓
Steering decision changes
```

Likewise:

```text
Motor / gearing changes
        ↓
Acceleration and movement change
        ↓
Camera scene changes faster/slower
        ↓
Control timing changes
        ↓
Stopping geometry changes
```

For this reason, mechanics, electronics and software are not documented as independent projects.

---

# Evidence Categories

The documentation distinguishes four kinds of evidence.

| Type | Meaning |
| --- | --- |
| **Recorded observation** | Behaviour observed during physical development or competition |
| **Specification** | Manufacturer rating or retained robot configuration |
| **Calculation** | Result derived from stated inputs and assumptions |
| **Computer study** | Result from a simplified numerical or simulated model |

These categories should not be mixed.

For example:

```text
600 RPM
```

is a motor specification.

```text
1.445 m/s
```

is an ideal calculated wheel-speed conversion for the current 1:1 drivetrain and 46 mm wheels.

Neither should automatically be described as a measured track speed.

---

# Testing Philosophy

Starlight is tested from the component level upward.

```text
Component
    ↓
Subsystem
    ↓
Integrated behaviour
    ↓
Complete challenge
```

Typical checks include:

- steering direction and travel;
- encoder response;
- motor operation;
- heading calibration;
- VL53L0X communication;
- camera calibration;
- colour separation;
- parking transitions;
- complete Open Challenge runs;
- complete Obstacle Challenge runs.

A successful component test does not automatically prove the complete robot will succeed.

Likewise, a successful complete run does not prove that every subsystem has a quantified reliability percentage.

---

# Reproducibility Principle

The project follows this rule:

```text
Physical robot
      =
Raspberry Pi source
      =
GitHub source
      =
Documentation
```

A competition result is meaningful only when the hardware and software configuration that produced it can be identified.

Before a final competition release:

```bash
git status
```

should not reveal undocumented source changes that exist only on the robot.

The tested revision can be recorded with:

```bash
git rev-parse HEAD
```

---

# Current Configuration vs Historical Material

The repository intentionally retains earlier:

- CAD;
- photographs;
- gearing calculations;
- motor references;
- software;
- test records.

These show engineering development.

However, historical information must be clearly labelled.

The current **Revision 29** configuration uses:

```text
600 RPM encoder motor
1:1 external gearing
4WD
Ackermann steering
mechanical differential
2 wide cameras
3 VL53L0X sensors
MPU6050
encoder feedback
multi-ROI vision
```

Older speed-increasing drivetrain configurations or previous camera layouts should not be interpreted as the current competition robot.

---

# Core Documentation Map

| Engineering Question | Where to Look |
| --- | --- |
| **What is Starlight?** | [`../README.md`](../README.md) |
| **Why was this design chosen?** | [`engineering-decisions.md`](engineering-decisions.md) |
| **What failed during development?** | [`failure-log.md`](failure-log.md) |
| **How was it tested?** | [`testing.md`](testing.md) |
| **How does the drivetrain work?** | [`hardware/drivetrain.md`](hardware/drivetrain.md) |
| **What hardware is installed?** | [`hardware/bom.md`](hardware/bom.md) |
| **How is it wired?** | [`hardware/wiring-guide.md`](hardware/wiring-guide.md) |
| **What changed for APOC?** | [`development/apoc-hardware-update.md`](development/apoc-hardware-update.md) |
| **What software is required?** | [`software/Software_Dependencies.md`](software/Software_Dependencies.md) |
| **How is the Raspberry Pi configured?** | [`software/pi_setup_instruction.md`](software/pi_setup_instruction.md) |
| **Where is the robot code?** | [`../src/`](../src/) |
| **Where are the CAD files?** | [`../Models/`](../Models/) |
| **Where are robot photographs?** | [`../v-photos/`](../v-photos/) |
| **Where is video evidence?** | [`../videos/`](../videos/) |

---

# Engineering Principle

Starlight was developed around a simple rule:

> **Do not document only what the robot became. Document why it became that way.**

A strong engineering record should connect:

```text
Problem
   ↓
Evidence
   ↓
Decision
   ↓
Implementation
   ↓
Test
   ↓
Result
```

That relationship is the purpose of this documentation directory.

---

**Team Sentio 6010**  
**Starlight**  
**World Robot Olympiad - Future Engineers 2026**  
**Robofun Lab (RFL), India**
