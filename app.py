import streamlit as st
import pandas as pd
from google_sheet_test import get_sheet_data

# Page configuration
st.set_page_config(page_title="Learn Page", layout="wide")

# Custom CSS for better design
st.markdown("""
    <style>
    /* Base button styling */
    .stButton > button {
        background-color: #f0f2f6;
        border: 1px solid #e0e3e9;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #e0e3e9;
        border-color: #c0c3c9;
    }
    .stButton > button:active {
        background-color: #d0d3d9;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding: 1rem;
        background-color: #f8f9fa;
    }
    
    /* Topic buttons in sidebar */
    [data-testid="stSidebarNav"] .stButton > button {
        width: 100%;
        text-align: left;
        background-color: #ffffff;
        margin: 0.25rem 0;
    }
    iframe {
        width: 100%;
        height: 100%;
        aspect-ratio: 16/9;  /* Optional: Use appropriate aspect ratio */
    }
    /* Quiz expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 4px;
        padding: 0.5rem;
        font-size: 1rem;
        width: fit-content;
        min-width: 200px;
    }
    
    /* Title and header styling */
    h1, h2, h3 {
        color: #1f1f1f;
        margin-bottom: 1rem;
    }
    
    /* Exercise button styling */
    .stButton > button[data-testid="exercise-button"] {
        background-color: #4CAF50;
        color: white;
        padding: 0.75rem 1.5rem;
        border: none;
    }
    .stButton > button[data-testid="exercise-button"]:hover {
        background-color: #45a049;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for sidebar visibility
if 'sidebar_visible' not in st.session_state:
    st.session_state.sidebar_visible = True
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = None

# Cache the data fetching function
@st.cache_data
def fetch_data():
    return get_sheet_data()

# Fetch data from Google Sheet
sheet_data = fetch_data()

# Enhanced Sidebar
if st.session_state.sidebar_visible:
    with st.sidebar:
        st.title("Topics")
        topics = sheet_data["Topic"].unique()
        
        # Create buttons for topics
        for topic in topics:
            if st.button(topic, key=f"topic_{topic}", use_container_width=True):
                st.session_state.selected_topic = topic

# Main content
if st.session_state.selected_topic:
    filtered_data = sheet_data[sheet_data["Topic"] == st.session_state.selected_topic]
    st.title(f"{st.session_state.selected_topic}")
    
    # Create horizontal buttons for subtopics
    subtopics = filtered_data["Subtopic"].unique()
    st.write("### Choose a subtopic to learn:")
    
    # Create columns for better button arrangement
    cols = st.columns(min(3, len(subtopics)))
    selected_subtopic = None
    
    # Create buttons in columns
    for idx, subtopic in enumerate(subtopics):
        col_idx = idx % 3
        with cols[col_idx]:
            if st.button(subtopic, key=f"subtopic_{idx}", use_container_width=True):
                selected_subtopic = subtopic
    
    # Display content for selected subtopic
    if selected_subtopic:
        subtopic_data = filtered_data[filtered_data["Subtopic"] == selected_subtopic]
        
        for index, row in subtopic_data.iterrows():
            video_link = row["Video"]
            quiz_link = row["Quiz"]
            sensai_link = row["SensAI"]
            
            st.subheader(f"Module: {selected_subtopic}")
            
            # Video section with error handling
            if pd.notna(video_link) and video_link.strip():
                try:
                    st.components.v1.html(video_link, height=400)
                except Exception as e:
                    st.error(f"Error loading video: {str(e)}")
            else:
                st.warning("Video not available for this subtopic.")
            
            # Interactive elements row
            col1, col2 = st.columns([1, 1])
            
            # Quiz section with error handling
            with col1:
                if pd.notna(quiz_link) and quiz_link.strip():
                    with st.expander("📝 Take Quiz", expanded=False):
                        try:
                            if quiz_link.startswith("<iframe"):
                                st.components.v1.html(quiz_link, height=400)
                            else:
                                st.markdown(f"[Start Quiz]({quiz_link})", unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error loading quiz: {str(e)}")
                else:
                    st.info("No quiz available for this subtopic.")
            
            # Exercise section with error handling
            with col2:
                if pd.notna(sensai_link) and sensai_link.strip() and not sensai_link.endswith(','):
                    st.link_button(
                        "🔍 Solve Exercise",
                        sensai_link,
                        use_container_width=True,
                        type="primary"
                    )
                else:
                    st.info("Exercise to be updated")
else:
    st.info("👈 Select a topic from the sidebar to begin")
