# Fix 502 + сделать статистику всегда доступной

## Проблема
- `deploy.yml` запускает деплой в pages при каждом пуше. Несколько пушей подряд → одновременные деплои → GitHub Pages на секунды выдаёт 502.
- `astap.pythonanywhere.com/stats` показывает статистику, но бэкенд может спать (502/timeout).

## Решение

### 1. deploy.yml — concurrency
Добавить перед `jobs:`:
```yaml
concurrency:
  group: production
  cancel-in-progress: false
```
Деплои больше не накладываются: каждый следующий ждёт завершения предыдущего.

### 2. daily-stats.py — генерация stats.html
Добавить в конец файла (после `tg_send(...)`) код генерации статической HTML-страницы с теми же данными (просмотры, уникальные, рефереры, популярные страницы, клоны). Сохраняется в `$GITHUB_WORKSPACE/stats.html`.

Полный код — см. ниже.

### 3. daily-stats.yml — commit+push
Добавить шаг после `daily-stats.py`:
```yaml
- name: Commit stats.html
  env:
    GH_TOKEN: ${{ secrets.GH_PAT }}
  run: |
    git config user.name "Stats Bot"
    git config user.email "stats@uriy-as.org"
    git add stats.html
    if git diff --quiet --staged; then
      echo "No changes"
    else
      git commit -m "Update stats.html $(date -u +%Y-%m-%d)"
      git remote set-url origin "https://x-access-token:${GH_TOKEN}@github.com/uriy-as/site.git"
      git push
    fi
```
При каждом запуске daily-stats генерируется свежий `stats.html`, коммитится в site, авто-деплоится на pages.

### 4. Футер — ссылка «Статистика»
В `index.html` (после `footer-privacy`):
```html
<p style="margin-top:4px;font-size:0.8rem;"><a href="stats.html" style="color:var(--muted);" data-i18n="footer-stats">Статистика</a></p>
```

В `en/index.html` (после `footer-privacy`):
```html
<p style="margin-top:4px;font-size:0.8rem;"><a href="stats.html" style="color:var(--muted);" data-i18n="footer-stats">Stats</a></p>
```

### 5. js/script.js — i18n
Добавить после `footer-privacy`:
```js
'footer-stats': { ru: 'Статистика', en: 'Stats' },
```

---

## Полный код для daily-stats.py (добавить в конец)

```python
# Generate stats.html
def esc(s):
    import html
    return html.escape(str(s))

def fmt_count(val):
    return str(val) if val else '0'

html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Статистика WebStudio</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:Arial,Helvetica,sans-serif; background:#f5f5f5; color:#222; padding:20px; line-height:1.5; }}
h1 {{ font-size:1.4rem; margin-bottom:4px; color:#333; }}
.meta {{ font-size:0.85rem; color:#888; margin-bottom:20px; }}
.grid {{ display:flex; gap:12px; flex-wrap:wrap; margin-bottom:20px; }}
.card {{ background:#fff; padding:14px 20px; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,0.1); flex:1; min-width:120px; text-align:center; }}
.card .num {{ font-size:1.6rem; font-weight:bold; color:#2563eb; }}
.card .label {{ font-size:0.8rem; color:#666; margin-top:2px; }}
h2 {{ font-size:1.1rem; margin:20px 0 10px; color:#444; }}
table {{ width:100%; border-collapse:collapse; background:#fff; border-radius:8px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.1); }}
th, td {{ padding:8px 12px; text-align:left; border-bottom:1px solid #eee; font-size:0.88rem; }}
th {{ background:#f8f9fa; color:#555; font-weight:600; }}
tr:hover {{ background:#f0f7ff; }}
a {{ color:#2563eb; text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
.note {{ color:#888; font-size:0.8rem; margin-top:8px; }}
</style>
</head>
<body>
<h1>&#x1f4ca; Статистика WebStudio</h1>
<p class="meta">Данные за последние 14 дней (GitHub Traffic API) &middot; Обновлено: {datetime.utcnow().strftime('%d.%m.%Y %H:%M')} UTC</p>

<div class="grid">
    <div class="card"><div class="num">{fmt_count(total_views)}</div><div class="label">Просмотров за 14 дней</div></div>
    <div class="card"><div class="num">{fmt_count(total_unique)}</div><div class="label">Уникальных посетителей</div></div>
</div>
<div class="grid">
    <div class="card"><div class="num">{fmt_count(y_views)}</div><div class="label">Просмотров вчера</div></div>
    <div class="card"><div class="num">{fmt_count(y_unique)}</div><div class="label">Уникальных вчера</div></div>
</div>'''

if total_clones:
    html += f'''
<div class="grid">
    <div class="card"><div class="num">{fmt_count(total_clones)}</div><div class="label">Клонов за 14 дней</div></div>
    <div class="card"><div class="num">{fmt_count(total_clone_unique)}</div><div class="label">Уникальных клонов</div></div>
    <div class="card"><div class="num">{fmt_count(y_clones)}</div><div class="label">Клонов вчера</div></div>
    <div class="card"><div class="num">{fmt_count(y_clone_unique)}</div><div class="label">Уникальных клонов вчера</div></div>
</div>'''

if refs:
    html += '<h2>&#x1f310; Откуда приходят</h2><table><thead><tr><th>Источник</th><th>Переходов</th></tr></thead><tbody>'
    for r in refs:
        html += f'<tr><td>{esc(r["referrer"])}</td><td>{r["count"]}</td></tr>'
    html += '</tbody></table>'

if content:
    html += '<h2>&#x1f4cc; Популярные страницы</h2><table><thead><tr><th>Страница</th><th>Просмотров</th><th>Уникальных</th></tr></thead><tbody>'
    for c in content:
        html += f'<tr><td>{esc(c["path"])}</td><td>{c["count"]}</td><td>{c["uniques"]}</td></tr>'
    html += '</tbody></table>'

html += '''
<p class="note">&#x1f517; Подробная статистика в реальном времени: <a href="https://astap.pythonanywhere.com/stats" target="_blank">astap.pythonanywhere.com/stats</a></p>
</body>
</html>'''

output_path = os.path.join(os.environ.get('GITHUB_WORKSPACE', '.'), 'stats.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'stats.html written to {output_path}')
```

## Итог
- `concurrency` в deploy.yml → деплои не накладываются → 502 уходит
- `stats.html` на GitHub Pages → всегда доступна, даже если PythonAnywhere спит
- Ссылка в футере → можно открыть в 1 клик
- Обновляется раз в день (по расписанию daily-stats) или вручную через workflow_dispatch
