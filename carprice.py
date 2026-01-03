import streamlit as st
import numpy as np
import joblib

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Car Price Prediction",
    layout="wide"
)

# ---------- ANIMATED BACKGROUND CSS ----------
st.markdown("""
<style>

/* Animated gradient background */
.stApp {
    background: linear-gradient(-45deg, #1e3c72, #2a5298, #11998e, #38ef7d);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

/* Animation */
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Glassmorphism container */
.block-container {
    background: rgba(255, 255, 255, 0.12);
    padding: 2.5rem;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

/* Title styling */
h1 {
    color: #ffffff;
    text-align: center;
    font-weight: bold;
}

/* Subheader */
h3 {
    color: #f1f1f1;
}

/* Input labels */
label {
    color: #ffffff !important;
    font-weight: 500;
}

/* Button styling */
div.stButton > button {
    background: linear-gradient(135deg, #ff512f, #dd2476);
    color: white;
    font-size: 18px;
    border-radius: 12px;
    padding: 0.6em 1.2em;
    transition: 0.3s ease-in-out;
}

div.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #dd2476, #ff512f);
}

/* Success box */
.stAlert {
    border-radius: 12px;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# ---------- APP CONTENT ----------
st.title("🚗 Car Price Prediction System")
st.subheader("Predict car resale value using Machine Learning")

# Load model & features
model = joblib.load("model.pkl")
features = joblib.load("features.pkl")

# Inputs
year = st.number_input("Year of Purchase", min_value=1990, max_value=2025)
present_price = st.number_input("Present Price (in Lakhs)", min_value=0.0)
kms_driven = st.number_input("Kilometers Driven", min_value=0)
mileage = st.number_input("Mileage (kmpl)", min_value=0.0)

fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
owner = st.selectbox("Owner Type", ["First", "Second", "Third"])

# Encoding
fuel_map = {"CNG": 0, "Diesel": 1, "Petrol": 2}
seller_map = {"Dealer": 0, "Individual": 1}
trans_map = {"Automatic": 0, "Manual": 1}
owner_map = {"First": 0, "Second": 1, "Third": 2}

# Input array
input_data = np.array([[ 
    year,
    present_price,
    kms_driven,
    fuel_map[fuel_type],
    seller_map[seller_type],
    trans_map[transmission],
    owner_map[owner],
    mileage
]])

# Prediction
if st.button("🚀 Predict Price"):
    prediction = model.predict(input_data)
    st.success(f"💰 Estimated Car Price: ₹ {prediction[0]:.2f} Lakhs")

