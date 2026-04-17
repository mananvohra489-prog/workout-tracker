import streamlit as st
import pandas as pd
import os
from datetime import date

# Initialize the database file
DATA_FILE = "workout_progress.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Session", "Exercise", "Weight (kg)", "Sets", "Reps", "Notes"])
    df.to_csv(DATA_FILE, index=False)

st.title("🏋️ 6-Day Custom Split Tracker")

# Sidebar for logging
st.sidebar.header("Log Today's Workout")

session_options = [
    "Chest & Biceps A", 
    "Back & Triceps A", 
    "Legs & Shoulders A",
    "Chest & Biceps B", 
    "Back & Triceps B", 
    "Legs & Shoulders B",
    "Custom / Single Muscle"  # NEW OPTION ADDED HERE
]

session_type = st.sidebar.selectbox("Session Type", session_options)
exercise = st.sidebar.text_input("Exercise Name")
weight = st.sidebar.number_input("Weight (kg)", min_value=0.0, step=2.5)
sets = st.sidebar.number_input("Sets", min_value=1, step=1)
reps = st.sidebar.number_input("Reps", min_value=1, step=1)
notes = st.sidebar.text_input("Notes (e.g., 'Chest only', 'Felt heavy')") # NEW NOTES FIELD

if st.sidebar.button("Log Lift"):
    if exercise:
        new_data = pd.DataFrame({
            "Date": [date.today()],
            "Session": [session_type],
            "Exercise": [exercise],
            "Weight (kg)": [weight],
            "Sets": [sets],
            "Reps": [reps],
            "Notes": [notes]
        })
        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
        st.sidebar.success(f"Logged {exercise}!")
    else:
        st.sidebar.error("Please enter an exercise name.")

st.markdown("---")

# Dashboard
st.header("📈 Strength Progress")
df = pd.read_csv(DATA_FILE)

if not df.empty:
    exercise_list = df["Exercise"].unique()
    selected_exercise = st.selectbox("Select Exercise to View Progress", exercise_list)
    filtered_df = df[df["Exercise"] == selected_exercise]
    
    st.line_chart(filtered_df.set_index("Date")["Weight (kg)"])
    
    st.write("Recent History")
    # Displaying notes in the history table
    st.dataframe(filtered_df[["Date", "Weight (kg)", "Sets", "Reps", "Notes"]].tail(5))
else:
    st.info("No data logged yet.")
