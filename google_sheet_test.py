import os
import json
import gspread
import pandas as pd
from google.oauth2 import service_account
import streamlit as st

def get_sheet_data():
    try:
        # Define required scopes for accessing Google Sheets
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        # Check if running in Streamlit Cloud (remote) or locally
        if "STREAMLIT_ENV" in os.environ:  # Custom check for Streamlit Cloud
            st.write("🔄 Running on Streamlit Cloud...")
            # Load credentials from Streamlit secrets
            credentials_info = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
            credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=scope)
        else:
            st.write("🔄 Running locally...")
            # Load credentials from the environment variable
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if not credentials_path:
                raise EnvironmentError("Environment variable 'GOOGLE_APPLICATION_CREDENTIALS' is not set.")
            credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scope)

        # Authenticate with Google Sheets
        client = gspread.authorize(credentials)

        # Open the Google Sheet and fetch data
        sheet = client.open("LMS").sheet1  # Replace "LMS" with your Google Sheet name
        data = sheet.get_all_records()

        # Convert to Pandas DataFrame
        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return None

# For testing
if __name__ == "__main__":
    df = get_sheet_data()
    if df is not None:
        print(df)
