import cv2
import numpy as np
import tensorflow as tf
from config import MODEL_PATH, EMOTION_LABELS
from emotion_detection.face_detector import detect_faces

# Load model globally to avoid reloading on every frame
try:
    emotion_model = tf.keras.models.load_model(MODEL_PATH)
    print("Emotion model loaded successfully.")
except Exception as e:
    print(f"Warning: Could not load model. Did you run train_emotion_model.py? Error: {e}")
    emotion_model = None

# Global variable to store the latest detected emotion
LATEST_EMOTION = "Neutral"

def predict_emotion(face_img):
    """ Runs CNN model on a 48x48 grayscale cropped face. """
    if emotion_model is None:
        return "Neutral"
        
    face_img = cv2.resize(face_img, (48, 48))
    face_img = np.expand_dims(face_img, axis=0)
    face_img = np.expand_dims(face_img, axis=-1)
    face_img = face_img.astype('float32') / 255.0 # Apply same normalization as training!
    
    predictions = emotion_model.predict(face_img, verbose=0)
    max_index = int(np.argmax(predictions))
    return EMOTION_LABELS[max_index]

def process_frame(frame):
    """ Process a single frame array and return the annotated frame and emotion. """
    global LATEST_EMOTION
    
    faces, gray_frame = detect_faces(frame)
    
    for (x, y, w, h) in faces:
        # Crop the face
        roi_gray = gray_frame[y:y+h, x:x+w]
        
        # Predict
        emotion = predict_emotion(roi_gray)
        LATEST_EMOTION = emotion # Update global state for the chatbot
        
        # Draw rectangle and text
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
    return frame, LATEST_EMOTION