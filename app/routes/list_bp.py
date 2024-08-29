from flask import Blueprint, render_template, request, jsonify
from app.services.youtube_downloader import map_link_list
from app.enums import Paths, Endpoints, TemplateNames, Messages

list_bp = Blueprint(Paths.LIST.value, __name__)

@list_bp.route(Endpoints.LIST.value, methods=['GET'])
def list():
    return render_template(TemplateNames.LIST.value)

@list_bp.route(Endpoints.DOWNLOAD_LIST.value, methods=['POST'])
def download_list():
    items = request.json.get('items', [])
    
    if not items:
        return jsonify({"message": Messages.EMPTY_LIST_ERROR.value}), 400
    
    try:
        downloaded_files = map_link_list(items)
        return jsonify({"downloaded_files": downloaded_files, "message": Messages.DOWNLOAD_SUCCESSFULL.value}), 200
    except Exception as e:
        return jsonify({"message": f"{Messages.UNEXPECTED_ERROR.value} {str(e)}"}), 500


