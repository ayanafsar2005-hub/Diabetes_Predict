import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open('diabetes_model.pkl', 'rb'))
columns = pickle.load(open('columns.pkl', 'rb'))

st.title('Diabetes Predictor')
st.write('Enter patient details below')

preg = st.number_input('Pregnancies', 0, 20, 1)
glucose = st.number_input('Glucose', 0, 300, 120)
bp = st.number_input('Blood Pressure', 0, 150, 70)
skin = st.number_input('Skin Thickness', 0, 100, 20)
insulin = st.number_input('Insulin', 0, 900, 80)
bmi = st.number_input('BMI', 0.0, 70.0, 25.0)
dpf = st.number_input('Diabetes Pedigree Function', 0.0, 3.0, 0.5)
age = st.number_input('Age', 1, 100, 30)

if st.button('Predict'):

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

    # Match training columns
    input_data = input_data.reindex(columns=columns, fill_value=0)

    # Prediction
    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.error('⚠️ High Risk of Diabetes')
    else:
        st.success('✅ Low Risk of Diabetes')