import streamlit as st
import google.generativeai as genai
from PIL import Image

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Textbook & Diagram Analyzer",
    page_icon="🥻",
    layout="wide"
)

st.title("Professor notes")
st.write("Upload a image and get insights using Gemini 3.6 Flash.")

# -----------------------------
# Gemini API Configuration
# -----------------------------
GOOGLE_API_KEY = "GOOGLE_API_KEY"

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-3.6-flash")

# -----------------------------
# Image Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload a Image",
    type=["jpg", "jpeg", "png"]
)

# -----------------------------
# Analyze Button
# -----------------------------
if uploaded_file is not None:

    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Uploaded Image", use_container_width=True)

    with col2:

        if st.button("Analyze Image"):

            with st.spinner("Analyzing image..."):

                prompt = """
                You are an AI Study Assistant for students.

                Analyze the uploaded educational image. The image may contain a textbook page, educational diagram, chart, graph, map, illustration, table, or handwritten educational content.

                Your goal is to convert the visual content into useful study material.

                Perform these tasks:

                1. TOPIC IDENTIFICATION
                Identify the main subject and topic.

                2. CONTENT EXTRACTION
                Extract the important visible information.
                Preserve important facts, terminology, numbers, formulas, labels, and relationships.

                3. SIMPLE EXPLANATION
                Explain the concept in simple language suitable for a beginner-level student.

                4. IMPORTANT TERMS
                Identify important terms and provide simple definitions.

                5. KEY POINTS
                Extract the most important points a student should remember.

                6. SUMMARY
                Provide a concise summary of the content.

                7. EXAM QUESTIONS
                Generate 5 important questions based strictly on the uploaded content.

                8. MCQs
                Generate 5 multiple-choice questions.
                Each question should have:
                - Four options
                - Correct answer
                - Short explanation

                9. EXAM REVISION
                Provide 3 important examination points.

                OUTPUT FORMAT:

                ## 📚 Topic
                ...

                ## 📝 Important Information
                ...

                ## 💡 Simple Explanation
                ...

                ## 📖 Important Terms
                | Term | Simple Definition |
                |---|---|

                ## 🔑 Key Points
                - ...

                ## 📌 Short Summary
                ...

                ## ❓ Important Questions
                1. ...
                2. ...
                3. ...
                4. ...
                5. ...

                ## 🧠 Multiple Choice Questions

                ### Q1
                A. ...
                B. ...
                C. ...
                D. ...

                **Answer:** ...
                **Explanation:** ...

                Repeat for Q2–Q5.

                ## 🎯 Exam Revision Points
                1. ...
                2. ...
                3. ...

                IMPORTANT:
                Do not invent information that is not present or reasonably explained by the uploaded educational material.
                """

                response = model.generate_content(
                    [prompt, image]
                )

                st.subheader("Analysis Result")
                st.write(response.text)
