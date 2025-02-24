import os
import time
import json
import gspread
import pandas as pd
from google.oauth2 import service_account
import streamlit as st
from pathlib import Path

def get_credentials():
    """Get credentials based on environment"""
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        
        # Check for local secrets.toml
        secrets_path = Path('.streamlit/secrets.toml')
        
        if secrets_path.exists():
            st.write("🌩️ Testing Cloud Authentication...")
            credentials_info = dict(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"])
            credentials = service_account.Credentials.from_service_account_info(
                credentials_info, 
                scopes=scope
            )
        else:
            st.write("💻 Testing Local Authentication...")
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if not credentials_path:
                st.error("❌ GOOGLE_APPLICATION_CREDENTIALS not set")
                return None
            
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path, 
                scopes=scope
            )
        
        st.success("✅ Credentials loaded successfully")
        return credentials
            
    except Exception as e:
        st.error(f"❌ Authentication error: {str(e)}")
        return None

@st.cache_resource
def get_client(_credentials):
    """Get cached client connection"""
    try:
        with st.spinner("🔄 Testing Google API connection..."):
            start = time.time()
            client = gspread.authorize(_credentials)
            auth_time = time.time() - start
            st.success(f"✅ Connected in {auth_time:.2f}s")
            return client
    except Exception as e:
        st.error(f"❌ Connection error: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def get_sheet_data(_client):
    """Get cached sheet data"""
    try:
        with st.spinner("🔄 Testing sheet access..."):
            start = time.time()
            sheet = _client.open("LMS").sheet1
            values = sheet.get_values()
            fetch_time = time.time() - start
            st.success(f"✅ Data fetched in {fetch_time:.2f}s")
            return values, fetch_time
    except Exception as e:
        st.error(f"❌ Sheet access error: {str(e)}")
        return None, None

# Main debug interface
st.title("🔍 Google Sheets Integration Debug")

if st.button("Run Debug Tests", type="primary"):
    # Step 1: Test credentials
    credentials = get_credentials()
    
    if credentials:
        # Step 2: Test client connection
        client = get_client(credentials)
        
        if client:
            # Step 3: Test data fetch
            values, fetch_time = get_sheet_data(client)
            
            if values:
                # Data preview
                df = pd.DataFrame(values[1:], columns=values[0])
                st.write(f"📊 Found {len(df)} rows and {len(df.columns)} columns")
                st.dataframe(df.head())
                
                # Performance metrics
                st.info(f"⏱️ Total fetch time: {fetch_time:.2f}s")

# Debug information
with st.expander("🔧 Debug Information"):
    st.write(f"- Environment: {'Cloud' if Path('.streamlit/secrets.toml').exists() else 'Local'}")
    st.write(f"- Working Directory: {os.getcwd()}")
    st.write(f"- Python Version: {pd.__version__}")
    st.write(f"- Streamlit Version: {st.__version__}")