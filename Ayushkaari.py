import streamlit as st
import pandas as pd
import json
from ayushkaari_sheet import get_sheet_data
from pathlib import Path
import requests
from PIL import Image
from io import BytesIO
import base64

# ✅ Page configuration
st.set_page_config(
    page_title="Ministry of Magic",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': 'Ministry of Magic Learning Platform'
    },
    # Use base64 encoded logo as favicon
    page_icon="✨"  # Temporary icon, will be replaced with logo
)

# Define logo URL - with a more reliable fallback for cloud deployment
# Primary URL directly from GitHub (most reliable for cloud deployment)
LOGO_URL_PRIMARY = "https://raw.githubusercontent.com/Atman-Deshmane/Streamlit-LMS/main/assets/ministry_of_magic_logo.jpg"
# Backup URL from original source
LOGO_URL_BACKUP = "https://assets.grok.com/users/4e4a32d1-260f-4808-b949-13b34b80fa83/yOir8l0r1u7F8UVC-generated_image.jpg"

# Use the primary URL by default
LOGO_URL = LOGO_URL_PRIMARY

# Modern CSS for both light and dark modes
st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        
        /* Base styles */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Fix for sidebar gap without affecting hide button position */
        header[data-testid="stHeader"] {
            background-color: transparent;
        }
        
        /* Preserve hide button position */
        button[kind="header"] {
            position: relative;
            top: 0;
            z-index: 100;
        }
        
        /* These selectors fix the gap but won't affect the hide button */
        div[data-testid="stSidebarUserContent"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        .main .block-container {
            padding-top: 1rem !important;
        }
        
        /* Sidebar header specific styling */
        .sidebar-header {
            text-align: center;
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
        }
        
        /* Force logo to be properly centered and larger */
        .sidebar-logo {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            width: 100% !important;
            padding: 1.5rem 0 !important;
            margin: 0 auto !important;
            text-align: center !important;
        }
        
        /* Make the logo container completely centered */
        .sidebar-logo > div {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 auto !important;
        }
        
        /* Force the image itself to be centered and larger */
        .sidebar-logo img {
            display: block !important;
            margin: 0 auto !important;
            width: auto !important;
            max-width: 90% !important;
            height: auto !important;
        }
        
        /* Styled larger Topics header */
        .topics-header {
            text-align: center !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            margin: 1.5rem 0 1rem 0 !important;
            color: inherit !important;
        }

        /* Topic buttons layout */
        .stButton > button {
            width: 100%;
            transition: all 0.2s ease !important;
            border-radius: 8px !important;
            border: 1px solid var(--border-color-primary) !important;
            margin-bottom: 0.5rem;
            font-weight: 500 !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        /* Quiz button - centered in the dropdown */
        .quiz-button {
            display: block !important;
            margin: 15px auto !important;
            text-align: center !important;
            width: 80% !important;
            padding: 10px 20px !important;
            border-radius: 8px !important;
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: 500 !important;
            text-decoration: none !important;
            transition: all 0.2s ease !important;
        }
        
        .quiz-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
        }

        /* Welcome container layout */
        .welcome-container {
            padding: 4rem 2rem;
            margin: 2rem auto;
            max-width: 800px;
            text-align: center;
            border-radius: 12px;
            border: 1px solid var(--border-color-primary);
            background-color: var(--background-color-secondary);
        }

        .welcome-title {
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            font-weight: 600;
        }

        .welcome-text {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            line-height: 1.6;
            opacity: 0.9;
        }

        /* Animated finger */
        .welcome-arrow {
            font-size: 3rem;
            animation: bounce 2s infinite;
            display: inline-block;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateX(0); }
            50% { transform: translateX(-20px); }
        }

        /* Video container */
        .video-container {
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 1.5rem;
            border: 1px solid var(--border-color-primary);
            position: relative;
        }

        /* Open in new tab button - improved visibility */
        .new-tab-button {
            position: absolute;
            bottom: 15px;
            right: 15px;
            background-color: rgba(0, 0, 0, 0.75);
            color: white !important;
            padding: 8px 12px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 13px;
            display: inline-flex;
            align-items: center;
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            transition: all 0.2s ease;
            z-index: 100;
            font-weight: 500;
        }
        
        .new-tab-button:hover {
            background-color: rgba(0, 0, 0, 0.9);
            transform: translateY(-2px);
        }

        /* Quiz container */
        .quiz-container {
            border-radius: 8px;
            overflow: hidden;
            margin-top: 10px;
            border: 1px solid var(--border-color-primary);
            background-color: var(--background-color-secondary);
        }
        
        /* Make the quiz expander look nicer */
        .st-emotion-cache-1h9e0ik {
            border-radius: 8px;
            border: 1px solid var(--border-color-primary);
            margin-bottom: 20px;
        }
        
        /* Clean embedded quiz styles */
        .quiz-embedded {
            margin-top: 10px;
            border-radius: 8px;
            overflow: hidden;
        }
        
        /* Hide extra HTML text in quizzes */
        .quiz-embedded a[href]:not(.quiz-button), 
        .quiz-embedded [target="_blank"]:not(.quiz-button) {
            display: none !important;
        }

        /* Exercise button - improved for both modes */
        .exercise-button {
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            background-color: #4CAF50;
            color: white !important;
            font-weight: 600;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            text-decoration: none;
            border: none;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        }
        
        .exercise-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            background-color: #45a049;
        }

        /* Subtopic header */
        .subtopic-header {
            margin: 2rem 0;
            font-size: 1.2rem;
            font-weight: 500;
            text-align: center;
            opacity: 0.9;
        }

        /* Hide footer */
        footer {display: none;}
        .viewerBadge_container__1QSob {display: none;}
        [data-testid="stFooter"] {display: none;}
        
        /* CSS variables for light/dark mode compatibility */
        :root {
            --border-color-primary: rgba(128, 128, 128, 0.2);
            --background-color-secondary: rgba(128, 128, 128, 0.05);
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Initialize session state variables
if "selected_subtopic" not in st.session_state:
    st.session_state.selected_subtopic = None

# ✅ Fetch Google Sheets Data with improved caching
@st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour
def fetch_data():
    return get_sheet_data()

# Cache the data at startup
if "sheet_data" not in st.session_state:
    st.session_state.sheet_data = fetch_data()
    
# Use the cached data
sheet_data = st.session_state.sheet_data

# Function to extract video URL from embed code
def extract_video_url(embed_code):
    if not embed_code or pd.isna(embed_code):
        return None
    
    # For YouTube embeds
    if "youtube.com/embed/" in embed_code:
        import re
        youtube_id = re.search(r'youtube.com/embed/([^"?]+)', embed_code)
        if youtube_id:
            return f"https://www.youtube.com/watch?v={youtube_id.group(1)}"
    
    # For Vimeo embeds
    if "player.vimeo.com/video/" in embed_code:
        import re
        vimeo_id = re.search(r'player.vimeo.com/video/([^"?]+)', embed_code)
        if vimeo_id:
            return f"https://vimeo.com/{vimeo_id.group(1)}"
    
    # For other platforms, try to extract src attribute
    import re
    src_match = re.search(r'src=["\']([^"\']+)["\']', embed_code)
    if src_match:
        return src_match.group(1)
    
    return None

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
        st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
        try:
            # Try the primary URL first with a longer timeout for cloud environments
            response = requests.get(LOGO_URL, timeout=10, stream=True)
            logo_loaded = False
            
            if response.status_code == 200:
                try:
                    img = Image.open(BytesIO(response.content))
                    logo_loaded = True
                except Exception:
                    # If we can't process the image, try the backup URL
                    try:
                        response = requests.get(LOGO_URL_BACKUP, timeout=10, stream=True)
                        if response.status_code == 200:
                            img = Image.open(BytesIO(response.content))
                            logo_loaded = True
                    except Exception:
                        logo_loaded = False
            else:
                # If primary URL fails, try the backup URL
                try:
                    response = requests.get(LOGO_URL_BACKUP, timeout=10, stream=True)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        logo_loaded = True
                except Exception:
                    logo_loaded = False
            
            if logo_loaded:
                # Set a larger target width for the sidebar image
                target_width = 320
                
                # Use proper HTML/CSS to ensure the image is centered
                st.markdown(f"""
                    <div class="sidebar-logo">
                        <div style="text-align: center; width: 100%;">
                            <img src="data:image/jpeg;base64,{base64.b64encode(BytesIO(response.content).getvalue()).decode()}" 
                                 width="{target_width}" 
                                 style="margin: 0 auto; display: block;">
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Set favicon dynamically
                favicon = BytesIO(response.content)
                encoded = base64.b64encode(favicon.getvalue()).decode()
                st.markdown(
                    f"""
                    <style>
                    [data-testid="stSidebarNav"] {{
                        background-image: url("data:image/png;base64,{encoded}");
                        background-repeat: no-repeat;
                        background-position: 20px 20px;
                        background-size: 30px;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                # Fallback to embedded sparkles icon if both URLs fail
                st.markdown("""
                    <div style="
                        width: 180px;
                        height: 180px;
                        background: rgba(128, 128, 128, 0.1);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto;
                        font-size: 3.5rem;
                    ">
                        ✨
                    </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            # Fallback text-based logo
            st.markdown("""
                <div style="
                    width: 180px;
                    height: 180px;
                    background: rgba(128, 128, 128, 0.1);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto;
                    font-size: 3.5rem;
                ">
                    ✨
                </div>
            """, unsafe_allow_html=True)
        
        # Close the sidebar header div
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Centered and larger Topics header
        st.markdown('<h2 class="topics-header">Topics</h2>', unsafe_allow_html=True)
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
                    # Extract direct URL for "Open in new tab" button
                    direct_url = extract_video_url(video_link)
                    
                    # Create a container for the video and button
                    st.markdown('<div class="video-container">', unsafe_allow_html=True)
                    st.components.v1.html(video_link, height=480)
                    
                    # Add the "Open in new tab" button inside the video container
                    if direct_url:
                        st.markdown(f"""
                            <a href="{direct_url}" target="_blank" class="new-tab-button">
                                <span style="margin-right: 5px;">↗️</span> Open in new tab
                            </a>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error loading video: {str(e)}")
                    
                    # If video fails to load, provide direct link
                    direct_url = extract_video_url(video_link)
                    if direct_url:
                        st.markdown(f"""
                            <a href="{direct_url}" target="_blank" style="
                                background-color: #4CAF50;
                                color: white;
                                padding: 10px 20px;
                                border-radius: 8px;
                                text-decoration: none;
                                font-size: 16px;
                                display: inline-flex;
                                align-items: center;
                                margin: 10px 0;
                            ">
                                <span style="margin-right: 8px;">▶️</span> Watch Video
                            </a>
                        """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 1])

            # ✅ Display Quiz - Fix to show quiz directly in dropdown
            with col1:
                if pd.notna(quiz_link) and quiz_link.strip():
                    with st.expander("📝 Take Quiz", expanded=False):
                        # Display the quiz content directly in the dropdown
                        if "<a href=" in quiz_link:
                            # Clean up the quiz content by removing unwanted links while keeping the quiz content
                            import re
                            cleaned_content = re.sub(r'<a href="[^"]*"[^>]*>|</a>', '', quiz_link)
                            st.markdown(f'<div class="quiz-embedded">{cleaned_content}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="quiz-embedded">{quiz_link}</div>', unsafe_allow_html=True)
                        
                        # Add the direct quiz start button - now centered with CSS
                        if "forms.gle" in quiz_link or "docs.google.com/forms" in quiz_link:
                            # Extract the direct URL to the form
                            form_url_match = re.search(r'(https://(?:forms\.gle|docs\.google\.com/forms)[^"\'&]+)', quiz_link)
                            if form_url_match:
                                form_url = form_url_match.group(1)
                                st.markdown(f'<a href="{form_url}" target="_blank" class="quiz-button">📝 Start Quiz</a>', unsafe_allow_html=True)
                else:
                    st.info("No quiz available for this subtopic.")

            # ✅ Display SensAI Exercise
            with col2:
                if pd.notna(sensai_link) and sensai_link.strip():
                    st.markdown(f'<a href="{sensai_link}" target="_blank" class="exercise-button">🔍 Solve Exercise</a>', unsafe_allow_html=True)
                else:
                    st.info("Exercise to be updated")
else:
    # Welcome message with animated finger
    st.markdown("""
    <div class="welcome-container">
        <h2 class="welcome-title">Welcome to Ministry of Magic</h2>
        <p class="welcome-text">Select a topic from the sidebar to begin your magical learning journey.</p>
        <div class="welcome-arrow">👈</div>
    </div>
    """, unsafe_allow_html=True)