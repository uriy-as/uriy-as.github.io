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

// Chat widget
const chatBtn = document.getElementById('chatBtn');
const chatPopup = document.getElementById('chatPopup');
const chatClose = document.getElementById('chatClose');
const chatForm = document.getElementById('chatForm');
const chatBody = document.getElementById('chatBody');
const chatInput = chatForm?.querySelector('input');

const TG_TOKEN = '8308743016:AAEwu53QB_rwy5Di40YON4NBZA4A6SbgRQ0';
const TG_CHAT = '1994948658';

function tgSend(text) {
    fetch(`https://api.telegram.org/bot${TG_TOKEN}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: TG_CHAT, text, parse_mode: 'HTML' })
    }).catch(() => {});
}

if (chatBtn) {
    chatBtn.addEventListener('click', () => {
        chatPopup.classList.toggle('chat-popup--open');
    });
}

if (chatClose) {
    chatClose.addEventListener('click', () => {
        chatPopup.classList.remove('chat-popup--open');
    });
}

if (chatForm) {
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = chatInput.value.trim();
        if (!text) return;

        const userMsg = document.createElement('div');
        userMsg.className = 'chat-msg chat-msg--user';
        userMsg.textContent = text;
        chatBody.appendChild(userMsg);

        chatInput.value = '';

        tgSend(`💬 <b>Сообщение с сайта</b>\n\n${text}`);

        setTimeout(() => {
            const botMsg = document.createElement('div');
            botMsg.className = 'chat-msg chat-msg--sent';
            botMsg.textContent = '✅ Отправлено! Я отвечу в ближайшее время.';
            chatBody.appendChild(botMsg);
            chatBody.scrollTop = chatBody.scrollHeight;
        }, 600);

        chatBody.scrollTop = chatBody.scrollHeight;
    });
}

// Visit tracker — отправка на PA
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
