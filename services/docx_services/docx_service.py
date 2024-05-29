from typing import Dict
from docx import Document
from .filler import fill_data
from .extractor import extract_data
from utils.paths import storage_path
from .helpers import get_base_64_and_delete_file
from werkzeug.datastructures import FileStorage

class DocxServices:
    @staticmethod
    def extract_from_docx(file: FileStorage) -> dict:
        doc = Document(file)
        data = extract_data(doc)
        return data
    
    @staticmethod
    def fill_data_2_file(data: Dict) -> str:
        file_to_save_path = storage_path('temp.docx') 
        doc = Document(storage_path('test.docx'))

        fill_data(doc, data)
        doc.save(file_to_save_path)
        return get_base_64_and_delete_file(file_to_save_path)
