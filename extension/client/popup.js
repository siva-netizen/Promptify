// popup.js
document.addEventListener('DOMContentLoaded', () => {
    // Load saved settings
    chrome.storage.sync.get(['provider', 'model', 'apiKey', 'apiUrl'], (items) => {
        if (items.provider) document.getElementById('provider').value = items.provider;
        if (items.model) document.getElementById('modelName').value = items.model;
        if (items.apiKey) document.getElementById('apiKey').value = items.apiKey;
        if (items.apiUrl) document.getElementById('apiUrl').value = items.apiUrl;
    });

    document.getElementById('save').addEventListener('click', () => {
        const provider = document.getElementById('provider').value;
        const model = document.getElementById('modelName').value;
        const apiKey = document.getElementById('apiKey').value;
        const apiUrl = document.getElementById('apiUrl').value;

        chrome.storage.sync.set({
            provider,
            model,
            apiKey,
            apiUrl
        }, () => {
            const status = document.getElementById('status');
            status.textContent = 'Settings saved!';
            setTimeout(() => status.textContent = '', 2000);
        });
    });
});
