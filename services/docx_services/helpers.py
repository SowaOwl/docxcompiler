from os import remove
from subprocess import run
from base64 import b64encode
from transliterate import translit
from utils.paths import storage_path

def get_base_64_and_delete_file(path: str) -> str:
    base64_string = ''
    pdf_path = storage_path('temp.pdf')
    command = ['libreoffice', '--headless', '--convert-to', 'pdf', path, '--outdir', storage_path('')]
    run(command, check=True)
    
    with open(pdf_path, 'rb') as file:
        base64_string = b64encode(file.read())
        
    remove(path)
    remove(pdf_path)
    
    return base64_string.decode('utf-8')

def translitkir_2_lat(text: str) -> str:
    text = translit(text, 'ru', reversed=True)
    text = text.lower()
    text = text.replace(' ', '_')
    return text