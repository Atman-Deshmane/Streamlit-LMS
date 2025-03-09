import streamlit as st
import pandas as pd
import json
from ayushkaari_sheet import get_sheet_data
from pathlib import Path
import requests
from PIL import Image
from io import BytesIO

# ✅ Page configuration
st.set_page_config(page_title="Ministry of Magic", layout="wide")

# Hide default Streamlit elements
st.markdown("""
    <style>
        /* Hide Streamlit header elements */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Remove extra padding at the top */
        .block-container {
            padding-top: 1rem !important;
        }
        
        /* Hide "Deploy" button */
        .stDeployButton {display: none;}

        /* Hide sidebar header decoration */
        section[data-testid="stSidebar"] > div:first-child {
            background-color: transparent;
            padding-top: 0;
            margin-top: -6rem;
        }
        
        section[data-testid="stSidebar"] .element-container:has(div.sidebar-header) {
            margin-top: -3rem;
        }

        /* Remove default sidebar gradient */
        section[data-testid="stSidebar"] > div {
            background-image: none !important;
        }

        /* Hide hamburger menu */
        button[kind="header"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Add custom CSS for a modern, minimalist design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
    
    /* Base styles */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Color variables */
    :root {
        --sage-100: #F1F4F0;
        --sage-200: #E3E8E2;
        --sage-300: #C5D1C3;
        --sage-400: #A7B9A5;
        --sage-500: #89A186;
        --sage-600: #6B8968;
        --text-primary: #2C3E2E;
        --text-secondary: #4A5E4C;
    }
    
    /* Main container styling */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
        background: var(--sage-100);
        border-radius: 20px;
        margin: 2rem auto;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--sage-200);
    }
    
    .sidebar-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 3rem;
        padding: 2rem 1rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .sidebar-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 1rem;
        text-align: center;
        color: var(--text-primary);
    }
    
    /* Welcome message styling */
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 2rem;
        margin: 2rem auto;
        max-width: 800px;
        text-align: center;
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05);
    }
    
    .welcome-title {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        color: var(--text-primary);
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    .welcome-text {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    .welcome-arrow {
        font-size: 2.5rem;
        color: var(--sage-500);
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(-10px); }
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 2px solid var(--sage-300);
        background-color: white;
        color: var(--text-primary);
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: var(--sage-200);
        border-color: var(--sage-400);
        transform: translateY(-2px);
    }
    
    /* Subtopic styling */
    .subtopic-header {
        margin: 2rem 0;
        font-size: 1.4rem;
        color: var(--text-primary);
        font-weight: 500;
        text-align: center;
    }
    
    /* Quiz and Exercise buttons */
    .quiz-button, .exercise-button {
        background-color: white;
        color: var(--text-primary);
        padding: 1rem 2rem;
        border: 2px solid var(--sage-300);
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    .quiz-button:hover, .exercise-button:hover {
        background-color: var(--sage-200);
        border-color: var(--sage-400);
        transform: translateY(-2px);
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--sage-100);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--sage-400);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--sage-500);
    }
</style>
""", unsafe_allow_html=True)

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
        # Add logo and title
        logo_url = "https://raw.githubusercontent.com/atmandeshmane/Streamlit-LMS/main/assets/logo.png"  # We'll need to upload the logo to the repository
        
        st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
        try:
            response = requests.get(logo_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                st.image(img, width=120, use_column_width=False)
            else:
                # Fallback text-based logo
                st.markdown("""
                    <div style="
                        width: 120px;
                        height: 120px;
                        background: var(--sage-300);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto;
                        font-size: 2rem;
                        color: white;
                    ">
                        MoM
                    </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            # Fallback text-based logo
            st.markdown("""
                <div style="
                    width: 120px;
                    height: 120px;
                    background: var(--sage-300);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto;
                    font-size: 2rem;
                    color: white;
                ">
                    MoM
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-title">Ministry of Magic</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### Topics")
        for topic in topics:
            if st.button(topic, key=f"topic_{topic}", use_container_width=True):
                st.session_state.selected_topic = topic
                st.session_state.selected_subtopic = None

# ✅ Main Content - Display Subtopics
if st.session_state.selected_topic:
    filtered_data = sheet_data[sheet_data["Topic"] == st.session_state.selected_topic]
    st.title(f"{st.session_state.selected_topic}")
    st.markdown('<div class="subtopic-header">Choose the lecture to watch:</div>', unsafe_allow_html=True)

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
                        st.markdown(f'''
                            <a href="{quiz_link}" target="_blank">
                                <button class="quiz-button">
                                    📝 Start Quiz
                                </button>
                            </a>
                        ''', unsafe_allow_html=True)
                else:
                    st.info("No quiz available for this subtopic.")

            # ✅ Display SensAI Exercise
            with col2:
                if pd.notna(sensai_link) and sensai_link.strip():
                    st.markdown(f'''
                        <a href="{sensai_link}" target="_blank">
                            <button class="exercise-button">
                                🔍 Solve Exercise
                            </button>
                        </a>
                    ''', unsafe_allow_html=True)
                else:
                    st.info("Exercise to be updated")
else:
    # Centered and highlighted welcome message
    st.markdown("""
    <div class="welcome-container">
        <h2 class="welcome-title">Welcome to Ministry of Magic</h2>
        <p class="welcome-text">Select a topic from the sidebar to begin your magical learning journey.</p>
        <div class="welcome-arrow">👈</div>
    </div>
    """, unsafe_allow_html=True)