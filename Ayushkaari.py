import streamlit as st
import pandas as pd
import json
from ayushkaari_sheet import get_sheet_data
from pathlib import Path

# ✅ Page configuration
st.set_page_config(page_title="Ayushkaari Learning Platform", layout="wide")

# ✅ Initialize session state variables
if "selected_subtopic" not in st.session_state:
    st.session_state.selected_subtopic = None

# ✅ Fetch Google Sheets Data
@st.cache_data
def fetch_data():
    return get_sheet_data()

sheet_data = fetch_data()

# ✅ Check if 'Topic' column exists
if "Topic" in sheet_data.columns:
    topics = sheet_data["Topic"].unique()
else:
    topics = []

# ✅ Sidebar Topics
if "sidebar_visible" not in st.session_state:
    st.session_state.sidebar_visible = True
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None

if st.session_state.sidebar_visible:
    with st.sidebar:
        st.title("Topics")
        for topic in topics:
            if st.button(topic, key=f"topic_{topic}", use_container_width=True):
                st.session_state.selected_topic = topic
                st.session_state.selected_subtopic = None

# ✅ Main Content - Display Subtopics
if st.session_state.selected_topic:
    filtered_data = sheet_data[sheet_data["Topic"] == st.session_state.selected_topic]
    st.title(f"{st.session_state.selected_topic}")
    st.write("### Choose the lecture to watch:")

    subtopics = filtered_data["Subtopic"].unique()
    cols = st.columns(min(3, len(subtopics)))

    for idx, subtopic in enumerate(subtopics):
        col_idx = idx % 3
        with cols[col_idx]:
            if st.button(subtopic, key=f"subtopic_{idx}", use_container_width=True):
                st.session_state.selected_subtopic = subtopic

    # ✅ Display Subtopic Content if Selected
    if st.session_state.selected_subtopic:
        subtopic_data = filtered_data[filtered_data["Subtopic"] == st.session_state.selected_subtopic]
        st.subheader(f"Module: {st.session_state.selected_subtopic}")

        for index, row in subtopic_data.iterrows():
            video_link = row["Video"]
            quiz_link = row["Quiz"]
            sensai_link = row["SensAI"]

            # ✅ Display Video
            if pd.notna(video_link) and video_link.strip():
                try:
                    st.components.v1.html(video_link, height=480)
                except Exception as e:
                    st.error(f"Error loading video: {str(e)}")

            col1, col2 = st.columns([1, 1])

            # ✅ Display Quiz
            with col1:
                if pd.notna(quiz_link) and quiz_link.strip():
                    with st.expander("📝 Take Quiz", expanded=False):
                        st.markdown(f"[Start Quiz]({quiz_link})", unsafe_allow_html=True)
                else:
                    st.info("No quiz available for this subtopic.")

            # ✅ Display SensAI Exercise
            with col2:
                if pd.notna(sensai_link) and sensai_link.strip():
                    st.markdown(f'''
                        <a href="{sensai_link}" target="_blank">
                            <button style="
                                background-color: #4CAF50;
                                color: white;
                                padding: 0.75rem 1.5rem;
                                border: none;
                                border-radius: 4px;
                                cursor: pointer;
                                width: 100%;
                                margin: 4px 0;
                            ">
                                🔍 Solve Exercise
                            </button>
                        </a>
                    ''', unsafe_allow_html=True)
                else:
                    st.info("Exercise to be updated")
else:
    st.info("👈 Select a topic from the sidebar to begin")