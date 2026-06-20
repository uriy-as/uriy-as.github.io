import json, os, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

GH_PAT = os.environ['GH_PAT']
TOKEN = os.environ['TELEGRAM_TOKEN']
ADMIN = os.environ['ADMIN_CHAT_ID']

repo = 'uriy-as/uriy-as.github.io'
headers = {
    'Authorization': f'token {GH_PAT}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'daily-stats/1.0'
}

def gh_api(path):
    req = urllib.request.Request(f'https://api.github.com/repos/{repo}/{path}', headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def tg_send(text):
    data = json.dumps({'chat_id': ADMIN, 'text': text, 'parse_mode': 'HTML'}).encode()
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{TOKEN}/sendMessage',
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)

# GitHub Traffic API
try:
    traffic = gh_api('traffic/views')
except Exception as e:
    tg_send(f'\u274c Daily Stats: error fetching traffic data\n{str(e)}')
    exit(1)

yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%d')
y_views = sum(d['count'] for d in traffic.get('views', []) if d['timestamp'].startswith(yesterday))
y_unique = sum(d['uniques'] for d in traffic.get('views', []) if d['timestamp'].startswith(yesterday))

total_views = traffic.get('count', 0)
total_unique = traffic.get('uniques', 0)

# Try to get referring sites (top 10)
refs = gh_api('traffic/popular/referrers')[:5]
ref_lines = ''
if refs:
    for r in refs:
        ref_lines += f'\n  \u2022 {r["referrer"]} \u2014 {r["count"]}'

# Try to get popular content (top 5)
content = gh_api('traffic/popular/paths')[:5]
content_lines = ''
if content:
    for c in content:
        content_lines += f'\n  \u2022 {c["path"]} \u2014 {c["count"]} views, {c["uniques"]} unique'

# Clones data
try:
    clones = gh_api('traffic/clones')
    total_clones = clones.get('count', 0)
    total_clone_unique = clones.get('uniques', 0)
    y_clones = sum(d['count'] for d in clones.get('clones', []) if d['timestamp'].startswith(yesterday))
    y_clone_unique = sum(d['uniques'] for d in clones.get('clones', []) if d['timestamp'].startswith(yesterday))
except:
    total_clones = total_clone_unique = y_clones = y_clone_unique = 0

lines = []
lines.append(f'\U0001f4ca Stats for {yesterday}')
lines.append('')
lines.append(f'\U0001f441 Views yesterday: {y_views} (unique: {y_unique})')
lines.append(f'\U0001f4c8 Views total (14d): {total_views} (unique: {total_unique})')
if total_clones:
    lines.append(f'\U0001f4be Clones yesterday: {y_clones} (unique: {y_clone_unique})')
    lines.append(f'\U0001f4e6 Clones total (14d): {total_clones} (unique: {total_clone_unique})')
lines.append('')
lines.append(f'\U0001f310 Top referrers:{ref_lines}')
lines.append('')
lines.append(f'\U0001f4cc Top pages:{content_lines}')

tg_send('\n'.join(lines))
