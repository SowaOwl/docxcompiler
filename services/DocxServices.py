from docx import Document
from docx.shared import Mm
from docx.oxml import parse_xml
from docx.enum.table import WD_TABLE_ALIGNMENT
import re
from utils.insturctions import INSTRUCTIONS
from utils.types import TYPES
from utils.xmlStyles import border_table_style

class DocxServices:

    __INSTRUCTIONS = INSTRUCTIONS
    __TYPES = TYPES
    
    def extractFromDocx(self, file) -> dict:
        doc = Document(file)
        data = self._extractData(doc)
        return data
    
    def fillDataToFile(self, data) -> True:
        doc = Document("test.docx")
        self._fillData(doc, data)
        doc.save('response.docx')
        return True
    
    def _fillData(self, doc, data) -> None:
        self._setTableBorder(doc)
        for section in doc.sections:
            if(not section.page_width):
                section.page_width = Mm(300)

        for paragraph in doc.paragraphs:
            paragraph.text = self._replaceText(paragraph.text, data)
        
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    cell.text = self._replaceText(cell.text, data)

        self._fillTables(doc, data)

    def _fillTables(self, doc, data) -> None:
        if 'tables' in data:
            for item in data['tables']:
                pattern = r'\{\{' + self.__TYPES['tables'] + r':' + item['name'] + r':[^}]+}}'
                for paragraph in doc.paragraphs:
                    if re.search(pattern, paragraph.text):
                        self._createTable(paragraph, item, doc)
                        paragraph.clear()
    
    def _createTable(self, paragraph, item, doc) -> None:
        table = doc.add_table(rows=len(item['data']), cols=len(item['data'][0]))
        self._moveTableAfter(table, paragraph)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = True
        table.style = 'TableGrid'

        for i, row in enumerate(item['data']):
            for j, cell_txt in enumerate(row):
                table.cell(i, j).text = str(cell_txt)

    def _moveTableAfter(self ,table, paragraph) -> None:
        tbl, p = table._tbl, paragraph._p
        p.addnext(tbl)

    def _setTableBorder(self, document) -> None:
        table_style = border_table_style
        document.styles.add_style('TableGrid', 3)
        style_element = parse_xml(table_style)
        document.styles._element.append(style_element)
    
    def _replaceText(self, text, data) -> str:
        for type_name, items in data.items():
            for item in items:
                placeholder = r'\{\{' + self.__TYPES[type_name] + r':' + item['name'] + r':[^}]+}}'
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

    def _extractData(self, doc) -> dict:
        data = {
            'stroke': [],
            'number': [],
            'logical': [],
            'switcher': [],
            'tables': []
        }
        
        for paragraph in doc.paragraphs:
            self._extractFromText(paragraph.text, data)
    
        for table in doc.tables:
            self._extractFromTable(table, data)
        
        return data

    def _extractFromText(self, text, data) -> None:
        for type_name, instr in self.__INSTRUCTIONS.items():
            matches = re.findall(instr['pattern'], text)
            for match in matches:
                if len(instr['attrNames']) == 1:  # Если только одно имя атрибута
                    data[type_name].append({instr['attrNames'][0]: match})
                else:                             # Если несколько имен атрибутов
                    data[type_name].append({name: value for name, value in zip(instr['attrNames'], match)})
    
    def _extractFromTable(self, table, data) -> None:
        for row in table.rows:
            for cell in row.cells:
                self._extractFromText(cell.text, data)