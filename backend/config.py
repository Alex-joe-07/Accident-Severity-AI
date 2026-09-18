import os

# Root directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Active model configuration
ACTIVE_MODEL_VERSION = os.environ.get("MODEL_VERSION", "V4")

# Model paths
V4_MODEL_DIR = os.path.join(BASE_DIR, "v4 model", "model")
V4_MODEL_PATH = os.path.join(V4_MODEL_DIR, "v4_best_accident_severity_model.pkl")
V4_ENCODER_PATH = os.path.join(V4_MODEL_DIR, "v4_label_encoder.pkl")
V4_DATASET_PATH = os.path.join(BASE_DIR, "v4 model", "dataset", "road_accident_severity_project_dataset_20000.csv")

# Flask Server Configuration
HOST = "127.0.0.1"
PORT = 5000
DEBUG = True

# Valid choices for dropdown features (discovered from V4 dataset analysis)
FEATURE_SCHEMA = {
    "city": {
        "type": "categorical",
        "label": "City",
        "options": ["Kolkata", "Pune", "Chennai", "Mumbai", "Chandigarh", "Hyderabad", "Bangalore", "Delhi"],
        "default": "Kolkata"
    },
    "state": {
        "type": "categorical",
        "label": "State",
        "options": ["West Bengal", "Maharashtra", "Tamil Nadu", "Punjab", "Telangana", "Karnataka", "Delhi"],
        "default": "West Bengal"
    },
    "hour": {
        "type": "numerical",
        "label": "Hour of Day (0-23)",
        "min": 0,
        "max": 23,
        "default": 16
    },
    "day_of_week": {
        "type": "categorical",
        "label": "Day of Week",
        "options": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "default": "Friday"
    },
    "is_weekend": {
        "type": "boolean",
        "label": "Is Weekend",
        "options": [0, 1],
        "default": 0
    },
    "road_type": {
        "type": "categorical",
        "label": "Road Type",
        "options": ["highway", "urban", "rural"],
        "default": "highway"
    },
    "lanes": {
        "type": "numerical",
        "label": "Number of Lanes",
        "min": 1,
        "max": 6,
        "default": 3
    },
    "traffic_signal": {
        "type": "boolean",
        "label": "Traffic Signal Present",
        "options": [0, 1],
        "default": 1
    },
    "weather": {
        "type": "categorical",
        "label": "Weather Condition",
        "options": ["clear", "fog", "rain"],
        "default": "clear"
    },
    "visibility": {
        "type": "categorical",
        "label": "Visibility Level",
        "options": ["high", "medium", "low"],
        "default": "high"
    },
    "temperature": {
        "type": "numerical",
        "label": "Temperature (°C)",
        "min": 0,
        "max": 50,
        "default": 28
    },
    "traffic_density": {
        "type": "categorical",
        "label": "Traffic Density",
        "options": ["low", "medium", "high"],
        "default": "medium"
    },
    "cause": {
        "type": "categorical",
        "label": "Primary Cause",
        "options": ["distraction", "drunk driving", "weather", "overspeeding", "poor road"],
        "default": "overspeeding"
    },
    "vehicles_involved": {
        "type": "numerical",
        "label": "Vehicles Involved",
        "min": 1,
        "max": 10,
        "default": 2
    },
    "is_peak_hour": {
        "type": "boolean",
        "label": "Is Peak Hour",
        "options": [0, 1],
        "default": 0
    }
}
