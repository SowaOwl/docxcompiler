from flask import Flask, Blueprint, request
from handlers.DocxHandler import DocxHandler
from handlers.WelcomeHandler import WelcomeHandler

docx_handler = DocxHandler()
welcome_handler = WelcomeHandler()
app = Flask(__name__, template_folder='public/views')
api = Blueprint('api', __name__, url_prefix='/api')

@app.route('/', methods=['GET'])
def index() -> str:
    return welcome_handler.welcome()

# Api routes
@api.route('/extract', methods=['POST'])
def extract() -> str:
    return docx_handler.extract(request)
    
@api.route('/fill-file', methods=['POST'])
def fill_file() -> str:
    return docx_handler.fill_file(request)

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)