from flask import Blueprint, render_template, request, jsonify
from app.services.youtube_downloader import download_audio_mp3_from_youtube
from app.enums import Paths, Endpoints, TemplateNames, Messages

list_bp = Blueprint(Paths.LIST.value, __name__)

@list_bp.route(Endpoints.LIST.value, methods=['GET'])
def list():
    return render_template(TemplateNames.LIST.value)

@list_bp.route(Endpoints.DOWNLOAD_LIST.value, methods=['POST'])
def download_list():
    youtube_link = request.json.get('item')

    if youtube_link:
        try:
            return download_audio_mp3_from_youtube(youtube_link)
        except Exception as e:
            return jsonify({"message": f"{Messages.DOWNLOAD_ERROR.value} {str(e)}"}), 500
        
    return render_template(TemplateNames.INDEX.value, message=Messages.YOUTUBE_LINK_ERROR.value)


