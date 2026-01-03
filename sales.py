import streamlit as st
import numpy as np
import pickle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sales Prediction App",
    layout="centered"
)

# ---------------- GREEN ANIMATED BACKGROUND CSS ----------------
st.markdown(
    """
    <style>
    /* Animated green gradient background */
    .stApp {
        background: linear-gradient(
            -45deg,
            #0b3d2e,
            #146356,
            #1e8449,
            #27ae60,
            #2ecc71
        );
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Title styling */
    h1 {
        color: #eaffea;
        text-align: center;
    }

    /* Subtitle text */
    p {
        color: #d4f7dc !important;
        font-size: 16px;
    }

    /* Label styling */
    label {
        color: #eaffea !important;
        font-size: 16px;
        font-weight: 600;
    }

    /* Input boxes */
    input {
        border-radius: 8px !important;
        border: 2px solid #2ecc71 !important;
        background-color: #ecfdf3 !important;
    }

    /* Button styling */
    div.stButton > button {
        background-color: #2ecc71;
        color: #0b3d2e;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 25px;
        border: none;
    }

    div.stButton > button:hover {
        background-color: #1e8449;
        color: white;
        transition: 0.3s ease-in-out;
    }

    /* Prediction output */
    .stSuccess {
        background-color: rgba(0, 50, 30, 0.7);
        color: #b9ffda;
        font-size: 18px;
        border-radius: 12px;
        border-left: 6px solid #2ecc71;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOAD MODEL ----------------
with open("sales_model.pkl", "rb") as file:
    model = pickle.load(file)

# ---------------- APP UI ----------------
st.title("📈 Sales Prediction using Machine Learning")

st.markdown(
    "<p style='text-align:center;'>"
    "Predict future product sales based on advertising investment"
    "</p>",
    unsafe_allow_html=True
)

tv = st.number_input("📺 TV Advertising Budget", min_value=0.0)
radio = st.number_input("📻 Radio Advertising Budget", min_value=0.0)
newspaper = st.number_input("📰 Newspaper Advertising Budget", min_value=0.0)

if st.button("🔮 Predict Sales"):
    input_data = np.array([[tv, radio, newspaper]])
    prediction = model.predict(input_data)
    st.success(f"💰 Predicted Sales: {prediction[0]:.2f}")
