import gspread
from google.oauth2 import service_account
import os
import streamlit as st

st.write("🔍 Checking GOOGLE_APPLICATION_CREDENTIALS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

try:
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not credentials_path:
        st.error("❌ No credentials found! Set GOOGLE_APPLICATION_CREDENTIALS in Streamlit Cloud.")
    else:
        st.success(f"✅ Found credentials: {credentials_path}")

    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=scope
    )
    client = gspread.authorize(credentials)
    sheet = client.open("LMS").sheet1  # ✅ Ensure the sheet name is correct
    data = sheet.get_all_records()

    if data:
        df = pd.DataFrame(data)
        st.write("✅ Google Sheets Data:", df.head())  # Show first few rows
    else:
        st.error("❌ ERROR: Google Sheets returned an empty response.")

except Exception as e:
    st.error(f"❌ ERROR: {str(e)}")