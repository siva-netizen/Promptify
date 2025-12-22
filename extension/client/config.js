// config.js
const CONFIG = {
    // Hardcoded API URL for Appwrite Cloud Backend
    API_URL: "https://6948e463003a88836e0a.nyc.appwrite.run/refine"
};

// Export for use in background service worker (if modules used) or global scope
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
