import os
import smtplib
import requests
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_to_blogger(content):
    sender_email = os.getenv("SENDER_EMAIL").strip()
    sender_password = os.getenv("SENDER_PASSWORD").strip()
    # هنا ضع إيميل بلوجر السري (الموجود في صورة الإعدادات اللي بعتها)
    blogger_email = os.getenv("BLOGGER_EMAIL").strip()

    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else "Gaming Update"

    # استخدام MIMEMultipart لضمان وصول التنسيق كـ HTML حقيقي
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = blogger_email

    # إرفاق المحتوى بتنسيق HTML
    msg.attach(MIMEText(content, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            smtp.quit()
        print(f"✅ تم الإرسال بنجاح إلى بلوجر: {subject}")
    except Exception as e:
        print(f"❌ خطأ: {e}")
