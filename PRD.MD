Create:

prd.md

It must document:

PROJECT OVERVIEW

Explain that the system predicts road accident severity from accident, road and environmental conditions.

TARGET USERS:

Primary:
- Researchers/students
- Road safety analysts
- Academic evaluators

Potential future:
- Traffic authorities
- Road safety departments
- Insurance/risk analysis organizations
- Fleet/logistics companies

CORE PROBLEM:

Road accidents differ in severity depending on multiple environmental, road and traffic-related conditions.

The system attempts to predict accident severity and provide interpretable information about influential factors.

CORE FEATURES:

1. Accident severity prediction
2. Minor/Major/Fatal classification
3. Input form for accident/road conditions
4. Prediction result card
5. Confidence/probability display if available from the model
6. Influential factors section
7. Model information
8. Prediction history for current browser session
9. Responsive UI
10. Error and validation handling
11. Loading state
12. Empty state
13. API connection status

IMPORTANT UX:

User enters conditions.

System sends data to backend.

Backend loads ML model.

Backend returns prediction.

Frontend displays:

Predicted Severity:
MINOR / MAJOR / FATAL

Then display:

"Influential Factors"

Only display explanation data actually returned by the backend.

NEVER fabricate AI explanations.