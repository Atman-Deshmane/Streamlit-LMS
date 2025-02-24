import time
import gspread
from google.oauth2 import service_account
import pandas as pd

credentials = service_account.Credentials.from_service_account_file(
    "/Users/atmandeshmane/Documents/physics-foundation-streamlit-5282814e8533.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets",
           "https://www.googleapis.com/auth/drive"]
)

client = gspread.authorize(credentials)
sheet = client.open("LMS").sheet1

start = time.time()
data = sheet.get_all_records()
end = time.time()

print(f"✅ Data fetched in {end - start:.2f} seconds")
df = pd.DataFrame(data)
print(df.head())  # Print first few rows