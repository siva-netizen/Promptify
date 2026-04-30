// popup.js
document.addEventListener('DOMContentLoaded', () => {
    // Load saved settings
    chrome.storage.sync.get(['provider', 'model', 'apiKey', 'outputFormat'], (items) => {
        if (items.provider) document.getElementById('provider').value = items.provider;
        if (items.model) document.getElementById('modelName').value = items.model;
        if (items.apiKey) document.getElementById('apiKey').value = items.apiKey;
        if (items.outputFormat) document.getElementById('outputFormat').value = items.outputFormat;
    });

    document.getElementById('save').addEventListener('click', () => {
        const provider = document.getElementById('provider').value;
        const model = document.getElementById('modelName').value;
        const apiKey = document.getElementById('apiKey').value;
        const outputFormat = document.getElementById('outputFormat').value;

        chrome.storage.sync.set({ provider, model, apiKey, outputFormat }, () => {
            const status = document.getElementById('status');
            status.textContent = 'Settings saved!';
            setTimeout(() => status.textContent = '', 2000);
        });
    });
});
