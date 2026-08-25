# Mechanical Differential — Beginner Guide  
### What it is, why a robot needs it, and how to build a Starlight-style drivetrain around it

> **Context:** This guide is written for a beginner building a four-wheel-drive robot with **Ackermann steering**, similar in concept to Team Sentio's **Starlight**.  
> The example drivetrain uses a **36-tooth driving gear → 24-tooth driven gear** stage, giving a **1.5× speed increase** before the wheel-drive system.

---

## 1. What is a mechanical differential?

A **mechanical differential** is a small gearbox that allows the **left and right driven wheels to rotate at different speeds while still receiving power from the same motor**.

That sounds strange at first because we normally want both wheels to move together.

The reason becomes clear when the robot turns.

### When the robot drives straight

Both wheels travel almost the same distance.

```text
LEFT WHEEL   ───────────────►
RIGHT WHEEL  ───────────────►
```

So both wheels can rotate at nearly the same speed.

### When the robot turns

The outside wheel follows a **larger circle** than the inside wheel.

```text
                   OUTSIDE WHEEL
              ┌───────────────────
          ┌───┘
      ROBOT
          └───┐
              └────────
               INSIDE WHEEL
```

The outside wheel therefore has to travel farther in the same amount of time.

That means:

```text
outside wheel speed > inside wheel speed
```

A differential allows this speed difference automatically.

---

# 2. Why is a differential useful?

Imagine connecting the left and right wheels rigidly to one solid axle.

Both wheels would then be forced to rotate at exactly the same speed.

During a turn:

- the outside wheel wants to rotate faster,
- the inside wheel wants to rotate slower,
- but the solid axle forces them to rotate together.

Something has to give.

Usually the tyres begin to:

- scrub,
- slide,
- skip,
- twist the chassis,
- or push the robot away from the intended steering path.

For a small autonomous robot, this can cause:

- inconsistent cornering,
- increased current draw,
- loss of traction,
- larger turning radius,
- unstable camera geometry,
- extra stress on gears and shafts.

A differential solves much of this mechanically.

---

# 3. Why this matters especially with Ackermann steering

Starlight uses **Ackermann-style steering**.

Ackermann steering already tries to make the front wheels point along the correct turning circles.

The inside steering wheel turns more than the outside steering wheel.

But correct wheel angles alone are not enough.

The wheels also need to rotate at the correct **speeds**.

So the two systems solve different parts of the same problem:

| System | What it allows |
|---|---|
| Ackermann steering | Left and right wheels point at different steering angles |
| Differential | Left and right driven wheels rotate at different speeds |

Together they make cornering much smoother.

---

# 4. The simplest way to imagine a differential

Think of the differential as a gearbox with:

```text
                 MOTOR INPUT
                     │
                     ▼
              ┌─────────────┐
              │ DIFFERENTIAL│
              └─────────────┘
                 /         \
                /           \
               ▼             ▼
        LEFT OUTPUT     RIGHT OUTPUT
```

When driving straight:

```text
Left output speed ≈ Right output speed
```

When turning:

```text
Left output speed ≠ Right output speed
```

The motor can continue powering both sides.

---

# 5. What is inside a basic differential?

A normal bevel-gear differential contains four important parts.

## 5.1 Differential housing or carrier

This is the rotating body driven by the motor.

It holds the smaller internal gears.

## 5.2 Ring gear / input gear

The drivetrain rotates the differential housing through this gear.

In LEGO Technic-style builds, the large toothed outer section of the differential often performs this job.

## 5.3 Side gears

There are two side gears:

- one connects to the left axle,
- one connects to the right axle.

## 5.4 Spider gears

Small bevel gears sit between the two side gears.

These are what allow one output axle to rotate faster than the other.

A simplified internal view looks like this:

```text
                     INPUT
                       │
                       ▼
              ┌────────────────┐
              │ rotating case  │
              │                │
 LEFT AXLE ◄──┤ side        side├──► RIGHT AXLE
              │ gear        gear│
              │      ╲  ╱       │
              │      spider     │
              │       gears     │
              └────────────────┘
```

---

# 6. What happens inside the differential?

## Case A — Robot travelling straight

Resistance at both wheels is similar.

The spider gears do not need to rotate much around their own axes.

The entire differential assembly rotates together.

Result:

```text
Left wheel speed ≈ Right wheel speed
```

---

## Case B — Robot turning

The inside wheel experiences a different required speed from the outside wheel.

The spider gears rotate inside the carrier.

This allows:

```text
one output to slow down
while
the other output speeds up
```

The important idea is:

> The differential does not decide which wheel is inside or outside.  
> It simply allows the wheels to rotate at the speeds demanded by the geometry and resistance of the turn.

---

# 7. Basic differential speed rule

For a simple open differential:

\[
\omega_{\text{carrier}}
=
\frac{\omega_L+\omega_R}{2}
\]

where:

- \(\omega_L\) = left-wheel angular speed,
- \(\omega_R\) = right-wheel angular speed,
- \(\omega_{\text{carrier}}\) = differential carrier speed.

### In very simple words

The differential carrier roughly rotates at the **average speed of the two outputs**.

Example:

```text
Left wheel  = 500 rpm
Right wheel = 700 rpm

Average = (500 + 700) / 2
        = 600 rpm
```

The differential can therefore accommodate the difference without forcing both wheels to 600 rpm.

---

# 8. Starlight-style gear stage: 36T → 24T

A drivetrain similar to Starlight can use:

```text
36-tooth driving gear
        ↓
24-tooth driven gear
```

The speed ratio is:

\[
\text{Speed ratio}
=
\frac{36}{24}
=
1.5
\]

So ideally:

```text
output speed = motor-side speed × 1.5
```

Example:

If the input shaft is turning at:

```text
600 rpm
```

then the ideal driven shaft speed is:

```text
600 × 1.5 = 900 rpm
```

### What this means in normal words

The 36T gear is larger than the 24T gear.

One revolution of the larger gear moves more teeth past the contact point, so the smaller gear has to rotate faster.

The trade-off is torque.

Ignoring losses:

\[
\text{Torque multiplier}
=
\frac{24}{36}
=
0.667
\]

So this gearing gives approximately:

```text
1.5× speed
but only about 0.67× torque
```

before friction and drivetrain losses.

That is why gearing must be tested under real robot load rather than chosen only from theoretical speed.

---

# 9. Where should the differential go?

A simple drivetrain layout is:

```text
MOTOR
  │
  ▼
36T GEAR
  │
  ▼
24T GEAR
  │
  ▼
DIFFERENTIAL
 /           \
▼             ▼
LEFT AXLE   RIGHT AXLE
```

For a **4WD robot**, there are several possible layouts.

---

# 10. 4WD differential arrangements

## Option A — One differential on each axle

```text
                    MOTOR
                      │
               central transmission
                 /             \
                ▼               ▼
       FRONT DIFFERENTIAL   REAR DIFFERENTIAL
          /       \            /       \
        FL        FR          RL        RR
```

Where:

- FL = front-left,
- FR = front-right,
- RL = rear-left,
- RR = rear-right.

### Advantages

- mechanically correct for four-wheel drive,
- each axle can accommodate left/right speed differences,
- smoothest turning.

### Disadvantages

- more parts,
- more backlash,
- more alignment work,
- more drivetrain losses.

---

## Option B — One differential with mechanically linked front/rear wheels

A simpler small-robot approach is:

```text
                       DIFFERENTIAL
                      /            \
                LEFT SIDE         RIGHT SIDE
                   │                  │
              shaft / gears       shaft / gears
               /       \           /       \
             FL        RL        FR        RR
```

Each differential output powers one **side** of the robot.

The front and rear wheels on that side are mechanically coupled.

### Advantages

- only one differential,
- compact,
- fewer gears,
- easier to build.

### Limitation

The front and rear wheel on the same side still cannot freely rotate at different speeds.

For a small robot with a short wheelbase and compliant tyres, this may still work well enough.

---

# 11. A practical Starlight-like concept

For a compact Ackermann robot, a useful conceptual drivetrain is:

```text
                        MOTOR
                          │
                          ▼
                     36T GEAR
                          │
                          ▼
                     24T GEAR
                          │
                          ▼
                  DIFFERENTIAL CASE
                    /           \
                   /             \
          LEFT OUTPUT          RIGHT OUTPUT
              │                    │
        left-side drive       right-side drive
          /        \            /        \
        FL          RL        FR          RR
```

This keeps all **four wheels driven** while still allowing the two sides of the robot to rotate at different average speeds.

> The exact shaft routing depends on the chassis.  
> The key design idea is that the differential should be located **before the drivetrain splits into left and right wheel groups**.

---

# 12. Parts needed for a LEGO/Technic-style differential

A beginner-friendly build normally needs:

### Differential components

- 1 differential housing / differential carrier
- 2 side bevel gears
- 2 or more spider bevel gears
- 2 output axles

### Input transmission

- 36T gear
- 24T gear
- motor output shaft
- supporting bearings/bushes

### Wheel transmission

- left output shaft
- right output shaft
- gears or shafts to transmit power to each wheel
- axle bushes / bearings
- wheel hubs

### Structural components

- rigid parallel beams or chassis plates
- cross-bracing
- axle supports
- spacers
- bushes
- retainers

The exact pieces can vary.

The important requirement is **geometry and alignment**, not the colour or exact beam type.

---

# 13. How to build the differential — beginner steps

## Step 1 — Build a rigid frame

Before installing gears, create two parallel structural rails.

```text
SIDE RAIL  =======================

          drivetrain space

SIDE RAIL  =======================
```

The rails should not twist easily.

A flexible frame causes:

- gears to separate,
- shafts to move,
- differential gears to bind.

---

## Step 2 — Install the differential carrier

Place the differential between the frame rails.

Its two output axles should point directly toward the left and right sides.

```text
LEFT SIDE  ◄──── [ DIFFERENTIAL ] ────► RIGHT SIDE
```

The differential must be:

- square to the chassis,
- centred,
- firmly supported.

---

## Step 3 — Support both output axles

Do not allow long unsupported axles.

Bad:

```text
[DIFF]──────────────WHEEL
```

Better:

```text
[DIFF]──[BEARING]──[BEARING]──WHEEL
```

In LEGO construction, a "bearing" is usually a properly aligned beam hole or axle support.

Multiple supports reduce axle bending.

---

## Step 4 — Add the input gear

Mount the gear that drives the differential housing.

Make sure the gears:

- fully mesh,
- are not forced together,
- cannot move sideways.

You should be able to rotate the drivetrain by hand.

---

## Step 5 — Add the 36T → 24T stage

A Starlight-like speed-up stage can be:

```text
motor shaft
    │
   36T
    ⚙
   24T
    │
differential input
```

Check that:

- both shafts are parallel,
- the gears overlap correctly,
- there is almost no sideways movement,
- the teeth do not skip under load.

---

## Step 6 — Connect left and right outputs

Connect:

```text
differential left output → left wheel drivetrain
differential right output → right wheel drivetrain
```

For 4WD, extend each side to both wheels.

Example:

```text
                LEFT OUTPUT
                     │
             ┌───────┴───────┐
             ▼               ▼
         FRONT LEFT       REAR LEFT
```

and similarly for the right side.

---

# 14. Very important: keep the shafts aligned

A differential can work perfectly on a table and still fail inside a robot because of poor shaft alignment.

Look for:

- bent axles,
- beams squeezing gears,
- gears touching structural parts,
- excessive sideways play,
- axle holes that are not parallel.

A good drivetrain should rotate easily by hand.

---

# 15. The hand test

Before connecting the motor, perform this test.

## Test 1 — Rotate the differential input

Both sides should turn smoothly.

## Test 2 — Hold the left wheel

Rotate the differential input.

The right wheel should still be able to rotate.

## Test 3 — Hold the right wheel

The left wheel should still move.

## Test 4 — Rotate one wheel manually

The opposite wheel may rotate in the opposite direction depending on how the drivetrain is constrained.

This is normal differential behaviour.

---

# 16. How to recognise a locked differential

If the left and right outputs are mechanically forced together:

```text
LEFT = RIGHT
```

the drivetrain behaves like a solid axle.

This can improve traction in some conditions, but it removes the main turning advantage of the differential.

For an Ackermann robot, a permanently locked axle usually creates more tyre scrub.

---

# 17. Open differential vs locked differential

| Open differential | Locked differential |
|---|---|
| Left/right speeds may differ | Left/right speeds forced equal |
| Smooth cornering | More tyre scrub |
| Lower mechanical stress in turns | Higher steering resistance |
| Can lose drive if one wheel has almost no traction | Better drive if one wheel slips |
| Good general choice for Ackermann steering | Useful only when traction is more important than turning freedom |

---

# 18. Why not simply control left and right wheels with software?

That is possible if the robot has separate left and right motors.

Software could command:

```text
inside motor  = slower
outside motor = faster
```

But a mechanical differential has an important advantage:

> It solves the speed difference automatically without requiring the computer to calculate exact wheel speeds.

For a robot already using:

- cameras,
- OpenCV,
- obstacle detection,
- heading estimation,
- parking logic,

it can be useful to let mechanics solve a mechanical problem.

---

# 19. Differential and Ackermann geometry together

During a left turn:

```text
Inside = LEFT
Outside = RIGHT
```

The steering geometry produces approximately:

\[
\delta_{\text{inside}} > \delta_{\text{outside}}
\]

and the wheel paths require:

\[
v_{\text{outside}} > v_{\text{inside}}
\]

Ackermann steering helps with the **first relationship**.

The differential helps with the **second relationship**.

That is why they complement each other.

---

# 20. Common beginner mistakes

## Mistake 1 — Building the differential loosely

If the carrier can move sideways, the gears may skip.

### Fix

Brace the differential from both sides.

---

## Mistake 2 — Over-constraining the axles

Too many badly aligned supports can create more friction than too few supports.

### Fix

Use several supports, but make sure they are actually collinear.

---

## Mistake 3 — Gears pressed too tightly together

This increases friction dramatically.

### Fix

Leave tiny mechanical clearance.

The gears should mesh, not grind.

---

## Mistake 4 — Very long unsupported axles

They twist and bend under torque.

### Fix

Place axle supports close to gears and wheels.

---

## Mistake 5 — Ignoring gear backlash

A small amount of gear play is normal.

Too much backlash causes:

- delayed response,
- jerky direction changes,
- inaccurate parking.

### Fix

Shorten the drivetrain and support gears properly.

---

## Mistake 6 — Testing only with the robot lifted

A drivetrain that works with the wheels in the air may fail on the floor.

### Why?

On the floor there is:

- tyre friction,
- robot mass,
- steering load,
- acceleration load.

Always test under real load.

---

# 21. Recommended testing sequence

Use the following order.

```text
1. Differential alone
        ↓
2. Gear train by hand
        ↓
3. Motor at low speed
        ↓
4. Wheels off ground
        ↓
5. Straight driving
        ↓
6. Slow steering
        ↓
7. Full left/right turns
        ↓
8. Higher-speed runs
        ↓
9. Repeated challenge laps
```

Do not go directly from assembly to full motor speed.

---

# 22. Differential troubleshooting

## Problem: drivetrain is difficult to rotate

Possible causes:

- gear mesh too tight,
- shafts misaligned,
- axle rubbing,
- differential squeezed by frame,
- bent axle.

---

## Problem: gears skip under acceleration

Possible causes:

- insufficient shaft support,
- loose frame,
- gear centres moving apart,
- motor torque too high for the structure.

---

## Problem: robot jerks during turning

Possible causes:

- differential binding,
- wheel on one side mechanically locked,
- front/rear coupling too rigid,
- steering geometry incorrect,
- tyre scrub.

---

## Problem: only one wheel spins

This can happen with an open differential when one side has much lower resistance.

Check whether:

- one wheel is lifted,
- one wheel has very low grip,
- the other side is jammed.

---

# 23. Differential design checklist

Before calling the drivetrain complete, check:

- [ ] Differential housing rotates smoothly
- [ ] Left axle rotates freely
- [ ] Right axle rotates freely
- [ ] Holding one side does not lock the entire gearbox
- [ ] 36T and 24T gears remain fully engaged
- [ ] Shafts have support close to major gears
- [ ] No gear rubs against chassis parts
- [ ] Axles cannot slide sideways excessively
- [ ] All four wheels receive drive
- [ ] Robot drives straight without severe binding
- [ ] Full steering lock does not cause excessive tyre hopping
- [ ] Drivetrain survives repeated acceleration and braking

---

# 24. A simple explanation for a judge

If someone asks:

> **Why did you use a mechanical differential?**

A good simple answer is:

> When the robot turns, the outside wheels have to travel farther than the inside wheels, so they cannot rotate at exactly the same speed. A mechanical differential allows the left and right sides of the drivetrain to rotate at different speeds while still receiving power from the same motor. This reduces tyre scrub and drivetrain stress and works well with our Ackermann steering system.

---

# 25. Slightly more technical explanation

> Starlight uses Ackermann steering, which creates different steering angles for the inside and outside wheels. The corresponding wheel paths also have different radii, so the two sides require different rotational speeds. A mechanical differential provides this speed freedom passively. It therefore reduces the need for tyre slip while preserving a single mechanical drive source.

---

# 26. Why the differential is a good engineering solution

The differential is a good example of an important engineering principle:

> **Do not solve every problem in software.**

The computer is already responsible for:

- camera processing,
- colour detection,
- wall geometry,
- state logic,
- obstacle avoidance,
- heading correction,
- parking.

The differential solves a turning-speed problem automatically using gears.

That makes the complete robot easier to control.

---

# 27. Final Starlight-style drivetrain concept

```text
                           MOTOR
                             │
                             ▼
                         [ 36T ]
                             ⚙
                         [ 24T ]
                             │
                             ▼
                    ┌────────────────┐
                    │  DIFFERENTIAL  │
                    └────────────────┘
                       /          \
                      /            \
                     ▼              ▼
               LEFT OUTPUT      RIGHT OUTPUT
                    │                │
             ┌──────┴──────┐  ┌─────┴──────┐
             ▼             ▼  ▼            ▼
        FRONT LEFT     REAR LEFT FRONT RIGHT REAR RIGHT

              ← four driven wheels / 4WD →
```

Combined with Ackermann steering:

```text
CAMERA / CONTROL
       │
       ▼
STEERING SERVO
       │
       ▼
ACKERMANN LINKAGE
       │
       ├── inside wheel: larger steering angle
       └── outside wheel: smaller steering angle

MOTOR
  │
  ▼
DIFFERENTIAL
  │
  ├── inside side: allowed to rotate slower
  └── outside side: allowed to rotate faster
```

This is the key idea:

> **Ackermann controls where the wheels point.  
> The differential allows them to rotate at the speeds the turn requires.**

---

# 28. One-page build summary

### Goal

Build a drivetrain that:

- powers all four wheels,
- allows left/right speed difference,
- works with Ackermann steering.

### Build order

```text
Rigid chassis
   ↓
Differential carrier
   ↓
Left/right output shafts
   ↓
36T → 24T input gearing
   ↓
Motor connection
   ↓
Front/rear side-drive connection
   ↓
Wheel installation
   ↓
Hand test
   ↓
Low-speed powered test
   ↓
Turning test
   ↓
Full robot test
```

### Most important rule

**If the drivetrain does not rotate smoothly by hand, do not fix it by increasing motor power.**

Find the mechanical resistance first.

---

## Final takeaway

A mechanical differential is not just an extra set of gears.

It is a device that allows the drivetrain to match the **geometry of a turn**.

For an Ackermann-steered four-wheel-drive robot, it can make the robot:

- smoother,
- more repeatable,
- easier to steer,
- less mechanically stressed,
- and easier for the software to control.

The best way to understand it is to build one, rotate the outputs by hand, and watch how the gears automatically allow one side to speed up while the other slows down.
