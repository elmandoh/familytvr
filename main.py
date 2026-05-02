import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage
from email.utils import formataddr

def clean_email_string(email_str):
    if not email_str: return ""
    return re.sub(r'[^\x00-\x7f]', '', email_str).strip()

def clean_html_for_blogger(content):
    """تنظيف المحتوى لضمان قبوله داخل جسم المقالة في بلوجر"""
    # إزالة أي وسوم زائدة قد يضيفها الذكاء الاصطناعي وتسبب رفض بلوجر للنشر التلقائي
    content = re.sub(r'<!DOCTYPE.*?>', '', content, flags=re.DOTALL)
    content = re.sub(r'<html.*?>|</html>', '', content, flags=re.DOTALL)
    content = re.sub(r'<body.*?>|</body>', '', content, flags=re.DOTALL)
    content = re.sub(r'<head.*?>.*?</head>', '', content, flags=re.DOTALL)
    return content.strip()

def send_to_blogger(content):
    if not content: return
    
    # تنظيف المحتوى قبل الإرسال
    content = clean_html_for_blogger(content)
    
    sender_email = clean_email_string(os.getenv("SENDER_EMAIL"))
    sender_password = os.getenv("SENDER_PASSWORD").strip()
    blogger_email = clean_email_string(os.getenv("BLOGGER_EMAIL"))
    
    # استخراج العنوان
    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"Gaming Secret {random.randint(100,999)}"
    clean_subject = re.sub(r'[^\x00-\x7f]', '', subject).strip()

    msg = EmailMessage()
    msg['Subject'] = clean_subject
    msg['From'] = formataddr(("Eslam Bot", sender_email))
    msg['To'] = formataddr(("Blogger", blogger_email))
    
    # إرسال المحتوى كـ HTML نظيف
    msg.set_content(content, subtype='html', charset='utf-8')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            smtp.quit()
        print(f"✅ تم الإرسال بنجاح: {clean_subject}")
    except Exception as e:
        print(f"❌ فشل: {str(e)}")

def generate_article():
    # دالة التوليد (Groq API)
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"}
    topic = "The Future of Gaming Automation"
    prompt = f"Write a blog post about {topic} in HTML. Use H1 for title."
    
    try:
        res = requests.post(url, headers=headers, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]})
        return res.json()['choices'][0]['message']['content']
    except: return None

if __name__ == "__main__":
    article = generate_article()
    send_to_blogger(article)
