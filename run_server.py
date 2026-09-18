import sys
import os

# Ensure backend directory is in python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import app
import backend.config as config

if __name__ == "__main__":
    print("================================================================")
    print(" EXPLAINABLE AI ACCIDENT SEVERITY FRAMEWORK - FLASK BACKEND")
    print(f" Active Model Version : {config.ACTIVE_MODEL_VERSION}")
    print(f" V4 Model Path       : {config.V4_MODEL_PATH}")
    print(f" Listening on        : http://{config.HOST}:{config.PORT}")
    print("================================================================")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
