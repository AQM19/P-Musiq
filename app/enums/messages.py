from enum import Enum

class Messages(Enum):
    DOWNLOAD_ERROR = 'Error al descargar el audio'
    DOWNLOAD_SUCCESSFULL = 'Descarga completada con éxito'
    EMPTY_LIST_ERROR = 'La lista está vacía'
    UNEXPECTED_ERROR = 'Ha ocurrido un error inesperado: '
    YOUTUBE_LINK_ERROR = 'Por favor, inserta un link a YouTube'