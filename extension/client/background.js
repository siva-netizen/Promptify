// background.js

const API_URL = "http://localhost:8000/refine"; // Default local, configurable

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "REFINE_PROMPT") {
        handleRefineRequest(request, sendResponse);
        return true; // Keep channel open for async response
    }
});

async function handleRefineRequest(request, sendResponse) {
    try {
        const { prompt } = request;

        // Get settings from storage
        const settings = await chrome.storage.sync.get(['apiUrl', 'apiKey', 'provider', 'model']);
        const endpoint = settings.apiUrl || API_URL;

        const payload = {
            prompt: prompt,
            model_provider: settings.provider || 'cerebras',
            model_name: settings.model,
            api_key: settings.apiKey
        };

        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const err = await response.text();
            throw new Error(`API Error: ${response.status} - ${err}`);
        }

        const data = await response.json();
        sendResponse({ success: true, refined: data.refined_prompt });

    } catch (error) {
        console.error("Refinement failed:", error);
        sendResponse({ success: false, error: error.message });
    }
}
