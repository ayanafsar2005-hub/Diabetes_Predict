import streamlit as st
import pandas as pd
import pickle

from database import add_user, login_user

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AAC Diabetes Prediction System",
    page_icon="Medical",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------

model = pickle.load(open("diabetes_model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {
    background-color: #eef2f7;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #0f172a;
    color: white;
}

/* Main Card */

.main-container {
    background-color: white;
    padding: 35px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
    margin-top: 20px;
}

/* Title */

.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    font-size: 17px;
    color: #64748b;
    margin-bottom: 30px;
}

/* Input Labels */

label {
    font-weight: 600 !important;
    color: #1e293b !important;
}

/* Inputs */

.stTextInput input,
.stNumberInput input {
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
    padding: 10px !important;
    background-color: #f8fafc !important;
}

/* Buttons */

.stButton > button {
    width: 100%;
    height: 48px;
    border-radius: 10px;
    border: none;
    background-color: #2563eb;
    color: white;
    font-size: 16px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

/* Result Box */

.result-success {
    padding: 18px;
    border-radius: 10px;
    background-color: #dcfce7;
    color: #166534;
    font-size: 20px;
    font-weight: 600;
    text-align: center;
    margin-top: 20px;
}

.result-danger {
    padding: 18px;
    border-radius: 10px;
    background-color: #fee2e2;
    color: #991b1b;
    font-size: 20px;
    font-weight: 600;
    text-align: center;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.title("AAC Healthcare")

menu = ["Login", "Signup"]

choice = st.sidebar.radio("Navigation", menu)

# ---------------- SIGNUP ----------------

if choice == "Signup":

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown(
        '<div class="main-title">Create Account</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Register to access the diabetes prediction system</div>',
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

            if not new_user or not new_password:
                st.warning("Please fill all fields")

            elif new_password != confirm_password:
                st.error("Passwords do not match")

            else:

                add_user(new_user, new_password)

                st.success("Account created successfully")
                st.info("Go to the login page")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LOGIN ----------------

elif choice == "Login":

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown(
        '<div class="main-title">AAC Diabetes Prediction System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Machine Learning Based Diabetes Risk Prediction</div>',
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

            st.subheader("Patient Information")

            col1, col2 = st.columns(2)

            with col1:

                preg = st.number_input(
                    "Pregnancies",
                    min_value=0,
                    max_value=20,
                    value=1
                )

                glucose = st.number_input(
                    "Glucose",
                    min_value=0,
                    max_value=300,
                    value=120
                )

                bp = st.number_input(
                    "Blood Pressure",
                    min_value=0,
                    max_value=150,
                    value=70
                )

                skin = st.number_input(
                    "Skin Thickness",
                    min_value=0,
                    max_value=100,
                    value=20
                )

            with col2:

                insulin = st.number_input(
                    "Insulin",
                    min_value=0,
                    max_value=900,
                    value=80
                )

                bmi = st.number_input(
                    "BMI",
                    min_value=0.0,
                    max_value=70.0,
                    value=25.0
                )

                dpf = st.number_input(
                    "Diabetes Pedigree Function",
                    min_value=0.0,
                    max_value=3.0,
                    value=0.5
                )

                age = st.number_input(
                    "Age",
                    min_value=1,
                    max_value=100,
                    value=30
                )

            st.markdown("")

            if st.button("Predict Diabetes"):

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
                        <div class="result-danger">
                        High Risk of Diabetes
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        """
                        <div class="result-success">
                        Low Risk of Diabetes
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        else:

            st.error("Invalid Username or Password")

    st.markdown('</div>', unsafe_allow_html=True)
