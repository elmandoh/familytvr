import os
import smtplib
import requests
import random
import re
import logging
from email.message import EmailMessage
from email.utils import formataddr

# إعداد سجل الأخطاء
logging.basicConfig(level=logging.INFO)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")

# إعدادات الروابط
BLOG_URL = "https://familytvr.blogspot.com"
YOUTUBE_PLAYLIST_ID = "PLN9vn0_krfsFF7mE3MyB_OIRz4XODZbA4"
DAILYMOTION_VIDEO_ID = "x91z8m8"

APPS = [
    {"name": "Luxury Estate Guide", "url": "https://play.google.com/store/apps/details?id=com.eslam.luxuryestate"},
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"}
]

GAMING_TOPICS = [
    "The Secret Evolution of Game Physics Engines",
    "Uncovering Hidden Files in Retro Gaming History",
    "How Game Developers Optimize Open Worlds for Mobile",
    "The Art of Coding Combat: Secrets of AAA Studios",
    "Procedural Generation: The Future of Endless Gaming Secrets"
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
    1. Viral H1 Title.
    2. Meta Description.
    3. PLACEHOLDER_YT: For YouTube.
    4. PROMOTION_BOX: Highlight {selected_app['name']} ({selected_app['url']}).
    5. PLACEHOLDER_DM: For Dailymotion.
    6. Language: Professional English."""

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=120)
        content = response.json()['choices'][0]['message']['content']
        content = content.replace("PLACEHOLDER_YT", yt_code).replace("PLACEHOLDER_DM", dm_code)
        
        promo_box = f'''<div style="background:#f8fafc;border:2px solid #3b82f6;padding:25px;text-align:center;border-radius:15px;margin:25px 0;">
            <h3 style="color:#1e40af;">🎮 Recommended: {selected_app['name']}</h3>
            <a href="{selected_app['url']}" style="background:#3b82f6;color:white;padding:12px 30px;text-decoration:none;border-radius:8px;font-weight:bold;display:inline-block;">Download Now</a>
        </div>'''
        content = content.replace("PROMOTION_BOX", promo_box)
        return content
    except Exception as e:
        print(f"❌ Generation Error: {e}")
        return None

def send_to_blogger(content):
    if not content:
        return
    
    # تنظيف شامل للمتغيرات لمنع خطأ ValueError: Header values
    sender_email = os.getenv("SENDER_EMAIL").strip()
    sender_password = os.getenv("SENDER_PASSWORD").strip()
    blogger_email = os.getenv("BLOGGER_EMAIL").strip()
    
    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"Gaming Insight {random.randint(100,999)}"
    
    # تنظيف العنوان من أي رموز غير قياسية ومن الأسطر الجديدة
    clean_subject = re.sub(r'[^\x00-\x7f]', r'', subject).replace('\n', '').replace('\r', '').strip()

    msg = EmailMessage()
    msg['Subject'] = clean_subject
    
    # بناء العناوين بتنسيق سليم
    msg['From'] = formataddr(("Eslam Automation", sender_email))
    msg['To'] = formataddr(("Blogger Publisher", blogger_email))
    
    msg.add_header('Content-Type', 'text/html', charset='utf-8')
    msg.set_payload(content.encode('utf-8'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            smtp.quit()
        
        print("-" * 35)
        print(f"✅ تم النشر بنجاح!")
        print(f"📝 العنوان: {clean_subject}")
        print(f"🔗 المدونة: {BLOG_URL}")
        print("-" * 35)
        
    except Exception as e:
        print(f"❌ فشل النشر. نوع الخطأ: {type(e).__name__}")
        print(f"❌ التفاصيل: {str(e)}")

if __name__ == "__main__":
    article_content = generate_article()
    if article_content:
        send_to_blogger(article_content)
