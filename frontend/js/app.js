/**
 * Main Application Logic & Controller (Static Fallback & Remote API Support)
 */
const DEFAULT_FEATURE_SCHEMA = {
    city: {
        type: "categorical",
        label: "City",
        options: ["Kolkata", "Pune", "Chennai", "Mumbai", "Chandigarh", "Hyderabad", "Bangalore", "Delhi"],
        default: "Kolkata"
    },
    state: {
        type: "categorical",
        label: "State",
        options: ["West Bengal", "Maharashtra", "Tamil Nadu", "Punjab", "Telangana", "Karnataka", "Delhi"],
        default: "West Bengal"
    },
    hour: {
        type: "numerical",
        label: "Hour of Day",
        min: 0,
        max: 23,
        default: 16
    },
    day_of_week: {
        type: "categorical",
        label: "Day of Week",
        options: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        default: "Friday"
    },
    is_weekend: {
        type: "boolean",
        label: "Is Weekend",
        options: [0, 1],
        default: 0
    },
    road_type: {
        type: "categorical",
        label: "Road Classification",
        options: ["highway", "urban", "rural"],
        default: "highway"
    },
    lanes: {
        type: "numerical",
        label: "Number of Lanes",
        min: 1,
        max: 6,
        default: 3
    },
    traffic_signal: {
        type: "boolean",
        label: "Traffic Signal Present",
        options: [0, 1],
        default: 1
    },
    weather: {
        type: "categorical",
        label: "Weather Condition",
        options: ["clear", "fog", "rain"],
        default: "clear"
    },
    visibility: {
        type: "categorical",
        label: "Visibility Level",
        options: ["high", "medium", "low"],
        default: "high"
    },
    temperature: {
        type: "numerical",
        label: "Temperature (°C)",
        min: 0,
        max: 50,
        default: 28
    },
    traffic_density: {
        type: "categorical",
        label: "Traffic Density",
        options: ["low", "medium", "high"],
        default: "medium"
    },
    cause: {
        type: "categorical",
        label: "Primary Cause",
        options: ["distraction", "drunk driving", "weather", "overspeeding", "poor road"],
        default: "overspeeding"
    },
    vehicles_involved: {
        type: "numerical",
        label: "Vehicles Involved",
        min: 1,
        max: 10,
        default: 2
    },
    is_peak_hour: {
        type: "boolean",
        label: "Is Peak Hour",
        options: [0, 1],
        default: 0
    }
};

const App = {
    featureSchema: DEFAULT_FEATURE_SCHEMA,
    history: [],

    // Preset Scenarios
    presets: {
        highway_night: {
            city: "Kolkata",
            state: "West Bengal",
            hour: 2,
            day_of_week: "Saturday",
            is_weekend: 1,
            road_type: "highway",
            lanes: 4,
            traffic_signal: 0,
            weather: "fog",
            visibility: "low",
            temperature: 15,
            traffic_density: "low",
            cause: "overspeeding",
            vehicles_involved: 3,
            is_peak_hour: 0
        },
        urban_peak: {
            city: "Mumbai",
            state: "Maharashtra",
            hour: 18,
            day_of_week: "Wednesday",
            is_weekend: 0,
            road_type: "urban",
            lanes: 3,
            traffic_signal: 1,
            weather: "clear",
            visibility: "high",
            temperature: 32,
            traffic_density: "high",
            cause: "distraction",
            vehicles_involved: 2,
            is_peak_hour: 1
        },
        rainy_fog: {
            city: "Pune",
            state: "Maharashtra",
            hour: 21,
            day_of_week: "Friday",
            is_weekend: 0,
            road_type: "rural",
            lanes: 2,
            traffic_signal: 0,
            weather: "rain",
            visibility: "low",
            temperature: 22,
            traffic_density: "medium",
            cause: "weather",
            vehicles_involved: 2,
            is_peak_hour: 0
        },
        clear_day: {
            city: "Bangalore",
            state: "Karnataka",
            hour: 11,
            day_of_week: "Sunday",
            is_weekend: 1,
            road_type: "highway",
            lanes: 4,
            traffic_signal: 1,
            weather: "clear",
            visibility: "high",
            temperature: 26,
            traffic_density: "low",
            cause: "distraction",
            vehicles_involved: 1,
            is_peak_hour: 0
        }
    },

    async init() {
        UI.init();
        // Immediately populate form using default schema so dropdowns are NEVER blank (e.g. Netlify static host)
        UI.populateFormOptions(this.featureSchema);
        this.bindEvents();
        await this.checkBackendStatus();
        await this.loadSchemaAndForm();
        this.loadHistory();
    },

    bindEvents() {
        // Tab Navigation
        const tabs = document.querySelectorAll(".nav-btn");
        tabs.forEach(tab => {
            tab.addEventListener("click", () => {
                const targetId = tab.getAttribute("data-tab");
                tabs.forEach(t => t.classList.remove("active"));
                tab.classList.add("active");

                document.querySelectorAll(".tab-pane").forEach(content => {
                    content.classList.remove("active");
                });
                const targetPane = document.getElementById(targetId);
                if (targetPane) targetPane.classList.add("active");
            });
        });

        // Form Submit
        const form = document.getElementById("prediction-form");
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            await this.handlePredictionSubmit();
        });

        // Reset Button
        document.getElementById("btn-reset").addEventListener("click", () => {
            form.reset();
            UI.populateFormOptions(this.featureSchema);
            UI.setResultState("empty");
        });

        // Retry Connection Button
        document.getElementById("btn-retry").addEventListener("click", async () => {
            await this.checkBackendStatus();
        });

        // Clear History
        document.getElementById("btn-clear-history").addEventListener("click", () => {
            this.history = [];
            sessionStorage.removeItem("accident_pred_history");
            UI.renderHistory(this.history);
        });

        // Preset Scenario Buttons
        document.querySelectorAll(".btn-scenario").forEach(btn => {
            btn.addEventListener("click", (e) => {
                const btnEl = e.currentTarget;
                const presetKey = btnEl.getAttribute("data-preset");
                if (this.presets[presetKey]) {
                    this.applyPreset(this.presets[presetKey]);
                }
            });
        });

        // Auto-derive Peak Hour & Weekend flags when Hour / Day of week change
        const hourInput = document.getElementById("input-hour");
        const dayInput = document.getElementById("input-day_of_week");

        if (hourInput && dayInput) {
            const updateFlags = () => {
                const hr = parseInt(hourInput.value, 10);
                const day = dayInput.value;

                const isWeekend = (day === "Saturday" || day === "Sunday");
                document.getElementById("input-is_weekend").checked = isWeekend;

                const isPeak = (hr >= 8 && hr <= 10) || (hr >= 17 && hr <= 20);
                document.getElementById("input-is_peak_hour").checked = isPeak;
            };

            hourInput.addEventListener("change", updateFlags);
            dayInput.addEventListener("change", updateFlags);
        }
    },

    async checkBackendStatus() {
        try {
            const health = await API.checkHealth();
            UI.setApiStatus(true, health);
        } catch (error) {
            UI.setApiStatus(false);
        }
    },

    async loadSchemaAndForm() {
        try {
            const res = await API.getFeatureSchema();
            if (res.success && res.features) {
                this.featureSchema = res.features;
                UI.populateFormOptions(this.featureSchema);
            }
        } catch (error) {
            console.warn("API feature schema unavailable, using local default schema:", error);
            // Always ensure form options are populated from default schema when API is unavailable (e.g. Netlify static hosting)
            UI.populateFormOptions(DEFAULT_FEATURE_SCHEMA);
        }
    },

    applyPreset(presetData) {
        for (const [key, val] of Object.entries(presetData)) {
            const el = document.getElementById(`input-${key}`);
            if (!el) continue;

            if (el.type === "checkbox") {
                el.checked = Boolean(val);
            } else {
                el.value = val;
            }
        }
    },

    getFormFeaturesPayload() {
        const payload = {};
        const form = document.getElementById("prediction-form");
        const formData = new FormData(form);

        // Extract select & text/number inputs
        for (const [key, value] of formData.entries()) {
            if (key === "hour" || key === "lanes" || key === "temperature" || key === "vehicles_involved") {
                payload[key] = Number(value);
            } else {
                payload[key] = value;
            }
        }

        // Extract checkboxes/switches explicitly
        payload["is_weekend"] = document.getElementById("input-is_weekend").checked ? 1 : 0;
        payload["is_peak_hour"] = document.getElementById("input-is_peak_hour").checked ? 1 : 0;
        payload["traffic_signal"] = document.getElementById("input-traffic_signal").checked ? 1 : 0;

        return payload;
    },

    async handlePredictionSubmit() {
        const payload = this.getFormFeaturesPayload();
        UI.setResultState("loading");

        try {
            const result = await API.predict(payload);

            if (result.success) {
                UI.renderPredictionResult(result);

                // Add to Session History
                const historyItem = {
                    timestamp: new Date().toLocaleTimeString(),
                    features: payload,
                    prediction: result.prediction,
                    explanation: result.explanation
                };
                this.history.unshift(historyItem);
                this.saveHistory();
                UI.renderHistory(this.history);
            } else {
                UI.setResultState("error", result.error || "Prediction request failed.");
            }
        } catch (error) {
            UI.setResultState("error", "Flask backend API is currently offline. Please start 'python run_server.py' locally or deploy the Flask backend server to Render/Railway to enable live predictions.");
        }
    },

    saveHistory() {
        try {
            sessionStorage.setItem("accident_pred_history", JSON.stringify(this.history));
        } catch (e) {
            console.warn("Could not save history to sessionStorage:", e);
        }
    },

    loadHistory() {
        try {
            const saved = sessionStorage.getItem("accident_pred_history");
            if (saved) {
                this.history = JSON.parse(saved);
                UI.renderHistory(this.history);
            }
        } catch (e) {
            this.history = [];
        }
    }
};

// Initialize App when DOM ready
document.addEventListener("DOMContentLoaded", () => {
    App.init();
});
