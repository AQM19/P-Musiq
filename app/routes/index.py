from app import Config
from app.services.youtube_downloader import download_audio_mp3_from_youtube
from flask import Blueprint, render_template, request, send_file
import os

index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@index_bp.route('/download', methods=['POST'])
def download():
    youtube_link = request.form.get('youtube_link')
    if youtube_link:
        try:
            filename = download_audio_mp3_from_youtube(youtube_link)
            download_path = os.path.join(Config.DOWNLOAD_DIRECTORY, filename)
            return send_file(download_path, as_attachment=True)
        except Exception as e:
            return render_template('index.html', message=f"Error al descargar el audio")

    return render_template('index.html', message="Por favor, inserta un link a YouTube")