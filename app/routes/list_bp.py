from flask import Blueprint, render_template, request, jsonify
from app.services.youtube_downloader import map_link_list

list_bp = Blueprint('list', __name__)

@list_bp.route('/list', methods=['GET'])
def list():
    return render_template('list.html')

@list_bp.route('/download-list', methods=['POST'])
def download_list():
    items = request.json.get('items', [])
    
    if not items:
        return jsonify({"message": "List provided is empty"}), 400
    
    try:
        downloaded_files = map_link_list(items)
        return jsonify({"downloaded_files": downloaded_files, "message": "Download completed successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


