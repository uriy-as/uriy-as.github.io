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
            body.innerHTML += `<div class="chat-msg chat-msg--bot">РћС€РёР±РєР° СЃРІСЏР·Рё. РџРѕРїСЂРѕР±СѓР№С‚Рµ РїРѕР·Р¶Рµ.</div>`;
        }
        body.scrollTop = body.scrollHeight;
    });

    function escapeHtml(text) {
        const d = document.createElement('div');
        d.textContent = text;
        return d.innerHTML;
    }
})();
