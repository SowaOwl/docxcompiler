from typing import Dict
from docx import Document
from .filler import fillData
from .extractor import extractData
from utils.paths import storagePath
from .helpers import getBase64AndDeleteFile
from werkzeug.datastructures import FileStorage

class DocxServices:
    @staticmethod
    def extractFromDocx(file: FileStorage) -> dict:
        doc = Document(file)
        data = extractData(doc)
        return data
    
    @staticmethod
    def fillDataToFile(data: Dict) -> str:
        file_to_save_path = storagePath('temp.docx') 
        doc = Document(storagePath('test.docx'))

        fillData(doc, data)
        doc.save(file_to_save_path)
        return getBase64AndDeleteFile(file_to_save_path)
