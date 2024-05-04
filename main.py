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

# Data Visualization and Analysis
def visualize_data(meal_data, symptoms_data):
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

def ai_investigator():
    st.header("AI Investigator")
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
        tab1, tab2, tab3, tab4= st.tabs(["Meal Entry Form", "Symptoms Logging", "Data Visualization and Analysis", "AI Investigator"])
        with tab1:
            log_meal()
        with tab2:
            log_symptom()
        with tab3:
            meal_data = pd.read_csv("data/food_entries.csv")
            symptoms_data = pd.read_csv("data/symptoms.csv")
            visualize_data(meal_data, symptoms_data)
        with tab4:
            ai_investigator()

if __name__ == "__main__":
    main()
