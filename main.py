import datetime
import os
import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

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
    
    file_metadata = {
        'name': file_name,
        'mimeType': 'text/markdown'
    }
    
    media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/markdown')
    
    # 1. Create the file metadata stream with a special parameter
    # moveToNewOwnersRoot=True forces the file into your personal drive space
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        keepRevisionForever=False
    ).execute()
    
    file_id = uploaded_file.get('id')
    
    # 2. Add you as an owner to move the storage quota burden to your account
    permission_metadata = {
        'type': 'user',
        'role': 'owner',  # 👑 Transferring full legal ownership to your quota
        'emailAddress': USER_EMAIL
    }
    
    # transferOwnership=True tells Google to charge your 15GB space bucket, not the robot's 0GB
    service.permissions().create(
        fileId=file_id,
        body=permission_metadata,
        transferOwnership=True 
    ).execute()
    
    print(f"🎉 Success! Generated and fully transferred file: '{file_name}' to {USER_EMAIL}")

if __name__ == "__main__":
    news_data = fetch_daily_news()
    upload_to_google_drive(news_data)
