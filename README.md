# Inicio de proyecto

## Instalación
```bash
phython3 -m venv .venv
source ./.venv/bin/activate
```

Presionar `F1` y escribir `Seleccionar intérprete` y seleccionar el entorno virtual ya creado.

```bash
pip install -r requirements.txt
```

## Creación del requirements.txt
```bash
pip freeze > requirements.txt
```

## Creación de las variables de entorno
Copiar el archivo `.env.template` que tiene las variables de entorno por defecto y nombrarlo como `.env`

## Ejecución
Abrir el archivo `main.py` y darle a iniciar, abrirá un servidor alojado localmente en el puerto 5000.
Lo suficientemente ligero como para poder ejecutarlo en una raspberry pi.

## Pytube 15.0.0
La libreria pytube tiene un bug en la versión 15.0.0 tras un cambio en los archivos de YouTube
Basta con pulsar `Ctrl + P` y buscar `cipher.py`
Una vez en el archivo buscar la línea 264 que debería corresponder con el inicio de la variable `function_patterns`
Reemplazar dicha función por esta otra:

```py
function_patterns = [
    # https://github.com/ytdl-org/youtube-dl/issues/29326#issuecomment-865985377
    # https://github.com/yt-dlp/yt-dlp/commit/48416bc4a8f1d5ff07d5977659cb8ece7640dcd8
    # var Bpa = [iha];
    # ...
    # a.C && (b = a.get("n")) && (b = Bpa[0](b), a.set("n", b),
    # Bpa.length || iha("")) }};
    # In the above case, `iha` is the relevant function name
    r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
    r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
    r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
```

Esto a día de hoy funciona. En algún momento se actualizará la librería.
De momento no se ha conseguido descargar música en extensión `mp3`

# Cosas por hacer

-   Mejora de la lógica de la página principal
-   Añadir un loader general
-   Añadir nueva página para descarga de vídeos en formato .mp4
-   Mejora de los estilos responsive