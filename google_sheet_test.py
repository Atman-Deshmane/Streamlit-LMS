import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Define a function to fetch data
def get_sheet_data():
    # Authenticate
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "physics-foundation-streamlit-5282814e8533.json", scope
    )
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = client.open("LMS").sheet1  # Replace "LMS" with your Sheet name

    # Fetch all records as a list of dictionaries
    data = sheet.get_all_records()

    # Convert to a DataFrame for easier handling
    df = pd.DataFrame(data)
    return df
