from flask import Flask, request, jsonify
import os
from wildfire_report import process_wildfire_data

app = Flask(__name__)

# Store uploaded files temporarily
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Wildfire Resource Allocation API is running"}), 200


@app.route("/upload", methods=["POST"])
def upload_file():
    """Upload wildfire CSV data"""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    return jsonify({"message": "File uploaded successfully", "file_path": filepath}), 200


@app.route("/process", methods=["POST"])
def process_data():
    """Process wildfire CSV and return allocation report"""
    data = request.json
    if "file_path" not in data:
        return jsonify({"error": "File path is required"}), 400

    file_path = data["file_path"]
    result = process_wildfire_data(file_path)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
