import datetime
import os
import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

# --- CONFIGURATION ---
# Your personal email address where you want to receive the daily news files
USER_EMAIL = "gnosfa@gmail.com"
SERVICE_ACCOUNT_FILE = "credentials.json"

def fetch_daily_news():
    """
    Fetches raw daily news headers across your 5 custom categories.
    Using NewsAPI.org developer tier as a placeholder.
    """
    categories = ["Current Affairs", "Business", "Technology", "Agriculture", "Sports"] [cite: 2]
    
    # 1. Establish the current date for the document header
    today_str = datetime.date.today().strftime("%B %d, %Y")
    markdown_content = f"# 📰 Daily News Update - {today_str}\n\n---\n\n" [cite: 8, 50]
    
    # 2. Loop through categories and mock/fetch data
    for category in categories:
        markdown_content += f"## {category}\n"
        # In production, replace this with active requests.get() calls to your NewsAPI endpoint [cite: 6]
        markdown_content += f"* **Verified Update 1:** Major global developments occurred in {category} today.\n"
        markdown_content += f"* **Verified Update 2:** Secondary credible market or regional event logged successfully.\n\n"
        
    return markdown_content

def upload_to_google_drive(content):
    """
    Authenticates with Google Drive, uploads the file to the service account's space,
    and then auto-shares it with the user to bypass standard storage quotas.
    """
    # Define API scopes and authenticate 
    SCOPES = ['https://www.googleapis.com/auth/drive'] [cite: 168]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES) [cite: 168]
    service = build('drive', 'v3', credentials=creds) [cite: 168]
    
    # Dynamically generate the filename with the daily date 
    current_date = datetime.date.today().strftime("%Y-%m-%d") [cite: 168]
    file_name = f"Daily_Update_{current_date}.md" [cite: 168]
    
    # File Metadata targeting the service account's own root space (Bypasses Quota Error) [cite: 321, 331]
    file_metadata = {
        'name': file_name,
        'mimeType': 'text/markdown' [cite: 168]
    }
    
    # Convert string payload into standard upload stream 
    media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/markdown') [cite: 168, 238]
    
    # 1. Execute file creation request 
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id' [cite: 168]
    ).execute() [cite: 168]
    
    file_id = uploaded_file.get('id')
    
    # 2. 🔑 CRITICAL ADDITION: Automatically share this file with your personal email
    permission_metadata = {
        'type': 'user',
        'role': 'writer',  # Allows you to move, edit, or organize it freely
        'emailAddress': USER_EMAIL
    }
    
    service.permissions().create(
        fileId=file_id,
        body=permission_metadata
    ).execute()
    
    print(f"🎉 Success! Generated, uploaded, and shared: '{file_name}' (ID: {file_id})")

if __name__ == "__main__":
    news_data = fetch_daily_news() [cite: 168]
    upload_to_google_drive(news_data) [cite: 168]
