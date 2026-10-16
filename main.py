import os
import requests
import feedparser

TOKEN = '8883687306:AAF-qJIwQ0Js099LYL9rr_dHu1S-tIunEJ4'
CHAT_ID = '-1004455970098'

# فید اخبار فارسی گوگل با کلیدواژه‌های سیاسی ایران و آمریکا
RSS_URL = 'https://news.google.com/rss/search?q=%D8%A7%DB%8C%D8%B1%D8%A7%D9%86+%D8%A2%D9%85%D8%B1%DB%8C%DA%A9%D8%A7&hl=fa&gl=IR&ceid=IR:fa'

HISTORY_FILE = 'sent_news.txt'

def load_sent_links():
    if not os.path.exists(HISTORY_FILE):
        return set()
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def save_sent_link(link):
    with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
        f.write(link + '\n')

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': False
    }
    requests.post(url, data=payload)

def main():
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        return

    sent_links = load_sent_links()

    # بررسی جدیدترین اخبار و ارسال اولین خبری که قبلاً فرستاده نشده باشد
    for entry in feed.entries:
        link = entry.link
        if link not in sent_links:
            title = entry.title
            
            message = (
                f"🚨 <b>خبر جدید | تحولات سیاسی:</b>\n\n"
                f"{title}\n\n"
                f"🔗 {link}\n\n"
                f"━━━━━━━━━━━━━━━\n"
                f"@TIIME_NEWS | تایم نیوز"
            )

            send_telegram_message(message)
            save_sent_link(link)
            break  # در هر بار اجرا فقط ۱ خبر جدید ارسال می‌شود تا گروه اسپم نشود

if __name__ == '__main__':
    main()
