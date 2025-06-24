import cv2
import numpy as np
import os

# Load Haar cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Path to voter images
data_path = 'voter_images'
images = []
labels = []
label_map = {}
label_count = 0
fixed_size = (200, 200)  # Fixed size for resizing images

# Load and label images
for file in os.listdir(data_path):
    if file.endswith('.png') or file.endswith('.jpeg'):
        img = cv2.imread(os.path.join(data_path, file), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            img_resized = cv2.resize(img, fixed_size)  # Resize to fixed size
            images.append(img_resized)
            label = file.split('.')[0]
            if label not in label_map:
                label_map[label] = label_count
                label_count += 1
            labels.append(label_map[label])

# Convert to NumPy arrays
images = np.array(images)
labels = np.array(labels)

# Train the recognizer (using LBPH)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(images, labels)

# Reverse label map for displaying names
reverse_label_map = {v: k for k, v in label_map.items()}

# Start video capture
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces using Haar cascade
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    voting_status = "Access Denied - Unregistered Voter"
    
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        face_resized = cv2.resize(face_roi, fixed_size)  # Resize for prediction
        
        # Predict face
        label, confidence = recognizer.predict(face_resized)
        name = reverse_label_map.get(label, "Unknown")
        
        if confidence < 100:
            voting_status = "Access Granted - Proceed to Vote"
            color = (0, 255, 0)  # Green for registered voters
        else:
            name = "Unknown"
            color = (0, 0, 255)  # Red for unregistered voters
        
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, f'{name} ({int(confidence)})', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Display voting status
    cv2.putText(frame, voting_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0) if voting_status == "Access Granted - Proceed to Vote" else (0, 0, 255), 2)

    # Display video output
    cv2.imshow('Smart Voting System', frame)
    
    # Quit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()
