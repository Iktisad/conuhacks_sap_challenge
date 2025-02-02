from flask import Blueprint, jsonify, request
from app.utils import process_wildfire_data, load_wildfire_data

wildfire_routes = Blueprint('wildfire_routes', __name__)

@wildfire_routes.route('/optimize_response', methods=['GET'])
def optimize_response():
    file_path = request.args.get("file", "data/current_wildfiredata.csv")
    result = process_wildfire_data(file_path)
    return jsonify(result)

@wildfire_routes.route('/data/load_data', methods=['POST'])
def load_data():
    data = request.get_json()
    file_path = data.get("file_path", "data/current_wildfiredata.csv")
    load_wildfire_data(file_path)
    return jsonify({"message": "Data successfully loaded", "file": file_path})