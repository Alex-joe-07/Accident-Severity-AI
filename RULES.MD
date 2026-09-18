Create:

rules.md

RULES:

A. GENERAL

- Keep code simple.
- Prefer readable code over clever code.
- Do not over-engineer.
- Do not add unnecessary libraries.
- Do not introduce unnecessary animations.
- Do not create unnecessary abstractions.
- Keep the MVP achievable within one week.

B. FRONTEND

Use:

HTML5
CSS3
Vanilla JavaScript

Do NOT use:

React
Next.js
Vue
Angular

unless explicitly requested later.

Use Fetch API for backend communication.

C. BACKEND

Use Flask.

Create REST endpoints.

Primary endpoint:

POST /api/predict

Optional:

GET /api/health

D. MACHINE LEARNING

Use the existing V4 .pkl model.

Do not retrain the model from the frontend.

Do not modify the model.

Do not fabricate prediction results.

Do not hardcode predictions.

Do not claim unsupported accuracy.

The model must be loaded once when the backend starts rather than reloaded on every request.

E. DATA LEAKAGE

NEVER use:

- target-derived information
- future accident outcomes
- manually fabricated labels
- test-set information
- hardcoded prediction rules

F. EXPLAINABILITY

The project requires explainability.

If SHAP is implemented and compatible with the model:

use SHAP.

If SHAP is not currently available:

do NOT fake SHAP values.

Instead return legitimate model feature importance where appropriate and label it correctly.

G. ERROR HANDLING

Backend must handle:

- missing input
- invalid input
- wrong data type
- model loading failure
- prediction failure
- malformed JSON

Frontend must display human-readable errors.

Never expose Python stack traces to users.

H. VALIDATION

Validate every user input.

Do not allow invalid values to reach the model.

I. MODEL REPLACEMENT

The application must allow:

V4 → V5 → V6 → future model

without redesigning the frontend.

The API response structure must remain stable.