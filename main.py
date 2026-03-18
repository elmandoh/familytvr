import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")

# قائمة تطبيقاتك الـ 20
APPS = [
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"},
    {"name": "Design AI 2", "url": "https://play.google.com/store/apps/details?id=design.ai2"},
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "Insurance App Guide", "url": "https://play.google.com/store/apps/details?id=insurance.aplicnem"}
    # أضف البقية هنا بنفس التنسيق
]

# كلمات مفتاحية قوية لرفع الـ SEO في أمريكا
KEYWORDS = ["US Housing Market 2026", "Gold Price Prediction", "Best Stocks to Buy", "Passive Income USA", "Luxury Real Estate Trends"]

def generate_pro_article():
    app = random.choice(APPS)
    kw = random.sample(KEYWORDS, 2) # اختيار كلمتين بحث عشوائيتين
    
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    # برومبت احترافي يركز على الـ SEO والزرار
    prompt = f"""Write a VIRAL 900-word SEO article for a US audience.
    Topic: High-impact analysis of {kw[0]} and {kw[1]} in 2026.
    
    Instructions:
    1. Viral H1 Title with hashtag.
    2. Add a 150-character SEO Meta Description at the very beginning.
    3. Use 5+ sections with H2 tags.
    4. Create an HTML data table for Gold, Silver, and Currency rates.
    5. PROMOTION: Include this EXACT HTML button: 
       <div style='text-align: center; margin: 20px;'><a href='{app['url']}' style='background-color: #28a745; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;'>Get the {app['name']} Now</a></div>
    6. Footer: Add a bold warning about downloading the blog's mobile app.
    7. Formatting: Strictly use clean HTML."""

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=120)
        return response.json()['choices'][0]['message']['content']
    except: return None

def send_to_blogger(content):
    if not content or len(content) < 2000: return

    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"Market Update {random.randint(100, 999)}"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(content, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
        smtp.send_message(msg)
    print(f"✅ Success: Published with SEO Boost and Button!")

if __name__ == "__main__":
    article = generate_pro_article()
    send_to_blogger(article)
