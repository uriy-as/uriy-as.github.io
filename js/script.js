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

// Private visit counter
(function() {
    const KEY = 'ws_visits';
    const now = new Date();
    const today = now.toDateString();

    let data = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (!data) {
        data = { total: 0, days: {}, lastVisit: null };
    }

    data.total = (data.total || 0) + 1;

    if (!data.days[today]) {
        data.days[today] = 0;
    }
    data.days[today] += 1;

    data.lastVisit = now.toLocaleString('ru-RU');
    localStorage.setItem(KEY, JSON.stringify(data));

    const uniqueDays = Object.keys(data.days).length;
    const todayCount = data.days[today] || 0;

    const adminPanel = document.getElementById('adminPanel');
    const adminTotal = document.getElementById('adminTotal');
    const adminToday = document.getElementById('adminToday');
    const adminDays = document.getElementById('adminDays');
    const adminLast = document.getElementById('adminLast');
    const adminClose = document.getElementById('adminClose');

    if (adminTotal) adminTotal.textContent = data.total;
    if (adminToday) adminToday.textContent = todayCount;
    if (adminDays) adminDays.textContent = uniqueDays;
    if (adminLast) adminLast.textContent = data.lastVisit;

    // Toggle on double-click of logo
    document.querySelector('.logo').addEventListener('dblclick', (e) => {
        e.preventDefault();
        adminPanel.classList.toggle('admin--visible');
    });

    if (adminClose) {
        adminClose.addEventListener('click', () => {
            adminPanel.classList.remove('admin--visible');
        });
    }
})();

// Modal + Telegram notification
const form = document.getElementById('contactForm');
const modal = document.getElementById('modal');
const modalClose = document.getElementById('modalClose');

const TG_TOKEN = '8308743016:AAEwu53QB_rwy5Di40YON4NBZA4A6SbgRQ0';
const TG_CHAT = '@webstudio_chanel';

function tgSend(text) {
    fetch(`https://api.telegram.org/bot${TG_TOKEN}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: TG_CHAT, text, parse_mode: 'HTML' })
    }).catch(() => {});
}

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const name = fd.get('name') || 'не указано';
    const email = fd.get('email') || 'не указан';
    const msg = fd.get('message') || 'не указано';
    tgSend(`📩 <b>Новая заявка с сайта!</b>\n\n👤 Имя: ${name}\n📧 Email: ${email}\n💬 Сообщение: ${msg}`);
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

// Visit notification (throttled – 1 per 2 hours)
(function() {
    const last = localStorage.getItem('ws_visit_notified');
    const now = Date.now();
    if (!last || now - parseInt(last) > 7200000) {
        tgSend(`👁 <b>Посещение сайта</b>\n${new Date().toLocaleString('ru-RU')}`);
        localStorage.setItem('ws_visit_notified', now.toString());
    }
})();
