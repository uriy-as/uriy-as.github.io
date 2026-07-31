# GA4 Service Account Setup

## Шаг 1: Создать проект в Google Cloud

1. Открой https://console.cloud.google.com/
2. В шапке слева — выпадашка **Select a project** → **NEW PROJECT**
3. Название: `webstudio-ga4`
4. Жми **CREATE**

## Шаг 2: Включить API

- Открой https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com
- Жми **ENABLE**

## Шаг 3: Создать сервисный аккаунт

- Открой https://console.cloud.google.com/iam-admin/serviceaccounts
- Выбери проект `webstudio-ga4`
- Жми **+ CREATE SERVICE ACCOUNT**
- Имя: `ga4-stats`, жми **CREATE AND CONTINUE**
- Роль: **Viewer** (Просмотрщик) → **CONTINUE** → **DONE**

## Шаг 4: Создать ключ

- В списке сервисных аккаунтов — нажми на `ga4-stats@...`
- Вкладка **KEYS** → **ADD KEY** → **Create new key** → **JSON**
- Файл скачается автоматически

## Шаг 5: Дать доступ в GA4

1. https://analytics.google.com/
2. Шестерёнка → Администратор → колонка Свойство → Управление доступом к свойству
3. + Добавить участника
4. Email: `ga4-stats@webstudio-ga4.iam.gserviceaccount.com`
5. Роль: **Просмотрщик**
6. Сохранить

## Шаг 6: Скинуть мне

Отправь мне содержимое JSON-файла (или сам файл) — я добавлю его в секреты и обновлю код.
