import datetime
import os
import sys
import requests

print(f"Python version: {sys.version}", flush=True)
print("Script started", flush=True)

# --- CONFIGURATION ---
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def call_gemini(prompt):
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    response = requests.post(GEMINI_URL, json=payload)
    result = response.json()
    
    # ✅ Debug — print full response if no candidates
    if "candidates" not in result:
        print(f"❌ Gemini API error response: {result}", flush=True)
        raise Exception(f"Gemini API error: {result}")
    
    return result["candidates"][0]["content"]["parts"][0]["text"]

def fetch_category_news(category, extra_context=""):
    print(f"🔍 Fetching {category} news...", flush=True)
    prompt = f"""
You are a professional news analyst. Today is {datetime.date.today().strftime("%B %d, %Y")}.

Give me the TOP 5 most important {category} news stories from today or the last 24 hours.
{extra_context}

For each story provide:
1. A clear headline
2. A 2-3 sentence summary of what happened
3. The impact — who is affected and why it matters

Format each story exactly like this:

### [Headline]
**What happened:** [2-3 sentence summary]
**Impact:** [Who is affected and why it matters]

---

Only include verified, credible news. No speculation.
"""
    return call_gemini(prompt)

def fetch_daily_news():
    print("📰 Starting news fetch...", flush=True)
    today_str = datetime.date.today().strftime("%B %d, %Y")
    markdown_content = f"# 📰 Daily News Brief - {today_str}\n\n---\n\n"

    categories = [
        {
            "name": "Current Affairs",
            "context": "Focus on major geopolitical, policy, and world events."
        },
        {
            "name": "Business & Economy",
            "context": "Focus on markets, trade, corporate news, and economic indicators. Include US market movements."
        },
        {
            "name": "Technology & AI",
            "context": "Focus on AI developments, tech industry news, product launches, and regulatory updates."
        },
        {
            "name": "Agriculture & Turmeric Markets",
            "context": """Focus on:
- Turmeric prices on NCDEX and MCX futures
- Spot market prices in Erode, Nizamabad, and Sangli
- India spice export news
- US and global agriculture commodity news
- Weather impacts on crops
Only cite verified sources like NCDEX.com, Agmarknet.gov.in, The Hindu BusinessLine, Economic Times Agri."""
        },
        {
            "name": "Sports",
            "context": "Focus on major results and upcoming events across cricket, football, tennis, and US sports."
        }
    ]

    for cat in categories:
        markdown_content += f"## {cat['name']}\n\n"
        news = fetch_category_news(cat['name'], cat['context'])
        markdown_content += news
        markdown_content += "\n\n"
        print(f"✅ {cat['name']} done.", flush=True)

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
        saved_file = save_daily_update(news_data)
        print(f"✅ Done. File saved: {saved_file}", flush=True)
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}", flush=True)
        import traceback
        traceback.print_exc()
        raise
