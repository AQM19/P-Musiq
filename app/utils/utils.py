import re

def clean_file_name(name) -> str:
    """Formatea un string con la expresión regular definida"""
    cleaned_name = re.sub(r'[\/:*?"<>|]', '_', name)
    cleaned_name = cleaned_name.strip()
    return cleaned_name