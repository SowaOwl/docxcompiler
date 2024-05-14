from services.DocxServices import DocxServices
from flask import jsonify
import json

docx_services = DocxServices()

class DocxHandler:

    def __init__(self) -> None:
        pass

    def extract(self, request):
        if 'file' not in request.files:
            return jsonify({"error": "No file"})
        
        file = request.files['file']
        if file.filename.endswith('.docx'):
            try:
                return jsonify(docx_services.extractFromDocx(file))
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"error": "Invalid file format. Please upload a .docx file."})
        
    def fillFile(self, request):
        data = request.json
        try:
            return jsonify(docx_services.fillDataToFile(data))
        except Exception as e:
            return jsonify({"error": str(e)})
