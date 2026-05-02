import os
import smtplib
import requests
import random
import re
import time
import logging
from email.message import EmailMessage

# إعداد سجل الأخطاء (Logging) لتعقب مشاكل النشر
logging.basicConfig(
    filename='gaming_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")

# إعدادات التضمين (تأكد من صحة الـ IDs لزيادة الأرباح وساعات المشاهدة)
YOUTUBE_PLAYLIST_ID = "PLN9vn0_krfsFF7mE3MyB_OIRz4XODZbA4"
DAILYMOTION_VIDEO_ID = "x91z8m8" # الفيديو الذي فعلت فيه التضمين مؤخراً

# قائمة تطبيقاتك الـ 20 (سيختار البوت واحداً عشوائياً للترويج له)
APPS = [
    {"name": "Luxury Estate Guide", "url": "https://play.google.com/store/apps/details?id=com.eslam.luxuryestate"},
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"}
]

# المواضيع العامة التي طلبتها (أسرار وإنتاج الألعاب)
GAMING_TOPICS = [
    "Hidden Secrets of Game Engine Optimization",
    "How AAA Studios Design Impossible Secret Levels",
    "The Physics of Combat: Coding Realistic Mechanics",
    "Evolution of Mobile Game Development: From Java to Kotlin",
    "Unsolved Mysteries Hidden in Classic Game Files",
    "Procedural Generation: How Games Create Infinite Worlds"
]

def get_embed_codes():
    """توليد أكواد التضمين المتجاوبة لليوتيوب ودايلي موشن"""
    yt_embed = f'''<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;margin:20px 0;"><iframe src="https://www.youtube.com/embed/videoseries?list={YOUTUBE_PLAYLIST_ID}" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allowfullscreen></iframe></div>'''
    dm_embed = f'''<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;margin:20px 0;border-radius:12px;"><iframe src="https://www.dailymotion.com/embed/video/{DAILYMOTION_VIDEO_ID}?syndication=276410" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allowfullscreen></iframe></div>'''
    return yt_embed, dm_embed

def generate_article():
    selected_app = random.choice(APPS)
    topic = random.choice(GAMING_TOPICS)
    yt_code, dm_code = get_embed_codes()
    
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    # الـ Prompt المطور لإنتاج محتوى "أسرار وإنتاج"
    prompt = f"""Write a professional 1500-word blog post in HTML about: "{topic}".
    STRICT REQUIREMENTS:
    1. Viral H1 Title about Gaming Secrets/Production.
    2. 150-char SEO Meta Description.
    3. Use <h2> and <h3> tags for: History, Development Insights, and Hidden Secrets.
    4. An HTML Table comparing 3 games related to the topic (Tech, Difficulty, Secret Level).
    5. PLACEHOLDER_YT: For YouTube Podcast.
    6. PROMOTION_BOX: Highlight {selected_app['name']} with a link to {selected_app['url']}.
    7. PLACEHOLDER_DM: For Monetized Video.
    8. Footer with bold warning about official game downloads.
    9. Language: Professional English (best for global ads)."""

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=120)
        content = response.json()['choices'][0]['message']['content']
        
        # استبدال الـ Placeholders بالأكواد الحقيقية
        content = content.replace("PLACEHOLDER_YT", yt_embed)
        content = content.replace("PLACEHOLDER_DM", dm_embed)
        
        # إنشاء صندوق الترويج بـ CSS احترافي
        promo_box = f'''<div style="background:#f8fafc;border:2px solid #3b82f6;padding:25px;text-align:center;border-radius:15px;margin:25px 0;">
            <h3 style="color:#1e40af;">🎮 Recommended Tool: {selected_app['name']}</h3>
            <p>Enhance your experience with our official pro app.</p>
            <a href="{selected_app['url']}" style="background:#3b82f6;color:white;padding:12px 30px;text-decoration:none;border-radius:8px;font-weight:bold;display:inline-block;">Download Now</a>
        </div>'''
        content = content.replace("PROMOTION_BOX", promo_box)
        
        return content
    except Exception as e:
        logging.error(f"Generation Error: {e}")
        return None

def send_to_blogger(content):
    if not content: return
    
    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"Gaming Secret {random.randint(100,999)}"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = "eslammosde.tech5@blogger.com" # إيميل بلوجر الصحيح الخاص بك
    msg.set_content(content, subtype='html')

    try:
        # استخدام نظام إغلاق الاتصال الآمن لمنع توقف النشر
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
            smtp.quit() 
        logging.info(f"✅ Successfully published: {subject}")
        print(f"✅ Published: {subject}")
    except Exception as e:
        logging.error(f"❌ Email Error: {e}")
        print(f"❌ Email Error: {e}")

if __name__ == "__main__":
    # تشغيل السكريبت ونشر مقال واحد
    logging.info("Bot started running...")
    article_content = generate_article()
    if article_content:
        send_to_blogger(article_content)
    
    # نصيحة: إذا كنت ستشغله في حلقة (Loop)، أضف time.sleep(900) هنا لمنع الحظر
