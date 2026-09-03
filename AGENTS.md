# ⚠️ ЗАПРЕТ — НЕ ТРОГАТЬ КОМП БЕЗ РАЗРЕШЕНИЯ ⚠️
## НИЧЕГО НЕ МЕНЯТЬ — НИ ФАЙЛОВ, НИ КОДА, НИ КОНФИГОВ — ПОКА НЕ СПРОШУ И НЕ СКАЖУ «ДА»

## 🔔 НАПОМИНАНИЕ ПРИ ВКЛЮЧЕНИИ КОМПА (21.07.2026)

### Что сделано сегодня (21.07.2026)
- ✅ Полный аудит сайта: техсостояние, индексация, трафик, SEO-ошибки, ссылочный профиль
- ✅ Исправлены 3 проблемы:
  1. `en/index.html` — `<title>` и `og:title` переведены на английский (были русские)
  2. `sitemap.xml` — privacy.html удалён из карты сайта (противоречие с noindex)
  3. Секция счетчиков («0 проектов», «0 клиентов» и т.д.) удалена с главной (RU + EN)

## Контекст (актуально на 18.07.2026)

- **Сайт**: GitHub Pages (`uriy-as/uriy-as.github.io`, ветка main), домен `uriy-as.org`
- **Исходники**: `uriy-as/site` — рабочая папка `C:\Users\Admin\Documents\site` (основная, синхронизирована с remote). НЕ вести план в worktree `opencode/shiny-cactus` — это устаревший дубликат
- **Бэкенд**: Flask на PythonAnywhere (`astap.pythonanywhere.com`)
- **Статистика**: `uriy-as.org/stats.html` (реальное время, авто-ретрай если сервер спит)
- **Индексация**: Все 30 URL в Google (17 RU + 13 EN статей)
- **Yandex.Metrica**: ID `109350815`, установлена на всех страницах
- **Auto-deploy**: `deploy.yml` — работает, через `GH_PAT` (`repo` scope, без `workflow`)
- **GH_PAT**: `<СЕКРЕТ — GH_PAT, хранится вне репо>`. ⚠️ Реальный PAT из этого файла убран: GitHub Secret Scanning блокирует push с секретами. При необходимости вставить вручную локально, НЕ коммитить
- **Plisio Secret Key**: `<СЕКРЕТ — Plisio, хранится вне репо>`. ⚠️ Убран из файла (см. GH_PAT выше)
- **PA загрузка файлов**: PA API v0 через GitHub Actions (`deploy-flask.yml`). Ключевой момент: эндпоинт `/api/v0/user/{user}/files/path/home/{user}/{domain}/file.py` требует `X-CSRFToken` + cookie-based auth (логин через веб-форму)
- **git push**: не работает локально — только через API GitHub
- **Проблема**: Украина блокирует Google, VK, Yandex — нужен VPN

## Важные файлы
- `vk-posts.txt` — 3 готовых поста для VK
- `olx-ad.txt`, `olx-ad-short.txt` — объявления для OLX
- `C:\Users\Admin\AppData\Local\Temp\opencode\vc_ru_article.txt` — статья для vc.ru
- `channels-for-promo.txt` — каналы для промо
- `promotion-checklist.md` — чеклист раскрутки
- `.github/scripts/flask_app.py` — бэкенд (PythonAnywhere)
- `.github/scripts/daily-stats.py` — ежедневная статистика (генерирует stats.html и пушит в pages)

## Что сделано сегодня (17.07.2026)
- ✅ Секция stats (счётчики) восстановлена на главной (RU + EN) + CSS + JS + i18n
- ✅ `stats.html` — статическая страница с реальными данными через `fetch(astap.pythonanywhere.com/api/stats)`, авто-ретрай при сне сервера
- ✅ `/api/stats` — JSON-эндпоинт на Flask (отдаёт посещения, устройства, страницы, заявки)
- ✅ `daily-stats.py` — сам пушит `stats.html` в pages-репозиторий (через Contents API)
- ✅ Ссылка «Статистика» в футере (RU + EN)
- ✅ Все статьи проиндексированы Google (30/30 URL)
- ✅ Посещения: 200 всего, 91 уникальный IP, 10 дней сбора
- ✅ `deploy.yml` — concurrency guard **не применён** (токен без `workflow` scope)
- ✅ `daily-stats.yml` — commit-шаг **не добавлен** (токен без `workflow` scope)

## Что сделано сегодня (18.07.2026)
- ✅ GSC: 19 страниц проиндексировано, 14 не проиндексировано (из них 1 — privacy.html с noindex)
- ✅ GSC: ручной запрос индексации для 12 из 13 URL (квота исчерпана)
- ✅ На главную (RU + EN) добавлен блок «Полезные статьи» с 4 прямыми ссылками на статьи блога
- ✅ Посещения: 28 визитов сегодня, 200 всего, 113 уникальных IP

## Что сделано сегодня (23.07.2026)
- ✅ Schema.org: BreadcrumbList добавлен на 30 страниц (16 RU + 10 EN блогов, services, articles)
- ✅ Medium: 3 статьи опубликованы:
  1. `https://medium.com/@uriy.as59/ai-bots-in-2026-what-they-can-actually-do-for-your-business-and-whats-still-hype-1b24f5ea5949` (20.07)
  2. `https://medium.com/@uriy.as59/website-vs-telegram-bot-which-one-does-your-business-actually-need-in-2026-5b3b5861f959` (23.07)
  3. `https://medium.com/@uriy.as59/how-i-built-a-telegram-bot-with-ai-for-200-and-you-can-too-a0e48fdd02b7` (30.07)
- ⚠️ Medium профиль (@uriy.as59): 0 подписчиков, нет bio/аватара. Нужно заполнить в браузере
- ✅ Dev.to: 2 статьи опубликованы:
  1. `https://dev.to/astap/telegram-bot-vs-website-which-one-does-your-business-actually-need-in-2026-2cl5` (11.08)
  2. `https://dev.to/astap/how-i-built-a-complete-web-studio-site-in-5-days-with-ai-chat-blog-and-analytics-56c2` (13.08)
- ✅ Organization schema: `medium.com/@uriy.as59` добавлен в sameAs на всех 8 страницах
- ✅ GSC: 10 EN-страниц + 2 RU-страницы подтверждены в индексе
- ✅ Посещения: 200 всего, 109 уникальных IP, 13 дней сбора, 7 лидов
- ⏳ Каталоги: требуют браузер/аккаунт — невозможно через CLI
- ⏳ Google Business Profile: инструкция дана, пользователь не создал

## 🔔 НАПОМИНАНИЕ НА ЗАВТРА (24.07.2026)
- Проверить посещения через API: `https://astap.pythonanywhere.com/api/stats`
- Сделать аналитику: трафик, устройства, популярные страницы, конверсия
- Сравнить с вчерашними данными (200 всего, 109 IP, 7 лидов)
- GSC: проверить новые индексации после BreadcrumbList

## Что сделано сегодня (21.08.2026)
- ✅ Полный аудит сайта: 17 проблем (2 Critical, 4 High, 6 Medium, 5 Low)
- ✅ Крипто-кнопки удалены из services.html (RU + EN)
- ✅ Chat race condition исправлен — mutex `pending`, input блокировка, reference-based typingEl
- ✅ Flask 404 handler: `is_bot()` проверка — боты/сканеры не шлют уведомления в Telegram
- ✅ Модалка формы: `modal--open` только после ответа сервера, `form.reset()` только при `r.ok`
- ✅ Валидация формы: имя/сообщение обязательны, email regex
- ✅ Git: коммит `a1d4b42` (rebase + conflict resolution в stats.html)
- ✅ **flask_app.py задеплоен на PA** через GitHub Actions (workflow `deploy-flask.yml`)
  - API v0: POST `/api/v0/user/{user}/files/path/home/{user}/{domain}/file.py`
  - Cookie-based auth + `X-CSRFToken` заголовок
  - Сервер перезагружен, чат и tracker работают
- ✅ **Проблема PA из Украины**: провайдер блокирует TCP 443 на AWS IP. DNS/ping OK, HTTPS timeout. Решение: VPN (Cloudflare WARP) или деплой через GitHub Actions

## Что нужно сделать завтра (22.08.2026)
- Крипто-кошелёк: попробовать Binance (единственная крупная биржа, может работать и в Украине, и в России)
- Продолжить публикации: Habr, vc.ru, каталоги (Google Business Profile, 2GIS, Clutch)
- Перепроверить индексацию `skolko-stoit-podderzhka-sayta.html`
- При необходимости — подключить Plisio крипто-кнопки обратно (backend эндпоинты уже на сервере)

## Что сделано сегодня (23.08.2026)
### Dev.to публикации
- ✅ **Статья 3**: "Shared vs VPS vs Cloud Hosting" → `https://dev.to/astap/shared-vs-vps-vs-cloud-hosting-which-do-you-actually-need-2hn8` (ID: 4469438)
- ✅ **Статья 4**: "10 Website Mistakes That Are Killing Your Conversion Rate" → `https://dev.to/astap/10-website-mistakes-that-are-killing-your-conversion-rate-and-how-to-fix-each-one-4gpc` (ID: 4469439)
- ✅ Dev.to статьи добавлены на сайт — секция "Публикации на Dev.to" в `en/articles.html` и `articles.html` (RU), по 4 карточки в каждом
- ✅ Скрипт `.github/scripts/devto_post.py` создан — авто-публикация devto-*.md через API

### Medium публикации
- ✅ **Статья 4**: "How Much Does a Website Cost in 2026?" → `https://medium.com/@uriy.as59/how-much-does-a-website-cost-in-2026-real-prices-no-bs-4ef58b70cebe`
- ✅ **Статья 5**: "Website Maintenance: The Cost Nobody Talks About" → `https://medium.com/@uriy.as59/website-maintenance-the-cost-nobody-talks-about-until-its-too-late-fde93a290a4b`
- ✅ Cover images: `medium-cover-website-cost.png` (56KB), `medium-cover-website-maintenance.png` (101KB)

### Метрики
- ✅ **Medium**: 5 статей, 0 подписчиков, 1 просмотр (только "AI Bots"). Профиль требует доработки: аватар, bio, подписи
- ✅ **Dev.to**: 4 статьи, 2 комментария на "Site in 5 Days", 0 реакций на новых
- ✅ **Индексация**: 53 из 58 страниц проиндексированы в Google. 5 не проиндексированы — это noindex (404, stats, thanks, privacy). Ошибки переадресации — Google видит http://www/www. варианты URL (редиректы работают корректно)

### Не закоммичено (нужно сделать)
- ⏳ `articles.html` + `en/articles.html` — добавлены Dev.to publications секции
- ⏳ `.github/scripts/devto_post.py` — новый скрипт
- ⏳ `.github/workflows/devto.yml` — workflow для Dev.to НЕ создан (скрипт есть, workflow нет)

## Что сделано сегодня (24.08.2026)
- ✅ Закоммичено и запушено: articles.html RU+EN (Dev.to секции), devto_post.py, статьи, обложки
  - Коммиты: `32b4a04`, `9a1ea86`, `99ac6ce`
- ✅ `.github/workflows/devto.yml` создан — cron 6:30 UTC, публикует devto-*.md через API
- ✅ Секрет `DEVTO_API_KEY` добавлен в GitHub (`<СЕКРЕТ — DEVTO_API_KEY, хранится вне репо>`)
- ✅ Dev.to статья 5: "How to Order a Telegram Bot" → `https://dev.to/astap/how-to-order-a-telegram-bot-step-by-step-guide-2026-4g06` (ID: 4477074)
- ✅ Статья готова для Medium: `medium-how-to-order-telegram-bot.md` (нужно опубликовать вручную)
- ✅ Проверка комментариев: 1 комментарий на "Site in 5 Days" от @vssdigital (положительный). Dev.to API не поддерживает публикацию комментариев — ответить в браузере
- ✅ Состояние devto_state.json обновлено

### Посещения (24.08)
- 83 визитов всего, 26 уникальных IP, 6 лидов, 18 дней сбора
- Сегодня: 2 визита

## Что сделать завтра (25.08.2026)
- Опубликовать статью "How to Order a Telegram Bot" на Medium (скопировать из `medium-how-to-order-telegram-bot.md`)
- Ответить @vssdigital на Dev.to (в браузере)
- Расширить публикации: Habr, vc.ru, каталоги (Google Business Profile, 2GIS, Clutch)
- Крипто-кошелёк: попробовать Binance

## Что сделано сегодня (28.08.2026)
### Dev.to публикации
- ✅ **Dev.to статья 6**: "How Telegram Bots Automate Sales: Real Funnel Setup Guide" → `https://dev.to/astap/how-telegram-bots-automate-sales-real-funnel-setup-guide-hf4` (ID: 4514701)
  - Файл `devto-telegram-bot-sales-automation.md` (canonical → `/en/blog/telegram-bot-sales-automation.html`)
  - Опубликовано через API-диспатч `devto.yml` (run 33190024133 success)
- ⏳ **НЕ добавлена карточка** статьи Dev.to #6 в `articles.html` (RU) + `en/articles.html` — нужно сделать завтра
- ВАЖНО: remote теперь впереди локального (коммиты workflow) — при push обязательно `git pull --rebase`. После диспатча devto.yml создаётся коммит "Update Dev.to post state" (статья `devto-telegram-bot-sales-automation.md` уже в `devto_state.json`)

### Medium автоматизация — РЕЗУЛЬТАТ ИССЛЕДОВАНИЯ
- ❌ **Автоматизировать Medium невозможно** (проверено глубоко):
  - Integration Token недоступен (Medium не выдаёт новым аккаунтам ≈ с 2023-2025, у @uriy.as59 в настройках нет секции "Integration tokens")
  - API `api.medium.com/v1/me` требует Bearer-токен, которого нет
  - GraphQL `medium.com/_/graphql` через sid-cookie → Cloudflare (403 для не-браузеров), а в браузере sid не залипает для `/new-story`
  - Playwright + CDP + залогиненная Opera: `/me/stories` видит вход, но `/new-story`/`/p/new` редиректит на signin (Google OAuth повторяет подтверждение по кругу)
  - **Вывод: Medium публикует ТОЛЬКО вручную копипастом** (~3 мин/статья) из пакетов `medium-package-*.md`
- ✅ Готов пакет **Medium #7**: `medium-package-7-sales-bot.md` (TITLE/TAGS/CANONICAL/CONTENT 5000 знаков) + обложка `images/medium-cover-telegram-bot-guide.png` (29KB)
- ✅ Готово `medium-profile-guide.md`: bio + список публикаций (Better Programming / Towards Dev / Plain English / Startup Stash / The Startup) + шаги по оформлению профиля
- ✅ Сентябрьский график Medium: 1/нед — #7 Sales Bot (готов), Hosting, 10 Website Mistakes, Website Cost; лучшее время вт/чт 14–17 UTC
- ✅ Техника CDP: Opera запускается `opera.exe --remote-debugging-port=9221 --user-data-dir=...`, Python + playwright (v1.62, chromium каталога ms-playwright/chromium-1234) подключается `connect_over_cdp`. Полезные скрипты остались в `.github/scripts/` (medium_publish.py, medium_post_api.py — для будущих попыток; дебаг-скрипты medium_*.py можно удалить)
- Отладочная Opera (порт 9221) закрыта в конце дня

### Посещения
- 28.08: 0 визитов. Всего: 104 хитов (Raw), 28 уникальных IP, 19 дней, 59 bot-хитов (16 IP), последние визиты 26.08 (тесты)
- Счётчик визитов переделан: `count_sessions` в flask_app.py — сессия = IP + таймаут 30 мин (открыл+закрыл сайт = 1 визит), задеплоено на PA через `deploy-flask.yml` (run 32997255394). В API/stats.html теперь лейбл «Всего хитов»
- Google считает 53/58 страниц индексированными; `site:` оператор показывает только выборку — для точности использовать GSC

## Что нужно сделать завтра (29.08.2026)
1. Добавить карточку **Dev.to #6** (Telegram Bots Automate Sales → `https://dev.to/astap/how-telegram-bots-automate-sales-real-funnel-setup-guide-hf4`) в `articles.html` (RU) + `en/articles.html`
2. Опубликовать **Medium #7** вручную по пакету `medium-package-7-sales-bot.md` (браузер: Write → вставка → обложка → теги Telegram/Bots/Sales/Automation → canonical `https://uriy-as.org/en/blog/telegram-bot-sales-automation.html` → Publish); после публикации добавить карточку на сайт
3. Medium-профиль: аватар, bio (готово в medium-profile-guide.md), подача в публикации
4. Проверить комментарий/реакции Dev.to #6
5. Продолжить: Habr, vc.ru, каталоги (Google Business Profile, 2GIS, Clutch)
6. Крипто-кошелёк: попробовать Binance
7. Видеоагент (продукт): продолжить разработку/продвижение

## Что сделано сегодня (30.08.2026)
- ✅ **Диагностика сайта** (полная): 55 URL из sitemap → все 200 OK; 59 внутр. путей (714 ссылок) → битых нет; robots.txt корректный; редиректы http/www → https 301 OK; SSL+HSTS валидный; canonical/title/h1/description/lang OK; Yandex.Metrica (109350815) на всех страницах; внешние ссылки (Dev.to/Medium) живые
- ✅ **Посещения**: вчера (29.08) 2 реальных визита (`/` 23:02 и `/blog/kak-zakazat-telegram-bota.html` 17:35); сегодня 0; всего 106 хитов, 30 IP, 6 лидов, 19 дней
- ✅ **Карточка Dev.to #6** (Sales Funnel) добавлена в `articles.html` + `en/articles.html` → коммит `9ede636` → запушен
- ✅ **Medium #7 опубликован ТАБОЙ вручную**: "How Telegram Bots Automate Sales: Real Funnel Setup Guide" → `https://medium.com/@uriy.as59/how-telegram-bots-automate-sales-real-funnel-setup-guide-f4d1ccb8784d` (4 min, #telegram #bots #sales #automation)
- ✅ Карточка Medium #7 добавлена в `articles.html` + `en/articles.html` → коммит `651c9eb` → запушен
- ✅ **Dev.to статы (API, `devto-*.md` через api-key)**: всего 143 просмотра, 3 комментария, 0 реакций. Топ: 10 Website Mistakes (52), Site in 5 Days (45), Bot vs Website (42), Hosting (4), How to Order (0), Sales Funnel (0). Новые статьи ещё без трафика
- ✅ **Medium статы (дашборд, вставил пользователь)**: всего 2 просмотра, 1 чтение (на "AI Bots in 2026"), 0 подписчиков, 0 сабов. Follower-first алгоритм: новичок без подписчиков = ноль раздачи
- ℹ️ Вердикт: **Dev.to отдаёт — Medium нет**. Ресурсы на Dev.to; на Medium только **подача в публикации** (Better Programming, Towards Dev, Plain English, Startup Stash, The Startup) — единственный путь к аудитории

## Что сделано сегодня (31.08.2026)
- ✅ **Dev.to #7 опубликована**: "How Much Does a Website Actually Cost in 2026?" → `https://dev.to/astap/how-much-does-a-website-actually-cost-in-2026-real-numbers-no-agency-fluff-3ha0` (id 4539128)
  - Файл `devto-website-cost.md` (canonical → `/en/blog/how-much-does-website-cost.html`)
  - Опубликовано локально через `devto_post.py` (скрипт работает — `requests` OK; `curl` из PowerShell даёт 403 на API — возвращать ниже), `DEVTO_API_KEY` в env
- ✅ Карточка Dev.to #7 добавлена в `articles.html` (RU) + `en/articles.html` (EN) → коммит `43f9a36` → запушен
- ✅ `devto_state.json` обновлён (`devto-website-cost.md` добавлен)
- ✅ **vc.ru заблокирован из Украины**: DNS `vc.ru` → "Non-existent domain" (резолвер 193.41.60.1), даже Google DNS 8.8.8.8 не отдаёт `api.dev.to`... но важное: `dev.to` и `https://dev.to/api/*` работают (API хостится на `dev.to/api`, не `api.dev.to`). Опера с CDP-портом 9221 открыта → JWT не перехвачен (vc.ru недоступен) → Opera закрыта
- ✅ **Сетевой статус 31.08**: без VPN сегодня доступны = dev.to/dev.to-api, GitHub, Google; НЕ доступны = vc.ru (DNS-блок), api.dev.to (поддомен не резолвится — использовать `dev.to/api`), Medium (403 без браузера)
- ✅ Отладочные скрипты Medium (`medium_debug*.py`, `medium_*.py` из цепочки CDP) удалены из worktree; оставлены рабочие: `devto_post.py`, `vcru.py`, `vcru_get_token.py`
- ℹ️ `devto_post.py` на старых `devto-*.md` (10 mistakes, hosting) давал 422 — они уже опубликованы ранее, но их filename НЕ в `devto_state.json`. Скрипту нужна защита: помечать 422 как "уже опубликовано" вместо ошибки

## Что сделано сегодня (01.09.2026)
- ✅ **Dev.to #8 опубликована**: "How Content Marketing Brings Clients from Telegram (Without Ads)" → `https://dev.to/astap/how-content-marketing-brings-clients-from-telegram-without-ads-2o84`
  - Файл `devto-content-marketing-telegram.md` (canonical → `/en/blog/content-marketing-telegram-clients.html`)
  - Опубликовано через `devto_post.py`; карточка добавлена в `articles.html` (RU) + `en/articles.html` (EN) → коммит `2c59ef2` → запушен
- ✅ **Статы Dev.to (API `/articles/me/all` с api-key — этот эндпоинт отдаёт `page_views_count` автору)**: 10 Mistakes 52, Site in 5 Days 45, Bot vs Website 42, Hosting 4, How to Order 0, Sales Funnel 0, Website Cost (#7) 0
  - **Тренд: новые статьи дают 0 просмотров** (последние 4-5 вышли в ноль). Трафик был только у первых 3. Возможно алгоритм разгоняет ранние статьи / аккаунт остыл
  - `page_views_count` НЕ отдаётся в API по `articles?username=` и по `articles/{id}` — только через `articles/me/all` с api-key
- ✅ **Готов пост для vc.ru**: `vcru-sales-bot-post.md` (копипаст для ручной публикации, тема «воронка продаж в Telegram-боте») → коммит `82101fa` → запушен
- ✅ **vc.ru статус**: `vc.ru` DNS-заблокирован (резолвер 193.41.60.1), но IP `185.65.149.135` → фронт открывается через `curl --resolve`. **`api.vc.ru` (158.160.209.7) заблокирован на уровне IP** (таймаут даже с `--resolve`) → **автопубликация через `vcru.py` в этой сети невозможна**. vc.ru = только ручная публикация через веб с VPN (как Medium/Habr). Профиль `vc.ru/id6095617`, авторизация через экосистему Osnova/DTF (`dtf.ru/id3531853`), раздела «Токены доступа» нет
- ✅ Habr-черновик `habr-sales-bot-draft.md` и vc.ru-инструменты (`.github/scripts/vcru.py`, `vcru_get_token.py`) закоммичены в репо (коммит `82101fa`)
- ✅ Посещения сайта (01.09 06:29): 108 хитов, 32 IP, 6 лидов, 22 дня; сегодня 1 визит на `/`

## Что сделать дальше (02.09.2026) — ЕЖЕДНЕВНО
1. **Ежедневная проверка статов**: Dev.to (`/articles/me/all` с api-key → `page_views_count`) + Medium (дашборд вставить вручную). Следить за #7 Website Cost и #8 Content Marketing Telegram — если дадут трафик, продолжать формат «Mistakes»; индексация Dev.to 7-14 дней, рано судить
2. **Печать статей**: Medium (#8 контент-маркетинг = есть `medium-*` пакеты; публиковать вручную копипастом), vc.ru — по `vcru-sales-bot-post.md`, Habr — по `habr-sales-bot-draft.md`
3. **Крипто-кошелёк (Binance)** и видеоагент (продукт)
4. **Проверка сайта на болезни** — минимальный набор: главные страницы 200, pixel+API живые, sitemap без 5xx
5. Каталоги: Google Business Profile, 2GIS, Clutch — по `promotion-checklist.md`; Medium подача в публикации (аватар/bio по `medium-profile-guide.md`)

## Сделано сегодня (02.09.2026)
- ✅ **Проверка сайта — болестей нет**: 55 URL sitemap → все 200 (1 временный 503 повторился = 200); 67 внутренних путей → 0 битых; http/www→https 301; SSL Let's Encrypt 57 дней; HSTS; Metrica+title+canonical на всех 55; бэкенд `/api/stats` 200 (0.7s) / без ключа 403 / `/pixel` 200; внешние dev.to/#8 #7 + t.me 200
- ✅ **Посещения (02.09)**: 109 хитов, 33 IP, 6 лидов, 23 дня; сегодня 1 визит `/articles.html` 09:33
- ✅ **Dev.to статы (02.09)**: без изменений — 10 Mistakes 52, Site in 5 Days 45 (3 комм), Bot vs Website 42, Hosting 4, остальные (How to Order, Sales Funnel, Website Cost #7, Content Marketing #8) 0
- ✅ **Medium #8 опубликован**: "How Content Marketing Brings Clients from Telegram (Without Ads)" → `https://medium.com/@uriy.as59/how-content-marketing-brings-clients-from-telegram-without-ads-2238b68c292f` (4 min, Sep 2). Пакет `medium-package-8-content-marketing.md` + cover `images/medium-cover-content-marketing.png` (1200x630). **Карточка добавлена** RU+EN (`articles.html`, `en/articles.html`) → коммит `09e447d`; `medium_last.json` обновлён
- ✅ **Medium статы (02.09, дашборд)**: 8 статей; cumulatively 0 views/reads кроме How-to-Order (1/1) и AI Bots (0/1). **Follower-first: 0 подписчиков = почти ноль раздачи. Ресурсы на Dev.to, Medium — только подача в публикации**
- ⏳ **vc.ru**: текст разделён на **22 блока** (файл `vcru-sales-bot-post.md`) → коммит `f6fa348`. **Пользователь не смог вставить: «слишком много текста в одном блоке» + подзаголовки/текст сливаются при вставке. Порядок: вставлять ПО ОДНОМУ блоку, Ctrl+Shift+V, вручную ставить H2/списки. Пользователь продолжит завтра**
- ⏳ **Worktree (`opencode/shiny-cactus`) НЕ синхронизирован**: 123 коммита расхождение с remote, куча незакоммиченных посторонних правок (articles.html, blog/*, en/*, sitemap.xml, новые файлы). AGENTS.md-коммит `4c775ec` есть локально, но `git pull --rebase` блокируется незакоммиченными файлами. **По согласованию — оставлено как есть, разобраться ЗАВТРА** (провидерить чужие изменения, решить коммитить/стэшить/отдельной веткой). ОСНОВНАЯ работа идёт в `C:\Users\Admin\Documents\site` (там чисто, коммиты `09e447d`, `f6fa348` запушены)

## Проверка сайта (01.09) — БОЛЕЗНЕЙ НЕТ
- ✅ 55 URL sitemap → все 200 (один 503 был транзитным, повторить = 200)
- ✅ 67 внутренних путей → битых 0; http/www→https 301; https://www → 301
- ✅ SSL Let's Encrypt валиден, 57 дней осталось, SAN uriy-as.org + www
- ✅ HSTS max-age присутствует
- ✅ Metrica (109350815) на всех 55; title + canonical на всех 55
- ✅ Бэкенд PA: `/api/stats` 200 (0.7s, с ключом), без ключа 403, `/pixel` 200
- ✅ Внешние ссылки: dev.to #8/#7 200, t.me/uriy_as59 200

## TelegramPoster
- График: пн, ср, пт, сб в 8:10
- Состояние: `C:\Users\Admin\.telegram-poster-state.json`
- Опубликованы индексы 0-8, state: `used:[0,1,2,3,4,5,6,7,8]`
- ⚠️ **Задача отключена 16.08** (`schtasks /change /tn "TelegramPoster" /disable`)
- Единственный постер: GitHub Actions `site/posts.yml` (пн/ср/пт/сб 05:10 UTC)
