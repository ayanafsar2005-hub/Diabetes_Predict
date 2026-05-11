import streamlit as st
import pandas as pd
import pickle

from database import add_user, login_user

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AAC Diabetes Predictor",
    page_icon="💙",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background: linear-gradient(to right, #141e30, #243b55);
}

.stApp {
    background: linear-gradient(to right, #141e30, #243b55);
    color: white;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #00F5FF;
    padding-bottom: 10px;
}

.sub {
    text-align: center;
    color: #dddddd;
    margin-bottom: 30px;
}

div.stButton > button {
    width: 100%;
    background-color: #00C9A7;
    color: white;
    font-size: 18px;
    border-radius: 10px;
    height: 50px;
    border: none;
}

div.stButton > button:hover {
    background-color: #00F5FF;
    color: black;
}

.stTextInput > div > div > input {
    background-color: #f0f2f6;
    color: black;
    border-radius: 10px;
}

.stNumberInput > div > div > input {
    background-color: #f0f2f6;
    color: black;
    border-radius: 10px;
}

.css-1d391kg {
    background-color: #1b263b;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------

model = pickle.load(open('diabetes_model.pkl', 'rb'))
columns = pickle.load(open('columns.pkl', 'rb'))

# ---------------- SIDEBAR ----------------

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2966/2966486.png",
    width=100
)

st.sidebar.title("🔐 Navigation")

menu = ["Login", "Signup"]

choice = st.sidebar.selectbox("Select Option", menu)

# ---------------- SIGNUP PAGE ----------------

if choice == "Signup":

    st.markdown(
        '<div class="title">📝 Create Account</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub">Signup to continue</div>',
        unsafe_allow_html=True
    )

    new_user = st.text_input("👤 Username")

    new_password = st.text_input(
        "🔑 Password",
        type='password'
    )

    if st.button("✨ Signup"):

        if new_user == "" or new_password == "":
            st.warning("⚠️ Please fill all fields")

        else:
            add_user(new_user, new_password)

            st.success("✅ Account Created Successfully")
            st.info("👉 Go to Login Page")

# ---------------- LOGIN PAGE ----------------

elif choice == "Login":

    st.markdown(
        '<div class="title">💙 AAC Diabetes Predictor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub">Login to continue</div>',
        unsafe_allow_html=True
    )

    username = st.text_input("👤 Username")

    password = st.text_input(
        "🔑 Password",
        type='password'
    )

    if st.button("🚀 Login"):

        result = login_user(username, password)

        if result:

            st.success(f"✅ Welcome {username}")

            st.markdown("---")

            st.header("🩺 Enter Patient Details")

            preg = st.number_input(
                'Pregnancies',
                0,
                20,
                1
            )

            glucose = st.number_input(
                'Glucose',
                0,
                300,
                120
            )

            bp = st.number_input(
                'Blood Pressure',
                0,
                150,
                70
            )

            skin = st.number_input(
                'Skin Thickness',
                0,
                100,
                20
            )

            insulin = st.number_input(
                'Insulin',
                0,
                900,
                80
            )

            bmi = st.number_input(
                'BMI',
                0.0,
                70.0,
                25.0
            )

            dpf = st.number_input(
                'Diabetes Pedigree Function',
                0.0,
                3.0,
                0.5
            )

            age = st.number_input(
                'Age',
                1,
                100,
                30
            )

            if st.button('🔍 Predict'):

                input_data = pd.DataFrame({

                    'Pregnancies': [preg],
                    'Glucose': [glucose],
                    'BloodPressure': [bp],
                    'SkinThickness': [skin],
                    'Insulin': [insulin],
                    'BMI': [bmi],
                    'DiabetesPedigreeFunction': [dpf],
                    'Age': [age]

                })

                input_data = input_data.reindex(
                    columns=columns,
                    fill_value=0
                )

                prediction = model.predict(input_data)

                st.markdown("---")

                if prediction[0] == 1:

                    st.error(
                        "⚠️ High Risk of Diabetes"
                    )

                    st.image(
                        "https://cdn-icons-png.flaticon.com/512/2785/2785482.png",
                        width=150
                    )

                else:

                    st.success(
                        "✅ Low Risk of Diabetes"
                    )

                    st.image(
                        "https://cdn-icons-png.flaticon.com/512/190/190411.png",
                        width=150
                    )

        else:

            st.error(
                "❌ Invalid Username or Password"
            )
