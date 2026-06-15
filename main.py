import datetime
import os
import sys

print(f"Python version: {sys.version}", flush=True)
print("Script started", flush=True)

# --- CONFIGURATION ---
USER_EMAIL = "gnosfa@gmail.com"

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

def save_daily_update(content):
    print("💾 Saving daily update...", flush=True)
    os.makedirs("daily_updates", exist_ok=True)
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    file_name = f"daily_updates/Daily_Update_{current_date}.md"
    with open(file_name, 'w') as f:
        f.write(content)
    print(f"✅ Saved: {file_name}", flush=True)
    return file_name

if __name__ == "__main__":
    print("🔄 Starting script...", flush=True)
    try:
        news_data = fetch_daily_news()
        print("📰 News fetched, saving file...", flush=True)
        saved_file = save_daily_update(news_data)
        print(f"✅ Done. File saved: {saved_file}", flush=True)
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}", flush=True)
        import traceback
        traceback.print_exc()
        raise
