import os
import time
import json
import gspread
import pandas as pd
from google.oauth2 import service_account
import streamlit as st
from pathlib import Path

def get_credentials():
    """Get credentials without caching"""
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        
        local_creds_path = "/Users/atmandeshmane/Documents/physics-foundation-streamlit-5282814e8533.json"
        
        if os.path.exists(local_creds_path):
            credentials = service_account.Credentials.from_service_account_file(
                local_creds_path,
                scopes=scope
            )
            st.success("✅ Credentials loaded")
            return credentials
        else:
            st.error("❌ Credentials file not found")
            return None
    except Exception as e:
        st.error(f"❌ Authentication error: {str(e)}")
        return None

@st.cache_resource
def get_client(_credentials):
    """Get cached client connection"""
    try:
        with st.spinner("🔄 Connecting to Google API..."):
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
        with st.spinner("🔄 Accessing sheet..."):
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
    # Step 1: Get credentials
    credentials = get_credentials()
    
    if credentials:
        # Step 2: Get cached client
        client = get_client(credentials)
        
        if client:
            # Step 3: Get cached data
            values, fetch_time = get_sheet_data(client)
            
            if values:
                # Data preview
                df = pd.DataFrame(values[1:], columns=values[0])
                st.write(f"📊 Found {len(df)} rows and {len(df.columns)} columns")
                st.dataframe(df.head())
                
                # Performance metric
                st.info(f"⏱️ Total fetch time: {fetch_time:.2f}s")

# System info
with st.expander("System Information"):
    st.write(f"- Python version: {pd.__version__}")
    st.write(f"- Working directory: {os.getcwd()}")
    st.write(f"- Streamlit version: {st.__version__}")