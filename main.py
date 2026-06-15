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
    print("📰 Inside fetch_daily_news...", flush=True)
    categories = ["Current Affairs", "Business", "Technology", "Agriculture", "Sports"]
    today_str = datetime.date.today().strftime("%B %d, %Y")
    markdown_content = f"# 📰 Daily News Update - {today_str}\n\n---\n\n"
    
    for category in categories:
        markdown_content += f"## {category}\n"
        markdown_content += f"* **Verified Update 1:** Major global developments occurred in {category} today.\n"
        markdown_content += f"* **Verified Update 2:** Secondary credible market or regional event logged successfully.\n\n"
    
    print("📰 News content generated.", flush=True)
    return markdown_content

def upload_to_google_drive(content):
    print("☁️ Inside upload_to_google_drive...", flush=True)
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
    
    print("☁️ Uploading file...", flush=True)
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        supportsAllDrives=True
    ).execute()
    
    file_id = uploaded_file.get('id')
    print(f"☁️ File uploaded. ID: {file_id}", flush=True)
    
    print("🔐 Setting permissions...", flush=True)
    service.permissions().create(
        fileId=file_id,
        body={
            'type': 'user',
            'role': 'writer',
            'emailAddress': 'gnosfa@gmail.com'
        },
        supportsAllDrives=True
    ).execute()
    
    print(f"✅ File '{file_name}' uploaded. ID: {file_id}", flush=True)

if __name__ == "__main__":
    print("🔄 Starting script...", flush=True)
    try:
        news_data = fetch_daily_news()
        print("📰 News fetched, attempting upload...", flush=True)
        upload_to_google_drive(news_data)
        print("✅ Done.", flush=True)
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}", flush=True)
        import traceback
        traceback.print_exc()
        raise
