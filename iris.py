import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# ---------------------------------------------------
# Page configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Iris Flower Classification",
    page_icon="🌸",
    layout="centered"
)

# ---------------------------------------------------
# Dark Green & Light Pink Styling
# ---------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f3d2e, #1b5e20, #fce4ec, #f8bbd0);
    background-size: 400% 400%;
    animation: gradientBG 16s ease infinite;
    font-family: 'Segoe UI', sans-serif;
}
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.block-container {
    background: linear-gradient(
        135deg,
        rgba(20, 83, 45, 0.85),
        rgba(252, 228, 236, 0.80)
    );
    border-radius: 22px;
    padding: 2rem;
    backdrop-filter: blur(14px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
}
h1, h2, h3 { color: #ecfdf5; text-align: center; }
p { color: #fce7f3; text-align: center; }
.stButton > button {
    background: linear-gradient(90deg, #14532d, #f472b6);
    color: #ffffff;
    border-radius: 14px;
    padding: 0.6em 2em;
    font-size: 16px;
    font-weight: bold;
    border: none;
    transition: 0.4s ease;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #f472b6, #14532d);
    transform: scale(1.05);
}
input { border-radius: 10px !important; }
.stAlert { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Load dataset
# ---------------------------------------------------
df = pd.read_csv(r"C:\Users\LENOVO\Downloads\archive (30)\Iris.csv")
if 'Id' in df.columns:
    df = df.drop(columns=['Id'])

# Encode species
le = LabelEncoder()
df['Species'] = le.fit_transform(df['Species'])

# Features & target
X = df[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]
y = df['Species']

# ---------------------------------------------------
# Train/Test split
# ---------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------------------------------
# Cached model training
# ---------------------------------------------------
@st.cache_data
def train_knn(X_train, y_train, n_neighbors=5):
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(X_train, y_train)
    return model

model = train_knn(X_train, y_train)

# Evaluate model on test set
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# ---------------------------------------------------
# Streamlit UI
# ---------------------------------------------------
st.title("🌿🌸  Iris Flower Classification")

st.markdown(f"""
### 🤖 Floral Intelligence System


🌱🌸 **Species Identified**
- Setosa  
- Versicolor  
- Virginica  

💡 **Model Accuracy on Test Data:** **{accuracy*100:.2f}%**
""")

st.markdown("---")

# Input section
sepal_length = st.number_input("Sepal Length (cm)", value=5.1)
sepal_width  = st.number_input("Sepal Width (cm)", value=3.5)
petal_length = st.number_input("Petal Length (cm)", value=1.4)
petal_width  = st.number_input("Petal Width (cm)", value=0.2)

# Prediction
if st.button("🌿🌸 Predict Species"):
    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = model.predict(input_data)
    probabilities = model.predict_proba(input_data)[0]
    predicted_species = le.inverse_transform(prediction)[0]
    confidence = np.max(probabilities) * 100

    st.success(f"🌸 Predicted Species: **{predicted_species}**")
    st.info(f"🤖 Confidence Level: **{confidence:.2f}%**")

    # Show probability bar chart
    st.markdown("### 📊 Prediction Probabilities")
    prob_df = pd.DataFrame({
        "Species": le.inverse_transform(np.arange(len(probabilities))),
        "Probability": probabilities
    })
    fig, ax = plt.subplots()
    ax.barh(prob_df["Species"], prob_df["Probability"], color=["#f472b6", "#14532d", "#f9a8d4"])
    ax.set_xlim(0,1)
    ax.set_xlabel("Probability")
    ax.set_title("Species Probability Distribution")
    st.pyplot(fig)


