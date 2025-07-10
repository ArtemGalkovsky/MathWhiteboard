function sendResponse(buttonContainer, url, csrfToken) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
    }).then(response => {
        if (response.ok) {
            buttonContainer.remove()
        }
    })
}


window.addEventListener('DOMContentLoaded', () => {
    let buttons = document.querySelectorAll('.friendship_requests_button');
    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');

    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            if (!button.dataset.url) {
                console.error(`Button url not found for ${button.textContent}`);
                return
            }

            if (!button.dataset.requestId) {
                console.error(`Button requestId not found for ${button.textContent}`);
                return
            }

            let buttonContainer = document.querySelector(`.friendship_request_container[data-id="${button.dataset.requestId}"]`);
            sendResponse(buttonContainer, button.dataset.url, csrfToken.value);
        })
    })
})