# Changelog

## Team Sentio — WRO Future Engineers 2026

This changelog records major engineering, software, validation, and repository changes for Team Sentio's WRO Future Engineers 2026 vehicle.

It is intentionally concise. Detailed calculations, failure analysis, testing evidence, and design reasoning remain in the engineering journal and supporting repository files.

---

## Unreleased

### Obstacle Challenge / Parking

- Final Obstacle Challenge and parking software remains under active development.
- The public `src/Obstacle_Challenge.py` should be treated as a development snapshot until the exact submitted executable completes physical robot validation.
- The final Obstacle/Parking release will only be identified after:
  - the exact executable completes a full physical robot run,
  - parking is validated using that same source,
  - all required dependencies are present,
  - the validated Git commit SHA is recorded,
  - the same validated file is retained in the public repository.
- No final competition tag or release should be created before this validation step is complete.

---

## 18 August 2026 — Repository Documentation and Reproducibility Update

### Added

- Added `src/heading.py` for MPU6050 heading integration.
- Added root-level `requirements.md` as the formal software dependency record.
- Added `docs/Software_Dependencies.md`.
- Added `docs/pi_setup_instruction.md` with Raspberry Pi setup, GPIO, I2C, camera, package-installation, safety, and run instructions.

### Updated

- Expanded `README.md` into the main repository-level engineering and reproduction guide.
- Synchronized the README with the Rev6 Open Challenge evidence:
  - **12 documented successful timed runs**
  - **22 s best observed time**
  - five video-backed tests from 15 August 2026
- Added clearer links between source code, CAD, wiring, photographs, video, dependencies, and setup documentation.
- Added explicit exact-source reproducibility guidance so the physically validated executable can be tied to a Git commit.

### Repository status

- Open Challenge documentation and dependency packaging are substantially complete.
- Obstacle/Parking remains the final software-validation blocker before a competition release can be frozen.

---

## Rev6 Submission / Release Candidate — Evidence Freeze: 16 August 2026

### Mechanical V3

- Final competition-focused mechanical platform recorded as **V3**.
- Final recorded envelope:
  - mass: **865 g**
  - dimensions: **170 × 128 × 265 mm**
  - wheelbase: **107.5 mm**
  - track width: **110 mm**
  - wheel diameter: **46 mm**
  - ground clearance: **14 mm**
- Retained purpose-built PLA structures where repeatable geometry was required.
- Retained selected LEGO Technic elements where serviceability, steering adjustment, and rapid replacement were useful.
- Final steering architecture retained as **Ackermann steering**.
- Final Open steering limits retained as:

```text
LEFT   = 70
CENTER = 95
RIGHT  = 125
```

- Wider servo travel was rejected after testing showed increased linkage stress and possible disconnection.

### Drivetrain redesign

- Replaced the earlier **1000 RPM Johnson geared motor** after heavy loading / stall behaviour.
- Replaced the damaged TB6612FNG motor driver.
- Adopted the **JGB37-520, 12 V, 600 RPM** motor.
- Retained the **36T driving → 20T driven** external gear stage.
- Prioritized repeatable operation and drivetrain reliability over maximum rated RPM.
- No recurrence of the earlier motor-stall / driver-failure pattern was reported in retained final testing.

### CAD and mechanical reproducibility

- Final custom PLA structures documented as Onshape-designed parts.
- Repository mechanical evidence recorded as:
  - six CAD render images,
  - two printable STL files,
  - one compressed GLB assembly/model.
- Printed parts were used to preserve repeatable camera, electronics, and drivetrain geometry.

### Power architecture

- Retained **3S 11.1 V 2200 mAh LiPo** as the primary energy source.
- Recorded charged-pack value: approximately **12.2 V**.
- Replaced the earlier **5 V / 3 A Raspberry Pi supply arrangement** after repeated undervoltage warnings.
- Moved to a higher-current regulated 5 V Raspberry Pi supply architecture.
- Preserved common-ground architecture between control electronics, sensors, and motor-driver references.

### Electrical and safety process changes

- Introduced stricter charging supervision and correct 3S / cell-count checks after an earlier LiPo charging incident.
- Introduced explicit polarity checks and a safer keyed / polarised connector strategy after reverse-polarity incidents.
- Added quicker power cut-off and staged drivetrain checks after the motor-stall / driver-failure event.
- Safety changes were treated as engineering responses to observed failures rather than as undocumented assumptions.

### Camera and sensing architecture

- Final V3 sensing stack recorded as:
  - 2 × Raspberry Pi Camera Module 3,
  - MPU6050 IMU,
  - SSD1306 OLED,
  - front illumination LED.
- Final front-camera pose recorded at approximately:
  - **5 mm right of centre**
  - **50° downward pitch**
- Final rear-camera pose recorded at approximately:
  - **45° downward pitch**
  - **0° yaw**
- Camera geometry was revised after earlier poses produced unstable corner-wall detection and late line detection.
- Startup image calibration retained:
  - AE/AWB enabled for approximately 2 seconds,
  - exposure and analogue gain captured,
  - AE/AWB then disabled to stabilize fixed LAB thresholds.
- Final V3 architecture does **not** claim LiDAR, ultrasonic sensing, or wheel encoders.

---

## Open V5 — Final Open Challenge Control

### Control architecture

- Final Open software retained as **Open V5**.
- Final camera stream:

```text
1280 × 680
RGB888
```

- Retained image-processing flow:

```text
Frame
→ Gaussian blur
→ LAB conversion
→ CLAHE
→ colour masks
→ morphology
→ contours
→ geometry
→ proportional steering
```

### Direction logic

- First valid marker determines direction:

```text
Blue first   → Anticlockwise
Orange first → Clockwise
```

- The first valid marker establishes direction but does not increment the lap count.

### Wall-following redesign

- Rejected the earlier symmetric two-wall centring strategy after corner meandering and asymmetric-wall visibility problems.
- Retained direction-aware wall following:
  - both walls visible → proportional geometric error,
  - one wall visible → direction-aware single-wall target,
  - no wall visible → small directional fallback.

### Final tuning

```text
KP = 0.012
LINE_COOLDOWN = 1.3 s
```

- `KP = 0.010` was rejected as too weak.
- `KP = 0.015–0.020` was rejected for Open because steering became more aggressive and increased linkage stress.
- `KP = 0.050` was rejected as excessively aggressive.
- `LINE_COOLDOWN = 0.8 s` was too short and could allow duplicate counting.
- Values approaching `1.8 s` were more likely to miss genuine crossings.
- `1.3 s` was retained as the best observed compromise.

### Lap-counting and stop logic

- Retained **3 laps × 4 counted events = 12 events**.
- Added rising-edge marker logic so one physical marker remaining visible over multiple frames is counted once.
- After 12 counted events:
  - steering centres,
  - motor stops,
  - the main control loop terminates.

### Performance evidence

- Rev6 records **12 successful timed Open Challenge runs**.
- Best observed time: **22 s**.
- Five additional video-backed tests on 15 August 2026 were recorded as:

| ID | Speed command | Time |
|---|---:|---:|
| V-01 | 100 | 23 s |
| V-02 | 90 | 29 s |
| V-03 | 90 | 28 s |
| V-04 | 100 | 22 s |
| V-05 | 100 | 23 s |

- No causal claim is made that speed command alone caused the timing differences because direction, battery state, lighting, and track state were not fully controlled per run.
- No Open Challenge success probability is claimed because the complete failed-attempt denominator was not retained.

---

## Obstacle Challenge Strategy Development

### Navigation redesign

- Rejected fixed / early obstacle-turn commitment after repeated corner-pillar collision / run-over failures.
- Moved to a **continuous visual target** strategy.
- Pillar target position changes continuously with image geometry rather than relying on one pre-timed turn.
- Vertical position / proximity is used to modify the obstacle target as the pillar approaches.
- After the obstacle is no longer relevant, the controller rejoins direction-aware wall-following logic.
- Lower obstacle speed was retained as a trade-off for more perception and steering-correction time.

### Obstacle state architecture

```text
Perceive
→ identify relevant pillar
→ choose passing target
→ continuously steer
→ rejoin wall following
→ complete course
→ parking stage
```

### Validation boundary

- More than **10 successful full Obstacle Challenge runs** were reported during development.
- The complete failed-attempt denominator was not retained; therefore no obstacle success percentage is claimed.
- Rev6 explicitly distinguishes:
  - historical development success,
  - static software checks,
  - physical validation of the exact final executable.

---

## Parking Architecture Development

- Parking architecture changed from an opaque single manoeuvre into a sequence of Ackermann-compatible corrections.
- Rear camera retained as the collision-critical parking view.
- MPU6050 heading retained for relative orientation feedback.
- Intended parking sequence:

```text
Course complete
→ locate parking geometry
→ reverse entry
→ IMU-assisted counter-steer
→ re-observe rear geometry
→ short forward/reverse correction
→ confirm position and heading
→ stop
```

- Non-zero forward / reverse motion is required because the Ackermann chassis cannot rotate in place.
- Parking logic is intended to use repeated observations rather than one long open-loop reverse movement.
- Physical validation of the exact final Obstacle/Parking executable remains pending.

---

## Development Lineage

The Rev6 engineering journal preserves the following confirmed development sequence:

### V0 — LEGO Mobility

- Initial LEGO-dominant mobility architecture.
- Used to establish basic vehicle movement before the final purpose-built chassis.

### V1 — Circuit + Camera

- Added working electronics and camera-based control development.

### V2 — Printed Electronics Mount

- Introduced a 3D-printed electronics mounting architecture.
- Improved packaging repeatability and integration.

### V3 — Purpose-Built Competition Chassis

- Introduced the final competition-focused chassis architecture.
- Added purpose-built PLA packaging.
- Retained serviceable LEGO Technic steering / drivetrain elements where useful.
- Integrated dual-camera geometry and the documented IMU / display sensor stack.

### Open V5 — Final Open Control

- Finalized direction-aware Open Challenge control.
- Retained `KP = 0.012`.
- Retained `LINE_COOLDOWN = 1.3 s`.
- Retained rising-edge marker counting.
- Retained 12-event completion logic.
- Documented 12 successful timed runs with a 22 s best.

> Note: Rev6 does not invent an exact label for prototype sub-versions whose labels were not retained.

---

## Final Competition Release — Pending

The final competition release should only be created when all of the following are true:

- [x] Open V5 source and constants are traced.
- [x] Printable STL files are present.
- [x] Open timing evidence is retained.
- [x] Heading helper is present.
- [x] Raspberry Pi setup and software dependencies are documented.
- [ ] Exact Obstacle Challenge replacement is physically validated.
- [ ] Exact parking behaviour is physically validated using the submitted source.
- [ ] Final validated source is unchanged after the successful robot run.
- [ ] Final Git commit SHA is recorded.
- [ ] Final competition tag / release is created from that validated commit.

The final release must represent the **same executable source that completed the physical robot validation**.

---

**Team Sentio**  
**WRO Future Engineers 2026**  
**Robofun Lab (RFL), India**
