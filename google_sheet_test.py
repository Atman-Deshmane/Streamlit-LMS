from google.oauth2 import service_account
import gspread
import pandas as pd
import os

def get_sheet_data():
    print("Starting get_sheet_data function...")
    
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # Load credentials from the environment variable
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    print(f"Credentials Path: {credentials_path}")
    
    credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scope)
    print("Credentials loaded successfully.")

    # Use the credentials to authorize Google Sheets API
    client = gspread.authorize(credentials)
    print("Google Sheets client authorized.")

    # Open the Google Sheet
    sheet = client.open("LMS").sheet1  # Replace "LMS" with your Sheet name
    print("Google Sheet opened successfully.")

    # Fetch all records as a list of dictionaries
    data = sheet.get_all_records()
    print("Data fetched successfully from Google Sheets.")
    
    # Convert to a DataFrame for easier handling
    df = pd.DataFrame(data)
    print("Data converted to DataFrame:")
    print(df)
    return df

if __name__ == "__main__":
    get_sheet_data()
