import streamlit as st
import pandas as pd
import os
from datetime import date

# 1. Database Setup
DATA_FILE = "workout_progress.csv"
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Session", "Exercise", "Weight (kg)", "Sets", "Reps", "Volume"])
    df.to_csv(DATA_FILE, index=False)

# 2. Page Config for iPhone
st.set_page_config(page_title="My Gym App", layout="centered")
st.title("🏋️ Ultimate 6-Day Tracker")

# --- SIDEBAR: MUSIC, TOOLS & LOGGING ---
st.sidebar.header("⚡ Quick Actions")

# FEATURE 1: Apple Music Button
playlist_url = "https://music.apple.com/library/playlists" 
st.sidebar.link_button("🎵 Open Apple Music", playlist_url)

st.sidebar.markdown("---")

# FEATURE 2: 1-Rep Max Calculator
st.sidebar.subheader("🧮 1RM Calculator")
calc_w = st.sidebar.number_input("Weight", min_value=0.0, key="cw", step=2.5)
calc_r = st.sidebar.number_input("Reps", min_value=1, key="cr")
if calc_w and calc_r:
    orm = round(calc_w * (1 + calc_r/30), 1)
    st.sidebar.metric("Estimated Max", f"{orm} kg")

st.sidebar.markdown("---")

# FEATURE 3: 6-Day Split Logging
st.sidebar.subheader("📝 Log Workout")
session = st.sidebar.selectbox("Session", [
    "Chest/Bi A", "Back/Tri A", "Legs/Shoulders A", 
    "Chest/Bi B", "Back/Tri B", "Legs/Shoulders B", 
    "Custom/Single Muscle"
])
ex = st.sidebar.text_input("Exercise Name")
w = st.sidebar.number_input("Weight (kg)", min_value=0.0, step=2.5, key="log_w")

# FEATURE 4: Automatic Plate Calculator
if w > 20:
    side_weight = (w - 20) / 2
    st.sidebar.info(f"💡 Load {side_weight}kg per side")

s = st.sidebar.number_input("Sets", min_value=1)
r = st.sidebar.number_input("Reps", min_value=1)

if st.sidebar.button("Log Lift"):
    if ex:
        volume = w * s * r
        new_data = pd.DataFrame({
            "Date": [date.today()], "Session": [session], "Exercise": [ex], 
            "Weight (kg)": [w], "Sets": [s], "Reps": [r], "Volume": [volume]
        })
        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
        st.sidebar.success(f"Logged {ex}!")

# --- MAIN DASHBOARD: PROGRESS ---
df = pd.read_csv(DATA_FILE)

if not df.empty:
    st.header("📈 Progress Charts")
    exercise_list = df["Exercise"].unique()
    selected_ex = st.selectbox("Select Exercise", exercise_list)
    filt = df[df["Exercise"] == selected_ex]
    
    # FEATURE 5: Double Charts (Weight & Volume)
    tab1, tab2 = st.tabs(["Weight Trend", "Volume Trend"])
    
    with tab1:
        st.line_chart(filt.set_index("Date")["Weight (kg)"])
    with tab2:
        st.line_chart(filt.set_index("Date")["Volume"])
    
    st.subheader("Session History")
    st.table(filt[["Date", "Weight (kg)", "Sets", "Reps"]].tail(5))
else:
    st.info("No data yet. Log your first lift in the sidebar!")
