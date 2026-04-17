import streamlit as st
import pandas as pd
import os
from datetime import date

# Initialize the database file
DATA_FILE = "workout_progress.csv"

# Create the CSV if it does not exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Session", "Exercise", "Weight (kg)", "Sets", "Reps"])
    df.to_csv(DATA_FILE, index=False)

st.title("🏋️ 6-Day Custom Split Tracker")
st.write("Log your heavy lifts and track your progressive overload.")

# Sidebar for logging new data
st.sidebar.header("Log Today's Workout")

# Updated to your new Chest/Bi and Back/Tri 6-day split format
session_options = [
    "Chest & Biceps A", 
    "Back & Triceps A", 
    "Legs & Shoulders A",
    "Chest & Biceps B", 
    "Back & Triceps B", 
    "Legs & Shoulders B"
]
session_type = st.sidebar.selectbox("Session", session_options)
exercise = st.sidebar.text_input("Exercise Name (e.g., Incline Dumbbell Press)")
weight = st.sidebar.number_input("Weight (kg)", min_value=0.0, step=2.5)
sets = st.sidebar.number_input("Sets", min_value=1, step=1)
reps = st.sidebar.number_input("Reps", min_value=1, step=1)

if st.sidebar.button("Log Lift"):
    if exercise:
        new_data = pd.DataFrame({
            "Date": [date.today()],
            "Session": [session_type],
            "Exercise": [exercise],
            "Weight (kg)": [weight],
            "Sets": [sets],
            "Reps": [reps]
        })
        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
        st.sidebar.success(f"Logged {weight}kg for {exercise}!")
    else:
        st.sidebar.error("Please enter an exercise name.")

st.markdown("---")

# Main dashboard for viewing progress
st.header("📈 Strength Progress")
df = pd.read_csv(DATA_FILE)

if not df.empty:
    # Filter the chart by specific exercise
    exercise_list = df["Exercise"].unique()
    selected_exercise = st.selectbox("Select Exercise to View Progress", exercise_list)

    filtered_df = df[df["Exercise"] == selected_exercise]
    
    # Display the visual progress chart
    st.line_chart(filtered_df.set_index("Date")["Weight (kg)"])
    
    # Display the raw history
    st.write("Recent Logs")
    st.dataframe(filtered_df.tail(5))
else:
    st.info("No data logged yet. Add your first heavy lift in the sidebar!")
