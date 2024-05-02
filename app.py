import streamlit as st
import pandas as pd
import pickle

# Load scaler and model using pickle
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Streamlit app

st.markdown("""
    <div style='text-align: center;'>
        <h2>About This Stress Predictor App</h2>
        <p>This stress predictor app is designed to provide an estimation of stress levels based on input parameters. It's important to note that the model used in this app may not be 100% accurate, and stress levels can vary greatly between individuals and situations.</p>
        <p>The predicted stress level provided by this app is on a scale from 3 to 8, where 3 indicates low stress and 8 indicates high stress. However, it's essential to interpret the results with caution and seek professional advice if necessary.</p>
    </div>
""", unsafe_allow_html=True)
# Input form to take user input
st.sidebar.header('Enter Patient Information')
gender = st.sidebar.selectbox('Gender', ['Male','Female'])
age = st.sidebar.number_input('Age', min_value=0, max_value=120, value=30)
sleep_duration = st.sidebar.number_input('Sleep Duration', min_value=0, max_value=24, value=7)
quality_of_sleep = st.sidebar.slider('Quality of Sleep', min_value=1, max_value=10, value=5)
physical_activity_level = st.sidebar.slider('Physical Activity Level', min_value=1, max_value=10, value=5)
bmi_category = st.sidebar.selectbox('BMI Category', ['Normal Weight','Under Weight', 'Overweight', 'Obese'])
blood_pressure = st.sidebar.text_input('Blood Pressure (sbp/dbp)',value=120/80)
heart_rate = st.sidebar.number_input('Heart Rate', min_value=0, max_value=300, value=70)
daily_steps = st.sidebar.number_input('Daily Steps', min_value=0, value=5000)
sleep_disorder = st.sidebar.selectbox('sleep disorder', ['NaN', 'Sleep Apnea', 'Insomnia'])

# Make prediction
if st.sidebar.button('Predict'):
    # Prepare input data
    input_data = pd.DataFrame({
        'Gender': [1 if gender == 'Male' else 0],
        'Age': [age],
        'Sleep Duration': [sleep_duration],
        'Quality of Sleep': [quality_of_sleep],
        'Physical Activity Level': [physical_activity_level],
        'BMI Category': [bmi_category],
        'Blood Pressure': [blood_pressure],
        'Heart Rate': [heart_rate],
        'Daily Steps': [daily_steps],
        'Sleep Disorder':[sleep_disorder]
    })
    df = pd.DataFrame(input_data)
    df['BMI Category'] = df['BMI Category'].map({'Under Weight':0,'Normal Weight':1,'Overweight':2,'Obese':3})
    df['SBP'] = ''
    df['DBP'] = ''
    for i in range(len(df)):
        k = df['Blood Pressure'][i].split("/")[0]
        j = df['Blood Pressure'][i].split("/")[1]
        df['SBP'][i] = k
        df['DBP'][i] = j
    df.drop(columns='Blood Pressure',inplace=True)
    df['Sleep_Disorder_Insomnia']=''
    df['Sleep_Disorder_Sleep Apnea']=''
    if(sleep_disorder=='Insomnia'):
        df['Sleep_Disorder_Insomnia']= 1
        df['Sleep_Disorder_Sleep Apnea']=0
    elif(sleep_disorder=='Sleep Apnea'):
        df['Sleep_Disorder_Sleep Apnea']=1
        df['Sleep_Disorder_Insomnia'] = 0
    else:
        df['Sleep_Disorder_Sleep Apnea']=0
        df['Sleep_Disorder_Insomnia'] = 0
    df.drop(columns='Sleep Disorder',inplace=True)
    # Scale input data
    input_data_scaled = scaler.transform(df)

    
    # Make prediction
    prediction = model.predict(input_data_scaled)
    stress_level = prediction[0]
    # Display prediction result
    st.markdown(f"<h3 style='text-align: center;'>Predicted Stress Level: {stress_level}</h3>", unsafe_allow_html=True)