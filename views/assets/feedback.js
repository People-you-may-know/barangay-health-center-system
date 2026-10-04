(() => {
    window.AppFeedback = {
        show(element, message, type = "info", retry = null) {
            if (!element) return;
            element.className = `feedback feedback-${type}`;
            element.innerHTML = "";

            const messageNode = document.createElement("span");
            messageNode.textContent = message;
            element.appendChild(messageNode);

            if (retry) {
                const button = document.createElement("button");
                button.type = "button";
                button.className = "retry-button";
                button.textContent = "Retry";
                button.addEventListener("click", retry, { once: true });
                element.appendChild(button);
            }
        }
    };
})();