import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")

# قائمة تطبيقاتك (تأكد من إضافة الـ 20 تطبيق هنا)
APPS = [
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"},
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "Design AI 2", "url": "https://play.google.com/store/apps/details?id=design.ai2"},
    # أضف بقية التطبيقات بنفس الشكل...
]

def generate_pro_article():
    # 1. اختيار تطبيق عشوائي للترويج له في هذا المقال
    selected_app = random.choice(APPS)
    
    # 2. اختيار عنوان تقني/ترفيهي
    topics = ["Best Streaming Apps 2026", "Top Tech Gadgets", "Future of Mobile Innovation", "Viral Entertainment Trends"]
    title = random.choice(topics)
    
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    # 3. البرومبت مع دمج بيانات التطبيق المختار
    prompt = f"""Write a viral, SEO-optimized blog post in HTML about: "{title}".
    
    STRICT INSTRUCTIONS:
    1. Viral H1 Title with #Tech #Entertainment.
    2. 150-char SEO Meta Description.
    3. 5+ sections with <h2> tags.
    4. HTML Data Table for Gold/Silver/Currency rates.
    5. PROMOTION: You MUST include this EXACT promotion box in the middle of the article:
       <div style='background: #f8f9fa; border: 2px solid #28a745; padding: 20px; text-align: center; border-radius: 10px; margin: 20px 0;'>
          <h3>🚀 Featured App of the Day</h3>
          <p>Looking for the best experience? Download <b>{selected_app['name']}</b> now!</p>
          <a href='{selected_app['url']}' style='background-color: #28a745; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;'>Install {selected_app['name']} from Play Store</a>
       </div>
    6. Footer: Add a bold warning about downloading only from official sources.
    7. Formatting: Clean HTML."""

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

# دالة الإرسال تبقى كما هي (send_to_blogger)
