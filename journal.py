import streamlit as st
from datetime import datetime

st.set_page_config(page_title="My Journal", page_icon="📖")

st.title("📖 My Daily Journal")

# --- Session State ---
if "entries" not in st.session_state:
    st.session_state.entries = []

# --- Mood Selector ---
mood = st.selectbox("How are you feeling today?", ["😊 Happy", "😐 Neutral", "😔 Sad", "😡 Angry", "😴 Tired"])

# --- Journal Entry ---
entry = st.text_area("Write something about your day:")

if st.button("Save Entry"):
    if entry.strip():
        st.session_state.entries.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "mood": mood,
            "entry": entry.strip()
        })
        st.success("✅ Entry saved!")
        st.rerun()

# --- Show Past Entries ---
st.divider()
st.subheader("📂 Past Entries")

if st.session_state.entries:
    for e in reversed(st.session_state.entries):
        st.write(f"**{e['date']}** — {e['mood']}")
        st.write(e['entry'])
        st.divider()
else:
    st.info("No entries yet. Start writing!")