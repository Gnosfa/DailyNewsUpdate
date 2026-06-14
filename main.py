{\rtf1\ansi\ansicpg1252\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import datetime\
import os\
import requests\
from google.oauth2.service_account import Credentials\
from googleapiclient.discovery import build\
from googleapiclient.http import MediaInMemoryUpload\
\
# --- CONFIGURATION ---\
# Replace with the long string of characters from your Google Drive folder's URL\
DRIVE_FOLDER_ID = "YOUR_GOOGLE_DRIVE_FOLDER_ID" \
SERVICE_ACCOUNT_FILE = "credentials.json"\
\
def fetch_daily_news():\
    """\
    Fetches raw daily news headers across your 5 custom categories.\
    Using NewsAPI.org developer tier as a placeholder.\
    """\
    categories = ["Current Affairs", "Business", "Technology", "Agriculture", "Sports"]\
    \
    # 1. Establish the current date for the document header\
    today_str = datetime.date.today().strftime("%B %d, %Y")\
    markdown_content = f"# \uc0\u55357 \u56560  Daily News Update - \{today_str\}\\n\\n---\\n\\n"\
    \
    # 2. Loop through categories and mock/fetch data\
    for category in categories:\
        markdown_content += f"## \{category\}\\n"\
        # In production, replace this with active requests.get() calls to your NewsAPI endpoint\
        markdown_content += f"* **Verified Update 1:** Major global developments occurred in \{category\} today.\\n"\
        markdown_content += f"* **Verified Update 2:** Secondary credible market or regional event logged successfully.\\n\\n"\
        \
    return markdown_content\
\
def upload_to_google_drive(content):\
    """\
    Authenticates with Google Drive and uploads the markdown string with a dated filename.\
    """\
    # Define API scopes and authenticate\
    SCOPES = ['https://www.googleapis.com/auth/drive']\
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)\
    service = build('drive', 'v3', credentials=creds)\
    \
    # Dynamically generate the filename with the daily date\
    current_date = datetime.date.today().strftime("%Y-%m-%d")\
    file_name = f"Daily_Update_\{current_date\}.md"\
    \
    # File Metadata targeting your specific shared folder\
    file_metadata = \{\
        'name': file_name,\
        'parents': [DRIVE_FOLDER_ID],\
        'mimeType': 'text/markdown'\
    \}\
    \
    # Convert string payload into standard upload stream\
    media = MediaInMemoryUpload(content.encode('utf-8'), mimeType='text/markdown')\
    \
    # Execute creation request\
    uploaded_file = service.files().create(\
        body=file_metadata,\
        media_body=media,\
        fields='id'\
    ).execute()\
    \
    print(f"\uc0\u55356 \u57225  Success! Generated and uploaded: '\{file_name\}' to Drive. (ID: \{uploaded_file.get('id')\})")\
\
if __name__ == "__main__":\
    news_data = fetch_daily_news()\
    upload_to_google_drive(news_data)}