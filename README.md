# 🚦 Explainable AI Framework for Road Accident Severity & Influential Factor Analysis

[![Live Demo](https://img.shields.io/badge/Live_Demo-Netlify-00C7B7.svg?style=for-the-badge&logo=netlify)](https://accident-severity-ai-v4.netlify.app/)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/backend-Flask-green.svg)](https://flask.palletsprojects.com/)
[![ML Model](https://img.shields.io/badge/ML-XGBoost-orange.svg)](https://xgboost.readthedocs.io/)
[![XAI](https://img.shields.io/badge/Explainability-SHAP-purple.svg)](https://shap.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

> 🌐 **Live Web Demo**: [https://accident-severity-ai-v4.netlify.app/](https://accident-severity-ai-v4.netlify.app/)  
> *Click the link above to test the live interactive web interface, evaluate accident conditions, and explore SHAP explainability feature cards.*

An end-to-end Machine Learning web application designed to predict road accident severity (**Minor**, **Major**, **Fatal**) based on environmental, road infrastructure, temporal, and traffic parameters. Integrates **SHAP (SHapley Additive exPlanations)** to explain the top driving risk factors for every prediction in real time.

Built with a modular **Plug-and-Play Model Adapter Architecture** so future ML models (V5, V6, etc.) can be plugged in without modifying any frontend application code.

---

## 🤖 ONE-CLICK AI AGENT INSTALLATION PROMPT
> **For users using AI Assistants (Google Antigravity, GitHub Copilot Workspace, Cursor, ChatGPT Code Interpreter, etc.):**  
> If you opened this repository in an AI editor/agent and want it to configure and launch the project automatically, **copy and paste the prompt below into your AI chat box**:

```text
Please set up and run this "Explainable AI Road Accident Severity Framework" project on my machine:

1. Create a Python virtual environment (if not present) and activate it.
2. Install all required dependencies from backend/requirements.txt (including flask, flask-cors, numpy, pandas, scikit-learn, xgboost, shap, joblib).
3. Verify that the pre-trained V4 model file exists at: v4 model/model/v4_best_accident_severity_model.pkl and encoder at v4 model/model/v4_label_encoder.pkl.
4. Run the automated test suite with: python -m unittest tests/test_api_and_model.py
5. Start the Flask application server by executing: python run_server.py
6. Report back with the local URL (http://127.0.0.1:5000) once the application server is live and connected.
```

---

## 🌟 Key Features

- 🚘 **Accident Severity Classification**: Predicts crash severity into 3 classes (`Minor`, `Major`, `Fatal`) with confidence probability distribution.
- 🧠 **Real SHAP Explainability**: Quantifies feature-level risk contributions (`Increases Risk` / `Reduces Risk`) for individual predictions using `shap.TreeExplainer`.
- 🔌 **Plug & Play Model Adapter Pattern**: Decouples ML model versions (V4, V5, V6) from the REST API & frontend via `BaseModelAdapter`.
- ⚡ **Preset Scenario Engine**: 1-click test scenarios ("Highway Night Collision", "Urban Rush Hour", "Foggy & Wet", "Clear Daylight").
- 🎨 **Modern AI Dashboard UI**: Responsive interface built with HTML5, CSS3, custom toggle switches, and Vanilla JavaScript.
- 📜 **Session Prediction History**: Keeps track of predictions run during the active browser session.

---

## 📋 Prerequisites

Before installing the project, ensure you have:
- **Python**: Version 3.9 or higher installed (`python --version`)
- **Git**: Installed on your system (`git --version`)
- **Pip**: Python package manager (`pip --version`)

---

## ⚙️ Manual Installation & Setup Instructions

Follow these step-by-step commands to install and configure the project on your system:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create and Activate a Virtual Environment (Recommended)

- **On Windows (PowerShell / Command Prompt)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```

- **On macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Backend Dependencies
Install all required libraries (Flask, XGBoost, SHAP, Scikit-Learn, Pandas, etc.):
```bash
pip install -r backend/requirements.txt
```

### 4. Verify Model Files
Ensure that the pre-trained V4 model artifacts are located in the dataset directory:
- Model: `v4 model/model/v4_best_accident_severity_model.pkl`
- Label Encoder: `v4 model/model/v4_label_encoder.pkl`
- Dataset: `v4 model/dataset/road_accident_severity_project_dataset_20000.csv`

### 5. Run Automated Unit Tests (Optional Verification)
Verify that the model adapter and REST API endpoints are functioning properly:
```bash
python -m unittest tests/test_api_and_model.py
```
*(All 5 tests should output `OK`)*

### 6. Start the Flask Server
Run the launcher script to start the web application:
```bash
python run_server.py
```

### 7. Open Web Browser
Once started, open your web browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🛠️ Project Architecture & File Structure

```text
├── v4 model/
│   ├── dataset/
│   │   └── road_accident_severity_project_dataset_20000.csv
│   ├── model/
│   │   ├── v4_best_accident_severity_model.pkl
│   │   └── v4_label_encoder.pkl
│   └── v4_train_model.ipynb
├── backend/
│   ├── app.py                    # Flask Server & REST Endpoints
│   ├── config.py                 # Configuration & Feature Schemas
│   ├── model_service.py          # Model Adapter Factory / Manager
│   ├── requirements.txt          # Python dependencies
│   └── adapters/
│       ├── base_adapter.py       # Abstract Base Class (BaseModelAdapter)
│       └── v4_adapter.py         # V4 Model Adapter & SHAP Engine
├── frontend/
│   ├── index.html                # Single Page Web UI
│   ├── css/
│   │   └── style.css             # Modern Slate/Indigo AI Dashboard Styles
│   └── js/
│       ├── api.js                # Fetch API Client
│       ├── ui.js                 # DOM Renderer & Result Cards
│       └── app.js                # Application Logic & Event Handlers
├── tests/
│   └── test_api_and_model.py     # Automated API & Model Unit Tests
├── run_server.py                 # Root Application Launcher
└── README.md                     # Project Documentation
```

---

## 🔌 How to Plug in a New Model Version (V5 / V6 / V7)

The project is built on a **Model Adapter Pattern** to ensure future model upgrades require 0 changes to the frontend.

To upgrade to a new model version (e.g., **V5**):
1. Save your trained V5 `.pkl` model and encoder files under `v5 model/model/`.
2. Create a new adapter file: `backend/adapters/v5_adapter.py` inheriting from `BaseModelAdapter`:
   ```python
   from backend.adapters.base_adapter import BaseModelAdapter

   class V5ModelAdapter(BaseModelAdapter):
       def load_model(self): ...
       def predict(self, raw_features): ...
       def get_metadata(self): ...
   ```
3. Update `ACTIVE_MODEL_VERSION = "V5"` in `backend/config.py`.
4. Restart the backend server with `python run_server.py`. The web interface will seamlessly render predictions and explanations from V5!

---

## 📡 API Endpoints Reference

| Endpoint | Method | Description |
|---|---|---|
| `/` | `GET` | Serves the Frontend Single Page Application |
| `/api/health` | `GET` | Returns backend health status & active model version |
| `/api/features` | `GET` | Returns form schema (options, defaults, numerical min/max) |
| `/api/model-info` | `GET` | Returns active model metadata (accuracy, algorithm, records) |
| `/api/predict` | `POST` | Accepts feature JSON payload, returns severity class, probabilities, and SHAP factor explanations |

### Sample `POST /api/predict` Payload
```json
{
  "features": {
    "city": "Mumbai",
    "state": "Maharashtra",
    "hour": 18,
    "day_of_week": "Wednesday",
    "is_weekend": 0,
    "road_type": "urban",
    "lanes": 3,
    "traffic_signal": 1,
    "weather": "clear",
    "visibility": "high",
    "temperature": 32,
    "traffic_density": "high",
    "cause": "distraction",
    "vehicles_involved": 2,
    "is_peak_hour": 1
  }
}
```

### Sample API Response
```json
{
  "success": true,
  "prediction": {
    "class": "Fatal",
    "class_id": 3,
    "probability": 0.6018,
    "probabilities": {
      "Fatal": 0.6018,
      "Major": 0.0379,
      "Minor": 0.3603
    }
  },
  "explanation": [
    {
      "feature": "Primary Cause: distraction",
      "impact": "Increases Risk",
      "importance": 0.0612
    }
  ],
  "model": {
    "version": "V4",
    "algorithm": "Optimized XGBoost Classifier",
    "accuracy": "68.90%"
  }
}
```

---

## 🎓 Academic Attribution & License

- **Project Title**: Explainable AI-Driven Framework for Road Accident Severity and Influential Factor Analysis
- **Benchmark Model**: V4 (Optimized XGBoost Classifier Pipeline — 68.90% Accuracy)
- **License**: [MIT License](LICENSE)
