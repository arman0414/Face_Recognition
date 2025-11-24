# 🚀 Complete Setup Guide

## Table of Contents
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [First-Time Setup](#first-time-setup)
- [Testing Your Installation](#testing-your-installation)
- [Common Issues](#common-issues)

---

## 💻 System Requirements

### Minimum Requirements
- **OS:** Windows 10, macOS 10.13+, or Linux (Ubuntu 18.04+)
- **Python:** 3.7 or higher
- **RAM:** 4GB minimum, 8GB recommended
- **Webcam:** Any USB or built-in camera
- **Storage:** 500MB free space

### Recommended
- **Python:** 3.9 or 3.10
- **RAM:** 8GB
- **CPU:** Multi-core processor for faster processing
- **GPU:** Not required (CPU processing is sufficient)

---

## 📥 Installation

### Step 1: Install Python

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ **Check "Add Python to PATH"**
4. Click "Install Now"
5. Verify installation:
```bash
python --version
```

#### macOS
```bash
# Using Homebrew
brew install python3

# Verify
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip

# Verify
python3 --version
```

---

### Step 2: Clone Repository

```bash
# HTTPS
git clone https://github.com/yourusername/Face_Recognition.git

# OR SSH
git clone git@github.com:yourusername/Face_Recognition.git

# Navigate to directory
cd Face_Recognition
```

**Don't have Git?**
- Download ZIP from GitHub → Extract → Open terminal in that folder

---

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# For Python 3 specifically
pip3 install -r requirements.txt
```

**What gets installed:**
- `opencv-python` - Computer vision library
- `numpy` - Numerical computing library

---

## 🎬 First-Time Setup

### 1. Verify Installation

```bash
python -c "import cv2; import numpy as np; print('✓ OpenCV version:', cv2.__version__); print('✓ NumPy version:', np.__version__)"
```

**Expected output:**
```
✓ OpenCV version: 4.8.1
✓ NumPy version: 1.24.3
```

---

### 2. Test Camera Access

```bash
python -c "import cv2; cap = cv2.VideoCapture(0); print('✓ Camera accessible!' if cap.isOpened() else '✗ Camera not found'); cap.release()"
```

**Expected output:**
```
✓ Camera accessible!
```

---

### 3. Collect Your First Dataset

```bash
python face_data_collect.py
```

**Follow the prompts:**
1. Enter your name (e.g., "John")
2. Face the camera
3. Wait for 50+ samples to be collected
4. Press `q` to save

**Result:** Creates `face_dataset/John.npy`

---

### 4. Test Recognition

```bash
python face_recognition.py
```

**What you'll see:**
- Your webcam opens
- System detects and recognizes your face
- Your name appears above your face
- Press `q` to quit

---

### 5. Test Filter Application (Optional)

First, place a test image in the project folder, then:

```bash
python snap.py
```

**Follow prompts:**
1. Enter image path or press Enter for default
2. System processes and displays result
3. Check `output_filtered.jpg`

---

## ✅ Testing Your Installation

### Test Suite

Run these commands to verify everything works:

```bash
# Test 1: Import check
python -c "import cv2, numpy as np; print('✓ Imports successful')"

# Test 2: File check
python -c "import os; print('✓ Cascade files exist' if all(os.path.exists(f) for f in ['haarcascade_frontalface_alt.xml', 'haarcascade_eye.xml', 'haarcascade_mcs_nose.xml']) else '✗ Missing files')"

# Test 3: Camera check
python -c "import cv2; cap = cv2.VideoCapture(0); print('✓ Camera works' if cap.isOpened() else '✗ Camera issue'); cap.release()"

# Test 4: Template check
python -c "import os; print('✓ Templates exist' if all(os.path.exists(f) for f in ['sunglasses_template.png', 'moustache_template.png']) else '⚠ Templates missing (optional)')"
```

---

## 🔧 Common Issues

### Issue 1: "No module named 'cv2'"

**Solution:**
```bash
pip install --upgrade opencv-python
# OR
pip3 install --upgrade opencv-python
```

---

### Issue 2: "Could not open camera"

**Possible causes & solutions:**

**A. Camera in use by another app**
- Close Zoom, Skype, or other camera apps
- Restart your computer

**B. Permission denied (macOS)**
```bash
# Grant camera permission:
System Preferences → Security & Privacy → Camera → Check Terminal/Python
```

**C. Multiple cameras (try different index)**
Edit files and change:
```python
cap = cv2.VideoCapture(0)  # Try 0, 1, 2
```

**D. Linux permissions**
```bash
sudo usermod -a -G video $USER
# Logout and login again
```

---

### Issue 3: "Could not load haarcascade file"

**Solution:**
```bash
# Verify files exist
ls -la *.xml

# If missing, download from:
# https://github.com/opencv/opencv/tree/master/data/haarcascades
```

---

### Issue 4: Poor Recognition Accuracy

**Solutions:**
- Collect more samples (50+ per person)
- Ensure good lighting
- Collect samples with varied angles
- Try adjusting `K_NEIGHBORS` in code:
  ```python
  K_NEIGHBORS = 5  # Try 3, 5, or 7
  ```

---

### Issue 5: Slow Performance

**Solutions:**
- Close other applications
- Increase `SAMPLE_RATE` to reduce processing:
  ```python
  SAMPLE_RATE = 20  # Collect fewer frames
  ```
- Lower camera resolution in code:
  ```python
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
  ```

---

### Issue 6: Python version conflicts

**Solution:**
```bash
# Use Python 3 explicitly
python3 face_recognition.py
pip3 install -r requirements.txt

# Or create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🌟 Advanced Setup

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv face_recog_env

# Activate it
# Windows:
face_recog_env\Scripts\activate
# macOS/Linux:
source face_recog_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Deactivate when done
deactivate
```

---

### GPU Acceleration (Optional)

For faster processing with NVIDIA GPU:

```bash
# Uninstall CPU version
pip uninstall opencv-python

# Install GPU version
pip install opencv-contrib-python
```

**Note:** Requires CUDA-compatible GPU and CUDA toolkit installed.

---

## 📞 Getting Help

If you're still stuck:

1. **Check existing issues:** [GitHub Issues](https://github.com/yourusername/Face_Recognition/issues)
2. **Create new issue:** Include error message, OS, Python version
3. **Stack Overflow:** Tag with `opencv` and `python`

---

## ✅ Setup Checklist

- [ ] Python 3.7+ installed
- [ ] Git installed (or ZIP downloaded)
- [ ] Repository cloned/extracted
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Imports working (OpenCV, NumPy)
- [ ] Camera accessible
- [ ] Cascade files present
- [ ] First dataset collected
- [ ] Recognition tested successfully

---

**🎉 Setup complete! You're ready to go!**

Return to [README.md](README.md) for usage instructions.

