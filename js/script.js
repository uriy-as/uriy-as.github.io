// Burger menu
const burger = document.getElementById('burger');
const nav = document.getElementById('nav');

burger.addEventListener('click', () => {
    nav.classList.toggle('nav--open');
});

document.querySelectorAll('.nav a').forEach(link => {
    link.addEventListener('click', () => {
        nav.classList.remove('nav--open');
    });
});

// Scroll reveal
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.15 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// Counter animation
const counters = document.querySelectorAll('.stats__num');

const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const el = entry.target;
            const target = +el.dataset.target;
            const duration = 1500;
            const step = target / (duration / 16);
            let current = 0;

            const update = () => {
                current += step;
                if (current < target) {
                    el.textContent = Math.round(current) + '+';
                    requestAnimationFrame(update);
                } else {
                    el.textContent = target + '+';
                }
            };

            update();
            counterObserver.unobserve(el);
        }
    });
}, { threshold: 0.5 });

counters.forEach(el => counterObserver.observe(el));

// Modal
const form = document.getElementById('contactForm');
const modal = document.getElementById('modal');
const modalClose = document.getElementById('modalClose');

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const data = {
        name: form.querySelector('[name="name"]').value,
        email: form.querySelector('[name="email"]').value,
        phone: form.querySelector('[name="phone"]').value,
        message: form.querySelector('[name="message"]').value
    };
    fetch('https://Astap.pythonanywhere.com/api/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        mode: 'cors'
    }).catch(() => {});
    modal.classList.add('modal--open');
    form.reset();
});

modalClose.addEventListener('click', () => {
    modal.classList.remove('modal--open');
});

modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.remove('modal--open');
    }
});

// Modal

// Visit tracker
(function() {
    const PA_URL = 'https://Astap.pythonanywhere.com/visit';
    const data = {
        page: window.location.pathname,
        ref: document.referrer || ''
    };
    try {
        fetch(PA_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
            mode: 'cors'
        }).catch(() => {});
    } catch(e) {}
})();

// Chat widget
(function() {
    const btn = document.getElementById('chatBtn');
    const popup = document.getElementById('chatPopup');
    const close = document.getElementById('chatClose');
    const body = document.getElementById('chatBody');
    const form = document.getElementById('chatForm');
    const input = form ? form.querySelector('input') : null;

    if (!btn || !popup || !close || !body || !form || !input) return;

    btn.addEventListener('click', () => {
        popup.classList.toggle('chat-popup--open');
    });

    close.addEventListener('click', () => {
        popup.classList.remove('chat-popup--open');
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const msg = input.value.trim();
        if (!msg) return;

        input.value = '';
        body.innerHTML += `<div class="chat-msg chat-msg--user">${escapeHtml(msg)}</div>`;
        body.scrollTop = body.scrollHeight;

        body.innerHTML += `<div class="chat-msg chat-msg--bot"><em>РџРµС‡Р°С‚Р°РµС‚...</em></div>`;
        body.scrollTop = body.scrollHeight;

        try {
            const r = await fetch('https://Astap.pythonanywhere.com/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msg }),
                mode: 'cors'
            });
            const data = await r.json();
            body.removeChild(body.lastChild);
            body.innerHTML += `<div class="chat-msg chat-msg--bot">${escapeHtml(data.reply)}</div>`;

            if (data.reply.includes('Р·Р°РїСЂРѕСЃ РїРµСЂРµРґР°РЅ')) {
                fetch('https://Astap.pythonanywhere.com/api/lead', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: msg }),
                    mode: 'cors'
                }).catch(() => {});
            }
        } catch(e) {
            body.removeChild(body.lastChild);
            body.innerHTML += `<div class="chat-msg chat-msg--bot">${document.querySelector('[data-i18n="chat-error"]').innerHTML}</div>`;
        }
        body.scrollTop = body.scrollHeight;
    });

    function escapeHtml(text) {
        const d = document.createElement('div');
        d.textContent = text;
        return d.innerHTML;
    }
})();

// Language switcher
(function() {
    const LANG_KEY = 'site_lang';
    let lang = localStorage.getItem(LANG_KEY) || 'ru';

    const translations = {
        'nav-services': { ru: 'РЈСЃР»СѓРіРё', en: 'Services' },
        'nav-about': { ru: 'Рћ РЅР°СЃ', en: 'About' },
        'nav-articles': { ru: 'РЎС‚Р°С‚СЊРё', en: 'Articles' },
        'nav-contacts': { ru: 'РљРѕРЅС‚Р°РєС‚С‹', en: 'Contacts' },
        'nav-chat': { ru: 'AI-С‡Р°С‚', en: 'AI Chat' },
        'hero-badge': { ru: 'Р’Р°С€ С†РёС„СЂРѕРІРѕР№ РїР°СЂС‚РЅС‘СЂ', en: 'Your Digital Partner' },
        'hero-title': { ru: 'РЎРѕР·РґР°С‘Рј С†РёС„СЂРѕРІС‹Рµ РїСЂРѕРґСѓРєС‚С‹ <span class="gradient-text">РґР»СЏ РІР°С€РµРіРѕ Р±РёР·РЅРµСЃР°</span>', en: 'We create digital products <span class="gradient-text">for your business</span>' },
        'hero-subtitle': { ru: 'Р’РµР±-СЃР°Р№С‚С‹, С‡Р°С‚-Р±РѕС‚С‹ Рё Telegram-РєР°РЅР°Р»С‹ СЃ РЅР°СѓС‡РЅС‹Рј РєРѕРЅС‚РµРЅС‚РѕРј вЂ” РїРѕРґ РєР»СЋС‡', en: 'Websites, chatbots, and Telegram channels with science content вЂ” turnkey' },
        'hero-btn-contact': { ru: 'РЎРІСЏР·Р°С‚СЊСЃСЏ СЃ РЅР°РјРё', en: 'Contact us' },
        'hero-btn-services': { ru: 'РќР°С€Рё СѓСЃР»СѓРіРё', en: 'Our services' },
        'section-services': { ru: 'РќР°С€Рё СѓСЃР»СѓРіРё', en: 'Our Services' },
        'service-site': { ru: 'РЎРѕР·РґР°РЅРёРµ СЃР°Р№С‚РѕРІ', en: 'Website Development' },
        'service-site-desc': { ru: 'Р Р°Р·СЂР°Р±РѕС‚РєР° СЃР°Р№С‚РѕРІ Р»СЋР±РѕР№ СЃР»РѕР¶РЅРѕСЃС‚Рё: РѕС‚ Р»РµРЅРґРёРЅРіРѕРІ РґРѕ РёРЅС‚РµСЂРЅРµС‚-РјР°РіР°Р·РёРЅРѕРІ. РђРґР°РїС‚РёРІРЅС‹Р№ РґРёР·Р°Р№РЅ, SEO-РѕРїС‚РёРјРёР·Р°С†РёСЏ, РІС‹СЃРѕРєР°СЏ СЃРєРѕСЂРѕСЃС‚СЊ Р·Р°РіСЂСѓР·РєРё.', en: 'Development of websites of any complexity: from landing pages to online stores. Responsive design, SEO optimization, fast loading.' },
        'service-bot': { ru: 'Р§Р°С‚-Р±РѕС‚С‹', en: 'Chatbots' },
        'service-bot-desc': { ru: 'РРЅС‚РµР»Р»РµРєС‚СѓР°Р»СЊРЅС‹Рµ Telegram-Р±РѕС‚С‹ РЅР° Р±Р°Р·Рµ AI РґР»СЏ РїРѕРґРґРµСЂР¶РєРё РєР»РёРµРЅС‚РѕРІ, РїСЂРѕРґР°Р¶, СЃР±РѕСЂР° Р·Р°СЏРІРѕРє Рё Р°РІС‚РѕРјР°С‚РёР·Р°С†РёРё СЂСѓС‚РёРЅС‹.', en: 'AI-powered Telegram bots for customer support, sales, lead collection, and routine automation.' },
        'service-articles': { ru: 'РќР°СѓС‡РЅС‹Рµ СЃС‚Р°С‚СЊРё РґР»СЏ Telegram', en: 'Science Articles for Telegram' },
        'service-articles-desc': { ru: 'РљР°С‡РµСЃС‚РІРµРЅРЅС‹Рµ РЅР°СѓС‡РЅРѕ-РїРѕРїСѓР»СЏСЂРЅС‹Рµ СЃС‚Р°С‚СЊРё, Р°РґР°РїС‚РёСЂРѕРІР°РЅРЅС‹Рµ РґР»СЏ Telegram-РєР°РЅР°Р»РѕРІ. Р“Р»СѓР±РѕРєРёР№ Р°РЅР°Р»РёР·, СѓРЅРёРєР°Р»СЊРЅС‹Р№ РєРѕРЅС‚РµРЅС‚, РІРѕРІР»РµРєР°СЋС‰РёР№ С„РѕСЂРјР°С‚.', en: 'High-quality science articles adapted for Telegram channels. Deep analysis, unique content, engaging format.' },
        'section-about': { ru: 'РџРѕС‡РµРјСѓ РјС‹?', en: 'Why Us?' },
        'about-individual': { ru: 'РРЅРґРёРІРёРґСѓР°Р»СЊРЅС‹Р№ РїРѕРґС…РѕРґ', en: 'Individual Approach' },
        'about-individual-desc': { ru: '100% СѓРЅРёРєР°Р»СЊРЅРѕРµ СЂРµС€РµРЅРёРµ РїРѕРґ Р·Р°РґР°С‡Рё РІР°С€РµРіРѕ Р±РёР·РЅРµСЃР°', en: '100% unique solution for your business needs' },
        'about-tech': { ru: 'РЎРѕРІСЂРµРјРµРЅРЅС‹Рµ С‚РµС…РЅРѕР»РѕРіРёРё', en: 'Modern Technologies' },
        'about-tech-desc': { ru: 'РђРєС‚СѓР°Р»СЊРЅС‹Р№ СЃС‚РµРє Рё Р»СѓС‡С€РёРµ РїСЂР°РєС‚РёРєРё СЂР°Р·СЂР°Р±РѕС‚РєРё', en: 'Cutting-edge stack and best development practices' },
        'about-support': { ru: 'РџРѕРґРґРµСЂР¶РєР° 24/7', en: '24/7 Support' },
        'about-support-desc': { ru: 'Р’СЃРµРіРґР° РЅР° СЃРІСЏР·Рё РґРѕ Рё РїРѕСЃР»Рµ СЃРґР°С‡Рё РїСЂРѕРµРєС‚Р°', en: 'Always in touch before and after project delivery' },
        'tg-widget-title': { ru: 'РџРѕСЃР»РµРґРЅРёРµ РїРѕСЃС‚С‹ РєР°РЅР°Р»Р°', en: 'Latest Channel Posts' },
        'tg-widget-subtitle': { ru: 'РџРѕРґРїРёС€РёС‚РµСЃСЊ, С‡С‚РѕР±С‹ РЅРµ РїСЂРѕРїСѓСЃРєР°С‚СЊ РїРѕР»РµР·РЅС‹Р№ РєРѕРЅС‚РµРЅС‚', en: 'Subscribe so you don\'t miss useful content' },
        'tg-widget-all': { ru: 'Р’СЃРµ РїРѕСЃС‚С‹ РІ РєР°РЅР°Р»Рµ', en: 'All posts in channel' },
        'stats-projects': { ru: 'Р—Р°РІРµСЂС€С‘РЅРЅС‹С… РїСЂРѕРµРєС‚РѕРІ', en: 'Completed Projects' },
        'stats-clients': { ru: 'РђРєС‚РёРІРЅС‹С… РєР»РёРµРЅС‚РѕРІ', en: 'Active Clients' },
        'stats-years': { ru: 'Р›РµС‚ РЅР° СЂС‹РЅРєРµ', en: 'Years on Market' },
        'stats-satisfaction': { ru: '% РґРѕРІРѕР»СЊРЅС‹С… РєР»РёРµРЅС‚РѕРІ', en: '% Satisfied Clients' },
        'tg-promo-title': { ru: 'РџРѕРґРїРёС€РёС‚РµСЃСЊ РЅР° РЅР°С€ Telegram-РєР°РЅР°Р»', en: 'Subscribe to our Telegram Channel' },
        'tg-promo-desc': { ru: 'РљРµР№СЃС‹, СЃС‚Р°С‚СЊРё Рё РёРЅСЃР°Р№С‚С‹ РїРѕ СЂР°Р·СЂР°Р±РѕС‚РєРµ СЃР°Р№С‚РѕРІ, Telegram-Р±РѕС‚РѕРІ Рё РєРѕРЅС‚РµРЅС‚-РјР°СЂРєРµС‚РёРЅРіСѓ. РџСѓР±Р»РёРєСѓРµРј РїРѕР»РµР·РЅС‹Р№ РєРѕРЅС‚РµРЅС‚ РєР°Р¶РґС‹Р№ РїРѕРЅРµРґРµР»СЊРЅРёРє, СЃСЂРµРґСѓ, РїСЏС‚РЅРёС†Сѓ Рё СЃСѓР±Р±РѕС‚Сѓ РІ 08:10.', en: 'Cases, articles and insights on website development, Telegram bots and content marketing. We publish useful content every Monday, Wednesday, Friday and Saturday at 08:10.' },
        'tg-promo-btn': { ru: 'РџРѕРґРїРёСЃР°С‚СЊСЃСЏ РІ Telegram', en: 'Subscribe on Telegram' },
        'contact-title': { ru: 'РЎРІСЏР¶РёС‚РµСЃСЊ СЃ РЅР°РјРё', en: 'Contact Us' },
        'contact-subtitle': { ru: 'РћСЃС‚Р°РІСЊС‚Рµ Р·Р°СЏРІРєСѓ, Рё РјС‹ РѕР±СЃСѓРґРёРј РІР°С€ РїСЂРѕРµРєС‚', en: 'Leave a request and we\'ll discuss your project' },
        'form-name': { ru: 'Р’Р°С€Рµ РёРјСЏ', en: 'Your name' },
        'form-email': { ru: 'Email', en: 'Email' },
        'form-phone': { ru: 'Р’Р°С€ С‚РµР»РµС„РѕРЅ / РµСЃР»Рё С‚СЂРµР±СѓРµС‚СЃСЏ СЃРєРѕСЂРѕСЃС‚СЊ', en: 'Your phone / if speed matters' },
        'form-message': { ru: 'РћРїРёС€РёС‚Рµ РІР°С€ РїСЂРѕРµРєС‚', en: 'Describe your project' },
        'form-submit': { ru: 'РћС‚РїСЂР°РІРёС‚СЊ Р·Р°СЏРІРєСѓ', en: 'Send request' },
        'contact-email': { ru: 'uriy.as59@yandex.com', en: 'uriy.as59@yandex.com' },
        'contact-tg': { ru: 'Telegram', en: 'Telegram' },
        'footer-copyright': { ru: 'В© 2026 WebStudio. Р’СЃРµ РїСЂР°РІР° Р·Р°С‰РёС‰РµРЅС‹.', en: 'В© 2026 WebStudio. All rights reserved.' },
        'footer-bot': { ru: '@NevWebStudio_bot вЂ” Р±РѕС‚ РѕС‚РІРµС‚РёС‚ РЅР° РІСЃРµ РёРЅС‚РµСЂРµСЃСѓСЋС‰РёРµ РІРѕРїСЂРѕСЃС‹', en: '@NevWebStudio_bot вЂ” the bot will answer all your questions' },
        'modal-thanks': { ru: 'РЎРїР°СЃРёР±Рѕ! РњС‹ СЃРІСЏР¶РµРјСЃСЏ СЃ РІР°РјРё РІ Р±Р»РёР¶Р°Р№С€РµРµ РІСЂРµРјСЏ.', en: 'Thank you! We will contact you shortly.' },
        'modal-btn': { ru: 'РћС‚Р»РёС‡РЅРѕ', en: 'Great' },
        'tg-float-text': { ru: 'Telegram', en: 'Telegram' },
        'chat-btn-text': { ru: 'AI-С‡Р°С‚', en: 'AI Chat' },
        'chat-title': { ru: 'Р§Р°С‚ СЃ WebStudio AI', en: 'Chat with WebStudio AI' },
        'chat-greeting': { ru: 'Р—РґСЂР°РІСЃС‚РІСѓР№С‚Рµ! Р—Р°РґР°Р№С‚Рµ РІР°С€ РІРѕРїСЂРѕСЃ.', en: 'Hello! Ask your question.' },
        'chat-placeholder': { ru: 'Р’Р°С€Рµ СЃРѕРѕР±С‰РµРЅРёРµ...', en: 'Your message...' },
        'chat-error': { ru: 'РћС€РёР±РєР° СЃРІСЏР·Рё. РџРѕРїСЂРѕР±СѓР№С‚Рµ РїРѕР·Р¶Рµ.', en: 'Connection error. Try again later.' },
        'article-hero-title': { ru: 'РџРѕР»РµР·РЅС‹Рµ СЃС‚Р°С‚СЊРё', en: 'Useful Articles' },
        'article-hero-subtitle': { ru: 'РљРµР№СЃС‹, СЃРѕРІРµС‚С‹ Рё РёРЅСЃС‚СЂСѓРєС†РёРё РїРѕ СЃРѕР·РґР°РЅРёСЋ СЃР°Р№С‚РѕРІ, Р±РѕС‚РѕРІ Рё РєРѕРЅС‚РµРЅС‚Р°', en: 'Cases, tips and guides on creating websites, bots and content' },
        'article-share-tg': { ru: 'Telegram', en: 'Telegram' },
        'article-share-email': { ru: 'Email', en: 'Email' },
        'service-hero-title': { ru: 'РќР°С€Рё СѓСЃР»СѓРіРё', en: 'Our Services' },
        'service-hero-subtitle': { ru: 'Р Р°Р·СЂР°Р±РѕС‚РєР° РїРѕРґ РєР»СЋС‡ вЂ” РѕС‚ РёРґРµРё РґРѕ РіРѕС‚РѕРІРѕРіРѕ РїСЂРѕРґСѓРєС‚Р°', en: 'Turnkey development вЂ” from idea to finished product' },
        'service-banner': { ru: 'рџЋ‰ РђРєС†РёСЏ: СЃРєРёРґРєР° 30% РґР»СЏ РїРµСЂРІС‹С… 5 РєР»РёРµРЅС‚РѕРІ! РЈСЃРїРµР№С‚Рµ Р·Р°РєР°Р·Р°С‚СЊ РїРѕ СЃС‚Р°СЂРѕР№ С†РµРЅРµ', en: 'рџЋ‰ Promo: 30% off for the first 5 customers! Order now at the old price' },
        'service-card-order': { ru: 'Р—Р°РєР°Р·Р°С‚СЊ', en: 'Order' },

        'service-card-visit': { ru: 'РЎР°Р№С‚-РІРёР·РёС‚РєР°', en: 'Business Card Website' },
        'service-card-visit-desc': { ru: 'РљРѕРјРїР°РєС‚РЅС‹Р№ СЃР°Р№С‚ РґР»СЏ РїСЂРµРґСЃС‚Р°РІР»РµРЅРёСЏ Р±РёР·РЅРµСЃР°', en: 'Compact website for business presentation' },
        'service-card-full': { ru: 'РЎР°Р№С‚ РїРѕРґ РєР»СЋС‡', en: 'Full Website' },
        'service-card-full-desc': { ru: 'Landing page, РёРЅС‚РµСЂРЅРµС‚-РјР°РіР°Р·РёРЅ, РєРѕСЂРїРѕСЂР°С‚РёРІРЅС‹Р№ СЃР°Р№С‚', en: 'Landing page, online store, corporate website' },
        'service-card-bot-simple': { ru: 'Р‘РѕС‚-РІРёР·РёС‚РєР°', en: 'Business Card Bot' },
        'service-card-bot-simple-desc': { ru: 'РџСЂРѕСЃС‚РѕР№ Telegram-Р±РѕС‚ РґР»СЏ СЃРІСЏР·Рё СЃ РєР»РёРµРЅС‚Р°РјРё', en: 'Simple Telegram bot for client communication' },
        'service-card-bot-gpt': { ru: 'Telegram-Р±РѕС‚ РЅР° GPT', en: 'GPT Telegram Bot' },
        'service-card-bot-gpt-desc': { ru: 'Р§Р°С‚-Р±РѕС‚ СЃ РЅРµР№СЂРѕСЃРµС‚СЊСЋ, РїСЂРёС‘Рј Р·Р°СЏРІРѕРє Рё РѕРїР»Р°С‚', en: 'Chatbot with neural network, order and payment processing' },
        'service-card-articles': { ru: 'РќР°СѓС‡РЅС‹Рµ СЃС‚Р°С‚СЊРё', en: 'Science Articles' },
        'service-card-articles-desc': { ru: 'РўРµРјР°С‚РёС‡РµСЃРєРёР№ РєРѕРЅС‚РµРЅС‚ РґР»СЏ Telegram Рё СЃРѕС†СЃРµС‚РµР№', en: 'Thematic content for Telegram and social media' },
        'service-card-promo': { ru: 'РџСЂРѕРґРІРёР¶РµРЅРёРµ', en: 'Promotion' },
        'service-card-promo-desc': { ru: 'SEO, РЇРЅРґРµРєСЃ.РњРµС‚СЂРёРєР°, СЂР°СЃРєСЂСѓС‚РєР° РєР°РЅР°Р»Р°', en: 'SEO, Yandex Metrica, channel promotion' },
        'service-promo-msg': { ru: 'рџ’° Р¦РµРЅС‹ СѓРєР°Р·Р°РЅС‹ РІ USD. Р’РѕР·РјРѕР¶РЅР° РѕРїР»Р°С‚Р° РІ СЂСѓР±Р»СЏС…, EUR, USDT, РєСЂРёРїС‚РѕРІР°Р»СЋС‚Рµ вЂ” РїРѕ РєСѓСЂСЃСѓ РЅР° РґРµРЅСЊ СЃРґРµР»РєРё.<br>рџЋЇ <strong>РЎРєРёРґРєР° 30%</strong> РґР»СЏ РїРµСЂРІС‹С… 5 Р·Р°РєР°Р·С‡РёРєРѕРІ. Р’РёР·РёС‚РєР° РѕС‚ $105, Р±РѕС‚ РѕС‚ $42, СЃС‚Р°С‚СЊСЏ РѕС‚ $21 вЂ” СѓСЃРїРµР№С‚Рµ!<br>рџ“© РЎРІСЏР¶РёС‚РµСЃСЊ СЃ РЅР°РјРё РІ Telegram: <a href="https://t.me/webstudio_chanel" style="color:var(--accent);">@webstudio_chanel</a>', en: 'рџ’° Prices in USD. Payment in RUB, EUR, USDT, crypto вЂ” at the exchange rate on the deal date.<br>рџЋЇ <strong>30% discount</strong> for the first 5 customers. Business card from $105, bot from $42, article from $21 вЂ” hurry up!<br>рџ“© Contact us on Telegram: <a href="https://t.me/webstudio_chanel" style="color:var(--accent);">@webstudio_chanel</a>' },
        'price-from': { ru: 'РѕС‚', en: 'from' },
        'price-project': { ru: 'Р·Р° РїСЂРѕРµРєС‚', en: 'per project' },
        'price-article': { ru: 'Р·Р° СЃС‚Р°С‚СЊСЋ', en: 'per article' },
        'price-month': { ru: 'Р·Р° РјРµСЃСЏС†', en: 'per month' },
        'svc-visit-l1': { ru: '1вЂ“3 СЃС‚СЂР°РЅРёС†С‹ (РіР»Р°РІРЅР°СЏ, СѓСЃР»СѓРіРё, РєРѕРЅС‚Р°РєС‚С‹)', en: '1вЂ“3 pages (home, services, contacts)' },
        'svc-visit-l2': { ru: 'РЈРЅРёРєР°Р»СЊРЅС‹Р№ РґРёР·Р°Р№РЅ РїРѕРґ РІР°С€ Р±СЂРµРЅРґ', en: 'Unique design for your brand' },
        'svc-visit-l3': { ru: 'РђРґР°РїС‚Р°С†РёСЏ РїРѕРґ С‚РµР»РµС„РѕРЅ Рё РїР»Р°РЅС€РµС‚', en: 'Mobile and tablet adaptation' },
        'svc-visit-l4': { ru: 'Р¤РѕСЂРјР° РѕР±СЂР°С‚РЅРѕР№ СЃРІСЏР·Рё', en: 'Contact form' },
        'svc-visit-l5': { ru: 'SEO-Р±Р°Р·Р° (РјРµС‚Р°-С‚РµРіРё, robots.txt, sitemap)', en: 'SEO basics (meta tags, robots.txt, sitemap)' },
        'svc-visit-l6': { ru: 'Р—Р°РіСЂСѓР·РєР° РЅР° С…РѕСЃС‚РёРЅРі / GitHub Pages', en: 'Upload to hosting / GitHub Pages' },
        'svc-visit-l7': { ru: 'РџРѕРґРґРµСЂР¶РєР° 14 РґРЅРµР№', en: '14 days support' },
        'svc-full-l1': { ru: 'РњРЅРѕРіРѕСЃС‚СЂР°РЅРёС‡РЅС‹Р№ СЃР°Р№С‚ СЃ СѓРЅРёРєР°Р»СЊРЅС‹Рј РґРёР·Р°Р№РЅРѕРј', en: 'Multi-page website with unique design' },
        'svc-full-l2': { ru: 'РђРґР°РїС‚Р°С†РёСЏ РїРѕРґ РІСЃРµ СѓСЃС‚СЂРѕР№СЃС‚РІР°', en: 'Adaptation for all devices' },
        'svc-full-l3': { ru: 'SEO-РѕРїС‚РёРјРёР·Р°С†РёСЏ', en: 'SEO optimization' },
        'svc-full-l4': { ru: 'Р¤РѕСЂРјР° РѕР±СЂР°С‚РЅРѕР№ СЃРІСЏР·Рё + CRM', en: 'Contact form + CRM' },
        'svc-full-l5': { ru: 'РџРѕРґРєР»СЋС‡РµРЅРёРµ Р°РЅР°Р»РёС‚РёРєРё (РњРµС‚СЂРёРєР°)', en: 'Analytics setup (Metrika)' },
        'svc-full-l6': { ru: 'РџРѕРґРґРµСЂР¶РєР° 30 РґРЅРµР№', en: '30 days support' },
        'svc-botsimple-l1': { ru: 'РњРµРЅСЋ РёР· 5 РїСѓРЅРєС‚РѕРІ (СѓСЃР»СѓРіРё, РєРѕРЅС‚Р°РєС‚С‹, Рѕ РЅР°СЃ)', en: '5-item menu (services, contacts, about us)' },
        'svc-botsimple-l2': { ru: 'РђРІС‚РѕРѕС‚РІРµС‚С‹ РЅР° С‡Р°СЃС‚С‹Рµ РІРѕРїСЂРѕСЃС‹', en: 'Auto-replies to FAQs' },
        'svc-botsimple-l3': { ru: 'РџРµСЂРµРІРѕРґ РЅР° РґРёР°Р»РѕРі СЃ Р°РґРјРёРЅРёСЃС‚СЂР°С‚РѕСЂРѕРј', en: 'Transfer to admin chat' },
        'svc-botsimple-l4': { ru: 'Р Р°СЃСЃС‹Р»РєР° СѓРІРµРґРѕРјР»РµРЅРёР№', en: 'Notification broadcasting' },
        'svc-botsimple-l5': { ru: 'РџРѕРґРґРµСЂР¶РєР° 14 РґРЅРµР№', en: '14 days support' },
        'svc-botgpt-l1': { ru: 'Р‘РѕС‚-РєРѕРЅСЃСѓР»СЊС‚Р°РЅС‚ РЅР° Р±Р°Р·Рµ GPT', en: 'GPT-based consultant bot' },
        'svc-botgpt-l2': { ru: 'РџСЂРёС‘Рј Р·Р°СЏРІРѕРє Рё РѕРїР»Р°С‚', en: 'Order and payment processing' },
        'svc-botgpt-l3': { ru: 'РђРІС‚РѕРїРѕСЃС‚РёРЅРі РїРѕ СЂР°СЃРїРёСЃР°РЅРёСЋ', en: 'Scheduled auto-posting' },
        'svc-botgpt-l4': { ru: 'РџР»Р°С‚РЅС‹Р№ РґРѕСЃС‚СѓРї РІ РєР°РЅР°Р»', en: 'Paid channel access' },
        'svc-botgpt-l5': { ru: 'РџР°РЅРµР»СЊ Р°РґРјРёРЅРёСЃС‚СЂР°С‚РѕСЂР°', en: 'Admin panel' },
        'svc-botgpt-l6': { ru: 'РџРѕРґРґРµСЂР¶РєР° 30 РґРЅРµР№', en: '30 days support' },
        'svc-art-up2k': { ru: 'Р”Рѕ 2 000 Р·РЅР°РєРѕРІ', en: 'Up to 2,000 characters' },
        'svc-art-2k4k': { ru: '2 000 вЂ“ 4 000 Р·РЅР°РєРѕРІ', en: '2,000 вЂ“ 4,000 characters' },
        'svc-art-4k7k': { ru: '4 000 вЂ“ 7 000 Р·РЅР°РєРѕРІ', en: '4,000 вЂ“ 7,000 characters' },
        'svc-art-from7k': { ru: 'РћС‚ 7 000 Р·РЅР°РєРѕРІ', en: 'From 7,000 characters' },
        'svc-art-l1': { ru: 'РўРµРјС‹: С‚РµС…РЅРѕР»РѕРіРёРё, РЅР°СѓРєР°, Р±РёР·РЅРµСЃ', en: 'Topics: technology, science, business' },
        'svc-art-l2': { ru: 'РђРґР°РїС‚Р°С†РёСЏ РїРѕРґ Telegram-РїРѕСЃС‚', en: 'Adapted for Telegram post' },
        'svc-art-l3': { ru: 'РР·РѕР±СЂР°Р¶РµРЅРёСЏ Рё РёРЅС„РѕРіСЂР°С„РёРєР°', en: 'Images and infographics' },
        'svc-art-l4': { ru: 'SEO-Р·Р°РіРѕР»РѕРІРєРё', en: 'SEO headlines' },
        'svc-art-l5': { ru: 'РџР°РєРµС‚ 10 СЃС‚Р°С‚РµР№ вЂ” СЃРєРёРґРєР° 20%', en: '10-article pack вЂ” 20% off' },
        'svc-promo-l1': { ru: 'SEO-РѕРїС‚РёРјРёР·Р°С†РёСЏ СЃР°Р№С‚Р°', en: 'Website SEO optimization' },
        'svc-promo-l2': { ru: 'РџРѕРґРєР»СЋС‡РµРЅРёРµ РЇРЅРґРµРєСЃ.Р’РµР±РјР°СЃС‚РµСЂ', en: 'Yandex Webmaster setup' },
        'svc-promo-l3': { ru: 'РќР°СЃС‚СЂРѕР№РєР° РЇРЅРґРµРєСЃ.РњРµС‚СЂРёРєРё', en: 'Yandex Metrica configuration' },
        'svc-promo-l4': { ru: 'Р Р°СЃСЃС‹Р»РєР° РїРѕ РєР°С‚Р°Р»РѕРіР°Рј', en: 'Directory submission' },
        'svc-promo-l5': { ru: 'РљРѕРЅС‚РµРЅС‚-РїР»Р°РЅ РЅР° РјРµСЃСЏС†', en: 'Monthly content plan' },
        'error-404-title': { ru: 'РЎС‚СЂР°РЅРёС†Р° РЅРµ РЅР°Р№РґРµРЅР°', en: 'Page not found' },
        'error-404-btn': { ru: 'РќР° РіР»Р°РІРЅСѓСЋ', en: 'Go home' }
    };

    window.translations = translations;
    const btn = document.getElementById('langBtnFloat');

    function applyLang(l) {
        lang = l;
        localStorage.setItem(LANG_KEY, l);

        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.dataset.i18n;
            if (translations[key]) {
                if (!el.hasAttribute('data-ru') && translations[key].ru) {
                    el.setAttribute('data-ru', translations[key].ru);
                }
                if (!el.hasAttribute('data-en') && translations[key].en) {
                    el.setAttribute('data-en', translations[key].en);
                }
                if (translations[key][l]) {
                    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                        el.placeholder = translations[key][l];
                    } else {
                        el.innerHTML = translations[key][l];
                    }
                }
            }
        });

        btn.textContent = lang === 'ru' ? 'EN' : 'RU';
        document.documentElement.lang = lang;
    }

    applyLang(lang);
})();
