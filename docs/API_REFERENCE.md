# 📚 API Reference

Complete reference for all functions, classes, and modules in the Face Recognition System.

---

## Table of Contents
- [face_data_collect.py](#face_data_collectpy)
- [face_recognition.py](#face_recognitionpy)
- [snap.py](#snapy)
- [Configuration Parameters](#configuration-parameters)
- [Data Formats](#data-formats)

---

## face_data_collect.py

### Purpose
Automated face data collection module for building training datasets.

### Constants

```python
SAMPLE_RATE = 10        # Collect every 10th frame
FACE_SIZE = 100         # Standardized face size (100x100 pixels)
FACE_PADDING = 10       # Pixel offset for face crop
SCALE_FACTOR = 1.3      # Haar Cascade scale factor
MIN_NEIGHBORS = 5       # Minimum neighbors for detection
```

### Main Workflow

```python
1. Initialize camera (VideoCapture)
2. Load Haar Cascade classifier
3. Get user input (person's name)
4. Start video capture loop:
   a. Read frame from camera
   b. Detect faces
   c. Extract largest face
   d. Crop and normalize to 100x100
   e. Collect every 10th frame
5. Save collected data as .npy file
6. Release resources
```

### Key Variables

| Variable | Type | Description |
|----------|------|-------------|
| `cap` | VideoCapture | Camera object |
| `face_cascade` | CascadeClassifier | Face detection model |
| `face_data` | list | Collected face samples |
| `skip` | int | Frame counter for sampling |
| `face_section` | ndarray | Cropped face region |
| `file_name` | str | Person's name (validated) |

### Output Format

**File:** `face_dataset/[name].npy`

**Shape:** `(n_samples, 30000)`
- `n_samples`: Number of collected samples (~50-100)
- `30000`: Flattened 100x100x3 RGB image

### Usage

```python
python face_data_collect.py
# Input: Person's name
# Output: face_dataset/[name].npy
```

---

## face_recognition.py

### Purpose
Real-time face recognition engine using custom KNN classifier.

### Constants

```python
K_NEIGHBORS = 5         # Number of neighbors for KNN
FACE_SIZE = 100         # Standardized face size
FACE_PADDING = 10       # Pixel offset for face crop
SCALE_FACTOR = 1.3      # Haar Cascade scale factor
MIN_NEIGHBORS = 5       # Minimum neighbors for detection
```

### Functions

#### `distance(v1, v2)`

Calculate Euclidean distance between two vectors.

**Parameters:**
- `v1` (ndarray): First vector
- `v2` (ndarray): Second vector

**Returns:**
- `float`: Euclidean distance

**Formula:**
```python
distance = √Σ(v1[i] - v2[i])²
```

**Example:**
```python
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
d = distance(v1, v2)  # Returns 5.196...
```

---

#### `knn(train, test, k=K_NEIGHBORS)`

K-Nearest Neighbors classifier for face recognition.

**Parameters:**
- `train` (ndarray): Training data matrix (n_samples, features+1)
  - Shape: `(n_samples, 30001)` where last column is label
- `test` (ndarray): Test sample vector (30000 features)
- `k` (int, optional): Number of neighbors (default: 5)

**Returns:**
- `float`: Predicted class label

**Algorithm:**
```
1. Calculate distance from test to all training samples
2. Sort by distance (ascending)
3. Select K nearest neighbors
4. Majority vote determines class
5. Return winning class label
```

**Example:**
```python
# Training set: 100 samples, 30001 features (30000 + label)
train = np.array([[...features..., 0],  # Person 0
                  [...features..., 1],  # Person 1
                  ...])

# Test sample: 30000 features
test = np.array([...features...])

# Predict
prediction = knn(train, test, k=5)  # Returns 0 or 1
```

**Complexity:**
- Time: O(n × d) where n = samples, d = dimensions
- Space: O(n) for distance storage

---

### Main Workflow

```python
1. Load all .npy files from face_dataset/
2. Create class mappings (id → name)
3. Concatenate all data into training matrix
4. Initialize camera
5. Start recognition loop:
   a. Capture frame
   b. Detect faces
   c. For each face:
      - Extract and normalize
      - Flatten to vector
      - Classify using KNN
      - Display result
6. Release resources
```

### Key Variables

| Variable | Type | Shape | Description |
|----------|------|-------|-------------|
| `face_data` | list | - | List of training arrays |
| `labels` | list | - | List of label arrays |
| `names` | dict | - | Mapping {id: name} |
| `face_dataset` | ndarray | (n, 30000) | All face features |
| `face_labels` | ndarray | (n, 1) | All labels |
| `training_set` | ndarray | (n, 30001) | Combined data + labels |

### Data Structure

```python
# Example training_set structure
training_set = [
    [pixel1, pixel2, ..., pixel30000, label0],  # Sample 1
    [pixel1, pixel2, ..., pixel30000, label0],  # Sample 2
    [pixel1, pixel2, ..., pixel30000, label1],  # Sample 3
    ...
]
```

### Usage

```python
python face_recognition.py
# No input required
# Output: Real-time video with face recognition
```

---

## snap.py

### Purpose
Apply AR filters to images with facial feature detection.

### Constants

```python
INPUT_IMAGE_PATH    # Path to input image (user prompt)
SUNGLASSES_PATH     # Path to sunglasses template
MOUSTACHE_PATH      # Path to moustache template
OUTPUT_CSV_PATH     # Path for coordinate CSV
OUTPUT_IMAGE_PATH   # Path for filtered image
```

### Functions

#### `overlay_transparent(background, overlay, x, y)`

Overlay a transparent image with alpha blending.

**Parameters:**
- `background` (ndarray): Background image (BGR)
- `overlay` (ndarray): Overlay image (BGRA with alpha)
- `x` (int): X position for overlay
- `y` (int): Y position for overlay

**Returns:**
- `ndarray`: Modified background image

**Algorithm:**
```
1. Extract alpha channel from overlay
2. Normalize alpha to 0-1 range
3. Get ROI from background
4. Blend: result = alpha×overlay + (1-alpha)×background
5. Place blended result back in background
```

**Example:**
```python
background = cv2.imread('image.jpg')
overlay = cv2.imread('filter.png', -1)  # With alpha

result = overlay_transparent(background, overlay, 100, 100)
# Overlay placed at (100, 100) with transparency
```

**Features:**
- ✅ Boundary checking (prevents overflow)
- ✅ Alpha channel blending
- ✅ Automatic clipping to image bounds

---

### Main Workflow

```python
1. Load input image
2. Load filter templates (sunglasses, moustache)
3. Load Haar Cascade classifiers
4. Detect faces in image
5. For each face:
   a. Detect eyes
   b. Apply sunglasses with alpha blending
   c. Detect nose
   d. Apply moustache with alpha blending
6. Save modified image
7. Export coordinates to CSV
```

### Output Formats

#### Modified Image
**File:** `output_filtered.jpg`
- Format: JPEG
- Contains: Original image with applied filters

#### Coordinate CSV
**File:** `output.csv`

**Format:**
```csv
x,y,type
120,150,sunglasses
125,200,moustache
```

**Columns:**
- `x`: X coordinate of filter placement
- `y`: Y coordinate of filter placement
- `type`: Filter type ("sunglasses" or "moustache")

### Usage

```python
python snap.py
# Input: Image path (prompted)
# Output: output_filtered.jpg, output.csv
```

---

## Configuration Parameters

### Global Settings

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `SAMPLE_RATE` | 10 | 1-30 | Frame collection frequency |
| `FACE_SIZE` | 100 | 50-200 | Face normalization size |
| `FACE_PADDING` | 10 | 0-50 | Crop padding in pixels |
| `K_NEIGHBORS` | 5 | 1-15 | KNN neighbor count |
| `SCALE_FACTOR` | 1.3 | 1.1-2.0 | Detection sensitivity |
| `MIN_NEIGHBORS` | 5 | 3-10 | Detection accuracy |

### Parameter Effects

**SAMPLE_RATE**
- Lower (1-5): More samples, slower collection
- Higher (15-30): Fewer samples, faster collection

**K_NEIGHBORS**
- Lower (1-3): More sensitive, may overfit
- Higher (7-15): More stable, may underfit
- Recommended: 3-7

**SCALE_FACTOR**
- Lower (1.1): More detections, slower, more false positives
- Higher (1.5-2.0): Fewer detections, faster, more misses
- Recommended: 1.1-1.3

---

## Data Formats

### .npy Files (Training Data)

**Format:** NumPy binary serialization

**Structure:**
```python
data = np.load('person.npy')
# Shape: (n_samples, 30000)
# Type: float64 or uint8
# Range: 0-255 (pixel values)
```

**Advantages:**
- Fast I/O operations
- Efficient storage
- Preserves data type and shape
- No parsing overhead

### CSV Files (Filter Metadata)

**Format:** Standard CSV

**Structure:**
```csv
x,y,type
120,150,sunglasses
125,200,moustache
```

**Fields:**
- `x`: Integer, X coordinate
- `y`: Integer, Y coordinate
- `type`: String, filter name

---

## Error Codes

### Exit Codes

| Code | Meaning | Cause |
|------|---------|-------|
| 0 | Success | Normal exit |
| 1 | Error | Camera/file/validation failure |

### Common Errors

**Camera Errors:**
- `Error: Could not open camera` → Camera unavailable
- `Warning: Failed to read frame` → Temporary read failure

**File Errors:**
- `Error: Could not load [file]` → File missing/corrupted
- `Error: No training data found` → Empty dataset

**Validation Errors:**
- `Error: Name must contain only...` → Invalid input
- `Error: Dataset directory not found` → Missing folder

---

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Face Detection | O(n×m) | n×m = frame size |
| KNN Classification | O(k×d) | k=samples, d=30000 |
| Distance Calc | O(d) | d=30000 per sample |
| Alpha Blending | O(w×h) | w×h = overlay size |

### Space Complexity

| Component | Space | Per Item |
|-----------|-------|----------|
| Training Sample | 30000 floats | ~234 KB |
| Training Set (50 samples) | ~1.5 MB | Per person |
| Frame Buffer | ~1 MB | 640×480×3 |
| Total Runtime | ~200 MB | Approximate |

### Performance Metrics

- **Frame Rate:** 30 FPS (typical)
- **Recognition Latency:** <33ms per frame
- **Detection Accuracy:** 85-95% (good lighting)
- **Training Time:** Instant (no training phase)

---

## Thread Safety

⚠️ **Not thread-safe**
- Camera access is single-threaded
- OpenCV GUI operations are not thread-safe
- Do not call functions from multiple threads

---

## Version Compatibility

| Component | Version | Notes |
|-----------|---------|-------|
| Python | 3.7+ | Required |
| OpenCV | 4.5+ | Recommended 4.8+ |
| NumPy | 1.19+ | Recommended 1.24+ |

---

## See Also

- [README.md](../README.md) - Main documentation
- [SETUP_GUIDE.md](../SETUP_GUIDE.md) - Installation instructions
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines

