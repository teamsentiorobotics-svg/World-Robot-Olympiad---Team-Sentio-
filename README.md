# Team Sentio - WRO Future Engineers 2026

> **Starlight**  
> Autonomous vehicle developed by **Team Sentio** for the **World Robot Olympiad 2026 - Future Engineers** category.

**Team:** Deyaan Agrawal, Darsh Zaveri, Aarav Jalan  
**Mentors:** Sunil Solanki, Shyam Satasiya  
**Institution / Training Environment:** Robofun Lab (RFL), India  
**Robot:** Starlight  
**Competition:** World Robot Olympiad 2026 - Future Engineers  
**Current Documentation Revision:** Revision 27, 22 September 2026

---

## Engineering Philosophy

Starlight was not developed as one finished design.

The vehicle evolved through repeated mechanical, electrical, sensing and software revisions.

Our development process has consistently followed:

> **Build → Test → Observe → Find the failure → Modify → Retest**

The final system combines:

- four-wheel drive;
- Ackermann steering;
- a mechanical differential;
- dual wide-angle cameras;
- multi-ROI computer vision;
- an MPU6050 heading reference;
- motor-encoder feedback;
- three VL53L0X time-of-flight sensors;
- modular Open, Obstacle and Parking controllers;
- Raspberry Pi 5 based processing.

The project is documented as an integrated engineering system rather than as a collection of independent components.

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
│   ├── N_Vision_final.py
│   ├── Final_Obstacle_Challenge.py
│   ├── Sentio_Open_2026.py
│   ├── openvision.py
│   ├── parking_final.py
│   ├── heading.py
│   ├── Cal_APOC.py
│   ├── servo_test.py
│   ├── encoder_test.py
│   └── TUF_test.py
│
├── Models/
│
├── docs/
│   ├── BOM_purchase_links.md
│   ├── wiring_guide.md
│   ├── differential_drive_system.md
│   ├── Software_Dependencies.md
│   └── pi_setup_instruction.md
│
├── schemes/
├── v-photos/
├── t-photos/
├── videos/
└── other/
```

| Location | Purpose |
|---|---|
| `src/` | Competition controllers, sensing modules, calibration tools and component tests |
| `Models/` | Chassis, robot-design and printable STL files |
| `docs/` | BOM, wiring, drivetrain background, dependencies and Raspberry Pi setup |
| `schemes/` | Electrical and wiring references |
| `v-photos/` | Vehicle photographs |
| `t-photos/` | Team photographs |
| `videos/` | Physical autonomous-driving evidence |
| `other/` | Supporting engineering, testing and planning material |
| `README.md` | Main repository-level project overview |
| `CHANGELOG.md` | Dated development history |
| `requirements.md` | Software dependency record |

---

# 1. System Overview

Starlight is a compact four-wheel autonomous vehicle designed around **car-like steering mechanics and camera-led navigation**.

The current configuration combines several different types of observations:

```text
CAMERAS
   ↓
Track geometry, walls, pillars and colour cues

MPU6050
   ↓
Relative heading and orientation change

MOTOR ENCODER
   ↓
Shaft rotation and movement feedback

3 × VL53L0X
   ↓
Short-range distance information

          ↓

     RASPBERRY PI 5

          ↓

Navigation state + steering + propulsion

          ↓

4WD + ACKERMANN STEERING
```

Each sensor answers a different question.

The system does not treat one sensor as an exact replacement for another.

---

# 2. Current Mechanical Architecture

The current vehicle uses:

- four-wheel drive;
- front Ackermann steering;
- a mechanical differential;
- custom structural components;
- LEGO Technic drivetrain and mechanism elements where appropriate;
- rigid camera supports;
- rigid distance-sensor mounts;
- a geared DC drive motor;
- encoder feedback.

The goal of the mechanical design is not only movement.

It must also keep the **camera geometry, sensor directions, drivetrain alignment and steering geometry repeatable**.

---

## Ackermann Steering

Starlight turns like a small car.

During a turn:

- the inside front wheel follows a smaller-radius path;
- the outside front wheel follows a larger-radius path;
- the inside wheel therefore requires a larger steering angle.

Ackermann geometry allows the front wheels to approximately follow their respective turning paths instead of forcing both wheels through the same angle.

This reduces tyre scrub and improves repeatability during curved motion.

---

## Mechanical Differential

Steering angle and driven-wheel speed solve different problems.

The outside driven wheel travels farther than the inside driven wheel during a turn.

The mechanical differential allows the two sides of the drivetrain to rotate at different speeds while remaining powered by the same motor.

```text
ACKERMANN STEERING
→ sets the wheel directions

DIFFERENTIAL
→ allows different driven-wheel speeds
```

Both mechanisms contribute to smoother car-like turning.

---

# 3. Drivetrain

The current drivetrain uses a:

```text
12 V geared DC encoder motor
Nominal output speed: 600 RPM
External gear ratio: 1:1
```

The final external transmission intentionally uses a **1:1 ratio**.

This differs from an earlier speed-increasing drivetrain configuration.

The revised design gives greater priority to:

- usable wheel torque;
- drivetrain reliability;
- controllable movement;
- reduced motor loading;
- repeatable challenge behaviour.

A nominal motor speed is a component rating and should not be interpreted as a measured vehicle ground speed.

---

## Four-Wheel Drive

Motor rotation is transferred through the mechanical drivetrain to all four wheels.

Four-wheel drive was retained because it provides:

- improved traction;
- more consistent propulsion;
- better load distribution;
- greater reliability during steering and obstacle manoeuvres.

---

## Motor Encoder

The drive motor contains a quadrature encoder.

The encoder reports shaft motion and direction through pulses.

It is used for:

- movement feedback;
- drivetrain testing;
- encoder-controlled movement requests;
- checking motor response;
- repeatable motion during selected manoeuvres.

Encoder rotation is not identical to physical vehicle displacement.

Wheel slip, tyre deformation, transmission play and surface conditions can all cause body travel to differ from shaft-based estimates.

---

# 4. Main Electronics

The current computing platform is:

```text
Raspberry Pi 5
4 GB RAM
```

The current robot includes:

| Qty. | Component | Function |
|---:|---|---|
| 1 | Raspberry Pi 5, 4 GB | Main computer |
| 2 | Raspberry Pi Camera Module 3 Wide | Track and parking perception |
| 3 | VL53L0X ToF sensors | Short-range distance sensing |
| 1 | 12 V geared DC encoder motor, 600 RPM | Propulsion |
| 1 | Integrated quadrature encoder | Shaft-motion feedback |
| 1 | TB6612FNG motor driver | Motor direction and PWM |
| 1 | DS3225 digital servo | Ackermann steering |
| 1 | MPU6050-based heading sensor | Relative angular motion |
| 1 | 3S LiPo battery | Main energy source |
| 1 | Regulated Raspberry Pi supply | Computer power |
| 1 | Start button | Physical run input |
| 1 | Status / illumination LED | Indication and illumination |

---

# 5. Power System

Main battery:

```text
3S LiPo
11.1 V nominal
2200 mAh
```

Nominal stored energy:

```text
11.1 V × 2.2 Ah
≈ 24.42 Wh
```

Starlight separates the main electrical loads into different functional branches.

```text
               BATTERY
                  │
        ┌─────────┴─────────┐
        │                   │
    MOTOR RAIL        REGULATED RAIL
        │                   │
 Motor driver          Raspberry Pi
 Drive motor           Cameras
                       Sensors
```

Connected control electronics share an appropriate common electrical reference.

Voltage stability is particularly important because motor starts, motor reversals and servo movement can produce rapidly changing current demand.

---

# 6. GPIO and Interfaces

Main Raspberry Pi control assignments include:

| Function | BCM GPIO |
|---|---:|
| Motor IN1 | GPIO5 |
| Motor IN2 | GPIO6 |
| Motor PWM | GPIO13 |
| Steering servo | GPIO22 |
| I2C SDA | GPIO2 |
| I2C SCL | GPIO3 |
| ToF 1 XSHUT | GPIO16 |
| ToF 2 XSHUT | GPIO20 |
| ToF 3 XSHUT | GPIO21 |

The MPU6050 uses the shared I2C bus.

The VL53L0X sensors also use I2C.

Because multiple VL53L0X sensors initially use the same default address, their XSHUT lines allow the sensors to be activated sequentially and assigned separate working addresses.

---

# 7. Camera Architecture

Starlight uses:

```text
2 × Raspberry Pi Camera Module 3 Wide
```

The camera system is positioned to observe the working area of the track while allowing different image regions to perform different tasks.

The documented viewing direction is approximately:

```text
60° from horizontal
```

The relatively downward-facing view prioritizes:

- nearby walls;
- pillar bases;
- track markers;
- parking geometry;
- immediate steering information.

The trade-off is reduced distant look-ahead and stronger perspective effects.

---

# 8. Multi-ROI Computer Vision

The current vision architecture uses a **720 × 360 image** divided into task-specific regions of interest.

A simplified representation is:

```text
┌──────────────────────────────────────────────┐
│ L1        L2        C        R2        R1    │
│                                              │
│            O / B course region               │
│                                              │
│              BODY EXCLUSION                  │
└──────────────────────────────────────────────┘
```

Different regions answer different navigation questions.

Typical responsibilities include:

- outer-wall observation;
- inner-wall observation;
- center reference;
- orange / blue course cues;
- pillar detection;
- body exclusion.

The robot's own structure may appear dark in the image.

Exclusion regions therefore prevent visible robot components from being interpreted as track walls.

---

# 9. Vision Processing

The current primary multi-ROI vision module is:

```text
src/N_Vision_final.py
```

The processing pipeline can be summarized as:

```text
Camera frame
     ↓
HSV / LAB conversion
     ↓
Task-specific ROI selection
     ↓
Colour / darkness thresholding
     ↓
Morphological filtering
     ↓
Contour extraction
     ↓
Area and geometry filtering
     ↓
Region-aware detection
     ↓
Navigation observation
```

The system uses a combination of:

- HSV colour information;
- LAB colour information;
- darkness information;
- contour size;
- contour geometry;
- image position;
- region identity.

This prevents navigation from depending only on whether a few pixels match a colour threshold.

---

# 10. Calibration

Field lighting can change the appearance of the same object.

The repository therefore includes:

```text
src/Cal_APOC.py
```

This provides interactive LAB / HSV calibration controls.

Calibration is used to adjust colour ranges for the actual competition environment before relying on those thresholds during autonomous navigation.

The vision system should be calibrated after changes involving:

- lighting;
- camera position;
- camera angle;
- exposure;
- physical track material;
- major mechanical reconstruction.

---

# 11. Software Architecture

The final software is divided into mission-level controllers and reusable hardware or sensing modules.

```text
                  N_Vision_final.py
                         │
               Multi-ROI perception
                         │
        ┌────────────────┴────────────────┐
        │                                 │
Sentio_Open_2026.py          Final_Obstacle_Challenge.py
        │                                 │
 Open Challenge                    Obstacle Challenge
        │                                 │
        └──────────────┬──────────────────┘
                       │
                parking_final.py
                       │
                   heading.py
                       │
               Drive interface
                       │
          Motor + encoder + steering
```

This makes faults easier to isolate.

A poor autonomous turn may originate from:

- perception;
- target selection;
- heading estimation;
- steering;
- drivetrain response;
- state logic.

Separating those responsibilities allows individual layers to be tested before a full challenge run.

---

# 12. Open Challenge

The current Open Challenge controller is:

```text
src/Sentio_Open_2026.py
```

Its primary Open vision module is:

```text
src/openvision.py
```

`N_Vision_final.py` can also be used through the compatible observation interface.

---

## Open Challenge Strategy

The Open Challenge primarily uses continuous wall-relative correction.

```text
Observe walls + course markers
            ↓
Determine course direction
            ↓
Select active wall reference
            ↓
Calculate image error
            ↓
Apply proportional steering
            ↓
Move
            ↓
Detect valid course event
            ↓
Repeat
```

A general proportional relationship is:

```text
steering request
=
center request
+
KP × image error
```

The controller repeatedly updates the steering response as the camera geometry changes.

This is different from relying entirely on predetermined timed turns.

---

## Course Direction

The controller uses track cues to determine the applicable course direction.

Direction information affects:

- wall selection;
- target image position;
- fallback behaviour;
- obstacle context;
- parking approach.

---

## Course Event Counting

A physical marker can remain visible across many consecutive camera frames.

The controller therefore distinguishes:

```text
NEW EVENT
```

from:

```text
SAME EVENT STILL VISIBLE
```

Cooldown and event-transition logic prevent one marker from being repeatedly counted simply because it remains in the image.

---

# 13. Obstacle Challenge

The current controller is:

```text
src/Final_Obstacle_Challenge.py
```

The Obstacle Challenge combines:

- wall geometry;
- red pillar detection;
- green pillar detection;
- course direction;
- heading;
- encoder-assisted movement;
- parking transition logic;
- repeated visual observations.

---

## Obstacle Selection

Red and green objects are treated as different navigation targets.

The controller considers:

- object colour;
- object position;
- bounding-box geometry;
- region identity;
- active manoeuvre;
- course direction.

A pillar becoming visible does not automatically mean that the robot should immediately abandon its current manoeuvre.

This matters especially near corners, where obstacle observations may appear before an existing turn is complete.

---

## Continuous Perception

The final obstacle architecture repeatedly returns to sensing.

```text
OBSERVE
   ↓
SELECT RELEVANT FEATURE
   ↓
CHOOSE ACTIVE CONTROL STATE
   ↓
STEER / MOVE
   ↓
OBSERVE AGAIN
```

The changing camera view is therefore part of the feedback loop.

---

# 14. MPU6050 Heading

Shared heading logic is contained in:

```text
src/heading.py
```

The heading module:

1. initializes communication with the MPU6050;
2. measures stationary gyro bias;
3. subtracts the estimated bias;
4. reads angular velocity;
5. integrates angular velocity over elapsed time;
6. maintains a relative heading estimate.

Conceptually:

```text
relative heading
=
previous heading
+
corrected angular velocity × elapsed time
```

The result is a **relative orientation estimate**.

It is not treated as an exact global compass or position measurement.

---

## Why Heading Feedback Is Useful

A fixed motor time does not always produce the same turn.

Variation may result from:

- battery condition;
- motor loading;
- tyre contact;
- friction;
- drivetrain resistance;
- surface conditions.

Heading feedback allows selected manoeuvres to end based on the robot's observed orientation rather than time alone.

---

# 15. Parking

The current parking controller is:

```text
src/parking_final.py
```

Parking combines:

- camera geometry;
- magenta parking references;
- wall observations;
- heading feedback;
- three VL53L0X distance sensors;
- forward and reverse Ackermann arcs;
- distance-confirmed stopping.

---

## Parking Objective

The final objective is to stop with the vehicle aligned **parallel to the magenta wall**.

Starlight cannot rotate about its center like a differential-drive robot.

Parking therefore requires a sequence of controlled forward and reverse arcs.

---

## Parking Sequence

```text
COURSE COMPLETE
       ↓
IDENTIFY APPROACH DIRECTION
       ↓
POSITION VEHICLE
       ↓
ALIGN USING STEERING + HEADING
       ↓
READ SHORT-RANGE DISTANCE
       ↓
CONFIRM DISTANCE CONDITION
       ↓
FORWARD / REVERSE ADJUSTMENT
       ↓
FINAL PARALLEL ALIGNMENT
       ↓
STOP
```

The range sensors complement the camera and heading system.

They do not replace them.

```text
CAMERA
→ Where is the feature?

HEADING
→ Which direction is the robot pointing?

ToF
→ How large is the nearby gap?

ENCODER
→ How much shaft movement occurred?
```

---

# 16. ToF Distance Sensing

The final vehicle uses:

```text
3 × VL53L0X
```

The distance sensors support short-range decisions during parking and wall-relative movement.

The current parking architecture includes concepts such as:

- sensor activation before use;
- repeated distance readings;
- confirmation instead of trusting one isolated reading;
- separation between qualifying detections;
- range-based movement termination;
- controlled forward and reverse stopping phases.

This makes close-range stopping less dependent on image geometry alone.

---

# 17. Clockwise and Anticlockwise Parking

The two possible course directions require different routes into the parking area.

```text
                    COURSE COMPLETE
                          │
                 Determine direction
                    ┌─────┴─────┐
                    │           │
                   CW          ACW
                    │           │
          CW entry position   U-turn
                    │           │
                    │      Follow wall
                    │           │
                    │    Opposite corner
                    └─────┬─────┘
                          │
                Shared final parking
                          │
              Parallel to magenta wall
                          │
                         STOP
```

The anticlockwise path performs the required repositioning before joining the same final parking logic used by the clockwise branch.

---

# 18. Component Test Programs

Full challenge runs are not the first debugging step.

The repository includes dedicated test programs.

---

## Steering Test

```text
src/servo_test.py
```

Used to verify:

- steering direction;
- center position;
- steering range;
- mechanical clearance;
- linkage behaviour.

---

## Encoder Test

```text
src/encoder_test.py
```

Used to verify:

- encoder pulse response;
- direction;
- motor movement;
- encoder-based drive control.

---

## Distance Sensor Test

```text
src/TUF_test.py
```

Used to verify:

- VL53L0X initialization;
- XSHUT sequencing;
- unique sensor addressing;
- distance readings;
- sensor orientation.

---

## Vision Calibration

```text
src/Cal_APOC.py
```

Used to verify and tune:

- HSV thresholds;
- LAB thresholds;
- field colour appearance.

---

# 19. Testing Workflow

Team Sentio uses a layered validation process.

```text
COMPONENT TEST
      ↓
SUBSYSTEM TEST
      ↓
LOW-SPEED INTEGRATED TEST
      ↓
FULL CHALLENGE RUN
      ↓
OBSERVE FAILURE
      ↓
IDENTIFY RESPONSIBLE LAYER
      ↓
MODIFY
      ↓
RETEST
```

Before a complete autonomous run, checks include:

- battery state;
- secure electrical connections;
- regulated Raspberry Pi supply;
- common electrical reference;
- motor direction;
- drivetrain freedom;
- gear engagement;
- steering linkage;
- steering limits;
- encoder response;
- camera operation;
- vision calibration;
- MPU6050 communication;
- ToF communication;
- sensor orientation;
- correct source-code revision.

---

# 20. Physical Timing Records

The engineering record retains successful-run timing observations from development and practice.

The retained datasets contain:

```text
Development cohort: 19 successful runs
Practice cohort:    12 successful runs
```

Recorded summaries:

| Cohort | n | Mean | Median | SD | Range |
|---|---:|---:|---:|---:|---:|
| Development | 19 | 25.05 s | 23 s | 5.74 s | 18-37 s |
| Practice | 12 | 23.00 s | 23 s | 1.28 s | 21-25 s |

These are **successful retained runs only**.

They are not presented as the success rate of all attempted runs.

Different runs also belong to changing development configurations, so the timing data should not be treated as a controlled comparison of one isolated design change.

---

# 21. Nationals Competition Record

The Nationals results belong to an **earlier competition configuration** and should not be interpreted as performance measurements of the current post-Nationals APOC revision.

| Round | Recorded Score | Recorded Time | Recorded Outcome |
|---|---:|---:|---|
| Open Run 1 | 0 / 30 | - | Inner-wall contact interrupted run |
| Open Run 2 | 30 / 30 | 56 s | Completed clockwise course |
| Obstacle Run 2 | 29 / 62 | 66 s to stop | Green-obstacle contact, parking not achieved |

These competition outcomes influenced the later redesign of:

- camera geometry;
- vision regions;
- drivetrain;
- sensing;
- obstacle behaviour;
- parking logic.

---

# 22. Post-Nationals / APOC Redesign

The September 2026 configuration is a new engineering revision rather than a retroactive description of the Nationals vehicle.

Major changes include:

- revised chassis;
- revised camera placement;
- rigid sensing geometry;
- dual Camera Module 3 Wide architecture;
- multi-ROI vision;
- explicit body-exclusion regions;
- LAB / HSV calibration tools;
- revised wall detection;
- revised pillar detection;
- revised Open Challenge controller;
- revised Obstacle Challenge controller;
- three VL53L0X distance sensors;
- encoder-assisted movement;
- revised parking-distance logic;
- 600 RPM motor;
- 1:1 external drivetrain ratio.

---

# 23. Important Engineering Decisions

| Engineering Decision | Reason |
|---|---|
| Four-wheel drive | Improved propulsion consistency and traction |
| Ackermann steering | Car-like turning geometry |
| Mechanical differential | Allows unequal wheel speeds during turns |
| 600 RPM encoder motor | Better balance of movement, torque and controllability |
| 1:1 external gearing | Retains more wheel torque than the earlier speed-increasing stage |
| Rigid camera supports | More repeatable visual geometry |
| 60° camera view | Emphasizes nearby track features |
| Multi-ROI vision | Gives different visual regions specific jobs |
| Body exclusion | Prevents the robot from detecting itself as a wall |
| HSV + LAB calibration | Better field-specific colour adjustment |
| MPU6050 heading | Orientation-sensitive manoeuvre feedback |
| Encoder feedback | Shaft-motion information |
| Three VL53L0X sensors | Close-range gap and parking information |
| Modular software | Easier debugging and replacement of individual subsystems |
| Component test scripts | Fault isolation before full runs |

---

# 24. CAD and Mechanical Files

Mechanical design resources are stored in:

```text
Models/
```

The directory contains the available mechanical-design and printable resources associated with Starlight.

The repository also preserves earlier CAD and prototype material where useful for documenting the development process.

Earlier models should not automatically be interpreted as the exact geometry of the current robot.

Development history is retained deliberately so that major changes remain traceable.

---

# 25. Electrical Documentation

Electrical and wiring information is contained in:

```text
docs/
schemes/
```

Important supporting documents include:

```text
docs/BOM_purchase_links.md
docs/wiring_guide.md
docs/Software_Dependencies.md
docs/pi_setup_instruction.md
```

Together, these describe:

```text
COMPONENTS
     +
POWER / SIGNAL CONNECTIONS
     +
GPIO ASSIGNMENTS
     +
SOFTWARE CONTROL
```

A reproducible robot requires all four.

---

# 26. Raspberry Pi Setup

Detailed Raspberry Pi setup information is provided in:

```text
docs/pi_setup_instruction.md
```

and:

```text
docs/Software_Dependencies.md
requirements.md
```

The software stack includes technologies such as:

- Python 3;
- OpenCV;
- NumPy;
- Picamera2;
- Raspberry Pi GPIO support;
- I2C / SMBus interfaces;
- sensor-specific Python libraries used by the final system.

The setup documentation should be followed before attempting to run the competition controllers.

---

# 27. Recommended Reproduction Workflow

A reproduction of Starlight should use the repository as a complete engineering package.

```text
1. Review README.md
        ↓
2. Review BOM and wiring
        ↓
3. Review Models/
        ↓
4. Assemble mechanical system
        ↓
5. Install Raspberry Pi environment
        ↓
6. Connect electronics
        ↓
7. Verify steering
        ↓
8. Verify motor + encoder
        ↓
9. Verify cameras
        ↓
10. Verify MPU6050
        ↓
11. Verify all VL53L0X sensors
        ↓
12. Calibrate vision
        ↓
13. Run low-speed integration
        ↓
14. Run challenge controller
        ↓
15. Record software + hardware revision
```

A challenge result should remain linked to the exact hardware arrangement, camera geometry, calibration and software revision that produced it.

---

# 28. Current Competition Software

The current project software map is:

```text
src/
├── N_Vision_final.py
├── Final_Obstacle_Challenge.py
├── Sentio_Open_2026.py
├── openvision.py
├── parking_final.py
├── heading.py
├── Cal_APOC.py
├── servo_test.py
├── encoder_test.py
└── TUF_test.py
```

### `N_Vision_final.py`

Final multi-ROI computer vision for walls, pillars and track colours.

### `Final_Obstacle_Challenge.py`

Main Obstacle Challenge controller.

### `Sentio_Open_2026.py`

Main Open Challenge controller.

### `openvision.py`

Primary Open Challenge vision module.

### `parking_final.py`

Direction-dependent parking entry and shared final parking routine.

### `heading.py`

Shared MPU6050 relative-heading estimator.

### `Cal_APOC.py`

Interactive LAB / HSV field-calibration tool.

### `servo_test.py`

Steering direction, center and range testing.

### `encoder_test.py`

Encoder and motor-control testing.

### `TUF_test.py`

VL53L0X distance-sensor testing.

---

# 29. Development History

Starlight progressed through multiple complete vehicle configurations.

| Stage | Main Development |
|---|---|
| Early LEGO platform | Wheel motion, steering and basic structure |
| Hybrid construction | LEGO mechanisms combined with printed supports |
| Nationals configuration | Integrated navigation, obstacle response and parking |
| Post-Nationals redesign | New chassis, camera geometry, vision regions and sensing |
| Current APOC configuration | Multi-ROI perception, encoder feedback and three-ToF architecture |

The important point is that improvements were not isolated.

Changing one subsystem changed the conditions faced by others.

```text
CAMERA POSITION
→ changes image geometry

MOTOR / GEARING
→ changes movement response

STEERING
→ changes the path produced by the same command

POWER
→ changes computer and actuator reliability

SOFTWARE
→ must respond to all of the above
```

The robot therefore evolved as a complete system.

---

# 30. Team Contributions

## Deyaan Agrawal

Primary areas included:

- software;
- autonomous algorithms;
- navigation logic;
- debugging;
- tuning;
- track testing.

## Darsh Zaveri

Primary areas included:

- hardware;
- LEGO mechanisms;
- mechanical assembly;
- circuits;
- wiring;
- drivetrain;
- physical troubleshooting;
- testing.

## Aarav Jalan

Primary areas included:

- CAD;
- algorithm contributions;
- custom structures;
- circuits;
- system integration;
- engineering documentation;
- technical records.

---

# 31. Mentors and Robofun Lab

### Sunil Solanki

Technical guidance, testing support and design review.

### Shyam Satasiya

Technical guidance, testing support and design review.

Robofun Lab provided the environment, facilities and technical guidance used during development and testing.

The robot, source code, design decisions, testing process and engineering record remain the work of **Team Sentio**.

---

# 32. Evidence Philosophy

The project distinguishes between different kinds of engineering evidence.

### Recorded observation

Something physically observed during development or competition.

### Specification

A component rating or documented configuration value.

### Calculation

A result derived mathematically from stated inputs and assumptions.

### Computer study

A result generated inside a simplified numerical model.

These categories should not be treated as interchangeable.

For example:

```text
600 RPM
```

is a motor specification.

It is not automatically the measured wheel speed of the robot.

Likewise, an encoder count is shaft-motion information and is not automatically exact ground displacement.

---

# 33. Repository Synchronization

The repository should remain synchronized with the software physically running on Starlight.

The active Git revision can be checked using:

```bash
git rev-parse HEAD
```

Calibration or controller changes should be physically tested before being treated as a new final competition configuration.

A useful run record should identify:

```text
Hardware configuration
+
Camera arrangement
+
Calibration
+
Software revision
+
Observed result
```

Without those together, reproducing a result becomes guesswork.

---

# Final Engineering Principle

Starlight was not created by getting every design choice correct on the first attempt.

The project progressed through:

- drivetrain problems;
- steering changes;
- camera-position experiments;
- colour-detection errors;
- power issues;
- obstacle-navigation failures;
- parking experiments;
- mechanical redesigns;
- sensor additions;
- repeated software tuning.

Each failure supplied information for the next revision.

> **Dream. Design. Build. Test. Fail. Understand. Improve. Repeat.**

---

**Team Sentio**  
**Starlight**  
**World Robot Olympiad - Future Engineers 2026**  
**Robofun Lab (RFL), India**
