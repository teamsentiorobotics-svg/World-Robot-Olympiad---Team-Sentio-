# WRO FINAL COMBINED VISION - RASPBERRY PI
# Resolution: 640 x 360
#
# Final combined version:
# - Keeps every ROI from the current 640x360 vision code
# - One HARD robot exclusion ROI covers the full visible black robot/body region
# - Separate HARD wire exclusion ROI covers the bottom-right wire
# - Exclusions apply to RED/GREEN/BLUE/ORANGE/MAGENTA/BLACK,
#   black-wall detection and black-pillar detection
# - Black detection uses darkness in HSV Value + LAB L
# - Camera AE/AWB settles for 1 s and is then locked when supported
# - Orange/Blue are constrained to ORANGE_BLUE_ROI
# - Duplicate wall/pillar detections are suppressed
#
# Controls:
#   Q / ESC = quit
#   M       = show/hide masks
#   S       = save screenshot

import cv2
from picamera2 import Picamera2
import numpy as np
import time


# ============================================================
# CAMERA
# ============================================================

WIDTH = 720
HEIGHT = 360
FPS = 60

CALIBRATION_SECONDS = 1.0

CALIBRATED_EXPOSURE = None
CALIBRATED_WB = None


# ============================================================
# TOP EXCLUSION
# ============================================================

TOP_BLACK_HEIGHT = 0

TOP_BLACK_ROI = (
    0,
    0,
    WIDTH,
    TOP_BLACK_HEIGHT
)

DETECTION_Y_START = TOP_BLACK_HEIGHT


# ============================================================
# HSV RANGES
# ============================================================

RED1_LOWER = np.array(
    [0, 115, 42],#[0, 115, 65],
    dtype=np.uint8
)

RED1_UPPER = np.array(
    [8, 255, 155],#[8, 255, 255],
    dtype=np.uint8
)

RED2_LOWER = np.array(
    [172, 115, 42],#[172, 115, 65],
    dtype=np.uint8
)

RED2_UPPER = np.array(
    [180, 255, 155],#[180, 255, 255],
    dtype=np.uint8
)

GREEN_LOWER = np.array(
    [47, 115, 89],#[51,102,91], #[49,56,88], #[49, 56, 88],
    dtype=np.uint8
)

GREEN_UPPER = np.array(
    [66, 185, 198],#[74, 190, 193], #[71, 163, 188],
    dtype=np.uint8
)


ORANGE_LOWER = np.array(
    [14, 20, 100],
    dtype=np.uint8
)

ORANGE_UPPER = np.array(
    [53, 209, 200],
    dtype=np.uint8
)


BLUE_LOWER = np.array(
    [100, 93, 81],
    dtype=np.uint8
)

BLUE_UPPER = np.array(
    [117, 227, 161],
    dtype=np.uint8
)


MAGENTA_LOWER = np.array(
    [161, 122, 72],
    dtype=np.uint8
)

MAGENTA_UPPER = np.array(
    [171, 241, 166],#[171, 241, 166],
    dtype=np.uint8
)


# Robust black definition.
# Pixel must be dark in BOTH HSV Value and LAB L.
BLACK_MAX_V = 85#100 
BLACK_MAX_L = 95#105 


# ============================================================
# ALL EXISTING ROIs
# ============================================================

LEFT_1_ROI = (
    0,
    0,
    105,
    HEIGHT - 20
)

LEFT_2_ROI = (
    150,
    150,
    200,
    HEIGHT - 100
)


RIGHT_1_ROI = (
    #130 - parking
    WIDTH - 105,
    0,
    WIDTH,
    HEIGHT - 20
)

RIGHT_2_ROI = (
    WIDTH - 200,
    150,
    WIDTH - 150,
    HEIGHT - 100
)


CENTER_BLACK_ROI = (
    320,
    20,
    WIDTH - 320,
    70
)

ORANGE_BLUE_ROI = (
    260,
    120,
    WIDTH -260,
    150
)

# MAGENTA_ROI = (
#     340,
#     200,
#     380,
#     235
#)
# PILLAR_ROI = (
#     35,
#     TOP_BLACK_HEIGHT + 10,
#     WIDTH - 35,
#     HEIGHT - 18
# )
PILLAR_ROI = (
    0,
    TOP_BLACK_HEIGHT + 10,
    WIDTH - 35,
    0
)


# ============================================================
# CRASH ZONE
# ============================================================

CRASH_ZONE_ROI = (
    200,
    170,
    WIDTH - 200,
    HEIGHT - 70
)


BLACK_ROIS = {
    "LEFT WALL": LEFT_1_ROI,

    "LEFT INNER": LEFT_2_ROI,

    "CENTER BLACK": CENTER_BLACK_ROI,

    "RIGHT INNER": RIGHT_2_ROI,

    "RIGHT WALL": RIGHT_1_ROI,
}


# ============================================================
# HARD ROBOT / WIRE EXCLUSIONS
# ============================================================
#
# IMPORTANT:
#
# Nothing inside either of these boxes can ever participate
# in ANY detection.
#
# ROBOT:
# One rectangle covers the complete visible black robot/body
# region from the screenshot, including the black protruding
# part on the lower-left.
#
# WIRE:
# Separate box for the bottom-right visible wire/hardware.
#

ROBOT_EXCLUSION_ROI = (
    200,
    HEIGHT- 70,
    WIDTH-200,
    HEIGHT
)


WIRE_EXCLUSION_ROI = (
    0,
    0,
    0,
    0
)


EXCLUSION_ROIS = [
    TOP_BLACK_ROI,

    ROBOT_EXCLUSION_ROI,

    WIRE_EXCLUSION_ROI,
]


# ============================================================
# DETECTION PARAMETERS
# ============================================================

MIN_CONFIDENCE = 0.55


MIN_AREA = {
    "RED": 300,

    "GREEN": 300,

    "BLUE": 20,#250

    "ORANGE": 20,#250

    "MAGENTA": 500,

    "BLACK": 250,
}


# ============================================================
# BLACK WALL FILTERS
# ============================================================

BLACK_MIN_AREA = 100

BLACK_MIN_WIDTH = 8

BLACK_MIN_HEIGHT = 6

BLACK_MIN_ASPECT = 0.45

BLACK_MAX_ASPECT = 8.0

BLACK_MIN_RECTANGULARITY = 0.20

BLACK_MIN_ROI_FILL = 0.002
BLACK_MIN_CONFIDENCE = 0.15


# ============================================================
# BLACK PILLAR FILTERS
# ============================================================

PILLAR_MIN_AREA = 500

PILLAR_MIN_WIDTH = 12

PILLAR_MIN_HEIGHT = 35

PILLAR_MIN_ASPECT = 1.15

PILLAR_MAX_ASPECT = 7.0

PILLAR_MIN_RECTANGULARITY = 0.32

PILLAR_MIN_DARK_RATIO = 0.55

PILLAR_MAX_CANDIDATES = 3


# Prevent the same black wall contour from also being
# reported as a BLACK PILLAR.
PILLAR_WALL_DUPLICATE_IOU = 0.30


KERNEL = cv2.getStructuringElement(
    cv2.MORPH_ELLIPSE,
    (7, 7)
)


# ============================================================
# LAB REFERENCES
# ============================================================

LAB_REFERENCE = {
    "RED": np.array(
        [194, 114, 139,],#[136, 208, 195],
        dtype=np.float32
    ),

    "GREEN": np.array(
        [150, 80, 170],
        dtype=np.float32
    ),

    "BLUE": np.array(
        [90, 180, 70],
        dtype=np.float32
    ),

    "ORANGE": np.array(
        [170, 150, 210],
        dtype=np.float32
    ),

    "MAGENTA": np.array(
        [150, 210, 120],
        dtype=np.float32
    ),
}


LAB_TOLERANCE = {
    "RED": 85,

    "GREEN": 85,

    "BLUE": 85,

    "ORANGE": 90,

    "MAGENTA": 90,
}


# ============================================================
# CAMERA
# ============================================================

def start_camera():

    """
    Start the camera using the same two-phase calibration approach
    as the previous working vision system.

    Phase 1:
        AE + AWB are explicitly enabled and allowed to settle for
        one second while the camera sees the actual competition field.

    Phase 2:
        The settled ExposureTime, AnalogueGain and ColourGains are
        read from camera metadata, applied back to the camera, and
        AE + AWB are then disabled so the values remain locked during
        the run.
    """

    global CALIBRATED_EXPOSURE
    global CALIBRATED_WB

    picam2 = Picamera2()

    config = picam2.create_video_configuration(
        main={
            "size": (
                WIDTH,
                HEIGHT
            ),
            "format": "BGR888"
        },
        controls={
            "FrameRate": FPS,
            "AeEnable": True,
            "AwbEnable": True,
        }
    )

    picam2.configure(config)
    picam2.start()

    # --------------------------------------------------------
    # PHASE 1: AUTO EXPOSURE + AUTO WHITE BALANCE
    # --------------------------------------------------------
    # Explicitly enable both automatic systems after start as well.
    # This guarantees the camera is allowed to adapt to the field
    # before we capture the calibration values.
    # --------------------------------------------------------
    picam2.set_controls({
        "AeEnable": True,
        "AwbEnable": True,
    })

    time.sleep(CALIBRATION_SECONDS)

    try:
        # Read the values calculated by AE/AWB after the one-second
        # settling period.
        metadata = picam2.capture_metadata()

        exposure = metadata.get("ExposureTime")
        gain = metadata.get("AnalogueGain")
        wb = metadata.get("ColourGains")

        # ----------------------------------------------------
        # PHASE 2: APPLY SETTLED VALUES AND LOCK THEM
        # ----------------------------------------------------
        controls = {
            "AeEnable": False,
            "AwbEnable": False,
        }

        if exposure is not None:
            controls["ExposureTime"] = int(exposure)

        if gain is not None:
            controls["AnalogueGain"] = float(gain)

        if wb is not None:
            controls["ColourGains"] = tuple(wb)

        picam2.set_controls(controls)

        CALIBRATED_EXPOSURE = {
            "ExposureTime": exposure,
            "AnalogueGain": gain,
        }

        CALIBRATED_WB = wb

        print(
            "Camera calibrated and locked: "
            f"ExposureTime={exposure}, "
            f"AnalogueGain={gain}, "
            f"ColourGains={wb}"
        )

    except Exception as exc:
        print(f"Camera lock warning: {exc}")

    return picam2


# ============================================================
# ROI / MASK HELPERS
# ============================================================

def rectangle_mask(
    shape,
    roi
):

    x1, y1, x2, y2 = roi


    x1 = max(
        0,
        min(
            shape[1],
            int(x1)
        )
    )


    x2 = max(
        0,
        min(
            shape[1],
            int(x2)
        )
    )


    y1 = max(
        0,
        min(
            shape[0],
            int(y1)
        )
    )


    y2 = max(
        0,
        min(
            shape[0],
            int(y2)
        )
    )


    mask = np.zeros(
        shape[:2],
        dtype=np.uint8
    )


    if (
        x2 > x1 and
        y2 > y1
    ):

        mask[
            y1:y2,
            x1:x2
        ] = 255


    return mask


def build_allowed_detection_mask(
    shape
):

    """
    255 = detection allowed.

    0 = absolutely forbidden.

    This is the master hard-exclusion mask.
    """

    allowed = np.full(
        shape[:2],
        255,
        dtype=np.uint8
    )


    for roi in EXCLUSION_ROIS:

        x1, y1, x2, y2 = roi


        x1 = max(
            0,
            min(
                shape[1],
                int(x1)
            )
        )


        x2 = max(
            0,
            min(
                shape[1],
                int(x2)
            )
        )


        y1 = max(
            0,
            min(
                shape[0],
                int(y1)
            )
        )


        y2 = max(
            0,
            min(
                shape[0],
                int(y2)
            )
        )


        if (
            x2 > x1 and
            y2 > y1
        ):

            allowed[
                y1:y2,
                x1:x2
            ] = 0


    return allowed


def clean_mask(
    mask
):

    mask = cv2.morphologyEx(
        mask,

        cv2.MORPH_OPEN,

        KERNEL
    )


    mask = cv2.morphologyEx(
        mask,

        cv2.MORPH_CLOSE,

        KERNEL
    )


    return mask


# ============================================================
# MASK CREATION
# ============================================================

def make_color_masks(
    hsv,
    lab,
    allowed_mask
):

    masks = {}


    red1 = cv2.inRange(
        hsv,

        RED1_LOWER,

        RED1_UPPER
    )


    red2 = cv2.inRange(
        hsv,

        RED2_LOWER,

        RED2_UPPER
    )


    masks["RED"] = clean_mask(

        cv2.bitwise_or(
            red1,
            red2
        )
    )


    masks["GREEN"] = clean_mask(

        cv2.inRange(
            hsv,

            GREEN_LOWER,

            GREEN_UPPER
        )
    )


    masks["ORANGE"] = clean_mask(

        cv2.inRange(
            hsv,

            ORANGE_LOWER,

            ORANGE_UPPER
        )
    )


    masks["BLUE"] = clean_mask(

        cv2.inRange(
            hsv,

            BLUE_LOWER,

            BLUE_UPPER
        )
    )


    masks["MAGENTA"] = clean_mask(

        cv2.inRange(
            hsv,

            MAGENTA_LOWER,

            MAGENTA_UPPER
        )
    )


    # --------------------------------------------------------
    # BLACK
    # --------------------------------------------------------
    #
    # Black hue is unstable and essentially meaningless.
    #
    # Instead:
    #
    #   HSV V <= BLACK_MAX_V
    #
    # AND
    #
    #   LAB L <= BLACK_MAX_L
    #

    black = np.where(

        (
            hsv[:, :, 2] <=
            BLACK_MAX_V
        )
        &
        (
            lab[:, :, 0] <=
            BLACK_MAX_L
        ),

        255,

        0

    ).astype(
        np.uint8
    )


    masks["BLACK"] = clean_mask(
        black
    )


    # --------------------------------------------------------
    # HARD EXCLUSION
    # --------------------------------------------------------
    #
    # Applied AFTER morphology.
    #
    # Every mask is guaranteed to be zero in:
    #
    # robot exclusion
    # wire exclusion
    # top exclusion
    #

    for name in masks:

        masks[name] = cv2.bitwise_and(

            masks[name],

            allowed_mask
        )


    return masks


# ============================================================
# GEOMETRY
# ============================================================

def geometry_score(
    contour
):

    area = cv2.contourArea(
        contour
    )


    if area <= 0:

        return 0.0


    _, _, w, h = (
        cv2.boundingRect(
            contour
        )
    )


    if (
        w <= 0 or
        h <= 0
    ):

        return 0.0


    fill = (
        area /
        float(
            w * h
        )
    )


    hull = cv2.convexHull(
        contour
    )


    hull_area = cv2.contourArea(
        hull
    )


    solidity = (
        area /
        float(
            max(
                hull_area,
                1.0
            )
        )
    )


    fill_score = np.clip(
        fill / 0.55,
        0.0,
        1.0
    )


    solidity_score = np.clip(
        solidity / 0.75,
        0.0,
        1.0
    )


    return float(

        0.65 * fill_score
        +
        0.35 * solidity_score
    )


# ============================================================
# LAB SCORE
# ============================================================

def lab_score(
    frame_lab,
    contour,
    color_name
):

    if (
        color_name not in
        LAB_REFERENCE
    ):

        return 1.0


    mask = np.zeros(
        frame_lab.shape[:2],
        dtype=np.uint8
    )


    cv2.drawContours(
        mask,

        [contour],

        -1,

        255,

        -1
    )


    pixels = frame_lab[
        mask > 0
    ]


    if len(
        pixels
    ) == 0:

        return 0.0


    # Limit pixel workload while keeping
    # a stable median measurement.

    step = max(
        1,

        len(pixels) //
        2048
    )


    median_lab = np.median(

        pixels[
            ::step
        ],

        axis=0

    ).astype(
        np.float32
    )


    distance = np.linalg.norm(

        median_lab
        -
        LAB_REFERENCE[
            color_name
        ]
    )


    score = (
        1.0
        -
        distance /
        LAB_TOLERANCE[
            color_name
        ]
    )


    return float(

        np.clip(
            score,
            0.0,
            1.0
        )
    )


# ============================================================
# HSV SCORE
# ============================================================

def hsv_score(
    hsv,
    contour,
    color_name
):

    mask = np.zeros(
        hsv.shape[:2],
        dtype=np.uint8
    )


    cv2.drawContours(
        mask,

        [contour],

        -1,

        255,

        -1
    )


    pixels = hsv[
        mask > 0
    ]


    if len(
        pixels
    ) == 0:

        return 0.0


    med_s = float(

        np.median(
            pixels[:, 1]
        )
    )


    med_v = float(

        np.median(
            pixels[:, 2]
        )
    )


    if color_name == "RED":

        s = np.clip(
            (med_s - 70) / 100,
            0.0,
            1.0
        )


        v = np.clip(
            (med_v - 45) / 100,
            0.0,
            1.0
        )


        return float(
            0.65 * s
            +
            0.35 * v
        )


    if color_name == "GREEN":

        s = np.clip(
            (med_s - 50) / 100,
            0.0,
            1.0
        )


        v = np.clip(
            (med_v - 30) / 100,
            0.0,
            1.0
        )


        return float(
            0.60 * s
            +
            0.40 * v
        )


    s = np.clip(
        (med_s - 40) / 120,
        0.0,
        1.0
    )


    v = np.clip(
        (med_v - 30) / 120,
        0.0,
        1.0
    )


    return float(
        0.60 * s
        +
        0.40 * v
    )


# ============================================================
# CONFIDENCE
# ============================================================

def calculate_confidence(
    lab,
    hsv,
    contour,
    color_name
):

    geom = geometry_score(
        contour
    )


    hsv_s = hsv_score(
        hsv,
        contour,
        color_name
    )


    lab_s = lab_score(
        lab,
        contour,
        color_name
    )


    if color_name in (
        "RED",
        "GREEN"
    ):

        confidence = (

            0.60 * hsv_s
            +
            0.20 * lab_s
            +
            0.20 * geom
        )


    else:

        confidence = (

            0.45 * hsv_s
            +
            0.30 * lab_s
            +
            0.25 * geom
        )


    return float(

        np.clip(
            confidence,
            0.0,
            1.0
        )
    )


# ============================================================
# COLOR DETECTION
# ============================================================

def detect_color(
    hsv,
    lab,
    mask,
    color_name
):

    contours, _ = cv2.findContours(

        mask,

        cv2.RETR_EXTERNAL,

        cv2.CHAIN_APPROX_SIMPLE
    )


    best = None


    for contour in contours:

        area = cv2.contourArea(
            contour
        )


        if (
            area <
            MIN_AREA[
                color_name
            ]
        ):

            continue


        confidence = calculate_confidence(

            lab,

            hsv,

            contour,

            color_name
        )


        if (
            confidence <
            MIN_CONFIDENCE
        ):

            continue


        # Combines confidence with meaningful size.
        #
        # Prevents one large weak contour from
        # automatically beating a clean object.

        score = (

            confidence
            *
            np.sqrt(
                max(
                    area,
                    1.0
                )
            )
        )


        if (
            best is None
            or
            score > best[0]
        ):

            best = (

                score,

                contour,

                confidence,

                area
            )


    if best is None:

        return None


    (
        _,
        contour,
        confidence,
        area
    ) = best


    x, y, w, h = cv2.boundingRect(
        contour
    )


    return {
        "color": color_name,

        "contour": contour,

        "bbox": (
            x,
            y,
            w,
            h
        ),

        "area": area,

        "confidence": confidence,
    }


# ============================================================
# BLACK WALL DETECTION
# ============================================================

def detect_black_walls(
    black_mask,
    color_masks,
    allowed_mask
):

    # ========================================================
    # BLACK WALL DETECTION
    # ========================================================
    #
    # IMPORTANT DESIGN:
    #
    # Each BLACK_ROI is treated as a completely independent
    # detection area.
    #
    # 1. Build one clean black mask.
    # 2. Clip that mask to ONE ROI.
    # 3. Run morphology INSIDE that ROI only.
    # 4. Find contours INSIDE that ROI only.
    # 5. Convert the contour coordinates back to the
    #    full-frame coordinates.
    #
    # Therefore:
    #
    # - A black object larger than an ROI is clipped at the
    #   ROI boundary.
    # - A contour can NEVER extend outside its own ROI.
    # - If the same black object is visible in RIGHT INNER
    #   and RIGHT WALL, each ROI gets its own independent
    #   contour.
    # - Contours from different ROIs are NEVER merged.
    # ========================================================

    # --------------------------------------------------------
    # Remove pixels already owned by a colour.
    # --------------------------------------------------------

    colored = np.zeros_like(
        black_mask
    )

    for name in (
        "RED",
        "GREEN",
        "BLUE",
        "ORANGE",
        "MAGENTA"
    ):

        colored = cv2.bitwise_or(
            colored,
            color_masks[name]
        )

    # Clean black pixels before entering the ROI loop.
    # The important part is that ROI-specific morphology
    # happens later, separately for every ROI.
    clean_black = cv2.bitwise_and(
        black_mask,
        cv2.bitwise_not(colored)
    )

    clean_black = cv2.bitwise_and(
        clean_black,
        allowed_mask
    )

    detections = []

    # --------------------------------------------------------
    # PROCESS EACH BLACK ROI INDEPENDENTLY
    # --------------------------------------------------------

    for label, roi in BLACK_ROIS.items():

        x1, y1, x2, y2 = roi

        # Keep coordinates inside the actual frame.
        x1 = max(0, min(int(x1), clean_black.shape[1]))
        x2 = max(0, min(int(x2), clean_black.shape[1]))
        y1 = max(0, min(int(y1), clean_black.shape[0]))
        y2 = max(0, min(int(y2), clean_black.shape[0]))

        if x2 <= x1 or y2 <= y1:
            continue

        # ----------------------------------------------------
        # IMPORTANT:
        # The mask is cropped BEFORE morphology.
        #
        # This prevents morphology from connecting/growing
        # black pixels from one ROI into another ROI.
        # ----------------------------------------------------

        roi_mask = clean_black[
            y1:y2,
            x1:x2
        ].copy()

        if roi_mask.size == 0:
            continue

        roi_area = (
            roi_mask.shape[0]
            *
            roi_mask.shape[1]
        )

        # ----------------------------------------------------
        # Morphology is now LOCAL to this ROI.
        # ----------------------------------------------------

        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (5, 5)
        )

        roi_mask = cv2.morphologyEx(
            roi_mask,
            cv2.MORPH_OPEN,
            kernel
        )

        roi_mask = cv2.morphologyEx(
            roi_mask,
            cv2.MORPH_CLOSE,
            kernel
        )

        # ----------------------------------------------------
        # Find contours ONLY inside this ROI.
        # ----------------------------------------------------

        contours, _ = cv2.findContours(
            roi_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        best = None

        for contour in contours:

            area = cv2.contourArea(
                contour
            )

            if area < BLACK_MIN_AREA:
                continue

            bx, by, bw, bh = cv2.boundingRect(
                contour
            )

            if (
                bw < BLACK_MIN_WIDTH
                or
                bh < BLACK_MIN_HEIGHT
            ):
                continue

            aspect = (
                bw /
                float(
                    max(
                        bh,
                        1
                    )
                )
            )

            # LEFT_1 / RIGHT_1 are wall ROIs.
            #
            # Their ROIs are intentionally narrow and tall.
            # A black wall filling most/all of the ROI can
            # therefore have a very small aspect ratio
            # (for example 105 / 340 ~= 0.31).
            #
            # Do NOT reject these wall contours because of
            # aspect ratio. The contour is already created
            # strictly inside this ROI, so the ROI itself
            # defines the valid detection area.
            #
            # Keep the original aspect-ratio filter unchanged
            # for LEFT_2, CENTER_BLACK and RIGHT_2.
            if label not in (
                "LEFT WALL",
                "RIGHT WALL"
            ):
                if not (
                    BLACK_MIN_ASPECT
                    <=
                    aspect
                    <=
                    BLACK_MAX_ASPECT
                ):
                    continue

            rectangularity = (
                area /
                float(
                    max(
                        bw * bh,
                        1
                    )
                )
            )

            if (
                rectangularity
                <
                BLACK_MIN_RECTANGULARITY
            ):
                continue

            roi_fill = (
                area /
                float(
                    max(
                        roi_area,
                        1
                    )
                )
            )

            if (
                roi_fill
                <
                BLACK_MIN_ROI_FILL
            ):
                continue

            score = (
                0.50
                *
                min(
                    area /
                    max(
                        roi_area * 0.20,
                        1
                    ),
                    1.0
                )
                +
                0.30
                *
                rectangularity
                +
                0.20
                *
                min(
                    bw /
                    max(
                        roi_mask.shape[1] * 0.50,
                        1
                    ),
                    1.0
                )
            )

            if (
                best is None
                or
                score > best[0]
            ):
                best = (
                    score,
                    contour.copy(),
                    area,
                    bx,
                    by,
                    bw,
                    bh,
                    rectangularity
                )

        if best is None:
            continue

        (
            score,
            contour,
            area,
            bx,
            by,
            bw,
            bh,
            rectangularity
        ) = best

        confidence = float(
            np.clip(
                score,
                0.0,
                1.0
            )
        )

        # Black walls use a lower confidence threshold so that
        # small genuine wall sections are not rejected simply
        # because they occupy a small part of the ROI.
        if confidence < BLACK_MIN_CONFIDENCE:
            continue

        # ----------------------------------------------------
        # Convert the selected contour from ROI-local
        # coordinates back to full-frame coordinates.
        #
        # It is still physically limited to this ROI.
        # ----------------------------------------------------

        contour[:, :, 0] += x1
        contour[:, :, 1] += y1

        detections.append({
            "name": label,
            "label": label,

            # Actual contour, not just a bounding rectangle.
            "contour": contour,

            "bbox": (
                x1 + bx,
                y1 + by,
                bw,
                bh
            ),

            "area": area,
            "confidence": confidence,
            "rectangularity": rectangularity,

            # Keep the ROI for debugging/verification.
            "roi": (
                x1,
                y1,
                x2,
                y2
            ),
        })

    return detections



# ============================================================
# BLACK PILLAR DETECTION
# ============================================================

def detect_black_pillars(
    black_mask,
    color_masks,
    allowed_mask
):

    x1, y1, x2, y2 = (
        PILLAR_ROI
    )


    crop = black_mask[
        y1:y2,
        x1:x2
    ]


    if crop.size == 0:

        return []


    colored = np.zeros_like(
        crop
    )


    for name in (
        "RED",
        "GREEN",
        "BLUE",
        "ORANGE",
        "MAGENTA"
    ):

        colored = cv2.bitwise_or(

            colored,

            color_masks[
                name
            ][
                y1:y2,
                x1:x2
            ]
        )


    mask = cv2.bitwise_and(

        crop,

        cv2.bitwise_not(
            colored
        )
    )


    kernel = cv2.getStructuringElement(

        cv2.MORPH_RECT,

        (5, 7)
    )


    mask = cv2.morphologyEx(

        mask,

        cv2.MORPH_CLOSE,

        kernel
    )


    mask = cv2.morphologyEx(

        mask,

        cv2.MORPH_OPEN,

        np.ones(
            (3, 3),
            np.uint8
        )
    )


    # --------------------------------------------------------
    # CRITICAL:
    #
    # Apply exclusion AGAIN after pillar morphology.
    #
    # Therefore robot/wire pixels CANNOT grow back.
    # --------------------------------------------------------

    mask = cv2.bitwise_and(

        mask,

        allowed_mask[
            y1:y2,
            x1:x2
        ]
    )


    contours, _ = cv2.findContours(

        mask,

        cv2.RETR_EXTERNAL,

        cv2.CHAIN_APPROX_SIMPLE
    )


    candidates = []


    for contour in contours:

        area = cv2.contourArea(
            contour
        )


        if (
            area <
            PILLAR_MIN_AREA
        ):

            continue


        bx, by, bw, bh = (
            cv2.boundingRect(
                contour
            )
        )


        if (
            bw <
            PILLAR_MIN_WIDTH
            or
            bh <
            PILLAR_MIN_HEIGHT
        ):

            continue


        aspect = (

            bh /
            float(
                max(
                    bw,
                    1
                )
            )
        )


        if not (
            PILLAR_MIN_ASPECT
            <=
            aspect
            <=
            PILLAR_MAX_ASPECT
        ):

            continue


        rectangularity = (

            area /
            float(
                max(
                    bw * bh,
                    1
                )
            )
        )


        if (
            rectangularity
            <
            PILLAR_MIN_RECTANGULARITY
        ):

            continue


        inside = np.zeros(
            (
                bh,
                bw
            ),
            dtype=np.uint8
        )


        shifted = (
            contour.copy()
        )


        shifted[
            :,
            :,
            0
        ] -= bx


        shifted[
            :,
            :,
            1
        ] -= by


        cv2.drawContours(

            inside,

            [shifted],

            -1,

            255,

            -1
        )


        contour_pixels = mask[

            by:
            by + bh,

            bx:
            bx + bw

        ][
            inside > 0
        ]


        if len(
            contour_pixels
        ) == 0:

            continue


        dark_ratio = (

            np.count_nonzero(
                contour_pixels
            )
            /
            float(
                len(
                    contour_pixels
                )
            )
        )


        if (
            dark_ratio
            <
            PILLAR_MIN_DARK_RATIO
        ):

            continue


        score = (

            0.40
            *
            min(
                area / 2500.0,
                1.0
            )

            +

            0.25
            *
            min(
                rectangularity / 0.75,
                1.0
            )

            +

            0.25
            *
            min(
                aspect / 3.0,
                1.0
            )

            +

            0.10
            *
            min(
                dark_ratio,
                1.0
            )
        )


        candidates.append({

            "name":
                "BLACK PILLAR",

            "label":
                "BLACK PILLAR",

            "bbox": (

                x1 + bx,

                y1 + by,

                bw,

                bh
            ),

            "area":
                area,

            "confidence":
                float(
                    np.clip(
                        score,
                        0.0,
                        1.0
                    )
                ),

            "rectangularity":
                rectangularity,

            "aspect":
                aspect,
        })


    candidates.sort(

        key=lambda d:
            d["confidence"],

        reverse=True
    )


    return candidates[
        :PILLAR_MAX_CANDIDATES
    ]


# ============================================================
# WALL / PILLAR DUPLICATE REMOVAL
# ============================================================

def bbox_iou(
    a,
    b
):

    ax, ay, aw, ah = a

    bx, by, bw, bh = b


    ax2 = ax + aw
    ay2 = ay + ah

    bx2 = bx + bw
    by2 = by + bh


    ix1 = max(
        ax,
        bx
    )

    iy1 = max(
        ay,
        by
    )


    ix2 = min(
        ax2,
        bx2
    )

    iy2 = min(
        ay2,
        by2
    )


    iw = max(
        0,
        ix2 - ix1
    )

    ih = max(
        0,
        iy2 - iy1
    )


    intersection = (
        iw * ih
    )


    union = (

        aw * ah
        +
        bw * bh
        -
        intersection
    )


    return (

        intersection /
        float(
            max(
                union,
                1
            )
        )
    )


def suppress_wall_duplicate_pillars(
    pillars,
    walls
):

    """
    Prevent one black wall from being reported
    simultaneously as a BLACK PILLAR.
    """

    kept = []


    for pillar in pillars:

        duplicate = any(

            bbox_iou(

                pillar[
                    "bbox"
                ],

                wall[
                    "bbox"
                ]
            )

            >=

            PILLAR_WALL_DUPLICATE_IOU

            for wall in walls
        )


        if not duplicate:

            kept.append(
                pillar
            )


    return kept


# ============================================================
# MASTER DETECTION
# ============================================================

def detect_all(
    frame
):

    hsv = cv2.cvtColor(

        frame,

        cv2.COLOR_BGR2HSV
    )


    lab = cv2.cvtColor(

        frame,

        cv2.COLOR_BGR2LAB
    )


    # --------------------------------------------------------
    # MASTER ALLOWED AREA
    # --------------------------------------------------------

    allowed_mask = (
        build_allowed_detection_mask(
            frame.shape
        )
    )


    # --------------------------------------------------------
    # CREATE MASKS
    # --------------------------------------------------------

    masks = make_color_masks(

        hsv,

        lab,

        allowed_mask
    )


    # --------------------------------------------------------
    # --------------------------------------------------------
    # DETECTION AREA
    # --------------------------------------------------------
    # No polygon limits the detection area.
    # Detection uses the full frame, subject only to the
    # hard exclusion ROIs in allowed_mask.

    main_mask = allowed_mask

    detections = []


    # --------------------------------------------------------
    # COLOUR DETECTION
    # --------------------------------------------------------

    for color_name in (

        "RED",

        "GREEN",

        "BLUE",

        "ORANGE",

        "MAGENTA"

    ):

        masked = cv2.bitwise_and(

            masks[
                color_name
            ],

            main_mask
        )


        # Orange and blue only matter
        # inside their dedicated ROI.

        if color_name in (
            "ORANGE",
            "BLUE"
        ):

            orange_blue_mask = (
                rectangle_mask(
                    frame.shape,
                    ORANGE_BLUE_ROI
                )
            )


            masked = cv2.bitwise_and(

                masked,

                orange_blue_mask
            )


        result = detect_color(

            hsv,

            lab,

            masked,

            color_name
        )


        if result is not None:

            detections.append(
                result
            )


    # --------------------------------------------------------
    # BLACK WALLS
    # --------------------------------------------------------

    black_detections = (
        detect_black_walls(

            masks[
                "BLACK"
            ],

            masks,

            allowed_mask
        )
    )


    # --------------------------------------------------------
    # BLACK PILLARS
    # --------------------------------------------------------

    pillar_detections = (
        detect_black_pillars(

            masks[
                "BLACK"
            ],

            masks,

            allowed_mask
        )
    )


    # Stop same wall being called a pillar.

    pillar_detections = (
        suppress_wall_duplicate_pillars(

            pillar_detections,

            black_detections
        )
    )


    return (

        detections,

        black_detections,

        pillar_detections,

        masks
    )


# ============================================================
# DRAW ROI
# ============================================================

def draw_roi(
    frame,
    roi,
    label,
    color=(0, 255, 255),
    thickness=2
):

    x1, y1, x2, y2 = roi


    cv2.rectangle(

        frame,

        (
            x1,
            y1
        ),

        (
            x2 - 1,
            y2 - 1
        ),

        color,

        thickness
    )


    cv2.putText(

        frame,

        label,

        (
            x1 + 3,
            max(
                12,
                y1 + 14
            )
        ),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.35,

        color,

        1,

        cv2.LINE_AA
    )


# ============================================================
# DRAW DETECTIONS
# ============================================================

def annotate(
    frame,
    color_detections,
    black_detections,
    pillar_detections
):

    output = frame.copy()


    # --------------------------------------------------------
    # ALL EXISTING ROIs
    # --------------------------------------------------------

    for roi, label in (

        (
            LEFT_1_ROI,
            "L"
        ),

        (
            LEFT_2_ROI,
            "LI"
        ),

        (
            RIGHT_1_ROI,
            "R"
        ),

        (
            RIGHT_2_ROI,
            "RI"
        ),

        (
            CENTER_BLACK_ROI,
            "C"
        ),

    ):

        draw_roi(
            output,
            roi,
            label
        )


    # --------------------------------------------------------
    # ORANGE / BLUE ROI
    # --------------------------------------------------------

    draw_roi(

        output,

        ORANGE_BLUE_ROI,

        "O/B",

        (
            255,
            255,
            0
        ),

        1
    )


    # --------------------------------------------------------
    # PILLAR SEARCH ROI
    # --------------------------------------------------------
# 
#     draw_roi(
# 
#         output,
# 
#         PILLAR_ROI,
# 
#         "PILLAR SEARCH",
# 
#         (
#             180,
#             180,
#             180
#         ),
# 
#         1
#     )
# 

    # --------------------------------------------------------
    # ROBOT EXCLUSION
    # --------------------------------------------------------

    draw_roi(

        output,

        ROBOT_EXCLUSION_ROI,

        "ROBOT EXCL",

        (
            170,
            170,
            170
        ),

        1
    )


    # --------------------------------------------------------
    # BOTTOM-RIGHT WIRE EXCLUSION
    # --------------------------------------------------------

    draw_roi(

        output,

        WIRE_EXCLUSION_ROI,

        "WIRE EXCL",

        (
            170,
            170,
            170
        ),

        1
    )


    # --------------------------------------------------------
    # TOP EXCLUSION / STATUS STRIP
    # --------------------------------------------------------

    cv2.rectangle(

        output,

        (
            0,
            0
        ),

        (
            WIDTH - 1,
            TOP_BLACK_HEIGHT - 1
        ),

        (
            0,
            0,
            0
        ),

        -1
    )


    contour_colors = {

        "RED":
            (
                0,
                0,
                255
            ),

        "GREEN":
            (
                0,
                255,
                0
            ),

        "BLUE":
            (
                255,
                0,
                0
            ),

        "ORANGE":
            (
                0,
                165,
                255
            ),

        "MAGENTA":
            (
                255,
                0,
                255
            ),
    }


    # --------------------------------------------------------
    # COLOUR DETECTIONS
    # --------------------------------------------------------

    for d in color_detections:

        x, y, w, h = (
            d[
                "bbox"
            ]
        )


        draw_color = (
            contour_colors.get(

                d[
                    "color"
                ],

                (
                    255,
                    255,
                    255
                )
            )
        )


        overlay = (
            output.copy()
        )


        cv2.drawContours(

            overlay,

            [
                d[
                    "contour"
                ]
            ],

            -1,

            draw_color,

            -1
        )


        output = cv2.addWeighted(

            overlay,

            0.18,

            output,

            0.82,

            0
        )


        cv2.drawContours(

            output,

            [
                d[
                    "contour"
                ]
            ],

            -1,

            draw_color,

            2
        )


        cv2.rectangle(

            output,

            (
                x,
                y
            ),

            (
                x + w - 1,
                y + h - 1
            ),

            draw_color,

            1
        )


        label = (

            f'{d["color"]} '
            f'{d["confidence"] * 100:.0f}%'
        )


        cv2.putText(

            output,

            label,

            (
                x,

                max(
                    15,
                    y - 4
                )
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.48,

            draw_color,

            1,

            cv2.LINE_AA
        )


    # --------------------------------------------------------
    # --------------------------------------------------------
    # BLACK WALL DETECTIONS
    # --------------------------------------------------------

    for d in black_detections:

        contour = d.get(
            "contour"
        )

        if contour is None:
            continue

        # Draw ONLY the contour found inside that ROI.
        # Never draw one rectangle around multiple ROIs.
        cv2.drawContours(
            output,
            [contour],
            -1,
            (
                0,
                255,
                255
            ),
            2
        )

        x, y, w, h = (
            d["bbox"]
        )

        label = (
            f'{d["name"]} '
            f'{d["confidence"] * 100:.0f}%'
        )

        cv2.putText(
            output,
            label,
            (
                x,
                max(
                    15,
                    y - 4
                )
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.40,
            (
                0,
                255,
                255
            ),
            1
        )


    # BLACK PILLAR DETECTIONS
    # --------------------------------------------------------

    for d in pillar_detections:

        x, y, w, h = (
            d[
                "bbox"
            ]
        )


        cv2.rectangle(

            output,

            (
                x,
                y
            ),

            (
                x + w - 1,
                y + h - 1
            ),

            (
                0,
                255,
                255
            ),

            2
        )


        label = (

            f'BLACK PILLAR '
            f'{d["confidence"] * 100:.0f}%'
        )


        cv2.putText(

            output,

            label,

            (
                x,

                max(
                    15,
                    y - 5
                )
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.40,

            (
                0,
                255,
                255
            ),

            1,

            cv2.LINE_AA
        )


    return output


# ============================================================
# STATUS
# ============================================================

def draw_status(
    frame,
    color_detections,
    black_detections,
    pillar_detections,
    fps
):

    output = frame.copy()


    if color_detections:

        objects = ", ".join(

            d[
                "color"
            ]

            for d in
            color_detections
        )


    else:

        objects = "NONE"


    all_black = (

        list(
            black_detections
        )

        +

        list(
            pillar_detections
        )
    )


    if all_black:

        black = ", ".join(

            d.get(
                "name",
                "BLACK"
            )

            for d in
            all_black
        )


    else:

        black = "NONE"


    cv2.putText(

        output,

        (
            f"FPS: {fps:.1f}   "
            f"OBJECTS: {objects}"
        ),

        (
            5,
            18
        ),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.43,

        (
            255,
            255,
            255
        ),

        1,

        cv2.LINE_AA
    )


    cv2.putText(

        output,

        f"BLACK: {black}",

        (
            5,
            37
        ),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.38,

        (
            255,
            255,
            255
        ),

        1,

        cv2.LINE_AA
    )


    cv2.putText(

        output,

        (
            "Q/ESC quit | "
            "M masks | "
            "S screenshot"
        ),

        (
            5,
            55
        ),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.30,

        (
            220,
            220,
            220
        ),

        1,

        cv2.LINE_AA
    )


    return output


# ============================================================
# MASK DISPLAY
# ============================================================

def create_mask_display(
    masks
):

    display = np.zeros(
        (
            HEIGHT,
            WIDTH,
            3
        ),
        dtype=np.uint8
    )


    display[
        masks["RED"] > 0
    ] = (
        0,
        0,
        255
    )


    display[
        masks["GREEN"] > 0
    ] = (
        0,
        255,
        0
    )


    display[
        masks["BLUE"] > 0
    ] = (
        255,
        0,
        0
    )


    display[
        masks["ORANGE"] > 0
    ] = (
        0,
        165,
        255
    )


    display[
        masks["MAGENTA"] > 0
    ] = (
        255,
        0,
        255
    )


    display[
        masks["BLACK"] > 0
    ] = (
        255,
        255,
        255
    )


    return display


# ============================================================
# OBSTACLE PROGRAM COMPATIBILITY API
# ============================================================
#
# The detection engine above is the new vision system.
# These helpers ONLY adapt its output to the data shape expected by the
# existing obstacle controller. They do not change detection thresholds,
# ROIs, exclusions, scoring, or obstacle steering decisions.

WHITE = (255, 255, 255)
YELLOW = (0, 255, 255)

DRAW_COLORS = {
    "RED": (0, 0, 255),
    "GREEN": (0, 255, 0),
    "BLUE": (255, 0, 0),
    "ORANGE": (0, 165, 255),
    "MAGENTA": (255, 0, 255),
}

# Map the new vision's black-wall names to the exact ROI names used by
# the existing obstacle logic.
OBSTACLE_BLACK_ROI = {
    "LEFT WALL": "LEFT_1",
    "LEFT INNER": "LEFT_2",
    "CENTER BLACK": "CENTER_BLACK",
    "RIGHT INNER": "RIGHT_2",
    "RIGHT WALL": "RIGHT_1",
    "CLOSE BLACK": "CLOSE_BLACK",
}


def _with_xywh(d):
    """Convert new-vision bbox data to the old controller's fields."""
    x, y, w, h = d["bbox"]
    out = dict(d)
    out["x"] = int(x)
    out["y"] = int(y)
    out["w"] = int(w)
    out["h"] = int(h)
    out["cx"] = float(x + w / 2.0)
    out["cy"] = float(y + h / 2.0)
    return out


def largest_detection(items):
    """Return the largest detection by contour area."""
    if not items:
        return None
    return max(items, key=lambda d: d.get("area", 0))


def draw_target(frame, point, color, label=None):
    """Controller-side visualization helper."""
    x, y = int(point[0]), int(point[1])
    cv2.circle(frame, (x, y), 5, color, -1)
    if label:
        cv2.putText(
            frame,
            str(label),
            (x + 6, max(15, y - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            color,
            1,
            cv2.LINE_AA,
        )


def obstacle_detections(frame):
    """
    Run the NEW vision engine and return both:

    1. detections: compatibility dictionary consumed by the existing
       obstacle controller.
    2. raw new-vision detections/masks for the new vision overlay.

    No detection decision is made here; detect_all() remains the source
    of truth.
    """
    color_detections, black_walls, pillar_detections, masks = detect_all(frame)

    detections = {
        "RED": [],
        "GREEN": [],
        "BLUE": [],
        "ORANGE": [],
        "MAGENTA": [],
        "BLACK": [],
    }

    for d in color_detections:
        color_name = d.get("color")
        if color_name in detections:
            detections[color_name].append(_with_xywh(d))

    # Only BLACK WALL detections enter the old BLACK channel.
    # Pillars remain available for the new vision overlay but are NOT
    # introduced into the existing avoidance strategy.
    for d in black_walls:
        out = _with_xywh(d)
        out["roi"] = OBSTACLE_BLACK_ROI.get(d.get("name"), None)
        detections["BLACK"].append(out)

    return (
        detections,
        color_detections,
        black_walls,
        pillar_detections,
        masks,
    )

# ============================================================
# PUBLIC API
# ============================================================

def process_frame(
    frame
):

    """
    Returns:

        color_detections
        black_detections
        pillar_detections
        masks
    """

    return detect_all(
        frame
    )


def process_frame_with_overlay(
    frame
):

    (
        color_detections,

        black_detections,

        pillar_detections,

        masks

    ) = detect_all(
        frame
    )


    output = annotate(

        frame,

        color_detections,

        black_detections,

        pillar_detections
    )


    return (

        output,

        color_detections,

        black_detections,

        pillar_detections,

        masks
    )


# ============================================================
# MAIN
# ============================================================

def main():

    cap = start_camera()


    show_masks = False


    previous_time = (
        time.time()
    )


    fps = 0.0


    print(
        "=" * 64
    )


    print(
        "WRO FINAL COMBINED VISION"
    )


    print(
        "640x360 | "
        "HARD ROBOT + "
        "BOTTOM-RIGHT WIRE EXCLUSIONS"
    )


    print(
        "=" * 64
    )


    try:

        while True:

            frame = (
                cap.capture_array()
            )


            if frame is None:

                print(
                    "ERROR: "
                    "Could not read frame."
                )

                break


            # Preserve the conversion used
            # by the current working version.

            frame = cv2.cvtColor(

                frame,

                cv2.COLOR_RGB2BGR
            )


            if (
                frame.shape[1] != WIDTH
                or
                frame.shape[0] != HEIGHT
            ):

                frame = cv2.resize(

                    frame,

                    (
                        WIDTH,
                        HEIGHT
                    ),

                    interpolation=
                        cv2.INTER_LINEAR
                )


            (
                color_detections,

                black_detections,

                pillar_detections,

                masks

            ) = detect_all(
                frame
            )


            output = annotate(

                frame,

                color_detections,

                black_detections,

                pillar_detections
            )


            now = time.time()


            dt = (
                now
                -
                previous_time
            )


            previous_time = now


            if dt > 0:

                instant_fps = (
                    1.0 / dt
                )


                if fps == 0.0:

                    fps = instant_fps


                else:

                    fps = (

                        0.90 * fps
                        +
                        0.10 * instant_fps
                    )


            output = draw_status(

                output,

                color_detections,

                black_detections,

                pillar_detections,

                fps
            )


            if show_masks:

                cv2.imshow(

                    "Detection Masks",

                    create_mask_display(
                        masks
                    )
                )


            cv2.imshow(

                "WRO Vision - Raspberry Pi",

                output
            )


            key = (
                cv2.waitKey(1)
                &
                0xFF
            )


            if (
                key == ord("q")
                or
                key == 27
            ):

                break


            if key == ord("m"):

                show_masks = (
                    not show_masks
                )


                if not show_masks:

                    try:

                        cv2.destroyWindow(
                            "Detection Masks"
                        )


                    except cv2.error:

                        pass


            if key == ord("s"):

                filename = (

                    "wro_test_"

                    +

                    time.strftime(
                        "%Y%m%d_%H%M%S"
                    )

                    +

                    ".jpg"
                )


                cv2.imwrite(
                    filename,
                    output
                )
                print(
                    f"Screenshot saved: "
                    f"{filename}"
                )
    finally:
        cap.stop()
        cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
