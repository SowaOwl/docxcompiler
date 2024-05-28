from flask import Request
from utils.ApiRepsponse import sendError, sendSuccess
from services.docx_services.docx_service import DocxServices
import traceback

docx_services = DocxServices()

class DocxHandler:
    @staticmethod
    def extract(request: Request) -> str:
        if 'file' not in request.files:
            return sendError('No file')
        
        file = request.files['file']
        if file.filename.endswith('.docx'):
            try:
                response = docx_services.extractFromDocx(file)
                return sendSuccess('Extract data fihish sucessful', response)
            except Exception as e:
                with open("log.txt", "a") as f:
                    f.write(traceback.format_exc() + '\n')
                return sendError(str(e))
        else:
            return sendError('Invalid file format. Please upload a .docx file.')
        
    @staticmethod
    def fillFile(request: Request) -> str:
        data = request.json
        try:
            response = docx_services.fillDataToFile(data)
            if response:
                return sendSuccess('Document fill finish success', response)
            else:
                return sendError('Document fill give an error')
        except Exception as e:
            return sendError(str(e))
