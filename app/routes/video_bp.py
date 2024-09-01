from flask import Blueprint, render_template, request
from app.enums import Paths, Endpoints, TemplateNames, Messages
from app.services import download_video_mp4_from_youtube

video_bp = Blueprint(Paths.VIDEO_DOWNLOADER.value, __name__)

@video_bp.route(Endpoints.VIDEO.value, methods=['GET'])
def video():
    return render_template(TemplateNames.VIDEO.value)

@video_bp.route(Endpoints.VIDEO_DOWNLOAD.value, methods=['POST'])
def download():
    youtube_link = request.form.get('youtube_link')
    if youtube_link:
        try:
            return download_video_mp4_from_youtube(youtube_link)
        except Exception:
            return render_template(TemplateNames.VIDEO.value, message=Messages.DOWNLOAD_ERROR.value)

    return render_template(TemplateNames.VIDEO.value, message=Messages.YOUTUBE_LINK_ERROR.value)