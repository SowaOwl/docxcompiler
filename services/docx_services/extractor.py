from re import findall
from typing import Dict
from docx import Document
from docx.table import Table
from utils.paths import storagePath
from .helpers import translitKir2Lat
from utils.insturctions import INSTRUCTIONS, DEFAULT_VALUES, TYPES

def extractData(doc: Document) -> dict:
    data = {key: [] for key in TYPES.keys()}
    
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
            name = match if len(instr['attrNames']) == 1 else match[0]
            type_array = data[instr['parrentName']] if 'parrentName' in instr else data[type_name]

            if any(item['name'] == name for item in type_array):
                continue
            else:
                match type_name:
                    case 'alt_stroke':
                        def_values = DEFAULT_VALUES.copy()
                        def_values['placeholder'] = match
                        def_values['name'] = translitKir2Lat(match)
                        data[instr['parrentName']].append(
                                {attr: def_values[attr] for attr in INSTRUCTIONS['stroke']['attrNames'] if attr in def_values}
                            )
                    case _:
                        if len(instr['attrNames']) == 1:
                            data[type_name].append({instr['attrNames'][0]: match})
                        else:
                            data[type_name].append({name: value for name, value in zip(instr['attrNames'], match)})
                
def _extractFromTable(table: Table, data: Dict) -> None:
    for row in table.rows:
        for cell in row.cells:
            _extractFromText(cell.text, data)