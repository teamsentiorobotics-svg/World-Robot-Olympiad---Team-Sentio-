# Team Sentio — WRO Future Engineers 2026

This repository documents **Team Sentio's autonomous vehicle, Starlight**, developed for the **World Robot Olympiad 2026 — Future Engineers** category.

**Team:** Deyaan Agrawal, Darsh Zaveri, Aarav Jalan  
**Institution / Training Environment:** Robofun Lab (RFL), India  
**Robot:** Starlight  
**Competition:** World Robot Olympiad 2026 — Future Engineers

Our engineering process throughout the project has been:

> **Build → Test → Observe → Find the failure → Modify → Retest**

Starlight was not developed as a single finished design. The robot evolved through repeated mechanical, electrical and software iterations. This repository records the final competition software together with the CAD, wiring, setup documentation, physical photographs, testing evidence and major engineering decisions required to understand the system.

The final Open Challenge, Obstacle Challenge and Parking behaviours have been physically tested on the robot and are working.

---

# Repository Structure

```text
.
├── README.md
├── CHANGELOG.md
├── requirements.md
├── .gitignore
│
├── src/
│   ├── open_challenge_final_ready_to_go.py
│   ├── Obstacle_Challenge.py
│   ├── drive.py
│   ├── openVision.py
│   ├── vision.py
│   ├── heading.py
│   └── parking.py
│
├── docs/
│   ├── Software_Dependencies.md
│   └── pi_setup_instruction.md
│
├── models/
├── schemes/
├── v-photos/
├── t-photos/
├── video/
└── other/
```

| Folder / File | Purpose |
|---|---|
| `src/` | Final competition software and supporting Python modules |
| `docs/` | Raspberry Pi setup and software dependency documentation |
| `models/` | CAD renders, 3D assembly files and printable components |
| `schemes/` | Electrical schematic and wiring information |
| `v-photos/` | Final robot and electronics photographs |
| `t-photos/` | Team photographs |
| `video/` | Autonomous driving evidence |
| `other/` | Logic design, planning, testing and supporting engineering material |
| `README.md` | Main project and engineering overview |
| `CHANGELOG.md` | Development and validation history |
| `requirements.md` | Software dependency and reproduction information |

---

# 1. Software Architecture

Starlight's software is divided into **challenge-level controllers** and reusable hardware, sensing and vision modules.

This keeps functions such as motor control, image processing and heading calculation separate from high-level navigation logic.

## Open Challenge

```text
open_challenge_final_ready_to_go.py
            │
            ├── drive.py
            │     └── motor + steering control
            │
            └── openVision.py
                  └── BLACK / BLUE / ORANGE vision
```

The final Open Challenge executable is:

```text
src/open_challenge_final_ready_to_go.py
```

It imports:

```python
import drive
import openVision as vision
```

The Open Challenge is therefore kept relatively lightweight and uses a dedicated computer-vision module containing only the detections required for that challenge.

---

## Obstacle Challenge

```text
Obstacle_Challenge.py
          │
          ├── drive.py
          ├── vision.py
          ├── heading.py
          └── parking.py
```

The Obstacle Challenge combines:

- wall following,
- red-pillar avoidance,
- green-pillar avoidance,
- course tracking,
- IMU-assisted manoeuvres,
- parking logic.

The additional complexity is separated into supporting modules rather than placing every function inside one competition file.

---

# 2. Mechanical Design

Starlight is a compact autonomous vehicle combining **custom 3D-printed PLA components with selected LEGO Technic mechanical elements**.

Final measured and documented physical parameters:

| Parameter | Value |
|---|---:|
| Mass | ~865 g |
| Length | ~210 mm |
| Width | 128 mm |
| Height | 265 mm |
| Wheelbase | 107.5 mm |
| Track width | 110 mm |
| Wheel diameter | 46 mm |
| Ground clearance | 14 mm |
| Steering | Front Ackermann |
| Drive | Four-wheel drive |

The purpose-built PLA components provide repeatable geometry for important structural areas such as:

- chassis packaging,
- camera positioning,
- electronics mounting,
- battery placement,
- rear parking camera support.

LEGO Technic elements were retained where they provided useful mechanical flexibility, rapid replacement and adjustment.

---

## Ackermann Steering

Starlight uses **front Ackermann-style steering**.

During a turn, the inner and outer front wheels follow different turning radii. Ackermann geometry allows the inner wheel to turn more sharply than the outer wheel, reducing tyre scrub and helping the robot follow smoother arcs.

This is especially important for WRO Future Engineers because Starlight behaves like a small car rather than a differential-drive robot.

The steering travel was limited experimentally.

Excessive steering caused problems such as:

- stress on the steering linkage,
- possible LEGO linkage disconnection,
- over-aggressive corrections,
- unstable cornering.

For this reason, the exact steering calibration used by the competition robot is maintained in the physically tested source files rather than being treated as a purely theoretical value.

---

# 3. Drivetrain

The final drivetrain uses:

```text
JGB37-520
12 V
600 RPM nominal
```

Starlight uses **four-wheel drive**.

The final external gear stage is:

```text
36T driving gear → 24T driven gear
```

The ideal external speed ratio is:

```text
36 / 24 = 1.5
```

Therefore:

```text
600 × 1.5 = 900 RPM
```

With a wheel diameter of approximately 46 mm:

```text
Wheel circumference
= π × 0.046
≈ 0.1445 m
```

At the theoretical geared output:

```text
900 RPM
= 15 revolutions/second

15 × 0.1445
≈ 2.17 m/s
```

The theoretical wheel-surface speed is therefore approximately **2.17 m/s**.

Practical output was estimated closer to approximately **800 RPM**, corresponding to around **1.93 m/s**.

These values are engineering calculations and estimates rather than laboratory speed measurements.

An earlier higher-speed motor experienced excessive loading and stall behaviour. The final motor and gearing were therefore selected with **reliability and repeatability** given greater priority than maximum theoretical speed.

---

# 4. Electronics and Power

The main computing platform is:

```text
Raspberry Pi 5
4 GB RAM
```

The final robot hardware includes:

- Raspberry Pi 5
- 2 × Raspberry Pi Camera Module 3
- JGB37-520 DC geared motor
- TB6612FNG motor driver
- DS3225 steering servo
- MPU6050 IMU
- 3S LiPo battery
- regulated Raspberry Pi power supply
- front illumination LED

Battery specification:

```text
3S LiPo
11.1 V nominal
2200 mAh
```

Nominal stored energy:

```text
11.1 × 2.2
= 24.42 Wh
```

The motor is supplied through the motor-driver system, while the Raspberry Pi and control electronics use a regulated supply.

All required control electronics share a common ground.

---

## GPIO Architecture

The main Raspberry Pi control assignments are:

| Function | BCM GPIO |
|---|---:|
| Motor IN1 | GPIO5 |
| Motor IN2 | GPIO6 |
| Motor PWM | GPIO13 |
| Steering servo | GPIO22 |
| I2C SDA | GPIO2 |
| I2C SCL | GPIO3 |

The low-level motor and steering implementation is contained in:

```text
src/drive.py
```

The challenge controllers can therefore use simple functions such as:

```python
drive.forward(speed)
drive.backward(speed)
drive.steer(angle)
drive.stop()
```

This prevents GPIO and PWM code from being unnecessarily duplicated across the challenge programs.

The full electrical schematic is available in:

```text
schemes/
```

---

# 5. Computer Vision

Computer vision is Starlight's main method of understanding the track.

The general image-processing pipeline is:

```text
Camera frame
     ↓
Colour-space conversion
     ↓
Colour thresholding
     ↓
Morphological filtering
     ↓
Contour extraction
     ↓
Area / geometry filtering
     ↓
Target selection
     ↓
Steering decision
```

Two separate computer-vision modules are retained because the Open and Obstacle Challenges require different information.

---

## Open Challenge Vision — `openVision.py`

The Open Challenge vision module detects:

```text
BLACK
BLUE
ORANGE
```

Black provides wall geometry.

Blue and orange provide course-marker information.

The final module uses a Raspberry Pi Camera Module through Picamera2 and processes frames using OpenCV and NumPy.

Keeping this module separate means that the Open Challenge does not need to process red, green or magenta objects that are irrelevant to its navigation task.

---

## Obstacle Vision — `vision.py`

The full Obstacle Challenge vision system detects:

```text
RED
GREEN
BLACK
BLUE
ORANGE
MAGENTA
```

The module combines:

- HSV colour information,
- LAB colour information,
- contour area,
- geometric filtering,
- confidence scoring,
- morphological filtering.

The purpose is not simply to react to any pixel matching a colour.

Instead, the robot tries to identify sufficiently large and meaningful objects before using them as navigation targets.

Red and green pillars are used for obstacle navigation, black provides wall geometry, and the additional course colours support track and parking behaviour.

---

# 6. Open Challenge Strategy

The Open Challenge is primarily a **continuous vision-based wall-following problem**.

The final controller performs the following sequence:

```text
Capture image
      ↓
Detect walls and markers
      ↓
Determine course direction
      ↓
Calculate visual error
      ↓
Apply proportional steering
      ↓
Count valid course events
      ↓
Continue autonomous navigation
      ↓
Stop after the required sequence
```

The basic steering relationship is:

```text
Steering
=
Centre
+
KP × Visual Error
```

This allows steering to be updated continuously from the observed track geometry instead of relying on fixed-duration turns.

The final Open source uses:

```text
LINE_COOLDOWN = 1.3 s
TOTAL_LINES   = 12
START_SPEED   = 40
TARGET_SPEED  = 100
KP            = 0.013
```

The motor speed ramps from the starting command toward the target speed during the initial acceleration period.

The driving direction is not fixed when the program begins.

The robot uses course-marker information to establish whether the course is being driven clockwise or anticlockwise.

Event/cooldown logic helps prevent one physical marker that remains visible for multiple camera frames from being repeatedly counted.

---

# 7. Obstacle Challenge Strategy

The Obstacle Challenge requires the robot to combine wall following with dynamic pillar avoidance.

The final controller uses:

```text
Observe
   ↓
Detect wall / pillar
   ↓
Determine relevant target
   ↓
Calculate steering
   ↓
Move
   ↓
Observe again
```

The current physical competition strategy uses continuous image geometry rather than depending entirely on fixed timed obstacle turns.

This was an important development decision.

During earlier testing, pillars positioned near corners could become visible before the robot had completed its existing turn. Responding too aggressively to a newly visible pillar could make the vehicle oversteer or take an incorrect path.

The final approach therefore uses:

- minimum colour-area filtering,
- continuous target updates,
- proportional steering,
- wall geometry,
- challenge direction,
- pillar geometry,
- repeated camera observations.

The current final program is configured for the required three-lap challenge sequence and has been physically tested on Starlight.

---

# 8. MPU6050 Heading

The helper module:

```text
src/heading.py
```

contains the MPU6050 heading system used during orientation-sensitive manoeuvres.

The module:

1. initializes the MPU6050,
2. determines gyro offset while the robot is stationary,
3. removes that offset from later measurements,
4. reads Z-axis angular velocity,
5. integrates rotational movement,
6. maintains a relative heading.

This provides orientation feedback for manoeuvres where camera geometry alone is not sufficient.

The IMU is particularly useful during controlled forward/reverse movements and parking alignment.

---

# 9. Parking

Parking is implemented separately in:

```text
src/parking.py
```

The parking architecture combines:

- front-camera perception,
- rear-camera perception,
- black-wall geometry,
- magenta parking detection,
- MPU6050 heading information,
- controlled forward and reverse movements.

The intended behaviour can be summarized as:

```text
Course complete
      ↓
Enter parking stage
      ↓
Observe parking geometry
      ↓
Control steering and movement
      ↓
Use rear-camera information
      ↓
Use heading feedback
      ↓
Perform forward/reverse corrections
      ↓
Final stop
```

Starlight uses Ackermann steering and therefore cannot rotate about its centre.

Parking must consequently be performed through a sequence of forward and reverse arcs.

The rear camera provides information that cannot reliably be obtained from the front camera once the vehicle begins reversing into the parking area.

The final parking behaviour has been physically tested on the robot and is working.

---

# 10. CAD and Mechanical Reproduction

The `models/` folder contains the mechanical reconstruction material for Starlight.

The repository currently includes CAD/render evidence for components such as:

- complete CAD assembly,
- lower chassis and drivetrain base,
- central battery/electronics compartment,
- PCB and electronics top mounting plate,
- front camera mount,
- rear parking camera mount.

It also includes:

- printable STL files,
- a compressed complete GLB model.

These resources allow the mechanical design to be understood independently of the physical photographs.

The goal is not only to show what Starlight looks like but also to document how its custom mechanical parts were designed.

---

# 11. Physical Robot Evidence

The `v-photos/` directory contains photographs of the final physical robot.

Views include:

- front view,
- rear view,
- side view,
- bird's-eye view,
- bottom view,
- circuit-board view,
- solder-side circuit-board view.

These photographs connect the CAD, wiring and software documentation to the actual built competition robot.

The `t-photos/` directory contains the team-member photographs.

---

# 12. Electrical Documentation

The electrical schematic is stored in:

```text
schemes/schematic.jpeg
```

Together with `drive.py` and the Raspberry Pi setup documentation, this provides three complementary levels of electrical information:

```text
Electrical schematic
        +
GPIO assignments
        +
Actual Python hardware control
```

This helps another person understand both how the electronics are connected and how the software controls them.

---

# 13. Raspberry Pi Setup and Dependencies

Detailed software setup documentation is provided in:

```text
docs/pi_setup_instruction.md
docs/Software_Dependencies.md
requirements.md
```

The software stack includes:

- Python 3
- OpenCV
- NumPy
- Picamera2
- RPi.GPIO-compatible GPIO support
- SMBus2

The Raspberry Pi setup guide covers:

- Raspberry Pi OS preparation,
- package installation,
- GPIO compatibility,
- I2C configuration,
- MPU6050 detection,
- camera detection,
- repository cloning,
- Python dependency checking,
- mechanical pre-run checks,
- electrical pre-run checks,
- challenge execution,
- troubleshooting.

The aim is to make the software environment understandable and reproducible rather than assuming that required dependencies are already installed.

---

# 14. Testing and Validation

The standard Team Sentio testing sequence is:

```text
Component test
      ↓
Subsystem test
      ↓
Low-speed integrated test
      ↓
Full challenge run
      ↓
Observe failure
      ↓
Modify
      ↓
Retest
```

Before a full autonomous run, the team checks:

- battery condition,
- polarity,
- regulated Raspberry Pi supply,
- common ground,
- motor direction,
- drivetrain freedom,
- gear engagement,
- steering linkage,
- steering limits,
- camera connections,
- front-camera detection,
- rear-camera operation,
- MPU6050 operation,
- correct source files,
- required Python modules.

The Open Challenge completed repeated successful timed runs during development.

The Obstacle Challenge completed more than **10 successful full runs** during development.

The final Open, Obstacle and Parking behaviours have been physically tested and are working.

Where the complete number of unsuccessful attempts was not retained, the repository does not invent a success percentage retrospectively.

---

# 15. Important Engineering Decisions

| Engineering Change | Reason |
|---|---|
| Higher-speed motor → JGB37-520 | Improved drivetrain reliability |
| Earlier drivetrain → 4WD | Improved traction and consistency |
| Final 36T → 24T gearing | Balanced speed and reliability |
| Excessive steering range → limited travel | Protected steering linkage |
| Single vision approach → separate Open/Obstacle vision | Challenge-specific processing |
| Fixed obstacle commitment → continuous vision targets | Better obstacle response |
| Camera-only manoeuvres → camera + IMU | Improved orientation feedback |
| Flexible camera geometry → rigid mounts | More repeatable perception |
| Ambient lighting only → front illumination | Improved visual consistency |
| Earlier electrical failures → stricter safety process | Improved reliability and safety |

These changes demonstrate one of the central lessons of the project:

> **Mechanical, electrical and software systems cannot be developed independently.**

A small physical change in camera position can affect vision.

A steering change can require new software tuning.

A drivetrain change can alter cornering behaviour.

A power-system problem can appear to be a software failure.

The final robot was developed by treating Starlight as one integrated system.

---

# 16. Supporting Engineering Material

The `other/` folder contains supporting development evidence including:

- logic-design material,
- parking logic design,
- planning/Gantt material,
- Raspberry Pi setup material,
- supporting experimental files.

This material complements the final source code by showing parts of the planning and design process used during development.

---

# 17. Video Evidence

The `video/` folder contains autonomous driving evidence from Starlight.

This provides a direct link between:

```text
Source code
    ↓
Physical robot
    ↓
Autonomous performance
```

Video evidence is used together with the source files, photographs and testing records rather than as a replacement for engineering documentation.

---

# 18. Reproducing the Project

A reproduction of Starlight should use the repository as a complete engineering package rather than copying only the main Python file.

Recommended process:

1. Clone the repository.
2. Review `README.md`.
3. Review `requirements.md`.
4. Follow `docs/pi_setup_instruction.md`.
5. Study the electrical schematic in `schemes/`.
6. Review the CAD and printable parts in `models/`.
7. Compare construction with `v-photos/`.
8. Install and verify Raspberry Pi dependencies.
9. Verify both cameras.
10. Verify the MPU6050.
11. Verify motor and steering control.
12. Test the vision modules.
13. Run the challenge software at controlled speed.
14. Physically validate the complete robot.

The current competition software package is:

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

The exact Git revision can be identified using:

```bash
git rev-parse HEAD
```

The repository should remain synchronized with the physically tested software used on Starlight.

Any later calibration change should be tested before being treated as a new final competition revision.

---

# 19. Development History

The project progressed through multiple generations.

| Stage | Main Development |
|---|---|
| V0 | Initial LEGO mobility prototype |
| V1 | Electronics and camera-based autonomous control |
| V2 | Improved printed electronics mounting and packaging |
| V3 | Purpose-built Starlight competition chassis |
| Open development | Direction-aware wall following and marker detection |
| Obstacle development | Continuous pillar avoidance and IMU-assisted manoeuvres |
| Parking development | Dual-camera and heading-assisted parking |

More detailed development and validation history is preserved in:

```text
CHANGELOG.md
```

The Git commit history also provides a record of repository changes and final documentation updates.

---

# 20. Team Contributions

### Deyaan Agrawal

Main responsibilities included:

- software development,
- autonomous algorithms,
- computer vision,
- navigation logic,
- debugging,
- parameter tuning,
- track testing.

### Darsh Zaveri

Main responsibilities included:

- mechanical construction,
- drivetrain,
- steering,
- electronics,
- wiring,
- hardware integration,
- physical testing.

### Aarav Jalan

Main responsibilities included:

- CAD and mechanical development,
- algorithm contributions,
- debugging,
- circuit construction,
- testing evidence,
- project documentation.

Robofun Lab provided access to facilities, mock runs and guidance during development roadblocks.

The submitted robot, source code, design decisions, testing process and engineering documentation remain the work of **Team Sentio**.

---

# Final Engineering Principle

Starlight was not created by getting every design decision correct on the first attempt.

The final robot evolved through:

- drivetrain failures,
- steering problems,
- camera-position experiments,
- colour-detection errors,
- electrical incidents,
- obstacle-navigation failures,
- parking experiments,
- repeated mechanical and software tuning.

Each failure gave the team information that influenced the next version.

The engineering philosophy behind Starlight can therefore be summarized as:

> **Dream. Design. Build. Test. Fail. Understand. Improve. Repeat.**

---

**Team Sentio**  
**Starlight**  
**World Robot Olympiad — Future Engineers 2026**  
**Robofun Lab (RFL), India**
