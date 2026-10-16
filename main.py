import os
import requests
import feedparser

TOKEN = '8883687306:AAF-qJIwQ0Js099LYL9rr_dHu1S-tIunEJ4'
# آیدی کانال یا گروه خود را اینجا وارد کنید (مثلاً '@TIIME_NEWS' یا آیدی عددی)
CHAT_ID = '-1004455970098'

# منبع اخبار سیاسی و جنگی فارسی
RSS_URL = 'https://www.radiofarda.com/api/z_yqteiv-q'
HISTORY_FILE = 'sent_news.txt'

KEYWORDS = ['ایران', 'آمریکا', 'جنگ', 'تحریم', 'نظامی', 'مذاکره', 'موشک', 'سیاسی', 'توافق', 'پدافند', 'حمله']

def load_sent_links():
    if not os.path.exists(HISTORY_FILE):
        return set()
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def save_sent_link(link):
    with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
        f.write(link + '\n')

def main():
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        return

    sent_links = load_sent_links()

    for entry in feed.entries:
        link = entry.link
        title = entry.title
        
        if any(keyword in title for keyword in KEYWORDS):
            if link not in sent_links:
                message = (
                    f"🚨 <b>فوری | اخبار سیاسی و تحولات:</b>\n\n"
                    f"{title}\n\n"
                    f"🔗 {link}\n\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"@TIIME_NEWS | تایم نیوز"
                )

                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                response = requests.post(url, data={
                    'chat_id': CHAT_ID,
                    'text': message,
                    'parse_mode': 'HTML'
                })
                print("Telegram Response:", response.text)
                
                save_sent_link(link)
                break

if __name__ == '__main__':
    main()
