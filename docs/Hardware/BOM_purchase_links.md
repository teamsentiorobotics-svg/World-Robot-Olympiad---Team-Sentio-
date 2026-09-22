# Parts & Purchase Links — Team Sentio / Starlight

## APOC 2026 Competition Configuration

Complete hardware, sourcing, interface and spares reference for **Starlight**, Team Sentio's WRO Future Engineers robot.

> **Configuration status:** This document describes the upgraded **APOC 2026 competition configuration**. It replaces the earlier JGB37-520 drivetrain entry with the **Rhino GB37 12 V 1000 RPM geared encoder motor**, adds **two VL53L0X Time-of-Flight sensors**, and makes the integrated quadrature encoder part of the final sensing/control architecture.
>
> **Important:** A competition BOM is only useful if it matches the robot actually on the table. Any change to the motor, gearing, wheel diameter, camera pose, ToF mounting, steering linkage or power rail can require software and calibration changes. Freeze the mechanical/electrical configuration before the event and update this file if the physical robot changes.

### APOC upgrade summary

| Upgrade | APOC configuration | Why it matters |
|---|---|---|
| **Drive motor** | Rhino GB37 12 V 1000 RPM 0.7 kg-cm geared encoder servo motor, RMCS-4091 | Higher-speed drivetrain with integrated feedback capability |
| **Motor feedback** | Integrated quadrature encoder, 325 counts/rev at output shaft | Enables measured speed/distance, repeatability checks and closed-loop speed control |
| **Distance sensing** | 2 × VL53L0X ToF sensors | Adds direct short-range distance feedback for wall/parking/reverse manoeuvres instead of relying only on camera geometry |
| **Sensor fusion** | Cameras + dual ToF + IMU + encoder | Gives complementary field geometry, range, heading and drivetrain-motion information |
| **Competition controls** | 1 power switch + 1 start push button | Matches the 2026 Future Engineers start procedure |
| **Event reliability** | Dedicated spares pack + pre-round electrical checklist | Reduces the chance that one cable, sensor or motor ends the event for reasons too boring to deserve a trophy |

---

# 1. Final Competition Robot — Core Electronics

These are the permanent electronic components of the APOC Starlight configuration.

| Qty. | Component | Final role on Starlight | Purchase link / source |
|---:|---|---|---|
| 1 | **Raspberry Pi 5 — 4 GB** | Main computer; runs Picamera2, OpenCV, sensor fusion, challenge logic, GPIO and control software | [Robu.in](https://robu.in/product/raspberry-pi-5-model-4gb/) |
| 2 | **Raspberry Pi Camera Module 3 Wide** | Front field perception + rear parking geometry | [Robu.in](https://robu.in/product/raspberry-pi-camera-module-3-wide/) |
| 2 | **VL53L0X Time-of-Flight distance sensor breakout** | Independent short-range ranging channels for parking / wall / reverse-distance logic | [Robokits India — Tiny LiDAR VL53L0X](https://robokits.co.in/sensors/lidar-laser-rangefinders/tiny-lidar-laser-ranging-sensor-tof-based-on-vl53l0x-2-meters-range) |
| 1 | **DS3225 25 kg-cm metal-gear digital servo, 180°** | Ackermann steering actuation | [Robu.in](https://robu.in/product/pro-range-ds3225-25kgcm-metal-gear-digital-servo-motor-180-degree/) |
| 1 | **TB6612FNG motor-driver module** | Drive-motor direction and PWM speed control | [Robu.in](https://robu.in/product/motor-driver-tb6612fng-module-performance-ultra-small-volume-3-pi-matching-performance-ultra-l298n/) |
| 1 | **Rhino GB37 12 V 1000 RPM 0.7 kg-cm DC geared encoder servo motor — RMCS-4091** | Main drivetrain motor; replaces the earlier JGB37-520 | [Robokits India](https://robokits.co.in/motors/rhino-gb37-12v-dc-geared-motor/dc-12v-encoder-servo-motors/rhino-gb37-12v-1000rpm-0.7kgcm-dc-geared-encoder-servo-motor) |
| 1 | **Integrated quadrature motor encoder** | Measures motor/output-shaft motion for velocity, travelled-distance and control feedback | **Included in RMCS-4091 motor; no separate encoder purchase required** |
| 1 | **MPU6050-based 10DOF module** | Heading/orientation reference for heading-sensitive obstacle and parking manoeuvres | [Robu.in](https://robu.in/product/mpu6050hmc5883lbmp180-10dof-3-axis-gyro-3-axis-acceleration-3-axis-magnetic-field-air-pres/) |
| 1 | **MicroSD card** | Raspberry Pi OS, source code, calibration and runtime files | [Amazon.in](https://www.amazon.in/gp/product/B08L5HMJVW) |
| 1 | **Main power switch** | The single competition power-on switch | Source locally; choose a mechanically secure part with adequate current rating |
| 1 | **Momentary start push button** | Starts the run from the powered-on waiting state | Source locally; wire as the single Start button used by competition software |
| 1 | **Status / illumination LED** | Controlled visual status and/or front illumination where used | Source locally / retain current installed LED |

### Core-electronics notes

- The **Rhino RMCS-4091 already contains the encoder**. Do not add an unrelated external rotary encoder unless there is a separate measured need.
- Keep the **Micro-HDMI cable, monitor, keyboard and mouse out of the competition-payload list**. They are development tools, not permanent robot hardware.
- The **TB6612FNG is retained from the existing architecture**, but the final build should be verified under real acceleration/load conditions with the new motor. Measure current draw and confirm the driver remains within a safe operating margin before freezing the APOC configuration.

---

# 2. New Drive Motor + Encoder — RMCS-4091

The APOC drivetrain motor is now:

**Rhino GB37 12 V 1000 RPM 0.7 kg-cm DC Geared Encoder Servo Motor — Model RMCS-4091**

Purchase link:  
[Robokits India — RMCS-4091](https://robokits.co.in/motors/rhino-gb37-12v-dc-geared-motor/dc-12v-encoder-servo-motors/rhino-gb37-12v-1000rpm-0.7kgcm-dc-geared-encoder-servo-motor)

## Published motor specifications

| Parameter | Published value |
|---|---:|
| Rated voltage | **12 V** |
| Base motor speed | **5800 RPM** |
| No-load output speed | **950 RPM** |
| Rated output speed | **928 RPM** |
| Gear ratio | **1 : 6.25** |
| Rated current | **300 mA** |
| Rated power | **1.3 W** |
| Rated torque | **0.17 kg-cm** |
| Stall torque | **0.7 kg-cm** |
| Output shaft | **6 mm D-shaft** |
| Shaft length | **15 mm** |

## Integrated encoder specifications

| Parameter | Published value |
|---|---:|
| Encoder type | **Quadrature** |
| PPR | **13** |
| Quadrature CPR | **52 counts per motor-shaft revolution** |
| Counts at output shaft | **325 counts per output-shaft revolution** |
| Encoder supply | **5 V** |

### Encoder wiring from the supplier listing

| Wire | Function |
|---|---|
| Red | Motor + (M1) |
| White | Motor − (M2) |
| Yellow | Encoder channel C2 |
| Green | Encoder channel C1 |
| Blue | Encoder Vcc, 5 V |
| Black | Ground |

### APOC encoder integration requirements

- Use **both quadrature channels** if direction as well as speed/distance is required.
- Share a **clean common ground** between encoder electronics and the controller.
- The encoder is powered from **5 V**. Do **not** assume its signal outputs are automatically safe for direct Raspberry Pi GPIO. Verify the actual C1/C2 high level on the installed motor and use a suitable level-shifting / conditioning stage if required.
- Route encoder wires away from motor-power wiring where practical; brushed motor noise and long untwisted signal wires are a charming way to invent imaginary wheel motion.
- Add software sanity checks for impossible count rates, no-count conditions while commanded to move, and count direction mismatch.

### What the encoder should be used for

The encoder should supplement, not replace, vision and IMU data. Useful control quantities include:

```text
motor angular velocity
relative travelled distance
repeatable reverse distance
acceleration / deceleration consistency
stall or drivetrain-jam detection
closed-loop speed correction
```

This is particularly valuable at APOC because the robot should behave consistently as battery voltage, floor grip and mechanical load vary.

---

# 3. Dual VL53L0X Time-of-Flight Sensor System

Starlight now uses **two VL53L0X ToF sensors** as permanent competition sensors.

| Qty. | Sensor | Role | Purchase link |
|---:|---|---|---|
| 2 | **VL53L0X ToF breakout** | Direct distance measurement for close-range parking, reverse stopping and wall-relative logic | [Robokits India — Tiny LiDAR VL53L0X](https://robokits.co.in/sensors/lidar-laser-rangefinders/tiny-lidar-laser-ranging-sensor-tof-based-on-vl53l0x-2-meters-range) |

The referenced breakout is specified by the seller with an **I²C interface**, **1 mm resolution**, a stated **maximum range of 2 m**, and a **2.6–5.5 V input range** on the breakout board.

## Critical two-sensor I²C note

Two VL53L0X sensors cannot simply be powered up together at their default address and expected to behave politely. ST's multi-sensor application guidance uses each sensor's **XSHUT** input so the controller can bring the sensors online one at a time and assign unique I²C addresses.

For the final harness, provide:

- shared **SDA**;
- shared **SCL**;
- shared power and ground as appropriate for the chosen breakout;
- **one separate XSHUT GPIO per ToF sensor**;
- rigid mounts with repeatable sensor orientation;
- labelled connectors so ToF #1 and ToF #2 cannot be silently swapped during a hurried repair.

Recommended boot sequence:

```text
1. Hold both VL53L0X sensors in shutdown.
2. Enable ToF #1.
3. Assign ToF #1 a unique I2C address.
4. Enable ToF #2.
5. Assign ToF #2 a second unique I2C address.
6. Verify both sensors respond before enabling motion.
```

Reference: STMicroelectronics application note **AN4846 — Using multiple VL53L0X in a single design**:  
https://www.st.com/resource/en/application_note/an4846-using-multiple-vl53l0x-in-a-single-design-stmicroelectronics.pdf

## ToF mechanical integration

- Mount each sensor on a **rigid, non-flexing bracket**.
- Keep the optical window unobstructed by chassis edges, wires or printed overhangs.
- Record the sensor's pose relative to the chassis so the same mount can be reproduced after repairs.
- Do not treat the advertised 2 m maximum as the control distance to use blindly. Final thresholds should be established on the actual APOC field materials, lighting and mounting geometry.

---

# 4. Sensor-Fusion Architecture

The upgraded robot is no longer just “camera + gyro + PWM.” The final architecture is:

```text
CAMERAS  = FIELD GEOMETRY + COLOUR / OBJECT PERCEPTION
TOF x2   = DIRECT SHORT-RANGE DISTANCE
IMU      = ORIENTATION / HEADING REFERENCE
ENCODER  = DRIVETRAIN MOTION / SPEED / RELATIVE DISTANCE
PI       = STATE FUSION + CHALLENGE LOGIC + CONTROL
DRIVER   = MOTOR DIRECTION + PWM
SERVO    = ACKERMANN STEERING ACTUATION
```

### Sensor roles

| Sensor | Best use on Starlight | Do not rely on it alone for |
|---|---|---|
| Front camera | Walls, direction lines, red/green pillars, magenta parking cues and scene geometry | Exact short-range distance |
| Rear camera | Reverse parking geometry and alignment | Encoder-level travelled distance |
| VL53L0X #1 | Direct range measurement for a selected parking/wall reference | Global track interpretation |
| VL53L0X #2 | Independent second range measurement, including reverse-distance logic | Heading estimation |
| MPU6050 | Heading change and orientation reference | Absolute position on the field |
| Motor encoder | Speed, relative motion and repeatability | Obstacle identity / lane geometry |

The point is **complementarity**. If every sensor is being asked to solve the same problem, the robot has redundancy. If each sensor covers a weakness of the others, it has sensor fusion.

---

# 5. Power System

Starlight separates the high-load motor/battery side from regulated low-voltage electronics rails.

| Qty. | Component | Purpose | Purchase link / status |
|---:|---|---|---|
| 1 | **3S LiPo battery — 11.1 V, 2200 mAh** | Main robot energy source | [Amazon.in](https://www.amazon.in/PRAYOG-INDIA-ROBOTICS-Rechargeable-Connector/dp/B0H9L6B694) |
| 1 | **LiPo balance charger** | Correct charging and cell balancing for the 3S pack | [Amazon.in](https://www.amazon.in/Pro3D-B6-AC-Battery-Balance-Charger/dp/B0CV9H28MQ) |
| 1 | **Higher-current regulated 5 V Raspberry Pi rail, approximately 5 A** | Main regulated Pi supply; retained after earlier undervoltage issues | **Exact final purchase link still to be recorded** |
| 1 | **5 V / 3 A buck converter / BEC** | Auxiliary regulated rail where required | [Robu.in](https://robu.in/product/ultra-small-size-dc-dc-5v-3a-bec-power-supply-buck-step-down-module/) |
| 1 | **Main power switch** | Single switch used to power on the vehicle | Source locally; current-rated |
| — | **Power-distribution wiring / perfboard / terminals** | Clean distribution to Pi, servo, sensors and motor system | Source locally |
| — | **XT-style battery connector pair** | Secure battery connection | Match the installed battery |
| — | **Heat-shrink / insulation / strain relief** | Electrical protection and serviceability | Source locally |

## Power-system requirements for the upgraded sensor stack

- Keep **motor current paths physically and electrically tidy** to reduce noise coupled into the encoder and I²C sensors.
- Avoid powering the Pi through a marginal regulator. A robot that can see the entire track but reboots in a corner is merely an expensive spectator.
- Verify 5 V rail stability with **both cameras active, both ToFs ranging, the servo moving and the drivetrain accelerating**.
- Confirm every ground reference is deliberate. Encoder, ToF and control-signal grounds must not be accidental through some heroic jumper wire.
- Provide strain relief on the battery, motor and regulator connections.

### LiPo handling

- charge with a compatible balance charger;
- select the correct cell count;
- never leave charging unattended;
- verify polarity before connecting electronics;
- inspect the pack for swelling or damage before use;
- provide a fast, accessible way to isolate power.

---

# 6. Competition Controls & 2026 APOC Rule-Critical Hardware

For an international WRO Open Championship, the **international 2026 Future Engineers rules** apply unless an official event clarification says otherwise.

Official rules:  
https://wro-association.org/wp-content/uploads/WRO-2026-Future-Engineers-Self-Driving-Cars-General-Rules.pdf

Relevant hardware constraints for the BOM/build review include:

| Requirement | Starlight BOM implication |
|---|---|
| Vehicle maximum size: **300 × 200 mm**, height **300 mm** | Check the final robot with camera and ToF mounts installed |
| Vehicle maximum mass: **1.5 kg** | Weigh the complete competition robot with battery |
| Four-wheeled vehicle with steering; no differential-wheeled base | Retain Ackermann steering and mechanically linked drivetrain |
| Sensors are unrestricted in brand/function/number | Dual VL53L0X sensors are permitted |
| DC motors / servos are unrestricted in brand | Rhino GB37 motor is permitted, subject to the rest of the vehicle rules |
| Drive wheels must remain physically linked; no independent one-motor-per-side electronic differential | Retain the mechanical drivetrain/differential architecture |
| Only wired communication between electromechanical components | Disable wireless communication during rounds |
| **Only one switch** to switch the vehicle on | Use the single main power switch listed in this BOM |
| Powered robot must wait for **one Start button** | Use the dedicated momentary Start push button |
| Bring enough spare parts | Maintain the APOC spares pack below |
| Only one competition vehicle is allowed in the competition area | Bring spare **components**, not a second assembled car |

### Start-system state

The intended competition flow is:

```text
ROBOT OFF
   ↓
main power switch ON
   ↓
boot + initialise sensors
   ↓
WAITING STATE
   ↓
judge says GO
   ↓
press the single Start button
   ↓
autonomous motion begins
```

The dual-ToF address assignment and encoder initialisation should therefore happen automatically during startup, before the robot reaches its waiting state.

---

# 7. Structural and Manufacturing Materials

A large part of Starlight is custom-built rather than purchased as one chassis kit.

| Item | Purpose / note |
|---|---|
| **PLA / final chosen print material** | Main chassis, electronics enclosure, camera and sensor mounts |
| **3D-printed front camera mount** | Holds the front Camera Module 3 at the calibrated field-view angle |
| **3D-printed rear camera mount** | Supports rear parking camera geometry |
| **2 × rigid VL53L0X mounts** | Fixes ToF sensor position and beam direction reproducibly |
| **Rhino GB37 motor mount / bracket** | Secures the 37 mm gearbox without allowing torque-induced movement |
| **6 mm D-shaft compatible coupling / hub interface** | Couples the new motor output to the retained drivetrain |
| **3D-printed electronics / chassis parts** | Packages Raspberry Pi, wiring and drivetrain around the mechanical frame |
| **Fasteners** | Screws, nuts, washers and spacers used to secure printed and electronic parts |
| **Perfboard / prototyping board** | Custom electronics / power-distribution mounting where used |
| **Hook-up wire / jumper wire / ribbon cable** | Signal and power distribution |
| **Cable ties / heat-shrink / insulation** | Cable management and electrical protection |

See [`3D_PRINTING_SETTINGS.md`](3D_PRINTING_SETTINGS.md) for the retained print profile.

> **APOC mechanical rule:** After adding the new 37 mm motor body, encoder wiring and dual ToF mounts, re-check the complete robot against the 300 × 200 × 300 mm and 1.5 kg limits.

---

# 8. LEGO Technic — Differential, Gearing and Drivetrain

LEGO Technic elements are used for the mechanical differential, external gearing, shafts, supports and parts of the 4WD transmission.

| Component | Main use | BrickLink |
|---|---|---|
| **2 × 4 L Beam** | Compact structural / drivetrain support | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=32140) |
| **Half bush** | Axle spacing and retention | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=4265c&idColor=3) |
| **Bush** | Axle retention and spacing | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3713) |
| **2L axle connector** | Joins axle sections | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=6538c) |
| **28-tooth differential** | Allows left/right driven outputs to rotate at different speeds in a turn | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=73071) |
| **24-tooth gear** | External transmission / drivetrain gearing | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3648) |
| **20-tooth gear** | Intermediate drivetrain gearing where required | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=32269) |
| **12-tooth bevel gear** | Changes transmission direction / meshes in compact drivetrain geometry | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=6589) |
| **9-unit beam** | Chassis and drivetrain structural support | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=40490) |
| **5L axle** | Drivetrain shaft | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?id=540&idColor=86) |
| **6L axle** | Drivetrain shaft | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3706&idColor=60) |
| **4L axle with stop** | Retained shaft / wheel or gear positioning | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?id=90241&idColor=85) |
| **Smooth pin** | Beam connection / pivot support | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3673) |
| **Universal joint** | Transfers rotation between shafts that are not perfectly collinear | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=62520c01) |
| **LEGO Technic wheel 43 × 14 with medium-azure tyre** | Wheel / tyre assembly | [BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=65834pb02) |
| **36-tooth driving gear** | Retained external speed stage | **Exact retained BrickLink catalogue entry still to be added** |

---

# 9. Starlight Drivetrain Summary

The APOC drivetrain remains a **four-wheel-drive mechanical system** using a differential and external LEGO gearing, now driven by the encoder-equipped Rhino GB37.

```text
Driven wheels : 4
Drive type    : mechanical 4WD
Drive motor   : Rhino GB37 RMCS-4091, 12 V, encoder-equipped
Differential  : LEGO Technic 28T differential
Gear stage    : 36T driving gear → 24T driven gear
Feedback      : integrated quadrature encoder
```

## Retained 36T → 24T speed stage

The external speed stage is retained as:

\[
\frac{36}{24}=1.5
\]

So the driven shaft rotates faster than the motor-side gear, with a corresponding ideal torque reduction before losses.

Because the **new motor itself is already a high-speed 1000 RPM-class unit**, do not assume the previous PWM values, braking distances or corner-entry speeds remain appropriate. Recalibrate speed control and validate drivetrain load after the motor swap.

For a beginner explanation of the differential and how to reproduce it, see:

[`Mechanical_Differential_Starlight_Style_Guide.md`](Mechanical_Differential_Starlight_Style_Guide.md)

---

# 10. Mechanical Differential — Why It Is There

During a turn, the outside wheels travel farther than the inside wheels.

```text
outside wheel speed > inside wheel speed
```

If left and right wheels were rigidly forced to rotate at exactly the same speed, the tyres would scrub or slide.

The mechanical differential allows the left and right drivetrain outputs to rotate at different speeds while remaining powered by the same drive system.

This complements Ackermann steering:

```text
ACKERMANN    → gives inside/outside wheels different steering angles
DIFFERENTIAL → allows inside/outside sides to rotate at different speeds
ENCODER      → measures the motion of the common drive source
```

---

# 11. Final Steering Hardware

| Item | Final role |
|---|---|
| **DS3225 servo** | Steering actuator |
| **Ackermann linkage** | Converts servo motion into different inner/outer steering angles |
| **LEGO / printed mechanical links** | Steering transmission and wheel support |

Current software calibration:

```text
LEFT   = 35
CENTER = 75
RIGHT  = 105
```

These are **servo command values**, not measured road-wheel steering angles. After any chassis or linkage change, re-check physical end stops before full-speed testing.

---

# 12. Final Camera Arrangement

Starlight uses two Raspberry Pi Camera Module 3 Wide units.

## Front camera

Used for:

- black-wall geometry;
- blue/orange direction markers;
- red/green obstacle pillars;
- magenta parking/course cues;
- challenge-state perception.

## Rear camera

Used primarily for:

- rear parking-slot geometry;
- reverse parking alignment.

Camera mounts are part of the calibrated sensing system. Rebuilding the software without reproducing approximately the same camera pose may require threshold and target recalibration.

The new ToF sensors are **additional range sensors**, not substitutes for the front/rear camera geometry.

---

# 13. Wiring / Harness Checklist — APOC Version

A competition build should have a labelled, serviceable harness rather than a small rainforest of jumper wires.

## Power and actuation

- [ ] appropriate-gauge battery wire;
- [ ] appropriate-gauge motor wire;
- [ ] secure battery connector pair;
- [ ] single main power switch;
- [ ] 5 V Pi rail wiring;
- [ ] servo power and signal wiring;
- [ ] motor-driver PWM/direction wiring;
- [ ] heat-shrink and strain relief.

## Cameras and I²C

- [ ] front camera ribbon cable of correct length;
- [ ] rear camera ribbon cable of correct length;
- [ ] SDA/SCL bus wiring;
- [ ] MPU6050 I²C wiring;
- [ ] ToF #1 power, SDA, SCL and XSHUT;
- [ ] ToF #2 power, SDA, SCL and XSHUT;
- [ ] labelled ToF connectors;
- [ ] common-ground verification.

## Encoder

- [ ] motor M1/M2 wires;
- [ ] encoder 5 V supply;
- [ ] encoder ground;
- [ ] encoder C1 signal;
- [ ] encoder C2 signal;
- [ ] verified logic-level compatibility / level shifting if required;
- [ ] physical separation from noisy motor wiring where practical.

## Competition control

- [ ] single Start push button;
- [ ] status LED if retained;
- [ ] Start button debounced in software/hardware;
- [ ] robot boots into waiting state automatically;
- [ ] wireless functions disabled for competition rounds.

## Mechanical / service

- [ ] fasteners;
- [ ] spacers / standoffs;
- [ ] perfboard or equivalent custom electronics mounting;
- [ ] cable ties;
- [ ] removable connectors on parts likely to be replaced at the event;
- [ ] no wire can enter gears, steering linkage or wheels at full steering lock.

---

# 14. APOC Spares Pack

The 2026 WRO Future Engineers rules explicitly tell teams to bring enough spare parts. Do that. International competitions are a terrible place to discover that a ₹119 sensor has become the most important object in Hyderabad.

Recommended spares:

| Spare | Suggested qty. | Reason |
|---|---:|---|
| **Rhino GB37 RMCS-4091 motor** | 1 | Highest-impact drivetrain replacement |
| **VL53L0X ToF sensor** | 2 | Small, inexpensive, easy to damage or miswire |
| **TB6612FNG motor driver** | 1–2 | Quick swap if the drive stage fails |
| **DS3225 steering servo** | 1 | Steering is mission-critical |
| **Camera Module 3 Wide** | 1 | Shared spare for front/rear camera failure |
| **Camera ribbon cables** | 2+ | Cables fail far more often than anyone wants to admit |
| **MicroSD card with tested image/code** | 1 | Fast recovery from filesystem/card failure |
| **5 V regulator / BEC** | 1 | Power faults can mimic software faults |
| **Main power switch** | 1 | Mechanical wear / impact spare |
| **Start push button** | 1 | Required control component |
| **Motor/encoder connector harness** | 1 | Avoid re-soldering under time pressure |
| **ToF harness / JST leads** | 2 | Allows immediate sensor replacement |
| **Fasteners, bushes, axles, gears** | Assorted | Mechanical repairs |
| **Heat-shrink, wire, solder, cable ties** | Assorted | Field repair consumables |

> Bring spare **components**, not a second competition vehicle. The 2026 rules allow only one vehicle in the competition area.

---

# 15. Development / Setup Equipment — Not Competition Payload

These are useful for reproduction and debugging but are not permanent competition hardware.

| Component | Link / source | Note |
|---|---|---|
| Keyboard + mouse | [Amazon.in](https://www.amazon.in/gp/product/B0BHYJ8CVF) | Direct Raspberry Pi access during setup |
| Monitor / HDMI display | Any compatible display | Bench setup and debugging |
| Micro-HDMI to HDMI cable | [Robu.in](https://robu.in/product/micro-hdmi-male-to-standard-hdmi-male-cable-for-raspberry-pi-4/) | Development access only |
| 0.96" I²C OLED display | [Robu.in](https://robu.in/product/0-96-inch-i2c-iic-oled-lcd-module-4pin-with-vcc-gnd-white/) | Earlier-revision / development item; not required on final Starlight |
| USB logic analyser | Any suitable model | Useful for debugging encoder and I²C timing |
| Bench power supply | Any suitable regulated supply | Controlled power testing before battery operation |

The final robot does **not** depend on the OLED, external monitor, keyboard or mouse.

---

# 16. Retired / Superseded Competition Hardware

Keep superseded hardware documented so old code, photos and repository commits still make sense.

| Component | Status | Replaced by |
|---|---|---|
| **JGB37-520 brushed DC geared motor, 12 V** | **Superseded for APOC 2026** | Rhino GB37 RMCS-4091 12 V 1000 RPM encoder motor |
| No drivetrain feedback sensor | **Superseded** | Integrated quadrature encoder on RMCS-4091 |
| Camera + IMU-only ranging architecture | **Superseded** | Camera + IMU + dual VL53L0X + encoder fusion |

Do not silently delete older parts from the engineering history. Mark them as superseded so judges can follow the actual design evolution.

---

# 17. Recommended Tools

| Tool | Why it is useful |
|---|---|
| Digital multimeter | Polarity, continuity, rail voltage and encoder-signal checks |
| Soldering iron | Secure power and signal connections |
| Wire stripper / cutter | Clean harness work |
| Hex drivers / screwdrivers | Mechanical assembly |
| Vernier caliper | Chassis, shaft, mount and clearance measurements |
| 3D printer | Custom chassis, ToF mounts and camera mounts |
| Laptop | SSH, Git, Python editing, calibration and video analysis |
| USB logic analyser | Diagnose encoder and I²C issues |
| External monitor + keyboard/mouse | Initial Pi setup and recovery |
| LiPo-safe charging area / bag | Battery handling |
| Small digital scale | Verify the complete robot remains under 1.5 kg |

---

# 18. APOC Pre-Event Hardware Freeze Checklist

Before declaring this BOM final:

- [ ] new Rhino motor physically installed and locked against rotation in its mount;
- [ ] 6 mm D-shaft coupling/drivetrain interface verified under full load;
- [ ] motor direction confirmed in software;
- [ ] encoder C1/C2 direction confirmed;
- [ ] encoder counts verified against a known output-shaft rotation;
- [ ] both VL53L0X sensors boot every time from cold power-on;
- [ ] each ToF receives a unique address automatically;
- [ ] ToF #1/#2 labels match software identifiers;
- [ ] camera cables secured and strain-relieved;
- [ ] full-load Pi power test passes without undervoltage warnings;
- [ ] steering reaches full intended range without binding;
- [ ] no wire can touch gears or tyres;
- [ ] robot fits inside **300 × 200 × 300 mm**;
- [ ] complete robot mass is **≤ 1.5 kg**;
- [ ] wireless communication is disabled for competition mode;
- [ ] one main power switch only;
- [ ] one Start button only;
- [ ] power-on leads to waiting state without manual calibration/input;
- [ ] spare SD card boots correctly;
- [ ] spare motor / sensor / driver parts have been electrically tested before packing;
- [ ] BOM, wiring diagram, GitHub README and actual robot agree with one another.

---

# 19. Suggested Purchase Order for the APOC Build

## Stage 1 — Immediate drivetrain + sensing upgrade

1. **Rhino GB37 RMCS-4091 12 V 1000 RPM encoder motor**
2. **VL53L0X ToF sensor ×2**
3. motor mounting hardware / 6 mm D-shaft coupling solution
4. encoder connector / wire / any required signal-conditioning parts
5. ToF connectors and XSHUT wiring

## Stage 2 — Verify retained competition electronics

6. Raspberry Pi 5, 4 GB
7. Camera Module 3 Wide ×2
8. DS3225 steering servo
9. TB6612FNG motor driver
10. MPU6050 module
11. MicroSD card
12. main power switch
13. Start push button

## Stage 3 — Power

14. 3S 11.1 V 2200 mAh LiPo
15. compatible balance charger
16. final high-current 5 V Raspberry Pi regulator
17. auxiliary 5 V regulator if required
18. connectors, wire, insulation and strain relief

## Stage 4 — Mechanics

19. print material
20. fasteners and spacers
21. dual ToF mounts
22. LEGO differential
23. gears including retained 36T → 24T stage
24. axles
25. bushes / connectors
26. universal joint
27. beams
28. wheels / tyres

## Stage 5 — Spares

29. spare Rhino motor
30. spare ToF sensors
31. spare motor driver
32. spare servo
33. spare camera / ribbon cables
34. spare regulator
35. spare imaged MicroSD
36. spare switches / connectors / mechanical consumables

---

# 20. Source-Link Maintenance

When updating the repository:

1. Keep links to the **actual parts used**, not merely similar products.
2. If a listing disappears, retain the original part name/model and add a replacement supplier separately.
3. Do not silently substitute motors, cameras, ToF sensors, regulators or steering servos; these can change calibration and control behaviour.
4. Record the exact final **5 V high-current Pi regulator** source.
5. Add the exact BrickLink entry for the retained **36T driving gear**.
6. If the motor driver changes after current testing, update both the BOM and the control/wiring documentation.
7. Record the exact ToF breakout revision actually mounted if it differs from the linked Robokits board.
8. Update photographs after the motor/ToF upgrade so the repository does not describe a robot that no longer exists.
9. Re-check the official 2026 WRO Future Engineers Q&A before APOC; official Q&A can clarify or override points in the base rules.
10. Update the date below whenever sourcing or final hardware changes.

---

# 21. Technical Sources for the APOC Upgrade

- **Rhino GB37 RMCS-4091 product page:**  
  https://robokits.co.in/motors/rhino-gb37-12v-dc-geared-motor/dc-12v-encoder-servo-motors/rhino-gb37-12v-1000rpm-0.7kgcm-dc-geared-encoder-servo-motor
- **VL53L0X breakout used as sourcing reference:**  
  https://robokits.co.in/sensors/lidar-laser-rangefinders/tiny-lidar-laser-ranging-sensor-tof-based-on-vl53l0x-2-meters-range
- **STMicroelectronics AN4846, multiple VL53L0X sensors:**  
  https://www.st.com/resource/en/application_note/an4846-using-multiple-vl53l0x-in-a-single-design-stmicroelectronics.pdf
- **WRO 2026 Future Engineers General & Game Rules:**  
  https://wro-association.org/wp-content/uploads/WRO-2026-Future-Engineers-Self-Driving-Cars-General-Rules.pdf
- **WRO 2026 Questions & Answers:**  
  https://wro-association.org/competition/questions-answers/

---

# Final Reproduction Snapshot — APOC 2026

```text
ROBOT        : Starlight
TEAM         : Team Sentio
COMPETITION  : WRO Future Engineers — APOC 2026

COMPUTE      : Raspberry Pi 5, 4 GB
VISION       : 2 × Raspberry Pi Camera Module 3 Wide
RANGE        : 2 × VL53L0X Time-of-Flight sensors
ORIENTATION  : MPU6050 gyro / IMU module
DRIVE MOTOR  : Rhino GB37 RMCS-4091, 12 V, 1000 RPM class
ENCODER      : integrated quadrature encoder, 325 counts/output-shaft rev
STEERING     : DS3225 servo + Ackermann geometry
DRIVER       : TB6612FNG, pending final current-margin validation with new motor
BATTERY      : 3S LiPo, 11.1 V, 2200 mAh
DRIVE        : mechanical 4WD
DIFFERENTIAL : LEGO Technic 28T differential
GEAR STAGE   : 36T driving → 24T driven
START SYSTEM : one power switch + one Start push button
CHASSIS      : custom 3D-printed + LEGO Technic drivetrain components
```

---

### Last updated

**19 September 2026 — Team Sentio / Starlight — APOC hardware update**
