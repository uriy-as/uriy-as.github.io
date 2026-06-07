import requests
import json
import os
import time
import sys

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    print("Missing TELEGRAM_TOKEN or GEMINI_API_KEY")
    sys.exit(1)

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

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

def ask_gemini(text):
    payload = {
        "contents": [{
            "parts": [{"text": text}]
        }]
    }
    try:
        r = requests.post(GEMINI_URL, json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "No response")
            return "Empty response from Gemini"
        else:
            return f"Gemini error: {r.status_code} {r.text[:200]}"
    except Exception as e:
        return f"Gemini request failed: {e}"

def send_message(chat_id, text):
    try:
        r = requests.post(f"{TELEGRAM_API}/sendMessage", json={
            "chat_id": chat_id,
            "text": text[:4096]
        }, timeout=15)
        if r.status_code != 200:
            print(f"sendMessage error: {r.status_code} {r.text[:200]}")
    except Exception as e:
        print(f"sendMessage failed: {e}")

print(f"Starting bot worker (ADMIN_CHAT_ID={ADMIN_CHAT_ID})")
print(f"Using offset file: {OFFSET_FILE}")

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

        if chat_id == int(ADMIN_CHAT_ID):
            reply = ask_gemini(text)
            print(f"Gemini reply: {reply[:200]}")
            send_message(chat_id, reply)
        else:
            print(f"Ignoring non-admin chat: {chat_id}")

        offset = update_id + 1

    save_offset(offset)
    print(f"Saved offset: {offset}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
