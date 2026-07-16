# ⚠️ ЗАПРЕТ — НЕ ТРОГАТЬ КОМП БЕЗ РАЗРЕШЕНИЯ ⚠️
## НИЧЕГО НЕ МЕНЯТЬ — НИ ФАЙЛОВ, НИ КОДА, НИ КОНФИГОВ — ПОКА НЕ СПРОШУ И НЕ СКАЖУ «ДА»

# Unfinished business — завтра (04.07.2026)

## Что сделано сегодня (02.07.2026)
- ✅ Hreflang фиксы запушены в `uriy-as/site` (commit `05530ff`) и `uriy-as.github.io` (commit `464e589`) через API
- ✅ OG image: `og-image.png` (1200×630px) создан через Pillow, ссылки `.svg` → `.png` заменены во всех HTML, запушено (site `195bcf27`, pages `9ceabd81`)
- ✅ `thanks.html` создан для GBP, запушен (site `5f0026e`, pages `29c3a9`)
- ✅ `leads.json` проверен — 6 записей, все с внутреннего IP 10.0.5.156
- ✅ Telegram-каналы: все 6 в отказ/пустышки
- ✅ **Telegram-бот подключён**: @NevWebStudio_bot, токен установлен, планировщик `TelegramPoster` — ежедневно в 8:10
- ✅ Оптимизация: defer/async/preconnect уже везде, дополнительно нечего делать

## Что сделано сегодня (03.07.2026)
- ✅ **Голосовой ввод/вывод в чат**: кнопка микрофона, SpeechRecognition → текст → отправка, SpeechSynthesis ответа бота. Запушено (site `2bb8fd41ad95`, pages `126c6ff6128b`)
- ✅ `posts.json`: 11 постов в очереди на авто-публикацию

## Что осталось (завтра)

### HIGH — сделать в первую очередь
1. **Google Business Profile** (3 профиля, все "Подтверждено")
   - Заполнить: описание, категория, контакты, часы работы
   - Вставить `thanks.html` как страницу подтверждения
   - Пропустить/закрыть навязывание рекламного бюджета
   - Яндекс.Вебмастер: добавить сайт, sitemap, проверить ошибки

2. **Продвижение**: опубликовать готовые материалы
   - VK: 3 поста из `vk-posts.txt`
   - OLX: объявление из `olx-ad.txt`
   - Каталоги: 2GIS, workspace.ru, fl.ru, Хабр Карьера, vc.ru

### MEDIUM
3. **GitHub Actions авто-деплой** — нужен новый токен с `workflow` scope (у текущего только `public_repo`)

### LOW
4. Проверить leads.json через неделю

## Контекст
- **Сайт на GitHub Pages**: `uriy-as/uriy-as.github.io` (ветка main), домен `uriy-as.org`
- **Исходники в `uriy-as/site`**: этот worktree — копия site
- **Бэкенд**: Flask на PythonAnywhere (`astap.pythonanywhere.com`, token: `365fa83e268c2e01b27bd39cb74ea400862602bc`)
- **Cohere API ключ**: `/home/Astap/mysite/cohere_key.txt`
- **GA Property ID**: `542628161` (не подключён — нет service account key)
- **Yandex.Metrica**: ID `109350815`, установлена на всех страницах
- **Проблема**: git push зависает (credential manager), использовать API GitHub

## Важные файлы
- `.github/scripts/flask_app.py` — бэкенд
- `js/script.js` — фронтенд
- `blog/*.html` (16 RU статей), `en/blog/*.html` (10 EN статей)
- `vk-posts.txt`, `olx-ad.txt`, `channels-for-promo.txt`, `promotion-checklist.md` — промо-материалы
