import streamlit as st
import google.generativeai as genai
from PIL import Image


# ---------------------------------------
# Load Environment Variables
# ---------------------------------------


GOOGLE_API_KEY = "AQ.Ab8RN6LDZtuBfG4PDrtKRZSUKpoaQKAISGrps1OekJv1i-0s9w"

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# ---------------------------------------
# Page Configuration
# ---------------------------------------
st.set_page_config(
    page_title="AI Food Image Classifier",
    page_icon="🍎",
    layout="wide"
)


# ---------------------------------------
# Initialize Session State
# ---------------------------------------
if "classification_result" not in st.session_state:
    st.session_state.classification_result = None

if "food_image" not in st.session_state:
    st.session_state.food_image = None

if "question_answer" not in st.session_state:
    st.session_state.question_answer = None


# ---------------------------------------
# Title
# ---------------------------------------
st.title("🍎 AI Food Image Classifier")

st.write(
    "Upload a food image and get food classification "
    "using Gemini 2.5 Flash."
)


# ---------------------------------------
# Image Upload
# ---------------------------------------
uploaded_file = st.file_uploader(
    "Upload a Food Image",
    type=["jpg", "jpeg", "png"]
)


# ---------------------------------------
# Process Uploaded Image
# ---------------------------------------
if uploaded_file is not None:

    image = Image.open(uploaded_file)

    # Store image in session state
    st.session_state.food_image = image.copy()

    # Display image and button
    col1, col2 = st.columns([1.5, 1])

    with col1:

        display_image = image.copy()
        display_image.thumbnail((600, 500))

        st.image(
            display_image,
            caption="Uploaded Food Image",
            use_container_width=True
        )

    with col2:

        st.subheader("🔍 Classification")

        classify_button = st.button(
            "Classify Food",
            use_container_width=True
        )

        if classify_button:

            with st.spinner("Analyzing image..."):

                prompt = """
                You are an AI Food Classification Assistant.

                Analyze the uploaded food image and classify it
                into ONE of the following categories:

                1. Healthy Food
                2. Fast Food
                3. Dessert
                4. Fruit
                5. Vegetable
                6. Beverage
                7. Snack
                8. Other

                Your task is to identify the food and assign
                the most appropriate category.

                Provide the result in exactly this format:

                ### Classification Result

                **Food Name:** [Name of the food]

                **Category:** [ONE category from the list]

                **Confidence:** [High / Medium / Low]

                **Reason:** [Brief explanation of why the food
                belongs to this category]

                Do not assign multiple categories.

                Always select exactly ONE category.
                """

                response = model.generate_content(
                    [prompt, st.session_state.food_image]
                )

                # Save result in session state
                st.session_state.classification_result = response.text

                # Clear previous question answer
                st.session_state.question_answer = None


# ---------------------------------------
# Display Classification Result
# ---------------------------------------
if st.session_state.classification_result:

    st.divider()

    st.subheader("📊 Analysis Result")

    st.markdown(
        st.session_state.classification_result
    )


# ---------------------------------------
# Follow-up Question Section
# ---------------------------------------
if st.session_state.food_image is not None:

    st.divider()

    st.subheader("💬 Ask About This Image")

    st.write(
        "Not satisfied with the classification? "
        "Ask one question about the uploaded food image."
    )

    # Form prevents execution while typing
    with st.form("question_form"):

        user_question = st.text_input(
            "Your Question",
            placeholder="Example: Is this a healthy food?"
        )

        ask_button = st.form_submit_button(
            "🤖 Ask Gemini",
            use_container_width=True
        )

    # ---------------------------------------
    # Process Follow-up Question
    # ---------------------------------------
    if ask_button:

        if user_question.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Gemini is thinking..."):

                question_prompt = f"""
                You are an AI Food Image Assistant.

                Look carefully at the uploaded food image.

                Answer the user's question based on what is
                visibly present in the image.

                User Question:
                {user_question}

                Give a clear, simple and useful answer.

                If the question asks whether the food is
                good or bad, explain whether it appears to be
                generally healthy or less healthy from a
                general food-quality and nutrition perspective.

                Do not invent information that cannot be
                determined from the image.

                Clearly mention uncertainty when appropriate.
                """

                question_response = model.generate_content(
                    [
                        question_prompt,
                        st.session_state.food_image
                    ]
                )

                # Store answer
                st.session_state.question_answer = (
                    question_response.text
                )


# ---------------------------------------
# Display Gemini Answer
# ---------------------------------------
if st.session_state.question_answer:

    st.subheader("🤖 Gemini's Answer")

    st.markdown(
        st.session_state.question_answer
    )