// Gestione toast: click per chiudere subito, auto-dismiss dopo 5s
function attachToastHandlers() {
    document.querySelectorAll('#toast-container .toast').forEach(function (toast) {
        if (toast.dataset.bound) return; // evita doppio binding
        toast.dataset.bound = "true";

        // X visibile in alto a destra del toast
        const closeBtn = document.createElement('span');
        closeBtn.className = 'toast-close';
        closeBtn.innerHTML = '&times;';
        closeBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            toast.remove();
        });
        toast.appendChild(closeBtn);

        toast.style.cursor = "pointer";
        toast.title = "Clicca per chiudere";

        toast.addEventListener('click', function () {
            toast.remove();
        });

        setTimeout(function () {
            toast.remove();
        }, 5000);
    });
}

// Al primo caricamento pagina
document.addEventListener('DOMContentLoaded', attachToastHandlers);

// Dopo ogni swap HTMX (anche out-of-band, vedi punto B)
document.addEventListener('htmx:afterSwap', attachToastHandlers);
document.addEventListener('htmx:oobAfterSwap', attachToastHandlers);
