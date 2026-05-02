import os
import smtplib
import requests
import random
import re
import logging
from email.message import EmailMessage
from email.utils import formataddr

# إعداد السجلات
logging.basicConfig(level=logging.INFO)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")

APPS = [
    {"name": "Luxury Estate Guide", "url": "https://play.google.com/store/apps/details?id=com.eslam.luxuryestate"},
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"}
]

GAMING_TOPICS = [
    "The Secret Evolution of Game Physics Engines",
    "Uncovering Hidden Files in Retro Gaming History",
    "How Game Developers Optimize Open Worlds for Mobile",
    "The Art of Coding Combat: Secrets of AAA Studios"
]

def clean_email_string(email_str):
    """تنظيف الإيميل من أي رموز مخفية مثل \u202b التي تسبب خطأ Unicode"""
    if not email_str: return ""
    # مسح أي رمز غير موجود في جدول ASCII (الرموز المخفية)
    return re.sub(r'[^\x00-\x7f]', '', email_str).strip()

def send_to_blogger(content):
    if not content: return
    
    # تنظيف صارم للمتغيرات
    sender_email = clean_email_string(os.getenv("SENDER_EMAIL"))
    sender_password = os.getenv("SENDER_PASSWORD").strip()
    blogger_email = clean_email_string(os.getenv("BLOGGER_EMAIL"))
    
    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"Gaming Insight {random.randint(100,999)}"
    clean_subject = re.sub(r'[^\x00-\x7f]', '', subject).replace('\n', '').replace('\r', '').strip()

    msg = EmailMessage()
    msg['Subject'] = clean_subject
    
    # formataddr مع إيميلات نظيفة تماماً
    msg['From'] = formataddr(("Eslam Automation", sender_email))
    msg['To'] = formataddr(("Blogger Publisher", blogger_email))
    
    msg.add_header('Content-Type', 'text/html', charset='utf-8')
    msg.set_payload(content.encode('utf-8'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            smtp.quit()
        print(f"✅ DONE! Published: {clean_subject}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def generate_article():
    # ... (نفس دالة التوليد السابقة بدون تغيير) ...
    yt_embed = f'''<div style="margin:20px 0;"><iframe src="https://www.youtube.com/embed/videoseries?list=PLN9vn0_krfsFF7mE3MyB_OIRz4XODZbA4" width="100%" height="315" frameborder="0" allowfullscreen></iframe></div>'''
    selected_app = random.choice(APPS)
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    prompt = f"Write a professional blog post in HTML about: {random.choice(GAMING_TOPICS)}. Include PROMOTION_BOX for {selected_app['name']} ({selected_app['url']})."
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}, timeout=120)
        content = response.json()['choices'][0]['message']['content']
        content = content.replace("PROMOTION_BOX", f'<a href="{selected_app["url"]}">{selected_app["name"]}</a>') + yt_embed
        return content
    except: return None

if __name__ == "__main__":
    article = generate_article()
    send_to_blogger(article)
