window.addEventListener('DOMContentLoaded', () => {
    let headerButtons = document.querySelectorAll(".header_menu_button");

    headerButtons.forEach(button => {
        if (!button.dataset.url) {
            console.error(`Header menu button ${button.textContent} url is missing `);
            return
        }

        button.addEventListener("click", (e) => {
            window.location.assign(button.dataset.url);
        })
    })
})