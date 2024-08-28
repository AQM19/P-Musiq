from pytube import YouTube
from app.utils.utils import clean_file_name
from flask import current_app

def download_audio_mp3_from_youtube(url):
    yt = YouTube(url)
    cleaned_name = clean_file_name(yt.title)
    audio_stream = yt.streams.filter(only_audio=True).first()
    filename = f"{cleaned_name}.mp3"
    
    download_dir = current_app.config['DOWNLOAD_DIRECTORY']
    download_dir.mkdir(parents=True, exist_ok=True)
    
    audio_stream.download(output_path=str(download_dir), filename=filename)
    return filename
