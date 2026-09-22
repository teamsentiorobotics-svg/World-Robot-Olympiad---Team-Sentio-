# Starlight Failure Log

**Project:** Starlight  
**Team:** Sentio 1747  
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
| **F02** | Motor stall was followed by motor-driver damage | Mechanical stall produced excessive electrical stress through the drive system | Replaced the damaged driver, revised drivetrain loading, and introduced faster power cut-off and inspection during testing | **Passed / monitored** |
| **F03** | Raspberry Pi undervoltage warnings occurred under load | Earlier regulated supply did not provide sufficient current headroom for the computer and connected electronics | Upgraded the Raspberry Pi supply to a higher-current regulated arrangement | **Passed** in subsequent integrated testing |
| **F04** | Camera perception became unstable in important parts of the course | Camera position and field geometry prevented threshold tuning alone from producing reliable observations | Repositioned cameras, redesigned mounts, fixed the camera pose, and later introduced task-specific vision regions | **Passed / integrated into final architecture** |
| **F05** | Parts of the robot entered the useful camera view | The chassis/body occupied pixels that could otherwise be interpreted as track features | Added a **body-exclusion mask** and reorganized the useful vision regions | **Passed** in the current vision architecture |
| **F06** | Corner and line features were difficult to observe consistently | Earlier camera placement did not provide enough useful near-field geometry during turns | Cameras were repositioned and mounted more rigidly; the vision system was revised around multiple task-specific ROIs | **Retested and retained** |
| **F07** | Large steering corrections stressed or disconnected the steering linkage | Excessive servo travel and aggressive controller corrections placed unnecessary load on the Ackermann mechanism | Added bounded steering commands and reduced excessive control response | **Passed**. Safe steering limits are enforced by the drive layer |
| **F08** | Red could be interpreted as magenta under warm/yellow lighting | Lighting changed the apparent HSV/LAB colour values enough to confuse two functionally different classes | Recalibrated colour ranges under field lighting and strengthened area/state conditions before accepting critical colour cues | **Retested; venue calibration remains part of pre-run setup** |
| **F09** | Green-pillar interaction near the inner wall produced insufficient clearance | Pillar detection, local wall geometry, and the active steering state could compete during corner exit | Revised perception regions and obstacle-control logic so pillar information is interpreted with course direction and current state | **Retested / obstacle logic revised** |
| **F10** | Green obstacle contact occurred during a competition configuration | Correct perception alone did not guarantee sufficient physical clearance during the manoeuvre | Revised obstacle approach geometry, steering behaviour, camera interpretation, and post-Nationals chassis/sensing configuration | **Redesigned and retested** |
| **F11** | Parking/course cue could be detected before the robot was in the intended terminal position | A visible magenta region could satisfy a simple detection condition too early | Added stronger confirmation logic using area/state conditions rather than treating one visual detection as sufficient | **Retested** |
| **F12** | A single short-range distance detection could create an unreliable parking transition | One sensor reading could represent a transient observation rather than a stable parking condition | Added repeated ToF detection with an inter-detection pause before advancing the parking state | **Implemented and retested** |
| **F13** | Parking behaviour differed depending on clockwise or anticlockwise course entry | The robot approached the parking area with different position and heading geometry in the two directions | Added direction-dependent entry logic; the anticlockwise branch repositions the robot before joining the shared final parking routine | **Integrated into final parking architecture** |
| **F14** | Camera-only or time-only parking manoeuvres were sensitive to starting pose and motion variation | Fixed-time turns could produce different final orientations as grip, battery condition, and initial pose changed | Combined vision with **IMU heading feedback** and later **ToF distance sensing** for terminal positioning | **Retained in final architecture** |
| **F15** | Full-robot debugging made it difficult to identify whether a failure came from sensing, steering, movement, or heading | Several modules were being tested simultaneously, hiding the original cause | Created dedicated calibration and component tests for colour, servo motion, encoder response, ToF sensing, and heading | **Passed as development workflow; component testing now precedes full runs** |

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
