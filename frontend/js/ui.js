/**
 * UI Rendering & DOM Manipulation Module (Modern UI Redesign)
 */
const UI = {
    // DOM Cache
    elements: {},

    init() {
        this.cacheElements();
    },

    cacheElements() {
        this.elements = {
            headerModelVersion: document.getElementById("header-model-version"),
            headerModelAccuracy: document.getElementById("header-model-accuracy"),
            apiStatusBadge: document.getElementById("api-status-badge"),
            apiStatusText: document.getElementById("api-status-text"),
            form: document.getElementById("prediction-form"),
            stateEmpty: document.getElementById("state-empty"),
            stateLoading: document.getElementById("state-loading"),
            stateError: document.getElementById("state-error"),
            stateResult: document.getElementById("state-result"),
            errorTitle: document.getElementById("error-title"),
            errorMessage: document.getElementById("error-message"),
            severityBanner: document.getElementById("severity-card-banner"),
            severityTitle: document.getElementById("severity-title"),
            confidencePercent: document.getElementById("confidence-percent"),
            probMinorVal: document.getElementById("prob-minor-val"),
            probMinorBar: document.getElementById("prob-minor-bar"),
            probMajorVal: document.getElementById("prob-major-val"),
            probMajorBar: document.getElementById("prob-major-bar"),
            probFatalVal: document.getElementById("prob-fatal-val"),
            probFatalBar: document.getElementById("prob-fatal-bar"),
            shapFactorsList: document.getElementById("shap-factors-list"),
            resModelVersion: document.getElementById("res-model-version"),
            resModelAlgo: document.getElementById("res-model-algo"),
            historyTableBody: document.getElementById("history-tbody"),
            historyCount: document.getElementById("history-count")
        };
    },

    /**
     * Update API Health status chip in header
     */
    setApiStatus(online, modelInfo = {}) {
        const dot = this.elements.apiStatusBadge.querySelector(".status-dot");
        if (online) {
            dot.className = "status-dot online";
            this.elements.apiStatusText.textContent = "API Connected";
            if (modelInfo.active_model) {
                this.elements.headerModelVersion.textContent = `${modelInfo.active_model} (XGBoost)`;
            }
            if (modelInfo.model_accuracy) {
                this.elements.headerModelAccuracy.textContent = modelInfo.model_accuracy;
            }
        } else {
            dot.className = "status-dot offline";
            this.elements.apiStatusText.textContent = "API Offline";
        }
    },

    /**
     * Populate select options dynamically from feature schema
     */
    populateFormOptions(schema) {
        for (const [key, field] of Object.entries(schema)) {
            const el = document.getElementById(`input-${key}`);
            if (!el) continue;

            if (field.type === "categorical" && field.options) {
                el.innerHTML = "";
                field.options.forEach(opt => {
                    const option = document.createElement("option");
                    option.value = opt;
                    option.textContent = opt;
                    if (opt === field.default) option.selected = true;
                    el.appendChild(option);
                });
            } else if (field.type === "numerical" && field.default !== undefined) {
                el.value = field.default;
            } else if (field.type === "boolean" && field.default !== undefined) {
                el.checked = Boolean(field.default);
            }
        }
    },

    /**
     * Switch result panel states: 'empty', 'loading', 'error', 'result'
     */
    setResultState(state, errorMsg = "") {
        const states = [this.elements.stateEmpty, this.elements.stateLoading, this.elements.stateError, this.elements.stateResult];
        states.forEach(s => s.classList.remove("active"));

        if (state === "empty") this.elements.stateEmpty.classList.add("active");
        else if (state === "loading") this.elements.stateLoading.classList.add("active");
        else if (state === "error") {
            this.elements.stateError.classList.add("active");
            if (errorMsg) this.elements.errorMessage.textContent = errorMsg;
        } else if (state === "result") this.elements.stateResult.classList.add("active");
    },

    /**
     * Render Prediction & Explanation payload into result panel
     */
    renderPredictionResult(data) {
        const pred = data.prediction;
        const explanation = data.explanation || [];
        const model = data.model || {};

        // 1. Hero Severity Banner
        const severityClass = pred.class.toLowerCase(); // 'minor', 'major', 'fatal'
        this.elements.severityBanner.className = `hero-severity-card ${severityClass}`;
        this.elements.severityTitle.textContent = pred.class.toUpperCase();

        // 2. Confidence
        const confidencePct = (pred.probability * 100).toFixed(2);
        this.elements.confidencePercent.textContent = `${confidencePct}%`;

        // 3. Class Probabilities
        const probs = pred.probabilities || {};
        const pMinor = probs.Minor ? (probs.Minor * 100).toFixed(1) : "0";
        const pMajor = probs.Major ? (probs.Major * 100).toFixed(1) : "0";
        const pFatal = probs.Fatal ? (probs.Fatal * 100).toFixed(1) : "0";

        this.elements.probMinorVal.textContent = `${pMinor}%`;
        this.elements.probMinorBar.style.width = `${pMinor}%`;

        this.elements.probMajorVal.textContent = `${pMajor}%`;
        this.elements.probMajorBar.style.width = `${pMajor}%`;

        this.elements.probFatalVal.textContent = `${pFatal}%`;
        this.elements.probFatalBar.style.width = `${pFatal}%`;

        // 4. SHAP Influential Factors Cards
        this.elements.shapFactorsList.innerHTML = "";
        if (explanation.length === 0) {
            this.elements.shapFactorsList.innerHTML = "<p class='box-desc'>No feature importances returned.</p>";
        } else {
            const maxImp = Math.max(...explanation.map(e => e.importance || 0.01), 0.01);

            explanation.forEach(item => {
                const barPct = Math.min(Math.round((item.importance / maxImp) * 100), 100);
                const impactClass = item.impact === "Increases Risk" ? "impact-risk" : "impact-safe";

                const factorDiv = document.createElement("div");
                factorDiv.className = "shap-card-item";
                factorDiv.innerHTML = `
                    <div class="shap-top-row">
                        <span class="shap-title">${item.feature}</span>
                        <span class="impact-pill ${impactClass}">${item.impact || "Influential Factor"}</span>
                    </div>
                    <div class="shap-meter-track">
                        <div class="shap-meter-fill" style="width: ${barPct}%"></div>
                    </div>
                `;
                this.elements.shapFactorsList.appendChild(factorDiv);
            });
        }

        // 5. Model Footnote Details
        this.elements.resModelVersion.textContent = model.version || "V4";
        this.elements.resModelAlgo.textContent = model.algorithm || "Optimized XGBoost Pipeline";

        // Show Result View State
        this.setResultState("result");
    },

    /**
     * Render Session Prediction History
     */
    renderHistory(historyList) {
        this.elements.historyCount.textContent = historyList.length;

        if (historyList.length === 0) {
            this.elements.historyTableBody.innerHTML = `
                <tr class="empty-tr">
                    <td colspan="8">No predictions recorded in this session yet.</td>
                </tr>
            `;
            return;
        }

        this.elements.historyTableBody.innerHTML = "";
        historyList.forEach((item, index) => {
            const tr = document.createElement("tr");
            const severityClass = item.prediction.class.toLowerCase();
            const topFactor = (item.explanation && item.explanation[0]) ? item.explanation[0].feature : "N/A";

            tr.innerHTML = `
                <td><strong>${index + 1}</strong></td>
                <td>${item.timestamp}</td>
                <td>${item.features.city}, ${item.features.state}</td>
                <td>${item.features.weather}, ${item.features.road_type} (${item.features.hour}:00)</td>
                <td>${item.features.vehicles_involved}</td>
                <td><span class="impact-pill ${severityClass === 'fatal' ? 'impact-risk' : 'impact-safe'}">${item.prediction.class}</span></td>
                <td>${(item.prediction.probability * 100).toFixed(1)}%</td>
                <td>${topFactor}</td>
            `;
            this.elements.historyTableBody.appendChild(tr);
        });
    }
};
