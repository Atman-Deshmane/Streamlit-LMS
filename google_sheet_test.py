import os
import gspread
import pandas as pd
from google.oauth2 import service_account
import streamlit as st
from pathlib import Path

def get_sheet_data():
    try:
        st.write("🔹 Starting get_sheet_data()...")  # Show progress in Streamlit UI

        # Define required scopes
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        
        st.write("🔹 Checking for secrets.toml file...")  # Show progress
        secrets_path = Path('.streamlit/secrets.toml')

        if secrets_path.exists():
            st.write("✅ Running on Streamlit Cloud... Using Streamlit Secrets")
            credentials_info = dict(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"])
            credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=scope)
        else:
            st.write("🔹 No secrets.toml found. Checking for GOOGLE_APPLICATION_CREDENTIALS environment variable...")
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

            if not credentials_path:
                st.error("❌ ERROR: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
                return pd.DataFrame()

            st.write(f"✅ Found credentials file at: {credentials_path}")  # Debugging step
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path, 
                scopes=scope
            )
            st.write("✅ Successfully loaded credentials.")

        # Common authentication logic
        st.write("🔹 Authenticating with Google Sheets API...")
        client = gspread.authorize(credentials)
        st.write("✅ Successfully authenticated.")

        st.write("🔹 Accessing LMS Google Sheet...")
        sheet = client.open("LMS").sheet1
        st.write("✅ Successfully opened the sheet!")

        st.write("🔹 Fetching all records from the sheet...")
        data = sheet.get_all_records()
        st.write(f"✅ Fetched {len(data)} records.")

        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"❌ ERROR: Failed to fetch data: {str(e)}")
        return pd.DataFrame()

# Only run when Streamlit executes the script
if __name__ == "__main__":
    st.write("🔹 Running in Streamlit mode...")
    df = get_sheet_data()
    
    if not df.empty:
        st.write("✅ Data Retrieved Successfully:")
        st.dataframe(df)  # Show the DataFrame in the Streamlit UI
    else:
        st.write("❌ No data retrieved. Check errors above.")