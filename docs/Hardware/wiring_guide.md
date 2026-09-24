# Starlight Wiring & Pin Reference

**Project:** Starlight  
**Team:** Sentio 6010 
**Competition:** WRO Future Engineers 2026  
**Configuration:** APOC / Revision 29  
**Last updated:** 22 September 2026

This document is a quick reference for Starlight's **power architecture, physical wiring, sensor interfaces and software GPIO assignments**.

> [!IMPORTANT]
> The [final schematic](../../schemes/schematic.png) is the authority for physical wiring.
>
> Source-code pin definitions are authoritative for software GPIO assignments. If this document, the schematic and the robot disagree, the discrepancy must be resolved before competition.

---

# Power Architecture

The current robot uses one 3S LiPo battery with separate propulsion and regulated electronics branches.

```text
                         3S LiPo
                   11.1 V nominal
                         │
                  Main power switch
                         │
        ┌────────────────┴─────────────────┐
        │                                  │
        │                                  │
        ▼                                  ▼
   MOTOR BRANCH                     REGULATED BRANCHES
        │                                  │
        ▼                         ┌────────┴────────┐
   TB6612FNG VMOT                 │                 │
        │                         ▼                 ▼
        ▼                    5 V / ~5 A        5 V / 3 A
600 RPM encoder motor         Pi supply       auxiliary rail
                                  │                 │
                                  ▼                 ├── Steering servo
                            Raspberry Pi 5          │
                                  │                 └── other 5 V loads
                 ┌────────────────┼───────────────┐
                 │                │               │
                 ▼                ▼               ▼
              Camera 0         Camera 1        I2C bus
                                                   │
                              ┌────────────────────┼─────────────────┐
                              │                    │                 │
                              ▼                    ▼                 ▼
                           MPU6050             VL53L0X #1       VL53L0X #2
                                                                     │
                                                                     ▼
                                                                VL53L0X #3
```

All control electronics share a **common electrical reference / ground**.

The propulsion branch and regulated electronics branches serve different loads even though they share the same battery.

---

# Current Hardware Relevant to Wiring

| Qty. | Component | Electrical role |
| ---: | --- | --- |
| 1 | Raspberry Pi 5, 4 GB | Main controller |
| 2 | Raspberry Pi Camera Module 3 Wide | Vision inputs |
| 3 | VL53L0X ToF sensors | Short-range distance sensing |
| 1 | MPU6050-based module | Heading / gyro input |
| 1 | 12 V, 600 RPM geared encoder motor | Propulsion |
| 1 | Integrated quadrature encoder | Shaft rotation and direction |
| 1 | TB6612FNG motor driver | Motor PWM and direction |
| 1 | DS3225 servo | Ackermann steering |
| 1 | 3S LiPo, 11.1 V, 2200 mAh | Main energy source |
| 1 | Regulated 5 V Pi supply, approximately 5 A | Raspberry Pi rail |
| 1 | 5 V / 3 A buck converter / BEC | Auxiliary regulated rail |
| 1 | Main power switch | Vehicle power isolation |
| 1 | Momentary Start button | Autonomous-run start input |

---

# Software GPIO Reference

These values follow the current robot source and Revision 27 wiring baseline.

| Function | BCM GPIO / Interface | Source / role |
| --- | ---: | --- |
| **Motor PWM** | **GPIO13** | `src/drive.py` |
| **Motor direction 1** | **GPIO5** | `src/drive.py` |
| **Motor direction 2** | **GPIO6** | `src/drive.py` |
| **Steering servo** | **GPIO22** | `src/drive.py` |
| **Encoder channel A** | **GPIO17** | `src/drive.py` |
| **Encoder channel B** | **GPIO27** | `src/drive.py` |
| **I2C SDA** | **GPIO2** | Shared sensor bus |
| **I2C SCL** | **GPIO3** | Shared sensor bus |
| **MPU6050 bus** | **I2C bus 1** | `src/heading.py` |
| **MPU6050 address** | **`0x68`** | `src/heading.py` |
| **ToF 1 XSHUT** | **GPIO16** | Distance-sensor initialization |
| **ToF 2 XSHUT** | **GPIO20** | Distance-sensor initialization |
| **ToF 3 XSHUT** | **GPIO21** | Distance-sensor initialization |

---

# Motor Driver Interface

The current drive interface uses:

```text
PWM_PIN   = GPIO13
IN1_PIN   = GPIO5
IN2_PIN   = GPIO6
```

Motor PWM frequency:

```text
1000 Hz
```

Conceptually:

```text
Raspberry Pi
     │
     ├── GPIO13 ──► PWM
     ├── GPIO5  ──► IN1
     └── GPIO6  ──► IN2
                       │
                       ▼
                  TB6612FNG
                       │
                       ▼
              600 RPM drive motor
```

The motor receives propulsion power through the motor-driver battery branch.

---

# Current Drive Motor

The current competition motor is:

```text
12 V geared DC motor
Nominal output speed: 600 RPM
Integrated quadrature encoder
```

The external drivetrain ratio is:

```text
1 : 1
```

The earlier:

```text
1000 RPM motor
36T → 24T
1.5 speed-increasing ratio
```

belongs to historical development documentation and must not be used as the current wiring/configuration reference.

---

# Encoder Wiring

The current drive motor includes an integrated quadrature encoder.

Software uses:

```text
ENCODER_A_PIN = GPIO17
ENCODER_B_PIN = GPIO27
```

Conceptually:

```text
ENCODER
   │
   ├── Channel A ──► GPIO17
   ├── Channel B ──► GPIO27
   ├── Supply
   └── Ground
```

The two channels allow the controller to observe:

```text
shaft rotation
+
rotation direction
```

---

## Encoder Electrical Warning

> [!CAUTION]
> Do not assume the encoder's output voltage is Raspberry Pi-safe simply because its encoder electronics use a particular supply voltage.

Before direct GPIO connection:

1. verify the installed encoder's output-high voltage;
2. verify common ground;
3. use level shifting or signal conditioning if required;
4. keep encoder signal wiring away from motor-current wiring where practical.

Brushed motor noise can otherwise produce false counts.

The software-level encoder test is:

```text
src/encoder_test.py
```

---

# Steering Wiring

The steering servo signal is connected to:

```text
GPIO22
```

Servo PWM frequency:

```text
50 Hz
```

Conceptually:

```text
Raspberry Pi GPIO22
        │
        ▼
   Servo signal

Regulated 5 V rail
        │
        ▼
    Servo VCC

Common ground
        │
        ▼
    Servo GND
```

The servo should **not** be powered directly from an unsuitable Raspberry Pi GPIO power path.

---

# Current Steering Values

The current `src/drive.py` defines:

```text
LEFT   = 40
CENTER = 75
RIGHT  = 110
```

These values are **servo command values**.

They are not measured road-wheel steering angles.

Do not silently replace them with older values such as:

```text
35 / 75 / 105
```

unless the physically tested final source has actually been recalibrated.

---

# I2C Bus

The main I2C bus uses:

```text
SDA = GPIO2
SCL = GPIO3
```

Connected sensor systems include:

```text
MPU6050
VL53L0X #1
VL53L0X #2
VL53L0X #3
```

Conceptually:

```text
Raspberry Pi
   │
   ├── GPIO2 / SDA ──────────────────────────────┐
   │                                             │
   └── GPIO3 / SCL ──────────────────────────────┤
                                                 │
                  ┌──────────────────────────────┼───────────────┐
                  │                              │               │
                  ▼                              ▼               ▼
              MPU6050                       VL53L0X #1      VL53L0X #2
                  │                                              │
                  │                                              ▼
                  └───────────────────────────────────────── VL53L0X #3
```

---

# MPU6050

The heading module uses:

```text
I2C bus : 1
Address : 0x68
```

Software:

```text
src/heading.py
```

The MPU6050 provides angular-rate information used to estimate relative heading.

It does not provide an absolute drift-free compass heading.

---

# Three VL53L0X Sensors

The current robot uses:

```text
3 × VL53L0X
```

All three sensors share:

```text
SDA
SCL
power
ground
```

but each requires an independent **XSHUT** control line.

| Sensor | XSHUT |
| --- | ---: |
| **ToF 1** | GPIO16 |
| **ToF 2** | GPIO20 |
| **ToF 3** | GPIO21 |

---

## Why XSHUT Is Required

Each VL53L0X begins at the same default I2C address.

If all three sensors became active simultaneously at that address, the Raspberry Pi could not reliably address them individually.

Startup therefore follows:

```text
All ToF sensors OFF
        ↓
Enable ToF 1
        ↓
Assign unique address
        ↓
Enable ToF 2
        ↓
Assign unique address
        ↓
Enable ToF 3
        ↓
Assign unique address
        ↓
Verify all three
```

The three independent XSHUT lines make this possible.

---

# ToF Wiring Concept

```text
                         Raspberry Pi 5
                               │
              ┌────────────────┴────────────────┐
              │                                 │
          GPIO2 SDA                         GPIO3 SCL
              │                                 │
        ┌─────┼─────────┐                 ┌─────┼─────────┐
        │     │         │                 │     │         │
        ▼     ▼         ▼                 ▼     ▼         ▼
      ToF1  ToF2      ToF3              ToF1  ToF2      ToF3


GPIO16 ─────────────────────────► ToF 1 XSHUT

GPIO20 ─────────────────────────► ToF 2 XSHUT

GPIO21 ─────────────────────────► ToF 3 XSHUT
```

All three sensors require a shared electrical reference.

The low-level sensor test is:

```text
src/TUF_test.py
```

---

# ToF Mounting Matters

The electrical connection alone does not determine what a distance reading means.

Each sensor must also be mounted so that its measurement direction corresponds to the intended:

- wall;
- parking boundary;
- nearby obstacle;
- stopping reference.

Therefore:

```text
sensor identity
+
GPIO identity
+
software identity
+
physical direction
```

must remain consistent.

Label the ToF connectors physically.

---

# Cameras

Starlight uses:

```text
2 × Raspberry Pi Camera Module 3 Wide
```

The software uses separate camera interfaces for the two available camera channels.

The retained logical mapping is:

| Camera | Index | Primary role |
| --- | ---: | --- |
| **Camera 0** | `0` | Main navigation / challenge perception |
| **Camera 1** | `1` | Secondary / parking view where used |

> [!NOTE]
> Camera placement changed during the post-Nationals redesign.
>
> Camera numbering is a **software interface**, while "front", "rear" or "rear-mounted" describes physical placement. Do not assume those are interchangeable labels after rebuilding the robot.

Before competition:

```bash
rpicam-hello --list-cameras
```

should be used to confirm both cameras.

---

# Main Power Branch

The drive motor uses the battery propulsion branch through the TB6612FNG.

```text
3S LiPo
   │
   ▼
Main switch
   │
   ▼
TB6612FNG VMOT
   │
   ▼
600 RPM drive motor
```

Do not route raw 3S LiPo voltage into a device expecting a regulated 5 V or 3.3 V supply.

---

# Raspberry Pi Supply

The current BOM specifies a regulated Raspberry Pi supply of approximately:

```text
5 V / 5 A capacity
```

This is a **supply-capacity rating**, not a claim that the Raspberry Pi continuously draws 5 A.

Earlier development produced Raspberry Pi undervoltage warnings, so adequate transient current margin is part of the final power architecture.

---

# Auxiliary Regulated Rail

The BOM retains a:

```text
5 V / 3 A buck converter / BEC
```

as an auxiliary regulated supply where used.

Typical regulated loads include the steering / low-voltage actuation side according to the final schematic.

The physical schematic remains authoritative for the exact final distribution.

---

# Common Ground

Connected control systems must share a common electrical reference.

Conceptually:

```text
Battery ground
      │
      ├── Motor driver ground
      ├── Raspberry Pi supply ground
      ├── Auxiliary regulator ground
      ├── Servo ground
      ├── MPU6050 ground
      ├── ToF grounds
      └── Encoder ground
```

Without a valid common reference, logic signals may not be interpreted correctly.

---

# Important Electrical Notes

- The **600 RPM motor** uses the propulsion branch through the TB6612FNG.
- The Raspberry Pi uses its regulated **5 V / approximately 5 A** supply.
- The auxiliary **5 V / 3 A** regulator is retained where required.
- The current robot uses **three VL53L0X sensors**, not two.
- The ToF XSHUT pins are **GPIO16, GPIO20 and GPIO21**.
- The encoder channels used by the current drive source are **GPIO17 and GPIO27**.
- The MPU6050 uses **I2C bus 1** at **`0x68`**.
- All connected control branches require an appropriate common electrical reference.
- Raw 3S battery voltage must not be connected directly to 5 V or 3.3 V inputs.
- Motor wiring should be kept away from low-level encoder and sensor wiring where practical.
- Connector and cable strain relief is part of the electrical design.
- Exact physical routing should follow the final schematic rather than an old robot photograph.

---

# Current Pin Summary

```text
MOTOR
GPIO13  → Motor PWM
GPIO5   → Motor direction IN1
GPIO6   → Motor direction IN2

STEERING
GPIO22  → Steering servo signal

ENCODER
GPIO17  → Encoder channel A
GPIO27  → Encoder channel B

I2C
GPIO2   → SDA
GPIO3   → SCL

MPU6050
Bus 1
Address 0x68

TOF XSHUT
GPIO16  → ToF 1
GPIO20  → ToF 2
GPIO21  → ToF 3
```

---

# Wiring Verification Checklist

Before a competition run:

- [ ] Battery polarity verified
- [ ] Main switch works
- [ ] Motor-driver battery branch secure
- [ ] Raspberry Pi regulated supply is 5 V
- [ ] Auxiliary regulated supply is 5 V where used
- [ ] Common ground verified
- [ ] GPIO5 and GPIO6 motor direction wiring verified
- [ ] GPIO13 motor PWM verified
- [ ] GPIO22 steering signal verified
- [ ] GPIO17 encoder channel A verified
- [ ] GPIO27 encoder channel B verified
- [ ] Encoder signal voltage confirmed safe
- [ ] GPIO2 SDA verified
- [ ] GPIO3 SCL verified
- [ ] MPU6050 responds at `0x68`
- [ ] ToF 1 XSHUT verified on GPIO16
- [ ] ToF 2 XSHUT verified on GPIO20
- [ ] ToF 3 XSHUT verified on GPIO21
- [ ] All three ToF sensors initialize from cold boot
- [ ] ToF sensors receive separate working addresses
- [ ] ToF physical labels match software identities
- [ ] Both cameras detected
- [ ] Camera ribbon cables strain-relieved
- [ ] No wire can enter the drivetrain
- [ ] No wire can enter the steering mechanism
- [ ] No exposed conductor can contact the chassis or adjacent terminal
- [ ] Motor acceleration does not reset the Raspberry Pi
- [ ] Servo movement does not produce an undervoltage warning

---

# Recorded Voltage Measurements

The following values were recorded during electrical testing:

| Measurement point | Condition | Recorded value |
| --- | --- | ---: |
| LiPo | Before run | **11.1 V** |
| LiPo | After multiple runs | **10.8 V** |
| Motor driver | Motor OFF | **11.1 V** |
| Motor driver | Motor ON | **10.8 V** |
| Auxiliary / Buck 1 | Tested output | **5.0 V** |
| Raspberry Pi supply | Tested output | **5.0 V** |

> [!NOTE]
> These measurements are retained as recorded observations.
>
> They should not automatically be treated as a full electrical characterization of the current Revision 27 system unless they were measured after the final **600 RPM motor + three-ToF** configuration was assembled.

No final peak-current trace is claimed here unless separately recorded.

---

# Full-Load Power Check

The final electrical configuration should be tested with:

```text
Raspberry Pi running
+
both cameras active
+
MPU6050 active
+
three ToF sensors ranging
+
encoder active
+
servo moving
+
drive motor accelerating
```

Monitor for:

```text
Pi undervoltage
unexpected reboot
camera disconnect
I2C failure
encoder corruption
servo reset
motor-driver overheating
```

A system that measures 5.0 V while sitting motionless has not yet demonstrated that it can hold that rail during a real run. Electricity remains inconveniently interested in load.

---

# Historical Wiring Notes

The following items may still appear in older documentation or commits:

| Historical reference | Current status |
| --- | --- |
| JGB37-520 motor | Superseded |
| 1000 RPM Rhino motor | Historical supplier / development reference |
| Two ToF sensors | Superseded by **three ToF sensors** |
| 36T → 24T current gearing | Historical; current external ratio is **1:1** |
| Steering `35 / 75 / 105` | Older calibration |
| OLED as permanent payload | Development equipment / not required by current architecture |

Historical information should remain traceable, but it must not be presented as the current competition wiring configuration.

---

# Related Documentation

| Document | Purpose |
| --- | --- |
| [`bom.md`](bom.md) | Current hardware inventory |
| [`drivetrain.md`](drivetrain.md) | Motor, gearing, differential and encoder architecture |
| [`../engineering-decisions.md`](../engineering-decisions.md) | Why major hardware choices were made |
| [`../failure-log.md`](../failure-log.md) | Electrical and mechanical failures that drove changes |
| [`../testing.md`](../testing.md) | Hardware and integrated testing |
| [`../development/apoc-hardware-update.md`](../development/apoc-hardware-update.md) | Post-Nationals hardware redesign |
| [`../../schemes/schematic.png`](../../schemes/schematic.png) | Authoritative physical wiring schematic |
| [`../../src/drive.py`](../../src/drive.py) | Motor, servo and encoder GPIO definitions |
| [`../../src/heading.py`](../../src/heading.py) | MPU6050 interface |
| [`../../src/TUF_test.py`](../../src/TUF_test.py) | Three-sensor distance test |
| [`../../src/encoder_test.py`](../../src/encoder_test.py) | Encoder verification |
| [`../../src/servo_test.py`](../../src/servo_test.py) | Steering verification |

---

## Configuration Rule

The four references below should describe the same robot:

```text
Physical wiring
      =
schematic
      =
source-code GPIO assignments
      =
documentation
```

Any mismatch should be corrected before the configuration is frozen.

---

**Team Sentio 6010**  
**Starlight | WRO Future Engineers 2026**
