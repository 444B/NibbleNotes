import streamlit as st
import pandas as pd
from datetime import datetime

def create_date_time_input(label):
    date_key = label + "_date"
    time_key = label + "_time"
    date = st.date_input(label + " Date", key=date_key)
    time = st.time_input(label + " Time", key=time_key)
    return date, time

def log_meal(meal_data):
    st.subheader("Meal Entry")
    meal_date, meal_time = create_date_time_input("Meal")
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
    food = st.text_input("Food Consumed")
    notes = st.text_area("Meal Notes")
    if st.button("Log Meal"):
        if notes.strip() == "":
            notes = None
        datetime_entry = datetime.combine(meal_date, meal_time)
        new_entry = {'datetime': pd.Timestamp(datetime_entry), 'meal_type': meal_type, 'food': food, 'notes': notes}
        meal_data = pd.concat([meal_data, pd.DataFrame([new_entry], columns=meal_data.columns)], ignore_index=True)
        meal_data.to_csv("food_entries.csv", index=False)
        st.success("Meal logged successfully!")
    return meal_data

def log_symptom(symptoms_data):
    st.subheader("Symptoms Logging")
    symptom_date, symptom_time = create_date_time_input("Symptom")
    symptom_type = st.selectbox("Symptom Type", ["Stomachache", "Headache", "Nausea", "Fatigue", "Other"])
    severity = st.slider("Severity", min_value=1, max_value=10)
    symptom_notes = st.text_area("Symptom Notes")
    if st.button("Log Symptom"):
        if symptom_notes.strip() == "":
            symptom_notes = None
        datetime_entry = datetime.combine(symptom_date, symptom_time)
        new_symptom = {'datetime': pd.Timestamp(datetime_entry), 'symptom_type': symptom_type, 'severity': severity, 'notes': symptom_notes}
        symptoms_data = pd.concat([symptoms_data, pd.DataFrame([new_symptom], columns=symptoms_data.columns)], ignore_index=True)
        symptoms_data.to_csv("symptoms.csv", index=False)
        st.success("Symptom logged successfully!")
    return symptoms_data

# Data Visualization and Analysis
def visualize_data(meal_data, symptoms_data):
    st.subheader("Data Visualization and Analysis")
    st.write("Meal Entries Data")
    st.write(meal_data)
    st.write("Symptoms Data")
    st.write(symptoms_data)
    # Add data analysis and visualization here

# UI
def main():
    meal_data = pd.read_csv("food_entries.csv")
    symptoms_data = pd.read_csv("symptoms.csv")
    
    tab1, tab2, tab3 = st.tabs(["Meal Entry Form", "Symptoms Logging", "Data Visualization and Analysis"])

    with tab1:
        meal_data = log_meal(meal_data)
    with tab2:
        symptoms_data = log_symptom(symptoms_data)
    with tab3:
        visualize_data(meal_data, symptoms_data)

if __name__ == "__main__":
    main()
