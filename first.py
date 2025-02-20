import os
import gspread
import pandas as pd
from google.oauth2 import service_account
import streamlit as st
import time
from pathlib import Path
def get_sheet_data():
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        running_in_cloud = "STREAMLIT_ENV" in os.environ

        if running_in_cloud:
            st.write("✅ Running on Streamlit Cloud...")
            if "GOOGLE_APPLICATION_CREDENTIALS" not in st.secrets:
                st.error("❌ ERROR: GOOGLE_APPLICATION_CREDENTIALS missing in Streamlit Cloud secrets!")
                return pd.DataFrame()

            credentials_info = dict(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"])
            credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=scope)

        else:
            st.write("💻 Running Locally...")
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            
            if not credentials_path:
                st.error("❌ ERROR: GOOGLE_APPLICATION_CREDENTIALS environment variable is missing!")
                return pd.DataFrame()

            if "google_credentials" not in st.session_state:
                st.session_state.google_credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scope)

            credentials = st.session_state.google_credentials

        client = gspread.authorize(credentials)
        sheet = client.open("LMS").sheet1

        # **DEBUG TIMING**
        start = time.time()
        data = sheet.get_all_records()
        end = time.time()

        st.write(f"✅ Data fetched in {end - start:.2f} seconds")

        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"❌ ERROR: {str(e)}")
        return pd.DataFrame()

df = get_sheet_data()

if not df.empty:
    st.dataframe(df)