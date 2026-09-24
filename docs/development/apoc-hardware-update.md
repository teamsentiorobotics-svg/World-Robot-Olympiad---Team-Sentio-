# APOC Hardware Update

**Project:** Starlight  
**Team:** Sentio 6010  
**Competition:** WRO Future Engineers 2026  
**Update:** Post-Nationals → Asia Pacific Open Championship (APOC)  
**Hardware Configuration:** Revision 29  
**Update Date:** September 2026

---

## Overview

Following the WRO India National Championship, Team Sentio did not simply retune the existing Starlight configuration.

The Nationals runs exposed limitations in:

- camera field geometry;
- obstacle clearance;
- parking information;
- drivetrain operating margin;
- movement repeatability;
- sensor placement;
- mechanical packaging.

The robot was therefore redesigned as a **complete integrated system** before APOC.

The post-Nationals development cycle was:

```text
Nationals configuration
        ↓
Competition observations
        ↓
Identify mechanical and sensing limitations
        ↓
Redesign chassis and mounts
        ↓
Reposition cameras
        ↓
Add distance sensing
        ↓
Change drivetrain operating point
        ↓
Add encoder feedback
        ↓
Update perception and parking architecture
        ↓
Component testing
        ↓
Integrated APOC configuration
```

The result is the current **APOC-oriented Starlight architecture**.

---

# Major Hardware Changes

| Subsystem | Nationals / Earlier Approach | APOC Configuration | Reason for Change |
| --- | --- | --- | --- |
| **Chassis** | Earlier competition chassis | Redesigned chassis and mounting structure | Support revised camera, sensor and drivetrain geometry |
| **Camera position** | Earlier mounting arrangement | Rear-mounted / rearward camera arrangement | Improve useful field geometry |
| **Camera mounts** | Earlier printed/support structures | Redesigned rigid mounts | Make camera pose more repeatable |
| **Vision geometry** | Earlier broad viewing arrangement | Camera geometry designed around task-specific ROIs | Reduce irrelevant visual information |
| **Distance sensing** | Camera and heading relied on more heavily | **3 × VL53L0X ToF sensors** | Directly measure nearby physical gaps |
| **Drive motor** | Earlier higher-speed drivetrain configuration | **12 V, 600 RPM geared encoder motor** | Improve usable torque and operating margin |
| **External gearing** | Earlier speed-increasing transmission | **1:1 gearing** | Prioritize torque and controllability |
| **Drive feedback** | Primarily time-based movement | **Quadrature encoder feedback** | Improve movement repeatability |
| **Parking sensing** | Camera + heading | Camera + heading + ToF + movement feedback | Measure both orientation and clearance |
| **Sensor mounts** | Added around earlier packaging | Mounting redesigned around sensing direction | Ensure sensors observe the intended physical surfaces |

---

# Development Background

Starlight has passed through several major physical configurations.

```text
Fully LEGO prototype
        ↓
Hybrid LEGO + printed structure
        ↓
Nationals configuration
        ↓
Post-Nationals redesign
        ↓
Current APOC configuration
```

Photographs of the earlier **fully LEGO**, **hybrid LEGO + 3D-printed**, and later robot configurations are retained in:

```text
v-photos/
```

These images are included as development evidence rather than being presented as photographs of the current competition robot.

The development history matters because the final design was reached through repeated physical iteration, not through a single finished CAD model.

---

# Why the Robot Was Redesigned After Nationals

Nationals produced useful whole-system evidence.

The earlier robot demonstrated that it could complete the Open Challenge, but the Obstacle Challenge also exposed physical interaction and parking limitations.

A correct visual detection does not automatically produce a safe vehicle path.

The complete chain is:

```text
Camera observes feature
        ↓
Software classifies feature
        ↓
Controller selects action
        ↓
Steering mechanism changes wheel direction
        ↓
Drivetrain moves vehicle
        ↓
Physical clearance determines success
```

A failure anywhere in this chain can appear as a navigation failure.

For APOC, several problems were therefore addressed through **hardware architecture changes**, not merely software tuning.

---

# 1. Chassis Redesign

The post-Nationals chassis was redesigned to support the revised sensing architecture.

The objective was not simply to make Starlight look different.

The chassis determines:

- camera location;
- camera height;
- camera angle;
- sensor direction;
- electronics position;
- drivetrain alignment;
- wire routing;
- wheel clearance;
- steering clearance;
- maintenance access.

The APOC redesign therefore treated the chassis as part of the sensing and control system.

```text
Required observation
        ↓
Required sensor position
        ↓
Required mount geometry
        ↓
Required chassis geometry
```

---

## Mechanical Design Principle

Starlight uses a hybrid construction philosophy:

```text
3D-printed structure
        +
LEGO Technic mechanisms
```

Printed components are used where **repeatable geometry** is important.

LEGO Technic components are retained where:

- adjustment;
- rapid repair;
- shaft alignment;
- steering modification;
- gear servicing

are useful.

This allows the robot to combine rigid reference geometry with serviceable mechanisms.

---

# 2. Camera Relocation

One of the largest APOC changes was the camera arrangement.

The earlier physical configuration restricted the useful field of view.

For the APOC design, the camera mounts were relocated toward the **rear of the robot**, allowing the cameras to look forward over more of the useful working area.

The current arrangement uses:

```text
2 × Raspberry Pi Camera Module 3 Wide
```

with rigid camera supports.

---

## Why Camera Position Is a Hardware Decision

A perception problem is not always a software problem.

Moving a camera changes:

- where walls appear in the image;
- where pillar bases appear;
- how early an obstacle becomes visible;
- perspective distortion;
- how much of the robot enters the frame;
- which pixels should belong to each ROI.

Therefore:

```text
Camera position
      ↓
Image geometry
      ↓
ROI placement
      ↓
Detection
      ↓
Steering decision
```

Threshold tuning alone cannot compensate for unsuitable physical camera geometry.

---

# 3. Camera Angle

The current camera arrangement uses a viewing direction of approximately:

```text
60° from horizontal
```

The purpose is to emphasize the nearby track region where immediate navigation information appears.

This improves observation of:

- floor geometry;
- wall boundaries;
- pillar bases;
- coloured course markers;
- parking references.

The trade-off is:

- reduced long-distance look-ahead;
- greater perspective change as objects approach;
- increased importance of rigid mounting.

For this reason, camera angle is treated as a **controlled mechanical parameter**.

---

# 4. Redesigned Camera Mounts

The camera mounts were redesigned together with the chassis.

A camera mount must do more than physically hold a camera.

It must preserve:

```text
Position
+
Angle
+
Orientation
+
Rigidity
```

because small movements can shift the apparent pixel location of a wall or obstacle.

The mount therefore forms part of the perception system.

---

# 5. Robot-Body Visibility

The revised rearward camera position can allow parts of Starlight itself to enter the camera frame.

Instead of moving the cameras back to a worse viewing position, the design accepts the useful camera geometry and removes the known robot-body area in software.

```text
Camera position optimized
        ↓
Robot body partly visible
        ↓
Known body region excluded
        ↓
Remaining image used for navigation
```

This allows physical camera placement to be selected for useful field geometry rather than merely for producing an unobstructed photograph.

---

# 6. Three VL53L0X Distance Sensors

The APOC robot adds:

```text
3 × VL53L0X
Time-of-Flight distance sensors
```

These sensors provide local physical distance information.

They are particularly useful during:

- parking;
- wall-relative positioning;
- final stopping;
- close-range manoeuvres.

---

## Why Distance Sensors Were Added

A camera can answer:

```text
What feature can I see?
```

The IMU can answer:

```text
How much have I turned?
```

The encoder can answer:

```text
How much has the motor shaft moved?
```

The ToF sensors answer a different question:

```text
How far away is the nearby physical surface?
```

These measurements are complementary.

---

# 7. Three Sensors on One I2C Bus

All three VL53L0X sensors initially use the same default I2C address.

To operate three identical sensors on the same bus, Starlight uses separate **XSHUT** lines.

The current hardware allocation is:

| Sensor Control | GPIO |
| --- | ---: |
| **ToF XSHUT 1** | GPIO16 |
| **ToF XSHUT 2** | GPIO20 |
| **ToF XSHUT 3** | GPIO21 |

Initialization follows the general sequence:

```text
Disable all sensors
        ↓
Enable sensor 1
        ↓
Assign unique address
        ↓
Enable sensor 2
        ↓
Assign unique address
        ↓
Enable sensor 3
        ↓
Assign unique address
        ↓
Read all sensors independently
```

The dedicated hardware test is:

```text
src/TUF_test.py
```

---

# 8. Distance-Sensor Mounting

Adding three sensors is useful only if each sensor observes the intended surface.

Mounting direction therefore became part of the hardware redesign.

A valid reading from a poorly positioned sensor may still describe the **wrong object**.

Therefore each sensor must be checked for:

- orientation;
- field of view;
- expected surface;
- minimum useful range;
- interference from robot structure;
- consistency during the relevant parking phase.

The physical mount and software state must agree on what the measurement represents.

---

# 9. New Drive Motor

The drivetrain was revised around a:

```text
12 V
600 RPM
geared DC motor
with integrated quadrature encoder
```

The earlier drivetrain experienced high-load stall behaviour.

That failure demonstrated that maximum speed was not the only important design requirement.

---

## Previous Failure Chain

```text
High mechanical load
        ↓
Motor stall
        ↓
High current stress
        ↓
Motor-driver damage
        ↓
Drivetrain redesign
```

For APOC, the drivetrain operating point was changed to favour:

- available torque;
- reliability;
- controllability;
- movement feedback.

---

# 10. 1:1 External Gearing

The current external gear ratio is:

```text
1 : 1
```

An earlier configuration used a speed-increasing transmission.

The 1:1 arrangement reduces the emphasis on maximum theoretical wheel speed and preserves more available wheel torque.

```text
Earlier design
Speed increase
      ↓
Higher theoretical speed
      ↓
Lower torque margin

Current design
1:1 gearing
      ↓
More torque margin
      ↓
More controllable movement
```

The APOC drivetrain therefore treats reliable completion as more important than theoretical maximum velocity.

---

# 11. Encoder Feedback

The new motor includes a quadrature encoder.

The encoder provides information about:

```text
shaft rotation
+
rotation direction
```

This makes it possible to perform motion requests based on measured drivetrain movement instead of relying entirely on timing.

---

## Time-Based Motion

```text
Drive for X seconds
```

can change with:

- battery voltage;
- motor loading;
- grip;
- drivetrain friction;
- starting velocity.

---

## Encoder-Assisted Motion

```text
Set movement target
        ↓
Read encoder
        ↓
Drive
        ↓
Compare current count with target
        ↓
Stop when target is reached
```

Encoder feedback improves repeatability, although wheel slip can still make actual vehicle travel differ from calculated shaft travel.

---

# 12. Updated Drivetrain Operating Point

The current drivetrain uses:

| Parameter | APOC Configuration |
| --- | --- |
| Motor | 12 V, 600 RPM geared DC encoder motor |
| External ratio | 1:1 |
| Drive architecture | 4WD |
| Steering | Front Ackermann |
| Differential | Mechanical |
| Motion feedback | Quadrature encoder |
| Wheel diameter | 46 mm |

This configuration is documented separately in:

```text
docs/hardware/drivetrain.md
```

---

# 13. Parking Hardware Architecture

Parking was one of the major reasons for expanding the sensing system.

The current parking hardware combines:

```text
Camera
+
MPU6050
+
3 × VL53L0X
+
Encoder
+
Ackermann steering
```

Each component supplies different information.

| Hardware | Parking Information |
| --- | --- |
| Camera | Course and parking geometry |
| MPU6050 | Relative orientation / heading |
| ToF sensors | Nearby physical distance |
| Encoder | Shaft-motion feedback |
| Steering servo | Vehicle curvature |
| Drive motor | Forward / reverse movement |

---

# 14. Why Parking Required Hardware Changes

The earlier approach relied more heavily on camera interpretation, heading and timed movement.

However:

```text
Correct heading
≠
Correct wall clearance
```

and:

```text
Correct distance
≠
Correct orientation
```

The APOC architecture therefore measures both.

```text
Visual geometry
      +
Heading
      +
Physical distance
      +
Movement
      ↓
Parking decision
```

---

# 15. Ackermann Parking Constraint

Starlight uses front Ackermann steering.

This means it cannot rotate in place like a differential-drive robot.

Parking must therefore use:

```text
Forward arc
     +
Reverse arc
     +
Alignment correction
```

The post-Nationals sensor additions were designed around this physical constraint rather than assuming that software alone could eliminate it.

---

# 16. Sensor Architecture After APOC Redesign

The current robot uses four different sensing principles.

| Sensor | What It Measures |
| --- | --- |
| **Camera Module 3 Wide ×2** | Appearance and image geometry |
| **MPU6050** | Angular-rate / relative heading information |
| **VL53L0X ×3** | Nearby physical distance |
| **Quadrature encoder** | Motor-shaft movement and direction |

The design deliberately avoids asking one sensor to solve every problem.

```text
Camera → What is visible?
IMU    → How much did we turn?
Encoder → How much did the shaft move?
ToF    → How large is the nearby gap?
```

---

# 17. Updated Hardware Inventory

The principal APOC hardware includes:

| Qty. | Component | Role |
| ---: | --- | --- |
| 1 | Raspberry Pi 5, 4 GB | Main computer |
| 2 | Raspberry Pi Camera Module 3 Wide | Vision |
| 3 | VL53L0X ToF sensors | Short-range distance |
| 1 | MPU6050-based module | Heading feedback |
| 1 | 12 V, 600 RPM geared encoder motor | Propulsion |
| 1 | Integrated quadrature encoder | Motion feedback |
| 1 | TB6612FNG | Motor drive |
| 1 | DS3225 servo | Ackermann steering |
| 1 | 3S battery system | Main vehicle power |
| Multiple | PLA printed structures | Rigid mounting and packaging |
| Multiple | LEGO Technic elements | Drivetrain and adjustable mechanisms |

---

# 18. Wiring Additions

The APOC changes introduced additional wiring requirements.

Important interfaces include:

| Function | Interface |
| --- | --- |
| Motor direction | GPIO5 / GPIO6 |
| Motor PWM | GPIO13 |
| Steering servo | GPIO22 |
| I2C SDA | GPIO2 |
| I2C SCL | GPIO3 |
| MPU6050 | I2C, address `0x68` |
| ToF XSHUT 1 | GPIO16 |
| ToF XSHUT 2 | GPIO20 |
| ToF XSHUT 3 | GPIO21 |
| Encoder | C1 / C2 from integrated motor encoder |

The complete wiring reference is maintained separately in:

```text
docs/hardware/wiring-guide.md
```

---

# 19. Mechanical Mount Changes

The post-Nationals redesign required new printed components for:

- camera mounting;
- rear sensor / camera structure;
- electronics support;
- ToF positioning;
- revised chassis packaging.

The purpose of these parts was not cosmetic.

They establish controlled geometry between:

```text
Robot
Sensor
Track
```

For perception hardware, mount design is therefore part of sensor calibration.

---

# 20. CAD and Printed Parts

Current and historical CAD evidence is maintained in:

```text
Models/
```

and vehicle photographs are maintained in:

```text
v-photos/
```

The repository should distinguish clearly between:

```text
Historical prototype
Earlier Nationals configuration
Current APOC configuration
```

so that an older CAD render is not accidentally interpreted as the final robot.

---

# 21. Hardware Change → Software Consequence

Although this document focuses on hardware, the APOC redesign directly changed the software requirements.

| Hardware Change | Software Consequence |
| --- | --- |
| Camera relocation | New image geometry |
| Fixed camera pose | Stable ROI positions |
| Rearward mounting | Body-exclusion requirement |
| Three ToF sensors | Multi-sensor initialization and parking states |
| Encoder motor | Encoder-assisted movement |
| 1:1 gearing | Movement values retuned |
| New chassis | Obstacle and parking paths retuned |
| Revised sensor placement | New stopping and confirmation conditions |

Hardware and software were therefore developed together.

---

# 22. Current Vision Relationship

The revised camera hardware enabled the final multi-ROI vision architecture.

The principal final vision file is:

```text
src/N_Vision_final.py
```

The frame is divided into regions with different jobs rather than treating every detected colour anywhere in the image as equivalent.

Typical information includes:

- inner wall;
- outer wall;
- centre reference;
- pillar region;
- course marker;
- parking cue.

This architecture depends on the camera mounts remaining in their calibrated physical position.

---

# 23. Current Parking Relationship

The post-Nationals hardware update also supports:

```text
src/parking_final.py
```

The parking architecture combines:

```text
Vision
      ↓
Heading
      ↓
ToF confirmation
      ↓
Forward / reverse Ackermann motion
      ↓
Final distance condition
```

The hardware redesign and parking software should therefore be treated as one engineering change rather than two unrelated upgrades.

---

# 24. Component-Level Testing

After the redesign, individual hardware functions are tested before a full challenge run.

| Subsystem | Test |
| --- | --- |
| Steering | `src/servo_test.py` |
| Encoder | `src/encoder_test.py` |
| Distance sensing | `src/TUF_test.py` |
| Heading | `src/heading.py` |
| Camera calibration | `src/Cal_APOC.py` |

The intended workflow is:

```text
Mechanical inspection
        ↓
Electrical inspection
        ↓
Individual sensor test
        ↓
Low-speed subsystem test
        ↓
Integrated challenge test
        ↓
Full-speed run
```

---

# 25. APOC Change Summary

The post-Nationals redesign can be summarized as:

```text
NATIONALS
│
├── Earlier chassis
├── Earlier camera geometry
├── Less direct parking-distance information
├── Earlier drivetrain operating point
└── Greater dependence on timing / visual interpretation

                    ↓ REDESIGN ↓

APOC
│
├── Revised chassis
├── Rearward rigid camera arrangement
├── Multi-ROI-compatible camera geometry
├── 3 × VL53L0X distance sensors
├── 600 RPM encoder motor
├── 1:1 external gearing
├── Encoder-assisted movement
├── Revised sensor mounts
└── Camera + IMU + encoder + ToF parking architecture
```

---

# Engineering Rationale

The APOC redesign follows one main principle:

> **A sensor, motor, camera or mount is useful only if its physical placement and behaviour provide information or motion that the controller can use reliably.**

The final robot therefore treats:

```text
Mechanics
+
Electronics
+
Sensing
+
Control
```

as one connected system.

---

# Evidence Status

The following distinctions are intentional:

| Statement | Evidence Type |
| --- | --- |
| Three VL53L0X units are installed | Hardware configuration |
| Motor nominal output is 600 RPM | Component specification |
| External gearing is 1:1 | Current mechanical configuration |
| Encoder reports shaft movement | Sensor function |
| Revised camera placement changes image geometry | Engineering relationship |
| ToF improves access to local gap information | Design rationale |
| Post-Nationals architecture was retained | Development record |

This document does not assign unsupported reliability percentages to the revised hardware.

---

# Related Documentation

| Document | Purpose |
| --- | --- |
| [`../engineering-decisions.md`](../engineering-decisions.md) | Why major design changes were selected |
| [`../failure-log.md`](../failure-log.md) | Failures that drove redesign |
| [`../testing.md`](../testing.md) | Physical verification and test records |
| [`../hardware/drivetrain.md`](../hardware/drivetrain.md) | Current drivetrain architecture |
| [`../hardware/wiring-guide.md`](../hardware/wiring-guide.md) | Electrical connections |
| [`../hardware/bom.md`](../hardware/bom.md) | Current hardware inventory |
| [`../../CHANGELOG.md`](../../CHANGELOG.md) | Chronological project changes |
| [`../../Models/`](../../Models/) | Mechanical design files |
| [`../../v-photos/`](../../v-photos/) | Vehicle and development photographs |
| [`../../src/`](../../src/) | Current robot software |

---

## Final Configuration Rule

Documentation, photographs, code and testing records must clearly distinguish the **current APOC configuration** from older prototypes.

In particular:

```text
Earlier speed-increasing gearing
Earlier motor specifications
Earlier camera locations
Earlier parking architecture
Earlier chassis photographs
```

must not be presented as current hardware.

The current Rev27 hardware configuration is the reference for APOC documentation.

---

**Team Sentio 6010**  
**Starlight**  
**WRO Future Engineers 2026**  
**Robofun Lab (RFL), India**
