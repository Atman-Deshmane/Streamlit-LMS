import streamlit as st
import secrets  # ✅ Generate random state value

# Ensure Azure Config is defined
AZURE_CONFIG = {
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "authority": "https://login.microsoftonline.com/common",
    "redirect_uri": "https://physiks.streamlit.app/",
    "scope": ["openid", "profile", "email"]
}

# ✅ Ensure session state variables are initialized
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "oauth_state" not in st.session_state or st.session_state.oauth_state is None:
    st.session_state.oauth_state = secrets.token_urlsafe(16)  # ✅ Generate a new state value

def microsoft_login():
    try:
        auth_url = f"{AZURE_CONFIG['authority']}/oauth2/v2.0/authorize" \
                   f"?client_id={AZURE_CONFIG['client_id']}" \
                   f"&response_type=code" \
                   f"&redirect_uri={AZURE_CONFIG['redirect_uri']}" \
                   f"&scope={' '.join(AZURE_CONFIG['scope'])}" \
                   f"&state={st.session_state.oauth_state}" \
                   f"&prompt=select_account"

        # ✅ **Updated button text to "Login to Save Progress"**
        st.markdown(f'''
            <a href="{auth_url}" target="_blank">
                <button style="
                    background-color: #2F2F2F;
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    width: 100%;
                    margin: 4px 0;
                ">
                    Login to Save Progress
                </button>
            </a>
        ''', unsafe_allow_html=True)

        # ✅ **Show the URL in Streamlit to manually test**
        st.write("🔗 **If the button doesn’t work, copy-paste this:**")
        st.code(auth_url, language="plaintext")  # ✅ Shows the link to test

    except Exception as e:
        st.error(f"Login failed: {str(e)}")

# ✅ **Debug Info in Sidebar**
with st.sidebar:
    st.write("### Debug Info 🐛")
    st.write(f"Authenticated: {st.session_state.authenticated}")  # ✅ Now properly initialized
    st.write(f"OAuth State: {st.session_state.oauth_state}")  # ✅ Debug: Show OAuth state

    # ✅ **Ensure login button is visible**
    if not st.session_state.authenticated:
        st.write("### Save Your Progress")
        microsoft_login()