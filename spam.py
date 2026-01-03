# ==============================
# STREAMLIT REAL-TIME SPAM PREDICTION
# ==============================

import streamlit as st
import joblib

# Load model & vectorizer
model = joblib.load("spam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Page config
st.set_page_config(page_title="Email Spam Detector", layout="centered")

# ---------- BACKGROUND CSS ----------
st.markdown(
    """
    <style>
    /* Light red to green gradient background */
    .stApp {
        background: linear-gradient(to bottom right, #ffcccc, #ccffcc);
        min-height: 100vh;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("📧 Email Spam Detection System")
st.write("Enter an email message below to check whether it is **Spam** or **Not Spam**.")

# Input box
email_text = st.text_area("✉️ Enter Email Content")

# Prediction function
def predict_email(text):
    vector = vectorizer.transform([text])
    prediction = model.predict(vector)[0]
    return prediction

# Button
if st.button("Check Email"):
    if email_text.strip() == "":
        st.warning("⚠️ Please enter an email message.")
    else:
        result = predict_email(email_text)

        if result == 1:
            st.error("🚨 This Email is SPAM")
        else:
            st.success("✅ This Email is NOT SPAM (HAM)")
