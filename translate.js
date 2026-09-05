const LANG_PREF_KEY = 'aidisciple_lang';

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
}

function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
}

function isUrdu() {
    return getCookie('googtrans') === '/en/ur';
}

function switchToUrdu() {
    setCookie('googtrans', '/en/ur', 365);
    setCookie(LANG_PREF_KEY, 'ur', 365);
    location.reload();
}

function switchToEnglish() {
    deleteCookie('googtrans');
    setCookie(LANG_PREF_KEY, 'en', 365);
    location.reload();
}

function updateToggleButton() {
    const btn = document.getElementById('lang-toggle');
    if (!btn) return;
    if (isUrdu()) {
        btn.innerHTML = '<img src="https://flagcdn.com/20x15/us.png" alt="US flag" style="vertical-align:middle;margin-right:6px;border-radius:2px;"> English';
    } else {
        btn.innerHTML = '<img src="https://flagcdn.com/20x15/pk.png" alt="Pakistan flag" style="vertical-align:middle;margin-right:6px;border-radius:2px;"> اردو';
    }
}

async function autoDetect() {
    if (getCookie(LANG_PREF_KEY)) return;
    try {
        const res = await fetch('https://ipapi.co/json/');
        const data = await res.json();
        if (data.country_code === 'PK') {
            switchToUrdu();
        }
    } catch (e) {
        // Silently fail — don't break the page if the API is unavailable
    }
}

function googleTranslateElementInit() {
    new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'ur,en',
        autoDisplay: false
    }, 'google_translate_element');
}

document.addEventListener('DOMContentLoaded', () => {
    updateToggleButton();

    const btn = document.getElementById('lang-toggle');
    if (btn) {
        btn.addEventListener('click', () => {
            isUrdu() ? switchToEnglish() : switchToUrdu();
        });
    }

    autoDetect();
});
