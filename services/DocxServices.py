import re
import base64
import os
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.shared import Mm
from docx.oxml import parse_xml
from docx.enum.table import WD_TABLE_ALIGNMENT
from werkzeug.datastructures import FileStorage
from typing import Dict
from utils.insturctions import INSTRUCTIONS
from utils.types import TYPES
from utils.xmlStyles import border_table_style

class DocxServices:

    __TEMP_PATH = 'storage/'

    @staticmethod
    def extractFromDocx(file: FileStorage) -> dict:
        doc = Document(file)
        data = DocxServices._extractData(doc)
        return data
    
    @staticmethod
    def fillDataToFile(data: Dict) -> str:
        file_to_save_path = DocxServices.__TEMP_PATH + 'temp.docx'
        doc = Document("test.docx")

        DocxServices._fillData(doc, data)
        doc.save(file_to_save_path)
        return DocxServices._getBase64AndDeleteFile(file_to_save_path)
    
    @staticmethod
    def _fillData(doc: Document, data: Dict) -> None:
        DocxServices._setTableBorder(doc)
        for section in doc.sections:
            if(not section.page_width):
                section.page_width = Mm(300)

        for paragraph in doc.paragraphs:
            paragraph.text = DocxServices._replaceText(paragraph.text, data)
        
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    cell.text = DocxServices._replaceText(cell.text, data)

        DocxServices._fillTables(doc, data)

    @staticmethod
    def _getBase64AndDeleteFile(path: str) -> str:
        base64_string = ''
        with open(path, "rb") as image_file:
            base64_string = base64.b64encode(image_file.read())
        os.remove(path)
        return base64_string.decode('utf-8')

    @staticmethod
    def _fillTables(doc: Document, data: Dict) -> None:
        if 'tables' in data:
            for item in data['tables']:
                pattern = r'\{\{' + TYPES['tables'] + r':' + item['name'] + r':[^}]+}}'
                for paragraph in doc.paragraphs:
                    if re.search(pattern, paragraph.text):
                        DocxServices._createTable(paragraph, item, doc)
                        paragraph.clear()
    
    @staticmethod
    def _createTable(paragraph: Paragraph, item: Dict, doc) -> None:
        table = doc.add_table(rows=len(item['data']), cols=len(item['data'][0]))
        DocxServices._moveTableAfter(table, paragraph)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = True
        table.style = 'TableGrid'

        for i, row in enumerate(item['data']):
            for j, cell_txt in enumerate(row):
                table.cell(i, j).text = str(cell_txt)

    @staticmethod
    def _moveTableAfter(table: Table, paragraph: Paragraph) -> None:
        tbl, p = table._tbl, paragraph._p
        p.addnext(tbl)

    @staticmethod
    def _setTableBorder(document: Document) -> None:
        table_style = border_table_style
        document.styles.add_style('TableGrid', 3)
        style_element = parse_xml(table_style)
        document.styles._element.append(style_element)
    
    @staticmethod
    def _replaceText(text: str, data: Dict) -> str:
        for type_name, items in data.items():
            for item in items:
                placeholder = r'\{\{' + TYPES[type_name] + r':' + item['name'] + r':[^}]+}}'
                match type_name:
                    case 'logical':
                        logicalTemp = 'Да' if item['data'] else 'Нет'
                        text = re.sub(placeholder, str(item['placeholder']) + ' - ' + logicalTemp, text)
                    case 'switcher':
                        logicalTemp = '✓' if item['data'] else '☓'
                        text = re.sub(placeholder, str(item['placeholder']) + ' - ' + logicalTemp, text)
                    case 'tables':
                        pass
                    case _:
                        text = re.sub(placeholder, str(item['data']), text)

        return text

    @staticmethod
    def _extractData(doc: Document) -> dict:
        data = {
            'stroke': [],
            'number': [],
            'logical': [],
            'switcher': [],
            'tables': []
        }
        
        for paragraph in doc.paragraphs:
            DocxServices._extractFromText(paragraph.text, data)
    
        for table in doc.tables:
            DocxServices._extractFromTable(table, data)
        
        return data
    
    @staticmethod
    def _extractFromText(text: str, data: Dict) -> None:
        for type_name, instr in INSTRUCTIONS.items():
            matches = re.findall(instr['pattern'], text)
            for match in matches:
                if len(instr['attrNames']) == 1:  # Если только одно имя атрибута
                    data[type_name].append({instr['attrNames'][0]: match})
                else:                             # Если несколько имен атрибутов
                    data[type_name].append({name: value for name, value in zip(instr['attrNames'], match)})
    
    @staticmethod
    def _extractFromTable(table: Table, data: Dict) -> None:
        for row in table.rows:
            for cell in row.cells:
                DocxServices._extractFromText(cell.text, data)