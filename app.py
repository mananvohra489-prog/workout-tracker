import streamlit as st
import pandas as pd
import os
import time
from datetime import date

# 1. Database Setup
DATA_FILE = "workout_progress.csv"
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Session", "Body Part", "Exercise", "Weight (kg)", "Sets", "Reps", "Volume"])
    df.to_csv(DATA_FILE, index=False)

st.set_page_config(page_title="6-Day Pro Tracker", layout="wide") # Wide layout for better visibility
st.title("🏋️ Ultimate 6-Day Tracker")

# --- SIDEBAR: QUICK TOOLS ---
st.sidebar.header("⚡ Quick Actions")
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

# --- MAIN LOGGING SECTION ---
st.header("📝 Log Your Session")

# Row 1: Date and Session Type
col1, col2, col3 = st.columns(3)
with col1:
    date_mode = st.radio("Workout Date:", ["Today", "Other Date"], horizontal=True)
    log_date = date.today() if date_mode == "Today" else st.date_input("Pick Date", date.today())
with col2:
    session = st.selectbox("Session Type", ["Chest/Bi A", "Back/Tri A", "Legs/Shoulders A", "Chest/Bi B", "Back/Tri B", "Legs/Shoulders B", "Custom"])
with col3:
    body_part = "N/A"
    if session == "Custom":
        body_part = st.selectbox("Target Muscle:", ["Chest", "Back", "Legs", "Shoulders", "Biceps", "Triceps", "Abs", "Cardio"])
    else:
        body_part = session.split("/")[0] if "/" in session else session

st.markdown("---")

# Row 2: Bulk Exercise Inputs (5 Slots)
st.subheader("Enter Exercises")
entries = []
for i in range(1, 6):
    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
    with c1:
        ex_name = st.text_input(f"Exercise {i}", key=f"ex_{i}", placeholder="e.g. Bench Press")
    with c2:
        w = st.number_input("Weight (kg)", min_value=0.0, step=2.5, key=f"w_{i}")
    with c3:
        s = st.number_input("Sets", min_value=0, step=1, key=f"s_{i}")
    with c4:
        r = st.number_input("Reps", min_value=0, step=1, key=f"r_{i}")
    
    if ex_name and s > 0:
        entries.append({
            "Date": log_date, "Session": session, "Body Part": body_part,
            "Exercise": ex_name, "Weight (kg)": w, "Sets": s, "Reps": r, "Volume": w * s * r
        })

if st.button("🔥 Log All Exercises", use_container_width=True):
    if entries:
        new_df = pd.DataFrame(entries)
        new_df.to_csv(DATA_FILE, mode='a', header=False, index=False)
        st.success(f"Successfully logged {len(entries)} exercises!")
        time.sleep(1)
        st.rerun()
    else:
        st.error("Please fill in at least one exercise.")

# --- CHARTS ---
st.markdown("---")
df = pd.read_csv(DATA_FILE)
if not df.empty:
    st.header("📈 Progress Dashboard")
    exercise_list = sorted(df["Exercise"].unique())
    selected_ex = st.selectbox("Select Exercise to View Trend", exercise_list)
    filt = df[df["Exercise"] == selected_ex]
    
    t1, t2 = st.tabs(["Weight Trend", "Volume Trend"])
    with t1: st.line_chart(filt.set_index("Date")["Weight (kg)"])
    with t2: st.line_chart(filt.set_index("Date")["Volume"])
