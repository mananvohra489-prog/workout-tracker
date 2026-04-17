import streamlit as st
import pandas as pd
import os
import time
from datetime import date

# 1. Database Setup with Safety Check
DATA_FILE = "workout_progress.csv"
# Added "Song" to the required columns
REQUIRED_COLS = ["Date", "Session", "Body Part", "Exercise", "Set", "Weight (kg)", "Reps", "Volume", "Song"]

if os.path.exists(DATA_FILE):
    existing_df = pd.read_csv(DATA_FILE)
    if "Song" not in existing_df.columns:
        os.remove(DATA_FILE) # Reset to add new column

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=REQUIRED_COLS)
    df.to_csv(DATA_FILE, index=False)

st.set_page_config(page_title="Pro PPL Tracker", layout="wide")
st.title("🏋️ Pro Multi-Set Tracker")

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

# --- LOGGING SECTION ---
st.header("📝 Log Your Session")

col1, col2, col3 = st.columns(3)
with col1:
    date_mode = st.radio("Workout Date:", ["Today", "Other Date"], horizontal=True)
    log_date = date.today() if date_mode == "Today" else st.date_input("Pick Date", date.today())
with col2:
    session = st.selectbox("Session Type", ["Chest/Bi A", "Back/Tri A", "Legs/Shoulders A", "Chest/Bi B", "Back/Tri B", "Legs/Shoulders B", "Custom"])
with col3:
    # NEW: Now Playing Feature
    current_song = st.text_input("🎵 Now Playing:", placeholder="e.g. Sidhu Moose Wala - 295")

st.markdown("---")

# Bulk Exercise Inputs
all_entries = []
for i in range(1, 9):
    with st.expander(f"Exercise {i}", expanded=(i==1)):
        c1, c2 = st.columns([2, 1])
        with c1:
            ex_name = st.text_input(f"Exercise Name {i}", key=f"ex_{i}")
        with c2:
            num_sets = st.number_input(f"Sets", min_value=1, max_value=6, value=3, key=f"n_sets_{i}")
        
        if ex_name:
            # Determine Body Part
            body_part = session.split("/")[0] if "/" in session else "Custom"
            
            st.markdown("**Set Details (Weight | Reps)**")
            set_cols = st.columns(num_sets)
            for s_idx in range(num_sets):
                with set_cols[s_idx]:
                    w = st.number_input(f"Set {s_idx+1} kg", min_value=0.0, step=0.5, key=f"w_{i}_{s_idx}")
                    r = st.number_input(f"Set {s_idx+1} reps", min_value=0, step=1, key=f"r_{i}_{s_idx}")
                    if w > 0 and r > 0:
                        all_entries.append({
                            "Date": log_date, "Session": session, "Body Part": body_part,
                            "Exercise": ex_name, "Set": s_idx + 1, "Weight (kg)": w, "Reps": r, 
                            "Volume": w * r, "Song": current_song # Saving the song name
                        })

if st.button("🔥 Log Full Session", use_container_width=True):
    if all_entries:
        new_df = pd.DataFrame(all_entries)
        new_df.to_csv(DATA_FILE, mode='a', header=False, index=False)
        st.success("Session Saved with Music Vibes!")
        time.sleep(1)
        st.rerun()

# --- CHARTS & HISTORY ---
st.markdown("---")
df = pd.read_csv(DATA_FILE)
if not df.empty:
    st.header("📈 Progress Dashboard")
    exercise_list = sorted(df["Exercise"].unique())
    selected_ex = st.selectbox("Select Exercise", exercise_list)
    filt = df[df["Exercise"] == selected_ex]
    
    t1, t2, t3 = st.tabs(["Max Weight", "Volume", "Music & History"])
    
    with t1:
        max_trend = filt.groupby("Date")["Weight (kg)"].max().reset_index()
        st.line_chart(max_trend.set_index("Date")["Weight (kg)"])
    with t2:
        vol_trend = filt.groupby("Date")["Volume"].sum().reset_index()
        st.line_chart(vol_trend.set_index("Date")["Volume"])
    with t3:
        st.write("### Previous Sets & Song Tracks")
        # Displaying the song in the history table
        st.dataframe(filt[["Date", "Weight (kg)", "Reps", "Song"]].tail(10))
