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

    # Download button
    meal_data = pd.read_csv("data/food_entries.csv")
    st.download_button(label="Download Food Entry Data as CSV", data=meal_data.to_csv(index=False), file_name="food_entries.csv")
    st.dataframe(meal_data)


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

    # Download button
    symptom_data = pd.read_csv("data/symptoms.csv")
    st.download_button(label="Download Symptom Data as CSV", data=symptom_data.to_csv(index=False), file_name="symptoms.csv")
    st.dataframe(symptom_data)

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

    # Download button
    emotion_data = pd.read_csv("data/emotions.csv")
    st.download_button(label="Download Emotion Data as CSV", data=emotion_data.to_csv(index=False), file_name="emotions.csv")
    st.dataframe(emotion_data)


# Data Visualization and Analysis
def visualize_data(meal_data, symptoms_data, emotions_data):
    st.subheader("Data Visualization and Analysis")
    
    # Convert timestamps
    meal_data['timestamp'] = pd.to_datetime(meal_data['timestamp'])
    symptoms_data['timestamp'] = pd.to_datetime(symptoms_data['timestamp'])
    emotions_data['timestamp'] = pd.to_datetime(emotions_data['timestamp'])
    
    # Combine data for correlation analysis
    combined_data = pd.merge(meal_data, symptoms_data, how='outer', on='timestamp').merge(emotions_data, how='outer', on='timestamp')
    
    # Time Series Analysis
    st.write("Time Series Analysis")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(meal_data['timestamp'], meal_data.index, label="Meal Entries")
    ax.plot(symptoms_data['timestamp'], symptoms_data.index, label="Symptom Occurrences")
    ax.plot(emotions_data['timestamp'], emotions_data.index, label="Emotion Occurrences")
    ax.set_xlabel("Date")
    ax.set_ylabel("Frequency")
    ax.set_title("Frequency of Meal, Symptom, and Emotion Entries Over Time")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Correlation Analysis
    st.write("Correlation Analysis")
    combined_data_corr = combined_data.corr(numeric_only=True)
    st.write(combined_data_corr)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(combined_data_corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)

    # Meal Type vs Symptom and Emotion Severity
    st.write("Meal Type vs Symptom and Emotion Severity")
    meal_severity = pd.merge(meal_data, symptoms_data[['timestamp', 'severity']], on='timestamp', how='left')
    meal_severity = pd.merge(meal_severity, emotions_data[['timestamp', 'severity']], on='timestamp', suffixes=('_symptom', '_emotion'), how='left')

    # Drop rows with missing values in required columns
    meal_severity = meal_severity.dropna(subset=['meal_type', 'severity_symptom', 'severity_emotion'])

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='meal_type', y='severity_symptom', data=meal_severity, ax=ax)
    ax.set_title("Meal Type vs Symptom Severity")
    ax.set_xlabel("Meal Type")
    ax.set_ylabel("Severity")
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='meal_type', y='severity_emotion', data=meal_severity, ax=ax)
    ax.set_title("Meal Type vs Emotion Severity")
    ax.set_xlabel("Meal Type")
    ax.set_ylabel("Severity")
    st.pyplot(fig)

def ai_investigator():
    st.header("AI Investigator (Work In Progress)")
    st.write("Still under development, it will probably give innacurate answers :)")
    if st.checkbox("run code?"):
        import openai
        from llama_index.llms.openai import OpenAI
        try:
            from llama_index import (Document, ServiceContext,
                                    SimpleDirectoryReader, VectorStoreIndex)
        except ImportError:
            from llama_index.core import (Document, ServiceContext,
                                        SimpleDirectoryReader,
                                        VectorStoreIndex)

        # st.set_page_config(page_title="Chat with the Streamlit docs, powered by LlamaIndex", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
        openai.api_key = st.secrets.openai_key
        if "messages" not in st.session_state.keys(): # Initialize the chat messages history
            st.session_state.messages = [
                {"role": "assistant", "content": "Ask me a question about the meals eaten or any symptoms!"}
            ]

        @st.cache_resource(show_spinner=False)
        def load_data():
            with st.spinner(text="Loading and indexing the data – hang tight! This should take a few seconds."):
                reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
                docs = reader.load_data()
                # llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert o$
                # index = VectorStoreIndex.from_documents(docs)
                service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert in statistics, meals and allergies. You answer questions base on two datasets: food entries and symptoms. Do not claim anything that can not be backed up by statistics or data."))
                index = VectorStoreIndex.from_documents(docs, service_context=service_context)
                return index

        index = load_data()

        if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
                st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

        if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

        for message in st.session_state.messages: # Display the prior chat messages
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # If last message is not from assistant, generate a new response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chat_engine.chat(prompt)
                    st.write(response.response)
                    message = {"role": "assistant", "content": response.response}
                    st.session_state.messages.append(message) # Add response to message history




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
