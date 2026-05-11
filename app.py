import streamlit as st
import pandas as pd
import pickle

from database import add_user, login_user

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AAC Diabetes Predictor",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------

model = pickle.load(open("diabetes_model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

body {
    font-family: Arial, sans-serif;
}

.stApp {
    background-color: #f4f6f9;
}

/* Main Container */

.main-box {
    background-color: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.1);
    margin-top: 20px;
}

/* Title */

.title {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    color: #1f2937;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #6b7280;
    margin-bottom: 30px;
}

/* Buttons */

.stButton > button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    height: 45px;
    font-size: 16px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

/* Input Fields */

.stTextInput input,
.stNumberInput input {
    border-radius: 8px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #1f2937;
}

section[data-testid="stSidebar"] .css-1d391kg {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.title("AAC Diabetes Predictor")

menu = ["Login", "Signup"]

choice = st.sidebar.selectbox("Menu", menu)

# ---------------- SIGNUP PAGE ----------------

if choice == "Signup":

    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    st.markdown(
        '<div class="title">Create Account</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Register to access the system</div>',
        unsafe_allow_html=True
    )

    new_user = st.text_input("Username")

    new_password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Signup"):

        if new_user == "" or new_password == "":
            st.warning("Please fill all fields")

        elif new_password != confirm_password:
            st.error("Passwords do not match")

        else:

            add_user(new_user, new_password)

            st.success("Account created successfully")
            st.info("Go to Login Page")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LOGIN PAGE ----------------

elif choice == "Login":

    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    st.markdown(
        '<div class="title">AAC Diabetes Predictor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Login to continue</div>',
        unsafe_allow_html=True
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        result = login_user(username, password)

        if result:

            st.success(f"Welcome {username}")

            st.markdown("---")

            st.subheader("Patient Details")

            col1, col2 = st.columns(2)

            with col1:

                preg = st.number_input(
                    "Pregnancies",
                    0,
                    20,
                    1
                )

                glucose = st.number_input(
                    "Glucose",
                    0,
                    300,
                    120
                )

                bp = st.number_input(
                    "Blood Pressure",
                    0,
                    150,
                    70
                )

                skin = st.number_input(
                    "Skin Thickness",
                    0,
                    100,
                    20
                )

            with col2:

                insulin = st.number_input(
                    "Insulin",
                    0,
                    900,
                    80
                )

                bmi = st.number_input(
                    "BMI",
                    0.0,
                    70.0,
                    25.0
                )

                dpf = st.number_input(
                    "Diabetes Pedigree Function",
                    0.0,
                    3.0,
                    0.5
                )

                age = st.number_input(
                    "Age",
                    1,
                    100,
                    30
                )

            if st.button("Predict"):

                input_data = pd.DataFrame({

                    "Pregnancies": [preg],
                    "Glucose": [glucose],
                    "BloodPressure": [bp],
                    "SkinThickness": [skin],
                    "Insulin": [insulin],
                    "BMI": [bmi],
                    "DiabetesPedigreeFunction": [dpf],
                    "Age": [age]

                })

                input_data = input_data.reindex(
                    columns=columns,
                    fill_value=0
                )

                prediction = model.predict(input_data)

                st.markdown("---")

                if prediction[0] == 1:

                    st.error(
                        "High Risk of Diabetes"
                    )

                else:

                    st.success(
                        "Low Risk of Diabetes"
                    )

        else:

            st.error(
                "Invalid Username or Password"
            )

    st.markdown('</div>', unsafe_allow_html=True)
