import requests
import json
import os
import sys
import base64

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    print("Missing TELEGRAM_TOKEN or GEMINI_API_KEY")
    sys.exit(1)

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

SYSTEM_PROMPT = """РўС‹ вЂ” РґСЂСѓР¶РµР»СЋР±РЅС‹Р№ Р°СЃСЃРёСЃС‚РµРЅС‚ СЃС‚СѓРґРёРё WebStudio. РћС‚РІРµС‡Р°Р№ РЅР° СЂСѓСЃСЃРєРѕРј СЏР·С‹РєРµ РєСЂР°С‚РєРѕ Рё РїРѕ РґРµР»Сѓ.

Р§РµРј Р·Р°РЅРёРјР°РµС‚СЃСЏ WebStudio:
вЂ” РЎРѕР·РґР°РЅРёРµ СЃР°Р№С‚РѕРІ РїРѕРґ РєР»СЋС‡ (Р»РµРЅРґРёРЅРіРё, РјРЅРѕРіРѕСЃС‚СЂР°РЅРёС‡РЅС‹Рµ, РёРЅС‚РµСЂРЅРµС‚-РјР°РіР°Р·РёРЅС‹)
вЂ” Р Р°Р·СЂР°Р±РѕС‚РєР° Telegram-Р±РѕС‚РѕРІ СЃ РёСЃРєСѓСЃСЃС‚РІРµРЅРЅС‹Рј РёРЅС‚РµР»Р»РµРєС‚РѕРј
вЂ” РќР°РїРёСЃР°РЅРёРµ РЅР°СѓС‡РЅРѕ-РїРѕРїСѓР»СЏСЂРЅС‹С… СЃС‚Р°С‚РµР№ РґР»СЏ Telegram-РєР°РЅР°Р»РѕРІ
вЂ” SEO-РѕРїС‚РёРјРёР·Р°С†РёСЏ Рё РїРѕРґРґРµСЂР¶РєР° СЃР°Р№С‚РѕРІ

РљРѕРЅС‚Р°РєС‚С‹:
вЂ” РЎР°Р№С‚: https://uriy-as.org
вЂ” РџРѕС‡С‚Р°: uriy.as59@yandex.com
вЂ” Telegram-РєР°РЅР°Р»: @webstudio_chanel
вЂ” РќР°РїРёСЃР°С‚СЊ Р°РґРјРёРЅСѓ: @uriy_as59

Р•СЃР»Рё РІРѕРїСЂРѕСЃ СЃР»РѕР¶РЅС‹Р№ РёР»Рё С‚СЂРµР±СѓРµС‚ РѕР±СЃСѓР¶РґРµРЅРёСЏ РґРµС‚Р°Р»РµР№ вЂ” РїСЂРµРґР»РѕР¶Рё РєР»РёРµРЅС‚Сѓ РЅР°РїРёСЃР°С‚СЊ РЅР° РїРѕС‡С‚Сѓ РёР»Рё РІ Telegram @uriy_as59."""

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
        "system_instruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
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
                texts = []
                images = []
                for part in parts:
                    if "text" in part:
                        texts.append(part["text"])
                    if "inlineData" in part:
                        images.append(part["inlineData"])
                return texts, images
            return ["Empty response from Gemini"], []
        else:
            return [f"Gemini error: {r.status_code} {r.text[:200]}"], []
    except Exception as e:
        return [f"Gemini request failed: {e}"], []

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

        texts, images = ask_gemini(text)
        reply = "\n".join(texts)
        print(f"Gemini reply: {reply[:200]}")
        if images:
            for img in images:
                send_photo(chat_id, img["data"], img.get("mimeType", "image/png"), reply[:1024])
        if reply.strip():
            send_message(chat_id, reply)

        if str(chat_id) != ADMIN_CHAT_ID:
            username = user.get('username') or user.get('first_name', '?')
            send_message(ADMIN_CHAT_ID, f"рџ’¬ Р’РѕРїСЂРѕСЃ РѕС‚ @{username}:\n\n{text}")

        offset = update_id + 1

    save_offset(offset)
    print(f"Saved offset: {offset}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
