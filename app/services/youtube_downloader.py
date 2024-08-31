from app.enums import FileExtension, Messages
from app.models import Config
from app.utils.utils import clean_file_name
from flask import send_file, jsonify
from pytube import YouTube
import logging
import os

def _get_youtube_video(url):
    """Obtiene el objeto YouTube para un URL dado."""
    return YouTube(url)

def _create_filename(yt, extension = FileExtension.MP3.value):
    """Crea un nombre de archivo basado en el título del video."""
    cleaned_name = clean_file_name(yt.title)
    return f"{cleaned_name}.{extension}"

def _download_video_stream(yt, filename, temp_dir):
    """Descarga el flujo de video de YouTube en el directorio temporal"""
    video_stream = yt.streams.filter(file_extension=FileExtension.MP4.value, progressive=True).get_highest_resolution()
    temp_file_path = os.path.join(temp_dir, filename)
    video_stream.download(output_path=temp_dir, filename=filename)
    return temp_file_path

def _download_audio_stream(yt, filename, temp_dir):
    """Descarga el flujo de audio del video de YouTube en el directorio temporal."""
    audio_stream = yt.streams.filter(only_audio=True).first()
    temp_file_path = os.path.join(temp_dir, filename)
    audio_stream.download(output_path=temp_dir, filename=filename)
    return temp_file_path

def download_audio_mp3_from_youtube(url):
    """Descarga un archivo de audio MP3 de YouTube y lo envía como respuesta."""
    try:
        yt = _get_youtube_video(url)
        filename = _create_filename(yt)
        temp_dir = Config.TEMPORARY_DIRECTORY
        
        temp_file_path = _download_audio_stream(yt, filename, temp_dir)
        logging.info(f"{Messages.DOWNLOAD_SUCCESSFULL.value} {filename}")
        
        response = send_file(temp_file_path, as_attachment=True, download_name=filename)

        os.remove(temp_file_path)

        return response
    
    except Exception as e:
        logging.error(f"{Messages.DOWNLOAD_ERROR.value} {url}: {str(e)}")
        return jsonify({'error': 'Error al procesar la solicitud'}), 500

def download_video_mp4_from_youtube(url):
    """Deacarga un archivo de video MP4 de YouTube y lo envía como respuesta"""
    try:
        yt = _get_youtube_video(url)
        filename = _create_filename(yt, extension=FileExtension.MP4.value)
        temp_dir = Config.TEMPORARY_DIRECTORY

        temp_file_path = _download_video_stream(yt, filename, temp_dir)
        logging.info(f"{Messages.DOWNLOAD_SUCCESSFULL.value} {filename}")

        response = send_file(temp_file_path, as_attachment=True, download_name=filename)

        os.remove(temp_file_path)

        return response
    except Exception as e:
        logging.error(f"{Messages.DOWNLOAD_ERROR.value} {url}: {str(e)}")
        return jsonify({'error': 'Error al procesar la solicitud'}), 500


def map_link_list(links):
    """Descarga archivos MP3 para una lista de enlaces de YouTube y maneja errores."""
    downloaded_files = []
    for link in links:
        try:
            response = download_audio_mp3_from_youtube(link)
            if hasattr(response, 'filename'):
                downloaded_files.append(response.filename)
        except Exception as e:
            logging.error(f"{Messages.DOWNLOAD_ERROR.value} {link}: {str(e)}")
    return downloaded_files
