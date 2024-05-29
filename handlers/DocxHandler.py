from flask import Request
from utils.ApiRepsponse import send_error, send_success
from services.docx_services.docx_service import DocxServices
import traceback

docx_services = DocxServices()

class DocxHandler:
    @staticmethod
    def extract(request: Request) -> str:
        if 'file' not in request.files:
            return send_error('No file')
        
        file = request.files['file']
        if file.filename.endswith('.docx'):
            try:
                response = docx_services.extract_from_docx(file)
                return send_success('Extract data fihish sucessful', response)
            except Exception as e:
                with open("log.txt", "a") as f:
                    f.write(traceback.format_exc() + '\n')
                return send_error(str(e))
        else:
            return send_error('Invalid file format. Please upload a .docx file.')
        
    @staticmethod
    def fill_file(request: Request) -> str:
        data = request.json
        try:
            response = docx_services.fill_data_2_file(data)
            if response:
                return send_success('Document fill finish success', response)
            else:
                return send_error('Document fill give an error')
        except Exception as e:
            return send_error(str(e))
