import streamlit as st
import pandas as pd
from datetime import datetime
import os

def create_date_time_input(label):
    date_key = label + "_date"
    time_key = label + "_time"
    date = st.date_input(label + " Date", key=date_key)
    time = st.time_input(label + " Time", key=time_key)
    return date, time

def log_meal():
    st.subheader("Meal Entry")
    meal_date, meal_time = create_date_time_input("Meal")
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
    food_consumed = st.text_input("Food Consumed")
    optional_notes = st.text_area("Optional Notes")
    if st.button("Log Meal"):
        if optional_notes.strip() == "":
            optional_notes = None
        datetime_entry = datetime.combine(meal_date, meal_time)
        new_entry = {'timestamp': datetime_entry, 'meal_type': meal_type, 'food_consumed': food_consumed, 'optional_notes': optional_notes}
        new_entry_df = pd.DataFrame([new_entry])
        new_entry_df.to_csv("food_entries.csv", mode='a', header=not os.path.exists("food_entries.csv"), index=False)
        st.success("Meal logged successfully!")


def log_symptom():
    st.subheader("Symptoms Logging")
    symptom_date, symptom_time = create_date_time_input("Symptom")
    symptom_type = st.selectbox("Symptom Type", ["Stomachache", "Headache", "Nausea", "Fatigue", "Other"])
    severity = st.slider("Severity", min_value=1, max_value=10)
    symptom_notes = st.text_area("Symptom Notes")
    if st.button("Log Symptom"):
        if symptom_notes.strip() == "":
            symptom_notes = None
        datetime_entry = datetime.combine(symptom_date, symptom_time)
        new_symptom = {'timestamp': datetime_entry, 'symptom_type': symptom_type, 'severity': severity, 'notes': symptom_notes}
        new_symptom_df = pd.DataFrame([new_symptom])
        new_symptom_df.to_csv("symptoms.csv", mode='a', header=not os.path.exists("symptoms.csv"), index=False)
        st.success("Symptom logged successfully!")

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
        meal_data = log_meal()
    with tab2:
        symptoms_data = log_symptom()
    with tab3:
        visualize_data(meal_data, symptoms_data)

if __name__ == "__main__":
    main()
