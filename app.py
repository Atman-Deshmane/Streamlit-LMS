import streamlit as st
import pandas as pd
import json
from google_sheet_test import get_sheet_data
from authlib.integrations.requests_client import OAuth2Session

# Page configuration
st.set_page_config(page_title="Learn Page", layout="wide")

# Azure App Configuration
AZURE_CONFIG = {
    "client_id": "44618fbb-163b-49c6-905e-302323aa3026",
    "client_secret": "f2d6f927-6306-4789-ac1c-c6ffe5f16804",
    "authority": "https://login.microsoftonline.com/common",
    "redirect_uri": "https://physiks.streamlit.app/",
    "scope": ["openid", "profile", "email"]
}

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "oauth_state" not in st.session_state:
    st.session_state.oauth_state = None
if "selected_subtopic" not in st.session_state:
    st.session_state.selected_subtopic = None

# ✅ Load subtopic progress from query params (if available)
if "subtopic_status" not in st.session_state:
    subtopic_status_json = st.query_params.get("subtopic_status", "{}")
    st.session_state.subtopic_status = json.loads(subtopic_status_json)

# ✅ Function to toggle subtopic status
def toggle_subtopic_status(subtopic):
    """Marks a subtopic as done/undone and updates query params."""
    st.session_state.subtopic_status[subtopic] = not st.session_state.subtopic_status.get(subtopic, False)

    # ✅ Store progress in query params
    st.query_params.update(subtopic_status=json.dumps(st.session_state.subtopic_status))

    # ✅ Refresh UI instantly
    st.rerun()

# ✅ Login Function to Open in a Pop-Up
def microsoft_login():
    try:
        auth_url = f"{AZURE_CONFIG['authority']}/oauth2/v2.0/authorize" \
                   f"?client_id={AZURE_CONFIG['client_id']}" \
                   f"&response_type=code" \
                   f"&redirect_uri={AZURE_CONFIG['redirect_uri']}" \
                   f"&scope={' '.join(AZURE_CONFIG['scope'])}" \
                   f"&state={st.session_state.oauth_state}" \
                   f"&prompt=select_account"

        js_code = f"""
        <script>
        function openLoginPopup() {{
            var popup = window.open("{auth_url}", "Microsoft Login", "width=500,height=600");
            var checkPopup = setInterval(function() {{
                if (!popup || popup.closed) {{
                    clearInterval(checkPopup);
                    window.location.reload();
                }}
            }}, 1000);
        }}
        </script>
        <button onclick="openLoginPopup()" style="
            background-color: #2F2F2F;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            margin: 4px 0;
        ">
            Login with Microsoft
        </button>
        """
        st.markdown(js_code, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Login failed: {str(e)}")

# Sidebar
with st.sidebar:
    if not st.session_state.authenticated:
        st.write("### Save Your Progress")
        microsoft_login()
    else:
        st.write(f"Welcome, {st.session_state.user_info.get('displayName', 'User')}")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.rerun()

# Debug Info
with st.expander("🐛 Debug Info"):
    st.write("Authorization URL:")
    if "oauth_state" in st.session_state:
        st.write(f"State: {st.session_state.oauth_state}")

# ✅ Fetch Google Sheets Data
@st.cache_data
def fetch_data():
    return get_sheet_data()

sheet_data = fetch_data()

# Sidebar Topics
if "sidebar_visible" not in st.session_state:
    st.session_state.sidebar_visible = True
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None

if st.session_state.sidebar_visible:
    with st.sidebar:
        st.title("Topics")
        topics = sheet_data["Topic"].unique()
        for topic in topics:
            if st.button(topic, key=f"topic_{topic}", use_container_width=True):
                st.session_state.selected_topic = topic
                st.session_state.selected_subtopic = None  # Reset subtopic when topic changes

# ✅ Main Content - Display Subtopics
if st.session_state.selected_topic:
    filtered_data = sheet_data[sheet_data["Topic"] == st.session_state.selected_topic]
    st.title(f"{st.session_state.selected_topic}")
    st.write("### Choose a subtopic to learn:")

    subtopics = filtered_data["Subtopic"].unique()
    cols = st.columns(min(3, len(subtopics)))

    for idx, subtopic in enumerate(subtopics):
        col_idx = idx % 3
        is_done = st.session_state.subtopic_status.get(subtopic, False)

        # ✅ Change button color dynamically
        button_label = f"✅ {subtopic}" if is_done else subtopic

        with cols[col_idx]:
            if st.button(button_label, key=f"subtopic_{idx}", use_container_width=True):
                st.session_state.selected_subtopic = subtopic  # ✅ Ensure subtopic is correctly set

            # ✅ "Mark as Done" or "Undo" Button
            if st.session_state.selected_subtopic == subtopic:
                if is_done:
                    if st.button(f"🔄 Undo '{subtopic}'", key=f"undo_{idx}", use_container_width=True):
                        toggle_subtopic_status(subtopic)
                else:
                    if st.button(f"✅ Mark '{subtopic}' as Done", key=f"done_{idx}", use_container_width=True):
                        toggle_subtopic_status(subtopic)

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