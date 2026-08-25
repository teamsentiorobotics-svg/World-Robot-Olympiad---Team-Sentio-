# Parts & Purchase Links — Team Sentio / Starlight

Complete hardware and sourcing reference for reproducing **Starlight**, Team Sentio's WRO Future Engineers robot.

> **Important:** This list separates parts used on the **final competition robot** from items that were used only during development or earlier revisions.  
> Prices, stock and product listings can change. The links below are the links used by the team or the closest retained sourcing reference as of the repository's latest update.

---

## 1. Final Competition Robot — Core Electronics

These are the main electronic components required to reproduce the final Starlight architecture.

| Qty. | Component | Purpose on Starlight | Purchase link |
|---:|---|---|---|
| 1 | **Raspberry Pi 5 — 4 GB** | Main computer; runs Picamera2, OpenCV, challenge logic, GPIO and control software | [Robu.in](https://robu.in/product/raspberry-pi-5-model-4gb/) |
| 2 | **Raspberry Pi Camera Module 3 Wide** | Front field perception + rear parking geometry | [Robu.in](https://robu.in/product/raspberry-pi-camera-module-3-wide/) |
| 1 | **DS3225 25 kg-cm metal-gear digital servo, 180°** | Ackermann steering actuation | [Robu.in](https://robu.in/product/pro-range-ds3225-25kgcm-metal-gear-digital-servo-motor-180-degree/) |
| 1 | **TB6612FNG motor-driver module** | Controls drive-motor direction and PWM speed | [Robu.in](https://robu.in/product/motor-driver-tb6612fng-module-performance-ultra-small-volume-3-pi-matching-performance-ultra-l298n/) |
| 1 | **JGB37-520 brushed DC geared motor, 12 V** | Main drivetrain motor | [Robu.in](https://robu.in/product/jgb37-520-dc12v-miniature-forward-and-reverse-brushed-dc-speed-reducer-motor/) |
| 1 | **MPU6050-based 10DOF module** | Gyroscope heading reference for heading-sensitive obstacle / parking manoeuvres | [Robu.in](https://robu.in/product/mpu6050hmc5883lbmp180-10dof-3-axis-gyro-3-axis-acceleration-3-axis-magnetic-field-air-pres/) |
| 1 | **MicroSD card** | Raspberry Pi OS, source code and local runtime files | [Amazon.in](https://www.amazon.in/gp/product/B08L5HMJVW) |
| 1 | **Micro-HDMI to HDMI cable** | Development / setup access to the Raspberry Pi | [Robu.in](https://robu.in/product/micro-hdmi-male-to-standard-hdmi-male-cable-for-raspberry-pi-4/) |

---

## 2. Power System

Starlight separates the high-load battery/motor side from the regulated low-voltage electronics supply.

| Qty. | Component | Purpose | Purchase link / status |
|---:|---|---|---|
| 1 | **3S LiPo battery — 11.1 V, 2200 mAh** | Main robot energy source | [Amazon.in](https://www.amazon.in/PRAYOG-INDIA-ROBOTICS-Rechargeable-Connector/dp/B0H9L6B694) |
| 1 | **LiPo balance charger** | Correct charging and cell balancing for the 3S pack | [Amazon.in](https://www.amazon.in/Pro3D-B6-AC-Battery-Balance-Charger/dp/B0CV9H28MQ) |
| 1 | **5 V / 3 A buck converter / BEC** | Regulated low-voltage auxiliary rail; useful for servo / logic loads during development | [Robu.in](https://robu.in/product/ultra-small-size-dc-dc-5v-3a-bec-power-supply-buck-step-down-module/) |
| 1 | **Higher-current 5 V Raspberry Pi rail, approximately 5 A** | Final Raspberry Pi supply architecture after earlier 5 V / 3 A undervoltage issues | **Exact purchase link not yet retained — add final sourced part here** |
| 1 | **Main power switch** | Physical power isolation / safe shutdown of robot power | Source locally / match current rating to the robot |
| — | **Power wiring, connectors and heat-shrink** | Battery, converter, motor and electronics connections | Source locally |
| — | **XT-style battery connectors / matching mating connectors** | Secure high-current battery connection | Source locally; match the battery actually used |

### Power-system note

Do **not** reproduce the earlier power architecture blindly. During development, a lower-current 5 V supply produced Raspberry Pi undervoltage warnings. The final build moved to a **higher-current 5 V rail** for the Pi.

Also observe normal LiPo safety practice:

- charge with a compatible balance charger;
- select the correct cell count;
- never leave charging unattended;
- verify polarity before connecting electronics;
- inspect a pack for swelling or damage before use;
- provide a fast way to isolate power.

---

## 3. Sensors and Field Perception

| Qty. | Component | Used for |
|---:|---|---|
| 1 | Front Camera Module 3 Wide | Walls, coloured direction markers, red/green pillars, parking cues and general field geometry |
| 1 | Rear Camera Module 3 Wide | Rear parking geometry during reverse / parking manoeuvres |
| 1 | MPU6050 gyro module | Orientation / heading during selected obstacle and parking phases |
| 1 | Front illumination LED | Controlled low-light illumination to improve visual stability in darker conditions |

### Architecture in one line

```text
VISION = FIELD GEOMETRY
IMU    = ORIENTATION
PI     = FUSION + CONTROL
PWM    = ACTUATION
```

The cameras tell the Raspberry Pi **where things appear to be**.  
The IMU gives an additional **orientation reference**.  
The Raspberry Pi combines state, perception and control logic.  
The motor driver and servo convert those decisions into physical motion.

---

## 4. Items Used During Development — Not Required on the Final Robot

These may still be useful when reproducing or debugging Starlight, but they are **not required as permanent competition hardware**.

| Component | Link | Note |
|---|---|---|
| Keyboard + mouse | [Amazon.in](https://www.amazon.in/gp/product/B0BHYJ8CVF) | Used for direct Raspberry Pi access during development |
| Monitor / HDMI display | Any compatible display | Useful during setup and debugging; not carried on the competition robot |
| Micro-HDMI cable | [Robu.in](https://robu.in/product/micro-hdmi-male-to-standard-hdmi-male-cable-for-raspberry-pi-4/) | Used with an external monitor |
| 0.96" I2C OLED display | [Robu.in](https://robu.in/product/0-96-inch-i2c-iic-oled-lcd-module-4pin-with-vcc-gnd-white/) | **Development / earlier-revision item; not part of the final Starlight architecture** |

> The final robot does **not** depend on an OLED display or programmable RGB status lighting.

---

# 5. Structural and Manufacturing Materials

A large part of Starlight is custom-built rather than purchased as one chassis kit.

| Item | Purpose / note |
|---|---|
| **PLA filament** | Main 3D-printed chassis, electronics enclosure, camera supports and custom mechanical parts |
| **3D-printed front camera mount** | Holds the final front Camera Module 3 at the calibrated field-view angle |
| **3D-printed rear camera mount** | Supports rear parking camera geometry |
| **3D-printed electronics / chassis parts** | Packages Raspberry Pi, wiring and drivetrain around the mechanical frame |
| **Fasteners** | Screws, nuts, washers and spacers used to secure printed and electronic parts |
| **Perfboard / prototyping board** | Custom electronics / power-distribution mounting where used |
| **Hook-up wire / jumper wire / ribbon cable** | Signal and power distribution |
| **Cable ties / heat-shrink / insulation** | Cable management and electrical protection |

See [`3D_PRINTING_SETTINGS.md`](3D_PRINTING_SETTINGS.md) for the team's retained print profile.

---

# 6. LEGO Technic — Differential, Gearing and Drivetrain

LEGO Technic elements are used for the mechanical differential, external gearing, shafts, supports and parts of the 4WD transmission.

Links below point to BrickLink catalogue entries.

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

---

# 7. Starlight Drivetrain Summary

The final drivetrain is a **four-wheel-drive mechanical system** using a differential and external LEGO gearing.

Key retained configuration:

```text
Driven wheels : 4
Drive type    : mechanical 4WD
Differential  : LEGO Technic 28T differential
Gear stage    : 36T driving gear → 24T driven gear
```

## 36T → 24T speed stage

The retained external gear ratio is:

\[
\frac{36}{24}=1.5
\]

So, ideally:

```text
driven-shaft speed = input-shaft speed × 1.5
```

The trade-off is that increasing speed reduces available torque by the inverse ratio before mechanical losses.

> The **36T driving gear** used in the robot should also be included in the final BrickLink sourcing list once the exact retained LEGO part number / catalogue link is confirmed.

For a beginner explanation of the differential and how to reproduce it, see:

[`Mechanical_Differential_Starlight_Style_Guide.md`](Mechanical_Differential_Starlight_Style_Guide.md)

---

# 8. Mechanical Differential — Why It Is There

During a turn, the outside wheels travel farther than the inside wheels.

Therefore:

```text
outside wheel speed > inside wheel speed
```

If left and right wheels were rigidly forced to rotate at exactly the same speed, the tyres would scrub or slide.

The mechanical differential allows the left and right drivetrain outputs to rotate at different speeds while remaining powered by the same drive system.

This complements Ackermann steering:

```text
ACKERMANN    → gives inside/outside wheels different steering angles
DIFFERENTIAL → allows inside/outside sides to rotate at different speeds
```

---

# 9. Final Steering Hardware

| Item | Final role |
|---|---|
| DS3225 servo | Steering actuator |
| Ackermann linkage | Converts servo motion into different inner/outer steering angles |
| LEGO / printed mechanical links | Steering transmission and wheel support |

Final software calibration currently uses:

```text
LEFT   = 35
CENTER = 75
RIGHT  = 105
```

These are **servo command values**, not measured road-wheel steering angles.

---

# 10. Final Camera Arrangement

Starlight uses two Raspberry Pi Camera Module 3 Wide units.

## Front camera

Used for:

- black-wall geometry;
- blue/orange direction markers;
- red/green obstacle pillars;
- magenta parking / course cues;
- challenge-state perception.

## Rear camera

Used primarily for:

- rear parking-slot geometry;
- reverse parking alignment.

Camera mounts should be treated as part of the calibrated sensing system. Rebuilding the software without reproducing approximately the same camera pose may require threshold / target recalibration.

---

# 11. Wiring / Small Parts Checklist

The major electronics above are not enough by themselves. A practical reproduction will also need:

- [ ] appropriate-gauge motor/battery wire;
- [ ] lower-current signal wire;
- [ ] GPIO jumper wires or custom harness;
- [ ] camera ribbon cables of suitable length;
- [ ] I2C wiring for the IMU;
- [ ] battery connector pair;
- [ ] main power switch;
- [ ] heat-shrink tubing;
- [ ] cable ties;
- [ ] electrical insulation;
- [ ] fasteners;
- [ ] spacers / standoffs;
- [ ] perfboard or equivalent custom electronics mounting;
- [ ] solder;
- [ ] suitable soldering equipment;
- [ ] multimeter for polarity / voltage checks.

---

# 12. Recommended Tools

These are not robot components, but they make reproduction much easier.

| Tool | Why it is useful |
|---|---|
| Digital multimeter | Check polarity, continuity and regulator output before connecting the Pi |
| Soldering iron | Build secure power and signal connections |
| Wire stripper / cutter | Prepare harnesses cleanly |
| Hex drivers / screwdrivers | Mechanical assembly |
| Vernier caliper | Check printed dimensions, shaft spacing and clearances |
| 3D printer | Produce the custom chassis and mounts |
| Laptop | SSH, Git, Python editing, calibration and video analysis |
| External monitor + keyboard/mouse | Useful during initial Raspberry Pi setup |
| LiPo-safe charging area / bag | Safer battery handling |

---

# 13. What Is *Not* a Final-Robot Requirement

To avoid confusion when reading earlier development material:

- **No OLED display is required on the final robot.**
- **No programmable RGB LED system is required.**
- A keyboard, mouse and external display are **development tools**, not competition payload.
- Earlier motor, power and chassis revisions should not be assumed to match the final Starlight configuration.

---

# 14. Suggested Purchase Order for a New Builder

If starting from nothing, buy in this order.

## Stage 1 — Compute and perception

1. Raspberry Pi 5, 4 GB
2. MicroSD card
3. Camera Module 3 Wide ×2
4. Micro-HDMI cable
5. keyboard/mouse if required for setup

## Stage 2 — Motion

6. JGB37-520 12 V drive motor
7. TB6612FNG motor driver
8. DS3225 steering servo
9. MPU6050 module

## Stage 3 — Power

10. 3S 11.1 V 2200 mAh LiPo
11. compatible balance charger
12. final high-current 5 V Raspberry Pi regulator
13. auxiliary regulator if required
14. switch, connectors, wire and protection materials

## Stage 4 — Mechanics

15. PLA filament
16. fasteners and spacers
17. LEGO differential
18. gears
19. axles
20. bushes / connectors
21. universal joint
22. beams
23. wheels / tyres

## Stage 5 — Build and test

24. print the chassis;
25. assemble drivetrain by hand first;
26. verify differential motion;
27. install steering;
28. install power wiring;
29. check polarity and regulator output;
30. connect the Raspberry Pi only after electrical checks;
31. install cameras in their final rigid positions;
32. recalibrate vision and steering;
33. test at low speed;
34. move to full challenge testing.

---

# 15. Source-Link Maintenance

When updating this repository:

1. Keep links to the **actual parts used**, not merely similar products.
2. If a listing disappears, retain the original part name and add a replacement supplier separately.
3. Do not silently substitute motors, cameras, regulators or steering servos — these can change calibration.
4. Add the exact source link for the final **5 V / high-current Pi regulator** once confirmed.
5. Add the exact BrickLink entry for the retained **36T driving gear** once confirmed.
6. Update the date below whenever sourcing information changes.

---

## Final Reproduction Snapshot

```text
ROBOT       : Starlight
TEAM        : Team Sentio
COMPETITION : WRO Future Engineers 2026

COMPUTE     : Raspberry Pi 5, 4 GB
VISION      : 2 × Raspberry Pi Camera Module 3 Wide
ORIENTATION : MPU6050 gyro module
STEERING    : DS3225 servo + Ackermann geometry
MOTOR       : JGB37-520, 12 V
DRIVER      : TB6612FNG
BATTERY     : 3S LiPo, 11.1 V, 2200 mAh
DRIVE       : 4WD
DIFFERENTIAL: LEGO Technic 28T differential
GEAR STAGE  : 36T driving → 24T driven
CHASSIS     : custom 3D-printed + LEGO Technic drivetrain components
```

---

### Last updated

**Team Sentio — Starlight / WRO Future Engineers 2026**

> Before ordering parts, re-check the supplier listing, electrical specifications, connector type and stock status. Product pages can change without notice.
