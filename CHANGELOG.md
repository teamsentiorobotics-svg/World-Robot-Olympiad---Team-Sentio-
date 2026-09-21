# Team Sentio — WRO Future Engineers 2026

## Engineering, Software & Validation Changelog

This changelog documents the major engineering milestones, software revisions, calibration work, hardware changes, validation results, and repository updates for **Team Sentio's WRO Future Engineers 2026 vehicle, Starlight**.

The document provides a chronological record of how the robot evolved from early mobility and perception prototypes into the competition-validated Nationals configuration and, subsequently, the redesigned **WRO Asia Pacific Open Championship (APOC)** configuration.

Detailed calculations, failure analysis, testing evidence, design decisions, and supporting engineering rationale remain documented in the engineering journal and associated repository files.

---

# 19 September 2026 — Post-Nationals APOC Redesign & Vision Calibration System

Following the India Nationals build, Starlight entered a new engineering and development cycle focused on preparation for the **WRO Asia Pacific Open Championship (APOC)**.

This revision introduced changes across the mechanical structure, camera architecture, computer vision pipeline, parking system, and calibration workflow. The Nationals configuration remains preserved as the validated competition baseline; the changes below represent the subsequent APOC development branch.

## Development-Version Photographic Record

- Photographs of the major physical development stages are retained in the repository under **`v-photos`**.
- These records document the mechanical evolution of the robot, including:
  - the **fully LEGO prototype**, used during the earliest mobility and mechanism-development stages;
  - the **hybrid LEGO + 3D-printed configuration**, where custom printed components were progressively introduced while retaining LEGO Technic drivetrain and steering elements;
  - the later purpose-built competition chassis.
- The photographs provide visual evidence of the mechanical development lineage documented throughout the project.

## Chassis & Camera-Layout Redesign

After Nationals, the chassis was substantially redesigned for the APOC configuration.

- The previous chassis, camera mounts, and selected printed support structures were replaced.
- The new architecture was designed around a revised sensing arrangement.
- **Both cameras are now positioned toward the rear of the robot.**
- The revised camera geometry provides a wider and more useful view of the competition environment.
- New camera placement required corresponding changes to:
  - printed camera mounts;
  - chassis packaging;
  - camera geometry;
  - custom PLA structures;
  - vision-processing assumptions.
- Camera placement is therefore treated as an integral component of the perception system rather than solely as a mechanical mounting decision.

## Vision-System Redesign

`vision.py` was substantially rewritten for the APOC configuration.

The new architecture moves away from a single broad detection region and instead uses a structured **multi-ROI perception system**.

### Major changes

- Multiple dedicated **Regions of Interest (ROIs)** were introduced.
- Different ROIs are assigned to different portions of the competition environment and different detection tasks.
- Explicit exclusion regions were added to prevent visible robot components, wiring, and other non-field objects from contaminating detections.
- Black-wall processing is performed independently within separate ROIs so detections from different regions are not incorrectly merged.
- Colour detection, black-wall detection, and pillar detection were recalibrated for the new rear-mounted camera geometry.
- Exposure and white-balance stabilization were retained to improve threshold consistency between runs.
- Camera-dependent geometric assumptions were recalculated following the physical camera relocation.

These changes were designed to improve the reliability and repeatability of wall, marker, pillar, and obstacle detection under the revised mechanical configuration.

---

# 19 September 2026 — HSV Calibration & Interactive Vision-Tuning System

A new **interactive colour-calibration system** was added on **19 September 2026** to improve the repeatability and efficiency of computer-vision development.

Previously, colour thresholds were adjusted primarily through repeated manual code edits and robot testing. The new calibration workflow provides a dedicated environment for tuning the vision system before committing threshold values to the main navigation code.

## HSV Slider Calibration

The calibration program introduces interactive **HSV sliders / trackbars** that allow the operator to adjust colour thresholds in real time.

The calibration workflow allows the following parameters to be tuned while viewing the camera feed:

- Hue lower bound;
- Hue upper bound;
- Saturation lower bound;
- Saturation upper bound;
- Value lower bound;
- Value upper bound.

The resulting mask is displayed simultaneously with the camera image, allowing the effect of each threshold adjustment to be evaluated immediately.

### Calibration workflow

```text
Camera Frame
      ↓
Colour-space conversion
      ↓
HSV threshold sliders
      ↓
Live colour mask
      ↓
Visual inspection
      ↓
Threshold refinement
      ↓
Contour / detection verification
      ↓
Final threshold values
      ↓
Integration into vision system
```

This significantly reduces the need to repeatedly modify source code simply to test a new threshold.

## Purpose of the HSV Calibration Tool

The new calibration system was introduced to make the vision-development process more systematic.

It allows the team to:

- identify suitable HSV ranges for competition colours;
- observe how lighting changes affect colour masks;
- remove unwanted background regions;
- distinguish genuine coloured objects from small noise regions;
- tune thresholds for different camera positions;
- rapidly test alternative threshold combinations;
- verify colour separation before integrating values into navigation code.

The calibration tool therefore functions as a **development and validation instrument**, rather than being treated as a separate competition-control algorithm.

## HSV + LAB Vision Development

The calibration workflow complements the existing LAB-based vision pipeline rather than replacing it.

The project continues to use colour-space processing appropriate to the detection task, with HSV providing an intuitive and highly tunable calibration interface and LAB remaining part of the established competition vision architecture.

The development workflow can therefore be represented as:

```text
Camera Image
      ↓
Initial HSV Calibration
      ↓
Threshold Investigation
      ↓
Mask Validation
      ↓
LAB / HSV Vision Pipeline
      ↓
Morphological Filtering
      ↓
Contour Detection
      ↓
Geometric Validation
      ↓
Robot Decision
```

This separation allows calibration to be performed independently from the final navigation logic.

## Calibration as an Engineering Process

The introduction of the HSV slider system also improves reproducibility.

Instead of treating threshold values as arbitrary constants, the team can now:

1. capture the camera view under the intended lighting conditions;
2. adjust HSV ranges interactively;
3. inspect the resulting mask;
4. verify that the desired object is isolated;
5. check that surrounding field elements are rejected;
6. record the resulting threshold values;
7. transfer validated values into the competition vision code;
8. physically test the resulting detection on the robot.

This creates a clearer link between **visual calibration, software implementation, and physical validation**.

---

# 19 September 2026 — APOC Open Challenge Software Revision

The **Open Challenge software** was updated to match the redesigned APOC vision architecture.

- Steering and navigation logic were modified to consume the revised multi-ROI wall and marker detections.
- Camera-dependent thresholds were recalibrated.
- Target positions were updated for the new camera geometry.
- Wall-following assumptions were adjusted to reflect the rear-mounted camera arrangement.
- Vision-processing parameters were reviewed using the new calibration workflow.
- The Open Challenge implementation is therefore a later software revision rather than a direct copy of the Nationals Open V5 implementation.

The APOC Open code should consequently be treated as a dedicated branch of development built around the redesigned perception system.

# 19 September 2026 — APOC Obstacle Challenge Revision

The **Obstacle Challenge software** was also updated for the new vision architecture.

- Obstacle detection was adapted to the revised camera geometry.
- Wall-following behaviour was updated to consume the new multi-ROI detections.
- Detection zones were recalibrated.
- Target geometry was recalculated for the new camera positions.
- Control behaviour was retuned following the chassis redesign.
- Colour and pillar detection were verified against the revised camera feed.

The underlying navigation objective remains continuous visual navigation around red / green pillars, while the perception and control layers have been revised for the APOC configuration.

# Dual ToF Sensing Added for Parking

Two **VL53L0X time-of-flight (ToF) distance sensors** were added to the APOC configuration.

The sensors supplement the existing camera and MPU6050 feedback during parking.

### Primary purpose

The ToF sensors provide direct short-range distance measurements to improve the repeatability of parking stops.

Parking logic therefore no longer depends exclusively on camera geometry, heading feedback, and fixed timing.

The APOC parking implementation includes:

- a startup delay before ToF detection becomes active;
- repeated distance measurements;
- a two-detection confirmation system;
- an inter-detection cooldown;
- ToF-confirmed stopping;
- additional ToF-controlled forward / reverse stopping phases.

The resulting architecture separates the responsibilities of the sensing systems:

```text
CAMERAS
→ Field geometry / visual positioning

VL53L0X ToF
→ Short-range distance / stopping confirmation

MPU6050
→ Heading / orientation

RASPBERRY PI 5
→ Sensor fusion / state logic / control

MOTOR + ACKERMANN STEERING
→ Physical execution
```

# APOC Sensing Architecture

```text
        2 × REAR-MOUNTED CAMERAS
                   ↓
        MULTI-ROI COMPUTER VISION
                   ↓
        WALL / MARKER / PILLAR DATA
                   ↓
           OPEN + OBSTACLE
             NAVIGATION


          2 × VL53L0X ToF
                   ↓
       SHORT-RANGE DISTANCE DATA
                   ↓
          PARKING STOP LOGIC


              MPU6050
                 ↓
        HEADING / ORIENTATION
                 ↓
          STATE ESTIMATION


           RASPBERRY PI 5
                 ↓
      SENSOR FUSION + CONTROL
                 ↓
       MOTOR + ACKERMANN STEERING
```

# APOC Revision Status

The APOC configuration should be treated as a **post-Nationals engineering revision** and not as a retroactive description of the Nationals robot.

The Nationals V3 / Open V5 configuration remains the documented and physically validated competition baseline.

The September APOC revision represents a new development stage involving:

- redesigned chassis;
- revised rear-mounted camera architecture;
- multi-ROI vision;
- new HSV calibration tooling;
- recalibrated colour detection;
- revised Open Challenge software;
- revised Obstacle Challenge software;
- dual ToF parking sensors;
- updated parking-distance logic.

---

# 24 August 2026 — Final Competition Validation

## Obstacle Challenge & Parking

- Final Obstacle Challenge software completed physical robot testing successfully.
- Final parking behaviour was also physically tested and was working.
- The working challenge code and required helper modules were pushed to GitHub.
- The final project package included:
  - `drive.py`
  - `vision.py`
  - `openVision.py`
  - `heading.py`
  - `parking.py`
- The final repository represented the working robot software rather than a development-only snapshot.
- Later field-calibration changes were intended to be committed and pushed so the Raspberry Pi and repository remained synchronized.

# 18 August 2026 — Repository Documentation & Reproducibility Update

## Added

- Added `src/heading.py` for MPU6050 heading integration.
- Added `requirements.md` as the formal software dependency record.
- Added `docs/Software_Dependencies.md`.
- Added `docs/pi_setup_instruction.md` containing Raspberry Pi setup, GPIO, I2C, camera, package-installation, safety, and run instructions.

## Updated

- Expanded `README.md` into the primary repository-level engineering and reproduction guide.
- Synchronized the README with the Rev6 Open Challenge evidence.
- Documented:
  - **12 successful timed runs**;
  - **22 s best observed time**;
  - five video-backed tests from 15 August 2026.
- Added clearer links between source code, CAD, wiring, photographs, videos, dependencies, and setup documentation.
- Added exact-source reproducibility guidance linking the physically validated executable to a Git commit.

## Repository Status

- Open Challenge documentation and dependency packaging were completed.
- Obstacle Challenge and Parking completed physical validation.
- The complete working project package and helper modules were pushed to GitHub.
- The repository could therefore be treated as the final competition project package, subject to later field-calibration revisions.

# Rev6 Submission / Release Candidate — Evidence Freeze: 16 August 2026

## Mechanical V3

The final competition-focused mechanical platform was recorded as **V3**.

### Final recorded dimensions

| Parameter | Value |
|---|---:|
| Mass | 865 g |
| Length | 210 mm |
| Width | 128 mm |
| Height | 265 mm |
| Wheelbase | 107.5 mm |
| Track width | 110 mm |
| Wheel diameter | 46 mm |
| Ground clearance | 14 mm |

- Purpose-built PLA structures were retained where repeatable geometry was required.
- Selected LEGO Technic elements were retained where serviceability, steering adjustment, and rapid replacement were beneficial.
- The final steering architecture used **Ackermann steering**.

### Final Open steering limits

```text
LEFT   = 70
CENTER = 95
RIGHT  = 125
```

Wider servo travel was rejected after testing indicated increased linkage stress and a greater possibility of mechanical disconnection.

## Drivetrain Redesign

- The earlier **1000 RPM Johnson geared motor** was replaced after heavy loading and stall behaviour.
- The damaged TB6612FNG motor driver was replaced.
- The final configuration adopted a **JGB37-520, 12 V, 600 RPM motor**.
- The **36T driving → 24T driven** external gear stage was retained.
- The design prioritised repeatability and drivetrain reliability over maximum rated motor speed.
- No recurrence of the earlier motor-stall / driver-failure pattern was reported in the retained final testing.

## CAD & Mechanical Reproducibility

The final custom PLA structures were documented as Onshape-designed components.

The repository mechanical evidence included:

- six CAD render images;
- two printable STL files;
- one compressed GLB assembly/model.

Printed parts were used to preserve repeatable geometry for the camera, electronics, drivetrain, and other integrated components.

## Power Architecture

The final Nationals configuration retained a **3S 11.1 V 2200 mAh LiPo**.

Recorded charged-pack voltage: **approximately 12.2 V**.

The earlier **5 V / 3 A Raspberry Pi supply arrangement** was replaced after repeated undervoltage warnings.

A higher-current regulated 5 V Raspberry Pi supply architecture was introduced.

The common-ground architecture between the control electronics, sensors, and motor-driver references was retained.

## Electrical & Safety Engineering Changes

The project incorporated several safety-driven engineering changes following observed failures.

- Stricter charging supervision and correct 3S / cell-count checks were introduced following an earlier LiPo charging incident.
- Explicit polarity checks were introduced.
- A safer keyed / polarised connector strategy was adopted following reverse-polarity incidents.
- Faster power cut-off procedures were introduced.
- Staged drivetrain checks were added following the motor-stall / driver-failure event.
- These changes were documented as engineering responses to observed failure modes rather than undocumented assumptions.

# Nationals Camera & Sensing Architecture

The final V3 Nationals sensing stack consisted of:

- 2 × Raspberry Pi Camera Module 3;
- MPU6050 IMU;
- SSD1306 OLED;
- front illumination LED.

### Recorded camera geometry

**Front camera**

- approximately 5 mm right of centre;
- approximately 50° downward pitch.

**Rear camera**

- approximately 45° downward pitch;
- approximately 0° yaw.

Camera geometry was revised after earlier positions produced unstable corner-wall detection and late line detection.

### Startup image calibration

The final V3 startup procedure retained:

1. AE/AWB enabled for approximately 2 seconds;
2. exposure and analogue gain captured;
3. AE/AWB disabled;
4. fixed LAB thresholds used during the run.

This was intended to reduce colour-threshold instability caused by changing exposure and white balance.

The Nationals V3 configuration did **not** claim LiDAR, ultrasonic sensing, or wheel encoders.

The later APOC configuration subsequently added **2 × VL53L0X ToF sensors** for parking-distance feedback and changed the camera/chassis architecture as documented in the September revision.

# Open V5 — Final Nationals Open Challenge Control

## Control Architecture

The final Nationals Open Challenge software was retained as **Open V5**.

### Camera stream

```text
1280 × 680
RGB888
```

### Image-processing pipeline

```text
Frame
  ↓
Gaussian Blur
  ↓
LAB Conversion
  ↓
CLAHE
  ↓
Colour Masks
  ↓
Morphological Filtering
  ↓
Contours
  ↓
Geometry
  ↓
Proportional Steering
```

# Direction Logic

The first valid marker established the driving direction:

```text
Blue first   → Anticlockwise
Orange first → Clockwise
```

The first valid marker established direction but did not increment the lap count.

# Wall-Following Redesign

The earlier symmetric two-wall centring strategy was rejected after testing revealed corner meandering and asymmetric-wall visibility problems.

The final Open V5 architecture retained direction-aware wall following:

- **Both walls visible** → proportional geometric error;
- **One wall visible** → direction-aware single-wall target;
- **No wall visible** → small directional fallback.

# Final Open Tuning

```text
KP = 0.012
LINE_COOLDOWN = 1.3 s
```

Testing documented the following observations:

- `KP = 0.010` was too weak.
- `KP = 0.015–0.020` produced more aggressive steering and increased linkage stress.
- `KP = 0.050` was excessively aggressive.
- `LINE_COOLDOWN = 0.8 s` was too short and could allow duplicate counting.
- Values approaching `1.8 s` were more likely to miss genuine crossings.
- `1.3 s` was retained as the observed compromise.

# Lap Counting & Stop Logic

The final Open V5 implementation retained:

**3 laps × 4 counted events = 12 events**

A rising-edge marker detection system was used so that a single physical marker remaining visible across multiple frames was counted only once.

After 12 counted events:

```text
Steering → Centre
Motor    → Stop
Control Loop → Terminate
```

# Open Challenge Performance Evidence

Rev6 records:

- **12 successful timed Open Challenge runs**
- **22 s best observed time**

Five additional video-backed tests from 15 August 2026 were recorded as:

| ID | Speed Command | Time |
|---|---:|---:|
| V-01 | 100 | 23 s |
| V-02 | 90 | 29 s |
| V-03 | 90 | 28 s |
| V-04 | 100 | 22 s |
| V-05 | 100 | 23 s |

No causal claim is made that speed command alone produced the observed timing differences because direction, battery state, lighting, and track state were not fully controlled for every run.

No Open Challenge success probability is claimed because a complete failed-attempt denominator was not retained.

# Obstacle Challenge Strategy Development

## Navigation Redesign

The earlier fixed / early obstacle-turn strategy was rejected following repeated corner-pillar collision and run-over failures.

The system was redesigned around a **continuous visual target** strategy.

- Pillar target position changes continuously according to image geometry.
- Vertical position / proximity modifies the target as the pillar approaches.
- Steering continuously tracks the selected passing target.
- Once the obstacle is no longer relevant, the controller rejoins direction-aware wall-following.
- Lower obstacle speed was retained to provide additional time for perception and steering corrections.

### Obstacle State Architecture

```text
Perceive
   ↓
Identify Relevant Pillar
   ↓
Choose Passing Target
   ↓
Continuously Steer
   ↓
Rejoin Wall Following
   ↓
Complete Course
   ↓
Parking Stage
```

# Obstacle Challenge Validation

- More than **10 successful full Obstacle Challenge runs** were reported during development.
- The final Obstacle Challenge framework completed physical robot testing successfully.
- The exact submitted software package, including required helper modules, was retained in the final GitHub project.
- The complete failed-attempt denominator was not retained; therefore, no obstacle success percentage is claimed.

# Parking Architecture Development

The parking architecture evolved from a single opaque manoeuvre into a sequence of controlled Ackermann-compatible corrections.

The rear camera remained the primary collision-critical parking view, while the MPU6050 provided relative orientation feedback.

### Intended parking sequence

```text
Course Complete
      ↓
Locate Parking Geometry
      ↓
Reverse Entry
      ↓
IMU-Assisted Counter-Steer
      ↓
Re-Observe Rear Geometry
      ↓
Short Forward / Reverse Correction
      ↓
Confirm Position & Heading
      ↓
Stop
```

Because the robot uses Ackermann steering, non-zero forward / reverse movement is required; the chassis cannot rotate in place.

The parking architecture is intended to use repeated observations rather than relying on one long open-loop reverse movement.

The final Nationals Obstacle / Parking behaviour completed physical robot validation successfully.

# Development Lineage

The Rev6 engineering record preserves the following development sequence. Photographs of the **fully LEGO** and later **hybrid LEGO + 3D-printed** versions are retained in `v-photos` as visual evidence of this progression.

## V0 — LEGO Mobility

- Initial LEGO-dominant mobility architecture.
- Established basic vehicle movement before the final purpose-built chassis.

## V1 — Circuit + Camera

- Added working electronics.
- Introduced camera-based control development.

## V2 — Printed Electronics Mount

- Introduced a 3D-printed electronics mounting architecture.
- Improved packaging repeatability and integration.

## V3 — Purpose-Built Competition Chassis

- Introduced the competition-focused chassis architecture.
- Added purpose-built PLA packaging.
- Retained serviceable LEGO Technic steering / drivetrain components where useful.
- Integrated dual-camera geometry and the documented IMU / display sensor stack.

## Open V5 — Final Nationals Open Control

- Finalised direction-aware Open Challenge control.
- Retained `KP = 0.012`.
- Retained `LINE_COOLDOWN = 1.3 s`.
- Retained rising-edge marker counting.
- Retained 12-event completion logic.
- Documented 12 successful timed runs with a 22 s best.

## APOC Revision — September 2026

- Redesigned chassis and camera layout.
- Moved both cameras toward the rear.
- Introduced multi-ROI vision.
- Added explicit exclusion regions.
- Recalibrated wall, marker, pillar, and colour detection.
- Added interactive **HSV slider calibration** on 19 September.
- Retuned the vision system using the new calibration workflow.
- Revised Open Challenge and Obstacle Challenge software.
- Added **2 × VL53L0X ToF sensors** for parking-distance feedback.
- Revised parking logic around direct distance confirmation.
- Continued integration of camera, ToF, IMU, and Raspberry Pi control into a unified sensing architecture.

# Engineering Revision Summary

| Date | Major Revision | Primary Outcome |
|---|---|---|
| Early development | LEGO mobility and initial electronics | Basic robot movement established |
| V1 | Camera-based development | Visual control introduced |
| V2 | 3D-printed electronics integration | Improved packaging and repeatability |
| V3 | Competition chassis | Final Nationals mechanical architecture |
| Open V5 | Open Challenge control | Direction-aware wall following and 12-event completion |
| 16 Aug | Rev6 evidence freeze | Competition release candidate documented |
| 18 Aug | Repository / reproducibility update | Software package and documentation consolidated |
| 24 Aug | Final competition validation | Obstacle Challenge and Parking physically validated |
| **19 Sep** | **APOC redesign + HSV calibration** | **New chassis, rear-camera architecture, multi-ROI vision, interactive HSV calibration and revised parking sensing** |

# Current Engineering Status

The project has progressed from a competition-validated Nationals platform into a dedicated APOC development configuration.

The September 2026 revision represents a broader engineering cycle in which the team is redesigning the relationship between:

**mechanical geometry → camera placement → calibration → perception → navigation → parking → validation.**

The addition of the interactive HSV calibration system on **19 September 2026** formalises the vision-development process by allowing colour thresholds to be experimentally calibrated and validated before being integrated into the robot's navigation software.

This provides a clearer and more reproducible workflow for continued development toward APOC.

---

**Team Sentio**  
**WRO Future Engineers 2026**  
**Robofun Lab (RFL), India**
