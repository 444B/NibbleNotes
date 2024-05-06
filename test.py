import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Brunch", "Lunch", "Dinner", "Snack"])
    food_consumed = st.text_input("Food Consumed")
    optional_notes = st.text_area("Optional Notes")
    
    # Sanitize inputs
    food_consumed = food_consumed.replace(',', '')
    optional_notes = optional_notes.replace(',', '')
    
    if st.button("Log Meal"):
        if optional_notes.strip() == "":
            optional_notes = None
        datetime_entry = datetime.combine(meal_date, meal_time)
        new_entry = {'timestamp': datetime_entry, 'meal_type': meal_type, 'food_consumed': food_consumed, 'optional_notes': optional_notes}
        new_entry_df = pd.DataFrame([new_entry])
        new_entry_df.to_csv("data/food_entries.csv", mode='a', header=not os.path.exists("data/food_entries.csv"), index=False)
        st.success("Meal logged successfully!")


def log_symptom():
    st.subheader("Symptoms Logging")
    symptom_date, symptom_time = create_date_time_input("Symptom")
    symptom_type = st.selectbox("Symptom Type", ["Stomachache", "Headache", "Nausea", "Fatigue", "Other"])
    severity = st.slider("Severity", min_value=1, max_value=10)
    symptom_notes = st.text_area("Symptom Notes")
    
    # Sanitize input
    symptom_notes = symptom_notes.replace(',', '')
    
    if st.button("Log Symptom"):
        if symptom_notes.strip() == "":
            symptom_notes = None
        datetime_entry = datetime.combine(symptom_date, symptom_time)
        new_symptom = {'timestamp': datetime_entry, 'symptom_type': symptom_type, 'severity': severity, 'notes': symptom_notes}
        new_symptom_df = pd.DataFrame([new_symptom])
        new_symptom_df.to_csv("data/symptoms.csv", mode='a', header=not os.path.exists("data/symptoms.csv"), index=False)
        st.success("Symptom logged successfully!")


def log_emotion():
    st.subheader("Emotion Logging")
    emotion_date, emotion_time = create_date_time_input("Emotion")
    emotion_type = st.selectbox("Emotion Type", ["Anxious", "Depressed", "Overwhelmed", "Bored", "Doom scrolling", "Other"])
    severity = st.slider("Intensity", min_value=1, max_value=10)
    emotion_notes = st.text_area("Emotion Notes")

    # Sanitize input
    emotion_notes = emotion_notes.replace(',', '')

    if st.button("Log Emotion"):
        if emotion_notes.strip() == "":
            emotion_notes = None
        datetime_entry = datetime.combine(emotion_date, emotion_time)
        new_emotion= {'timestamp': datetime_entry, 'emotion_type': emotion_type, 'severity': severity, 'notes': emotion_notes}
        new_emotion_df = pd.DataFrame([new_emotion])
        new_emotion_df.to_csv("data/emotions.csv", mode='a', header=not os.path.exists("data/emotions.csv"), index=False)
        st.success("Emotion logged successfully!")


# Data Visualization and Analysis
def visualize_data(meal_data, symptoms_data, emotions_data):
    st.subheader("Data Visualization and Analysis")
    
    # Meal Data Analysis
    st.write("Meal Entries Data")
    st.write(meal_data.describe())  # Basic statistics
    st.write("Meal Types Distribution")
    st.write(meal_data['meal_type'].value_counts())  # Count of meal types
    st.write("Top 5 Most Consumed Foods")
    st.write(meal_data['food_consumed'].value_counts().head())  # Most consumed foods

    # Visualize Meal Types Distribution
    st.write("Meal Types Distribution")
    meal_type_counts = meal_data['meal_type'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=meal_type_counts.index, y=meal_type_counts.values, ax=ax)
    ax.set_xlabel("Meal Type")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Meal Types")
    st.pyplot(fig)

    # Symptom Data Analysis
    st.write("Symptoms Data")
    st.write(symptoms_data.describe())  # Basic statistics
    st.write("Symptom Types Distribution")
    st.write(symptoms_data['symptom_type'].value_counts())  # Count of symptom types

    # Visualize Symptom Types Distribution
    st.write("Symptom Types Distribution")
    symptom_type_counts = symptoms_data['symptom_type'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=symptom_type_counts.index, y=symptom_type_counts.values, ax=ax)
    ax.set_xlabel("Symptom Type")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Symptom Types")
    st.pyplot(fig)

    # Emotion Data Analysis
    st.write("Emotions Data")
    st.write(emotions_data.describe())  # Basic statistics
    st.write("Emotion Types Distribution")
    st.write(emotions_data['emotion_type'].value_counts())  # Count of symptom types

    # Time-Series Analysis
    st.write("Time-Series Analysis")
    meal_data['timestamp'] = pd.to_datetime(meal_data['timestamp'])
    symptoms_data['timestamp'] = pd.to_datetime(symptoms_data['timestamp'])

    # Plot frequency of meal entries and symptom occurrences over time
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(meal_data['timestamp'], meal_data.index, label="Meal Entries")
    ax.plot(symptoms_data['timestamp'], symptoms_data.index, label="Symptom Occurrences")
    ax.set_xlabel("Date")
    ax.set_ylabel("Frequency")
    ax.set_title("Frequency of Meal Entries and Symptom Occurrences Over Time")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)


# UI
def main():
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Meal Entry Form", "Symptoms Logging", "Emotion Logging", "Data Visualization and Analysis", "AI Investigator (WIP)"])
        with tab1:
            log_meal()
        with tab2:
            log_symptom()
        with tab3:
            log_emotion()
        with tab4:
            meal_data = pd.read_csv("data/food_entries.csv")
            symptoms_data = pd.read_csv("data/symptoms.csv")
            emotions_data = pd.read_csv("data/emotions.csv")
            visualize_data(meal_data, symptoms_data, emotions_data)
        with tab5:
            ai_investigator()

if __name__ == "__main__":
    main()
