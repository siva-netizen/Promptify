// config.js
const CONFIG = {
    API_URL: fetch("http://localhost:8000/health", { signal: AbortSignal.timeout(1000) })
        .then(res => res.ok ? "http://localhost:8000/refine" : "https://6948e463003a88836e0a.nyc.appwrite.run/refine")
        .catch(() => "https://6948e463003a88836e0a.nyc.appwrite.run/refine")
};

// Export for use in background service worker (if modules used) or global scope
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
