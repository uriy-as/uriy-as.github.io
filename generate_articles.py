#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate individual article HTML pages for blog/ and en/blog/"""

import os, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))

HEAD_COMMON = '''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/svg+xml" href="/images/logo.svg">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://uriy-as.org{path}">
    <meta property="og:image" content="https://uriy-as.org/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="{locale}">
    <meta property="og:site_name" content="WebStudio">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="https://uriy-as.org/og-image.png">
    <link rel="canonical" href="https://uriy-as.org{path}">
    <link rel="alternate" hreflang="x-default" href="https://uriy-as.org{path_ru}">
    <link rel="alternate" hreflang="ru" href="https://uriy-as.org{path_ru}">
    <link rel="alternate" hreflang="en" href="https://uriy-as.org{path_en}">
    <link rel="dns-prefetch" href="https://Astap.pythonanywhere.com">
    <link rel="preconnect" href="https://Astap.pythonanywhere.com" crossorigin>
    <link rel="dns-prefetch" href="https://mc.yandex.ru">
    <link rel="preconnect" href="https://mc.yandex.ru" crossorigin>
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-MY48PMFD5M"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-MY48PMFD5M')</script>
    <link rel="stylesheet" href="/css/style.css?v=4">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{headline}",
        "description": "{description}",
        "author": {{ "@type": "Organization", "name": "WebStudio", "url": "https://uriy-as.org" }},
        "publisher": {{ "@type": "Organization", "name": "WebStudio", "url": "https://uriy-as.org" }},
        "datePublished": "{date_iso}",
        "dateModified": "2026-06-26",
        "mainEntityOfPage": "https://uriy-as.org{path}"
    }}
    </script>
    <style>
        .article-hero {{ padding: 140px 0 40px; text-align: center; }}
        .article-hero h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
        .article-content {{ max-width: 800px; margin: 0 auto; padding-bottom: 80px; line-height: 1.8; font-size: 1.05rem; }}
        .article-content p {{ margin-bottom: 1.2rem; color: var(--muted); }}
        .article-content h2 {{ font-size: 1.4rem; margin: 2rem 0 1rem; color: var(--accent); }}
        .article-content h3 {{ font-size: 1.15rem; margin: 1.5rem 0 0.8rem; }}
        .article-content ul, .article-content ol {{ margin-bottom: 1.2rem; padding-left: 1.5rem; color: var(--muted); }}
        .article-content li {{ margin-bottom: 0.5rem; }}
        .article-content .meta {{ font-size: 0.85rem; color: var(--muted); margin-bottom: 1rem; }}
        .article-back {{ display: inline-block; margin-bottom: 2rem; color: var(--accent); text-decoration: none; }}
        .article-back:hover {{ text-decoration: underline; }}
        .share-btns {{ display: flex; gap: 0.75rem; margin-top: 2rem; flex-wrap: wrap; }}
        .share-btn {{ display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none; font-size: 0.9rem; border: 1px solid var(--border); transition: all 0.2s; }}
        .share-btn svg {{ width: 18px; height: 18px; }}
        .share-btn--tg {{ background: #2AABEE; color: #fff; border-color: #2AABEE; }}
        .share-btn--tg:hover {{ background: #229ED9; }}
        .share-btn--email {{ background: var(--card-bg); color: var(--text); }}
        .share-btn--email:hover {{ border-color: var(--accent); }}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header__inner">
                <a href="/" class="logo"><img src="/images/logo.svg" alt="WebStudio" class="logo__img"></a>
                <nav class="nav">
                    <a href="/#services" data-i18n="nav-services">{nav_services}</a>
                    <a href="/#about" data-i18n="nav-about">{nav_about}</a>
                    <a href="/articles.html" data-i18n="nav-articles">{nav_articles}</a>
                    <a href="/#contact" data-i18n="nav-contacts">{nav_contacts}</a>
                    <a href="#" class="nav__bot" data-i18n="nav-chat" onclick="event.preventDefault();document.getElementById('chatBtn').click();this.blur();return false;">{nav_chat}</a>
                </nav>
                <button class="burger" id="burger" aria-label="{burger_label}">
                    <span></span><span></span><span></span>
                </button>
            </div>
        </div>
    </header>

    <section class="article-hero">
        <div class="container">
            <a href="/articles.html" class="article-back" data-i18n="article-back">{back}</a>
            <h1>{h1}</h1>
            <div class="meta">{date_str}</div>
        </div>
    </section>

    <section class="article-content">
        <div class="container">
            {content}

            <div class="share-btns">
                <a href="https://t.me/share/url?url=https://uriy-as.org{share_url}&text={share_text}" target="_blank" class="share-btn share-btn--tg" data-i18n="article-share-tg">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M22.26.76a1.73 1.73 0 0 0-1.76-.35L1.84 9.58a1.66 1.66 0 0 0 .05 3.08l4.88 1.9 2.94 8.86a1.38 1.38 0 0 0 .9.87 1.32 1.32 0 0 0 1.2-.21l4.23-3.46a1.8 1.8 0 0 1 2.05-.12l4.85 3.52a1.35 1.35 0 0 0 1.45.12 1.38 1.38 0 0 0 .78-1.15L23.7 2.47a1.73 1.73 0 0 0-1.44-1.71z"/></svg>
                    {share_tg}
                </a>
                <a href="mailto:?subject={email_subject}&body=https://uriy-as.org{share_url}" class="share-btn share-btn--email" data-i18n="article-share-email">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 4L12 13 2 4"/></svg>
                    {share_email}
                </a>
            </div>
            <p style="margin-top:1.5rem"><a href="{cta_url}" class="btn btn--primary btn--sm">{cta_text}</a></p>
        </div>
    </section>

    <section class="tg-promo section">
        <div class="container">
            <div class="tg-promo__inner">
                <h2 data-i18n="tg-promo-title">{promo_title}</h2>
                <p data-i18n="tg-promo-desc">{promo_desc}</p>
                <a href="https://t.me/webstudio_chanel" target="_blank" class="btn btn--tg" data-i18n="tg-promo-btn">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M22.26.76a1.73 1.73 0 0 0-1.76-.35L1.84 9.58a1.66 1.66 0 0 0 .05 3.08l4.88 1.9 2.94 8.86a1.38 1.38 0 0 0 .9.87 1.32 1.32 0 0 0 1.2-.21l4.23-3.46a1.8 1.8 0 0 1 2.05-.12l4.85 3.52a1.35 1.35 0 0 0 1.45.12 1.38 1.38 0 0 0 .78-1.15L23.7 2.47a1.73 1.73 0 0 0-1.44-1.71z"/></svg>
                    {promo_btn}
                </a>
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <div class="footer__inner">
                <div class="footer__left">
                    <a href="/" class="logo"><img src="/images/logo.svg" alt="WebStudio" class="logo__img"></a>
                    <p data-i18n="footer-copyright">{footer_copy}</p>
                    <p style="margin-top:8px;font-size:0.85rem;" data-i18n="footer-bot"><a href="https://t.me/NevWebStudio_bot" target="_blank" style="color:var(--accent);">{footer_bot}</a> {footer_bot_text}</p>
                    <p style="margin-top:4px;font-size:0.8rem;"><a href="/privacy.html" style="color:var(--muted);" data-i18n="footer-privacy">{footer_privacy}</a></p>
                </div>
                <div class="footer__social">
                    <a href="https://t.me/uriy_as59" target="_blank" aria-label="Telegram">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M22.26.76a1.73 1.73 0 0 0-1.76-.35L1.84 9.58a1.66 1.66 0 0 0 .05 3.08l4.88 1.9 2.94 8.86a1.38 1.38 0 0 0 .9.87 1.32 1.32 0 0 0 1.2-.21l4.23-3.46a1.8 1.8 0 0 1 2.05-.12l4.85 3.52a1.35 1.35 0 0 0 1.45.12 1.38 1.38 0 0 0 .78-1.15L23.7 2.47a1.73 1.73 0 0 0-1.44-1.71z"/></svg>
                    </a>
                    <a href="https://youtube.com/@webstudio" target="_blank" aria-label="YouTube">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2a2.96 2.96 0 0 0-2.08-2.1C19.55 3.5 12 3.5 12 3.5s-7.55 0-9.42.6A2.96 2.96 0 0 0 .5 6.2 30.9 30.9 0 0 0 0 12a30.9 30.9 0 0 0 .5 5.8 2.96 2.96 0 0 0 2.08 2.1c1.87.6 9.42.6 9.42.6s7.55 0 9.42-.6a2.96 2.96 0 0 0 2.08-2.1 30.9 30.9 0 0 0 .5-5.8 30.9 30.9 0 0 0-.5-5.8zM9.55 15.57V8.43L15.82 12l-6.27 3.57z"/></svg>
                    </a>
                </div>
            </div>
        </div>
    </footer>

    <a href="https://t.me/uriy_as59" target="_blank" class="tg-float" aria-label="Telegram">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M22.26.76a1.73 1.73 0 0 0-1.76-.35L1.84 9.58a1.66 1.66 0 0 0 .05 3.08l4.88 1.9 2.94 8.86a1.38 1.38 0 0 0 .9.87 1.32 1.32 0 0 0 1.2-.21l4.23-3.46a1.8 1.8 0 0 1 2.05-.12l4.85 3.52a1.35 1.35 0 0 0 1.45.12 1.38 1.38 0 0 0 .78-1.15L23.7 2.47a1.73 1.73 0 0 0-1.44-1.71z"/></svg>
        <span data-i18n="article-share-tg">{tg_float}</span>
    </a>

    <div class="lang-widget" id="langWidget">
        <button class="lang-btn-floating" id="langBtnFloat" aria-label="Switch language" onclick="toggleLang()">{lang_btn}</button>
    </div>

    <div class="chat-widget" id="chatWidget">
        <button class="chat-btn" id="chatBtn" aria-label="{chat_aria}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            <span data-i18n="chat-btn-text">{chat_btn}</span>
        </button>
        <div class="chat-popup" id="chatPopup">
            <div class="chat-popup__header">
                <h4 data-i18n="chat-title">{chat_title}</h4>
                <button class="chat-popup__close" id="chatClose">&times;</button>
            </div>
            <div class="chat-popup__body" id="chatBody">
                <div class="chat-msg chat-msg--bot" data-i18n="chat-error" style="display:none;"></div>
            </div>
            <form class="chat-popup__form" id="chatForm">
                <input type="text" placeholder="{chat_placeholder}" autocomplete="off" required data-i18n="chat-placeholder">
                <button type="submit">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
                </button>
            </form>
        </div>
    </div>

    <script defer src="/js/script.js?v=2a1f9c3"></script>
    <noscript><img src="https://Astap.pythonanywhere.com/pixel?page={path}&ref=" style="position:absolute;left:-9999px" alt="" /></noscript>
    <noscript><div><img src="https://mc.yandex.ru/watch/109350815" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
    <script>(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r){{return}}}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(109350815,"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true}});</script>
</body>
</html>'''

def ru_article(slug, title, date_str, description, content, cta_text, cta_url, date_iso, has_image=False, img_src="", img_alt=""):
    path = f"/blog/{slug}.html"
    img_html = ''
    if has_image:
        img_html = f'<img src="{img_src}" alt="{img_alt}" width="800" height="600" loading="lazy" style="width:100%;max-width:600px;height:auto;border-radius:12px;margin-bottom:1rem;">\n            '
    content_html = img_html + content if has_image else content
    return HEAD_COMMON.format(
        lang="ru",
        title=f"{title} — WebStudio",
        description=description,
        path=path,
        path_ru=path,
        path_en="/en/blog/" + en_slug_for(slug) + ".html",
        headline=title,
        date_iso=date_iso,
        locale="ru_RU",
        nav_services="Услуги",
        nav_about="О нас",
        nav_articles="Статьи",
        nav_contacts="Контакты",
        nav_chat="AI-чат",
        burger_label="Меню",
        back="← Все статьи",
        h1=title,
        date_str=date_str,
        content=content_html,
        share_url=path,
        share_text=urllib.parse.quote(title),
        share_tg="Telegram",
        share_email="Email",
        email_subject=urllib.parse.quote(f"WebStudio: {title}"),
        cta_url=cta_url,
        cta_text=cta_text,
        promo_title="Подпишитесь на наш Telegram-канал",
        promo_desc="Кейсы, статьи и инсайты по разработке сайтов, Telegram-ботов и контент-маркетингу. Публикуем полезный контент каждый понедельник, среду, пятницу и субботу в 08:10.",
        promo_btn="Подписаться в Telegram",
        footer_copy="© 2026 WebStudio. Все права защищены.",
        footer_bot="@NevWebStudio_bot",
        footer_bot_text="— бот ответит на все интересующие вопросы",
        footer_privacy="Политика конфиденциальности",
        tg_float="Telegram",
        lang_btn="EN",
        chat_aria="Чат",
        chat_btn="Чат",
        chat_title="Чат с WebStudio",
        chat_placeholder="Ваше сообщение..."
    )

def en_slug_for(ru_slug):
    mapping = {
        "seo-optimizatsiya-sayta": "seo-optimization-guide",
        "telegram-bot-ili-sayt": "telegram-bot-vs-website",
        "sayt-za-5-dney": "website-in-5-days",
        "ai-boty-vozmozhnosti": "ai-bots-capabilities",
        "nauchnye-stati-prodazhi": "science-articles-sell",
        "5-priznakov-plohogo-sayta": "5-signs-bad-website",
        "kak-vybrat-hosting": "how-to-choose-hosting",
        "ssl-sertifikat": "ssl-certificate-guide",
        "telegram-kanal-biznes-strategiya": "telegram-channel-strategy",
        "seo-dlya-nachinayushchikh": "seo-for-beginners",
    }
    return mapping.get(ru_slug, ru_slug)

def en_article(slug, ru_slug, title, date_str, description, content, cta_text, cta_url, date_iso, has_image=False, img_src="", img_alt=""):
    path = f"/en/blog/{slug}.html"
    path_ru = f"/blog/{ru_slug}.html"
    img_html = ''
    if has_image:
        img_html = f'<img src="{img_src}" alt="{img_alt}" width="800" height="600" loading="lazy" style="width:100%;max-width:600px;height:auto;border-radius:12px;margin-bottom:1rem;">\n            '
    content_html = img_html + content if has_image else content
    return HEAD_COMMON.format(
        lang="en",
        title=f"{title} — WebStudio",
        description=description,
        path=path,
        path_ru=path_ru,
        path_en=path,
        headline=title,
        date_iso=date_iso,
        locale="en_US",
        nav_services="Services",
        nav_about="About",
        nav_articles="Articles",
        nav_contacts="Contact",
        nav_chat="AI Chat",
        burger_label="Menu",
        back="← All articles",
        h1=title,
        date_str=date_str,
        content=content_html,
        share_url=path,
        share_text=urllib.parse.quote(title),
        share_tg="Telegram",
        share_email="Email",
        email_subject=urllib.parse.quote(f"WebStudio: {title}"),
        cta_url=cta_url,
        cta_text=cta_text,
        promo_title="Subscribe to our Telegram channel",
        promo_desc="Cases, articles and insights on website development, Telegram bots and content marketing. We publish useful content every Monday, Wednesday, Friday and Saturday at 08:10.",
        promo_btn="Subscribe on Telegram",
        footer_copy="© 2026 WebStudio. All rights reserved.",
        footer_bot="@NevWebStudio_bot",
        footer_bot_text="— the bot will answer all your questions",
        footer_privacy="Privacy Policy",
        tg_float="Telegram",
        lang_btn="RU",
        chat_aria="Chat",
        chat_btn="Chat",
        chat_title="Chat with WebStudio",
        chat_placeholder="Your message..."
    )


articles_ru = [
    {
        "slug": "seo-optimizatsiya-sayta",
        "title": "Что такое SEO и почему оно важно для сайта",
        "date_str": "31 мая 2026",
        "date_iso": "2026-05-31",
        "description": "Узнайте, что такое SEO (поисковая оптимизация) и почему без него сайт не приносит клиентов. Основные шаги для продвижения в Google и Яндексе.",
        "cta_text": "Заказать SEO-продвижение",
        "cta_url": "/services.html",
        "has_image": True,
        "img_src": "/images/seo.jpg",
        "img_alt": "SEO оптимизация сайта: ключевые метрики и инструменты",
        "content": """<h2>Что такое SEO простыми словами</h2>
<p>SEO (Search Engine Optimization) — это комплекс мер, направленных на повышение позиций сайта в результатах поисковой выдачи. Проще говоря, это то, что помогает вашему сайту оказаться на первой странице Google или Яндекса, когда потенциальные клиенты ищут ваши товары или услуги.</p>
<p>Без SEO ваш сайт может быть красивым, современным и функциональным, но о нём никто не узнает. Поисковые системы — основной источник трафика для большинства сайтов. Более 70% пользователей никогда не переходят на вторую страницу поиска. Если вашего сайта нет в топ-10, вы теряете до 90% потенциальных клиентов.</p>
<h2>Почему SEO важно для бизнеса</h2>
<p>SEO — это не просто про трафик. Это про деньги. Когда ваш сайт находится на первой странице по коммерческим запросам, вы получаете целевых посетителей, которые уже заинтересованы в вашем продукте. Они не случайно зашли на сайт — они искали именно то, что вы предлагаете.</p>
<p>В отличие от контекстной рекламы, SEO даёт долгосрочный эффект. Вы платите один раз за оптимизацию, а трафик идёт годами. При этом клик по органической выдаче воспринимается пользователями как более заслуживающий доверия, чем рекламное объявление.</p>
<h2>Основные компоненты SEO</h2>
<h3>Техническое SEO</h3>
<p>Это фундамент, на котором держится весь сайт. Поисковые роботы должны легко сканировать и индексировать ваши страницы. Основные элементы технического SEO включают: скорость загрузки сайта (рекомендуется до 2 секунд), мобильную адаптацию, правильную структуру URL, файл robots.txt, карту сайта sitemap.xml, SSL-сертификат и чистый код без ошибок.</p>
<h3>Внутренняя оптимизация (On-page SEO)</h3>
<p>Это оптимизация контента и HTML-кода каждой страницы. Ключевые элементы: мета-теги title и description (уникальные для каждой страницы), правильная структура заголовков H1-H3, ключевые слова в тексте, оптимизация изображений (alt-теги, сжатие), внутренняя перелинковка и читабельные URL.</p>
<h3>Внешняя оптимизация (Off-page SEO)</h3>
<p>Это всё, что происходит за пределами вашего сайта, но влияет на его позиции. Главный фактор — ссылочный профиль: количество и качество внешних сайтов, которые ссылаются на вас.</p>
<h2>Как WebStudio включает SEO в каждый проект</h2>
<p>Мы не рассматриваем SEO как отдельную услугу, которую можно добавить «потом». Каждый сайт, который мы разрабатываем, с самого начала создаётся с учётом требований поисковых систем. Правильная семантическая вёрстка, оптимизированные изображения, мета-теги, скорость загрузки, микроразметка — всё это закладывается на этапе разработки.</p>"""
    },
    {
        "slug": "telegram-bot-ili-sayt",
        "title": "Telegram-бот или сайт: что выбрать для бизнеса",
        "date_str": "30 мая 2026",
        "date_iso": "2026-05-30",
        "description": "Сравнение Telegram-ботов и сайтов для бизнеса. Когда нужен сайт, когда достаточно бота, и почему идеально — оба инструмента вместе.",
        "cta_text": "Посмотреть услуги по разработке",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>Сайт и Telegram-бот: разные инструменты для разных задач</h2>
<p>Многие предприниматели задаются вопросом: что выбрать для бизнеса — сайт или Telegram-бота? На самом деле, это не взаимозаменяемые, а взаимодополняющие инструменты. Понимание их сильных и слабых сторон поможет вам принять правильное решение.</p>
<h2>Сайт — это витрина вашего бизнеса</h2>
<p>Сайт выполняет функцию цифровой витрины. Это место, где потенциальный клиент может подробно изучить ваши услуги, посмотреть портфолио, почитать отзывы, узнать историю компании.</p>
<p>Основные преимущества сайта: SEO и органический трафик, полный контроль над дизайном и брендингом, возможность контекстной рекламы, повышение доверия к бизнесу, полная интеграция с аналитикой.</p>
<h2>Telegram-бот — это коммуникация и автоматизация</h2>
<p>Бот — это не про красивый дизайн, а про удобство взаимодействия. Он работает там, где пользователь уже находится, — в Telegram. Не нужно открывать браузер, вводить адрес, ждать загрузки. Бот всегда под рукой.</p>
<h2>Когда выбрать бота</h2>
<p>Telegram-бот идеален, если ваш бизнес строится на быстрой коммуникации: приём заявок, консультации, запись на услуги, обработка заказов. Если бюджет ограничен и нужно быстро начать получать заявки — начните с бота.</p>
<h2>Когда нужен сайт</h2>
<p>Сайт необходим для комплексного представления бизнеса: портфолио, кейсы, блог, отзывы. Сайт незаменим для контекстной рекламы и SEO-продвижения.</p>
<h2>Идеальная стратегия: и то, и другое</h2>
<p>Максимальный эффект даёт комбинация сайта и бота. Клиент находит ваш сайт через поиск или рекламу, а для быстрой связи переходит в бота. И наоборот: бот обрабатывает запрос, а для детального знакомства отправляет на сайт.</p>"""
    },
    {
        "slug": "sayt-za-5-dney",
        "title": "Сайт за 5 дней — это реально?",
        "date_str": "21 мая 2026",
        "date_iso": "2026-05-21",
        "description": "Реально ли создать сайт за 5 дней? Разбираем сроки разработки: от лендинга до интернет-магазина. Что можно успеть, а что требует больше времени.",
        "cta_text": "Заказать сайт",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>Можно ли создать сайт за 5 дней?</h2>
<p>Короткий ответ: да, если речь идёт о landing page или сайте-визитке. Длинный ответ: всё зависит от сложности проекта, готовности контента и количества правок.</p>
<h2>Что можно успеть за 5 дней: лендинг</h2>
<p>День 1: Дизайн — готовим макет основных блоков. День 2-3: Вёрстка и адаптация под мобильные устройства. День 4: Хостинг и SEO-база — загружаем на хостинг, подключаем домен, SSL, мета-теги. День 5: Финальные тесты и запуск.</p>
<h2>Какие сайты требуют больше времени</h2>
<p>Интернет-магазин — от 2 недель. Корпоративный сайт — от 2 недель. Веб-сервис — от 1 месяца. Сайт с уникальным дизайном — от 2 недель.</p>
<h2>Что влияет на сроки</h2>
<p>Готовность контента, количество правок, интеграции с CRM и платёжными системами.</p>
<h2>Что WebStudio доставляет за 5 дней</h2>
<p>Landing page с современным дизайном, адаптацией под все устройства, базовым SEO, SSL, формой заявки и аналитикой.</p>"""
    },
    {
        "slug": "ai-boty-vozmozhnosti",
        "title": "AI-боты: что они умеют прямо сейчас",
        "date_str": "19 мая 2026",
        "date_iso": "2026-05-19",
        "description": "Современные возможности AI-ботов на нейросетях: распознавание голоса, анализ документов, интеллектуальные диалоги. Как GPT меняет Telegram-ботов.",
        "cta_text": "Заказать GPT-бота",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>AI-боты: эпоха интеллектуальных диалогов</h2>
<p>Искусственный интеллект кардинально меняет возможности чат-ботов. Современные AI-боты понимают естественный язык, анализируют контекст и ведут осмысленный диалог.</p>
<h2>Что умеют AI-боты сегодня</h2>
<h3>Понимание естественного языка (NLP)</h3>
<p>Современные нейросети, такие как GPT, понимают не только команды, но и свободные формулировки. Пользователь может написать «хочу узнать о тарифах» или «расскажите про цены» — бот поймёт оба варианта.</p>
<h3>Распознавание голоса</h3>
<p>AI-боты интегрируются с сервисами распознавания речи (Whisper, Google Speech), что позволяет пользователям отправлять голосовые сообщения. Бот переводит речь в текст и отвечает.</p>
<h3>Анализ документов</h3>
<p>Продвинутые боты могут принимать файлы (PDF, DOCX, изображения), извлекать из них текст и анализировать содержимое. Например, бот может прочитать договор и выделить ключевые условия.</p>
<h2>Применение в бизнесе</h2>
<p>E-commerce: подбор товаров, оформление заказов, поддержка 24/7. Образование: AI-тьюторы объясняют темы, проверяют задания. Консультации: юридические, медицинские, финансовые.</p>
<h2>Как WebStudio интегрирует GPT</h2>
<p>Мы встраиваем большие языковые модели в Telegram-ботов и веб-чаты. Бот получает системный промпт, базу знаний компании и доступ к API.</p>"""
    },
    {
        "slug": "nauchnye-stati-prodazhi",
        "title": "Почему научные статьи продают услуги",
        "date_str": "17 мая 2026",
        "date_iso": "2026-05-17",
        "description": "Как научно-популярный контент повышает доверие к бренду, привлекает целевую аудиторию и демонстрирует экспертизу.",
        "cta_text": "Заказать научную статью",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>Научные статьи как инструмент продаж</h2>
<p>Научно-популярный контент становится одним из самых эффективных инструментов контент-маркетинга для B2B и экспертных ниш. Статьи с научным подходом продают услуги лучше прямой рекламы.</p>
<h2>Доверие — новая валюта маркетинга</h2>
<p>Потребители устали от рекламы. Баннерная слепота, блокировщики, скептицизм — современный клиент не доверяет рекламным обещаниям. Но он доверяет фактам, исследованиям и экспертному мнению.</p>
<h2>Чем научные статьи отличаются от обычных</h2>
<p>Обычные статьи часто поверхностны: «5 советов», «топ-10 инструментов». Научно-популярный подход опирается на данные, исследования, статистику. Он объясняет не «что делать», а «почему это работает».</p>
<h2>В каких нишах работают научные статьи</h2>
<p>IT и разработка, медицина и здоровье, финансы и инвестиции, образование, маркетинг.</p>
<h2>Долгосрочная ценность</h2>
<p>Научно-популярный контент остаётся актуальным долгое время. Он накапливает просмотры, ссылки и упоминания годами. Это вечный актив вашего бренда.</p>"""
    },
    {
        "slug": "5-priznakov-plohogo-sayta",
        "title": "5 признаков плохого сайта",
        "date_str": "15 мая 2026",
        "date_iso": "2026-05-15",
        "description": "Пять признаков, что ваш сайт нуждается в обновлении: медленная загрузка, отсутствие мобильной версии, сложная навигация, нет призыва к действию, устаревший дизайн.",
        "cta_text": "Обновить сайт",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>Как понять, что ваш сайт устарел</h2>
<p>Сайт — это живой инструмент. То, что работало 3 года назад, сегодня может отпугивать клиентов.</p>
<h2>Признак 1: Медленная загрузка</h2>
<p>53% мобильных пользователей покидают сайт, если он грузится дольше 3 секунд. Каждая секунда задержки снижает конверсию на 7%. Проверьте сайт через PageSpeed Insights.</p>
<h2>Признак 2: Отсутствие мобильной версии</h2>
<p>Более 70% трафика приходит с мобильных устройств. Google использует mobile-first indexing.</p>
<h2>Признак 3: Сложная навигация</h2>
<p>Пользователь должен находить нужную информацию за 3 клика. Если меню перегружено — посетители уходят.</p>
<h2>Признак 4: Нет призыва к действию</h2>
<p>На каждой странице должен быть понятный CTA: «Заказать», «Связаться», «Получить консультацию».</p>
<h2>Признак 5: Устаревший дизайн</h2>
<p>Современный тренд: минимализм, крупная типографика, воздух, плавные анимации.</p>"""
    },
    {
        "slug": "kak-vybrat-hosting",
        "title": "Как выбрать хостинг для сайта",
        "date_str": "3 июня 2026",
        "date_iso": "2026-06-03",
        "description": "Гайд по выбору хостинга: сравнение shared-хостинга, VPS и облачных серверов. Критерии выбора, цены и рекомендации.",
        "cta_text": "Посмотреть услуги",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>Хостинг — фундамент вашего сайта</h2>
<p>От качества хостинга зависят скорость загрузки, стабильность работы и безопасность сайта.</p>
<h2>Типы хостинга</h2>
<h3>Shared-хостинг</h3>
<p>Самый доступный вариант от $3-5/мес. Подходит для сайтов-визиток и небольших блогов.</p>
<h3>VPS (Virtual Private Server)</h3>
<p>Гарантированные ресурсы от $10-30/мес. Root-доступ, настройка под свои нужды.</p>
<h3>Облачный хостинг</h3>
<p>Масштабирование и оплата по факту от $15/мес. Высокая отказоустойчивость.</p>
<h3>Выделенный сервер</h3>
<p>Максимальная производительность от $50/мес. Для крупных проектов.</p>
<h2>Ключевые критерии</h2>
<p>Скорость (SSD, расположение сервера), uptime 99.9%, поддержка PHP и MySQL, бесплатный SSL, техподдержка.</p>
<h2>Как WebStudio помогает с хостингом</h2>
<p>Подбираем хостинг под ваш бюджет, настраиваем сервер, SSL, кэширование, CDN.</p>"""
    },
    {
        "slug": "ssl-sertifikat",
        "title": "SSL-сертификат: зачем он нужен сайту",
        "date_str": "3 июня 2026",
        "date_iso": "2026-06-03",
        "description": "Всё о SSL-сертификатах: что это, зачем нужен, как влияет на SEO и доверие. Как получить SSL бесплатно через Let's Encrypt.",
        "cta_text": "Заказать сайт",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>Что такое SSL-сертификат</h2>
<p>SSL (Secure Sockets Layer) шифрует данные между сервером и браузером. Когда сайт имеет SSL, в адресной строке отображается значок замка, а адрес начинается с HTTPS.</p>
<h2>Почему SSL обязателен</h2>
<p>Браузеры помечают сайты без HTTPS как «Не защищён». 85% пользователей не совершают покупки на таких сайтах. Google использует HTTPS как фактор ранжирования.</p>
<h2>Как получить SSL бесплатно</h2>
<p>Let's Encrypt выдаёт бесплатные SSL-сертификаты. На GitHub Pages SSL включается автоматически при подключении кастомного домена.</p>
<h2>Типы SSL-сертификатов</h2>
<p>DV (Domain Validation) — базовый, бесплатный. OV (Organization Validation) — с проверкой компании. EV (Extended Validation) — зелёная строка адреса.</p>
<h2>Как WebStudio настраивает SSL</h2>
<p>SSL — обязательная часть каждого проекта. Настраиваем Let's Encrypt, редирект с HTTP на HTTPS.</p>"""
    },
]

articles_ru.extend([
    {
        "slug": "telegram-kanal-biznes-strategiya",
        "title": "Telegram-канал для бизнеса: стратегия запуска",
        "date_str": "2 июня 2026",
        "date_iso": "2026-06-02",
        "description": "Стратегия запуска Telegram-канала для бизнеса: контент-план, регулярность, продвижение, кросс-промо и автоматизация через бота.",
        "cta_text": "Заказать продвижение",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>Telegram — главный канал для бизнеса в 2026 году</h2>
<p>Telegram — мощная маркетинговая платформа с каналами, ботами, форумами и платежами. По вовлечённости он обгоняет Instagram и Facebook во многих нишах.</p>
<h2>Шаг 1: Определение темы и аудитории</h2>
<p>Канал должен быть узко тематическим. Чем уже ниша, тем легче привлечь лояльную аудиторию.</p>
<h2>Шаг 2: Контент-стратегия и план</h2>
<p>Составьте контент-план на месяц. Определите рубрики: экспертные статьи, кейсы, новости индустрии, короткие советы. Публикуйте 3-5 раз в неделю.</p>
<h2>Шаг 3: Набор первых подписчиков</h2>
<p>Кросс-промо с другими каналами, SEO канала, внешние площадки, таргетированная реклама.</p>
<h2>Шаг 4: Автоматизация через бота</h2>
<p>Модерация, рассылки, сбор заявок, аналитика. Бот экономит время на рутинных операциях.</p>
<h2>Шаг 5: Монетизация</h2>
<p>Для B2B компаний канал работает как воронка, приводящая тёплых клиентов.</p>"""
    },
    {
        "slug": "seo-dlya-nachinayushchikh",
        "title": "SEO для начинающих: с чего начать",
        "date_str": "1 июня 2026",
        "date_iso": "2026-06-01",
        "description": "Пошаговое руководство по SEO для начинающих: настройка Search Console и Вебмастера, мета-теги, структура заголовков, оптимизация скорости.",
        "cta_text": "Заказать SEO-продвижение",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>SEO для начинающих: с чего начать в 2026 году</h2>
<p>Базовые шаги SEO доступны каждому и не требуют большого бюджета.</p>
<h2>Шаг 1: Настройка инструментов</h2>
<p>Зарегистрируйте сайт в Google Search Console и Яндекс.Вебмастер. Отправьте sitemap.xml.</p>
<h2>Шаг 2: Мета-теги title и description</h2>
<p>Каждая страница должна иметь уникальный title и description. Title — самый важный тег для SEO.</p>
<h2>Шаг 3: Структура заголовков</h2>
<p>Используйте иерархию H1-H3. Один H1 на страницу, H2 для разделов, H3 для подразделов.</p>
<h2>Шаг 4: Оптимизация скорости</h2>
<p>Сжимайте изображения, включите кэширование, используйте CDN. Цель — 90+ баллов PageSpeed Insights.</p>
<h2>Шаг 5: Семантическое ядро</h2>
<p>Соберите список ключевых слов, по которым вас будут искать. Используйте Wordstat и Планировщик ключевых слов Google.</p>"""
    },
    {
        "slug": "telegram-bot-avtomatizatsiya-prodazh",
        "title": "Как Telegram-бот может автоматизировать продажи и сбор заявок",
        "date_str": "25 июня 2026",
        "date_iso": "2026-06-25",
        "description": "Telegram-бот для автоматизации продаж: приём заявок, обработка заказов, сбор контактов и платежи. Как настроить автоворонку продаж.",
        "cta_text": "Заказать GPT-бота",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>Telegram-бот как инструмент продаж</h2>
<p>При правильной настройке бот становится полноценной воронкой продаж, работающей 24/7.</p>
<h2>Автоворонка продаж</h2>
<p>Шаг 1: Привлечение. Шаг 2: Знакомство. Шаг 3: Квалификация. Шаг 4: Предложение. Шаг 5: Оплата или заявка. Шаг 6: Фиксация в CRM.</p>
<h2>Сбор контактов и лидогенерация</h2>
<p>Бот собирает номер телефона, email, имя. Контакты сегментируются по интересам.</p>
<h2>Интеграция с CRM</h2>
<p>Bitrix24, AmoCRM, HubSpot. Каждая заявка создаёт карточку лида с историей диалога.</p>
<h2>Приём платежей</h2>
<p>Telegram Stars, ЮKassa, Stripe. Оплата прямо в диалоге повышает конверсию.</p>
<h2>Результаты</h2>
<p>Бизнесы отмечают рост заявок на 30-50% и снижение нагрузки на менеджеров.</p>"""
    },
    {
        "slug": "gpt-boty-obrazovanie-konsultatsii",
        "title": "GPT-боты в образовании и консультациях: реальные кейсы",
        "date_str": "23 июня 2026",
        "date_iso": "2026-06-23",
        "description": "Реальные кейсы использования GPT-ботов в образовании и консультационных проектах.",
        "cta_text": "Заказать GPT-бота",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>GPT-боты меняют образование и консалтинг</h2>
<p>Искусственный интеллект берёт на себя рутинные задачи преподавателей и консультантов.</p>
<h2>Кейс 1: Школа английского — бот-тьютор</h2>
<p>Студенты практикуют диалоги с GPT-ботом. Нагрузка на преподавателей снизилась на 40%, вовлечённость выросла на 60%.</p>
<h2>Кейс 2: Юридическая консультация</h2>
<p>80% вопросов обрабатываются без участия юриста. Время ответа сократилось с 2 часов до 2 минут.</p>
<h2>Кейс 3: Проверка домашних заданий</h2>
<p>GPT проверяет задания по критериям. Время проверки сократилось с 5 дней до 12 часов.</p>
<h2>Техническая реализация</h2>
<p>Системный промпт, база знаний, API внешних сервисов, система эскалации.</p>
<h2>Окупаемость</h2>
<p>30 000-100 000 руб разработка, 2000-8000 руб/мес API. Окупаемость 1-3 месяца.</p>"""
    },
    {
        "slug": "kontent-marketing-telegram-klienty",
        "title": "Как контент-маркетинг приводит клиентов из Telegram",
        "date_str": "20 июня 2026",
        "date_iso": "2026-06-20",
        "description": "Механика привлечения клиентов через Telegram-канал с помощью контент-маркетинга.",
        "cta_text": "Заказать научную статью",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>Telegram — идеальная платформа для контент-маркетинга</h2>
<p>В Telegram каждый подписчик получает ваши посты в хронологическом порядке. Нет алгоритмической ленты.</p>
<h2>Механика: контент продаёт без рекламы</h2>
<p>Публикуете полезный контент — подписчики видят экспертизу и приходят с заказом.</p>
<h2>Регулярность</h2>
<p>3-5 постов в неделю. Контент-план на месяц помогает соблюдать регулярность.</p>
<h2>Форматы контента</h2>
<p>Экспертные статьи, кейсы, инструкции, инфографика, новости с анализом.</p>
<h2>Призыв к действию</h2>
<p>Каждый пост должен заканчиваться CTA. Не обязательно продающим — вовлекающим.</p>"""
    },
    {
        "slug": "5-oshibok-kontent-strategii-telegram",
        "title": "5 ошибок в контент-стратегии Telegram-канала",
        "date_str": "18 июня 2026",
        "date_iso": "2026-06-18",
        "description": "Пять типичных ошибок в контент-стратегии Telegram-канала: расплывчатая тема, редкие посты, отсутствие CTA, игнорирование аналитики, копипаст.",
        "cta_text": "Посмотреть услуги",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>Почему даже хорошие каналы не растут</h2>
<p>Вы публикуете контент, но рост останавливается. Возможно, вы допускаете одну из пяти ошибок.</p>
<h2>Ошибка 1: Расплывчатая тема</h2>
<p>Сегодня про SEO, завтра про кулинарию — подписчики уходят. Определите одну узкую тему.</p>
<h2>Ошибка 2: Редкие посты</h2>
<p>Раз в неделю — про вас забывают. Норма: 3-5 постов в неделю.</p>
<h2>Ошибка 3: Отсутствие CTA</h2>
<p>Пост прочитали, но что делать дальше — непонятно. Добавьте призыв к действию.</p>
<h2>Ошибка 4: Игнорирование аналитики</h2>
<p>Используйте статистику Telegram, отслеживайте охваты и сохранения.</p>
<h2>Ошибка 5: Копипаст без адаптации</h2>
<p>Адаптируйте контент под Telegram. Используйте форматирование, списки, отбивки.</p>"""
    },
    {
        "slug": "formatirovanie-statey-telegram",
        "title": "Как форматировать статьи для Telegram: структура, заголовки, визуал",
        "date_str": "16 июня 2026",
        "date_iso": "2026-06-16",
        "description": "Правила форматирования статей для Telegram: структура, заголовки, визуальное оформление.",
        "cta_text": "Заказать научную статью",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>Статья в Telegram: не просто текст</h2>
<p>Правильное форматирование напрямую влияет на дочитываемость и вовлечённость.</p>
<h2>Структура поста</h2>
<p>Лид (2-3 предложения), подзаголовки через жирный текст, списки, отбивки.</p>
<h2>Оптимальная длина</h2>
<p>1000-2000 знаков. Короче 500 — поверхностно. Длиннее 3000 — теряет дочитываемость.</p>
<h2>Визуал обязателен</h2>
<p>Посты с изображениями получают на 40% больше дочитываний. Инфографика работает лучше стоковых фото.</p>
<h2>Эмодзи как навигация</h2>
<p>3-5 эмодзи на пост для выделения разделов. Не переусердствуйте.</p>
<h2>Адаптация под мобильные</h2>
<p>Короткие абзацы, отступы, короткие ссылки.</p>"""
    },
    {
        "slug": "ekspertnye-stati-prodazhi",
        "title": "Почему экспертные статьи продают услуги лучше, чем реклама",
        "date_str": "14 июня 2026",
        "date_iso": "2026-06-14",
        "description": "Сравнение эффективности экспертных статей и рекламы для привлечения клиентов.",
        "cta_text": "Заказать научную статью",
        "cta_url": "/services.html",
        "has_image": False,
        "content": """<h2>Реклама обещает, статьи доказывают</h2>
<p>Клиент не верит обещаниям. Он верит фактам, кейсам и экспертному мнению.</p>
<h2>Доверие — новая валюта</h2>
<p>Экспертная статья работает как доказательство компетентности. Клиент видит: «Эти ребята разбираются».</p>
<h2>Сравнение: реклама vs статьи</h2>
<p>Реклама: мгновенный эффект, высокая стоимость, низкое доверие. Статьи: долгий разгон, низкая стоимость, высокое доверие, вечный результат.</p>
<h2>Принцип «попробуй перед покупкой»</h2>
<p>Вы даёте часть знаний бесплатно. Если понравилось — клиент придёт за полным объёмом услуг.</p>
<h2>Кейсы, которые продают</h2>
<p>Реальная история проекта с цифрами и результатами — самый убедительный формат.</p>
<h2>Кому подходит</h2>
<p>B2B, профессиональные услуги, сложные продукты. Чем дороже услуга, тем важнее контент-маркетинг.</p>"""
    },
])

articles_en = [
    {
        "slug": "seo-optimization-guide",
        "ru_slug": "seo-optimizatsiya-sayta",
        "title": "What Is SEO and Why It Matters for Your Website",
        "date_str": "May 31, 2026",
        "date_iso": "2026-05-31",
        "description": "Learn what SEO (search engine optimization) is and why your website needs it. Key steps for Google and Yandex promotion.",
        "cta_text": "Order SEO promotion",
        "cta_url": "/en/services.html",
        "has_image": True,
        "img_src": "/images/seo.jpg",
        "img_alt": "SEO optimization: key metrics and tools",
        "content": """<h2>What Is SEO in Simple Words</h2>
<p>SEO (Search Engine Optimization) is a set of measures aimed at improving your website's position in search engine results. It helps your website appear on the first page of Google or Yandex when potential clients search for your products or services.</p>
<p>Without SEO, your website may be beautiful but nobody will find it. Over 70% of users never go past the first search page. If your site isn't in the top 10, you lose up to 90% of potential clients.</p>
<h2>Why SEO Matters for Business</h2>
<p>SEO provides long-term traffic. You pay once for optimization and the traffic keeps coming for years. Organic clicks are more trusted than paid ads.</p>
<h2>Key SEO Components</h2>
<h3>Technical SEO</h3>
<p>Fast loading, mobile responsiveness, clean URL structure, sitemap.xml, SSL certificate.</p>
<h3>On-Page SEO</h3>
<p>Title and meta description tags, H1-H3 heading structure, keywords, optimized images.</p>
<h3>Off-Page SEO</h3>
<p>Link profile — quality and quantity of external sites linking to yours.</p>
<h2>How WebStudio Includes SEO</h2>
<p>Every site we develop is built with search engine requirements from day one.</p>"""
    },
    {
        "slug": "telegram-bot-vs-website",
        "ru_slug": "telegram-bot-ili-sayt",
        "title": "Telegram Bot or Website: What to Choose for Business",
        "date_str": "May 30, 2026",
        "date_iso": "2026-05-30",
        "description": "Comparison of Telegram bots vs websites for business. When you need a website, when a bot is enough, and why both together is ideal.",
        "cta_text": "View development services",
        "cta_url": "/en/services.html",
        "has_image": False,
        "content": """<h2>Different Tools for Different Tasks</h2>
<p>A website and a Telegram bot are complementary tools. Understanding their strengths helps you decide.</p>
<h2>Website — Your Storefront</h2>
<p>A digital storefront for portfolios, testimonials, detailed service descriptions. Full control over branding, SEO traffic, advertising.</p>
<h2>Telegram Bot — Communication and Automation</h2>
<p>A bot works where users already are — inside Telegram. Launched in 1-3 days, costs less, offers instant responses and automation 24/7.</p>
<h2>When to Choose a Bot</h2>
<p>Fast lead capture, consultations, appointment booking, limited budget.</p>
<h2>When You Need a Website</h2>
<p>Comprehensive business representation, SEO, large catalogs, paid ads.</p>
<h2>The Ideal Strategy</h2>
<p>Combine both: website attracts via search, bot converts via instant communication.</p>"""
    },
    {
        "slug": "website-in-5-days",
        "ru_slug": "sayt-za-5-dney",
        "title": "A Website in 5 Days — Is It Real?",
        "date_str": "May 21, 2026",
        "date_iso": "2026-05-21",
        "description": "Is it realistic to create a website in 5 days? We break down development timelines from landing pages to online stores.",
        "cta_text": "Order a website",
        "cta_url": "/en/services.html",
        "has_image": False,
        "content": """<h2>Can a Website Be Built in 5 Days?</h2>
<p>Yes, for a landing page. It depends on complexity, content readiness, and revision count.</p>
<h2>5-Day Landing Page Process</h2>
<p>Day 1: Design. Days 2-3: Development and mobile adaptation. Day 4: Hosting, SSL, SEO basics. Day 5: Testing and launch.</p>
<h2>Which Sites Take Longer</h2>
<p>E-commerce: 2+ weeks. Corporate sites: 2+ weeks. SaaS: 1+ month.</p>
<h2>What Affects Timeline</h2>
<p>Content readiness, revision count, integrations with CRM and payment systems.</p>
<h2>What WebStudio Delivers in 5 Days</h2>
<p>Landing page with modern design, mobile adaptation, SEO, SSL, contact form, analytics.</p>"""
    },
    {
        "slug": "ai-bots-capabilities",
        "ru_slug": "ai-boty-vozmozhnosti",
        "title": "AI Bots: What They Can Do Right Now",
        "date_str": "May 19, 2026",
        "date_iso": "2026-05-19",
        "description": "Modern capabilities of AI-powered bots: voice recognition, document analysis, intelligent conversations.",
        "cta_text": "Order a GPT bot",
        "cta_url": "/en/services.html",
        "has_image": False,
        "content": """<h2>AI Bots: The Era of Intelligent Conversations</h2>
<p>Modern AI bots understand natural language, analyze context, and hold meaningful conversations.</p>
<h2>What AI Bots Can Do</h2>
<h3>Natural Language Understanding</h3>
<p>GPT understands free-form language. No rigid commands needed.</p>
<h3>Voice Recognition</h3>
<p>Convert speech to text via Whisper or Google Speech.</p>
<h3>Document Analysis</h3>
<p>Read PDF, DOCX, images — extract and analyze content.</p>
<h3>Personalization</h3>
<p>Remember history and preferences. Recommend products.</p>
<h2>Business Applications</h2>
<p>E-commerce, education, consulting, customer support.</p>
<h2>How WebStudio Integrates GPT</h2>
<p>System prompt, knowledge base, API access. Meaningful conversations that solve real problems.</p>"""
    },
    {
        "slug": "science-articles-sell",
        "ru_slug": "nauchnye-stati-prodazhi",
        "title": "Why Science Articles Sell Services",
        "date_str": "May 17, 2026",
        "date_iso": "2026-05-17",
        "description": "How science content builds brand trust, attracts target audience and demonstrates expertise.",
        "cta_text": "Order a science article",
        "cta_url": "/en/services.html",
        "has_image": False,
        "content": """<h2>Science as a Sales Tool</h2>
<p>Science-backed content is one of the most effective content marketing tools for B2B and expert niches.</p>
<h2>Trust Is the New Currency</h2>
<p>Consumers trust facts, research, and expert opinions — not ads.</p>
<h2>What Makes Science Content Different</h2>
<p>Deep research, data, statistics. Explains not just what but why.</p>
<h2>Where It Works Best</h2>
<p>IT, healthcare, finance, education, marketing.</p>
<h2>Long-Term Value</h2>
<p>Evergreen content stays relevant for years, accumulates views and backlinks.</p>"""
    },
    {
        "slug": "5-signs-bad-website",
        "ru_slug": "5-priznakov-plohogo-sayta",
        "title": "5 Signs of a Bad Website",
        "date_str": "May 15, 2026",
        "date_iso": "2026-05-15",
        "description": "Five signs your website needs an update: slow loading, no mobile version, complex navigation, no CTA, outdated design.",
        "cta_text": "Update your website",
        "cta_url": "/en/services.html",
        "has_image": False,
        "content": """<h2>How to Tell Your Website Is Outdated</h2>
<p>If you notice at least two signs, it's time for an update.</p>
<h2>1. Slow Loading</h2>
<p>53% of users leave if it takes over 3 seconds. Each second delay reduces conversion by 7%.</p>
<h2>2. No Mobile Version</h2>
<p>Over 70% of traffic is mobile. Google uses mobile-first indexing.</p>
<h2>3. Complex Navigation</h2>
<p>Users should find what they need in 3 clicks.</p>
<h2>4. No Call to Action</h2>
<p>Every page needs a clear CTA: Order, Contact, Get Consultation.</p>
<h2>5. Outdated Design</h2>
<p>Modern trends: minimalism, large typography, whitespace, smooth animations.</p>"""
    },
    {
        "slug": "how-to-choose-hosting",
        "ru_slug": "kak-vybrat-hosting",
        "title": "How to Choose Hosting for Your Website",
        "date_str": "June 3, 2026",
        "date_iso": "2026-06-03",
        "description": "Hosting selection guide: comparison of shared hosting, VPS and cloud servers. Selection criteria and recommendations.",
        "cta_text": "View services",
        "cta_url": "/en/services.html",
        "has_image": False,
        "content": """<h2>Hosting — The Foundation</h2>
<p>Hosting affects loading speed, stability, and security.</p>
<h2>Types of Hosting</h2>
<h3>Shared Hosting</h3>
<p>$3-5/month. Suitable for small sites and blogs.</p>
<h3>VPS</h3>
<p>$10-30/month. Guaranteed resources, root access.</p>
<h3>Cloud Hosting</h3>
<p>From $15/month. Scalable, pay per use.</p>
<h3>Dedicated Server</h3>
<p>$50+/month. Maximum performance for large projects.</p>
<h2>Key Criteria</h2>
<p>Speed, uptime 99.9%, PHP/MySQL support, free SSL, support quality.</p>"""
    },
    {
        "slug": "ssl-certificate-guide",
        "ru_slug": "ssl-sertifikat",
        "title": "SSL Certificate: Why Your Website Needs It",
        "date_str": "June 3, 2026",
        "date_iso": "2026-06-03",
        "description": "Everything about SSL certificates: what they are, why you need one, how they affect SEO and visitor trust.",
        "cta_text": "Order a website",
        "cta_url": "/en/services.html",
        "has_image": False,
        "content": """<h2>What Is an SSL Certificate</h2>
<p>SSL encrypts data between server and browser. Shows a padlock icon in the address bar.</p>
<h2>Why SSL Is Mandatory</h2>
<p>Browsers mark HTTP sites as "Not secure". Google uses HTTPS as a ranking factor. 85% of users avoid purchasing on non-HTTPS sites.</p>
<h2>Get SSL for Free</h2>
<p>Let's Encrypt offers free certificates. GitHub Pages provides automatic SSL for custom domains.</p>
<h2>SSL Types</h2>
<p>DV (free), OV (company verified), EV (green address bar). DV is enough for most sites.</p>"""
    },
    {
        "slug": "telegram-channel-strategy",
        "ru_slug": "telegram-kanal-biznes-strategiya",
        "title": "Telegram Channel for Business: Launch Strategy",
        "date_str": "June 2, 2026",
        "date_iso": "2026-06-02",
        "description": "Telegram channel launch strategy: content plan, consistency, promotion, cross-promotion and bot automation.",
        "cta_text": "Order promotion",
        "cta_url": "/en/services.html",
        "has_image": False,
        "content": """<h2>Telegram for Business</h2>
<p>Telegram surpasses Instagram and Facebook in engagement for many niches.</p>
<h2>Step 1: Define Your Topic</h2>
<p>Narrow focus. "B2B marketing for IT" works better than "everything about business".</p>
<h2>Step 2: Content Plan</h2>
<p>Monthly calendar. Mix articles, cases, news, tips. Post 3-5 times per week.</p>
<h2>Step 3: Get Subscribers</h2>
<p>Cross-promotion, channel SEO, external platforms, targeted ads.</p>
<h2>Step 4: Automate with a Bot</h2>
<p>Moderation, welcome messages, lead collection, analytics.</p>
<h2>Step 5: Monetize</h2>
<p>A channel works as a sales funnel bringing warm clients.</p>"""
    },
    {
        "slug": "seo-for-beginners",
        "ru_slug": "seo-dlya-nachinayushchikh",
        "title": "SEO for Beginners: Where to Start",
        "date_str": "June 1, 2026",
        "date_iso": "2026-06-01",
        "description": "Step-by-step SEO guide: setting up Search Console, meta tags, heading structure, speed optimization, semantic core.",
        "cta_text": "Order SEO promotion",
        "cta_url": "/en/services.html",
        "has_image": False,
        "content": """<h2>SEO for Beginners in 2026</h2>
<p>Basic SEO steps are accessible to everyone.</p>
<h2>Step 1: Webmaster Tools</h2>
<p>Google Search Console and Bing Webmaster Tools. Submit sitemap.xml.</p>
<h2>Step 2: Meta Tags</h2>
<p>Unique title and description for every page.</p>
<h2>Step 3: Heading Structure</h2>
<p>Use H1-H3 hierarchy. One H1 per page.</p>
<h2>Step 4: Speed Optimization</h2>
<p>Compress images, enable caching, use CDN. Aim for 90+ PageSpeed score.</p>
<h2>Step 5: Keyword Research</h2>
<p>Build a semantic core with Wordstat and Google Keyword Planner.</p>"""
    },
]

def main():
    blog_dir = os.path.join(BASE, "blog")
    en_blog_dir = os.path.join(BASE, "en", "blog")
    os.makedirs(blog_dir, exist_ok=True)
    os.makedirs(en_blog_dir, exist_ok=True)

    count = 0

    # Generate RU articles
    for art in articles_ru:
        html = ru_article(**art)
        fpath = os.path.join(blog_dir, f"{art['slug']}.html")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
        print(f"  [RU] {fpath}")

    # Generate EN articles
    for art in articles_en:
        html = en_article(**art)
        fpath = os.path.join(en_blog_dir, f"{art['slug']}.html")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
        print(f"  [EN] {fpath}")

    print(f"\nTotal files generated: {count}")

if __name__ == "__main__":
    main()
