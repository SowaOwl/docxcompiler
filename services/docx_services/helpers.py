from os import remove
from subprocess import run
from base64 import b64encode
from utils.paths import storagePath

def getBase64AndDeleteFile(path: str) -> str:
    base64_string = ''
    pdf_path = storagePath('temp.pdf')
    command = ['libreoffice', '--headless', '--convert-to', 'pdf', path, '--outdir', storagePath('')]
    run(command, check=True)
    
    with open(pdf_path, 'rb') as file:
        base64_string = b64encode(file.read())
        
    remove(path)
    remove(pdf_path)
    
    return base64_string.decode('utf-8')