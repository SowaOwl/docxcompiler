from docx import Document
import re
from utils.insturctions import INSTRUCTIONS

class DocxServices:

    __INSTRUCTIONS = INSTRUCTIONS

    def __init__(self) -> None:
        pass

    def extractFromDocx(self, file):
        doc = Document(file)
        data = self.__extractData(doc)
        return data

    def __extractData(self, doc):
        data = {
            "stroke": [],
            "number": [],
            "logical": [],
            "switcher": [],
            "tables": []
        }
        
        for paragraph in doc.paragraphs:
            self.__extractFromText(paragraph.text, data)
    
        for table in doc.tables:
            self.__extractFromTable(table, data)
        
        return data

    def __extractFromText(self, text, data):
        for type_name, instr in self.__INSTRUCTIONS.items():
            matches = re.findall(instr['pattern'], text)
            for match in matches:
                if len(instr['attrNames']) == 1:  # Если только одно имя атрибута
                    data[type_name].append({instr['attrNames'][0]: match})
                else:                             # Если несколько имен атрибутов
                    data[type_name].append({name: value for name, value in zip(instr['attrNames'], match)})
    
    def __extractFromTable(self, table, data):
        for row in table.row:
            for cell in row.cell:
                self.__extractFromText