import cv2
import numpy as np
import os
import csv

# Load input image and templates
input_image = cv2.imread('/Users/armanmalik/Desktop/face_recog/Test/Before.png', cv2.IMREAD_COLOR)
sunglasses_template = cv2.imread('/Users/armanmalik/Desktop/face_recog/sunglasses_template.png', -1)
moustache_template = cv2.imread('/Users/armanmalik/Desktop/face_recog/moustache_template.png', -1)

# Load Haar cascade files for face and facial keypoint detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml") 
nose_cascade = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")

# Detect faces in the input image
faces = face_cascade.detectMultiScale(input_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Prepare data for CSV
data = []

for (x, y, w, h) in faces:
    # Detect eyes and nose in the face region
    roi_gray = input_image[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    nose = nose_cascade.detectMultiScale(roi_gray)

    # Overlay sunglasses
    # Overlay sunglasses
    # Overlay sunglasses
    for (ex, ey, ew, eh) in eyes:
        sunglasses_resized = cv2.resize(sunglasses_template, (ew, eh))
        sunglasses_rgb = cv2.cvtColor(sunglasses_resized, cv2.COLOR_BGRA2BGR)
        input_image[y+ey:y+ey+eh, x+ex:x+ex+ew] = sunglasses_rgb
        data.append({'x': x+ex, 'y': y+ey, 'type': 'sunglasses'})

    # Overlay moustache
    for (nx, ny, nw, nh) in nose:
        moustache_resized = cv2.resize(moustache_template, (nw, nh))
        moustache_rgb = cv2.cvtColor(moustache_resized, cv2.COLOR_BGRA2BGR)
        input_image[y+ny:y+ny+nh, x+nx:x+nx+nw] = moustache_rgb
        data.append({'x': x+nx, 'y': y+ny, 'type': 'moustache'})
# Write data to CSV
csv_file_path = '/Users/armanmalik/Desktop/face_recog/output.csv'
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['x', 'y', 'type'])
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print(f"CSV file saved to {csv_file_path}")

# Display or save the modified image
cv2.imshow('Modified Image', input_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
