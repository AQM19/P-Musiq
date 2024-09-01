from tests import *
from unittest.mock import patch, MagicMock
from app.services.youtube_downloader import get_youtube_video, create_filename, download_audio_stream, download_audio_mp3_from_youtube, download_video_mp4_from_youtube, map_link_list

def test_get_youtube_video():
    with patch('app.services.youtube_downloader.YouTube') as mock_youtube:
        yt = get_youtube_video(VALID_LINK)
        
        mock_youtube.assert_called_once_with(VALID_LINK)
        assert yt == mock_youtube.return_value

def test_create_filename():
    mock_yt = MagicMock()
    mock_yt.title = "Test Video"
    
    filename = create_filename(mock_yt)
    
    assert filename == "Test Video.mp3"

def test_download_audio_stream():
    mock_yt = MagicMock()
    mock_stream = MagicMock()
    mock_yt.streams.filter.return_value.first.return_value = mock_stream
    
    with patch('app.services.youtube_downloader.os.path.join', return_value="/tmp/fakepath/file.mp3"):
        temp_file_path = download_audio_stream(mock_yt, "file.mp3", "/tmp/fakepath")
    
    mock_yt.streams.filter.assert_called_once_with(only_audio=True)
    mock_stream.download.assert_called_once_with(output_path="/tmp/fakepath", filename="file.mp3")
    assert temp_file_path == "/tmp/fakepath/file.mp3"

def test_download_audio_mp3_from_youtube():
    url = VALID_LINK
    mock_response = MagicMock()
    
    with patch('app.services.youtube_downloader.get_youtube_video') as mock_get_youtube, \
            patch('app.services.youtube_downloader.create_filename', return_value="test.mp3"), \
            patch('app.services.youtube_downloader.download_audio_stream', return_value="/tmp/test.mp3"), \
            patch('app.services.youtube_downloader.send_file', return_value=mock_response), \
            patch('app.services.youtube_downloader.os.remove') as mock_os_remove:
        
        response = download_audio_mp3_from_youtube(url)
        
        mock_get_youtube.assert_called_once_with(url)
        mock_os_remove.assert_called_once_with("/tmp/test.mp3")
        assert response == mock_response
    
def test_download_video_mp4_from_youtube():
    url = VALID_LINK
    mock_response = MagicMock()
    
    with patch('app.services.youtube_downloader.get_youtube_video') as mock_get_youtube, \
            patch('app.services.youtube_downloader.create_filename', return_value="test.mp4"), \
            patch('app.services.youtube_downloader.download_video_stream', return_value="/tmp/test.mp4"), \
            patch('app.services.youtube_downloader.send_file', return_value=mock_response), \
            patch('app.services.youtube_downloader.os.remove') as mock_os_remove:
        
        response = download_video_mp4_from_youtube(url)
        
        mock_get_youtube.assert_called_once_with(url)
        mock_os_remove.assert_called_once_with("/tmp/test.mp4")
        assert response == mock_response

def test_map_link_list():
    links = [VALID_LINK, VALID_LINK]
    
    mock_response = MagicMock()
    mock_response.filename = "test.mp3"
    
    with patch('app.services.youtube_downloader.download_audio_mp3_from_youtube', return_value=mock_response):
        downloaded_files = map_link_list(links)
    
    assert downloaded_files == ["test.mp3", "test.mp3"]