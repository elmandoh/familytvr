import os
import smtplib
import requests
import random
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# --- إعدادات وتصنيفات ---
APPS = [
    {"name": "Luxury Estate Guide", "url": "https://play.google.com/store/apps/details?id=com.eslam.luxuryestate"},
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"}
]

GAMING_TOPICS = [
    "Evolution of Mobile Game Engines",
    "Retro Gaming: Uncovering Hidden Secrets",
    "The Future of AI in Game Development",
    "Top 10 High-Performance Android Games"
]

def clean_input(data):
    """تنظيف أي رموز مخفية أو مسافات زائدة من الإعدادات"""
    if not data: return ""
    return re.sub(r'[^\x00-\x7f]', '', data).strip()

def send_to_blogger(content):
    """إرسال المقال لمدونة بلوجر عبر الإيميل"""
    sender_email = clean_input(os.getenv("SENDER_EMAIL"))
    sender_password = os.getenv("SENDER_PASSWORD")
    blogger_email = clean_input(os.getenv("BLOGGER_EMAIL")) # تأكد أنه إيميل بلوجر السري

    # استخراج العنوان من وسم H1
    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"Tech Update {random.randint(100,999)}"
    clean_subject = clean_input(subject)

    # إنشاء الرسالة بتنسيق Multipart لضمان ظهور الـ HTML
    msg = MIMEMultipart()
    msg['Subject'] = clean_subject
    msg['From'] = formataddr(("eslammosde@gmail.com", sender_email))
    msg['To'] = blogger_email

    # إرفاق المحتوى كـ HTML
    msg.attach(MIMEText(content, 'html', 'utf-8'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            smtp.quit()
        print(f"✅ تم النشر بنجاح: {clean_subject}")
    except Exception as e:
        print(f"❌ فشل النشر: {str(e)}")

def generate_article():
    """توليد المقال باستخدام Groq API"""
    api_key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    selected_app = random.choice(APPS)
    topic = random.choice(GAMING_TOPICS)
    
    prompt = f"""Write a professional blog post in HTML about '{topic}'. 
    Include an H1 title and a recommendation for the app '{selected_app['name']}' with link: {selected_app['url']}."""

    try:
        response = requests.post(url, 
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]},
            timeout=60
        )
        return response.json()['choices'][0]['message']['content']
    except:
        return None

if __name__ == "__main__":
    article = generate_article()
    if article:
        send_to_blogger(article)
