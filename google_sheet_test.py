from google.oauth2 import service_account
import gspread
import pandas as pd
import os

def get_sheet_data():
    # Define required scopes for accessing Google Sheets
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # Load credentials from the environment variable
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise EnvironmentError("Environment variable 'GOOGLE_APPLICATION_CREDENTIALS' is not set.")
    
    # Load credentials with the specified scope
    credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scope)

    # Authorize the Google Sheets client
    client = gspread.authorize(credentials)

    # Open the specified Google Sheet and access the first worksheet
    sheet = client.open("LMS").sheet1  # Replace "LMS" with your Sheet name

    # Fetch all records as a list of dictionaries
    data = sheet.get_all_records()

    # Convert the data into a Pandas DataFrame for easier handling
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # Fetch and print the data from the sheet (for local testing)
    df = get_sheet_data()
    print(df)
