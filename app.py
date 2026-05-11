import streamlit as st
import pandas as pd
import pickle
from database import add_user, login_user

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AAC Diabetes Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD MODEL ----------------

model = pickle.load(open("diabetes_model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #334155;
}

/* Main Container */

.main-container {
    background: rgba(255,255,255,0.05);
    padding: 35px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
    margin-top: 20px;
}

/* Headings */

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    color: #38bdf8;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #cbd5e1;
    margin-bottom: 30px;
}

/* Input Boxes */

.stTextInput input,
.stNumberInput input {
    background-color: #f8fafc !important;
    color: black !important;
    border-radius: 12px !important;
    border: 1px solid #94a3b8 !important;
    padding: 10px !important;
}

/* Buttons */

.stButton > button {
    width: 100%;
    background: linear-gradient(to right, #0ea5e9, #2563eb);
    color: white;
    border: none;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(to right, #0284c7, #1d4ed8);
}

/* Prediction Card */

.result-box {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    margin-top: 20px;
}

.low-risk {
    background-color: rgba(34,197,94,0.2);
    border: 2px solid #22c55e;
    color: #22c55e;
}

.high-risk {
    background-color: rgba(239,68,68,0.2);
    border: 2px solid #ef4444;
    color: #ef4444;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3774/3774299.png",
    width=120
)

st.sidebar.title("AAC Healthcare")

menu = ["Login", "Signup"]

choice = st.sidebar.radio("Navigation", menu)

# ---------------- SIGNUP PAGE ----------------

if choice == "Signup":

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown(
        '<div class="main-title">Create Account</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Register to access the Diabetes Prediction System</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        new_user = st.text_input("Username")

        new_password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Create Account"):

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

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown(
        '<div class="main-title">AAC Diabetes Predictor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">AI Powered Diabetes Risk Detection System</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login Securely"):

            result = login_user(username, password)

            if result:

                st.success(f"Welcome, {username}")

                st.markdown("---")

                st.subheader("Patient Health Information")

                c1, c2 = st.columns(2)

                with c1:

                    preg = st.number_input(
                        "Pregnancies",
                        0,
                        20,
                        1
                    )

                    glucose = st.number_input(
                        "Glucose Level",
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

                with c2:

                    insulin = st.number_input(
                        "Insulin Level",
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

                st.markdown("")

                if st.button("Predict Diabetes Risk"):

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

                    if prediction[0] == 1:

                        st.markdown(
                            """
                            <div class="result-box high-risk">
                            ⚠️ High Risk of Diabetes
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            """
                            <div class="result-box low-risk">
                            ✅ Low Risk of Diabetes
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            else:

                st.error("Invalid Username or Password")

    st.markdown('</div>', unsafe_allow_html=True)
