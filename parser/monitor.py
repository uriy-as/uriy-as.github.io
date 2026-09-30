#!/usr/bin/env python3
"""Мониторинг цен конкурентов: сбор -> сравнение с состоянием -> алерты."""

import argparse
import json
import os
import re
import sys
import time
import urllib.robotparser
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = BASE_DIR / 'sources.json'
DEFAULT_STATE = BASE_DIR / 'state.json'
DEFAULT_REPORT = BASE_DIR / 'report.html'
USER_AGENT = 'WebStudioPriceBot/1.0 (+https://uriy-as.org)'
CURRENCY_TOKEN = r'(?:[€$₴₽£])|(?:грн\.?|UAH|руб\.?|RUB|USD|EUR)'
NUMBER_TOKEN = r'\d{1,3}(?:[   .,]\d{3})*(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?'
PRICE_RE = re.compile(
    rf'(?P<cur1>{CURRENCY_TOKEN})\s*(?P<num1>{NUMBER_TOKEN})'
    rf'|(?P<num2>{NUMBER_TOKEN})\s*(?P<cur2>{CURRENCY_TOKEN})'
)
CURRENCY_ALIASES = {
    '€': 'EUR', '$': 'USD', '₴': 'UAH', '₽': 'RUB', '£': 'GBP',
    'грн': 'UAH', 'грн.': 'UAH', 'uah': 'UAH',
    'руб': 'RUB', 'руб.': 'RUB', 'rub': 'RUB',
    'usd': 'USD', 'eur': 'EUR',
}


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def log(message):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {message}', flush=True)


def normalize_currency(token):
    return CURRENCY_ALIASES.get(token.lower().strip(), token.upper())


def parse_number(raw):
    cleaned = re.sub(r'[   ]', '', raw)
    if re.fullmatch(r'\d{1,3}(?:[.,]\d{3})+(?:[.,]\d{1,2})?', cleaned):
        cleaned = cleaned.replace(',', '')
    else:
        if cleaned.count(',') and cleaned.count('.'):
            cleaned = cleaned.replace(',', '.') if cleaned.rfind(',') > cleaned.rfind('.') else cleaned.replace(',', '')
        else:
            cleaned = cleaned.replace(',', '.')
    try:
        return float(cleaned)
    except ValueError:
        return None


def load_config(path):
    with open(path, encoding='utf-8') as handle:
        config = json.load(handle)
    if not config.get('sources'):
        raise ValueError('В конфиге нет ни одного источника')
    return config


def load_state(path):
    if not Path(path).exists():
        return {'updated': None, 'sources': {}}
    with open(path, encoding='utf-8') as handle:
        try:
            return json.load(handle)
        except json.JSONDecodeError:
            return {'updated': None, 'sources': {}}


def save_state(path, state):
    Path(path).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def robots_allows(url, user_agent):
    parsed = urlparse(url)
    robots_url = f'{parsed.scheme}://{parsed.netloc}/robots.txt'
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(robots_url)
    try:
        parser.read()
    except Exception:
        return True
    if parser.last_checked == 0:
        return True
    try:
        return parser.can_fetch(user_agent, url)
    except Exception:
        return True


def fetch(url, timeout, retries, delay, respect_robots):
    if respect_robots and not robots_allows(url, USER_AGENT):
        raise PermissionError(f'robots.txt запрещает доступ к {url}')
    headers = {'User-Agent': USER_AGENT, 'Accept-Language': 'uk,ru,en;q=0.8'}
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 429:
                wait = 2 ** attempt
                log(f'  429 от {urlparse(url).netloc}, ждём {wait} с')
                time.sleep(wait)
                continue
            response.raise_for_status()
            if not response.encoding or response.encoding.lower() == 'iso-8859-1':
                response.encoding = response.apparent_encoding or 'utf-8'
            time.sleep(delay)
            return response.text
        except requests.RequestException as error:
            last_error = error
            if attempt < retries:
                time.sleep(2 ** attempt)
    raise last_error


def count_prices(text):
    return len(PRICE_RE.findall(text))


def refine_containers(containers, max_depth=4):
    result = []
    for container in containers:
        node = container
        for _ in range(max_depth):
            text = node.get_text(' ', strip=True)
            if count_prices(text) <= 1:
                break
            children = [c for c in node.find_all(recursive=False) if count_prices(c.get_text(' ', strip=True))]
            if not children:
                break
            node = children[0] if len(children) == 1 else node
            if len(children) > 1:
                result.extend(refine_containers(children, max_depth - 1))
                node = None
                break
        if node is not None and count_prices(node.get_text(' ', strip=True)) <= 1:
            result.append(node)
    return result or containers


STRUCK_SELECTOR = 'del, s, strike, [class*="old" i], [class*="was" i], [class*="pold" i], [class*="cross" i]'
PLACEHOLDER_LABELS = ('спецпредложение', 'акция', 'акція')


def prepare_soup(html):
    soup = BeautifulSoup(html, 'lxml')
    for element in soup.select(STRUCK_SELECTOR):
        element.decompose()
    return soup


CURRENCY_WORDS = re.compile(
    r'(?:\b(?:грн|uah|usd|eur|rub|руб|євро)\b)|[€$₴₽£]', re.IGNORECASE)
FILLER_WORDS = {'від', 'от', 'з', 'від.', 'от.', 'from', 'starting', 'at', 'цена', 'price'}


def clean_label(text):
    text = re.sub(r'\s+', ' ', text).strip(' -—–·|,.:;«»"')
    text = re.sub(r'^(?:от|від|з|starting at)\s*', '', text, flags=re.IGNORECASE).strip(' -—–·|,.:;')
    text = re.sub(r'\s*(?:от|від)$', '', text, flags=re.IGNORECASE).strip(' -—–·|,.:;')
    if text.lower() in FILLER_WORDS:
        return ''
    if len(re.sub(r'[^A-Za-zА-Яа-яІіЇїЄєҐґ]', '', CURRENCY_WORDS.sub(' ', text))) < 3:
        return ''
    return text[:70].strip(' -—–·|,.:;')


def build_label(text, match):
    prefix = clean_label(text[:match.start()])
    suffix = clean_label(text[match.end():])
    label = prefix or suffix
    if not label:
        label = clean_label(text) or PLACEHOLDER_LABELS[0]
    return label


def extract_prices(soup, selector, limit, label_selector=None):
    containers = soup.select(selector) if selector else [soup]
    if selector and not containers:
        return []
    if not label_selector:
        containers = refine_containers(containers)
    found = []
    seen = set()
    for container in containers:
        text = container.get_text(' ', strip=True)
        if not text:
            continue
        base_label = ''
        if label_selector:
            label_node = container.select_one(label_selector)
            if label_node:
                base_label = clean_label(label_node.get_text(' ', strip=True))
        for match in PRICE_RE.finditer(text):
            number_raw = match.group('num1') or match.group('num2')
            currency_raw = match.group('cur1') or match.group('cur2')
            value = parse_number(number_raw)
            if value is None or value <= 0:
                continue
            currency = normalize_currency(currency_raw)
            label = base_label or build_label(text, match)
            key = (label.lower(), value, currency)
            if key in seen:
                continue
            seen.add(key)
            found.append({'label': label, 'value': value, 'currency': currency, 'raw': match.group(0).strip()})
            if len(found) >= limit:
                return found
    return found


def collect_source(source, config, dry_run):
    url = source['url']
    delay = config.get('delay_seconds', 2)
    timeout = config.get('timeout_seconds', 25)
    retries = config.get('retries', 3)
    limit = source.get('max_items', config.get('max_items', 40))
    log(f'  GET {url}')
    html = fetch(url, timeout, retries, delay, config.get('respect_robots', True))
    prices = extract_prices(prepare_soup(html), source.get('selector'), limit, source.get('label_selector'))
    return {'url': url, 'ok': True, 'count': len(prices), 'prices': prices,
            'checked_at': now_iso(), 'http_bytes': len(html), 'dry_run': dry_run}


def diff_source(previous, current, threshold_pct):
    if not previous:
        return {'baseline': True, 'changed': [], 'unchanged': len(current['prices']), 'added': len(current['prices'])}
    old_index = {(p['label'].lower(), p['currency']): p['value'] for p in previous.get('prices', [])}
    new_index = {(p['label'].lower(), p['currency']): p['value'] for p in current['prices']}
    changed, unchanged = [], 0
    for key, new_value in new_index.items():
        if key not in old_index:
            continue
        old_value = old_index[key]
        if old_value <= 0:
            continue
        delta_pct = (new_value - old_value) / old_value * 100
        if abs(delta_pct) >= threshold_pct:
            changed.append({
                'label': next(p['label'] for p in current['prices']
                              if (p['label'].lower(), p['currency']) == key),
                'currency': key[1],
                'old': old_value,
                'new': new_value,
                'delta_pct': round(delta_pct, 1),
            })
        else:
            unchanged += 1
    return {
        'baseline': False,
        'changed': changed,
        'unchanged': unchanged,
        'added': len([k for k in new_index if k not in old_index]),
        'removed': len([k for k in old_index if k not in new_index]),
    }


def format_value(value, currency):
    if value is None:
        return '—'
    formatted = f'{value:,.2f}'.rstrip('0').rstrip('.')
    return f'{formatted} {currency}'


def build_tg_message(report, config):
    lines = ['<b>📉 Мониторинг цен конкурентов</b>', '']
    total_changed = 0
    for entry in report['sources']:
        name = entry['name']
        if not entry.get('ok'):
            lines.append(f'❌ <b>{escape(name)}</b> — {escape(str(entry.get("error", "ошибка")))[:80]}')
            continue
        delta = entry['delta']
        if delta.get('baseline'):
            lines.append(f'🆕 <b>{escape(name)}</b> — база: {delta["unchanged"]} позиций')
            continue
        for change in delta['changed']:
            arrow = '📈' if change['delta_pct'] > 0 else '📉'
            sign = '+' if change['delta_pct'] > 0 else ''
            lines.append(
                f'{arrow} <b>{escape(name)}</b>\n'
                f'   {escape(change["label"])}\n'
                f'   {format_value(change["old"], change["currency"])} → '
                f'<b>{format_value(change["new"], change["currency"])}</b> ({sign}{change["delta_pct"]}%)'
            )
            total_changed += 1
    if total_changed == 0:
        lines.append(f'✅ Изменений выше порога {config.get("threshold_pct", 5)}% нет')
    lines.append('')
    lines.append(f'Источников: {len(report["sources"])} · порог: {config.get("threshold_pct", 5)}%')
    return '\n'.join(lines)


def first_env(names):
    names = names if isinstance(names, list) else [names]
    for name in names:
        value = os.environ.get(name)
        if value:
            return value, name
    return None, names[0]


def send_tg(text, config):
    token, token_name = first_env(config.get('telegram_token_env', ['TELEGRAM_TOKEN', 'TELEGRAM_BOT_TOKEN', 'TG_BOT_TOKEN']))
    chat_id, chat_name = first_env(config.get('telegram_chat_env', ['ADMIN_CHAT_ID', 'TELEGRAM_CHAT_ID', 'CHAT_ID']))
    if not token or not chat_id:
        return False, f'нет {token_name} / {chat_name} в окружении'
    try:
        response = requests.post(
            f'https://api.telegram.org/bot{token}/sendMessage',
            json={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML', 'disable_web_page_preview': True},
            timeout=20,
        )
        return response.ok, f'HTTP {response.status_code}'
    except requests.RequestException as error:
        return False, str(error)


def render_report(report, config, out_path):
    generated = datetime.now().strftime('%d.%m.%Y %H:%M')
    rows = []
    for entry in report['sources']:
        if not entry.get('ok'):
            rows.append(f'<tr class="err"><td colspan="4">❌ {escape(entry["name"])} — '
                        f'{escape(str(entry.get("error", "ошибка")))}</td></tr>')
            continue
        delta = entry['delta']
        for price in entry['prices']:
            change = next(
                (c for c in delta.get('changed', [])
                 if c['label'].lower() == price['label'].lower() and c['currency'] == price['currency']),
                None)
            if change:
                css = 'up' if change['delta_pct'] > 0 else 'down'
                sign = '+' if change['delta_pct'] > 0 else ''
                change_html = f'<span class="chg {css}">{sign}{change["delta_pct"]}%</span>'
                old_html = f'<s>{format_value(change["old"], price["currency"])}</s> '
            else:
                change_html = '<span class="same">—</span>'
                old_html = ''
            rows.append(
                f'<tr><td class="name">{escape(entry["name"])}</td>'
                f'<td class="label">{escape(price["label"])}</td>'
                f'<td class="val">{old_html}{format_value(price["value"], price["currency"])}</td>'
                f'<td class="chg-cell">{change_html}</td></tr>'
            )
    body = '\n'.join(rows) or '<tr><td colspan="4">Нет данных</td></tr>'
    total_prices = sum(entry.get('count', 0) for entry in report['sources'])
    ok_sources = sum(1 for entry in report['sources'] if entry.get('ok'))
    html = f"""<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8">
<title>Мониторинг цен — отчёт</title>
<style>
  :root {{ color-scheme: light; }}
  body {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 32px;
         background: #f6f7f9; color: #1a1d21; }}
  .wrap {{ max-width: 1080px; margin: 0 auto; background: #fff; border-radius: 12px;
           box-shadow: 0 1px 3px rgba(0,0,0,.1); overflow: hidden; }}
  header {{ background: #1a1d21; color: #fff; padding: 22px 28px; }}
  header h1 {{ margin: 0 0 4px; font-size: 20px; }}
  header p {{ margin: 0; opacity: .75; font-size: 13px; }}
  .stats {{ display: flex; gap: 28px; padding: 18px 28px; border-bottom: 1px solid #e8eaed; }}
  .stat b {{ display: block; font-size: 22px; }}
  .stat span {{ font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: .04em; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
  th, td {{ padding: 9px 14px; text-align: left; border-bottom: 1px solid #f0f1f3; vertical-align: top; }}
  th {{ background: #fafbfc; font-size: 11px; text-transform: uppercase; letter-spacing: .05em; color: #6b7280; }}
  .name {{ width: 150px; font-weight: 600; color: #374151; }}
  .label {{ color: #4b5563; }}
  .val {{ white-space: nowrap; font-variant-numeric: tabular-nums; font-weight: 600; }}
  .chg-cell {{ width: 90px; }}
  .chg {{ font-weight: 700; }}
  .up {{ color: #dc2626; }}
  .down {{ color: #16a34a; }}
  .same {{ color: #d1d5db; }}
  .err {{ color: #dc2626; }}
  footer {{ padding: 16px 28px; font-size: 12px; color: #9ca3af; border-top: 1px solid #e8eaed; }}
  s {{ color: #9ca3af; font-weight: 400; }}
</style></head>
<body><div class="wrap">
<header>
  <h1>Мониторинг цен конкурентов</h1>
  <p>Автоматический сбор публичных прайсов · порог алерта {config.get('threshold_pct', 5)}% · сгенерировано {generated}</p>
</header>
<div class="stats">
  <div class="stat"><b>{ok_sources}</b><span>источников собрано</span></div>
  <div class="stat"><b>{total_prices}</b><span>позиций с ценой</span></div>
  <div class="stat"><b>{config.get('threshold_pct', 5)}%</b><span>порог алерта</span></div>
  <div class="stat"><b>0%</b><span>обхода авторизации</span></div>
</div>
<table><thead><tr><th>Источник</th><th>Услуга</th><th>Цена</th><th>Δ</th></tr></thead>
<tbody>
{body}
</tbody></table>
<footer>Python 3 · requests + BeautifulSoup · соблюдение robots.txt · вежливый User-Agent · алерты в Telegram</footer>
</div></body></html>"""
    Path(out_path).write_text(html, encoding='utf-8')
    return out_path


def main():
    parser = argparse.ArgumentParser(description='Мониторинг цен конкурентов')
    parser.add_argument('--config', default=str(DEFAULT_CONFIG))
    parser.add_argument('--state', default=str(DEFAULT_STATE))
    parser.add_argument('--report', default=str(DEFAULT_REPORT))
    parser.add_argument('--threshold', type=float, default=None, help='порог изменения, %%')
    parser.add_argument('--no-alert', action='store_true', help='не слать алерты в Telegram')
    parser.add_argument('--always-alert', action='store_true', help='слать отчёт, даже если изменений нет')
    parser.add_argument('--skip-local-only', action='store_true',
                        help='пропустить источники, помеченные local_only (для запуска с CI)')
    parser.add_argument('--dry-run', action='store_true', help='собрать, но не менять state.json')
    parser.add_argument('--only', default=None, help='снять только источники через запятую')
    args = parser.parse_args()

    config = load_config(args.config)
    if args.threshold is not None:
        config['threshold_pct'] = args.threshold
    threshold = config.get('threshold_pct', 5)

    sources = config['sources']
    if args.skip_local_only:
        skipped = [s['name'] for s in sources if s.get('local_only')]
        sources = [s for s in sources if not s.get('local_only')]
        if skipped:
            log(f'Пропущены источники только для локального запуска: {", ".join(skipped)}')
    if args.only:
        wanted = {name.strip() for name in args.only.split(',')}
        sources = [s for s in sources if s['name'] in wanted]
        if not sources:
            log(f'Нет источников по фильтру {args.only}')
            return 1

    state = load_state(args.state)
    report = {'generated': now_iso(), 'threshold_pct': threshold, 'sources': []}

    log(f'Старт: {len(sources)} источников, порог {threshold}%')
    for source in sources:
        entry = {'name': source['name']}
        try:
            collected = collect_source(source, config, args.dry_run)
            previous = state['sources'].get(source['name'])
            entry.update(collected)
            entry['delta'] = diff_source(previous, collected, threshold)
            log(f'  OK {source["name"]}: {collected["count"]} цен, '
                f'{"база" if entry["delta"]["baseline"] else str(len(entry["delta"]["changed"])) + " изменений"}')
        except Exception as error:
            entry.update({'ok': False, 'error': f'{type(error).__name__}: {error}',
                          'checked_at': now_iso(), 'count': 0, 'prices': [], 'delta': {'changed': []}})
            log(f'  FAIL {source["name"]}: {type(error).__name__}: {error}')
        report['sources'].append(entry)

    render_report(report, config, args.report)
    log(f'Отчёт: {args.report}')

    if not args.dry_run:
        for entry in report['sources']:
            if entry.get('ok'):
                state['sources'][entry['name']] = {'prices': entry['prices'], 'checked_at': entry['checked_at'],
                                                   'url': entry['url']}
        state['updated'] = now_iso()
        save_state(args.state, state)
        log(f'Состояние сохранено: {args.state}')

    changed_total = sum(len(e['delta'].get('changed', [])) for e in report['sources'])
    if not args.no_alert:
        message = build_tg_message(report, config)
        if changed_total or args.always_alert:
            ok, detail = send_tg(message, config)
            log(f'Telegram: {"отправлено" if ok else "не отправлено — " + detail}')
            if not ok:
                print('--- сообщение, которое ушло бы в Telegram ---')
                print(message)
        else:
            log('Telegram: изменений выше порога нет, уведомление не отправлялось')
    return 0


if __name__ == '__main__':
    sys.exit(main())
