from re import findall
from typing import Dict
from docx import Document
from docx.table import Table
from utils.paths import storagePath
from utils.insturctions import INSTRUCTIONS

def extractData(doc: Document) -> dict:
    data = {
        'stroke': [],
        'number': [],
        'logical': [],
        'switcher': [],
        'tables': []
    }
    
    for paragraph in doc.paragraphs:
        _extractFromText(paragraph.text, data)

    for table in doc.tables:
        _extractFromTable(table, data)
    
    doc.save(storagePath('test.docx'))

    return data

def _extractFromText(text: str, data: Dict) -> None:
    for type_name, instr in INSTRUCTIONS.items():
        matches = findall(instr['pattern'], text)
        for match in matches:
            if any(item['name'] == match[0] for item in data[type_name]):
                continue
            else:
                if len(instr['attrNames']) == 1:
                    data[type_name].append({instr['attrNames'][0]: match})
                else:
                    data[type_name].append({name: value for name, value in zip(instr['attrNames'], match)})

def _extractFromTable(table: Table, data: Dict) -> None:
    for row in table.rows:
        for cell in row.cells:
            _extractFromText(cell.text, data)