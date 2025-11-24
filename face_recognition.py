import cv2
import numpy as np  
import os

# Constants
K_NEIGHBORS = 5       # Number of neighbors for KNN
FACE_SIZE = 100       # Standardized face size
FACE_PADDING = 10     # Pixel offset for face crop
SCALE_FACTOR = 1.3
MIN_NEIGHBORS = 5

# KNN Algorithm
def distance(v1, v2):
    """Calculate Euclidean distance between two vectors"""
    return np.sqrt(((v1 - v2) ** 2).sum())

def knn(train, test, k=K_NEIGHBORS):
    """
    K-Nearest Neighbors classifier
    
    Args:
        train: Training data with labels in last column
        test: Test sample to classify
        k: Number of neighbors to consider
    
    Returns:
        Predicted label
    """
    dist = []
    
    for i in range(train.shape[0]):
        # Get the vector and label
        ix = train[i, :-1]
        iy = train[i, -1]
        # Compute the distance from test point
        d = distance(test, ix)
        dist.append([d, iy])
    # Sort based on distance and get top k
    dk = sorted(dist, key=lambda x: x[0])[:k]
    # Retrieve only the labels
    labels = np.array(dk)[:, -1]
    
    # Get frequencies of each label
    output = np.unique(labels, return_counts=True)
    # Find max frequency and corresponding label
    index = np.argmax(output[1])
    return output[0][index]

# Get dataset path relative to script location
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, 'face_dataset')

# Validate dataset directory exists
if not os.path.exists(dataset_path):
    print(f"Error: Dataset directory not found: {dataset_path}")
    print("Please run face_data_collect.py first to collect training data.")
    exit(1)

# Init camera
cap = cv2.VideoCapture(0)

# Validate camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera. Please check your camera connection.")
    exit(1)

print("Camera initialized successfully!")

# Face Detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

# Validate cascade file loaded
if face_cascade.empty():
    print("Error: Could not load haarcascade_frontalface_alt.xml")
    cap.release()
    exit(1)

face_data = []
labels = []
class_id = 0  # Labels for the given file
names = {}    # Mapping between id and name

# Load all training data
print(f"\nLoading training data from: {dataset_path}")
for fx in os.listdir(dataset_path):
    if fx.endswith('.npy'):
        # Create a mapping between class_id and name
        names[class_id] = fx[:-4]
        file_path = os.path.join(dataset_path, fx)
        
        try:
            data_item = np.load(file_path)
            print(f"✓ Loaded {fx}: {data_item.shape[0]} samples")
            face_data.append(data_item)
            
            # Create labels for the class
            target = class_id * np.ones((data_item.shape[0],))
            class_id += 1
            labels.append(target)
        except Exception as e:
            print(f"⚠ Error loading {fx}: {e}")
            continue

# Validate that we have training data
if len(face_data) == 0:
    print("\nError: No training data found!")
    print("Please run face_data_collect.py first to collect face samples.")
    cap.release()
    exit(1)

# Concatenate all data and labels
face_dataset = np.concatenate(face_data, axis=0)
face_labels = np.concatenate(labels, axis=0).reshape((-1, 1))
training_set = np.concatenate((face_dataset, face_labels), axis=1)

print(f"\n✓ Training set created: {training_set.shape}")
print(f"✓ Loaded {len(names)} person(s): {', '.join(names.values())}")
print("\nPress 'q' to quit")

# Testing - Real-time face recognition
while True:
    ret, frame = cap.read()
    if not ret:
        print("Warning: Failed to read frame from camera")
        continue
    
    # Get frame dimensions for boundary checking
    frame_height, frame_width = frame.shape[:2]
    
    faces = face_cascade.detectMultiScale(frame, SCALE_FACTOR, MIN_NEIGHBORS)
    
    for face in faces:
        x, y, w, h = face
        
        # Boundary checking for face crop
        y_start = max(0, y - FACE_PADDING)
        y_end = min(frame_height, y + h + FACE_PADDING)
        x_start = max(0, x - FACE_PADDING)
        x_end = min(frame_width, x + w + FACE_PADDING)
        
        face_section = frame[y_start:y_end, x_start:x_end]
        
        # Only process if face section is valid
        if face_section.size > 0:
            face_section = cv2.resize(face_section, (FACE_SIZE, FACE_SIZE))
            
            # Predict label using KNN
            output = knn(training_set, face_section.flatten())
            pred_name = names[int(output)]
            
            # Display prediction
            cv2.putText(frame, pred_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
    
    cv2.imshow("Face Recognition", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()  # Release camera
cv2.destroyAllWindows()
print("Camera released and windows closed.")