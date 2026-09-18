import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import backend.config as config
from backend.model_service import model_service

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)  # Enable Cross-Origin Resource Sharing for dev environment

# Serve Frontend SPA
@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

# API Endpoints
@app.route("/api/health", methods=["GET"])
def health_check():
    metadata = model_service.get_metadata()
    return jsonify({
        "status": "online",
        "active_model": metadata.get("version", "V4"),
        "model_accuracy": metadata.get("accuracy", "68.90%"),
        "message": "Explainable AI Accident Severity Prediction Framework API is running."
    }), 200

@app.route("/api/features", methods=["GET"])
def get_feature_schema():
    return jsonify({
        "success": True,
        "features": config.FEATURE_SCHEMA
    }), 200

@app.route("/api/model-info", methods=["GET"])
def get_model_info():
    metadata = model_service.get_metadata()
    return jsonify({
        "success": True,
        "model": metadata
    }), 200

@app.route("/api/predict", methods=["POST"])
def predict_accident_severity():
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({
                "success": False,
                "error": "Invalid request. Expected JSON payload."
            }), 400

        # Support both {"features": {...}} and flat {...} JSON payloads
        features = data.get("features", data)
        if not isinstance(features, dict):
            return jsonify({
                "success": False,
                "error": "'features' must be a dictionary object."
            }), 400

        # Perform prediction via Model Service
        result = model_service.predict(features)
        return jsonify(result), 200

    except Exception as e:
        print(f"Error processing prediction request: {e}")
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred while processing the prediction request."
        }), 500

if __name__ == "__main__":
    print(f"Starting Flask Server on http://{config.HOST}:{config.PORT}")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
