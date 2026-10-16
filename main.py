import os
import requests
import feedparser

TOKEN = '8883687306:AAF-qJIwQ0Js099LYL9rr_dHu1S-tIunEJ4'
CHAT_ID = '-1004455970098'

# استفاده از خبرگزاری ۱۰۰٪ فارسی (یورونیوز فارسی)
RSS_URL = 'https://parsi.euronews.com/api/1.0/rss'

HISTORY_FILE = 'sent_news.txt'

# کلمات کلیدی برای پیدا کردن اخبار مهم سیاسی و جنگی
KEYWORDS = ['ایران', 'آمریکا', 'جنگ', 'اسرائیل', 'حمله', 'نظامی', 'تحریم', 'خاورمیانه', 'موشک', 'پدافند']

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

    # بررسی اخبار
    for entry in feed.entries:
        link = entry.link
        title = entry.title
        
        # بررسی اینکه آیا خبر جدید است و کلمات کلیدی سیاسی/جنگی را دارد یا نه
        if any(keyword in title for keyword in KEYWORDS):
            if link not in sent_links:
                message = (
                    f"🚨 <b>خبر جدید | تحولات سیاسی:</b>\n\n"
                    f"{title}\n\n"
                    f"🔗 {link}\n\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"@TIIME_NEWS | تایم نیوز"
                )

                send_telegram_message(message)
                save_sent_link(link)
                break  # ارسال فقط یک خبر در هر ۲۰ دقیقه

if __name__ == '__main__':
    main()
