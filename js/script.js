// Burger menu
(function() {
    const burger = document.getElementById('burger');
    const nav = document.getElementById('nav');
    if (!burger || !nav) return;
    burger.addEventListener('click', function() {
        nav.classList.toggle('nav--open');
    });
    var links = nav.querySelectorAll('a');
    for (var i = 0; i < links.length; i++) {
        links[i].addEventListener('click', function() {
            nav.classList.remove('nav--open');
        });
    }
})();

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
            if (!el.dataset.target) return;
            const target = +el.dataset.target;
            const duration = 1500;
            const start = performance.now();

            const update = (now) => {
                const elapsed = now - start;
                const progress = Math.min(elapsed / duration, 1);
                el.textContent = Math.round(target * progress) + '+';
                if (progress < 1) requestAnimationFrame(update);
            };

            requestAnimationFrame(update);
            counterObserver.unobserve(el);
        }
    });
}, { threshold: 0.5 });

counters.forEach(el => counterObserver.observe(el));

// Modal
const form = document.getElementById('contactForm');
const modal = document.getElementById('modal');
const modalClose = document.getElementById('modalClose');
const modalIcon = document.getElementById('modalIcon');
const modalText = document.getElementById('modalText');

const modalSuccess = () => {
    modalIcon.innerHTML = '&#10024;';
    modalText.textContent = modalText.dataset.i18n === 'modal-thanks'
        ? (document.documentElement.lang === 'en' ? 'Thank you! We will contact you shortly.' : 'Спасибо! Мы свяжемся с вами в ближайшее время.')
        : modalText.dataset.i18n;
};

const modalError = () => {
    modalIcon.innerHTML = '&#10060;';
    modalText.textContent = document.documentElement.lang === 'en'
        ? 'Server error. Try again later or write to Telegram.'
        : 'Ошибка сервера. Попробуйте позже или напишите в Telegram.';
};

if (form && modal && modalClose) {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const data = {
            name: form.querySelector('[name="name"]')?.value || '',
            email: form.querySelector('[name="email"]')?.value || '',
            phone: form.querySelector('[name="phone"]')?.value || '',
            message: form.querySelector('[name="message"]')?.value || ''
        };
        fetch('https://astap.pythonanywhere.com/api/lead', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
            mode: 'cors'
        }).then(r => {
            if (r.ok) modalSuccess();
            else modalError();
        }).catch(() => modalError());
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
}

// Modal

// Visit tracker
(function() {
    const PA_URL = 'https://astap.pythonanywhere.com/visit';
    const data = {
        page: window.location.pathname,
        ref: document.referrer || '',
        screen: (screen.width || '') + 'x' + (screen.height || '')
    };
    try {
        fetch(PA_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
            mode: 'cors'
        }).catch(function() {});
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

    var greetingTimer = null;

    function getGreeting() {
        var lang = window.currentLang || 'ru';
        return lang === 'en' ? 'Hello! Ask your question.' : 'Здравствуйте! Задайте ваш вопрос.';
    }

    function addGreeting() {
        if (!body.querySelector('.chat-msg--greeting')) {
            var gr = document.createElement('div');
            gr.className = 'chat-msg chat-msg--bot chat-msg--greeting';
            gr.textContent = getGreeting();
            body.insertBefore(gr, body.firstChild);
        }
    }

    btn.addEventListener('click', () => {
        var isOpen = popup.classList.contains('chat-popup--open');
        popup.classList.toggle('chat-popup--open');
        if (!isOpen && !greetingTimer && !body.querySelector('.chat-msg--greeting')) {
            greetingTimer = setTimeout(addGreeting, 7000);
        }
        if (isOpen && greetingTimer) {
            clearTimeout(greetingTimer);
            greetingTimer = null;
        }
    });

    close.addEventListener('click', function() {
        popup.classList.remove('chat-popup--open');
    });

    function sendMessage(msg, retries) {
        if (!msg) return;
        retries = retries || 0;
        if (retries === 0) {
            input.value = '';
            body.insertAdjacentHTML('beforeend', '<div class="chat-msg chat-msg--user">' + escapeHtml(msg) + '</div>');
            body.scrollTop = body.scrollHeight;
        }
        body.insertAdjacentHTML('beforeend', '<div class="chat-msg chat-msg--bot"><em>Печатает...</em></div>');
        body.scrollTop = body.scrollHeight;
        var ac = new AbortController();
        var timeout = retries > 0 ? 25000 : 15000;
        setTimeout(function() { ac.abort(); }, timeout);
        fetch('https://astap.pythonanywhere.com/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg, lang: window.currentLang || 'ru' }),
            mode: 'cors',
            signal: ac.signal
        }).then(function(r) { return r.json(); }).then(function(data) {
            body.removeChild(body.lastChild);
            body.insertAdjacentHTML('beforeend', '<div class="chat-msg chat-msg--bot">' + escapeHtml(data.reply) + '</div>');
        }).catch(function() {
            body.removeChild(body.lastChild);
            if (retries < 5) {
                body.insertAdjacentHTML('beforeend', '<div class="chat-msg chat-msg--bot" style="font-size:0.85rem;color:#888;"><em>Пробуждаю сервер...</em></div>');
                body.scrollTop = body.scrollHeight;
                setTimeout(function() { body.removeChild(body.lastChild); sendMessage(msg, retries + 1); }, 3000);
            } else {
                var errMsg = 'Извините, сервер временно недоступен. Напишите нам в Telegram: <a href="https://t.me/uriy_as59" target="_blank" style="color:#6c63ff;">@uriy_as59</a>';
                body.insertAdjacentHTML('beforeend', '<div class="chat-msg chat-msg--bot" style="font-size:0.85rem;">' + errMsg + '</div>');
            }
        });
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        sendMessage(input.value.trim());
    });

    function escapeHtml(text) {
        var d = document.createElement('div');
        d.textContent = text;
        return d.innerHTML;
    }
})();

// Language switcher
(function() {
    const LANG_KEY = 'site_lang';
    let lang = document.documentElement.lang || 'ru';
    try { lang = localStorage.getItem(LANG_KEY) || lang; } catch(e) {}

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
        'tg-promo-title': { ru: 'Подпишитесь на наш Telegram-канал', en: 'Subscribe to our Telegram Channel' },
        'tg-promo-desc': { ru: 'Кейсы, статьи и инсайты по разработке сайтов, Telegram-ботов и контент-маркетингу. Публикуем полезный контент каждый понедельник, среду, пятницу и субботу в 08:10.', en: 'Cases, articles and insights on website development, Telegram bots and content marketing. We publish useful content every Monday, Wednesday, Friday and Saturday at 08:10.' },
        'tg-promo-btn': { ru: 'Подписаться в Telegram', en: 'Subscribe on Telegram' },
        'stats-projects': { ru: 'Завершённых проектов', en: 'Completed Projects' },
        'stats-clients': { ru: 'Активных клиентов', en: 'Active Clients' },
        'stats-years': { ru: 'Лет на рынке', en: 'Years on Market' },
        'stats-satisfaction': { ru: '% довольных клиентов', en: '% Satisfied Clients' },
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
        'footer-bot': { ru: '@NevWebStudio_bot — бот ответит на все интересующие вопросы', en: '@NevWebStudio_bot — the bot will answer all your questions' },
        'modal-thanks': { ru: 'Спасибо! Мы свяжемся с вами в ближайшее время.', en: 'Thank you! We will contact you shortly.' },
        'modal-btn': { ru: 'Отлично', en: 'Great' },
        'contact-alt-title': { ru: 'Выберите удобный канал', en: 'Choose your preferred channel' },
        'contact-alt-desc': { ru: 'Свяжитесь через любой мессенджер', en: 'Reach us via any messenger' },
        'contact-alt-tg': { ru: 'Telegram', en: 'Telegram' },
        'contact-alt-bot': { ru: 'Telegram-бот', en: 'Telegram Bot' },
        'contact-alt-whatsapp': { ru: 'WhatsApp', en: 'WhatsApp' },
        'contact-alt-viber': { ru: 'Viber', en: 'Viber' },
        'tg-float-text': { ru: 'Telegram', en: 'Telegram' },
        'chat-btn-text': { ru: 'AI-чат', en: 'AI Chat' },
        'chat-title': { ru: 'AI-ассистент', en: 'AI Assistant' },
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
        'service-promo-msg': { ru: '💰 Цены указаны в USD. Возможна оплата в рублях, EUR, USDT, криптовалюте — по курсу на день сделки.<br>🎯 <strong>Скидка 30%</strong> для первых 5 заказчиков. Визитка от $175, бот от $90, статья от $35 — успейте!<br>📩 Свяжитесь с нами в Telegram: <a href="https://t.me/uriy_as59" style="color:var(--accent);">@uriy_as59</a>', en: '💰 Prices in USD. Payment in RUB, EUR, USDT, crypto — at the exchange rate on the deal date.<br>🎯 <strong>30% discount</strong> for the first 5 customers. Business card from $175, bot from $90, article from $35 — hurry up!<br>📩 Contact us on Telegram: <a href="https://t.me/uriy_as59" style="color:var(--accent);">@uriy_as59</a>' },
        'price-from': { ru: 'от', en: 'from' },
        'price-project': { ru: 'за проект', en: 'per project' },
        'price-article': { ru: 'за статью', en: 'per article' },
        'price-month': { ru: 'за месяц', en: 'per month' },
        'svc-visit-l1': { ru: '1–3 страницы (главная, услуги, контакты)', en: '1–3 pages (home, services, contacts)' },
        'svc-visit-l2': { ru: 'Уникальный дизайн под ваш бренд', en: 'Unique design for your brand' },
        'svc-visit-l3': { ru: 'Адаптация под телефон и планшет', en: 'Mobile and tablet adaptation' },
        'svc-visit-l4': { ru: 'Форма обратной связи', en: 'Contact form' },
        'svc-visit-l5': { ru: 'SEO-база (мета-теги, robots.txt, sitemap)', en: 'SEO basics (meta tags, robots.txt, sitemap)' },
        'svc-visit-l6': { ru: 'Загрузка на хостинг / GitHub Pages', en: 'Upload to hosting / GitHub Pages' },
        'svc-visit-l7': { ru: 'Поддержка 14 дней', en: '14 days support' },
        'svc-full-l1': { ru: 'Многостраничный сайт с уникальным дизайном', en: 'Multi-page website with unique design' },
        'svc-full-l2': { ru: 'Адаптация под все устройства', en: 'Adaptation for all devices' },
        'svc-full-l3': { ru: 'SEO-оптимизация', en: 'SEO optimization' },
        'svc-full-l4': { ru: 'Форма обратной связи + CRM', en: 'Contact form + CRM' },
        'svc-full-l5': { ru: 'Подключение аналитики (Метрика)', en: 'Analytics setup (Metrika)' },
        'svc-full-l6': { ru: 'Поддержка 30 дней', en: '30 days support' },
        'svc-botsimple-l1': { ru: 'Меню из 5 пунктов (услуги, контакты, о нас)', en: '5-item menu (services, contacts, about us)' },
        'svc-botsimple-l2': { ru: 'Автоответы на частые вопросы', en: 'Auto-replies to FAQs' },
        'svc-botsimple-l3': { ru: 'Перевод на диалог с администратором', en: 'Transfer to admin chat' },
        'svc-botsimple-l4': { ru: 'Рассылка уведомлений', en: 'Notification broadcasting' },
        'svc-botsimple-l5': { ru: 'Поддержка 14 дней', en: '14 days support' },
        'svc-botgpt-l1': { ru: 'Бот-консультант на базе GPT', en: 'GPT-based consultant bot' },
        'svc-botgpt-l2': { ru: 'Приём заявок и оплат', en: 'Order and payment processing' },
        'svc-botgpt-l3': { ru: 'Автопостинг по расписанию', en: 'Scheduled auto-posting' },
        'svc-botgpt-l4': { ru: 'Платный доступ в канал', en: 'Paid channel access' },
        'svc-botgpt-l5': { ru: 'Панель администратора', en: 'Admin panel' },
        'svc-botgpt-l6': { ru: 'Поддержка 30 дней', en: '30 days support' },
        'svc-art-up2k': { ru: 'До 2 000 знаков', en: 'Up to 2,000 characters' },
        'svc-art-2k4k': { ru: '2 000 – 4 000 знаков', en: '2,000 – 4,000 characters' },
        'svc-art-4k7k': { ru: '4 000 – 7 000 знаков', en: '4,000 – 7,000 characters' },
        'svc-art-from7k': { ru: 'От 7 000 знаков', en: 'From 7,000 characters' },
        'svc-art-l1': { ru: 'Темы: технологии, наука, бизнес', en: 'Topics: technology, science, business' },
        'svc-art-l2': { ru: 'Адаптация под Telegram-пост', en: 'Adapted for Telegram post' },
        'svc-art-l3': { ru: 'Изображения и инфографика', en: 'Images and infographics' },
        'svc-art-l4': { ru: 'SEO-заголовки', en: 'SEO headlines' },
        'svc-art-l5': { ru: 'Пакет 10 статей — скидка 20%', en: '10-article pack — 20% off' },
        'svc-promo-l1': { ru: 'SEO-оптимизация сайта', en: 'Website SEO optimization' },
        'svc-promo-l2': { ru: 'Подключение Яндекс.Вебмастер', en: 'Yandex Webmaster setup' },
        'svc-promo-l3': { ru: 'Настройка Яндекс.Метрики', en: 'Yandex Metrica configuration' },
        'svc-promo-l4': { ru: 'Рассылка по каталогам', en: 'Directory submission' },
        'svc-promo-l5': { ru: 'Контент-план на месяц', en: 'Monthly content plan' },
        'error-404-title': { ru: 'Страница не найдена', en: 'Page not found' },
        'error-404-btn': { ru: 'На главную', en: 'Go home' },
        'footer-privacy': { ru: 'Политика конфиденциальности', en: 'Privacy Policy' },
        'footer-stats': { ru: 'Статистика', en: 'Stats' }
    };

    window.translations = translations;
    const btn = document.getElementById('langBtnFloat');

    function applyLang(l) {
        lang = l;
        window.currentLang = l;
        try { localStorage.setItem(LANG_KEY, l); } catch(e) {}

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

    window.toggleLang = function() {
        var newLang = lang === 'ru' ? 'en' : 'ru';
        applyLang(newLang);
    };
})();
