import cv2
import numpy as np
import os
import csv

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Configuration - Change this path to your input image
INPUT_IMAGE_PATH = input("Enter the path to input image (or press Enter for default): ").strip()
if not INPUT_IMAGE_PATH:
    INPUT_IMAGE_PATH = os.path.join(script_dir, "test_image.jpg")
    print(f"Using default path: {INPUT_IMAGE_PATH}")

# Template paths (relative to script directory)
SUNGLASSES_PATH = os.path.join(script_dir, "templates", "sunglasses_template.png")
MOUSTACHE_PATH = os.path.join(script_dir, "templates", "moustache_template.png")
OUTPUT_CSV_PATH = os.path.join(script_dir, "output.csv")
OUTPUT_IMAGE_PATH = os.path.join(script_dir, "output_filtered.jpg")

# Load input image
input_image = cv2.imread(INPUT_IMAGE_PATH, cv2.IMREAD_COLOR)
if input_image is None:
    print(f"Error: Could not load input image from: {INPUT_IMAGE_PATH}")
    print("Please provide a valid image path.")
    exit(1)

print(f"✓ Loaded input image: {INPUT_IMAGE_PATH}")

# Load templates with alpha channel
sunglasses_template = cv2.imread(SUNGLASSES_PATH, -1)
if sunglasses_template is None:
    print(f"⚠ Warning: Could not load sunglasses template from: {SUNGLASSES_PATH}")
    print("Sunglasses filter will be skipped.")

moustache_template = cv2.imread(MOUSTACHE_PATH, -1)
if moustache_template is None:
    print(f"⚠ Warning: Could not load moustache template from: {MOUSTACHE_PATH}")
    print("Moustache filter will be skipped.")

# Load Haar cascade files for face and facial keypoint detection
face_cascade = cv2.CascadeClassifier("models/haarcascade_frontalface_alt.xml")
eye_cascade = cv2.CascadeClassifier("models/haarcascade_eye.xml") 
nose_cascade = cv2.CascadeClassifier("models/haarcascade_mcs_nose.xml")

# Validate cascade files loaded
if face_cascade.empty():
    print("Error: Could not load haarcascade_frontalface_alt.xml")
    exit(1)
if eye_cascade.empty():
    print("⚠ Warning: Could not load haarcascade_eye.xml")
if nose_cascade.empty():
    print("⚠ Warning: Could not load haarcascade_mcs_nose.xml")

def overlay_transparent(background, overlay, x, y):
    """
    Overlay a transparent image (with alpha channel) on a background image.
    
    Args:
        background: Background image (BGR)
        overlay: Overlay image (BGRA with alpha channel)
        x, y: Position to place overlay
    
    Returns:
        Modified background image
    """
    overlay_height, overlay_width = overlay.shape[:2]
    background_height, background_width = background.shape[:2]
    
    # Boundary checking
    if x < 0 or y < 0 or x + overlay_width > background_width or y + overlay_height > background_height:
        # Crop overlay to fit within boundaries
        x_start = max(0, x)
        y_start = max(0, y)
        x_end = min(background_width, x + overlay_width)
        y_end = min(background_height, y + overlay_height)
        
        overlay_x_start = max(0, -x)
        overlay_y_start = max(0, -y)
        overlay_x_end = overlay_x_start + (x_end - x_start)
        overlay_y_end = overlay_y_start + (y_end - y_start)
        
        overlay = overlay[overlay_y_start:overlay_y_end, overlay_x_start:overlay_x_end]
        x, y = x_start, y_start
        overlay_height, overlay_width = overlay.shape[:2]
    
    if overlay.shape[2] == 4:  # Has alpha channel
        # Split the overlay into color and alpha channels
        overlay_bgr = overlay[:, :, :3]
        overlay_alpha = overlay[:, :, 3:] / 255.0
        
        # Get the region of interest from background
        roi = background[y:y+overlay_height, x:x+overlay_width]
        
        # Blend the images using alpha channel
        blended = (overlay_alpha * overlay_bgr + (1 - overlay_alpha) * roi).astype(np.uint8)
        background[y:y+overlay_height, x:x+overlay_width] = blended
    else:  # No alpha channel, just overlay directly
        background[y:y+overlay_height, x:x+overlay_width] = overlay
    
    return background

# Detect faces in the input image
print("\nDetecting faces and applying filters...")
faces = face_cascade.detectMultiScale(input_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

if len(faces) == 0:
    print("⚠ No faces detected in the image!")
else:
    print(f"✓ Detected {len(faces)} face(s)")

# Prepare data for CSV
data = []
filters_applied = 0

for (x, y, w, h) in faces:
    # Detect eyes and nose in the face region
    roi_gray = input_image[y:y+h, x:x+w]
    
    # Detect eyes
    if not eye_cascade.empty() and sunglasses_template is not None:
        eyes = eye_cascade.detectMultiScale(roi_gray)
        
        # Overlay sunglasses on detected eyes
        for (ex, ey, ew, eh) in eyes:
            # Scale sunglasses to be wider than single eye for more natural look
            sunglasses_width = int(ew * 2.5)
            sunglasses_height = int(eh * 1.2)
            
            # Center sunglasses over both eyes
            sunglasses_x = x + ex - int(ew * 0.75)
            sunglasses_y = y + ey - int(eh * 0.1)
            
            sunglasses_resized = cv2.resize(sunglasses_template, (sunglasses_width, sunglasses_height))
            input_image = overlay_transparent(input_image, sunglasses_resized, sunglasses_x, sunglasses_y)
            
            data.append({'x': sunglasses_x, 'y': sunglasses_y, 'type': 'sunglasses'})
            filters_applied += 1
            break  # Only apply sunglasses once per face
    
    # Detect nose
    if not nose_cascade.empty() and moustache_template is not None:
        nose = nose_cascade.detectMultiScale(roi_gray)
        
        # Overlay moustache on detected nose
        for (nx, ny, nw, nh) in nose:
            # Scale moustache appropriately
            moustache_width = int(nw * 2)
            moustache_height = int(nh * 1.5)
            
            # Position moustache below nose
            moustache_x = x + nx - int(nw * 0.5)
            moustache_y = y + ny + int(nh * 0.5)
            
            moustache_resized = cv2.resize(moustache_template, (moustache_width, moustache_height))
            input_image = overlay_transparent(input_image, moustache_resized, moustache_x, moustache_y)
            
            data.append({'x': moustache_x, 'y': moustache_y, 'type': 'moustache'})
            filters_applied += 1
            break  # Only apply moustache once per face

print(f"✓ Applied {filters_applied} filter(s)")
# Write data to CSV
if len(data) > 0:
    try:
        with open(OUTPUT_CSV_PATH, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['x', 'y', 'type'])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f"✓ CSV file saved to: {OUTPUT_CSV_PATH}")
    except Exception as e:
        print(f"⚠ Warning: Could not save CSV file: {e}")
else:
    print("⚠ No filters applied, CSV file not created.")

# Save the modified image
try:
    cv2.imwrite(OUTPUT_IMAGE_PATH, input_image)
    print(f"✓ Modified image saved to: {OUTPUT_IMAGE_PATH}")
except Exception as e:
    print(f"⚠ Warning: Could not save output image: {e}")

# Display the modified image
print("\nDisplaying modified image. Press any key to close...")
cv2.imshow('Modified Image', input_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("\n✓ Processing complete!")
