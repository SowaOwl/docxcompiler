from services.DocxServices import DocxServices

docx_services = DocxServices()

class DocxHandler:

    def __init__(self) -> None:
        pass

    def extract(self, file):
        return docx_services.extractFromDocx(file)