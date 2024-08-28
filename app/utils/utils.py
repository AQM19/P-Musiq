import re

def clean_file_name(name):
    cleaned_name = re.sub(r'[\/:*?"<>|]', '_', name)
    cleaned_name = cleaned_name.strip()
    return cleaned_name