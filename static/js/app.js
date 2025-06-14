document.addEventListener('DOMContentLoaded', function() {
    const firstInput = document.querySelector('form input, form select');
    if (firstInput) firstInput.focus();

    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            let btn = form.querySelector('button[type="submit"]');
            if (btn) btn.innerHTML = "Predicting...";
        });
    }
});