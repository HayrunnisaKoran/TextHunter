// Please see documentation at https://learn.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.

// Karanlık Mod Fonksiyonları
(function() {
    'use strict';

    // Sayfa yüklendiğinde karanlık modu kontrol et ve uygula
    function initDarkMode() {
        const darkMode = localStorage.getItem('darkMode') === 'true';
        const darkModeSwitch = document.getElementById('darkModeSwitch');
        
        if (darkMode) {
            document.body.classList.add('dark-mode');
            if (darkModeSwitch) {
                darkModeSwitch.checked = true;
            }
        } else {
            document.body.classList.remove('dark-mode');
            if (darkModeSwitch) {
                darkModeSwitch.checked = false;
            }
        }
    }

    // Karanlık modu toggle et
    function toggleDarkMode(enabled) {
        if (enabled) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'true');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'false');
        }
    }

    // Sayfa yüklendiğinde çalıştır
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDarkMode);
    } else {
        initDarkMode();
    }

    // Global olarak erişilebilir yap
    window.toggleDarkMode = toggleDarkMode;
    window.initDarkMode = initDarkMode;
})();