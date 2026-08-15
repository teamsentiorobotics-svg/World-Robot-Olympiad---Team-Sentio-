# Team Sentio — WRO Future Engineers 2026

This repository documents Team Sentio’s autonomous vehicle for the **World Robot Olympiad 2026 – Future Engineers** category.

**Team:** Deyaan Patel, Darsh Zaveri, Aarav Jalan
**Institution:** Robofun Lab (RFL), India
**Mechanical platform:** V3 | **Open software:** V5

Our engineering cycle is:

**Build → Test → Observe → Find the failure → Modify → Retest**

## Repository structure

* `src/` — Open and Obstacle Challenge programs
* `models/` — CAD views of chassis and mounts
* `schemes/` — electrical schematic and wiring
* `v-photos/` — vehicle photographs
* `t-photos/` — team photographs
* `video/` — driving demonstration
* `other/` — supporting notes and tests

## 1. Mobility and mechanical design

V3 is about **865 g** and measures **170 × 128 × 265 mm**. Wheelbase is **107.5 mm**, track width **110 mm**, wheel diameter **46 mm**, and ground clearance **14 mm**.

The chassis is mainly 3D-printed PLA with selected LEGO Technic parts. The robot uses **pure Ackermann steering**; both front wheels steer together and are driven through a differential.

Open steering limits are `LEFT=70`, `CENTER=95`, `RIGHT=125`. Larger commands stressed the LEGO steering supports and could disconnect the linkage, so the final range balances turning ability with reliability.

### Drivetrain

Current motor: **JGB37-520, 12 V, 600 RPM**.
Gear pair: **36T driving → 20T driven**.

`36 / 20 = 1.8`
`600 × 1.8 = 1080 RPM ideal`

With 46 mm wheels, ideal wheel-surface speed is about **2.60 m/s**. Practical/test-derived output was closer to **800 RPM**, or about **1.93 m/s**. This is an estimate, not a laboratory measurement.

The previous 1000 RPM Johnson motor stalled after crashes/high load and the TB6612FNG driver smoked. We replaced both; the same stall has not returned. Reliability became more important than maximum RPM.

## 2. Power and sensor architecture

The controller is a **Raspberry Pi 5, 4 GB**. Main components are two Camera Module 3 cameras, JGB37-520 motor, TB6612FNG driver, DS3225 servo, MPU6050 IMU, SSD1306 OLED and **3S 11.1 V 2200 mAh LiPo**.

Battery energy is `11.1 × 2.2 = 24.42 Wh`. A full pack measured about **12.2 V**; observed endurance was about **1.5 h / 50–60 laps**, not a controlled discharge test.

An earlier **5 V / 3 A** Pi supply produced repeated undervoltage warnings, so we moved to a higher-current 5 V supply.

Main pins:

* GPIO5/6/13 — motor direction/PWM
* GPIO22 — servo
* GPIO2/3 — I2C SDA/SCL

The detailed wiring diagram is in `schemes/`.

A LiPo charging failure and a reverse-polarity incident also changed our safety process: supervised charging, polarity checks and a safer connector strategy.

## 3. Sensor placement and calibration

Front camera: about **5 mm right of centre**, **50° downward pitch**.
Rear camera: about **45° downward pitch, 0° yaw**, mainly for parking.

Earlier camera positions caused late line and unstable corner-wall detection. Changing the physical geometry solved much of it: **a software-looking problem can have a mechanical solution**.

At startup, auto exposure/white balance run for about two seconds, then exposure and gain are locked. A front LED also improved low-light detection without noticeable saturation.

## 4. Open Challenge software

`src/Open_Challenge.py` uses Python, OpenCV, NumPy, Picamera2 and RPi.GPIO at **1280 × 680 RGB888**.

Image flow:

**Frame → blur → LAB → CLAHE → masks → morphology → contours → geometry → steering**

Black-wall contours guide the robot. Both-wall geometry gives proportional error; one-wall visibility uses a direction-aware reference; no wall gives a small directional bias. This replaced an older centring method that meandered in corners.

Final Open value:

`KP = 0.012`

We tested about **0.010–0.050**. `0.010` was too weak, `0.015–0.020` was more aggressive, and `0.050` could overload the steering linkage. `0.012` gave the best observed balance.

### Direction and lap counting

The first valid marker sets direction:

* Blue first → anticlockwise
* Orange first → clockwise

The first marker only sets direction. Later crossings use **rising-edge logic**, so one marker staying visible is counted once.

`LINE_COOLDOWN = 1.3 s`

Shorter values caused duplicate counts; longer values could miss genuine crossings.

The setup uses **3 laps × 4 events = 12 counts**, then centres and stops.

Successful Open times: **36, 30, 27, 28, 24, 25, 27 s**. Best recorded time: **24 s**.

## 5. Obstacle Challenge

`src/Obstacle_Challenge.py` detects black walls, red/green pillars, direction markers and the magenta/purple parking cue.

Instead of one fixed timed turn, each pillar is treated as a **continuous image target**. Steering keeps updating as the pillar moves through the frame.

This came from a corner-pillar failure where older logic committed too early. The new method uses pillar position/proximity before passing, then returns to wall following. Obstacle runs also use a lower preferred speed for more reaction time.

The team has achieved **10+ successful full Obstacle Challenge runs**. We did not retain the total number of failed attempts, so we do not claim a success percentage.

## 6. Parking

Parking uses the rear camera because rear-wall geometry becomes the main constraint.

**Course complete → parking stage → magenta/purple cue → rear view → MPU6050 heading → short forward/reverse corrections → stop inside the area**

Parking combines rear-camera feedback, gyro/IMU heading and controlled forward/reverse movement.

The main problem has been contacting the back wall. Ackermann steering cannot rotate in place, so parking needs several small positioning movements.

## 7. Engineering decisions and trade-offs

* **1000 RPM motor → 600 RPM JGB37-520:** old motor stalled and damaged the driver.
* **Maximum servo travel → safe limits:** protected LEGO steering supports.
* **Two-wall centring → direction-aware wall logic:** reduced meandering.
* **Fixed obstacle turn → proportional pillar target:** improved corner behaviour.
* **Old camera pose → revised front/rear geometry:** improved perception.
* **Ambient light → front LED:** improved low-light detection.
* **Power connector → safer keyed connector:** reduced polarity risk.
* **Rear wing → removed:** testing did not justify it.

These choices show that mechanics, electronics and software affected each other.

## 8. Testing method

Normal sequence:

**Component test → subsystem test → low-speed integrated test → full challenge run → classify failure → modify → retest**

Before a run we check power/polarity, drivetrain, servo centre, motor direction, cameras, colour detection, IMU and the correct program.

We separate measurements from estimates. Exact motor torque, whole-robot current, processing latency and a controlled obstacle success-rate denominator were not retained, so we do not invent them.

## 9. Reproducing the robot

1. Use `v-photos/` and `models/` for the mechanical build.
2. Assemble and freely test the differential/Ackermann drivetrain.
3. Wire from `schemes/`; confirm polarity and common ground.
4. Use GPIO5/6/13 for motor, GPIO22 servo and GPIO2/3 I2C.
5. Set camera angles and calibrate safe steering limits.
6. Test motor, servo, cameras and IMU separately.
7. Install the required Python libraries.
8. Start at low speed and change one tuning variable at a time.

## 10. Development history and GitHub practice

* **V0** — LEGO mobility prototype
* **V0.5** — rear-wing experiment
* **V1** — working circuit + camera control
* **V2** — 3D-printed electronics mount
* **V3** — purpose-built chassis, revised drivetrain and dual cameras
* **Open V5** — direction-aware wall control, `KP=0.012`, rising-edge counting

Commit messages should explain what changed and why, for example `fix(power): upgrade Pi supply after undervoltage` or `feat(open): add rising-edge line counting`.

## Team contributions

**Deyaan Patel:** software, algorithms, debugging, tuning and track testing.
**Darsh Zaveri:** hardware integration, LEGO mechanisms, circuits, wiring and testing.
**Aarav Jalan:** CAD, algorithm contributions, debugging, documentation and circuit construction.

Robofun Lab provided test access, mock runs and guidance at roadblocks. The submitted vehicle, code, testing and decisions remain Team Sentio’s work.
