import gspread
from google.oauth2 import service_account
import os
import pandas as pd
import streamlit as st
import time

st.write("🔍 Checking GOOGLE_APPLICATION_CREDENTIALS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# Check if credentials are available
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not credentials_path:
    if "GOOGLE_APPLICATION_CREDENTIALS" in st.secrets:
        credentials_path = "/tmp/credentials.json"
        with open(credentials_path, "w") as f:
            f.write(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"])
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        st.success("✅ Credentials loaded from Streamlit Secrets!")
    else:
        st.error("❌ No credentials found! Set GOOGLE_APPLICATION_CREDENTIALS in your environment or Streamlit Secrets.")

@st.cache_data  # Caches the fetched data, preventing repeated slow API calls
def fetch_google_sheet_data():
    try:
        start_time = time.time()
        
        # Authenticate using credentials
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scope)
        client = gspread.authorize(credentials)

        elapsed_time = time.time() - start_time
        st.write(f"✅ Authentication completed in {elapsed_time:.2f} seconds")

        # Open Google Sheet
        sheet = client.open("LMS").sheet1  # ✅ Ensure sheet name is correct
        data = sheet.get_all_records()

        elapsed_time = time.time() - start_time
        st.write(f"✅ Fetched data in {elapsed_time:.2f} seconds")

        if data:
            df = pd.DataFrame(data)
            return df
        else:
            st.error("❌ ERROR: Google Sheets returned an empty response.")
            return pd.DataFrame()  # Return an empty DataFrame

    except Exception as e:
        st.error(f"❌ ERROR: {str(e)}")
        return pd.DataFrame()

# Fetch data
df = fetch_google_sheet_data()

# Display data if available
if not df.empty:
    st.write("✅ Google Sheets Data:")
    st.dataframe(df)