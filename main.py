from flask import Flask, render_template, request, send_file
from pathlib import Path
from pytube import YouTube
import os
import re

app = Flask(__name__)

HOME_DIRECTORY = Path.home()
DOWNLOAD_DIRECTORY = HOME_DIRECTORY / "Downloads"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    youtube_link = request.form.get('youtube_link')
    if youtube_link:
        try:
            filename = download_audio_mp3_from_youtube(youtube_link)
            download_path = os.path.join(DOWNLOAD_DIRECTORY, filename)
            return send_file(download_path, as_attachment=True)
        except Exception as e:
            return render_template('index.html', message=f"Error downloading audio: {e}")
    else:
        return render_template('index.html', message="Please provide a YouTube link.")

def download_audio_mp3_from_youtube(url):
    yt = YouTube(url)
    claned_name = clean_file_name(yt.title)
    audio_stream = yt.streams.filter(only_audio=True).first()
    filename = f"{claned_name}.mp3"
    DOWNLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    audio_stream.download(output_path=DOWNLOAD_DIRECTORY, filename=filename)
    return filename

def clean_file_name(name):
    cleaned_name = re.sub(r'[\/:*?"<>|]', '_', name)
    cleaned_name = cleaned_name.strip()
    return cleaned_name 

if __name__ == '__main__':
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    debug = os.getenv('DEBUG_MODE')
    
    app.run(host, port, debug)