import os
import json
import gspread
import pandas as pd
from google.oauth2 import service_account
import streamlit as st
from pathlib import Path

def get_sheet_data(sheet_name="Ayushkaari", worksheet_name="Sheet1"):
    try:
        # Define required scopes
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        # Check for local secrets.toml
        secrets_path = Path('.streamlit/secrets.toml')
        
        if secrets_path.exists():
            # Load credentials directly from Streamlit secrets and convert to dict
            credentials_info = dict(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"])
            credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=scope)
        else:
            # Local environment with env variable
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if not credentials_path:
                st.error("Please set GOOGLE_APPLICATION_CREDENTIALS environment variable")
                return pd.DataFrame()
            
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path, 
                scopes=scope
            )

        # Common authentication logic
        client = gspread.authorize(credentials)
        
        # Open the specific sheet and worksheet
        spreadsheet = client.open(sheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    

    except Exception as e:
        st.error(f"Failed to fetch data: {str(e)}")
        return pd.DataFrame()

if __name__ == "__main__":
    df = get_sheet_data()
    if not df.empty:
        print(df) 