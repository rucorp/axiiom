/* Archived PLATFORMA franchise landing — restored script.js */
(function () {
    'use strict';

    /* Theme toggle */
    function applyTheme(theme) {
        if (theme === 'light') {
            document.documentElement.setAttribute('data-theme', 'light');
        } else {
            document.documentElement.removeAttribute('data-theme');
        }
    }

    var saved = null;
    try { saved = localStorage.getItem('platforma-theme'); } catch (e) {}
    if (!saved) {
        saved = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
    }
    applyTheme(saved);

    function toggleTheme() {
        var current = document.documentElement.getAttribute('data-theme');
        var next = current === 'light' ? 'dark' : 'light';
        applyTheme(next);
        try { localStorage.setItem('platforma-theme', next); } catch (e) {}
    }

    var themeBtns = [
        document.getElementById('themeToggle'),
        document.getElementById('themeToggleMobile')
    ];
    themeBtns.forEach(function (btn) {
        if (btn) btn.addEventListener('click', toggleTheme);
    });

    /* Mobile menu */
    var toggle = document.getElementById('mobileMenuToggle');
    var overlay = document.getElementById('mobileMenuOverlay');
    if (toggle && overlay) {
        toggle.addEventListener('click', function () {
            overlay.classList.toggle('open');
        });
        overlay.addEventListener('click', function (e) {
            if (e.target.tagName === 'A') overlay.classList.remove('open');
        });
    }

    /* Hash-based slide navigation (single-page sections) */
    var slides = document.querySelectorAll('section.slide');
    function showSlide() {
        var hash = location.hash || '#products';
        var target = document.querySelector(hash);
        var found = false;
        for (var i = 0; i < slides.length; i++) {
            if (slides[i] === target) {
                slides[i].classList.add('active');
                found = true;
            } else {
                slides[i].classList.remove('active');
            }
        }
        if (!found && slides.length) slides[0].classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    if (slides.length) {
        window.addEventListener('hashchange', showSlide);
        showSlide();
    }
})();
