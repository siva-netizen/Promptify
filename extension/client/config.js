// config.js
const CONFIG = {
    // Hardcoded API URL for Appwrite Cloud Backend
    API_URL: "https://6948346f001194e559d2.nyc.appwrite.run/refine"
};

// Export for use in background service worker (if modules used) or global scope
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
