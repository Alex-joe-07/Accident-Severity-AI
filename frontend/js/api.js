/**
 * API Service for Backend Communication
 */
const API = {
    // Dynamic Base URL detection:
    // If hosted on Netlify / static origin without backend, fallback to window.API_BASE_URL or localhost
    get baseUrl() {
        if (window.API_BASE_URL) return window.API_BASE_URL;
        if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
            return "";
        }
        // Fallback for local development testing when static HTML opened directly
        return "http://127.0.0.1:5000";
    },

    /**
     * Helper to perform fetch requests with error handling
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const defaultHeaders = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        };

        const config = {
            ...options,
            headers: {
                ...defaultHeaders,
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `HTTP Error ${response.status}`);
            }

            return data;
        } catch (error) {
            console.warn(`API request to ${url} failed:`, error);
            throw error;
        }
    },

    /**
     * Check backend API health & active model status
     */
    async checkHealth() {
        return await this.request("/api/health");
    },

    /**
     * Fetch feature schema (dropdown options, ranges, defaults)
     */
    async getFeatureSchema() {
        return await this.request("/api/features");
    },

    /**
     * Fetch active model metadata
     */
    async getModelInfo() {
        return await this.request("/api/model-info");
    },

    /**
     * Send prediction request
     * Request format: { "features": { ... } }
     */
    async predict(featuresPayload) {
        return await this.request("/api/predict", {
            method: "POST",
            body: JSON.stringify({
                features: featuresPayload
            })
        });
    }
};
