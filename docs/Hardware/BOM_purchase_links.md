# Starlight Bill of Materials

**Team:** Sentio 1747  
**Robot:** Starlight  
**Competition:** WRO Future Engineers 2026  
**Configuration:** APOC / Revision 27  
**Last updated:** 22 September 2026

---

## Configuration Status

This document describes the **current physical Starlight configuration** used after the post-Nationals redesign.

The authoritative current configuration is:

```text
COMPUTE      : Raspberry Pi 5, 4 GB
VISION       : 2 × Raspberry Pi Camera Module 3 Wide
RANGE        : 3 × VL53L0X Time-of-Flight sensors
ORIENTATION  : MPU6050-based heading sensor
DRIVE MOTOR  : 12 V geared DC encoder motor, nominal 600 RPM
ENCODER      : integrated quadrature encoder
STEERING     : DS3225 servo + Ackermann linkage
DRIVER       : TB6612FNG
BATTERY      : 3S LiPo, 11.1 V, 2200 mAh
DRIVE        : mechanical 4WD
DIFFERENTIAL : mechanical differential
GEAR STAGE   : 1:1 external gearing
START SYSTEM : one main power switch + one Start button
CHASSIS      : custom printed structure + LEGO Technic mechanisms
```

> [!IMPORTANT]
> Earlier references to a **1000 RPM Rhino motor**, **two ToF sensors**, **325 encoder counts per output revolution**, or a **36T → 24T current drivetrain ratio** are historical development information.
>
> They do **not** describe the current Revision 27 robot.

---

# 1. Current Competition Robot

## Core Electronics and Motion Hardware

| Qty. | Component | Current role on Starlight | Purchase link / source |
| ---: | --- | --- | --- |
| 1 | **Raspberry Pi 5, 4 GB** | Main computer running vision, sensor interfaces, challenge logic and control | [Robu.in](https://robu.in/product/raspberry-pi-5-model-4gb/) |
| 2 | **Raspberry Pi Camera Module 3 Wide** | Track, obstacle and parking perception | [Robu.in](https://robu.in/product/raspberry-pi-camera-module-3-wide/) |
| 3 | **VL53L0X Time-of-Flight distance sensor breakout** | Short-range physical gap measurement during parking and wall-relative movement | [Robokits India](https://robokits.co.in/sensors/lidar-laser-rangefinders/tiny-lidar-laser-ranging-sensor-tof-based-on-vl53l0x-2-meters-range) |
| 1 | **12 V geared DC encoder motor, nominal 600 RPM** | Main drivetrain motor | **Current installed motor. Exact SKU / purchase URL should be confirmed from the physical motor before final hardware freeze.** |
| 1 | **Integrated quadrature encoder** | Reports drive-motor shaft rotation and direction | Integrated into current 600 RPM motor |
| 1 | **TB6612FNG motor-driver module** | Motor direction and PWM control | [Robu.in](https://robu.in/product/motor-driver-tb6612fng-module-performance-ultra-small-volume-3-pi-matching-performance-ultra-l298n/) |
| 1 | **DS3225 25 kg-cm digital servo, 180°** | Front Ackermann steering | [Robu.in](https://robu.in/product/pro-range-ds3225-25kgcm-metal-gear-digital-servo-motor-180-degree/) |
| 1 | **MPU6050-based 10DOF module** | Gyro input for relative-heading estimation | [Robu.in](https://robu.in/product/mpu6050hmc5883lbmp180-10dof-3-axis-gyro-3-axis-acceleration-3-axis-magnetic-field-air-pres/) |
| 1 | **MicroSD card** | Raspberry Pi OS, code and calibration files | [Amazon.in](https://www.amazon.in/gp/product/B08L5HMJVW) |
| 1 | **Main power switch** | Isolates complete vehicle power | Source locally |
| 1 | **Momentary Start push button** | Starts autonomous operation after initialization | Source locally |
| 1 | **Status / illumination LED** | Status indication and/or illumination where retained | Source locally |

---

## Current vs Historical Hardware

| Item | Current Rev27 | Historical / superseded |
| --- | --- | --- |
| Drive motor | **600 RPM geared encoder motor** | Rhino GB37 RMCS-4091 / 1000 RPM reference |
| External gearing | **1:1** | 36T → 24T, ratio 1.5 |
| ToF sensors | **3 × VL53L0X** | 2 × VL53L0X |
| Encoder calibration | **Installed encoder must be calibrated** | 325 counts/output revolution worked example |
| Parking sensing | **Camera + IMU + 3 ToF + movement feedback** | Camera + IMU / dual-ToF development architecture |

---

# 2. Current Drive Motor and Encoder

The current competition drivetrain uses:

```text
12 V geared DC motor
Nominal gearbox-output speed: 600 RPM
Integrated quadrature encoder
External drivetrain ratio: 1:1
```

The motor provides propulsion while the encoder provides shaft-motion feedback.

---

## Encoder Role

The encoder supports:

- drive-response testing;
- movement repeatability;
- direction detection;
- encoder-targeted movement;
- stall or no-motion detection;
- comparison of commanded and observed drivetrain movement.

Conceptually:

```text
Movement request
      ↓
Motor command
      ↓
Encoder pulses
      ↓
Count / direction
      ↓
Target reached?
   ↙       ↘
 No        Yes
 ↓          ↓
Continue    Stop
```

---

## Encoder Calibration Rule

Do **not** document:

```text
325 counts/output revolution
```

as a specification of the current motor unless it has actually been measured or confirmed for the installed unit.

That value belongs to the older 1000 RPM supplier example.

The current installed encoder should instead be characterized using:

```text
src/encoder_test.py
```

Record:

```text
encoder counting mode
edges counted per cycle
count direction
counts per gearbox-output revolution
repeatability
```

before using a physical distance-per-count conversion.

---

## Encoder Electrical Interface

The encoder interface should provide:

```text
Channel 1
Channel 2
Encoder power
Ground
```

The Raspberry Pi and encoder must share an appropriate signal reference.

> [!CAUTION]
> Encoder supply voltage alone does not prove that its output signal is safe for direct Raspberry Pi GPIO.
>
> Verify actual encoder output levels on the installed motor before connecting the signals directly.

Route encoder signal wiring away from high-current motor wiring where practical.

---

# 3. Three VL53L0X Distance Sensors

Starlight now uses:

```text
3 × VL53L0X
```

as permanent competition sensors.

| Qty. | Sensor | Current role | Purchase link |
| ---: | --- | --- | --- |
| 3 | **VL53L0X ToF breakout** | Local distance measurement during parking, stopping and wall-relative movement | [Robokits India](https://robokits.co.in/sensors/lidar-laser-rangefinders/tiny-lidar-laser-ranging-sensor-tof-based-on-vl53l0x-2-meters-range) |

These sensors complement the cameras rather than replacing visual perception.

---

## Why Three ToF Sensors?

Each sensor provides information about a local physical gap.

The architecture separates:

```text
CAMERA
→ What feature is visible?

IMU
→ How much has the robot turned?

ENCODER
→ How much has the drivetrain moved?

TOF
→ How far away is the nearby physical surface?
```

The value of the sensor stack comes from these different measurements being used together.

---

# 4. Three-Sensor I2C Architecture

VL53L0X sensors begin with the same default I2C address.

Three sensors therefore cannot simply be enabled simultaneously and expected to identify themselves individually.

Starlight uses dedicated **XSHUT** lines:

| ToF | XSHUT GPIO |
| --- | ---: |
| **ToF 1** | GPIO16 |
| **ToF 2** | GPIO20 |
| **ToF 3** | GPIO21 |

All three share the main I2C bus:

```text
SDA → GPIO2
SCL → GPIO3
```

---

## Startup Sequence

```text
Power on
   ↓
Hold ToF 1 OFF
Hold ToF 2 OFF
Hold ToF 3 OFF
   ↓
Enable ToF 1
   ↓
Assign unique I2C address
   ↓
Enable ToF 2
   ↓
Assign unique I2C address
   ↓
Enable ToF 3
   ↓
Assign unique I2C address
   ↓
Verify all three sensors
   ↓
Enter waiting state
```

The distance-sensor hardware test is:

```text
src/TUF_test.py
```

---

## ToF Harness Requirements

Provide:

- shared SDA;
- shared SCL;
- appropriate shared supply;
- common ground;
- separate XSHUT line for each sensor;
- labelled sensor connectors;
- rigid sensor mounts;
- repeatable sensor orientation.

The software identifier and physical sensor must remain matched after repairs.

---

# 5. ToF Mechanical Integration

Each VL53L0X requires a rigid mount.

The mount determines **which physical surface the sensor measures**.

Check that:

- the optical aperture is unobstructed;
- no chassis edge enters the useful sensing path;
- wiring cannot move in front of the sensor;
- the sensor cannot rotate inside the mount;
- the intended wall or parking reference remains inside the useful measurement region.

The current chassis therefore uses:

```text
3 × ToF sensor positions
```

rather than the earlier two-sensor arrangement.

---

# 6. Current Sensor-Fusion Architecture

The Revision 27 architecture is:

```text
CAMERAS  = field appearance + image geometry
TOF ×3   = direct short-range distance
IMU      = relative heading / turn information
ENCODER  = drivetrain shaft movement
PI       = state logic + perception + control
DRIVER   = propulsion direction + PWM
SERVO    = Ackermann steering
```

---

## Sensor Roles

| Sensor | Primary question |
| --- | --- |
| Camera Module 3 Wide ×2 | What track, wall, pillar or parking feature is visible? |
| VL53L0X ×3 | How far away is the nearby physical surface? |
| MPU6050 | How much has the robot turned? |
| Motor encoder | How much has the drive shaft rotated and in which direction? |

No sensor is treated as a perfect substitute for another.

---

# 7. Current Drivetrain

Starlight uses:

```text
Drive type     : mechanical 4WD
Drive motor    : 12 V geared encoder motor, 600 RPM
External ratio : 1:1
Differential   : mechanical differential
Feedback       : integrated quadrature encoder
Steering       : front Ackermann
```

---

## 1:1 External Gearing

The current external drivetrain ratio is:

\[
G = 1
\]

Therefore, ideally:

```text
1 motor gearbox-output revolution
             ↓
1 wheel-transmission revolution
```

The exact current gear tooth counts should follow the physically installed drivetrain.

Do not describe the historical:

```text
36T driving → 24T driven
```

pair as the current gear stage.

That historical configuration gave:

\[
G = \frac{36}{24} = 1.5
\]

and was a speed-increasing drivetrain configuration.

---

## Why the Current Ratio Changed

The current 1:1 arrangement prioritizes:

- wheel torque;
- controllability;
- drivetrain operating margin;
- reliable acceleration;
- repeatable motion.

over maximum theoretical speed.

This decision followed earlier high-load and stall behaviour.

---

# 8. Mechanical Differential

A turn requires the inside and outside wheels to travel different distances.

```text
Outer wheel
→ longer path

Inner wheel
→ shorter path
```

The mechanical differential allows driven sides to rotate at different speeds while receiving propulsion from the same motor.

This works together with Ackermann steering:

```text
ACKERMANN
→ different steering angles

DIFFERENTIAL
→ different wheel speeds

ENCODER
→ drive-source rotation feedback
```

---

# 9. Steering Hardware

| Item | Current role |
| --- | --- |
| **DS3225 servo** | Steering actuator |
| **Ackermann linkage** | Produces different inside/outside steering angles |
| **LEGO / printed links** | Mechanical steering transmission |
| **Software steering clamp** | Prevents excessive servo travel |

Published control interface:

```text
Servo signal: GPIO22
PWM: 50 Hz
```

Calibration values should follow the physically tested final source.

Servo command values are **not** measured road-wheel angles.

---

# 10. Camera Hardware

Starlight uses:

```text
2 × Raspberry Pi Camera Module 3 Wide
```

The current mechanical arrangement places the cameras in repeatable rigid mounts designed around the final field geometry.

The documented viewing direction is approximately:

```text
60° from horizontal
```

Camera pose affects:

- ROI geometry;
- wall location in the frame;
- pillar appearance;
- marker detection;
- parking geometry.

The mount is therefore part of the sensing system, not decorative structure.

---

# 11. Power System

| Qty. | Component | Purpose | Purchase link / status |
| ---: | --- | --- | --- |
| 1 | **3S LiPo, 11.1 V, 2200 mAh** | Main energy source | [Amazon.in](https://www.amazon.in/PRAYOG-INDIA-ROBOTICS-Rechargeable-Connector/dp/B0H9L6B694) |
| 1 | **LiPo balance charger** | Charging and cell balancing | [Amazon.in](https://www.amazon.in/Pro3D-B6-AC-Battery-Balance-Charger/dp/B0CV9H28MQ) |
| 1 | **Regulated 5 V Raspberry Pi supply, approximately 5 A** | Main computer rail | Exact installed unit should be recorded |
| 1 | **5 V / 3 A buck converter / BEC** | Auxiliary regulated rail where used | [Robu.in](https://robu.in/product/ultra-small-size-dc-dc-5v-3a-bec-power-supply-buck-step-down-module/) |
| 1 | **Main power switch** | Main vehicle isolation | Source locally |
| — | Distribution wiring / terminals | Power distribution | Installed wiring |
| — | Battery connector pair | Battery connection | Match installed pack |
| — | Heat-shrink / insulation | Electrical protection | Source locally |

---

## Power Validation

Test the regulated electronics rail with:

```text
Raspberry Pi active
+
both cameras active
+
all three ToF sensors ranging
+
MPU6050 active
+
encoder active
+
servo moving
+
motor accelerating
```

Earlier undervoltage behaviour is one reason the higher-current Pi supply was retained.

---

# 12. Structural and Manufacturing Materials

Starlight combines custom printed structures with LEGO Technic mechanisms.

| Item | Purpose |
| --- | --- |
| **PLA / final print material** | Chassis, electronics structure and sensor mounts |
| **Rigid camera mounts** | Preserve calibrated camera pose |
| **3 × rigid ToF mounts** | Preserve range-sensor direction |
| **Motor mount / bracket** | Secure current 600 RPM motor |
| **Motor-to-drivetrain coupling** | Transfer motor output to mechanical transmission |
| **Electronics mounts** | Secure Raspberry Pi and electrical hardware |
| **Fasteners** | Printed-part and electronics assembly |
| **Perfboard / distribution board** | Electrical mounting where used |
| **Hook-up wire / ribbon cable** | Signal and power distribution |
| **Cable ties / heat-shrink** | Cable management and protection |

See:

```text
Models/
```

for current mechanical model files.

---

# 13. LEGO Technic Drivetrain Components

LEGO Technic parts are retained where serviceability and mechanical adjustment are useful.

| Component | Role | Reference |
| --- | --- | --- |
| **2 × 4 L Beam** | Compact mechanical support | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=32140) |
| **Half bush** | Axle spacing / retention | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=4265c&idColor=3) |
| **Bush** | Axle retention | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3713) |
| **2L axle connector** | Joins shaft sections | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=6538c) |
| **28-tooth differential** | Allows unequal driven-wheel speed | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=73071) |
| **24-tooth gear** | Retained drivetrain inventory / historical or other transmission use | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3648) |
| **20-tooth gear** | Intermediate drivetrain use where installed | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=32269) |
| **12-tooth bevel gear** | Compact direction-changing transmission | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=6589) |
| **9-unit beam** | Drivetrain structure | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=40490) |
| **5L axle** | Drivetrain shaft | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?id=540&idColor=86) |
| **6L axle** | Drivetrain shaft | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3706&idColor=60) |
| **4L axle with stop** | Shaft positioning | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?id=90241&idColor=85) |
| **Smooth pin** | Beam connection / pivot | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3673) |
| **Universal joint** | Rotation transfer between non-collinear shafts | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=62520c01) |
| **43 × 14 wheel / tyre assembly** | Wheel contact | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=65834pb02) |

> [!NOTE]
> The exact pair of external gears forming the **current 1:1 ratio** should be recorded from the installed Rev27 drivetrain.
>
> Do not label the older 36T → 24T speed-increasing pair as current.

---

# 14. Current Wiring Baseline

| Function | Current interface |
| --- | --- |
| Motor direction | GPIO5 / GPIO6 |
| Motor PWM | GPIO13 |
| Motor PWM frequency | 1 kHz |
| Steering servo | GPIO22 |
| Steering PWM frequency | 50 Hz |
| I2C SDA | GPIO2 |
| I2C SCL | GPIO3 |
| MPU6050 | I2C address `0x68` |
| ToF 1 XSHUT | GPIO16 |
| ToF 2 XSHUT | GPIO20 |
| ToF 3 XSHUT | GPIO21 |
| Encoder | Integrated C1 / C2 channels |

See:

```text
wiring-guide.md
```

for complete wiring.

---

# 15. Harness Checklist

## Power and Actuation

- [ ] Battery connector secure
- [ ] Motor wiring secured
- [ ] Main switch installed
- [ ] Raspberry Pi regulated supply connected
- [ ] Servo power and signal secure
- [ ] Motor-driver PWM and direction wiring secure
- [ ] Common grounds verified
- [ ] Heat-shrink / insulation fitted
- [ ] High-current wiring strain-relieved

## Cameras and I2C

- [ ] Camera 1 ribbon secured
- [ ] Camera 2 ribbon secured
- [ ] SDA / SCL wiring secure
- [ ] MPU6050 connection verified
- [ ] ToF 1 power / SDA / SCL / XSHUT verified
- [ ] ToF 2 power / SDA / SCL / XSHUT verified
- [ ] ToF 3 power / SDA / SCL / XSHUT verified
- [ ] GPIO16 / GPIO20 / GPIO21 labels verified
- [ ] All ToF connectors labelled physically
- [ ] Sensor orientation matches software naming

## Encoder

- [ ] Motor power wires secure
- [ ] Encoder supply correct
- [ ] Encoder ground connected
- [ ] Encoder channel 1 verified
- [ ] Encoder channel 2 verified
- [ ] Count direction verified
- [ ] Logic-level compatibility verified
- [ ] Signal wiring routed away from motor wiring where practical

---

# 16. Component Tests

Before a full run:

```text
Steering   → src/servo_test.py
Encoder    → src/encoder_test.py
ToF ×3     → src/TUF_test.py
Heading    → src/heading.py
Vision     → src/Cal_APOC.py
```

Recommended order:

```text
Mechanical inspection
        ↓
Power inspection
        ↓
Steering test
        ↓
Encoder test
        ↓
ToF test
        ↓
Heading test
        ↓
Camera calibration
        ↓
Low-speed integrated run
        ↓
Full challenge
```

---

# 17. Competition Controls

The current physical control system includes:

```text
1 × main power switch
1 × momentary Start button
```

Expected startup flow:

```text
ROBOT OFF
   ↓
Main switch ON
   ↓
Raspberry Pi boots
   ↓
Cameras initialize
   ↓
IMU initializes
   ↓
Encoder initializes
   ↓
Three ToF sensors receive separate addresses
   ↓
WAITING STATE
   ↓
Start button
   ↓
Autonomous motion
```

Always confirm the final hardware against the current official WRO Future Engineers rules and event Q&A before competition.

---

# 18. APOC Spares Pack

| Spare | Suggested qty. | Reason |
| --- | ---: | --- |
| **Current 600 RPM encoder motor** | 1 | High-impact drivetrain spare |
| **VL53L0X ToF sensor** | 2–3 | Small and easy to damage or miswire |
| **TB6612FNG motor driver** | 1–2 | Drive-stage replacement |
| **DS3225 steering servo** | 1 | Steering-critical component |
| **Camera Module 3 Wide** | 1 | Shared spare |
| **Camera ribbon cable** | 2+ | Frequent physical failure point |
| **MicroSD card with tested image/code** | 1 | Fast software recovery |
| **5 V regulator / BEC** | 1 | Power-system spare |
| **Main power switch** | 1 | Mechanical spare |
| **Start push button** | 1 | Control spare |
| **Motor / encoder harness** | 1 | Fast drivetrain replacement |
| **ToF harness / leads** | 2–3 | Fast range-sensor replacement |
| **Fasteners / bushes / axles / gears** | Assorted | Mechanical repairs |
| **Wire / solder / heat-shrink / cable ties** | Assorted | Electrical repairs |

---

# 19. Development Equipment

These items are useful during setup but are not permanent robot payload.

| Component | Purpose |
| --- | --- |
| Keyboard + mouse | Local Pi setup |
| External monitor | Bench debugging |
| Micro-HDMI cable | Raspberry Pi display |
| USB logic analyser | Encoder / I2C diagnosis |
| Digital multimeter | Voltage, continuity and signal checks |
| Bench supply | Controlled electrical testing |
| Laptop | Git, SSH, calibration and code |
| 3D printer | Sensor / camera / chassis parts |
| Vernier caliper | Dimensional checks |
| Digital scale | Final robot mass check |

---

# 20. Historical / Superseded Hardware

Historical components are retained here for traceability.

They must not be confused with the current competition configuration.

| Historical item | Status | Current replacement |
| --- | --- | --- |
| **Rhino GB37 RMCS-4091, 1000 RPM-class encoder motor** | Historical supplier / development reference | **Current 600 RPM encoder motor** |
| **325 counts/output revolution** | Worked example from historical motor specification | **Installed current encoder calibration** |
| **36T → 24T external gearing, ratio 1.5** | Historical speed-increasing drivetrain | **Current 1:1 gearing** |
| **Two VL53L0X sensors** | Earlier APOC development state | **Three VL53L0X sensors** |
| **Dual-ToF sensor fusion** | Earlier architecture | **Three-ToF architecture** |
| Camera + IMU-only parking information | Superseded | Camera + heading + three ToF + drivetrain feedback |

---

## Historical 1000 RPM Motor Reference

The older BOM used:

```text
Rhino GB37 RMCS-4091
12 V
1000 RPM class
integrated encoder
```

Historical supplier link:

[Robokits India — Rhino GB37 RMCS-4091](https://robokits.co.in/motors/rhino-gb37-12v-dc-geared-motor/dc-12v-encoder-servo-motors/rhino-gb37-12v-1000rpm-0.7kgcm-dc-geared-encoder-servo-motor)

This link is retained only so older:

- calculations;
- commits;
- photographs;
- design notes

remain understandable.

It is **not the current competition motor specification**.

---

# 21. Pre-Event Hardware Freeze Checklist

Before declaring the APOC hardware configuration frozen:

- [ ] current motor confirmed as nominal **600 RPM**
- [ ] exact motor model / SKU recorded
- [ ] exact motor purchase URL recorded
- [ ] motor mount secure
- [ ] current external gear ratio confirmed as **1:1**
- [ ] drivetrain rotates freely
- [ ] differential operates correctly
- [ ] all four driven wheels receive propulsion
- [ ] encoder direction confirmed
- [ ] current encoder counts/revolution physically calibrated
- [ ] no historical 325-count assumption used without verification
- [ ] **three** VL53L0X sensors physically installed
- [ ] ToF 1 initializes from cold boot
- [ ] ToF 2 initializes from cold boot
- [ ] ToF 3 initializes from cold boot
- [ ] GPIO16 / GPIO20 / GPIO21 XSHUT sequence works
- [ ] each ToF receives a unique address automatically
- [ ] all sensor labels match software identifiers
- [ ] both cameras initialize
- [ ] camera mounts cannot shift
- [ ] Pi supply passes full-load test
- [ ] no undervoltage warning during normal integrated operation
- [ ] steering travels without binding
- [ ] no wire can enter gears, wheels or steering linkage
- [ ] main power switch functions correctly
- [ ] Start button functions correctly
- [ ] robot boots into waiting state automatically
- [ ] spare SD card boots
- [ ] spare hardware has been tested
- [ ] `bom.md` matches the physical robot
- [ ] `wiring-guide.md` matches the physical robot
- [ ] `drivetrain.md` matches the physical robot
- [ ] engineering journal matches the physical robot
- [ ] GitHub source matches the Raspberry Pi source

---

# 22. Purchase / Verification Priority

## Already Part of the Current Architecture

1. Raspberry Pi 5, 4 GB
2. Camera Module 3 Wide ×2
3. VL53L0X ×3
4. DS3225 servo
5. TB6612FNG motor driver
6. MPU6050 module
7. 3S 11.1 V battery
8. encoder-equipped 600 RPM motor
9. main power switch
10. Start button

## Items That Must Be Explicitly Verified Before Freeze

1. **Exact manufacturer / SKU of the current 600 RPM motor**
2. **Exact current motor purchase link**
3. **Installed encoder count convention**
4. **Measured counts per gearbox-output revolution**
5. **Exact current 1:1 gear tooth-count pair**
6. **Exact high-current 5 V regulator**
7. **Exact ToF breakout revision if different from linked board**

Do not replace missing information with a specification from an older part merely because the number is conveniently available.

---

# 23. Source-Link Maintenance

When maintaining this BOM:

1. Link to the **actual component installed**.
2. Keep superseded components in the historical section.
3. Never copy a motor specification onto a different motor.
4. Never copy encoder counts from an old encoder onto the current encoder.
5. Keep current and historical gearing clearly separated.
6. Update ToF quantity everywhere if the sensor architecture changes.
7. Keep XSHUT GPIO assignments synchronized with the wiring guide and source code.
8. Update photographs after major mechanical changes.
9. Update the BOM whenever the physical robot changes.
10. Record the date of every configuration freeze.

---

# 24. Technical References

### Current project references

- `docs/hardware/drivetrain.md`
- `docs/hardware/wiring-guide.md`
- `docs/software/Software_Dependencies.md`
- `docs/testing.md`
- `docs/engineering-decisions.md`
- `docs/failure-log.md`
- `docs/development/apoc-hardware-update.md`
- `src/encoder_test.py`
- `src/TUF_test.py`
- `src/servo_test.py`
- `src/heading.py`

### Component references

- [Raspberry Pi 5](https://robu.in/product/raspberry-pi-5-model-4gb/)
- [Raspberry Pi Camera Module 3 Wide](https://robu.in/product/raspberry-pi-camera-module-3-wide/)
- [VL53L0X breakout](https://robokits.co.in/sensors/lidar-laser-rangefinders/tiny-lidar-laser-ranging-sensor-tof-based-on-vl53l0x-2-meters-range)
- [DS3225 servo](https://robu.in/product/pro-range-ds3225-25kgcm-metal-gear-digital-servo-motor-180-degree/)
- [TB6612FNG](https://robu.in/product/motor-driver-tb6612fng-module-performance-ultra-small-volume-3-pi-matching-performance-ultra-l298n/)
- [MPU6050-based 10DOF module](https://robu.in/product/mpu6050hmc5883lbmp180-10dof-3-axis-gyro-3-axis-acceleration-3-axis-magnetic-field-air-pres/)

### Historical motor reference

- [Rhino GB37 RMCS-4091 1000 RPM-class motor](https://robokits.co.in/motors/rhino-gb37-12v-dc-geared-motor/dc-12v-encoder-servo-motors/rhino-gb37-12v-1000rpm-0.7kgcm-dc-geared-encoder-servo-motor)

---

# Final Reproduction Snapshot

```text
ROBOT        : Starlight
TEAM         : Team Sentio 1747
COMPETITION  : WRO Future Engineers 2026 / APOC

COMPUTE      : Raspberry Pi 5, 4 GB
VISION       : 2 × Raspberry Pi Camera Module 3 Wide
RANGE        : 3 × VL53L0X
ORIENTATION  : MPU6050
DRIVE MOTOR  : 12 V geared encoder motor, nominal 600 RPM
ENCODER      : integrated quadrature encoder
               installed count calibration required
STEERING     : DS3225 + Ackermann
DRIVER       : TB6612FNG
BATTERY      : 3S LiPo, 11.1 V, 2200 mAh
DRIVE        : mechanical 4WD
DIFFERENTIAL : mechanical differential
GEAR STAGE   : 1:1 external ratio
TOF XSHUT    : GPIO16 / GPIO20 / GPIO21
START SYSTEM : one power switch + one Start button
STRUCTURE    : printed chassis / mounts + LEGO Technic mechanisms
```

---

## Revision Note

This revision corrects the principal configuration conflicts in the previous BOM:

```text
2 ToF          → 3 ToF
1000 RPM motor → 600 RPM motor
1.5 gearing    → 1:1 gearing
325 counts/rev → historical only, not assigned to current encoder
dual ToF       → three-sensor ToF architecture
```

The 1000 RPM motor and 36T → 24T gearing remain documented only as **historical development references**.

---

**Team Sentio 1747**  
**Starlight**  
**WRO Future Engineers 2026**  
**Robofun Lab (RFL), India**
