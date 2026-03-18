import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")

# قائمة تطبيقاتك الـ 20 (سيختار البوت واحداً عشوائياً لكل مقال)
APPS = [
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"},
    {"name": "Design AI 2", "url": "https://play.google.com/store/apps/details?id=design.ai2"},
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "Insurance App Guide", "url": "https://play.google.com/store/apps/details?id=insurance.aplicnem"}
]

def generate_pro_article():
    # اختيار تطبيق وعنوان عشوائي
    selected_app = random.choice(APPS)
    topics = ["Streaming Trends 2026", "Next-Gen AI Gadgets", "Future of Entertainment Tech"]
    title = random.choice(topics)
    
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    # تم إصلاح المسافات (Indentation) هنا لضمان عمل الكود
    prompt = f"""Write a viral, SEO-optimized blog post in HTML about: "{title}".
    STRICT INSTRUCTIONS:
    1. Viral H1 Title with #Tech #Entertainment.
    2. 150-char SEO Meta Description at the beginning.
    3. 5+ sections with <h2> tags.
    4. HTML Data Table for Gold/Silver/Currency (USD/EUR).
    5. PROMOTION: Include this exact box in the middle of content:
       <div style='background: #f0fdf4; border: 2px solid #16a34a; padding: 20px; text-align: center; border-radius: 10px; margin: 20px 0;'>
          <h3>🚀 Featured App: {selected_app['name']}</h3>
          <p>Get the best experience. Download our official app now!</p>
          <a href='{selected_app['url']}' style='background-color: #16a34a; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;'>Install from Play Store</a>
       </div>
    6. Footer: Bold warning about official downloads.
    7. Formatting: Clean HTML only."""

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=120)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_to_blogger(content):
    if not content: return
    # استخراج العنوان من H1
    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"Tech Update {random.randint(100,999)}"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = "familytvr11.eslammosde@blogger.com" # الإيميل الصحيح
    msg.set_content(content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
        print("✅ Published to Blogger with Promo Box!")
    except Exception as e:
        print(f"❌ Email Error: {e}")

if __name__ == "__main__":
    article = generate_pro_article()
    if article:
        send_to_blogger(article)
