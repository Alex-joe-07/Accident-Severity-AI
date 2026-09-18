import os
import joblib
import numpy as np
import pandas as pd
import shap
from typing import Dict, Any, List

from backend.adapters.base_adapter import BaseModelAdapter
import backend.config as config

class V4ModelAdapter(BaseModelAdapter):
    """
    Concrete Model Adapter for V4 Model.
    
    Model Info:
    - Algorithm: Optimized XGBoost Classifier Pipeline
    - Test Accuracy: 68.90%
    - Target Classes: minor, major, fatal
    """

    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.explainer = None
        self.preprocessor = None
        self.xgb_model = None
        self.all_feature_names = []
        self.loaded = False
        self.load_model()

    def load_model(self) -> None:
        if not os.path.exists(config.V4_MODEL_PATH):
            raise FileNotFoundError(f"V4 model file not found at {config.V4_MODEL_PATH}")
        if not os.path.exists(config.V4_ENCODER_PATH):
            raise FileNotFoundError(f"V4 label encoder file not found at {config.V4_ENCODER_PATH}")

        # Load trained sklearn pipeline and label encoder
        self.model = joblib.load(config.V4_MODEL_PATH)
        self.label_encoder = joblib.load(config.V4_ENCODER_PATH)

        # Extract preprocessor and XGBClassifier steps
        self.preprocessor = self.model.named_steps["preprocessor"]
        self.xgb_model = self.model.named_steps["model"]

        # Reconstruct transformed feature names for SHAP mapping
        num_cols = list(self.preprocessor.transformers_[0][2])
        cat_ohe = self.preprocessor.transformers_[1][1].named_steps["onehot"]
        cat_cols = list(self.preprocessor.transformers_[1][2])
        cat_feature_names = list(cat_ohe.get_feature_names_out(cat_cols))
        self.all_feature_names = num_cols + cat_feature_names

        # Initialize SHAP TreeExplainer on XGBClassifier
        try:
            self.explainer = shap.TreeExplainer(self.xgb_model)
        except Exception as e:
            print(f"Warning: SHAP TreeExplainer initialization failed: {e}")
            self.explainer = None

        self.loaded = True
        print(f"V4ModelAdapter loaded successfully! Target classes: {self.label_encoder.classes_}")

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """V4 exact feature engineering function."""
        data = df.copy()

        # Time Cyclical Features
        if "hour" in data.columns:
            hour = pd.to_numeric(data["hour"], errors="coerce").fillna(12)
            data["hour_sin"] = np.sin(2 * np.pi * hour / 24)
            data["hour_cos"] = np.cos(2 * np.pi * hour / 24)

        # Traffic Density Mapping
        if "traffic_density" in data.columns:
            traffic_map = {"low": 0, "medium": 1, "high": 2}
            data["traffic_density_score"] = (
                data["traffic_density"].astype(str).str.lower().map(traffic_map).fillna(1)
            )

        # Visibility Features
        if "visibility" in data.columns:
            visibility_num_map = {"low": 2, "medium": 5, "high": 10}
            # Handle string or numeric visibility
            vis_numeric = data["visibility"].astype(str).str.lower().map(visibility_num_map)
            vis_numeric = vis_numeric.fillna(pd.to_numeric(data["visibility"], errors="coerce")).fillna(5)
            data["visibility_squared"] = vis_numeric ** 2
            data["poor_visibility"] = (vis_numeric < 5).astype(int)

        # Vehicles Features
        if "vehicles_involved" in data.columns:
            vehicles = pd.to_numeric(data["vehicles_involved"], errors="coerce").fillna(1)
            data["vehicles_squared"] = vehicles ** 2
            data["multi_vehicle"] = (vehicles >= 2).astype(int)
            data["high_vehicle_count"] = (vehicles >= 3).astype(int)

        # Lanes Features
        if "lanes" in data.columns:
            lanes = pd.to_numeric(data["lanes"], errors="coerce").fillna(2)
            data["lanes_squared"] = lanes ** 2
            data["multi_lane"] = (lanes >= 3).astype(int)

        # Temperature Features
        if "temperature" in data.columns:
            temp = pd.to_numeric(data["temperature"], errors="coerce").fillna(25)
            data["temperature_squared"] = temp ** 2
            data["extreme_temperature"] = ((temp < 5) | (temp > 40)).astype(int)

        # Interaction Features
        if "is_peak_hour" in data.columns and "traffic_density_score" in data.columns:
            data["peak_traffic"] = data["is_peak_hour"].astype(int) * data["traffic_density_score"].fillna(0)

        if "is_weekend" in data.columns and "is_peak_hour" in data.columns:
            data["weekend_peak"] = data["is_weekend"].astype(int) * data["is_peak_hour"].astype(int)

        if "vehicles_involved" in data.columns and "traffic_density_score" in data.columns:
            vehicles = pd.to_numeric(data["vehicles_involved"], errors="coerce").fillna(1)
            data["vehicle_traffic_interaction"] = vehicles * data["traffic_density_score"].fillna(0)

        if "lanes" in data.columns and "traffic_density_score" in data.columns:
            lanes = pd.to_numeric(data["lanes"], errors="coerce").fillna(2)
            data["lane_traffic_interaction"] = lanes * data["traffic_density_score"].fillna(0)

        return data

    def _format_feature_label(self, raw_feature_name: str, raw_input_val: Any) -> str:
        """Formats encoded/engineered feature names into clean, user-friendly labels."""
        clean = raw_feature_name
        if "_" in clean:
            parts = clean.split("_")
            # Handle one-hot features e.g. road_type_urban -> Road Type: urban
            if len(parts) >= 2 and parts[0] in config.FEATURE_SCHEMA:
                field_label = config.FEATURE_SCHEMA[parts[0]]["label"]
                val = "_".join(parts[1:])
                return f"{field_label}: {val}"
        
        if raw_feature_name in config.FEATURE_SCHEMA:
            field_label = config.FEATURE_SCHEMA[raw_feature_name]["label"]
            return f"{field_label} ({raw_input_val})"

        # Fallback pretty printing
        return raw_feature_name.replace("_", " ").title()

    def predict(self, raw_features: Dict[str, Any]) -> Dict[str, Any]:
        if not self.loaded:
            self.load_model()

        # Sanitize and fill missing features with default schema values
        processed_input = {}
        for key, schema in config.FEATURE_SCHEMA.items():
            if key in raw_features and raw_features[key] is not None:
                val = raw_features[key]
                if schema["type"] == "numerical":
                    try:
                        val = float(val)
                    except (ValueError, TypeError):
                        val = schema["default"]
                elif schema["type"] == "boolean":
                    val = 1 if str(val).lower() in ["1", "true", "yes"] else 0
                processed_input[key] = val
            else:
                processed_input[key] = schema["default"]

        # Convert to single-row DataFrame
        df_raw = pd.DataFrame([processed_input])

        # Apply V4 Feature Engineering
        df_engineered = self.engineer_features(df_raw)

        # Run Model Inference
        pred_class_idx = int(self.model.predict(df_engineered)[0])
        probabilities_array = self.model.predict_proba(df_engineered)[0]

        # Decode Class Label
        class_name_raw = str(self.label_encoder.inverse_transform([pred_class_idx])[0]) # 'minor', 'major', 'fatal'
        class_name = class_name_raw.capitalize() # 'Minor', 'Major', 'Fatal'

        # Map Probabilities
        prob_dict = {}
        for cls_name, prob in zip(self.label_encoder.classes_, probabilities_array):
            prob_dict[cls_name.capitalize()] = round(float(prob), 4)

        current_prob = round(float(probabilities_array[pred_class_idx]), 4)

        # Class ID mapping (1: Minor, 2: Major, 3: Fatal for user clarity)
        class_id_map = {"Minor": 1, "Major": 2, "Fatal": 3}
        class_id = class_id_map.get(class_name, pred_class_idx)

        # Generate Real SHAP Explanation
        explanations: List[Dict[str, Any]] = []
        if self.explainer is not None:
            try:
                X_trans = self.preprocessor.transform(df_engineered)
                shap_res = self.explainer(X_trans)
                # Select SHAP values for predicted class index
                shap_vals_row = shap_res.values[0, :, pred_class_idx]

                # Rank features by absolute SHAP magnitude
                ranked_features = []
                for fname, s_val in zip(self.all_feature_names, shap_vals_row):
                    if len(self.all_feature_names) == len(shap_vals_row):
                        ranked_features.append((fname, float(s_val)))

                ranked_features.sort(key=lambda x: abs(x[1]), reverse=True)

                # Collect top 6 influential factors
                for fname, s_val in ranked_features[:6]:
                    impact_text = "Increases Risk" if s_val > 0 else "Reduces Risk"
                    raw_val = processed_input.get(fname.split("_")[0], "")
                    label = self._format_feature_label(fname, raw_val)
                    explanations.append({
                        "feature": label,
                        "raw_feature": fname,
                        "importance": round(abs(s_val), 4),
                        "impact": impact_text,
                        "shap_value": round(s_val, 4)
                    })
            except Exception as e:
                print(f"SHAP explanation calculation warning: {e}")

        # Fallback to feature importances if SHAP failed
        if not explanations and hasattr(self.xgb_model, "feature_importances_"):
            importances = self.xgb_model.feature_importances_
            ranked = sorted(zip(self.all_feature_names, importances), key=lambda x: x[1], reverse=True)
            for fname, imp in ranked[:6]:
                raw_val = processed_input.get(fname.split("_")[0], "")
                label = self._format_feature_label(fname, raw_val)
                explanations.append({
                    "feature": label,
                    "raw_feature": fname,
                    "importance": round(float(imp), 4),
                    "impact": "Influential Factor"
                })

        return {
            "success": True,
            "prediction": {
                "class": class_name,
                "class_id": class_id,
                "probability": current_prob,
                "probabilities": prob_dict
            },
            "explanation": explanations,
            "model": {
                "version": "V4",
                "algorithm": "Optimized XGBoost Classifier",
                "accuracy": "68.90%",
                "status": "Active (Working V4 Model)"
            }
        }

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "version": "V4",
            "name": "Road Accident Severity Predictor V4",
            "algorithm": "Optimized XGBoost Pipeline",
            "accuracy": "68.90%",
            "macro_f1": "67.45%",
            "dataset_records": 20000,
            "target_classes": ["Minor", "Major", "Fatal"],
            "features_count": len(config.FEATURE_SCHEMA),
            "status": "Operational"
        }
