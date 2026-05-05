import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure the API
genai.configure(api_key=GEMINI_API_KEY)

# Storing memory in memory (pun intended) for simple local execution.
chat_history = []

def get_system_prompt(emotion):
    """ Dynamically updates instructions based on the user's face. """
    base_prompt = "You are an AI emotional support and conversational chatbot. "
    
    emotion_guidelines = {
        "Happy": "The user looks HAPPY. Match their energy, be cheerful, friendly, and engaging.",
        "Sad": "The user looks SAD. Be highly empathetic, comforting, supportive, and gentle. Ask if they want to talk about it.",
        "Angry": "The user looks ANGRY. Remain calm, grounding, and de-escalating. Do not be overly cheerful.",
        "Fear": "The user looks FEARFUL or ANXIOUS. Be reassuring, safe, and calming. Offer breathing exercises if appropriate.",
        "Surprise": "The user looks SURPRISED. Be curious and engaged.",
        "Disgust": "The user looks DISGUSTED. Be neutral and try to understand what is bothering them.",
        "Neutral": "The user looks NEUTRAL. Provide normal, helpful, and polite responses."
    }
    
    guideline = emotion_guidelines.get(emotion, emotion_guidelines["Neutral"])
    return base_prompt + guideline

def generate_emotion_response(user_message, current_emotion):
    global chat_history
    
    system_instruction = get_system_prompt(current_emotion)
    
    # Using Gemini 1.5 Flash as it's the fastest and supports system instructions natively
    model = genai.GenerativeModel(
        model_name='gemini-flash-latest',
        system_instruction=system_instruction
    )
    
    # Initialize a chat session with previous history
    chat = model.start_chat(history=chat_history)
    
    # Note: I pass the emotion context invisibly into the prompt so the model is strictly aware.
    contextual_prompt = f"[System Notice: The user's current detected emotion is {current_emotion}]. User says: {user_message}"
    
    try:
        response = chat.send_message(contextual_prompt)
        # Update history
        chat_history = chat.history
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "I'm having trouble connecting to my brain right now. Please check my API key."