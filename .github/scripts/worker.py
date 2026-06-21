import requests
import json
import os
import sys
import base64
import re
import html
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
GH_TOKEN = os.environ.get("GH_TOKEN")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    print("Missing TELEGRAM_TOKEN or GEMINI_API_KEY")
    sys.exit(1)

if not ADMIN_CHAT_ID:
    print("Missing ADMIN_CHAT_ID")
    sys.exit(1)

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
GH_REPO = "uriy-as/uriy-as.github.io"
GH_HEADERS = {"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
PA_BASE = "https://Astap.pythonanywhere.com"

SYSTEM_PROMPT = """Ты - виртуальный ассистент студии WebStudio. Отвечай на русском языке.

Услуги WebStudio:
- Создание сайтов (визитка, под ключ, интернет-магазин)
- Telegram-боты с интеграцией GPT
- Научные статьи для Telegram-каналов
- SEO-продвижение и доработка сайтов

Контакты:
- Сайт: https://uriy-as.org
- Email: uriy.as59@yandex.com
- Telegram-канал: @webstudio_chanel
- Связаться: @uriy_as59

Если вопрос не по услугам - ответь как обычный ассистент."""

OFFSET_FILE = "offset.txt"

def get_offset():
    try:
        with open(OFFSET_FILE) as f:
            return int(f.read().strip())
    except:
        return 0

def save_offset(offset):
    with open(OFFSET_FILE, "w") as f:
        f.write(str(offset))

def commit_offset():
    if not GH_TOKEN:
        print("No GH_TOKEN, skipping commit")
        return
    import subprocess
    subprocess.run(["git", "config", "user.name", "bot-worker"], capture_output=True)
    subprocess.run(["git", "config", "user.email", "bot@uriy-as.org"], capture_output=True)
    subprocess.run(["git", "add", OFFSET_FILE], capture_output=True)
    r = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
    if r.returncode != 0:
        subprocess.run(["git", "commit", "-m", "Update offset"], capture_output=True)
        remote = f"https://x-access-token:{GH_TOKEN}@github.com/uriy-as/uriy-as.github.io"
        subprocess.run(["git", "push", remote, "HEAD:main"], capture_output=True)

# --- GitHub API helpers ---
def gh_get(path):
    r = requests.get(f"https://api.github.com/repos/{GH_REPO}/contents/{path}", headers=GH_HEADERS, timeout=15)
    if r.status_code == 200:
        data = r.json()
        content = base64.b64decode(data["content"]).decode("utf-8")
        return json.loads(content), data["sha"]
    return None, None

def gh_put(path, content_json, sha=None):
    body = {
        "message": f"Update {path}",
        "content": base64.b64encode(json.dumps(content_json, ensure_ascii=False, indent=2).encode("utf-8")).decode("utf-8")
    }
    if sha:
        body["sha"] = sha
    r = requests.put(f"https://api.github.com/repos/{GH_REPO}/contents/{path}", json=body, headers=GH_HEADERS, timeout=15)
    if r.status_code not in (200, 201):
        print(f"gh_put error: {r.status_code} {r.text[:200]}")

# --- Leads CRM ---
def load_leads():
    leads, _ = gh_get(".github/scripts/leads.json")
    return leads if leads else []

def save_leads(leads):
    _, sha = gh_get(".github/scripts/leads.json")
    gh_put(".github/scripts/leads.json", leads, sha)

def fetch_leads_from_pa():
    try:
        r = requests.get(f"{PA_BASE}/stats", timeout=15)
        if r.status_code != 200:
            print(f"PA stats error: {r.status_code}")
            return []
        text = r.text
        leads = []
        table_match = re.search(r'<h2>[^<]*Заявки с сайта[^<]*</h2>\s*<table>(.*?)</table>', text, re.DOTALL)
        if not table_match:
            print("No leads table found on PA stats page")
            return []
        rows = re.findall(r'<tr>(.*?)</tr>', table_match.group(1), re.DOTALL)
        for row in rows:
            cells = re.findall(r'<td>(.*?)</td>', row, re.DOTALL)
            if len(cells) >= 4:
                date_str = cells[0].strip()
                contact_raw = html.unescape(cells[1].strip())
                msg = html.unescape(cells[2].strip())
                ip = cells[3].strip()
                parts = [p.strip() for p in contact_raw.split("|")]
                name = parts[0] if len(parts) > 0 else ""
                phone = parts[1] if len(parts) > 1 else ""
                email = parts[2] if len(parts) > 2 else ""
                leads.append({
                    "name": name, "phone": phone, "email": email,
                    "message": msg, "ip": ip, "date": date_str
                })
        return leads
    except Exception as e:
        print(f"fetch_leads_from_pa error: {e}")
        return []

def sync_leads():
    existing = load_leads()
    existing_keys = set((l.get("name",""), l.get("phone",""), l.get("message","")[:50]) for l in existing)
    pa_leads = fetch_leads_from_pa()
    new_count = 0
    max_id = max((l.get("id", 0) or 0) for l in existing) if existing else 0
    for pl in pa_leads:
        key = (pl.get("name",""), pl.get("phone",""), pl.get("message","")[:50])
        if key not in existing_keys:
            max_id += 1
            pl["id"] = max_id
            pl["status"] = "new"
            existing.append(pl)
            existing_keys.add(key)
            new_count += 1
    if new_count:
        save_leads(existing)
        print(f"Synced {new_count} new leads from PA")
    else:
        print("No new leads to sync")
    return new_count

def format_lead(lead, index=None):
    prefix = f"#{lead['id']} " if lead.get("id") else (f"{index}. " if index else "")
    status_icon = {"new": "🆕", "working": "🔨", "done": "✅"}.get(lead.get("status", "new"), "🆕")
    name = lead.get("name", "") or "—"
    phone = lead.get("phone", "") or "—"
    email = lead.get("email", "") or "—"
    msg = lead.get("message", "") or "—"
    date = lead.get("date", "")[:19].replace("T", " ")
    contact = " | ".join(filter(None, [name, phone, email]))
    return f"{prefix}{status_icon} {date}\n{contact}\n📝 {msg}"

def cmd_help(chat_id, args):
    send_message(chat_id, (
        "🤖 Команды CRM:\n"
        "/list — список всех заявок\n"
        "/list new — только новые\n"
        "/list working — в работе\n"
        "/list done — готовые\n"
        "/view N — просмотр заявки\n"
        "/work N — взять в работу\n"
        "/done N — отметить готовой\n"
        "/sync — загрузить заявки с сайта\n"
        "/leads — количество заявок\n"
        "/help — эта справка"
    ))

def cmd_list(chat_id, args):
    leads = load_leads()
    if not leads:
        send_message(chat_id, "Заявок нет.")
        return
    status_filter = args[0] if args else None
    filtered = leads
    if status_filter in ("new", "working", "done"):
        filtered = [l for l in leads if l.get("status") == status_filter]
    if not filtered:
        send_message(chat_id, f"Заявок со статусом '{status_filter}' нет.")
        return
    lines = [f"📋 Заявки ({len(filtered)} шт.):"]
    for l in filtered[-10:]:
        sid = l.get("id", "?")
        s = {"new": "🆕", "working": "🔨", "done": "✅"}.get(l.get("status", "new"), "🆕")
        name = l.get("name", "—")
        msg = (l.get("message", "") or "")[:40]
        lines.append(f"#{sid} {s} {name}: {msg}")
    send_message(chat_id, "\n".join(lines))

def cmd_view(chat_id, args):
    if not args:
        send_message(chat_id, "Укажите ID: /view 1")
        return
    try:
        lid = int(args[0])
    except ValueError:
        send_message(chat_id, "ID должен быть числом.")
        return
    leads = load_leads()
    for l in leads:
        if l.get("id") == lid:
            send_message(chat_id, format_lead(l))
            return
    send_message(chat_id, f"Заявка #{lid} не найдена.")

def cmd_status_change(chat_id, args, new_status):
    if not args:
        send_message(chat_id, f"Укажите ID: /{new_status} 1")
        return
    try:
        lid = int(args[0])
    except ValueError:
        send_message(chat_id, "ID должен быть числом.")
        return
    leads = load_leads()
    for l in leads:
        if l.get("id") == lid:
            old = l.get("status", "new")
            l["status"] = new_status
            save_leads(leads)
            send_message(chat_id, f"Заявка #{lid}: {old} → {new_status}")
            return
    send_message(chat_id, f"Заявка #{lid} не найдена.")

def cmd_counts(chat_id, args):
    leads = load_leads()
    n = sum(1 for l in leads if l.get("status") == "new")
    w = sum(1 for l in leads if l.get("status") == "working")
    d = sum(1 for l in leads if l.get("status") == "done")
    send_message(chat_id, f"📊 Заявки: всего {len(leads)}, 🆕 {n}, 🔨 {w}, ✅ {d}")

def cmd_sync(chat_id, args):
    send_message(chat_id, "⏳ Синхронизирую заявки с сайта...")
    n = sync_leads()
    send_message(chat_id, f"✅ Синхронизация завершена. Новых заявок: {n}")

def cmd_lead_add(chat_id, args):
    if len(args) < 1:
        send_message(chat_id, "Добавить: /add Имя | Телефон | Сообщение")
        return
    text = " ".join(args)
    parts = [p.strip() for p in text.split("|")]
    leads = load_leads()
    max_id = max((l.get("id", 0) or 0) for l in leads) if leads else 0
    leads.append({
        "id": max_id + 1,
        "name": parts[0],
        "phone": parts[1] if len(parts) > 1 else "",
        "email": "",
        "message": parts[2] if len(parts) > 2 else parts[0],
        "page": "",
        "ip": "",
        "date": datetime.now().isoformat(),
        "status": "new"
    })
    save_leads(leads)
    send_message(chat_id, f"✅ Заявка #{max_id + 1} добавлена.")

# --- Gemini ---
def ask_gemini(text):
    payload = {
        "contents": [{
            "parts": [{"text": f"{SYSTEM_PROMPT}\n\nВопрос: {text}"}]
        }]
    }
    try:
        r = requests.post(GEMINI_URL, json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                texts = [p["text"] for p in parts if "text" in p]
                images = [p["inlineData"] for p in parts if "inlineData" in p]
                return texts or ["Empty response from Gemini"], images
            return ["Empty response from Gemini"], []
        else:
            return [f"Gemini error: {r.status_code} {r.text[:200]}"], []
    except Exception as e:
        return [f"Gemini request failed: {e}"], []

# --- Telegram ---
def send_message(chat_id, text):
    for chunk in [text[i:i+4000] for i in range(0, len(text), 4000)]:
        try:
            r = requests.post(f"{TELEGRAM_API}/sendMessage", json={
                "chat_id": chat_id,
                "text": chunk
            }, timeout=15)
            if r.status_code != 200:
                print(f"sendMessage error: {r.status_code} {r.text[:200]}")
        except Exception as e:
            print(f"sendMessage failed: {e}")

def send_photo(chat_id, image_data, mime_type, caption=""):
    try:
        img_bytes = base64.b64decode(image_data)
        files = {"photo": ("image." + mime_type.split("/")[-1], img_bytes, mime_type)}
        data = {"chat_id": chat_id, "caption": caption[:1024]}
        r = requests.post(f"{TELEGRAM_API}/sendPhoto", data=data, files=files, timeout=30)
        if r.status_code != 200:
            print(f"sendPhoto error: {r.status_code} {r.text[:200]}")
    except Exception as e:
        print(f"sendPhoto failed: {e}")

# --- Main ---
COMMANDS = {
    "/help": cmd_help,
    "/start": cmd_help,
    "/list": cmd_list,
    "/view": cmd_view,
    "/work": lambda c,a: cmd_status_change(c,a,"working"),
    "/done": lambda c,a: cmd_status_change(c,a,"done"),
    "/leads": cmd_counts,
    "/sync": cmd_sync,
    "/add": cmd_lead_add,
}

print(f"Starting bot worker (ADMIN_CHAT_ID={ADMIN_CHAT_ID})")
offset = get_offset()
print(f"Current offset: {offset}")

try:
    r = requests.get(f"{TELEGRAM_API}/getUpdates", params={
        "offset": offset,
        "timeout": 5
    }, timeout=10)
    if r.status_code != 200:
        print(f"getUpdates error: {r.status_code} {r.text[:300]}")
        sys.exit(1)

    updates = r.json().get("result", [])
    print(f"Got {len(updates)} updates")

    for update in updates:
        update_id = update["update_id"]
        message = update.get("message")
        if not message:
            offset = update_id + 1
            continue

        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        user = message.get("from", {})

        print(f"Update {update_id}: from {user.get('first_name', '?')} (chat={chat_id}): {text[:100]}")

        is_admin = str(chat_id) == ADMIN_CHAT_ID

        if is_admin and text.startswith("/"):
            cmd = text.split()[0].lower()
            args = text.split()[1:]
            handler = COMMANDS.get(cmd)
            if handler:
                handler(chat_id, args)
                offset = update_id + 1
                continue

        texts, images = ask_gemini(text)
        reply = "\n".join(texts)
        print(f"Gemini reply: {reply[:200]}")
        if images:
            for img in images:
                send_photo(chat_id, img["data"], img.get("mimeType", "image/png"), reply[:1024])
        if reply.strip():
            send_message(chat_id, reply)

        if not is_admin:
            username = user.get('username') or user.get('first_name', '?')
            send_message(ADMIN_CHAT_ID, f"Сообщение от @{username}:\n\n{text}")

        offset = update_id + 1

    save_offset(offset)
    print(f"Saved offset: {offset}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)