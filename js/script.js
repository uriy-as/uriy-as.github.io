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

        body.innerHTML += `<div class="chat-msg chat-msg--bot"><em>Печатает...</em></div>`;
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

            if (data.reply.includes('запрос передан')) {
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
        'nav-services': { ru: 'Услуги', en: 'Services' },
        'nav-about': { ru: 'О нас', en: 'About' },
        'nav-articles': { ru: 'Статьи', en: 'Articles' },
        'nav-contacts': { ru: 'Контакты', en: 'Contacts' },
        'nav-chat': { ru: 'AI-чат', en: 'AI Chat' },
        'hero-badge': { ru: 'Ваш цифровой партнёр', en: 'Your Digital Partner' },
        'hero-title': { ru: 'Создаём цифровые продукты <span class="gradient-text">для вашего бизнеса</span>', en: 'We create digital products <span class="gradient-text">for your business</span>' },
        'hero-subtitle': { ru: 'Веб-сайты, чат-боты и Telegram-каналы с научным контентом — под ключ', en: 'Websites, chatbots, and Telegram channels with science content — turnkey' },
        'hero-btn-contact': { ru: 'Связаться с нами', en: 'Contact us' },
        'hero-btn-services': { ru: 'Наши услуги', en: 'Our services' },
        'section-services': { ru: 'Наши услуги', en: 'Our Services' },
        'service-site': { ru: 'Создание сайтов', en: 'Website Development' },
        'service-site-desc': { ru: 'Разработка сайтов любой сложности: от лендингов до интернет-магазинов. Адаптивный дизайн, SEO-оптимизация, высокая скорость загрузки.', en: 'Development of websites of any complexity: from landing pages to online stores. Responsive design, SEO optimization, fast loading.' },
        'service-bot': { ru: 'Чат-боты', en: 'Chatbots' },
        'service-bot-desc': { ru: 'Интеллектуальные Telegram-боты на базе AI для поддержки клиентов, продаж, сбора заявок и автоматизации рутины.', en: 'AI-powered Telegram bots for customer support, sales, lead collection, and routine automation.' },
        'service-articles': { ru: 'Научные статьи для Telegram', en: 'Science Articles for Telegram' },
        'service-articles-desc': { ru: 'Качественные научно-популярные статьи, адаптированные для Telegram-каналов. Глубокий анализ, уникальный контент, вовлекающий формат.', en: 'High-quality science articles adapted for Telegram channels. Deep analysis, unique content, engaging format.' },
        'section-about': { ru: 'Почему мы?', en: 'Why Us?' },
        'about-individual': { ru: 'Индивидуальный подход', en: 'Individual Approach' },
        'about-individual-desc': { ru: '100% уникальное решение под задачи вашего бизнеса', en: '100% unique solution for your business needs' },
        'about-tech': { ru: 'Современные технологии', en: 'Modern Technologies' },
        'about-tech-desc': { ru: 'Актуальный стек и лучшие практики разработки', en: 'Cutting-edge stack and best development practices' },
        'about-support': { ru: 'Поддержка 24/7', en: '24/7 Support' },
        'about-support-desc': { ru: 'Всегда на связи до и после сдачи проекта', en: 'Always in touch before and after project delivery' },
        'tg-widget-title': { ru: 'Последние посты канала', en: 'Latest Channel Posts' },
        'tg-widget-subtitle': { ru: 'Подпишитесь, чтобы не пропускать полезный контент', en: 'Subscribe so you don\'t miss useful content' },
        'tg-widget-all': { ru: 'Все посты в канале', en: 'All posts in channel' },
        'stats-projects': { ru: 'Завершённых проектов', en: 'Completed Projects' },
        'stats-clients': { ru: 'Активных клиентов', en: 'Active Clients' },
        'stats-years': { ru: 'Лет на рынке', en: 'Years on Market' },
        'stats-satisfaction': { ru: '% довольных клиентов', en: '% Satisfied Clients' },
        'tg-promo-title': { ru: 'Подпишитесь на наш Telegram-канал', en: 'Subscribe to our Telegram Channel' },
        'tg-promo-desc': { ru: 'Кейсы, статьи и инсайты по разработке сайтов, Telegram-ботов и контент-маркетингу. Публикуем полезный контент каждый понедельник, среду, пятницу и субботу в 08:10.', en: 'Cases, articles and insights on website development, Telegram bots and content marketing. We publish useful content every Monday, Wednesday, Friday and Saturday at 08:10.' },
        'tg-promo-btn': { ru: 'Подписаться в Telegram', en: 'Subscribe on Telegram' },
        'contact-title': { ru: 'Свяжитесь с нами', en: 'Contact Us' },
        'contact-subtitle': { ru: 'Оставьте заявку, и мы обсудим ваш проект', en: 'Leave a request and we\'ll discuss your project' },
        'form-name': { ru: 'Ваше имя', en: 'Your name' },
        'form-email': { ru: 'Email', en: 'Email' },
        'form-phone': { ru: 'Ваш телефон / если требуется скорость', en: 'Your phone / if speed matters' },
        'form-message': { ru: 'Опишите ваш проект', en: 'Describe your project' },
        'form-submit': { ru: 'Отправить заявку', en: 'Send request' },
        'contact-email': { ru: 'uriy.as59@yandex.com', en: 'uriy.as59@yandex.com' },
        'contact-tg': { ru: 'Telegram', en: 'Telegram' },
        'footer-copyright': { ru: '© 2026 WebStudio. Все права защищены.', en: '© 2026 WebStudio. All rights reserved.' },
        'footer-bot': { ru: '@NevChatAI_bot — бот ответит на все интересующие вопросы', en: '@NevChatAI_bot — the bot will answer all your questions' },
        'modal-thanks': { ru: 'Спасибо! Мы свяжемся с вами в ближайшее время.', en: 'Thank you! We will contact you shortly.' },
        'modal-btn': { ru: 'Отлично', en: 'Great' },
        'tg-float-text': { ru: 'Telegram', en: 'Telegram' },
        'chat-btn-text': { ru: 'AI-чат', en: 'AI Chat' },
        'chat-title': { ru: 'Чат с WebStudio AI', en: 'Chat with WebStudio AI' },
        'chat-greeting': { ru: 'Здравствуйте! Задайте ваш вопрос.', en: 'Hello! Ask your question.' },
        'chat-placeholder': { ru: 'Ваше сообщение...', en: 'Your message...' },
        'chat-error': { ru: 'Ошибка связи. Попробуйте позже.', en: 'Connection error. Try again later.' },
        'article-hero-title': { ru: 'Полезные статьи', en: 'Useful Articles' },
        'article-hero-subtitle': { ru: 'Кейсы, советы и инструкции по созданию сайтов, ботов и контента', en: 'Cases, tips and guides on creating websites, bots and content' },
        'article-share-tg': { ru: 'Telegram', en: 'Telegram' },
        'article-share-email': { ru: 'Email', en: 'Email' },
        'service-hero-title': { ru: 'Наши услуги', en: 'Our Services' },
        'service-hero-subtitle': { ru: 'Разработка под ключ — от идеи до готового продукта', en: 'Turnkey development — from idea to finished product' },
        'service-banner': { ru: '🎉 Акция: скидка 30% для первых 5 клиентов! Успейте заказать по старой цене', en: '🎉 Promo: 30% off for the first 5 customers! Order now at the old price' },
        'service-card-order': { ru: 'Заказать', en: 'Order' },
        'service-promo': { ru: '💰 Цены указаны в USD. Возможна оплата в рублях, EUR, USDT, криптовалюте — по курсу на день сделки.<br>🎯 <strong>Скидка 30%</strong> для первых 5 заказчиков. Визитка от $105, бот от $42, статья от $21 — успейте!<br>📩 Свяжитесь с нами в Telegram: <a href="https://t.me/webstudio_chanel" style="color:var(--accent);">@webstudio_chanel</a>', en: '💰 Prices in USD. Payment in RUB, EUR, USDT, crypto — at the exchange rate on the deal date.<br>🎯 <strong>30% discount</strong> for the first 5 customers. Business card from $105, bot from $42, article from $21 — hurry up!<br>📩 Contact us on Telegram: <a href="https://t.me/webstudio_chanel" style="color:var(--accent);">@webstudio_chanel</a>' },
        'service-card-visit': { ru: 'Сайт-визитка', en: 'Business Card Website' },
        'service-card-visit-desc': { ru: 'Компактный сайт для представления бизнеса', en: 'Compact website for business presentation' },
        'service-card-full': { ru: 'Сайт под ключ', en: 'Full Website' },
        'service-card-full-desc': { ru: 'Landing page, интернет-магазин, корпоративный сайт', en: 'Landing page, online store, corporate website' },
        'service-card-bot-simple': { ru: 'Бот-визитка', en: 'Business Card Bot' },
        'service-card-bot-simple-desc': { ru: 'Простой Telegram-бот для связи с клиентами', en: 'Simple Telegram bot for client communication' },
        'service-card-bot-gpt': { ru: 'Telegram-бот на GPT', en: 'GPT Telegram Bot' },
        'service-card-bot-gpt-desc': { ru: 'Чат-бот с нейросетью, приём заявок и оплат', en: 'Chatbot with neural network, order and payment processing' },
        'service-card-articles': { ru: 'Научные статьи', en: 'Science Articles' },
        'service-card-articles-desc': { ru: 'Тематический контент для Telegram и соцсетей', en: 'Thematic content for Telegram and social media' },
        'service-card-promo': { ru: 'Продвижение', en: 'Promotion' },
        'service-card-promo-desc': { ru: 'SEO, Яндекс.Метрика, раскрутка канала', en: 'SEO, Yandex Metrica, channel promotion' },
        'error-404-title': { ru: 'Страница не найдена', en: 'Page not found' },
        'error-404-btn': { ru: 'На главную', en: 'Go home' }
    };

    const btn = document.getElementById('langBtnFloat');

    function applyLang(l) {
        lang = l;
        localStorage.setItem(LANG_KEY, l);

        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.dataset.i18n;
            if (translations[key] && translations[key][l]) {
                el.innerHTML = translations[key][l];
            }
        });

        btn.textContent = lang === 'ru' ? 'EN' : 'RU';
        document.documentElement.lang = lang;
    }

    btn.addEventListener('click', () => {
        applyLang(lang === 'ru' ? 'en' : 'ru');
    });

    applyLang(lang);
})();
