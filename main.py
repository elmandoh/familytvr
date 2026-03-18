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

def generate_tech_content(title):
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192", # أو الموديل اللي بتستخدمه
            messages=[
                {"role": "system", "content": "You are a tech and entertainment journalist."},
                {"role": "user", "content": prompt} # البرومبت اللي فوق
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating content: {e}")
        return f"<h1>{title}</h1><p>Check out our latest post on the blog!</p>"
    # برومبت احترافي يركز على الـ SEO والزرار
   prompt = 
    f"""
      You are an expert Content Creator in Tech and Entertainment. 
        Write a viral, SEO-optimized blog post in HTML format about this topic: "{title}".

   STRICT INSTRUCTIONS:
    1. Viral H1 Title: Create a catchy title including a trending hashtag (e.g., #Tech, #Streaming, #Gaming).
    2. Meta Description: Start with a 150-character SEO Meta Description at the very beginning.
    3. Content Structure: Use at least 5+ sections with <h2> tags (e.g., Overview, Top Features, Why it's Viral, How to Access, Final Verdict).
    4. HTML Data Table: Create a professional HTML table showing current market rates for Gold, Silver, and Currency (USD/EUR) as a 'Daily Tech-Finance' bonus section.
    5. PROMOTION: Include this EXACT HTML button: 
      <div style='text-align: center; margin: 20px;'><a href='https://familytvr.blogspot.com/' style='background-color: #28a745; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;'>Get the Family TV App Now</a></div>
    6. Footer: Add a bold <footer> with a warning: "⚠️ **Warning: Ensure you download our official mobile app only from our blog to avoid fake versions!**"
    7. Formatting: Use strictly clean HTML tags (p, h2, ul, li, table).

  Target Audience: USA & Europe. 
  Tone: Energetic, Professional, and Tech-savvy."""

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
