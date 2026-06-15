import datetime
import os
import sys                          # ✅ Add this import
import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

# ✅ Add these two debug lines right here, after imports
print(f"Python version: {sys.version}", flush=True)
print("Script started", flush=True)

# --- CONFIGURATION ---
USER_EMAIL = "gnosfa@gmail.com"
SERVICE_ACCOUNT_FILE = "credentials.json"

def fetch_daily_news():
    # ... your existing code ...

def upload_to_google_drive(content):
    # ... your existing code ...

if __name__ == "__main__":
    print("🔄 Starting script...", flush=True)
    news_data = fetch_daily_news()
    print("📰 News fetched, attempting upload...", flush=True)
    upload_to_google_drive(news_data)
    print("✅ Done.", flush=True)
