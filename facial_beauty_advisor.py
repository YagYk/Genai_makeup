import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import os
import google.generativeai as genai
from dotenv import load_dotenv
from login import main as login_main, init_db

# Load environment variables and configure Google Generative AI
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    min_detection_confidence=0.5
)

# Initialize the database
init_db()

def detect_facial_features(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        features = {
            "eye_distance": np.sqrt((landmarks[33].x - landmarks[263].x)**2 + 
                                  (landmarks[33].y - landmarks[263].y)**2),
            "nose_to_lip_distance": np.sqrt((landmarks[4].x - landmarks[61].x)**2 + 
                                          (landmarks[4].y - landmarks[61].y)**2),
            "lip_width": np.sqrt((landmarks[61].x - landmarks[291].x)**2 + 
                                (landmarks[61].y - landmarks[291].y)**2),
        }
        return features
    return None

def get_recommendations(features):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Based on these facial features, recommend makeup and beauty accessories:
    - Eye distance: {features['eye_distance']:.4f}
    - Nose to lip distance: {features['nose_to_lip_distance']:.4f}
    - Lip width: {features['lip_width']:.4f}
    
    Please provide specific recommendations for:
    1. Eye makeup
    2. Lip color and style
    3. Face contouring
    4. Accessories (earrings, necklaces)
    """
    response = model.generate_content(prompt)
    return response.text

def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    return response

# Streamlit UI
st.title("Facial Beauty Advisor")

# Check if user is logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_main()
else:
    # Initialize session states
    if 'image' not in st.session_state:
        st.session_state.image = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None

    # Camera input
    camera_input = st.camera_input("Take a picture")

    if st.button("Save Image"):
        if st.session_state.image is not None:
            st.success("Image saved successfully!")

    # Process captured image
    if camera_input:
        st.session_state.image = camera_input.getvalue()
        
    if st.session_state.image:
        st.image(st.session_state.image, caption="Captured Image", use_column_width=True)
        
        image = cv2.imdecode(np.frombuffer(st.session_state.image, np.uint8), cv2.IMREAD_COLOR)
        features = detect_facial_features(image)
        
        if features:
            st.write("Detected facial features:", features)
            st.session_state.recommendations = get_recommendations(features)
            st.subheader("Makeup and Accessory Recommendations")
            st.write(st.session_state.recommendations)
        else:
            st.error("No face detected. Please try again with a clear facial image.")
    else:
        st.info("Please take a photo to get makeup and accessory recommendations.")

    # Chat interface
    st.subheader("Chat with Beauty Assistant")
    user_query = st.text_input("Ask about beauty or makeup:", key="user_query")
    submit = st.button("Ask")

    if submit and user_query:
        response = get_gemini_response(user_query)
        st.subheader("Beauty Assistant Response:")
        for chunk in response:
            st.write(chunk.text)

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
