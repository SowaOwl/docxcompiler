from docx import Document
import re
from utils.insturctions import INSTRUCTIONS
from utils.types import TYPES

class DocxServices:

    __INSTRUCTIONS = INSTRUCTIONS
    __TYPES = TYPES

    def __init__(self) -> None:
        pass

    def extractFromDocx(self, file):
        doc = Document(file)
        data = self._extractData(doc)
        return data
    
    def fillDataToFile(self, data):
        doc = Document("test.docx")
        self._fillData(doc, data)
        doc.save('response.docx')
        return "OK"
    
    def _fillData(self, doc, data):
        for paragraph in doc.paragraphs:
            paragraph.text = self._replaceText(paragraph.text, data)
        
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    cell.text = self._replaceText(cell.text, data)
    
    def _replaceText(self, text, data):
        for type_name, items in data.items():
            for item in items:
                placeholder = r'\{\{' + self.__TYPES[type_name] + r':' + item['name'] + r':[^}]+}}'
                if type_name == 'logical':
                    logicalTemp = 'Да' if item['data'] else 'Нет';
                    text = re.sub(placeholder, str(item['placeholder']) + ' - ' + logicalTemp, text)
                else:
                    text = re.sub(placeholder, str(item['data']), text)
                # file = open("log.txt", "a")
                # file.write(text + " | " + placeholder + '\n')
                # file.close()

        return text

    def _extractData(self, doc):
        data = {
            "stroke": [],
            "number": [],
            "logical": [],
            "switcher": [],
            "tables": []
        }
        
        for paragraph in doc.paragraphs:
            self._extractFromText(paragraph.text, data)
    
        for table in doc.tables:
            self._extractFromTable(table, data)
        
        return data

    def _extractFromText(self, text, data):
        for type_name, instr in self.__INSTRUCTIONS.items():
            matches = re.findall(instr['pattern'], text)
            for match in matches:
                if len(instr['attrNames']) == 1:  # Если только одно имя атрибута
                    data[type_name].append({instr['attrNames'][0]: match})
                else:                             # Если несколько имен атрибутов
                    data[type_name].append({name: value for name, value in zip(instr['attrNames'], match)})
    
    def _extractFromTable(self, table, data):
        for row in table.rows:
            for cell in row.cells:
                self.__extractFromText(cell.text, data)