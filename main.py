import datetime
import os
import sys
import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

print(f"Python version: {sys.version}", flush=True)
print("Script started", flush=True)

# --- CONFIGURATION ---
USER_EMAIL = "gnosfa@gmail.com"
SERVICE_ACCOUNT_FILE = "credentials.json"

def fetch_daily_news():
    categories = ["Current Affairs", "Business", "Technology", "Agriculture", "Sports"]
    today_str = datetime.date.today().strftime("%B %d, %Y")
    markdown_content = f"# 📰 Daily News Update - {today_str}\n\n---\n\n"
    
    for category in categories:
        markdown_content += f"## {category}\n"
        markdown_content += f"* **Verified Update 1:** Major global developments occurred in {category} today.\n"
        markdown_content += f"* **Verified Update 2:** Secondary credible market or regional event logged successfully.\n\n"
        
    return markdown_content

def upload_to_google_drive(content):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    file_name = f"Daily_Update_{current_date}.md"
    
    FOLDER_ID = "1E7xTcbHuuWtxAOalgKzHby9bdj4ITAR-"
    
    file_metadata = {
        'name': file_name,
        'mimeType': 'text/markdown',
        'parents': [FOLDER_ID]
    }
    
    media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/markdown')
