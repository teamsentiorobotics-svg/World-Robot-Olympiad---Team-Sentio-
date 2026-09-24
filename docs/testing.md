# Starlight Failure Log

**Project:** Starlight  
**Team:** Sentio 6010 
**Competition:** WRO Future Engineers 2026  
**Purpose:** Record observed failures, identify likely causes, document engineering changes, and verify whether each change improved the system.

---

## Why We Keep a Failure Log

Starlight was developed through repeated cycles of:

**Build → Test → Observe → Identify Failure → Modify → Retest**

Many failures crossed subsystem boundaries. A mechanical problem could create an electrical failure, a camera-placement problem could appear to be a software problem, and an incorrect visual interpretation could produce an unsuitable steering command.

For this reason, failures are recorded by **observed symptom, diagnosis, engineering response, and retest result** rather than simply listing whether a run passed or failed.

---

## Failure Register

| ID | Observed Failure | Diagnosis / Cause | Engineering Change | Retest / Current Status |
| --- | --- | --- | --- | --- |
| **F01** | Earlier drive motor stalled under high load | Drivetrain load exceeded the useful operating margin of the earlier motor | Replaced the earlier motor with a **12 V, 600 RPM geared encoder motor** and revised the drivetrain operating point | **Passed**. No recurrence of the same stall was reported in retained final testing |
| **F02** | Motor stall was followed by motor-driver damage | Mechanical stall produced excessive electrical stress through the drive system | Replaced the damaged driver, revised drivetrain loading, and introduced faster power cut-off and inspection during testing | **Passed / Monitored** |
| **F03** | Raspberry Pi undervoltage warnings occurred under load | Earlier regulated supply did not provide sufficient current headroom for the computer and connected electronics | Upgraded the Raspberry Pi supply to a higher-current regulated arrangement | **Passed** in subsequent integrated testing |
| **F04** | Camera perception became unstable in important parts of the course | Camera position and field geometry prevented threshold tuning alone from producing reliable observations | Repositioned cameras, redesigned mounts, fixed the camera pose, and later introduced task-specific vision regions | **Passed / Integrated into final architecture** |
| **F05** | Parts of the robot entered the useful camera view | The chassis/body occupied pixels that could otherwise be interpreted as track features | Added a **body-exclusion mask** and reorganized the useful vision regions | **Passed** in the current vision architecture |
| **F06** | Corner and line features were difficult to observe consistently | Earlier camera placement did not provide enough useful near-field geometry during turns | Cameras were repositioned and mounted more rigidly; the vision system was revised around multiple task-specific ROIs | **Retested and retained** |
| **F07** | Large steering corrections stressed or disconnected the steering linkage | Excessive servo travel and aggressive controller corrections placed unnecessary load on the Ackermann mechanism | Added bounded steering commands and reduced excessive control response | **Passed**. Safe steering limits are enforced by the drive layer |
| **F08** | Red could be interpreted as magenta under warm/yellow lighting | Lighting changed the apparent HSV/LAB colour values enough to confuse two functionally different classes | Recalibrated colour ranges under field lighting and strengthened area/state conditions before accepting critical colour cues | **Retested**. Venue calibration remains part of pre-run setup |
| **F09** | Green-pillar interaction near the inner wall produced insufficient clearance | Pillar detection, local wall geometry, and the active steering state could compete during corner exit | Revised perception regions and obstacle-control logic so pillar information is interpreted with course direction and current state | **Retested / Obstacle logic revised** |
| **F10** | Green obstacle contact occurred during a competition configuration | Correct perception alone did not guarantee sufficient physical clearance during the manoeuvre | Revised obstacle approach geometry, steering behaviour, camera interpretation, and post-Nationals chassis/sensing configuration | **Redesigned and retested** |
| **F11** | Parking/course cue could be detected before the robot was in the intended terminal position | A visible magenta region could satisfy a simple detection condition too early | Added stronger confirmation logic using area/state conditions rather than treating one visual detection as sufficient | **Retested** |
| **F12** | A single short-range distance detection could create an unreliable parking transition | One sensor reading could represent a transient observation rather than a stable parking condition | Added repeated ToF detection with an inter-detection pause before advancing the parking state | **Implemented and retested** |
| **F13** | Parking behaviour differed depending on clockwise or anticlockwise course entry | The robot approached the parking area with different position and heading geometry in the two directions | Added direction-dependent entry logic; the anticlockwise branch repositions the robot before joining the shared final parking routine | **Integrated into final parking architecture** |
| **F14** | Camera-only or time-only parking manoeuvres were sensitive to starting pose and motion variation | Fixed-time turns could produce different final orientations as grip, battery condition, and initial pose changed | Combined vision with **IMU heading feedback** and later **ToF distance sensing** for terminal positioning | **Retained in final architecture** |
| **F15** | Full-robot debugging made it difficult to identify whether a failure came from sensing, steering, movement, or heading | Several modules were being tested simultaneously, hiding the original cause | Created dedicated calibration and component tests for colour, servo motion, encoder response, ToF sensing, and heading | **Passed as development workflow**. Component testing now precedes full runs |

---

## Selected Failure Chains

### F01–F02: Drivetrain Stall → Electrical Failure

The earlier drivetrain demonstrated that a mechanical failure could propagate into the electrical system.

```text
High mechanical load
        ↓
Motor stall
        ↓
High electrical stress
        ↓
Motor-driver damage
        ↓
Motor / drivetrain redesign
        ↓
Low-speed retest
        ↓
Full-system testing
```

The response was therefore not limited to replacing the failed component. The team changed the motor operating point and revised how the drivetrain was tested.

---

### F04–F06: Camera Geometry → Perception Failure

Repeated perception problems showed that threshold values cannot compensate for unsuitable camera geometry.

```text
Track feature difficult to observe
        ↓
Check colour thresholds
        ↓
Threshold adjustment insufficient
        ↓
Inspect camera pose and useful image area
        ↓
Reposition camera / redesign mount
        ↓
Create task-specific ROIs
        ↓
Recalibrate on physical field
```

This led to the current vision architecture in which different image regions have different jobs rather than treating the complete camera frame as one undifferentiated input.

---

### F07: Steering Stress → Command Limits

Testing showed that the software could request steering values beyond what was mechanically useful.

The solution was to make the low-level drive layer responsible for enforcing the safe steering range.

```text
Vision requests large correction
        ↓
Drive layer receives request
        ↓
Request exceeds safe mechanical range?
        ↓
YES → Clamp command
NO  → Send command directly
```

This prevents a high-level control error from automatically becoming a mechanical linkage failure.

---

### F08: Warm Lighting → Red / Magenta Confusion

Red and magenta have very different meanings in the obstacle controller:

- **Red:** Obstacle / pillar information
- **Magenta:** Course-state or parking information

Under warm lighting, the visual separation between these classes became less reliable.

The response included:

1. Recalibrating HSV and LAB ranges under the actual lighting.
2. Rejecting blobs below useful area thresholds.
3. Considering the robot's current state before accepting a magenta event.
4. Using geometry and region information alongside colour.
5. Repeating calibration before competition runs.

This failure demonstrated why colour classification cannot be treated independently from lighting and state logic.

---

### F11–F12: Parking Trigger Reliability

Parking is particularly vulnerable to false transitions because a premature state change can terminate an otherwise successful run.

The parking controller therefore moved away from:

```text
Detection → Immediately act
```

toward:

```text
Detection
    ↓
Check required state / phase
    ↓
Check size or distance condition
    ↓
Confirmation
    ↓
Inter-detection delay where applicable
    ↓
Second qualifying observation
    ↓
Execute parking transition
```

The addition of multiple distance sensors also provides local physical information that does not depend entirely on camera appearance.

---

## Engineering Lessons

The most important failures were rarely isolated to one component.

| Failure Origin | Possible Downstream Effect |
| --- | --- |
| Mechanical load | Motor stall → electrical stress |
| Power instability | Interrupted computation or unreliable sensing |
| Camera position | Incorrect or missing visual observation |
| Colour calibration | Incorrect course-state interpretation |
| Steering command | Mechanical stress or obstacle contact |
| State logic | Correct detection used at the wrong moment |
| Sensor placement | Correct measurement of the wrong physical surface |

The development process therefore treats **mechanics, electronics, perception, and control as one connected system**.

---

## Current Debugging Procedure

When a new failure appears:

1. **Record the observable symptom.**
2. **Do not immediately change several parameters.**
3. Identify the most likely layer:
   - Power
   - Mechanical drive
   - Steering
   - Camera geometry
   - Colour classification
   - Distance sensing
   - Heading
   - State logic
4. Run the relevant component test.
5. Change one meaningful variable.
6. Repeat the same test.
7. Integrate the corrected module at low speed.
8. Run the complete challenge.
9. Record whether the failure:
   - Disappeared
   - Became less frequent
   - Changed form
   - Remained unresolved
10. Commit the verified change so the tested software and documentation remain traceable.

---

## Status Definitions

| Status | Meaning |
| --- | --- |
| **Passed** | The modification removed the recorded failure in retained testing |
| **Retested** | The change was tested physically, but no formal reliability percentage is claimed |
| **Integrated** | The solution forms part of the current robot architecture |
| **Monitored** | The failure has not recently recurred but remains something checked during testing |
| **Calibration required** | Architecture is retained, but values may need adjustment for venue conditions |
| **Open** | Root cause or reliable correction has not yet been established |

---

## Evidence Policy

A successful retest shows that a modification can work. It does **not** automatically establish a statistical reliability percentage.

Where the number of total attempts was not recorded, this log uses terms such as **passed**, **retested**, or **no recurrence observed** rather than inventing a success rate.

Failures are intentionally retained in this document because they show how Starlight changed from an early prototype into the current competition vehicle.

---

**Team Sentio 6010**  
**Starlight | WRO Future Engineers 2026**
