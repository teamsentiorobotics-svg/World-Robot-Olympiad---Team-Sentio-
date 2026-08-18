# Team Sentio — World Robot Olympiad Future Engineers 2026

This repository documents **Team Sentio's autonomous vehicle for the World Robot Olympiad 2026 — Future Engineers category**.

**Team:** Deyaan Agrawal, Darsh Zaveri, Aarav Jalan  
**Institution:** Robofun Lab (RFL), India  
**Mechanical platform:** V3  
**Open Challenge software:** V5

Our engineering cycle is:

> **Build → Test → Observe → Find the failure → Modify → Retest**

The repository is intended to make the robot, software architecture, testing process and major engineering decisions traceable and reproducible.

---

## Repository Structure

| Path | Contents |
|---|---|
| [`src/`](src/) | Competition source code: Open Challenge, Obstacle Challenge and MPU6050 heading helper |
| [`docs/`](docs/) | Raspberry Pi setup and software-dependency documentation |
| [`models/`](models/) | CAD renders, printable STL files and final chassis model |
| [`schemes/`](schemes/) | Electrical schematic and wiring reference |
| [`v-photos/`](v-photos/) | Final vehicle views, circuit-board photographs and hardware evidence |
| [`t-photos/`](t-photos/) | Team photographs |
| [`video/`](video/) | Driving demonstration video evidence |
| [`other/`](other/) | Supporting design material, Gantt sheet, logic diagrams and supplementary documentation |
| [`requirements.md`](requirements.md) | Formal software dependency record |

### Competition source

```text
src/
├── Open_Challenge.py
├── Obstacle_Challenge.py
└── heading.py
```

`heading.py` provides the `MPU6050Heading` class used by the Obstacle Challenge software.

---

# 1. Mobility and Mechanical Design

The final V3 robot is approximately **865 g** and measures approximately **170 × 128 × 265 mm**.

| Parameter | Final V3 value |
|---|---:|
| Mass | ~865 g |
| Length | 170 mm |
| Width | 128 mm |
| Height | 265 mm |
| Wheelbase | 107.5 mm |
| Track width | 110 mm |
| Wheel diameter | 46 mm |
| Ground clearance | 14 mm |

The chassis is primarily 3D-printed PLA with selected LEGO Technic elements. The front wheels use **Ackermann steering geometry**, while the rear drivetrain uses a differential arrangement.

### Steering

The Open Challenge software uses:

```text
LEFT   = 70
CENTER = 95
RIGHT  = 125
```

Larger steering commands were rejected because they placed excessive mechanical stress on the LEGO steering supports and could disconnect the linkage. The final range therefore prioritises repeatability and mechanical reliability rather than maximum steering travel.

### Drivetrain

Final motor:

```text
JGB37-520
12 V
600 RPM nominal
```

Gear pair:

```text
36T driving → 20T driven
```

The ideal speed ratio is:

```text
36 / 20 = 1.8
600 × 1.8 = 1080 RPM ideal wheel-side speed
```

With 46 mm wheels, the ideal wheel-surface speed is approximately **2.60 m/s**. Practical/test-derived output was closer to approximately **800 RPM**, corresponding to about **1.93 m/s**. This is an engineering estimate rather than a laboratory measurement.

The earlier 1000 RPM Johnson motor stalled after crashes/high mechanical load and the motor driver failed. The team replaced both the motor and driver and prioritised drivetrain reliability over maximum RPM.

Mechanical reconstruction resources are available in [`models/`](models/) and [`v-photos/`](v-photos/).

---

# 2. Power and Sensor Architecture

The main controller is a **Raspberry Pi 5, 4 GB**.

Primary hardware includes:

- 2 × Raspberry Pi Camera Module 3
- JGB37-520 drivetrain motor
- TB6612FNG motor driver
- DS3225 steering servo
- MPU6050 IMU
- SSD1306 OLED
- 3S 11.1 V 2200 mAh LiPo battery

Battery energy:

```text
11.1 V × 2.2 Ah = 24.42 Wh
```

A fully charged pack was observed at approximately **12.2 V**. Practical endurance was around **1.5 hours / 50–60 laps**, but this was not a controlled battery-discharge experiment.

An earlier **5 V / 3 A** Raspberry Pi supply produced repeated undervoltage warnings. The robot was therefore moved to a higher-current regulated 5 V supply.

### Main GPIO map

| Function | BCM GPIO |
|---|---:|
| Motor IN1 | GPIO5 |
| Motor IN2 | GPIO6 |
| Motor PWM | GPIO13 |
| Steering servo | GPIO22 |
| I2C SDA | GPIO2 |
| I2C SCL | GPIO3 |

The detailed electrical schematic is available in [`schemes/`](schemes/).

Development failures also changed the team's safety process. A LiPo charging incident and a reverse-polarity incident led to stricter polarity checks, supervised charging and improved connector discipline.

---

# 3. Sensor Placement and Calibration

### Front camera

- Approximately **5 mm right of vehicle centre**
- Approximately **50° downward pitch**
- Used for wall, marker and obstacle perception

### Rear camera

- Approximately **45° downward pitch**
- Approximately **0° yaw**
- Primarily intended for parking and rear-wall geometry

Earlier camera placements caused late line detection and unstable corner-wall perception. Changing the physical camera geometry significantly improved software behaviour, reinforcing an important engineering lesson:

> A software-looking problem can have a mechanical solution.

At program startup, automatic exposure and white balance are allowed to settle for approximately two seconds. Exposure and analogue gain are then locked so that the fixed colour thresholds operate under more repeatable image conditions.

A front LED was also found to improve low-light detection without noticeable saturation in the tested setup.

---

# 4. Open Challenge Software

[`src/Open_Challenge.py`](src/Open_Challenge.py) uses:

- Python 3
- OpenCV
- NumPy
- Picamera2
- RPi.GPIO-compatible GPIO control

Final image configuration:

```text
1280 × 680
RGB888 camera stream
```

### Vision pipeline

```text
Frame
  ↓
Gaussian blur
  ↓
LAB conversion
  ↓
CLAHE
  ↓
Colour masks
  ↓
Morphology
  ↓
Contours
  ↓
Geometry
  ↓
Proportional steering
```

Black-wall contours guide the robot. When both walls are visible, the controller uses their relative geometry to calculate steering error. When only one wall is visible, direction-aware references are used. If no wall is visible, a small directional fallback is applied.

This replaced an earlier symmetric centring method that caused more corner meandering.

### Final Open tuning

```text
KP = 0.012
LINE_COOLDOWN = 1.3 s
```

Values from approximately `0.010` to `0.050` were tested. `0.010` was too weak, `0.015–0.020` produced more aggressive steering, and `0.050` could overstress the steering mechanism. `0.012` gave the best observed balance between responsiveness and mechanical stability.

### Direction and lap counting

The first valid direction marker determines the travel direction:

```text
Blue first   → Anticlockwise
Orange first → Clockwise
```

The marker-counting logic uses a rising-edge approach so that a marker remaining visible across multiple frames is not counted repeatedly.

The competition configuration uses:

```text
3 laps × 4 gate events = 12 counts
```

After the required count is reached, the steering is centred and the drivetrain is stopped.

### Performance evidence

The engineering record contains **12 successful timed Open Challenge runs** with a **best recorded time of 22 s**.

A five-run video-backed cohort recorded:

```text
23 s
29 s
28 s
22 s
23 s
```

The team does not claim that motor-speed command alone caused the timing difference because all environmental variables were not controlled.

The repository currently includes an Open Challenge driving video in [`video/`](video/).

---

# 5. Obstacle Challenge

[`src/Obstacle_Challenge.py`](src/Obstacle_Challenge.py) contains the team's computer-vision development for:

- Black-wall detection
- Red pillar detection
- Green pillar detection
- Direction-marker detection
- Magenta/purple parking-cue detection
- Obstacle steering target generation
- MPU6050-assisted parking logic

The obstacle strategy evolved from fixed timed steering toward **continuous image-target geometry**. This change followed failures in which a corner pillar caused the robot to commit to a turn too early.

The intended control sequence is:

```text
Perceive environment
        ↓
Detect pillar / wall state
        ↓
Generate steering target
        ↓
Continuously update target while passing obstacle
        ↓
Return to wall-following state
        ↓
Complete course
        ↓
Enter parking stage
```

The team has reported **10+ successful full Obstacle Challenge runs** during development. Because the total number of failed attempts was not retained, no obstacle success percentage is claimed.

### Public-code release status

The exact physically validated Obstacle/Parking executable must be the file published as `src/Obstacle_Challenge.py` for the final competition release.

A development or calibration snapshot should not be treated as a validated release merely because it is present in the repository.

---

# 6. Parking

The parking strategy uses the rear-camera geometry together with the MPU6050 heading helper in [`src/heading.py`](src/heading.py).

Intended sequence:

```text
Course complete
      ↓
Parking stage
      ↓
Detect magenta/purple cue
      ↓
Use rear geometry
      ↓
Use MPU6050 heading
      ↓
Short forward/reverse corrections
      ↓
Reobserve position
      ↓
Stop inside parking area
```

Ackermann steering cannot rotate the robot in place. Parking therefore requires a sequence of small forward/reverse corrections rather than a single point turn.

The most important parking failure mode observed during development was contact with the rear wall. This led to the use of shorter correction movements and repeated re-observation rather than one long open-loop reverse command.

---

# 7. Engineering Decisions and Trade-offs

| Engineering decision | Reason |
|---|---|
| 1000 RPM motor → JGB37-520 600 RPM | Previous motor stalled and damaged the driver |
| Maximum servo travel → safe steering limits | Protected steering supports and linkage |
| Symmetric wall centring → direction-aware wall logic | Reduced corner meandering |
| Fixed obstacle turn → continuous pillar target | Improved response to corner obstacles |
| Earlier camera pose → revised front/rear geometry | Improved perception stability |
| Ambient light only → front LED support | Improved low-light detection |
| Earlier connector practice → safer polarity process | Reduced power-connection risk |
| Rear wing → removed | Testing did not justify retaining it |

These decisions show that mechanics, electronics and software were treated as one interacting system rather than isolated subsystems.

---

# 8. Testing Method

The normal Team Sentio testing sequence is:

```text
Component test
      ↓
Subsystem test
      ↓
Low-speed integrated test
      ↓
Full challenge run
      ↓
Classify failure
      ↓
Modify
      ↓
Retest
```

Before a full run, the team checks:

- Power and polarity
- Common ground
- Drivetrain freedom
- Motor direction
- Servo centre and mechanical steering limits
- Camera detection
- Colour detection
- MPU6050 / I2C operation
- Correct competition program

Measurements are kept separate from estimates. Values that were not retained or measured under controlled conditions are not invented retrospectively.

---

# 9. Reproducing the Robot

A new Raspberry Pi setup should begin with the detailed guide:

**[`docs/pi_setup_instruction.md`](docs/pi_setup_instruction.md)**

Software dependencies are documented in:

**[`requirements.md`](requirements.md)** and **[`docs/Software_Dependencies.md`](docs/Software_Dependencies.md)**

Recommended reproduction order:

1. Use [`models/`](models/) and [`v-photos/`](v-photos/) to reproduce the mechanical platform.
2. Assemble the drivetrain and verify the differential and steering move freely.
3. Wire the robot using [`schemes/`](schemes/).
4. Confirm polarity and common ground before power-up.
5. Configure the Raspberry Pi using [`docs/pi_setup_instruction.md`](docs/pi_setup_instruction.md).
6. Install and verify the required software dependencies.
7. Set the documented camera geometry.
8. Verify steering centre and safe travel limits.
9. Test motor, servo, cameras and MPU6050 independently.
10. Test at reduced speed before a full autonomous run.
11. Record the exact Git commit used for physical validation.
12. Treat any code modification after validation as a new revision requiring retesting.

### Exact-source reproducibility

For the final competition release, the repository should identify the exact commit containing the physically validated competition executables.

Useful command:

```bash
git rev-parse HEAD
```

The source that physically completes the challenge should be the same source published in the final release.

---

# 10. Development History

| Version | Development stage |
|---|---|
| **V0** | LEGO mobility prototype |
| **V0.5** | Rear-wing experiment |
| **V1** | Working circuit and camera control |
| **V2** | 3D-printed electronics mounting architecture |
| **V3** | Purpose-built chassis, revised drivetrain and dual-camera platform |
| **Open V5** | Direction-aware wall control, `KP=0.012`, rising-edge marker counting |

The repository commit history records ongoing mechanical, electrical, software and documentation development.

For the final competition release, descriptive commit messages and an identifiable validated source revision are preferred over generic upload-only messages.

---

# 11. Reproduction Resources

| Resource | Location |
|---|---|
| Main project overview | [`README.md`](README.md) |
| Software requirements | [`requirements.md`](requirements.md) |
| Raspberry Pi setup | [`docs/pi_setup_instruction.md`](docs/pi_setup_instruction.md) |
| Software dependency guide | [`docs/Software_Dependencies.md`](docs/Software_Dependencies.md) |
| Open Challenge code | [`src/Open_Challenge.py`](src/Open_Challenge.py) |
| Obstacle Challenge code | [`src/Obstacle_Challenge.py`](src/Obstacle_Challenge.py) |
| MPU6050 heading helper | [`src/heading.py`](src/heading.py) |
| Electrical schematic | [`schemes/`](schemes/) |
| CAD and printable models | [`models/`](models/) |
| Vehicle photographs | [`v-photos/`](v-photos/) |
| Team photographs | [`t-photos/`](t-photos/) |
| Driving video | [`video/`](video/) |
| Supporting engineering material | [`other/`](other/) |

---

# Team Contributions

**Deyaan Agrawal** — software, algorithms, debugging, tuning and track testing.  
**Darsh Zaveri** — hardware integration, LEGO mechanisms, circuits, wiring and testing.  
**Aarav Jalan** — CAD, algorithm contributions, debugging, documentation and circuit construction.

Robofun Lab provided access to testing facilities, mock runs and guidance at development roadblocks. The submitted vehicle, source code, testing process and engineering decisions remain Team Sentio's work.

---

**Team Sentio**  
**WRO Future Engineers 2026**  
**Robofun Lab (RFL), India**
