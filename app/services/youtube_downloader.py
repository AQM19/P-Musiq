from pytube import YouTube
from app.utils.utils import clean_file_name
from flask import current_app
import logging
from app.enums import FileExtension, Messages

def download_audio_mp3_from_youtube(url):
    try:
        yt = YouTube(url)
        cleaned_name = clean_file_name(yt.title)
        audio_stream = yt.streams.filter(only_audio=True).first()
        filename = f"{cleaned_name}{FileExtension.MP3.value}"

        download_dir = current_app.config['DOWNLOAD_DIRECTORY']
        download_dir.mkdir(parents=True, exist_ok=True)
        
        audio_stream.download(output_path=str(download_dir), filename=filename)
        logging.info(f"{Messages.DOWNLOAD_SUCCESSFULL.value} {filename}")
        return filename
    except Exception as e:
        logging.error(f"{Messages.DOWNLOAD_ERROR.value} {url}: {str(e)}")
        raise

def map_link_list(links):
    downloaded_files = []
    for link in links:
        try:
            filename = download_audio_mp3_from_youtube(link)
            downloaded_files.append(filename)
        except Exception as e:
            logging.error(f"{Messages.DOWNLOAD_ERROR.value} {link}: {str(e)}")
    return downloaded_files

