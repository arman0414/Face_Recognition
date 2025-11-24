import cv2
import numpy as np
import os

# Constants
SAMPLE_RATE = 10  # Collect every 10th frame
FACE_SIZE = 100   # Standardized face size
FACE_PADDING = 10 # Pixel offset for face crop
SCALE_FACTOR = 1.3
MIN_NEIGHBORS = 5

# Get dataset path relative to script location
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, 'face_dataset')

# Create dataset directory if it doesn't exist
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)
    print(f"Created dataset directory: {dataset_path}")

# Get person name with validation
file_name = input("Enter the name of the person: ").strip()
while not file_name or not file_name.replace('_', '').isalnum():
    print("Error: Name must contain only letters, numbers, and underscores")
    file_name = input("Enter the name of the person: ").strip()

# Init Camera
cap = cv2.VideoCapture(0)

# Validate camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera. Please check your camera connection.")
    exit(1)

print("Camera initialized successfully!")
print("Press 'q' to quit and save data")

# Face Detection
face_cascade = cv2.CascadeClassifier("models/haarcascade_frontalface_alt.xml")

# Validate cascade file loaded
if face_cascade.empty():
    print("Error: Could not load haarcascade_frontalface_alt.xml")
    cap.release()
    exit(1)

skip = 0
face_data = []
face_section = None  # Define face_section outside the loop

while True:
    ret, frame = cap.read()

    if not ret:
        print("Warning: Failed to read frame from camera")
        continue
    
    # Get frame dimensions for boundary checking
    frame_height, frame_width = frame.shape[:2]
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    faces = face_cascade.detectMultiScale(frame, SCALE_FACTOR, MIN_NEIGHBORS)
    
    if len(faces) > 0:
        faces = sorted(faces, key=lambda f: f[2] * f[3])  # Sort the faces based on area (f[2]*f[3])
        print(f"Detected {len(faces)} face(s)")

        for face in faces[-1:]:  # Get the largest face
            x, y, w, h = face
            center = (x + w // 2, y + h // 2)
            radius = max(w, h) // 2
            cv2.circle(frame, center, radius, (255, 0, 0), 2)

            # Crop required face: Region of Interest with boundary checking
            y_start = max(0, y - FACE_PADDING)
            y_end = min(frame_height, y + h + FACE_PADDING)
            x_start = max(0, x - FACE_PADDING)
            x_end = min(frame_width, x + w + FACE_PADDING)
            
            face_section = frame[y_start:y_end, x_start:x_end]
            
            # Only process if face section is valid
            if face_section.size > 0:
                face_section = cv2.resize(face_section, (FACE_SIZE, FACE_SIZE))
                skip += 1
                if skip % SAMPLE_RATE == 0:
                    face_data.append(face_section)
                    print(f"Collected {len(face_data)} samples")

    cv2.imshow("Video_Frame", frame)
    if face_section is not None:
        cv2.imshow("Face Section", face_section)

    key_pressed = cv2.waitKey(1) & 0xFF  # 8 bit integer
    if key_pressed == ord('q'):
        break

# Convert face list to numpy array
if len(face_data) > 0:
    face_data = np.asarray(face_data)
    face_data = face_data.reshape((face_data.shape[0], -1))
    print(f"\nData shape: {face_data.shape}")
    
    # Save this data into the file system
    output_file = os.path.join(dataset_path, file_name + '.npy')
    np.save(output_file, face_data)
    print(f"✓ Successfully saved {len(face_data)} samples to: {output_file}")
else:
    print("\n⚠ No data collected! Make sure your face is visible to the camera.")

cap.release()
cv2.destroyAllWindows()
print("Camera released and windows closed.")
