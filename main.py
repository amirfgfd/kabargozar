import os
import requests
import feedparser

TOKEN = '8883687306:AAF-qJIwQ0Js099LYL9rr_dHu1S-tIunEJ4'
CHAT_ID = '-1004455970098'

# استفاده از فید خبری خبرگزاری‌های معتبر فارسی برای پوشش اخبار سیاسی و تحولات
RSS_URL = 'https://www.radiofarda.com/api/z_yqteiv-q'

HISTORY_FILE = 'sent_news.txt'

# کلمات کلیدی برای فیلتر دقیق اخبار سیاسی، نظامی و جنگی
KEYWORDS = ['ایران', 'آمریکا', 'جنگ', 'تحریم', 'نظامی', 'مذاکره', 'موشک', 'سیاسی', 'توافق', 'پدافند', 'حمله']

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
    response = requests.post(url, data=payload)
    print("Telegram Response Status:", response.status_code)
    print("Telegram Response Body:", response.text)

def main():
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        print("خطایی در دریافت اخبار رخ داد یا فید خالی است.")
        return

    sent_links = load_sent_links()

    # بررسی اخبار جدید
    for entry in feed.entries:
        link = entry.link
        title = entry.title
        
        # چک کردن کلمات کلیدی سیاسی/جنگی
        if any(keyword in title for keyword in KEYWORDS):
            if link not in sent_links:
                message = (
                    f"🚨 <b>فوری | اخبار سیاسی و تحولات:</b>\n\n"
                    f"{title}\n\n"
                    f"🔗 {link}\n\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"@TIIME_NEWS | تایم نیوز"
                )

                send_telegram_message(message)
                save_sent_link(link)
                break  # ارسال تنها یک خبر در هر نوبت برای جلوگیری از اسپم

if __name__ == '__main__':
    main()
