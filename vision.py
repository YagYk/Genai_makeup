# Q&A Chatbot
#from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("AIzaSyD_tMm09r_1yEMQRLorJq0JfPZedu67Ar8"))



def get_gemini_response(input, image, chat_history=[]):
    model = genai.GenerativeModel('gemini-pro-vision')
    prompt = f"""
    Analyze the facial features in this image and recommend suitable makeup and accessories.
    Consider skin tone, eye color, face shape, and any other relevant features.
    Provide specific product recommendations for makeup items.
    
    User query: {input}
    """
    if image is not None:
        response = model.generate_content([prompt, image] + chat_history)
    else:
        response = model.generate_content(prompt + "\n".join([f"{role}: {msg}" for role, msg in chat_history]))
    return response.text

def chatbot_response(query, chat_history):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    You are a helpful beauty assistant. The user has already received makeup recommendations.
    Answer their questions about facial features, makeup application, or product recommendations.
    Be concise and friendly in your responses.

    User query: {query}
    """
    response = model.generate_content(prompt + "\n".join([f"{role}: {msg}" for role, msg in chat_history]))
    return response.text

##initialize our streamlit app

st.set_page_config(page_title="Beauty Advisor")
st.header("Beauty Advisor Application")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

input_prompt = st.text_input("Describe what kind of look you're going for:", key="input_prompt")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

if st.button("Get Makeup Recommendations"):
    if image:
        with st.spinner("Analyzing image and generating recommendations..."):
            response = get_gemini_response(input_prompt, image)
        st.subheader("Makeup and Accessory Recommendations")
        st.write(response)
        st.session_state.chat_history = [("AI", response)]
    else:
        st.error("Please upload an image to get makeup recommendations.")

st.subheader("Chat with Beauty Assistant")
user_query = st.text_input("Ask about your facial features or makeup:", key="user_query")

if st.button("Ask"):
    if user_query:
        with st.spinner("Generating response..."):
            ai_response = chatbot_response(user_query, st.session_state.chat_history)
        st.session_state.chat_history.append(("Human", user_query))
        st.session_state.chat_history.append(("AI", ai_response))

if st.session_state.chat_history:
    st.subheader("Conversation History")
    for role, text in st.session_state.chat_history:
        if role == "Human":
            st.write(f"You: {text}")
        else:
            st.write(f"Beauty Assistant: {text}")
