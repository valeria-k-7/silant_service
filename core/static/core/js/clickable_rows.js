document.addEventListener('DOMContentLoaded', () => {
    const rows = document.querySelectorAll('[data-clickable-row]');

    rows.forEach((row) => {
        const detailLink = row.querySelector('[data-row-detail-link]');

        if (!detailLink) {
            return;
        }

        row.addEventListener('click', (event) => {
            const interactiveElement = event.target.closest(
                'a, button, input, select, textarea, label'
            );

            if (interactiveElement) {
                return;
            }

            const selectedText = window.getSelection()?.toString();

            if (selectedText) {
                return;
            }

            window.location.href = detailLink.href;
        });
    });
});