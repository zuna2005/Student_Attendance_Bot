import face_recognition
import os
import numpy as np
from constants import DATASET_DIR_PATH, KNOWN_FACES_PATH, KNOWN_ENCODINGS_PATH


# Initialize lists to store face encodings and names
known_face_encodings = []
known_face_names = []

# Iterate through the dataset folders
for folder_name in os.listdir(DATASET_DIR_PATH):
    folder_path = os.path.join(DATASET_DIR_PATH, folder_name)
    print(folder_path)
    if os.path.isdir(folder_path):  # Check if it's a directory
        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)
            image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(image)[0]  # Assuming only one face per image
            known_face_encodings.append(face_encoding)
            known_face_names.append(folder_name)

# Save the encodings and names to files
np.save(KNOWN_FACES_PATH, known_face_encodings)
np.save(KNOWN_ENCODINGS_PATH, known_face_names)