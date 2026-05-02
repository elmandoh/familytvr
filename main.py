import os
import smtplib
import requests
import random
import re
import time
import logging
from email.message import EmailMessage

# إعداد سجل الأخطاء
logging.basicConfig(level=logging.INFO)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")

# إعدادات الروابط والتطبيقات
BLOG_URL = "https://familytvr.blogspot.com"
YOUTUBE_PLAYLIST_ID = "PLN9vn0_krfsFF7mE3MyB_OIRz4XODZbA4"
DAILYMOTION_VIDEO_ID = "x91z8m8"

APPS = [
    {"name": "Luxury Estate Guide", "url": "https://play.google.com/store/apps/details?id=com.eslam.luxuryestate"},
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"}
]

GAMING_TOPICS = [
    "Hidden Secrets of Game Engine Optimization",
    "How AAA Studios Design Impossible Secret Levels",
    "The Physics of Combat: Coding Realistic Mechanics",
    "Evolution of Mobile Game Development: From Java to Kotlin",
    "Unsolved Mysteries Hidden in Classic Game Files",
    "Procedural Generation: How Games Create Infinite Worlds"
]

def get_embed_codes():
    yt_embed = f'''<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;margin:20px 0;"><iframe src="https://www.youtube.com/embed/videoseries?list={YOUTUBE_PLAYLIST_ID}" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allowfullscreen></iframe></div>'''
    dm_embed = f'''<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;margin:20px 0;border-radius:12px;"><iframe src="https://www.dailymotion.com/embed/video/{DAILYMOTION_VIDEO_ID}?syndication=276410" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allowfullscreen></iframe></div>'''
    return yt_embed, dm_embed

def generate_article():
    selected_app = random.choice(APPS)
    topic = random.choice(GAMING_TOPICS)
    yt_code, dm_code = get_embed_codes()
    
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""Write a professional 1500-word blog post in HTML about: "{topic}".
    STRICT REQUIREMENTS:
    1. Viral H1 Title about Gaming Secrets/Production.
    2. 150-char SEO Meta Description.
    3. Use <h2> and <h3> tags for sections.
    4. An HTML Table comparing 3 games.
    5. PLACEHOLDER_YT: For YouTube.
    6. PROMOTION_BOX: Highlight {selected_app['name']} ({selected_app['url']}).
    7. PLACEHOLDER_DM: For Dailymotion.
    8. Language: Professional English."""

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=120)
        content = response.json()['choices'][0]['message']['content']
        
        content = content.replace("PLACEHOLDER_YT", yt_code)
        content = content.replace("PLACEHOLDER_DM", dm_code)
        
        promo_box = f'''<div style="background:#f8fafc;border:2px solid #3b82f6;padding:25px;text-align:center;border-radius:15px;margin:25px 0;">
            <h3 style="color:#1e40af;">🎮 Recommended Tool: {selected_app['name']}</h3>
            <a href="{selected_app['url']}" style="background:#3b82f6;color:white;padding:12px 30px;text-decoration:none;border-radius:8px;font-weight:bold;display:inline-block;">Download Now</a>
        </div>'''
        content = content.replace("PROMOTION_BOX", promo_box)
        return content
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        return None

def send_to_blogger(content):
    if not content:
        print("❌ No content generated to publish.")
        return
    
    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"Gaming Secret {random.randint(100,999)}"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    
    # التعديل الجوهري: إضافة التشفير هنا يمنع خطأ الـ 555 نهائياً
    msg.set_content(content, subtype='html', charset='utf-8') 

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
            smtp.quit()
        
        # طباعة تفاصيل النشر كما طلبت
        print("-" * 30)
        print(f"✅ تم النشر بنجاح!")
        print(f"📝 عنوان المقالة: {subject}")
        # بلوجر يقوم بتحويل العنوان لرابط، هذا رابط تقريبي للمدونة
        print(f"🔗 رابط المدونة: {BLOG_URL}")
        print("-" * 30)
        
    except Exception as e:
        print(f"❌ فشل النشر. السبب: {e}")

if __name__ == "__main__":
    article_content = generate_article()
    if article_content:
        send_to_blogger(article_content)
