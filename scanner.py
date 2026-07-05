import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="AI Math Scanner", page_icon="📐", layout="centered")

st.title("AI Solver")
st.write("Upload a picture of any math problem, and the AI will solve it step-by-step!")

# 1. Initialize the Gemini Client
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Missing Gemini API Key. Please set your GEMINI_API_KEY environment variable.")
    st.stop()

# 2. Image Upload Feature
uploaded_file = st.file_uploader("Choose a math problem image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Math Problem", use_container_width=True)
    
    # 3. Trigger the Math Solver
    if st.button("🚀 Scan & Solve Problem", type="primary"):
        with st.spinner("Analyzing math notation and calculating step-by-step solution..."):
            try:
                # We pass both the image and a text prompt to the model
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        image, 
                        "Solve this math problem step-by-step. Show all work clearly and explain the logic or formula used to simplify it."
                    ]
                )
                
                st.success("Problem Solved!")
                st.subheader("📝 Step-by-Step Solution")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")