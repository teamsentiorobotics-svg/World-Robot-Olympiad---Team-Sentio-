import cv2
import numpy as np
from picamera2 import Picamera2

# ============================================================
# CAMERA SETTINGS
# ============================================================

WIDTH = 720
HEIGHT = 360
FPS = 60

# ============================================================
# INITIAL HSV VALUES
# ============================================================

ranges = {
    "RED1": {
        "lower": [0, 115, 65],
        "upper": [8, 255, 255],
    },
    "RED2": {
        "lower": [172, 115, 65],
        "upper": [180, 255, 255],
    },
    "GREEN": {
        "lower": [49, 56, 50],
        "upper": [71, 163, 150],
    },
    "ORANGE": {
        "lower": [12, 100, 100],
        "upper": [22, 255, 200],
    },
    "BLUE": {
        "lower": [100, 93, 81],
        "upper": [117, 227, 161],
    },
    "MAGENTA": {
        "lower": [161, 122, 72],
        "upper": [171, 241, 166],
    },
}

current_color = "RED1"
last_clicked_hsv = None

# Only colors selected by the user will be printed.
calibrated_colors = set()

# ============================================================
# CAMERA
# ============================================================

picam2 = Picamera2()

config = picam2.create_video_configuration(
    main={"size": (WIDTH, HEIGHT), "format": "BGR888"},
    controls={"FrameRate": FPS}
)

picam2.configure(config)
picam2.start()

# ============================================================
# HSV TRACKBARS
# ============================================================

cv2.namedWindow("HSV CALIBRATION", cv2.WINDOW_NORMAL)
cv2.resizeWindow("HSV CALIBRATION", WIDTH, HEIGHT)


def nothing(x):
    pass


cv2.createTrackbar("H MIN", "HSV CALIBRATION", 0, 180, nothing)
cv2.createTrackbar("H MAX", "HSV CALIBRATION", 180, 180, nothing)
cv2.createTrackbar("S MIN", "HSV CALIBRATION", 0, 255, nothing)
cv2.createTrackbar("S MAX", "HSV CALIBRATION", 255, 255, nothing)
cv2.createTrackbar("V MIN", "HSV CALIBRATION", 0, 255, nothing)
cv2.createTrackbar("V MAX", "HSV CALIBRATION", 255, 255, nothing)


def set_values():
    r = ranges[current_color]

    cv2.setTrackbarPos("H MIN", "HSV CALIBRATION", r["lower"][0])
    cv2.setTrackbarPos("S MIN", "HSV CALIBRATION", r["lower"][1])
    cv2.setTrackbarPos("V MIN", "HSV CALIBRATION", r["lower"][2])

    cv2.setTrackbarPos("H MAX", "HSV CALIBRATION", r["upper"][0])
    cv2.setTrackbarPos("S MAX", "HSV CALIBRATION", r["upper"][1])
    cv2.setTrackbarPos("V MAX", "HSV CALIBRATION", r["upper"][2])


def get_values():
    lower = [
        cv2.getTrackbarPos("H MIN", "HSV CALIBRATION"),
        cv2.getTrackbarPos("S MIN", "HSV CALIBRATION"),
        cv2.getTrackbarPos("V MIN", "HSV CALIBRATION"),
    ]

    upper = [
        cv2.getTrackbarPos("H MAX", "HSV CALIBRATION"),
        cv2.getTrackbarPos("S MAX", "HSV CALIBRATION"),
        cv2.getTrackbarPos("V MAX", "HSV CALIBRATION"),
    ]

    return lower, upper


def print_current_values():
    lower, upper = get_values()

    ranges[current_color]["lower"] = lower
    ranges[current_color]["upper"] = upper

    calibrated_colors.add(current_color)

    print("\n" + "=" * 65)
    print(f"CURRENT {current_color} HSV VALUES")
    print("=" * 65)

    print(
        f'{current_color}_LOWER = np.array({lower}, dtype=np.uint8)'
    )
    print(
        f'{current_color}_UPPER = np.array({upper}, dtype=np.uint8)'
    )

    print("-" * 65)

    if last_clicked_hsv is not None:
        print(
            f"LAST CLICKED PIXEL HSV = "
            f"[{last_clicked_hsv[0]}, {last_clicked_hsv[1]}, {last_clicked_hsv[2]}]"
        )

    print("=" * 65)


def print_all_values():
    # Save the currently adjusted color.
    lower, upper = get_values()
    ranges[current_color]["lower"] = lower
    ranges[current_color]["upper"] = upper

    # The current color counts as calibrated only if the user
    # explicitly pressed S for it.
    if current_color not in calibrated_colors:
        print("\nNo calibrated colors yet.")
        print("Press S after adjusting a color.")
        return

    print("\n" + "=" * 75)
    print("CALIBRATED HSV VALUES")
    print("=" * 75)

    for name in ranges:
        if name in calibrated_colors:
            r = ranges[name]

            print(
                f'{name}_LOWER = np.array({r["lower"]}, dtype=np.uint8)'
            )
            print(
                f'{name}_UPPER = np.array({r["upper"]}, dtype=np.uint8)'
            )
            print()

    print("=" * 75)

def mouse_callback(event, x, y, flags, param):
    global last_clicked_hsv

    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_frame = param

        if (
            hsv_frame is not None
            and 0 <= x < hsv_frame.shape[1]
            and 0 <= y < hsv_frame.shape[0]
        ):
            pixel = hsv_frame[y, x]

            last_clicked_hsv = [
                int(pixel[0]),
                int(pixel[1]),
                int(pixel[2]),
            ]

            print("\n" + "-" * 65)
            print(f"CLICKED PIXEL: X={x}, Y={y}")
            print(
                f"HSV = [{last_clicked_hsv[0]}, "
                f"{last_clicked_hsv[1]}, "
                f"{last_clicked_hsv[2]}]"
            )
            print(
                f"BGR = "
                f"{param_bgr[y, x].tolist()}"
            )
            print(f"CURRENT COLOR = {current_color}")
            print("-" * 65)


# Global BGR frame used only for terminal click information.
param_bgr = None

# Start with RED1 values.
set_values()

print("\n" + "=" * 75)
print("HSV CALIBRATION STARTED")
print("=" * 75)
print("1 = RED1")
print("2 = RED2")
print("3 = GREEN")
print("4 = ORANGE")
print("5 = BLUE")
print("6 = MAGENTA")
print()
print("LEFT CLICK  = print HSV value of clicked pixel in terminal")
print("S            = save/print THIS color's HSV values")
print("A / W        = print ONLY colors you calibrated")
print("Q / ESC      = quit")
print("=" * 75)

while True:

    frame = picam2.capture_array()

    # Convert RGB/BGR frame to HSV.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Current HSV range.
    lower = np.array(
        cv2.getTrackbarPos("H MIN", "HSV CALIBRATION"),
        dtype=np.uint8
    )

    h_min = cv2.getTrackbarPos("H MIN", "HSV CALIBRATION")
    h_max = cv2.getTrackbarPos("H MAX", "HSV CALIBRATION")
    s_min = cv2.getTrackbarPos("S MIN", "HSV CALIBRATION")
    s_max = cv2.getTrackbarPos("S MAX", "HSV CALIBRATION")
    v_min = cv2.getTrackbarPos("V MIN", "HSV CALIBRATION")
    v_max = cv2.getTrackbarPos("V MAX", "HSV CALIBRATION")

    lower = np.array([h_min, s_min, v_min], dtype=np.uint8)
    upper = np.array([h_max, s_max, v_max], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower, upper)

    # Mask preview.
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Display current color and values.
    display  = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    cv2.putText(
        display,
        f"COLOR: {current_color}",
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        display,
        f"H: {h_min}-{h_max}  S: {s_min}-{s_max}  V: {v_min}-{v_max}",
        (10, 52),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 255, 255),
        1,
    )

    # Put the mask on the right half.
    mask_small = cv2.resize(mask_bgr, (WIDTH // 2, HEIGHT // 2))

    display_small = cv2.resize(
        display,
        (WIDTH // 2, HEIGHT // 2)
    )

    combined = np.hstack((display_small, mask_small))

    cv2.imshow("HSV CALIBRATION", combined)

    # Update mouse callback with the CURRENT HSV frame.
    param_bgr = frame
    cv2.setMouseCallback(
        "HSV CALIBRATION",
        mouse_callback,
        hsv
    )

    key = cv2.waitKey(1) & 0xFF

    # --------------------------------------------------------
    # COLOR SELECTION
    # --------------------------------------------------------

    if key == ord("1"):
        ranges[current_color]["lower"], ranges[current_color]["upper"] = get_values()
        current_color = "RED1"
        set_values()
        print("\nSwitched to RED1")

    elif key == ord("2"):
        ranges[current_color]["lower"], ranges[current_color]["upper"] = get_values()
        current_color = "RED2"
        set_values()
        print("\nSwitched to RED2")

    elif key == ord("3"):
        ranges[current_color]["lower"], ranges[current_color]["upper"] = get_values()
        current_color = "GREEN"
        set_values()
        print("\nSwitched to GREEN")

    elif key == ord("4"):
        ranges[current_color]["lower"], ranges[current_color]["upper"] = get_values()
        current_color = "ORANGE"
        set_values()
        print("\nSwitched to ORANGE")

    elif key == ord("5"):
        ranges[current_color]["lower"], ranges[current_color]["upper"] = get_values()
        current_color = "BLUE"
        set_values()
        print("\nSwitched to BLUE")

    elif key == ord("6"):
        ranges[current_color]["lower"], ranges[current_color]["upper"] = get_values()
        current_color = "MAGENTA"
        set_values()
        print("\nSwitched to MAGENTA")

    # --------------------------------------------------------
    # PRINT CURRENT VALUES
    # --------------------------------------------------------

    elif key == ord("s"):
        print_current_values()

    # --------------------------------------------------------
    # PRINT ALL VALUES
    # --------------------------------------------------------

    elif key == ord("a") or key == ord("w"):
        print_all_values()

    # --------------------------------------------------------
    # QUIT
    # --------------------------------------------------------

    elif key == ord("q") or key == 27:
        break

# ============================================================
# CLEANUP
# ============================================================

# Save the final current color before quitting.
ranges[current_color]["lower"], ranges[current_color]["upper"] = get_values()

print_all_values()

cv2.destroyAllWindows()
picam2.stop()
