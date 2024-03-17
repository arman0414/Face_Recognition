import cv2
import numpy as np

# Init Camera
cap = cv2.VideoCapture(0)

# Face Detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
skip = 0
face_data = []
dataset_path = '/Users/armanmalik/Desktop/face_recog/'
file_name = input("Enter the name of the person: ")
face_section = None  # Define face_section outside the loop

while True:
    ret, frame = cap.read()

    if ret == False:
        continue
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    faces = face_cascade.detectMultiScale(frame, 1.3, 5)  # 1.3 is the scaling factor, 5 is the neighbors
    faces = sorted(faces, key=lambda f: f[2] * f[3])  # Sort the faces based on area (f[2]*f[3])
    print(faces)

    for face in faces[-1:]:  # -1 is the last face
        x, y, w, h = face
        center = (x + w // 2, y + h // 2)
        radius = max(w, h) // 2
        cv2.circle(frame, center, radius, (255, 0, 0), 2)

        # crop required face: Region of Interest
        offset = 10
        face_section = frame[y - offset:y + h + offset, x - offset:x + w + offset]
        face_section = cv2.resize(face_section, (100, 100))
        skip += 1
        if (skip % 10 == 0):
            face_data.append(face_section)
            print(len(face_data))

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
    print(face_data.shape)
    print("Data Collected" + dataset_path + file_name + '.npy')
# Save this data into the file system
    np.save(dataset_path + file_name + '.npy', face_data)
else:
    print("No Data Collected")
cap.release()
cv2.destroyAllWindows()
