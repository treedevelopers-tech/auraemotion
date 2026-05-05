from flask import Flask, render_template, request, jsonify
import base64
import numpy as np
import cv2
import emotion_detection.detect_emotion as ed
from chatbot.gemini_chat import generate_emotion_response

app = Flask(__name__)

@app.route('/')
def index():
    # Serves the main frontend page
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame_route():
    data = request.json
    if not data or 'image' not in data:
        return jsonify({"error": "No image provided"}), 400
        
    # Decode base64 image
    image_data = data['image'].split(',')[1]
    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Process frame
    processed_frame, emotion = ed.process_frame(frame)
    
    # Encode back to base64
    _, buffer = cv2.imencode('.jpg', processed_frame)
    processed_image_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return jsonify({
        "emotion": emotion,
        "image": f"data:image/jpeg;base64,{processed_image_base64}"
    })

@app.route('/get_current_emotion', methods=['GET'])
def get_current_emotion():
    # Frontend will poll this endpoint to update the UI label
    return jsonify({"emotion": ed.LATEST_EMOTION})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    
    # Grab the globally detected emotion
    current_emotion = ed.LATEST_EMOTION
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
        
    # Get response adapted to current emotion
    bot_reply = generate_emotion_response(user_message, current_emotion)
    
    return jsonify({
        "response": bot_reply,
        "emotion_used": current_emotion
    })

if __name__ == '__main__':
    # Running locally on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)