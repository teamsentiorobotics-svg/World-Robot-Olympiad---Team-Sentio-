from picamera2 import Picamera2
import cv2
import numpy as np

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)

picam2.configure(config)
picam2.start()

kernel = np.ones((5, 5), np.uint8)

while True:

    # Capture frame from Pi Camera
    frame = picam2.capture_array()

    # Convert RGB to BGR because OpenCV uses BGR
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_ranges = {

        "Blue": {
            "lower": np.array([85, 50, 50]),
            "upper": np.array([140, 255, 255])
        },

        "Green": {
            "lower": np.array([35, 40, 40]),
            "upper": np.array([90, 255, 255])
        },

        "Orange": {
            "lower": np.array([5, 80, 80]),
            "upper": np.array([25, 255, 255])
        },

        "Pink": {
            "lower": np.array([135, 40, 40]),
            "upper": np.array([175, 255, 255])
        }

    }

    best_area = 0
    best_contour = None
    best_color = None
    best_box_color = None

    # ----------------------------
    # Red (two HSV ranges)
    # ----------------------------

    red_mask1 = cv2.inRange(
        hsv,
        np.array([0, 70, 50]),
        np.array([12, 255, 255])
    )

    red_mask2 = cv2.inRange(
        hsv,
        np.array([165, 70, 50]),
        np.array([180, 255, 255])
    )

    masks = {
        "Red": red_mask1 + red_mask2
    }

    for color_name, values in color_ranges.items():

        masks[color_name] = cv2.inRange(
            hsv,
            values["lower"],
            values["upper"]
        )

    for color_name, mask in masks.items():

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:

            area = cv2.contourArea(cnt)

            if area > 1500 and area > best_area:

                best_area = area
                best_contour = cnt
                best_color = color_name

                if color_name == "Red":
                    best_box_color = (0, 0, 255)
                elif color_name == "Blue":
                    best_box_color = (255, 0, 0)
                elif color_name == "Green":
                    best_box_color = (0, 255, 0)
                elif color_name == "Orange":
                    best_box_color = (0, 165, 255)
                elif color_name == "Pink":
                    best_box_color = (255, 0, 255)

    if best_contour is not None:

        x, y, w, h = cv2.boundingRect(best_contour)

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            best_box_color,
            3
        )

        cv2.putText(
            frame,
            best_color,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            best_box_color,
            2
        )

    cv2.imshow("Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
picam2.stop()