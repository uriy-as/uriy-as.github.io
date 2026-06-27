import json, os, urllib.request, urllib.error, sys

TOKEN = os.environ['TELEGRAM_TOKEN']
ADMIN = os.environ['ADMIN_CHAT_ID']

URLS = [
    'https://uriy-as.github.io/',
    'https://uriy-as.github.io/services.html',
    'https://uriy-as.github.io/en/',
    'https://astap.pythonanywhere.com/',
    'https://astap.pythonanywhere.com/api/chat',
]

def tg_send(text):
    data = json.dumps({'chat_id': ADMIN, 'text': text, 'parse_mode': 'HTML'}).encode()
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{TOKEN}/sendMessage',
        data=data, headers={'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)

failed = []
for url in URLS:
    try:
        r = urllib.request.urlopen(url, timeout=15)
        if r.status != 200:
            failed.append(f'{url} — {r.status}')
    except Exception as e:
        failed.append(f'{url} — {str(e)[:60]}')

if failed:
    tg_send('<b>❌ Сайт не отвечает</b>\n' + '\n'.join(failed))
    sys.exit(1)
