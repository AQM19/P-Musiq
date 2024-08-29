from enum import Enum

class Messages(Enum):
    DOWNLOAD_ERROR = 'Error al descargar el audio'
    YOUTUBE_LINK_ERROR = 'Por favor, inserta un link a YouTube'
    EMPTY_LIST_ERROR = 'La lista está vacía'
    UNEXPECTED_ERROR = 'Ha ocurrido un error inesperado: '
    DOWNLOAD_SUCCESSFULL = 'Descarga completada con éxito'