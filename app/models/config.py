import os
from pathlib import Path

HOME_DIRECTORY = Path.home()
DOWNLOAD_DIRECTORY = HOME_DIRECTORY / "Downloads"

class Config:
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't')
    DOWNLOAD_DIRECTORY = DOWNLOAD_DIRECTORY