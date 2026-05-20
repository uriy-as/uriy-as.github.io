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
