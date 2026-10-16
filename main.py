import os
import requests
import feedparser

TOKEN = '8883687306:AAF-qJIwQ0Js099LYL9rr_dHu1S-tIunEJ4'
CHAT_ID = '-1004455970098'

RSS_URL = 'https://www.radiofarda.com/api/z_yqteiv-q'

def main():
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        print("خطا: هیچ خبری دریافت نشد.")
        return

    # برداشتن اولین خبر برای تست مستقیم
    latest_entry = feed.entries[0]
    title = latest_entry.title
    link = latest_entry.link

    message = (
        f"🚨 <b>تست ارسال مستقیم:</b>\n\n"
        f"{title}\n\n"
        f"🔗 {link}\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"@TIIME_NEWS | تایم نیوز"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    response = requests.post(url, data=payload)
    
    # چاپ پاسخ دقیق سرور تلگرام در لاگ گیت‌هاب
    print("STATUS CODE:", response.status_code)
    print("RESPONSE BODY:", response.text)

if __name__ == '__main__':
    main()
