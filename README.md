# Team Sentio — WRO Future Engineers 2026

This repository documents **Team Sentio's autonomous vehicle, Starlight, developed for the World Robot Olympiad 2026 — Future Engineers category**.

**Team:** Deyaan Agrawal, Darsh Zaveri, Aarav Jalan  
**Institution / Training Environment:** Robofun Lab (RFL), India  
**Robot:** Starlight  
**Competition:** World Robot Olympiad 2026 — Future Engineers

Our engineering process is:

> **Build → Test → Observe → Find the failure → Modify → Retest**

Starlight was developed through repeated mechanical, electrical and software iterations rather than as a single finished design. This repository records the final robot architecture, competition software, CAD, wiring, testing evidence and major engineering decisions required to understand and reproduce the system.

---

## Repository Structure

```text
.
├── README.md
├── requirements.md
├── src/
│   ├── Open_Challenge.py
│   ├── Obstacle_Challenge.py
│   ├── drive.py
│   ├── openVision.py
│   ├── vision.py
│   ├── heading.py
│   └── parking.py
├── docs/
├── models/
├── schemes/
├── v-photos/
├── t-photos/
├── video/
└── other/
````

| Folder / FilePurpose |                                                         |
| -------------------- | ------------------------------------------------------- |
| `src/`               | Competition programs and required Python helper modules |
| `docs/`              | Raspberry Pi setup and software documentation           |
| `models/`            | CAD, chassis models and printable parts                 |
| `schemes/`           | Electrical schematic and wiring information             |
| `v-photos/`          | Robot and hardware photographs                          |
| `t-photos/`          | Team photographs                                        |
| `video/`             | Autonomous driving evidence                             |
| `other/`             | Testing, planning and supporting engineering material   |
| `requirements.md`    | Software dependency information                         |

---

# Software Architecture

The software is divided into challenge-level controllers and reusable hardware, sensor and computer-vision modules.

## Open Challenge

```text
Open_Challenge.py
       │
       ├── drive.py
       │     └── motor + steering control
       │
       └── openVision.py
             └── BLACK / BLUE / ORANGE detection
```

The Open Challenge uses a dedicated lightweight vision module because it does not require obstacle or parking colour detection.

`openVision.py` detects:

- Black walls
- Blue course markers
- Orange course markers

The Open Challenge controller handles:

- camera acquisition,
- wall detection,
- proportional steering,
- marker detection,
- course-event counting,
- speed control,
- stopping logic.

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

`vision.py` is the more complete computer-vision module and detects:

- Red pillars
- Green pillars
- Black walls
- Blue markers
- Orange markers
- Magenta parking features

`heading.py` provides MPU6050-based heading estimation.

`parking.py` contains the separate final parking behaviour.

Keeping `openVision.py` and `vision.py` separate allows each challenge to be tuned independently and avoids unnecessary image processing during the Open Challenge.

---

# 1. Mechanical Design

Starlight is a compact autonomous vehicle combining a **custom 3D-printed PLA structure with selected LEGO Technic mechanical components**.

Final measured and documented parameters:

| ParameterValue   |                  |
| ---------------- | ---------------- |
| Mass             | \~865 g          |
| Length           | \~210 mm         |
| Width            | 128 mm           |
| Height           | 265 mm           |
| Wheelbase        | 107.5 mm         |
| Track width      | 110 mm           |
| Wheel diameter   | 46 mm            |
| Ground clearance | 14 mm            |
| Steering         | Front Ackermann  |
| Drive            | Four-wheel drive |

The PLA structure provides repeatable geometry for the chassis, electronics and camera mounting.

LEGO Technic components were retained where they provided rapid adjustment, easy replacement and useful mechanical flexibility.

## Ackermann Steering

Starlight uses **Ackermann-style front steering**.

During a turn, the inside and outside front wheels follow different radii. Ackermann geometry allows the inside wheel to steer more sharply than the outside wheel, reducing tyre scrub and improving predictable cornering.

The steering range was limited experimentally.

Excessive servo movement could:

- stress the steering linkage,
- disconnect LEGO steering components,
- create unnecessary oscillation,
- produce overly aggressive corrections.

The final steering limits are therefore treated as a **mechanical reliability constraint**, not only a software parameter.

The low-level servo implementation is contained in:

```text
src/drive.py
```

while the challenge programs request steering through:

```python
drive.steer(angle)
```

This keeps hardware actuation separate from the high-level navigation logic.

---

# 2. Drivetrain

The final drive motor is:

```text
JGB37-520
12 V
600 RPM nominal
```

The final robot uses **four-wheel drive**.

External gearing:

```text
36T driving gear → 24T driven gear
```

Ideal speed ratio:

```text
36 / 24 = 1.5
```

Therefore the theoretical geared output is:

```text
600 × 1.5 = 900 RPM
```

With 46 mm wheels:

```text
Wheel circumference
= π × 0.046
≈ 0.1445 m
```

At 900 RPM:

```text
900 / 60 = 15 revolutions/s

15 × 0.1445
≈ 2.17 m/s
```

The ideal wheel-surface speed is therefore approximately **2.17 m/s**.

Practical output was estimated closer to approximately **800 RPM**, corresponding to about **1.93 m/s**.

These figures are engineering calculations and estimates rather than laboratory speed measurements.

An earlier higher-speed motor suffered from loading and stall behaviour during development. The drivetrain was redesigned with reliability and repeatability given greater priority than maximum theoretical speed.

---

# 3. Electronics and Power

The main computer is:

```text
Raspberry Pi 5
4 GB RAM
```

Main hardware includes:

- Raspberry Pi 5
- Raspberry Pi Camera Module 3
- Second camera for parking
- JGB37-520 DC motor
- TB6612FNG motor driver
- DS3225 steering servo
- MPU6050 IMU
- 3S LiPo battery
- Regulated electronics power supply
- Front illumination LED

Battery specification:

```text
3S LiPo
11.1 V nominal
2200 mAh
```

Nominal stored energy:

```text
11.1 × 2.2 = 24.42 Wh
```

The battery supplies the robot's main power system, while a regulated lower-voltage rail supplies the Raspberry Pi and other electronics.

All control electronics share a common ground.

Development also included electrical failures. These incidents led to stricter procedures for:

- battery supervision,
- polarity checking,
- connector inspection,
- common-ground verification,
- controlled power-up,
- safer LiPo charging.

---

# 4. GPIO Architecture

Main Raspberry Pi GPIO assignments:

| FunctionBCM GPIO |        |
| ---------------- | ------ |
| Motor IN1        | GPIO5  |
| Motor IN2        | GPIO6  |
| Motor PWM        | GPIO13 |
| Steering servo   | GPIO22 |
| I2C SDA          | GPIO2  |
| I2C SCL          | GPIO3  |

Low-level actuation is handled by `drive.py`.

The challenge programs therefore use simple commands such as:

```python
drive.forward(speed)
drive.backward(speed)
drive.steer(angle)
drive.stop()
```

This prevents motor and servo implementation details from being duplicated across both competition programs.

The detailed electrical design is available in:

```text
schemes/
```

---

# 5. Computer Vision

Computer vision is the robot's primary environmental sensing method.

The general perception pipeline is:

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

Two separate vision modules are used because the two competition challenges have different requirements.

---

## Open Challenge Vision — `openVision.py`

The Open Challenge requires detection of:

```text
BLACK
BLUE
ORANGE
```

Black contours provide wall geometry.

Blue and orange features provide course-marker information.

The dedicated Open Challenge vision module avoids running unnecessary red, green and magenta detection.

This keeps the Open Challenge software simpler and allows its thresholds to be tuned independently.

---

## Obstacle Vision — `vision.py`

The Obstacle Challenge requires:

```text
RED
GREEN
BLACK
BLUE
ORANGE
MAGENTA
```

The obstacle vision system uses:

- colour thresholding,
- contour geometry,
- contour area,
- confidence checks,
- morphological noise filtering,
- largest-target selection.

Small or low-quality detections are filtered so that isolated colour noise does not immediately influence steering.

The goal is not only to identify colour but to identify a sufficiently large and geometrically meaningful object that can safely be used as a steering target.

---

# 6. Open Challenge Strategy

The Open Challenge is primarily a **vision-based wall-following problem**.

The controller:

1. captures a frame,
2. detects black walls,
3. determines the relevant wall target,
4. calculates visual steering error,
5. applies proportional steering,
6. detects blue/orange course markers,
7. counts valid marker events,
8. stops after completing the required course sequence.

The basic steering relationship is:

```text
Steering
=
Centre
+
KP × Visual Error
```

This allows continuous correction rather than relying on fixed timed turns.

When a wall temporarily disappears from view, a small direction-aware fallback correction is used.

Course-marker counting uses event-based logic so that one physical marker remaining visible across several consecutive camera frames is not counted multiple times.

A cooldown provides an additional safeguard against repeated counting.

Exact competition tuning values such as:

- proportional gain,
- line cooldown,
- speed,
- total event count,
- steering calibration

remain in the actual source code so that the README remains valid even after final field calibration.

---

# 7. Obstacle Challenge Strategy

The Obstacle Challenge combines:

- wall following,
- red-pillar avoidance,
- green-pillar avoidance,
- course tracking,
- heading-based manoeuvres,
- parking.

The robot continuously recalculates steering using image geometry.

Conceptually:

```text
Observe
   ↓
Detect wall / pillar
   ↓
Choose target
   ↓
Calculate steering
   ↓
Move
   ↓
Observe again
```

This replaced earlier approaches that depended more heavily on fixed steering durations.

A major development lesson was that pillars placed close to corners may become visible before the robot has fully completed its cornering movement.

If pillar avoidance reacts too aggressively at that instant, the new steering command can overpower the robot's current orientation and create an excessive turn.

The final strategy therefore uses:

- target geometry,
- minimum detection areas,
- proportional steering,
- continuous re-observation,

rather than reacting simply to the first coloured pixels seen.

---

# 8. MPU6050 Heading

The MPU6050 is used where orientation information is more useful than image position alone.

The helper module:

```text
heading.py
```

contains the:

```python
MPU6050Heading
```

class.

At startup it:

1. wakes the MPU6050,
2. measures the Z-axis gyro offset while stationary,
3. removes this offset from later measurements,
4. integrates Z-axis rotational velocity,
5. maintains heading between `0°` and `360°`.

The heading system is particularly useful during controlled forward and reverse manoeuvres and parking alignment.

Using heading allows certain movements to terminate based on measured orientation instead of only elapsed time.

---

# 9. Parking

Parking is implemented separately in:

```text
parking.py
```

The parking system combines:

- front-camera wall geometry,
- rear-camera parking geometry,
- magenta detection,
- MPU6050 heading,
- controlled forward/reverse motion.

General sequence:

```text
Course complete
      ↓
Enter parking stage
      ↓
Follow parking-side wall
      ↓
Rear camera detects magenta reference
      ↓
Stop
      ↓
Heading-controlled correction
      ↓
Forward / reverse alignment
      ↓
Final stop
```

Because Starlight uses Ackermann steering, it cannot rotate about its centre like a differential-drive robot.

Parking therefore requires multiple forward and reverse arcs rather than a single point turn.

Earlier parking attempts occasionally contacted the parking wall. This led to shorter movements, repeated observations and heading-based stopping conditions.

---

# 10. Important Engineering Decisions

| ChangeReason                                         |                                      |
| ---------------------------------------------------- | ------------------------------------ |
| Higher-speed motor → JGB37-520                       | Improved drivetrain reliability      |
| Earlier drivetrain → 4WD                             | Improved traction                    |
| 36T → 24T final gearing                              | Balanced speed and reliability       |
| Excessive steering range → limited travel            | Protected steering linkage           |
| One universal vision system → two vision modules     | Challenge-specific processing        |
| Fixed obstacle turns → continuous vision targets     | Better obstacle response             |
| Camera-only alignment → camera + IMU                 | Improved orientation control         |
| Flexible camera positioning → rigid geometry         | More repeatable vision               |
| Ambient light only → front illumination              | Improved detection consistency       |
| Earlier battery practice → stricter safety procedure | Reduced electrical risk              |
| Rear-wing experiment → removed                       | Testing did not justify retaining it |

These decisions show that mechanical design, electronics, perception and software cannot be treated as isolated systems.

A change in one subsystem can directly affect the behaviour of another.

---

# 11. Testing Process

Our normal testing sequence is:

```text
Component test
      ↓
Subsystem test
      ↓
Low-speed robot test
      ↓
Full challenge run
      ↓
Identify failure
      ↓
Modify
      ↓
Retest
```

Before full-speed testing we verify:

- battery condition,
- polarity,
- common ground,
- drivetrain freedom,
- gear engagement,
- motor direction,
- steering centre,
- steering limits,
- front camera,
- rear camera,
- black-wall detection,
- red/green detection,
- blue/orange marker detection,
- magenta detection,
- MPU6050 operation,
- correct competition program,
- required helper modules.

The Open Challenge completed repeated successful timed runs during development.

The Obstacle Challenge also completed **10+ successful full runs**.

Where a complete controlled dataset was not retained, no artificial success percentage is claimed.

Measurements, estimates and observations are kept separate wherever possible.

---

# 12. Reproducing the Robot

The required competition software package is:

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

The Open Challenge requires:

```python
import drive
import openVision as vision
```

The Obstacle Challenge requires:

```python
from heading import MPU6050Heading
import drive
import vision
import parking
```

Therefore all helper modules must be present in the GitHub repository.

A program that works only because a missing Python file already exists locally on the team's Raspberry Pi is not considered reproducible from the repository.

Recommended reproduction process:

1. Clone the repository.
2. Build the mechanical platform using `models/`.
3. Use `schemes/` to reproduce the electronics.
4. Install Raspberry Pi dependencies.
5. Verify the motor and steering using `drive.py`.
6. Test both cameras independently.
7. Test `openVision.py`.
8. Test `vision.py`.
9. Calibrate the MPU6050.
10. Verify `heading.py`.
11. Test the Open Challenge at reduced speed.
12. Test the Obstacle Challenge at reduced speed.
13. Validate parking.
14. Run the full challenge.
15. Commit the exact physically tested source.

The exact Git revision can be obtained using:

```bash
git rev-parse HEAD
```

If competition calibration changes the code, the new version should be tested, committed and pushed so that the robot and public repository remain synchronized.

---

# 13. Development History

| VersionMain development |                                                                  |
| ----------------------- | ---------------------------------------------------------------- |
| V0                      | LEGO mobility prototype                                          |
| V0.5                    | Rear-wing experiment                                             |
| V1                      | Camera-based autonomous control                                  |
| V2                      | Improved electronics mounting                                    |
| V3                      | Starlight chassis, 4WD drivetrain and final sensing architecture |
| Open development        | Wall following, marker detection and dedicated Open vision       |
| Obstacle development    | Pillar avoidance, IMU-assisted movement and parking              |

The Git history is intended to preserve the engineering process rather than only the final answer.

Useful commit-message styles include:

```text
feat(open): improve wall-following logic
feat(vision): add separate Open Challenge vision
feat(obstacle): tune red-green pillar avoidance
feat(parking): add rear-camera parking logic
fix(imu): update heading-based turn termination
fix(mech): update final 4WD drivetrain
docs: synchronize README with final project files
release: freeze tested competition build
```

---

# 14. Reproduction Resources

| ResourceLocation                |                             |
| ------------------------------- | --------------------------- |
| Main project overview           | `README.md`                 |
| Software dependencies           | `requirements.md`           |
| Raspberry Pi setup              | `docs/`                     |
| Open Challenge controller       | `src/Open_Challenge.py`     |
| Open Challenge vision           | `src/openVision.py`         |
| Obstacle Challenge controller   | `src/Obstacle_Challenge.py` |
| Obstacle vision                 | `src/vision.py`             |
| Drive control                   | `src/drive.py`              |
| MPU6050 heading helper          | `src/heading.py`            |
| Parking controller              | `src/parking.py`            |
| Electrical schematic            | `schemes/`                  |
| CAD and printable models        | `models/`                   |
| Vehicle photographs             | `v-photos/`                 |
| Team photographs                | `t-photos/`                 |
| Autonomous driving videos       | `video/`                    |
| Supporting engineering material | `other/`                    |

---

# Team Contributions

**Deyaan Agrawal**
Software development, computer vision, autonomous-control logic, debugging, tuning and track testing.

**Darsh Zaveri**
Mechanical and hardware integration, drivetrain, steering, electronics, wiring and physical testing.

**Aarav Jalan**
CAD, mechanical development, algorithm contributions, debugging, circuit construction, testing evidence and engineering documentation.

Robofun Lab provided access to facilities, mock runs and guidance during development roadblocks.

The submitted robot, software, testing process and engineering decisions remain the work of **Team Sentio**.

---

# Final Principle

Starlight was not created by getting every design decision correct on the first attempt.

It evolved through drivetrain failures, steering problems, camera-placement issues, colour-detection errors, electrical incidents, obstacle-navigation failures and parking experiments.

Each failure provided information that influenced the next version.

That process became the central engineering philosophy of the project:

> **Dream. Design. Build. Test. Fail. Understand. Improve. Repeat.**

---

**Team Sentio**
**Starlight**
**World Robot Olympiad — Future Engineers 2026**
**Robofun Lab (RFL), India**
