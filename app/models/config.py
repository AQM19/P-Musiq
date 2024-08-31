import os
import tempfile

class Config:
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't')
    TEMPORARY_DIRECTORY = tempfile.gettempdir()