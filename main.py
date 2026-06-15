def save_daily_update(content):
    import os
    os.makedirs("daily_updates", exist_ok=True)
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    file_name = f"daily_updates/Daily_Update_{current_date}.md"
    with open(file_name, 'w') as f:
        f.write(content)
    print(f"✅ Saved: {file_name}", flush=True)

if __name__ == "__main__":
    print("🔄 Starting script...", flush=True)
    try:
        news_data = fetch_daily_news()
        save_daily_update(news_data)
        print("✅ Done.", flush=True)
    except Exception as e:
        print(f"❌ ERROR: {e}", flush=True)
        raise
