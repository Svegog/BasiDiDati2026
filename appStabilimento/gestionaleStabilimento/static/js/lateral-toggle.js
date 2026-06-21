// Toggle generico per bottoni con hx-get sostituito da data-url/data-target.
// Eseguito subito (NON su DOMContentLoaded): questo script arriva dentro al
// fragment HTML swappato da HTMX, quindi quell'evento è già scattato in
// precedenza e non si ripeterebbe mai.
(function () {
    const buttons = document.querySelectorAll('.toggle-btn');
    const defaults = {};        // selector -> html di partenza
    const activeButtons = {};   // selector -> bottone attivo per quel target

    buttons.forEach(function (btn) {
        const selector = btn.dataset.target;
        const target = document.querySelector(selector);
        if (!target) return;

        if (!(selector in defaults)) {
            defaults[selector] = target.innerHTML;
            activeButtons[selector] = null;
        }

        btn.addEventListener('click', function () {
            const url = btn.dataset.url;
            const current = activeButtons[selector];

            if (btn === current) {
                target.innerHTML = defaults[selector];
                btn.classList.remove('active');
                activeButtons[selector] = null;
                return;
            }

            if (current) current.classList.remove('active');

            btn.classList.add('active');
            activeButtons[selector] = btn;

            htmx.ajax('GET', url, { target: selector, swap: 'innerHTML' });
        });
    });
})();