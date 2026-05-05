import os
import cv2

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBiwxRPnNB2Tm_NBREdm5xxHPd_PrZ59fA")

MODEL_PATH = "models/emotion_model.h5"

HAAR_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

EMOTION_LABELS = [
    'Angry',
    'Disgust',
    'Fear',
    'Happy',
    'Sad',
    'Surprise',
    'Neutral'
]

