from app.enums import Paths, Endpoints, TemplateNames, Messages
from app.services.youtube_downloader import download_audio_mp3_from_youtube
from flask import Blueprint, render_template, request

index_bp = Blueprint(Paths.INDEX.value, __name__)

@index_bp.route(Endpoints.BASE.value, methods=['GET'])
def index():
    return render_template(TemplateNames.INDEX.value)

@index_bp.route(Endpoints.DOWNLOAD.value, methods=['POST'])
def download():
    youtube_link = request.form.get('youtube_link')
    if youtube_link:
        try:
            return download_audio_mp3_from_youtube(youtube_link)
        except Exception:
            return render_template(TemplateNames.INDEX.value, message=Messages.DOWNLOAD_ERROR.value)

    return render_template(TemplateNames.INDEX.value, message=Messages.YOUTUBE_LINK_ERROR.value)