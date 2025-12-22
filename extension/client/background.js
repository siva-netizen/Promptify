// background.js
try {
    importScripts('config.js');
} catch (e) {
    console.error(e);
}

const API_URL = "http://localhost:8000/refine"; // Default local, configurable

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "REFINE_PROMPT") {
        handleRefineRequest(request, sendResponse);
        return true; // Keep channel open for async response
    }
});

async function handleRefineRequest(request, sendResponse) {
    console.log("[Background] Handling refine request:", request);
    try {
        const { prompt } = request;

        // Get settings from storage (API URL is now hardcoded)
        const settings = await chrome.storage.sync.get(['apiKey', 'provider', 'model']);

        // Use hardcoded URL from config.js (loaded via manifest or import)
        // Note: ensuring config.js is loaded in background.html/manifest
        const endpoint = CONFIG.API_URL;

        console.log(`[Background] Using endpoint: ${endpoint}`);

        const payload = {
            prompt: prompt,
            model_provider: settings.provider || 'cerebras',
            model_name: settings.model,
            api_key: settings.apiKey
        };

        // Create a timeout signal
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s timeout

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                const err = await response.text();
                throw new Error(`API Error: ${response.status} - ${err}`);
            }

            const data = await response.json();
            console.log("[Background] Refinement successful");
            sendResponse({ success: true, refined: data.refined_prompt });

        } catch (fetchError) {
            clearTimeout(timeoutId);
            throw fetchError;
        }

    } catch (error) {
        console.error("[Background] Refinement failed:", error);
        sendResponse({ success: false, error: error.message });
    }
}
