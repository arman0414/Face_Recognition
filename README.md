# 🎭 Face Recognition System

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Real-time face recognition system with custom KNN classifier and AR filter capabilities built from scratch using Python and OpenCV.

---

## 🎯 What It Does

This system performs **three main functions**:

1. **Collects Face Data** - Captures and stores face samples for training
2. **Recognizes Faces** - Identifies people in real-time using webcam (85-95% accuracy at 30 FPS)
3. **Applies AR Filters** - Adds sunglasses and moustache overlays to images

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/arman0414/Face_Recognition.git
cd Face_Recognition

# Install dependencies
pip install -r requirements.txt
```

### Usage

**Step 1: Collect Training Data**
```bash
python face_data_collect.py
# Enter person's name → Face camera → Press 'q' when done (collect 50+ samples)
```

**Step 2: Run Face Recognition**
```bash
python face_recognition.py
# System recognizes faces in real-time → Press 'q' to quit
```

**Step 3: Apply Filters (Optional)**
```bash
python snap.py
# Enter image path → System applies filters → Check output_filtered.jpg
```

---

## 🧠 Technical Approach

### Architecture
```
Data Collection → Feature Extraction → KNN Classification → Real-time Recognition
```

### Algorithm: K-Nearest Neighbors (Custom Implementation)

**Training Phase:**
1. Capture face images from webcam
2. Detect faces using Haar Cascade Classifiers
3. Normalize to 100×100 pixels
4. Flatten to 30,000-dimensional feature vectors
5. Store as binary `.npy` files

**Recognition Phase:**
1. Capture live frame from webcam
2. Detect and extract face region
3. Calculate Euclidean distance to all training samples
4. Select K=5 nearest neighbors
5. Majority vote determines identity

**Formula:**
```
distance = √Σ(pixel_test - pixel_train)²
prediction = mode(labels of 5 nearest neighbors)
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

<div align="center">

**Made with ❤️ using Python, OpenCV, and NumPy**

[Report Bug](https://github.com/arman0414/Face_Recognition/issues) · [Request Feature](https://github.com/arman0414/Face_Recognition/issues)

</div>
