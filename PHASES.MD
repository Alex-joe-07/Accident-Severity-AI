Create:

phases.md

PHASE 1 — PROJECT FOUNDATION

- Create project structure
- Create documentation files
- Create frontend/backend separation
- Confirm V4 model location

PHASE 2 — UI FOUNDATION

- Create application shell
- Navigation/header
- Dashboard
- Prediction section
- Result section
- Explanation section

PHASE 3 — PREDICTION FORM

Create fields based on the actual V4 model input features.

IMPORTANT:

Inspect the V4 notebook/model metadata/code to determine the actual required input features.

Do not invent model fields.

Add:
- labels
- inputs/selects
- validation
- reset button
- predict button

PHASE 4 — BACKEND

Create Flask server.

Implement:

GET /api/health

POST /api/predict

Load V4 model.

Connect model_service.py.

PHASE 5 — FRONTEND/API INTEGRATION

Connect Fetch API.

Flow:

form submit
→ validation
→ loading
→ API request
→ prediction response
→ result UI

PHASE 6 — RESULT EXPERIENCE

Display:

Prediction:
MINOR / MAJOR / FATAL

Probability/confidence if available.

Display influential factors.

Display model information.

PHASE 7 — ERROR STATES

Implement:

loading
error
empty
API offline
invalid input
prediction failure

PHASE 8 — RESPONSIVE POLISH

Desktop
Tablet
Mobile

PHASE 9 — DEMO PREPARATION

Create clean sample inputs.

Make the demo flow fast.

Ensure teacher can understand:

Input
→ Prediction
→ Explanation

PHASE 10 — FUTURE MODEL SWAP

Document how to replace:

v4 model

with:

future model

without changing frontend architecture.