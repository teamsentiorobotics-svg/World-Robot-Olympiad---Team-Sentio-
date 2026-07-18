import cv2
import numpy as np

# 1. Initialize your laptop's default webcam (0 is usually built-in, 1 for external USB)
cap = cv2.VideoCapture(0)

# Set resolution to match the intended Pi configuration
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Laptop camera active. Hold up red or green vertical objects!")
print("Press 'q' to close the program.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame from laptop camera.")
        break

    # 2. Convert laptop video frame to HSV space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 3. Define Precise Color Bounds (Calibrated for standard indoor/office lighting)
    # Green Color Range
    lower_green = np.array([40, 70, 40])
    upper_green = np.array([80, 255, 255])
    
    # Red Color Range (Splits across the 0/180 degree line in Hue)
    lower_red1 = np.array([0, 100, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 100, 50])
    upper_red2 = np.array([180, 255, 255])

    # 4. Generate the Color Masks
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # 5. Clean up background speckles and edge noise
    kernel = np.ones((5, 5), np.uint8)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)

    # 6. Process shapes and isolate vertical pillars
    def detect_pillars(mask, color_label, box_color):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000: # Pixel size threshold (raise if it detects small desk items)
                x, y, w, h = cv2.boundingRect(contour)
                
                #print(y)
                #print(w)
                #print(h)
                # PILLAR FILTER: Checks if the object is taller than it is wide
                aspect_ratio = float(h) / w
                if aspect_ratio > 1.2:
                    # Draw tracking box and label
                    cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
                    cv2.putText(frame, f"{color_label} Pillar", (x, y - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)
                    print("x - ",y)
    # Check the laptop feed for both target pillars
    detect_pillars(mask_green, "Green", (0, 255, 0))
    detect_pillars(mask_red, "Red", (0, 0, 255))

    # 7. Show live testing windows
    cv2.imshow("Laptop Pillar Tracker", frame)
    # Optional: uncomment to see what the computer actually sees in black & white
    # cv2.imshow("Red Mask debug", mask_red) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
