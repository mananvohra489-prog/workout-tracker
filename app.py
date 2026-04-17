import streamlit as st
import pandas as pd
import os
import time
from datetime import date

# 1. Database Setup
DATA_FILE = "workout_progress.csv"
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Session", "Exercise", "Weight (kg)", "Sets", "Reps", "Volume"])
    df.to_csv(DATA_FILE, index=False)

st.set_page_config(page_title="My Gym App", layout="centered")
st.title("🏋️ Ultimate 6-Day Tracker")

# --- SIDEBAR: MUSIC, TIMER, & TOOLS ---
st.sidebar.header("⚡ Quick Actions")

# FEATURE 1: Apple Music Button
playlist_url = "https://music.apple.com/library/playlists" 
st.sidebar.link_button("🎵 Open Apple Music", playlist_url)

st.sidebar.markdown("---")

# FEATURE 2: Rest Timer (Countdown)
st.sidebar.subheader("⏱️ Rest Timer")
timer_seconds = st.sidebar.selectbox("Select Rest", [60, 90, 120, 180], index=1)
if st.sidebar.button("Start Timer"):
    placeholder = st.sidebar.empty()
    for t in range(timer_seconds, -1, -1):
        placeholder.metric("Resting...", f"{t}s")
        time.sleep(1)
    st.sidebar.success("⏰ Back to work!")
    st.balloons()

st.sidebar.markdown("---")

# FEATURE 3: 1RM Calculator
st.sidebar.subheader("🧮 1RM Calculator")
calc_w = st.sidebar.number_input("Weight", min_value=0.0, key="cw", step=2.5)
calc_r = st.sidebar.number_input("Reps", min_value=1, key="cr")
if calc_w and calc_r:
    orm = round(calc_w * (1 + calc_r/30), 1)
    st.sidebar.metric("Est. 1RM", f"{orm} kg")

st.sidebar.markdown("---")

# FEATURE 4: Logging with Date Toggle
st.sidebar.subheader("📝 Log Workout")

# DATE TOGGLE: Manual vs Automatic
custom_date_check = st.sidebar.checkbox("Log for a different day?")
log_date = date.today()
if custom_date_check:
    log_date = st.sidebar.date_input("Select Workout Date", date.today())

session = st.sidebar.selectbox("Session", ["Chest/Bi A", "Back/Tri A", "Legs/Shoulders A", "Chest/Bi B", "Back/Tri B", "Legs/Shoulders B", "Custom"])
ex = st.sidebar.text_input("Exercise Name")
w = st.sidebar.number_input("Weight (kg)", min_value=0.0, step=2.5, key="log_w")

# FEATURE 5: Automatic Plate Calculator
if w > 20:
    side_weight = (w - 20) / 2
    st.sidebar.info(f"💡 Put {side_weight}kg on each side")

s = st.sidebar.number_input("Sets", min_value=1)
r = st.sidebar.number_input("Reps", min_value=1)

if st.sidebar.button("Log Lift"):
    if ex:
        vol = w * s * r
        new_data = pd.DataFrame({"Date": [log_date], "Session": [session], "Exercise": [ex], "Weight (kg)": [w], "Sets": [s], "Reps": [r], "Volume": [vol]})
        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
        st.sidebar.success(f"Logged {ex}!")

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
    st.table(filt[["Date", "Weight (kg)", "Sets", "Reps"]].tail(3))
else:
    st.info("Start logging to see your charts!")
