from flask import Flask, render_template, request, send_file
import re
from pytube import YouTube
import os
from pathlib import Path

app = Flask(__name__)

# Set the download directory generically to the user's "Downloads" folder
home_directory = Path.home()
downloads_directory = home_directory / "Downloads"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    youtube_link = request.form.get('youtube_link')
    if youtube_link:
        try:
            # Download the MP3 file
            filename = download_audio_mp3_from_youtube(youtube_link)
            # Send the file back to the user
            return send_file(os.path.join(downloads_directory, filename), as_attachment=True)
        except Exception as e:
            return render_template('index.html', message=f"Error downloading audio: {e}")
    else:
        return render_template('index.html', message="Please provide a YouTube link.")

def download_audio_mp3_from_youtube(url):
    yt = YouTube(url)
    claned_name = clean_file_name(yt.title)
    audio_stream = yt.streams.filter(only_audio=True).first()
    filename = f"{claned_name}.mp3"
    downloads_directory.mkdir(parents=True, exist_ok=True)
    audio_stream.download(output_path=downloads_directory, filename=filename)
    return filename

def clean_file_name(name):
    cleaned_name = re.sub(r'[\/:*?"<>|]', '_', name)
    cleaned_name = cleaned_name.strip()
    return cleaned_name 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)