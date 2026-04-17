import streamlit as st
import pandas as pd
import os
import time
from datetime import date

# 1. Database Setup
DATA_FILE = "workout_progress.csv"
if not os.path.exists(DATA_FILE):
    # Added "Body Part" column to the database
    df = pd.DataFrame(columns=["Date", "Session", "Body Part", "Exercise", "Weight (kg)", "Sets", "Reps", "Volume"])
    df.to_csv(DATA_FILE, index=False)

st.set_page_config(page_title="Pro Gym Tracker", layout="centered")
st.title("🏋️ Ultimate 6-Day Tracker")

# --- SIDEBAR ---
st.sidebar.header("⚡ Quick Actions")

# Apple Music
st.sidebar.link_button("🎵 Open Apple Music", "https://music.apple.com/library/playlists")

st.sidebar.markdown("---")

# Rest Timer
st.sidebar.subheader("⏱️ Rest Timer")
timer_seconds = st.sidebar.selectbox("Select Seconds", [60, 90, 120, 180], index=1)
if st.sidebar.button("Start Timer"):
    placeholder = st.sidebar.empty()
    for t in range(timer_seconds, -1, -1):
        placeholder.metric("Resting...", f"{t}s")
        time.sleep(1)
    st.sidebar.success("⏰ Time's up!")
    st.balloons()

st.sidebar.markdown("---")

# Logging Section
st.sidebar.subheader("📝 Log Workout")

# DATE TOGGLE
date_mode = st.sidebar.radio("Workout Date:", ["Today", "Other Date"], horizontal=True)
log_date = date.today() if date_mode == "Today" else st.sidebar.date_input("Pick Date", date.today())

# Session Selection
session = st.sidebar.selectbox("Session", ["Chest/Bi A", "Back/Tri A", "Legs/Shoulders A", "Chest/Bi B", "Back/Tri B", "Legs/Shoulders B", "Custom"])

# NEW: Body Part selection for Custom workouts
body_part = "N/A"
if session == "Custom":
    body_part = st.sidebar.selectbox("Target Muscle:", ["Chest", "Back", "Legs", "Shoulders", "Biceps", "Triceps", "Abs", "Cardio"])
else:
    # Auto-assign body part based on session name for cleaner data
    body_part = session.split(" ")[0]

ex = st.sidebar.text_input("Exercise Name")
w = st.sidebar.number_input("Weight (kg)", min_value=0.0, step=2.5)

# PLATE CALCULATOR
if w > 20:
    side_weight = (w - 20) / 2
    st.sidebar.info(f"💡 Load {side_weight}kg on each side")

s = st.sidebar.number_input("Sets", min_value=1)
r = st.sidebar.number_input("Reps", min_value=1)

if st.sidebar.button("Log Lift"):
    if ex:
        vol = w * s * r
        new_data = pd.DataFrame({
            "Date": [log_date], 
            "Session": [session], 
            "Body Part": [body_part],
            "Exercise": [ex], 
            "Weight (kg)": [w], 
            "Sets": [s], 
            "Reps": [r], 
            "Volume": [vol]
        })
        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
        st.sidebar.success(f"Logged {ex} ({body_part})!")

# --- MAIN DASHBOARD ---
df = pd.read_csv(DATA_FILE)
if not df.empty:
    st.header("📈 Progress")
    exercise_list = df["Exercise"].unique()
    selected_ex = st.selectbox("Select Exercise", exercise_list)
    filt = df[df["Exercise"] == selected_ex]
    
    t1, t2 = st.tabs(["Weight Trend", "Volume Trend"])
    with t1: st.line_chart(filt.set_index("Date")["Weight (kg)"])
    with t2: st.line_chart(filt.set_index("Date")["Volume"])
    
    # Show the body part in the history table
    st.write("### History")
    st.table(filt[["Date", "Body Part", "Weight (kg)", "Sets", "Reps"]].tail(5))
    
