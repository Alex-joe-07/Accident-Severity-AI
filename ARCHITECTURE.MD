Create:

architecture.md

Document the complete architecture.

Preferred architecture:

Frontend:
HTML
CSS
Vanilla JavaScript

Backend:
Python
Flask

ML:
scikit-learn / compatible saved model
joblib

Current model:
V4 .pkl

Future model:
Replaceable model adapter

Architecture:

User
 ↓
Vanilla JS UI
 ↓
Fetch API
 ↓
Flask REST API
 ↓
Model Service
 ↓
V4 .pkl
 ↓
Prediction
 ↓
Explanation generation
 ↓
JSON response
 ↓
Frontend
 ↓
Prediction + Influential Factors

Create a model abstraction such as:

model_service.py

The frontend must NEVER directly access .pkl files.

Suggested project structure:

project-root/
│
├── v4-model/
│   ├── dataset/
│   │   └── existing CSV
│   ├── model/
│   │   ├── existing V4 .pkl files
│   │   └── ...
│   └── *.ipynb
│
├── backend/
│   ├── app.py
│   ├── model_service.py
│   ├── schemas.py
│   ├── config.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── app.js
│   │   ├── api.js
│   │   └── ui.js
│   └── assets/
│
├── prd.md
├── architecture.md
├── rules.md
├── phases.md
├── design.md
└── memory.md

The exact structure may be adjusted if necessary, but maintain clear separation between:

UI
API
ML
configuration
documentation
