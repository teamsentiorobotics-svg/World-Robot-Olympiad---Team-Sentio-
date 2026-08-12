# World-Robot-Olympiad Team-Sentio
Engineering materials
====

This repository contains engineering materials of a self-driven vehicle's model participating in the WRO Future Engineers competition in the season 2026.

## Content

* `t-photos` contains 2 photos of the team (an official one and one funny photo with all team members)
* `v-photos` contains 6 photos of the vehicle (from every side, from top and bottom)
* `video` contains the video.md file with the link to a video where driving demonstration exists
* `schemes` contains one or several schematic diagrams in form of JPEG, PNG or PDF of the electromechanical components illustrating all the elements (electronic components and motors) used in the vehicle and how they connect to each other.
* `src` contains code of control software for all components which were programmed to participate in the competition
* `models` is for the files for models used by 3D printers, laser cutting machines and CNC machines to produce the vehicle elements. If there is nothing to add to this location, the directory can be removed.
* `other` is for other files which can be used to understand how to prepare the vehicle for the competition. It may include documentation how to connect to a SBC/SBM and upload files there, datasets, hardware specifications, communication protocols descriptions etc. If there is nothing to add to this location, the directory can be removed.

# Team Sentio — WRO Future Engineers 2026

This repository documents Team Sentio’s autonomous vehicle for the World Robot Olympiad 2026 Future Engineers category.

## Vehicle Overview

The current V3 vehicle has a mass of approximately 865 g. The chassis is mainly 3D printed in PLA with selected LEGO Technic parts.

Its dimensions are 170 mm length, 128 mm width, 265 mm height, 107.5 mm wheelbase, 110 mm front and rear track width, 46 mm wheel diameter, and 14 mm ground clearance.

It uses pure Ackermann steering. Both front wheels steer together and both are driven through a differential.

## Electronics and Drivetrain

The controller is a Raspberry Pi 5 with 4 GB RAM running Raspberry Pi OS. Main components include two Raspberry Pi Camera Module 3 cameras, a JGB37-520 12 V geared DC motor, DFRobot TB6612FNG motor driver, DS3225 steering servo, MPU6050 IMU, SSD1306 OLED, 5 V 3 A step-down supply, 11.1 V 2200 mAh 3S LiPo battery, and front illumination LED.

The motor is rated at 600 RPM. A 36-tooth driving gear meshes with a 20-tooth driven gear and transfers power through the differential to both front wheels.

The previous 1000 RPM Johnson motor stalled under heavy load after crashes and damaged the motor driver. Both were replaced. The new motor is lighter and the stalling problem has not returned.

Steering limits are LEFT = 70, CENTER = 95 and RIGHT = 125. Larger commands stressed the LEGO steering supports, so these values balance turning ability with reliability.

## Open Challenge Software

The Open Challenge uses Python, OpenCV, Picamera2 and RPi.GPIO. The main camera runs at 1280 × 680 in RGB888 format. Auto exposure and white balance settle for about two seconds before exposure and gain are locked.

Frames are blurred using a 5 × 5 Gaussian kernel and processed in LAB colour space. CLAHE improves local contrast and black wall contours provide proportional steering.

python
KP = 0.012
LINE_COOLDOWN = 1.3
CENTER = 95
LEFT = 70
RIGHT = 125
IN1_PIN = 5
IN2_PIN = 6
PWM_PIN = 13
SERVO_PIN = 22


The first valid blue marker selects anticlockwise travel and the first valid orange marker selects clockwise travel. The first marker determines direction only. Later crossings use rising-edge logic and a cooldown. The configuration uses 3 laps, 4 line events per lap, and 12 counted events before stopping.

## Obstacle Challenge

The Obstacle Challenge uses LAB colour detection for red and green pillars and proportional visual steering. Purple is part of the parking trigger. Parking begins only when the required line-count stage is reached and purple is detected. The MPU6050 provides heading information during parking.

Approximately 10 successful Obstacle Challenge runs have been achieved. The main remaining difficulties are parking and wall detection for certain block positions.

## Cameras and Testing

The front camera is approximately 5 mm right of centre with about 50° downward pitch. The rear camera is on a raised LEGO stand at about 45° downward pitch and 0° yaw for parking.

A front LED controlled by a slide switch improves detection in lower room lighting. Testing showed better low-light detection without noticeable saturation.

Recorded Open Challenge times are 36, 30, 27, 28, 24, 25 and 27 seconds, with a best time of 24 seconds.

## Development and Failures

The project began with an almost completely LEGO prototype. Later versions added a working circuit, 3D-printed circuit mount, purpose-built chassis, second camera, and revised camera geometry.

Failures changed the design. Camera-angle problems caused late detections. A polarity-reversal incident damaged a Raspberry Pi and caused repeated rebooting. An earlier 2100 mAh LiPo also suffered a charging-related failure. These events led to stricter power, polarity, charging, and pre-run checks.

Source code is stored in src/, CAD in models/, wiring diagrams in schemes/, photographs in t-photos/ and v-photos/, video material in video/, and test evidence in other/.

Our process is: build, test, observe, identify the failure, modify, and retest.](https://github.com/teamsentiorobotics-svg/World-Robot-Olympiad---Team-Sentio-.git)
