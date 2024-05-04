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


# UI
def main():
    meal_data = pd.read_csv("food_entries.csv")

    log_meal()

if __name__ == "__main__":
    main()
