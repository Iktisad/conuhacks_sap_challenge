import os
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from app.utils import process_wildfire_data, load_wildfire_data

wildfire_routes = Blueprint("wildfire_routes", __name__)

# Apply CORS to the Blueprint
CORS(wildfire_routes)

# Directory to store uploaded files
UPLOAD_FOLDER = "data"
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
