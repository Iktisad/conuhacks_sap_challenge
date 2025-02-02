import os
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from app.utils import process_wildfire_data, load_wildfire_data, save_uploaded_files,train_fire_model, load_environmental_data,predict_wildfire


wildfire_routes = Blueprint("wildfire_routes", __name__)

# Apply CORS to the Blueprint
CORS(wildfire_routes)

# Directory to store uploaded files
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@wildfire_routes.route("/data/load_data", methods=["POST"])
def load_data():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Load data into the system
    load_wildfire_data(file_path)

    return jsonify({"message": "File uploaded successfully", "file_path": file_path})


@wildfire_routes.route("/optimize_response", methods=["GET"])
def optimize_response():
    file_path = request.args.get("file")

    if not file_path:
        return jsonify({"error": "File path is required"}), 400

    # Process the uploaded file
    result = process_wildfire_data(file_path)

    return jsonify(result)

@wildfire_routes.route("/upload", methods=["POST"])
def upload_data():
    try:
        env_file = request.files.get("env_file")
        fire_file = request.files.get("fire_file")
        future_env_file = request.files.get("future_env_file")

        if not env_file or not fire_file or not future_env_file:
            return jsonify({"error": "Missing one or more files"}), 400

        # Save files using utility function
        file_paths = save_uploaded_files(env_file, fire_file, future_env_file)

        return jsonify({"message": "Files uploaded successfully", "paths": file_paths})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wildfire_routes.route("/", methods=["POST"])
def train_model():
    try:
        env_file = request.json.get("env_file")
        fire_file = request.json.get("fire_file")
        future_env_file = request.json.get("future_env_file")

        if not env_file or not fire_file or not future_env_file:
            return jsonify({"error": "File paths are required"}), 400

        historical_env_data, future_env_data = load_environmental_data(env_file, fire_file, future_env_file)
        result = train_fire_model(historical_env_data)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@wildfire_routes.route("/predict", methods=["POST"])
def predict():
    try:
        future_env_file = request.json.get("future_env_file")

        if not future_env_file:
            return jsonify({"error": "Future environment file path is required"}), 400

        predictions = predict_wildfire(future_env_file)

        return jsonify({"predictions": predictions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500